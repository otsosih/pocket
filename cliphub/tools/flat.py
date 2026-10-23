"""Flat 2D cartoon scenes (rounded shapes, soft colors). Drawn at 2x and downscaled for smooth edges."""
import random
from PIL import Image, ImageDraw, ImageFilter

OUT = 1080
S = 2                      # supersampling
N = OUT * S


def _k(c, k):
    return tuple(max(0, min(255, int(v * k))) for v in c[:3])


class Scene:
    def __init__(self, night=False):
        self.night = night
        self.img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.d = ImageDraw.Draw(self.img)
        self.dim = 0.45 if night else 1.0

    def c(self, col):
        return _k(col, self.dim)

    def rect(self, box, col, r=0, outline=None, w=0):
        box = [v * S for v in box]
        self.d.rounded_rectangle(box, radius=r * S, fill=self.c(col) if col else None,
                                 outline=self.c(outline) if outline else None, width=w * S)

    def ell(self, box, col, outline=None, w=0):
        self.d.ellipse([v * S for v in box], fill=self.c(col) if col else None,
                       outline=self.c(outline) if outline else None, width=w * S)

    def poly(self, pts, col):
        self.d.polygon([(x * S, y * S) for x, y in pts], fill=self.c(col))

    def line(self, pts, col, w):
        self.d.line([(x * S, y * S) for x, y in pts], fill=self.c(col), width=w * S, joint="curve")

    def glow(self, x, y, r, col, alpha=110):
        g = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=(*col, alpha))
        self.img.alpha_composite(g.filter(ImageFilter.GaussianBlur(r * S // 2)))

    def vignette(self, strength=170):
        v = Image.new("L", (N, N), 0)
        ImageDraw.Draw(v).ellipse([-N * 0.15, -N * 0.15, N * 1.15, N * 1.15], fill=255)
        v = v.filter(ImageFilter.GaussianBlur(N // 8))
        dark = Image.new("RGBA", (N, N), (0, 0, 10, strength))
        dark.putalpha(Image.eval(v, lambda a: int(strength * (1 - a / 255))))
        self.img.alpha_composite(dark)

    def save(self, path):
        self.img.resize((OUT, OUT), Image.LANCZOS).convert("RGB").save(path)


# ---------- backgrounds ----------

def room(s, wall=(232, 214, 190), floor=(170, 120, 85), window=True):
    s.rect([0, 0, OUT, 760], wall)
    s.rect([0, 740, OUT, OUT], floor)
    for x in range(0, OUT, 120):
        s.line([(x, 760), (x - 60, OUT)], _k(floor, 0.85), 3)
    s.rect([0, 735, OUT, 760], _k(wall, 0.8))
    if window:
        sky = (25, 30, 70) if s.night else (150, 205, 245)
        s.rect([640, 140, 960, 480], (250, 250, 250), r=12)
        s.rect([660, 160, 940, 460], sky, r=6)
        s.line([(800, 160), (800, 460)], (250, 250, 250), 10)
        s.line([(660, 310), (940, 310)], (250, 250, 250), 10)
        if s.night:
            s.ell([860, 185, 915, 240], (255, 250, 210))
        s.rect([610, 120, 680, 520], (190, 80, 80), r=20)
        s.rect([920, 120, 990, 520], (190, 80, 80), r=20)


def kitchen(s):
    room(s, wall=(210, 230, 225), floor=(200, 200, 205))
    for x in range(0, OUT, 90):
        for y in range(760, OUT, 90):
            s.rect([x + 3, y + 3, x + 87, y + 87], (215, 215, 220) if (x // 90 + y // 90) % 2 else (190, 190, 198))
    s.rect([40, 520, 520, 760], (240, 240, 240), r=8)
    s.rect([40, 500, 520, 530], (120, 100, 90), r=6)
    for x in (60, 220, 380):
        s.rect([x, 560, x + 130, 740], (225, 225, 228), r=8)
        s.rect([x + 55, 640, x + 75, 650], (150, 150, 150), r=4)
    s.rect([60, 200, 500, 380], (240, 240, 240), r=8)


def table(s, x=540, y=760, cup=None):
    s.rect([x - 220, y - 230, x + 220, y - 200], (150, 100, 65), r=8)
    s.rect([x - 200, y - 200, x - 175, y], (130, 85, 55), r=6)
    s.rect([x + 175, y - 200, x + 200, y], (130, 85, 55), r=6)
    if cup is not None:
        cx = x + cup
        s.rect([cx - 35, y - 300, cx + 35, y - 230], (240, 90, 90), r=10)
        s.ell([cx + 25, y - 285, cx + 65, y - 245], None, outline=(240, 90, 90), w=10)
        if not s.night:
            for i in range(3):
                s.line([(cx - 15 + i * 15, y - 320), (cx - 5 + i * 15, y - 360)], (255, 255, 255), 5)


def hallway(s):
    s.rect([0, 0, OUT, OUT], (120, 110, 130))
    s.poly([(0, 0), (300, 220), (300, 820), (0, OUT)], (95, 85, 105))
    s.poly([(OUT, 0), (780, 220), (780, 820), (OUT, OUT)], (95, 85, 105))
    s.poly([(0, OUT), (300, 820), (780, 820), (OUT, OUT)], (140, 100, 75))
    s.rect([300, 220, 780, 820], (150, 140, 160))
    s.rect([440, 380, 640, 820], (110, 70, 50), r=6)
    s.ell([600, 590, 620, 610], (230, 200, 90))


def front_door(s, locks=3, chain=True):
    s.rect([0, 0, OUT, OUT], (205, 195, 180))
    s.rect([0, 900, OUT, OUT], (140, 100, 75))
    s.rect([290, 80, 790, 905], (120, 75, 55), r=10)
    s.rect([320, 110, 760, 880], (135, 88, 62), r=8)
    for i in range(locks):
        y = 380 + i * 110
        s.rect([660, y, 720, y + 70], (190, 190, 195), r=10)
        s.ell([678, y + 20, 702, y + 44], (60, 60, 60))
    if chain:
        for i in range(6):
            s.ell([560 + i * 22, 300 + (i % 2) * 6, 586 + i * 22, 322 + (i % 2) * 6], None, outline=(200, 200, 205), w=5)
    s.rect([480, 200, 600, 230], (190, 190, 195), r=6)


def bedroom(s):
    room(s, wall=(170, 175, 215))
    s.rect([80, 560, 700, 780], (110, 80, 60), r=16)
    s.rect([60, 430, 120, 800], (100, 70, 55), r=14)
    s.rect([110, 520, 690, 640], (245, 245, 250), r=30)
    s.rect([120, 500, 280, 580], (255, 255, 255), r=30)
    s.rect([270, 560, 690, 700], (110, 150, 210), r=30)
    s.rect([760, 600, 900, 780], (150, 105, 75), r=8)


def closet(s, open_=False, hidden=False):
    s.rect([0, 0, OUT, OUT], (200, 185, 165))
    s.rect([0, 900, OUT, OUT], (140, 100, 75))
    s.rect([240, 100, 840, 900], (160, 115, 80), r=10)
    if open_:
        s.rect([270, 130, 810, 880], (45, 35, 30), r=6)
        s.line([(280, 200), (800, 200)], (180, 180, 180), 8)
        for i, col in enumerate([(200, 70, 70), (70, 110, 180), (90, 160, 100), (220, 180, 80)]):
            x = 320 + i * 120
            s.line([(x + 40, 200), (x + 40, 230)], (180, 180, 180), 5)
            s.rect([x, 230, x + 90, 520], col, r=14)
        if hidden:
            s.rect([470, 560, 620, 860], (20, 15, 15), r=4)
            s.glow(545, 700, 120, (255, 220, 140), 80)
            s.rect([470, 560, 620, 860], None, outline=(120, 90, 60), w=6)
    else:
        s.line([(540, 100), (540, 900)], (120, 85, 60), 6)
        s.ell([500, 480, 520, 500], (230, 200, 90))
        s.ell([560, 480, 580, 500], (230, 200, 90))


def stairwell(s):
    s.rect([0, 0, OUT, OUT], (150, 170, 160))
    for i in range(8):
        y = 980 - i * 90
        s.rect([100 + i * 60, y, OUT, y + 90], (120, 120, 125))
        s.rect([100 + i * 60, y, OUT, y + 14], (165, 165, 170))
    s.rect([60, 120, 300, 700], (110, 70, 50), r=6)
    s.ell([260, 400, 280, 420], (230, 200, 90))


def secret_room(s):
    s.rect([0, 0, OUT, OUT], (55, 45, 40))
    s.rect([0, 820, OUT, OUT], (75, 60, 50))
    s.glow(540, 200, 260, (255, 220, 150), 120)
    s.line([(540, 0), (540, 150)], (30, 30, 30), 4)
    s.ell([510, 150, 570, 210], (255, 235, 170))
    s.rect([120, 720, 620, 830], (150, 140, 120), r=20)
    s.rect([150, 690, 300, 740], (210, 205, 190), r=20)
    rnd = random.Random(5)
    for _ in range(26):
        x, y = rnd.randrange(80, 1000), rnd.randrange(260, 640)
        a = rnd.randrange(-12, 12)
        s.rect([x, y, x + 70, y + 90], (235, 230, 220), r=4)
        s.rect([x + 8, y + 8, x + 62, y + 66], (120, 130, 150), r=3)
    for i in range(4):
        s.rect([700 + i * 60, 760, 740 + i * 60, 820], (200, 80, 60), r=6)


def phone_screen(s, name="Лена", calling=True):
    s.rect([0, 0, OUT, OUT], (35, 40, 60))
    s.glow(540, 540, 330, (90, 120, 255), 70)
    s.rect([330, 120, 750, 960], (25, 25, 30), r=60)
    s.rect([350, 150, 730, 930], (60, 70, 110), r=44)
    s.ell([480, 300, 600, 420], (230, 170, 200))
    s.ell([505, 330, 525, 350], (40, 40, 40)); s.ell([555, 330, 575, 350], (40, 40, 40))
    s.rect([515, 375, 565, 385], (150, 60, 80), r=5)
    if calling:
        s.ell([400, 760, 500, 860], (230, 70, 70))
        s.ell([580, 760, 680, 860], (70, 200, 110))


# ---------- characters ----------

def person(s, x, y, body=(90, 120, 200), skin=(245, 205, 175), hair=(80, 50, 35), long_hair=False,
           glasses=False, cane=False, mood="calm", scale=1.0, look=0, uniform=False, old=False):
    """Rounded cartoon person; (x, y) = feet center."""
    u = 10 * scale
    if cane:
        s.line([(x + 9 * u, y - 14 * u), (x + 13 * u, y)], (250, 250, 250), int(1.2 * u))
        s.line([(x + 12.4 * u, y - 2.5 * u), (x + 13 * u, y)], (220, 50, 50), int(1.3 * u))
    s.rect([x - 6 * u, y - 10 * u, x - 1 * u, y], _k(body, 0.6), r=int(2 * u))
    s.rect([x + 1 * u, y - 10 * u, x + 6 * u, y], _k(body, 0.6), r=int(2 * u))
    s.rect([x - 9 * u, y - 27 * u, x + 9 * u, y - 8 * u], body, r=int(6 * u))
    if uniform:
        s.rect([x - 2 * u, y - 25 * u, x + 2 * u, y - 10 * u], (230, 200, 60), r=int(u))
    s.rect([x - 12 * u, y - 25 * u, x - 7 * u, y - 12 * u], _k(body, 0.85), r=int(2.5 * u))
    s.rect([x + 7 * u, y - 25 * u, x + 12 * u, y - 12 * u], _k(body, 0.85), r=int(2.5 * u))
    hx, hy, hr = x + look * u, y - 37 * u, 10 * u
    if long_hair:
        s.rect([hx - 11 * u, hy - 8 * u, hx + 11 * u, hy + 13 * u], hair, r=int(8 * u))
    s.ell([hx - hr, hy - hr, hx + hr, hy + hr], skin)
    if old:
        s.d.chord([(hx - hr) * S, (hy - hr - u) * S, (hx + hr) * S, (hy + hr) * S], 180, 360, fill=s.c((200, 200, 200)))
    else:
        s.d.chord([(hx - hr - u) * S, (hy - hr - 2 * u) * S, (hx + hr + u) * S, (hy + hr * 0.6) * S], 180, 360, fill=s.c(hair))
    if uniform:
        s.rect([hx - 11 * u, hy - 13 * u, hx + 11 * u, hy - 6 * u], (40, 60, 120), r=int(3 * u))
        s.rect([hx - 13 * u, hy - 7 * u, hx + 8 * u, hy - 5 * u], (30, 45, 95), r=int(u))
    ey = hy - 0.5 * u
    if glasses:
        s.rect([hx - 8 * u, ey - 2.5 * u, hx - 1 * u, ey + 2.5 * u], (25, 25, 30), r=int(2 * u))
        s.rect([hx + 1 * u, ey - 2.5 * u, hx + 8 * u, ey + 2.5 * u], (25, 25, 30), r=int(2 * u))
        s.line([(hx - 1 * u, ey - u), (hx + 1 * u, ey - u)], (25, 25, 30), int(u))
    else:
        big = mood in ("scared", "shock")
        r = 2.2 * u if big else 1.6 * u
        for ex in (hx - 4 * u, hx + 4 * u):
            s.ell([ex - r, ey - r, ex + r, ey + r], (255, 255, 255))
            s.ell([ex - r * 0.5, ey - r * 0.5, ex + r * 0.5, ey + r * 0.5], (40, 40, 50))
    my = hy + 5 * u
    if mood == "happy":
        s.d.chord([(hx - 4 * u) * S, (my - 3 * u) * S, (hx + 4 * u) * S, (my + 3 * u) * S], 0, 180, fill=s.c((150, 50, 60)))
    elif mood in ("scared", "shock"):
        s.ell([hx - 2.2 * u, my - 1.5 * u, hx + 2.2 * u, my + 2.5 * u], (120, 40, 50))
        if mood == "scared":
            s.ell([hx + 8 * u, hy - 6 * u, hx + 10 * u, hy - 2 * u], (150, 200, 255))
    elif mood == "sad":
        s.d.arc([(hx - 3 * u) * S, my * S, (hx + 3 * u) * S, (my + 4 * u) * S], 200, 340, fill=s.c((120, 40, 50)), width=int(u * S))
    else:
        s.line([(hx - 2.5 * u, my), (hx + 2.5 * u, my)], (150, 60, 70), int(u))


def vera(s, x=380, y=900, mood="calm", scale=1.0):
    person(s, x, y, body=(110, 170, 160), hair=(120, 70, 40), long_hair=True, glasses=True, cane=True,
           mood=mood, scale=scale)


def lena(s, x=700, y=900, mood="happy", scale=1.0):
    person(s, x, y, body=(230, 130, 90), hair=(40, 30, 30), long_hair=True, mood=mood, scale=scale)


def neighbor(s, x=700, y=900, mood="calm", scale=1.0):
    person(s, x, y, body=(120, 110, 90), hair=(200, 200, 200), old=True, mood=mood, scale=scale)


def police(s, x=720, y=900, mood="calm", scale=1.0):
    person(s, x, y, body=(50, 70, 130), hair=(60, 40, 30), uniform=True, mood=mood, scale=scale)


def stranger(s, x=740, y=900, scale=1.0):
    person(s, x, y, body=(70, 75, 80), hair=(50, 45, 40), skin=(220, 200, 185), mood="calm", scale=scale)


def shadow(s, x=760, y=900, scale=1.0, alpha=230):
    u = 10 * scale
    g = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    def R(b, r): gd.rounded_rectangle([v * S for v in b], radius=r * S, fill=(8, 8, 14, alpha))
    R([x - 10 * u, y - 30 * u, x + 10 * u, y], 8 * u)
    gd.ellipse([(x - 11 * u) * S, (y - 50 * u) * S, (x + 11 * u) * S, (y - 28 * u) * S], fill=(8, 8, 14, alpha))
    s.img.alpha_composite(g.filter(ImageFilter.GaussianBlur(3 * S)))
    for ex in (x - 4 * u, x + 4 * u):
        s.ell([ex - 1.6 * u, y - 40 * u, ex + 1.6 * u, y - 37 * u], (255, 255, 255))


def sound_marks(s, x, y, col=(255, 255, 255)):
    for i in range(3):
        s.d.arc([(x - 30 - i * 30) * S, (y - 30 - i * 30) * S, (x + 30 + i * 30) * S, (y + 30 + i * 30) * S],
                -40, 40, fill=s.c(col), width=6 * S)


def bell(s, x, y, ring=False):
    s.line([(x, y - 60), (x, y)], (90, 70, 50), 4)
    s.d.chord([(x - 30) * S, (y - 10) * S, (x + 30) * S, (y + 60) * S], 180, 360, fill=s.c((230, 190, 60)))
    s.rect([x - 32, y + 22, x + 32, y + 32], (210, 170, 50), r=4)
    if ring:
        sound_marks(s, x + 50, y + 15, (255, 230, 120))


# ---------- dark horror additions (sunken-archives-like look) ----------
from PIL import ImageFont

FONT_PATH = None   # set by the builder to Montserrat-Black.ttf


def _font(size):
    return ImageFont.truetype(FONT_PATH, size * S) if FONT_PATH else ImageFont.load_default()


def text(s, x, y, txt, size=48, col=(255, 255, 255), angle=0, alpha=255, anchor="mm"):
    layer = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((x * S, y * S), txt, font=_font(size), fill=(*s.c(col), alpha), anchor=anchor)
    if angle:
        layer = layer.rotate(angle, center=(x * S, y * S), resample=Image.BICUBIC)
    s.img.alpha_composite(layer)


def graffiti(s, txt, x, y, angle=8, col=(200, 60, 110), size=70):
    text(s, x, y, txt, size, col, angle, alpha=150)


def hud(s, x, y, small, big):
    """Corner info tag like «ЭТАЖ 9»."""
    s.rect([x, y, x + 8, y + 110], (230, 50, 50))
    text(s, x + 26, y + 22, small, 22, (170, 170, 180), anchor="lm")
    text(s, x + 26, y + 72, big, 56, (240, 240, 240), anchor="lm")


def flashlight(s, x, y, r=260, darkness=215):
    m = Image.new("L", (N, N), darkness)
    ImageDraw.Draw(m).ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=0)
    m = m.filter(ImageFilter.GaussianBlur(r * S // 3))
    dark = Image.new("RGBA", (N, N), (0, 0, 8, 255)); dark.putalpha(m)
    s.img.alpha_composite(dark)


def city_night(s):
    s.rect([0, 0, OUT, OUT], (22, 26, 44))
    rnd = random.Random(11)
    for _ in range(70):
        x, y = rnd.randrange(OUT), rnd.randrange(500)
        s.rect([x, y, x + 3, y + 3], (200, 200, 220))
    s.ell([780, 90, 880, 190], (225, 225, 215))
    for i, (x, w, h) in enumerate([(0, 230, 520), (210, 200, 640), (400, 260, 470), (650, 190, 600), (830, 250, 540)]):
        s.rect([x, OUT - 180 - h, x + w, OUT - 180], (48, 52, 70) if i % 2 else (58, 62, 80))
        for wx in range(x + 20, x + w - 30, 46):
            for wy in range(OUT - 160 - h, OUT - 200, 60):
                lit = rnd.random() < 0.12
                s.rect([wx, wy, wx + 24, wy + 32], (240, 210, 120) if lit else (30, 34, 50))
    s.rect([0, OUT - 180, OUT, OUT], (40, 40, 48))


def metro_entrance(s, sign="ВХОД ЗАКРЫТ"):
    city_night(s)
    s.rect([300, 640, 780, 900], (25, 25, 32))
    for i in range(6):
        s.rect([300, 640 + i * 44, 780, 652 + i * 44], (70, 70, 80))
    s.rect([270, 560, 810, 640], (120, 120, 130), r=6)
    s.rect([290, 575, 790, 625], (150, 30, 40), r=4)
    text(s, 540, 600, sign, 34, (255, 230, 230))
    s.glow(540, 760, 160, (120, 160, 255), 60)


def platform(s, light=True):
    s.rect([0, 0, OUT, OUT], (60, 66, 80))
    for x in range(0, OUT, 54):
        for y in range(0, 620, 54):
            s.rect([x + 2, y + 2, x + 52, y + 52], (78, 86, 100) if (x + y) // 54 % 2 else (70, 78, 92))
    for x in (110, 520, 930):
        s.rect([x - 40, 0, x + 40, 780], (95, 100, 115))
        s.rect([x - 50, 0, x + 50, 40], (110, 115, 130))
    s.rect([0, 620, OUT, 780], (120, 110, 100))
    s.rect([0, 770, OUT, 790], (220, 190, 60))
    s.rect([0, 790, OUT, OUT], (20, 20, 24))
    for x in (200, 420):
        pass
    s.line([(0, 900), (OUT, 900)], (110, 110, 120), 10)
    s.line([(0, 1000), (OUT, 1000)], (110, 110, 120), 10)
    if light:
        for x in (310, 730):
            s.rect([x - 70, 60, x + 70, 80], (250, 250, 230), r=8)
            s.glow(x, 120, 140, (255, 250, 220), 50)


def tunnel(s, depth=7):
    s.rect([0, 0, OUT, OUT], (14, 14, 20))
    for i in range(depth):
        k = i / depth
        m = int(60 + k * 420)
        col = tuple(int(70 - 55 * k) for _ in range(3))
        s.rect([m, m - 40, OUT - m, OUT - m + 40], None, outline=col, w=max(4, 22 - i * 3))
    s.poly([(470, OUT), (520, 560), (560, 560), (610, OUT)], (40, 40, 46))
    s.line([(380, OUT), (525, 560)], (120, 120, 130), 8)
    s.line([(700, OUT), (555, 560)], (120, 120, 130), 8)


def wagon(s, lit=False):
    s.rect([0, 0, OUT, OUT], (35, 40, 50))
    s.rect([0, 120, OUT, 160], (90, 90, 100))
    for x in (60, 400, 740):
        s.rect([x, 200, x + 280, 470], (20, 25, 35) if not lit else (60, 70, 90), r=14)
        s.rect([x + 10, 210, x + 270, 460], None, outline=(120, 120, 130), w=6)
    s.rect([0, 560, OUT, 680], (130, 70, 60), r=10)
    s.rect([0, 680, OUT, 720], (90, 50, 45))
    s.rect([0, 720, OUT, OUT], (50, 50, 55))
    for x in range(80, OUT, 240):
        s.line([(x, 160), (x, 560)], (170, 170, 180), 8)


def phone_msg(s, sender="НЕИЗВЕСТНЫЙ НОМЕР", lines=(), note="1 новое сообщение"):
    s.rect([0, 0, OUT, OUT], (10, 12, 18))
    s.glow(540, 540, 360, (60, 80, 160), 60)
    s.rect([260, 60, 820, 1040], (24, 26, 34), r=60)
    s.rect([285, 90, 795, 1010], (34, 38, 52), r=44)
    text(s, 540, 170, sender, 26, (170, 175, 190))
    text(s, 540, 205, "+7 ··· ··· ·· ··", 24, (120, 125, 140))
    if lines:
        h = 70 + 54 * len(lines)
        s.rect([320, 300, 760, 300 + h], (55, 60, 80), r=26)
        for i, ln in enumerate(lines):
            text(s, 350, 350 + i * 54, ln, 34, (235, 235, 240), anchor="lm")
    else:
        s.rect([340, 300, 740, 360], (55, 60, 80), r=20)
        text(s, 540, 330, note, 26, (220, 220, 230))


def hood_person(s, x, y, body=(230, 180, 40), skin=(245, 205, 175), hair=(60, 40, 30), mood="calm", scale=1.0, look=0):
    """Person with a hood up — main-character look."""
    u = 10 * scale
    person(s, x, y, body=body, skin=skin, hair=hair, mood=mood, scale=scale, look=look)
    hx, hy = x + look * u, y - 37 * u
    s.d.arc([(hx - 13 * u) * S, (hy - 14 * u) * S, (hx + 13 * u) * S, (hy + 14 * u) * S], 160, 380,
            fill=s.c(_k(body, 0.8)), width=int(3.5 * u * S))
