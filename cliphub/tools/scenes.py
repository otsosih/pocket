"""Blocky (Minecraft-like) scene drawing with Pillow. No AI, no credits."""
import random
from PIL import Image, ImageDraw, ImageFilter

SIZE = 1080
BLOCK = 60


def _shade(c, k):
    return tuple(max(0, min(255, int(v * k))) for v in c)


def sky(img, night=False):
    d = ImageDraw.Draw(img)
    top, bottom = ((10, 12, 40), (40, 30, 90)) if night else ((70, 150, 255), (170, 220, 255))
    for y in range(SIZE):
        t = y / SIZE
        d.line([(0, y), (SIZE, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    rnd = random.Random(7)
    if night:
        for _ in range(90):
            x, y = rnd.randrange(SIZE), rnd.randrange(SIZE // 2)
            d.rectangle([x, y, x + 5, y + 5], fill=(255, 255, 220))
        d.rectangle([820, 90, 940, 210], fill=(235, 235, 210))
    else:
        d.rectangle([820, 90, 940, 210], fill=(255, 240, 120))
        for cx, cy in [(120, 160), (460, 110), (650, 230)]:
            for i in range(4):
                d.rectangle([cx + i * 50, cy, cx + i * 50 + 50, cy + 40], fill=(250, 250, 255))
            d.rectangle([cx + 50, cy - 30, cx + 150, cy], fill=(250, 250, 255))


def ground(img, y0=780, night=False):
    d = ImageDraw.Draw(img)
    rnd = random.Random(3)
    k = 0.45 if night else 1.0
    for bx in range(0, SIZE, BLOCK):
        for by in range(y0, SIZE, BLOCK):
            base = (95, 170, 60) if by == y0 else (130, 90, 55)
            d.rectangle([bx, by, bx + BLOCK, by + BLOCK], fill=_shade(base, k))
            for _ in range(10):
                px, py = bx + rnd.randrange(0, BLOCK, 10), by + rnd.randrange(0, BLOCK, 10)
                d.rectangle([px, py, px + 10, py + 10], fill=_shade(base, k * rnd.uniform(0.8, 1.15)))
            d.rectangle([bx, by, bx + BLOCK, by + BLOCK], outline=_shade(base, k * 0.7), width=2)


def character(img, x, y, shirt=(40, 160, 200), skin=(230, 180, 140), hair=(70, 45, 25),
              pants=(50, 50, 140), mood="normal", wave=False, scale=1.0, night=False):
    """Blocky person; (x, y) is the feet center."""
    d = ImageDraw.Draw(img)
    k = 0.55 if night else 1.0
    u = int(20 * scale)
    sk, sh, ha, pa = (_shade(c, k) for c in (skin, shirt, hair, pants))
    # legs
    d.rectangle([x - 2 * u, y - 6 * u, x - 1, y], fill=pa)
    d.rectangle([x, y - 6 * u, x + 2 * u, y], fill=_shade(pa, 0.85))
    # body
    d.rectangle([x - 2 * u, y - 12 * u, x + 2 * u, y - 6 * u], fill=sh)
    # arms
    d.rectangle([x - 4 * u, y - 12 * u, x - 2 * u, y - 6 * u], fill=_shade(sh, 0.85))
    if wave:
        d.rectangle([x + 2 * u, y - 17 * u, x + 4 * u, y - 11 * u], fill=_shade(sh, 0.85))
        d.rectangle([x + 2 * u, y - 18 * u, x + 4 * u, y - 16 * u], fill=sk)
    else:
        d.rectangle([x + 2 * u, y - 12 * u, x + 4 * u, y - 6 * u], fill=_shade(sh, 0.85))
    # head
    hx0, hy0 = x - 2 * u, y - 16 * u
    d.rectangle([hx0, hy0, x + 2 * u, y - 12 * u], fill=sk)
    d.rectangle([hx0, hy0, x + 2 * u, hy0 + u // 2 + 2], fill=ha)
    # face
    e = max(4, u // 2)
    eye_y = hy0 + int(1.6 * u)
    for ex in (x - u - e // 2, x + u - e // 2):
        d.rectangle([ex, eye_y, ex + e, eye_y + e], fill=(255, 255, 255))
        d.rectangle([ex + e // 2, eye_y, ex + e, eye_y + e], fill=(40, 40, 120))
    my = hy0 + int(3 * u)
    if mood == "happy":
        d.rectangle([x - u, my, x + u, my + e // 2], fill=(120, 40, 40))
        d.rectangle([x - u - e // 2, my - e // 2, x - u, my], fill=(120, 40, 40))
        d.rectangle([x + u, my - e // 2, x + u + e // 2, my], fill=(120, 40, 40))
    elif mood == "angry":
        d.rectangle([x - u, my, x + u, my + e // 2], fill=(120, 40, 40))
        d.line([(x - u - e, eye_y - e), (x - e // 2, eye_y - 2)], fill=(30, 20, 10), width=5)
        d.line([(x + u + e, eye_y - e), (x + e // 2, eye_y - 2)], fill=(30, 20, 10), width=5)
    elif mood == "shock":
        d.rectangle([x - e, my - e // 2, x + e, my + e], fill=(60, 20, 20))
    else:
        d.rectangle([x - u // 2, my, x + u // 2, my + e // 2], fill=(120, 40, 40))


def chest(img, x, y, open_=False, night=False, s=1.0):
    d = ImageDraw.Draw(img)
    k = 0.55 if night else 1.0
    w, h = int(150 * s), int(120 * s)
    wood, dark = _shade((160, 105, 45), k), _shade((100, 60, 25), k)
    d.rectangle([x - w // 2, y - h, x + w // 2, y], fill=wood, outline=dark, width=6)
    d.line([(x - w // 2, y - h * 0.6), (x + w // 2, y - h * 0.6)], fill=dark, width=6)
    d.rectangle([x - 10, y - h * 0.7, x + 10, y - h * 0.45], fill=_shade((200, 200, 200), k))
    if open_:
        d.polygon([(x - w // 2, y - h), (x + w // 2, y - h), (x + w // 2 - 20, y - h - 70 * s),
                   (x - w // 2 + 20, y - h - 70 * s)], fill=dark)


def emerald(img, x, y, r=28, glow=True):
    if glow:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse([x - r * 2.2, y - r * 2.2, x + r * 2.2, y + r * 2.2], fill=(80, 255, 140, 90))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(r)))
    d = ImageDraw.Draw(img)
    d.polygon([(x, y - r), (x + r * 0.7, y), (x, y + r), (x - r * 0.7, y)], fill=(40, 200, 90),
              outline=(10, 110, 50), width=4)
    d.polygon([(x, y - r * 0.5), (x + r * 0.3, y), (x, y + r * 0.2)], fill=(170, 255, 200))


def house(img, x, y, night=False):
    d = ImageDraw.Draw(img)
    k = 0.5 if night else 1.0
    for bx in range(x - 180, x + 180, BLOCK):
        for by in range(y - 240, y, BLOCK):
            d.rectangle([bx, by, bx + BLOCK, by + BLOCK], fill=_shade((175, 130, 80), k),
                        outline=_shade((120, 85, 50), k), width=3)
    d.rectangle([x - 40, y - 140, x + 40, y], fill=_shade((90, 60, 30), k))
    win = (255, 220, 120) if night else (150, 210, 255)
    d.rectangle([x + 70, y - 200, x + 150, y - 130], fill=win)
    d.polygon([(x - 210, y - 240), (x + 210, y - 240), (x, y - 380)], fill=_shade((150, 60, 50), k))


def exclamation(img, x, y, color=(255, 60, 60)):
    d = ImageDraw.Draw(img)
    d.rectangle([x - 18, y, x + 18, y + 110], fill=color, outline=(0, 0, 0), width=5)
    d.rectangle([x - 18, y + 130, x + 18, y + 166], fill=color, outline=(0, 0, 0), width=5)


def new_canvas():
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 255))
