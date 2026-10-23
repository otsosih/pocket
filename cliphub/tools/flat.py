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
