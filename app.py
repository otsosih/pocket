"""
Сайт с учебными сигналами ВВЕРХ / ВНИЗ (Streamlit).

Запуск на компьютере:  streamlit run app.py
Стратегия та же, что в боте: «отскок» по RSI + полосам Боллинджера.
Котировки — Yahoo Finance (реальный рынок), не OTC-котировки брокера.
Сигналы учебные и не гарантируют прибыль.
"""

import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Сигналы", page_icon="📈", layout="centered")

PAIRS = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "CAD=X",
    "EUR/JPY": "EURJPY=X",
    "USD/EGP": "EGP=X",
    "BTC/USD": "BTC-USD",
}
TIMEFRAMES = {"1m": ("1m", "5d"), "5m": ("5m", "30d"), "15m": ("15m", "30d")}
PAYOUT = 0.85
EXPIRIES = (1, 3, 5)


# ---------- Данные и расчёты ----------

@st.cache_data(ttl=30, show_spinner=False)
def load(ticker: str, tf: str) -> pd.DataFrame | None:
    interval, period = TIMEFRAMES[tf]
    try:
        df = yf.Ticker(ticker).history(interval=interval, period=period)
    except Exception:
        return None
    if df is None or df.empty:
        return None
    df = df[["Open", "High", "Low", "Close"]].dropna()
    return df if len(df) >= 30 else None


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    close = df["Close"]
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
    with np.errstate(divide="ignore", invalid="ignore"):
        rsi = 100 - 100 / (1 + gain / loss)
    rsi = rsi.where(loss != 0, 100.0)
    rsi = rsi.where((gain != 0) | (loss != 0), 50.0)
    df["rsi"] = rsi
    mid = close.rolling(20).mean()
    std = close.rolling(20).std()
    df["bb_up"] = mid + 2 * std
    df["bb_low"] = mid - 2 * std
    df["ema_fast"] = close.ewm(span=9, adjust=False).mean()
    df["ema_slow"] = close.ewm(span=21, adjust=False).mean()
    return df


def signals(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    up = (df["rsi"] < 30) & (df["Close"] < df["bb_low"])
    down = (df["rsi"] > 70) & (df["Close"] > df["bb_up"])
    return up, down


def backtest(df: pd.DataFrame, expiry: int) -> dict:
    up, down = signals(df)
    close = df["Close"]
    future = close.shift(-expiry)
    valid = future.notna()
    win = ((up & (future > close)) | (down & (future < close))) & valid
    lose = ((up & (future < close)) | (down & (future > close))) & valid
    draw = ((up | down) & (future == close)) & valid
    w, l, d = int(win.sum()), int(lose.sum()), int(draw.sum())
    return {
        "Экспирация": f"{expiry} св.",
        "Сигналов": w + l + d,
        "Верно": w,
        "Неверно": l,
        "Точность, %": round(w / (w + l) * 100, 1) if w + l else None,
        "Итог, ставок": round(w * PAYOUT - l, 2),
    }


def fmt(x: float) -> str:
    return f"{x:.5f}" if x < 10 else f"{x:.3f}" if x < 1000 else f"{x:,.2f}"


# ---------- Страница ----------

st.title("📈 Сигналы ВВЕРХ / ВНИЗ")
st.caption(
    "Учебный инструмент. Котировки с реального рынка (Yahoo Finance, возможна задержка). "
    "OTC-пары брокера — его собственные котировки, они могут отличаться."
)

c1, c2 = st.columns(2)
pair = c1.selectbox("Валютная пара", list(PAIRS))
tf = c2.selectbox("Таймфрейм", list(TIMEFRAMES))

if st.button("🔄 Обновить", use_container_width=True):
    load.clear()

with st.spinner("Загружаю котировки…"):
    raw = load(PAIRS[pair], tf)

if raw is None:
    st.error(
        f"Нет данных по {pair} · {tf}. Возможно, рынок закрыт (выходные) или у Yahoo "
        "нет внутридневных котировок по этой паре. Попробуй другой таймфрейм или пару."
    )
    st.stop()

df = add_indicators(raw).dropna()
last = df.iloc[-1]
up, down = signals(df)

if up.iloc[-1]:
    st.success("## 🟢 ВВЕРХ\nПерепроданность: RSI ниже 30 и цена под нижней полосой Боллинджера.")
elif down.iloc[-1]:
    st.error("## 🔴 ВНИЗ\nПерекупленность: RSI выше 70 и цена над верхней полосой Боллинджера.")
else:
    st.info("## ⚪️ Нет сигнала\nУсловия стратегии сейчас не выполнены. Лучше подождать.")

m1, m2, m3 = st.columns(3)
m1.metric("Цена", fmt(last["Close"]))
m2.metric("RSI(14)", f"{last['rsi']:.1f}")
m3.metric("Тренд EMA", "вверх" if last["ema_fast"] > last["ema_slow"] else "вниз")
st.caption(f"Последняя свеча: {df.index[-1]:%d.%m %H:%M} (время биржи)")

chart = df[["Close", "bb_up", "bb_low"]].tail(120).rename(
    columns={"Close": "Цена", "bb_up": "Верхняя полоса", "bb_low": "Нижняя полоса"}
)
st.line_chart(chart)

st.subheader("Как такие сигналы срабатывали раньше")
breakeven = 100 / (1 + PAYOUT)
st.caption(
    f"{len(df)} свечей, {df.index[0]:%d.%m} – {df.index[-1]:%d.%m}. "
    f"При выплате {PAYOUT:.0%} для выхода в ноль нужно угадывать не меньше {breakeven:.1f}%."
)
st.dataframe(
    pd.DataFrame([backtest(df, e) for e in EXPIRIES]),
    hide_index=True,
    use_container_width=True,
)
st.caption("Прошлые результаты не гарантируют будущих. Мало сигналов — статистика ненадёжна.")
