"""
Проверка стратегий ВВЕРХ/ВНИЗ на реальных котировках (Yahoo Finance).

Запуск:  python research/backtest.py
Для каждой пары, таймфрейма, стратегии и экспирации считает:
  сделок, процент угаданных, 95% доверительный интервал и итог в ставках
  при выплате PAYOUT (выигрыш +PAYOUT, проигрыш -1, ничья 0).
Безубыточность при выплате 85%: 1 / 1.85 = 54.05% угаданных.
"""

import math
import sys

import numpy as np
import pandas as pd
import yfinance as yf

PAYOUT = 0.85
BREAKEVEN = 1 / (1 + PAYOUT)
PAIRS = ["EURUSD=X", "GBPUSD=X", "JPY=X", "AUDUSD=X", "EURJPY=X", "BTC-USD"]
TIMEFRAMES = {"1m": "7d", "5m": "60d"}
EXPIRIES = (1, 3, 5)


def load(ticker: str, interval: str, period: str) -> pd.DataFrame:
    df = yf.Ticker(ticker).history(interval=interval, period=period)
    return df[["Open", "High", "Low", "Close"]].dropna()


def indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    c = df["Close"]
    d = c.diff()
    gain = d.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean()
    loss = (-d.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
    df["rsi"] = 100 - 100 / (1 + gain / loss.replace(0, np.nan))
    mid, std = c.rolling(20).mean(), c.rolling(20).std()
    df["bb_up"], df["bb_low"] = mid + 2 * std, mid - 2 * std
    df["ema9"] = c.ewm(span=9, adjust=False).mean()
    df["ema21"] = c.ewm(span=21, adjust=False).mean()
    df["ret"] = c.diff()
    return df.dropna()


# Каждая стратегия возвращает +1 (ВВЕРХ), -1 (ВНИЗ) или 0 (нет сделки) на каждой свече.
def s_rsi_bb(df):
    up = (df["rsi"] < 30) & (df["Close"] < df["bb_low"])
    dn = (df["rsi"] > 70) & (df["Close"] > df["bb_up"])
    return up.astype(int) - dn.astype(int)


def s_ema_trend(df):
    return np.sign(df["ema9"] - df["ema21"]).astype(int)


def s_ema_cross(df):
    side = np.sign(df["ema9"] - df["ema21"])
    return (side * (side != side.shift())).fillna(0).astype(int)


def s_momentum(df):
    return np.sign(df["ret"]).astype(int)


def s_reversal(df):
    return -np.sign(df["ret"]).astype(int)


def s_three_candles(df):
    s = np.sign(df["ret"])
    three = s.rolling(3).sum()
    return (-(three == 3).astype(int) + (three == -3).astype(int))


def s_random(df):
    rng = np.random.default_rng(42)
    return pd.Series(rng.choice([-1, 1], len(df)), index=df.index)


STRATEGIES = {
    "RSI+Боллинджер (как в app.py)": s_rsi_bb,
    "Тренд EMA9/21": s_ema_trend,
    "Пересечение EMA": s_ema_cross,
    "Импульс (за прошлой свечой)": s_momentum,
    "Разворот (против свечи)": s_reversal,
    "3 свечи подряд -> разворот": s_three_candles,
    "Монетка (контроль)": s_random,
}


def evaluate(df, sig, expiry):
    move = df["Close"].shift(-expiry) - df["Close"]
    mask = (sig != 0) & move.notna()
    res = np.sign(move[mask]) * sig[mask]
    w, l = int((res > 0).sum()), int((res < 0).sum())
    n = w + l
    if n == 0:
        return None
    p = w / n
    ci = 1.96 * math.sqrt(p * (1 - p) / n)
    return {"n": n, "win": p, "lo": p - ci, "hi": p + ci, "pnl": w * PAYOUT - l}


def main():
    rows = []
    for tf, period in TIMEFRAMES.items():
        for t in PAIRS:
            try:
                df = indicators(load(t, tf, period))
            except Exception as e:
                print(f"пропуск {t} {tf}: {e}", file=sys.stderr)
                continue
            for name, fn in STRATEGIES.items():
                sig = fn(df)
                for e in EXPIRIES:
                    r = evaluate(df, sig, e)
                    if r:
                        rows.append({"tf": tf, "pair": t, "strategy": name, "expiry": e, **r})
    res = pd.DataFrame(rows)

    # Сводка: все пары вместе
    g = res.groupby(["tf", "strategy", "expiry"]).agg(n=("n", "sum"), pnl=("pnl", "sum"))
    wins = res.assign(w=res["win"] * res["n"]).groupby(["tf", "strategy", "expiry"])["w"].sum()
    g["win%"] = (wins / g["n"] * 100).round(2)
    g["pnl_на_сделку"] = (g["pnl"] / g["n"]).round(3)
    pd.set_option("display.width", 200)
    print(f"Безубыточность при выплате {PAYOUT:.0%}: {BREAKEVEN:.2%}\n")
    print(g.sort_values("win%", ascending=False).to_string())

    best = res[res["n"] >= 100].sort_values("win", ascending=False).head(10)
    print("\nЛучшие 10 комбинаций (пара отдельно, >=100 сделок):")
    print(best.round(3).to_string(index=False))
    print(f"\nВсего проверено комбинаций: {len(res)}")
    res.to_csv("research/results.csv", index=False)


if __name__ == "__main__":
    main()
