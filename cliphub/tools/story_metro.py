"""«Станция, которой нет на схеме» — episode 1. Dark flat-2D horror series, full-screen 9:16.

Text markup: ^word — word highlighted red in subtitles (the ^ is not spoken).
Usage: python3 story_metro.py --out ep1.mp4 --banner ClipHub_services.mov --voice ru.onnx --font Montserrat-Black.ttf
"""
import argparse
import os
import re
import tempfile

from PIL import Image, ImageDraw

import flat as f
from make_video import FPS, W, H, BANNER_Y, BANNER_FROM, run, tts, ken_burns, ass_time

SCENE_Y = 560          # square scene sits under the banner; black above and below
SUB_Y = 1250           # subtitles mid-screen, like the reference channel
SERIES = "СТАНЦИЯ, КОТОРОЙ НЕТ"
NEXT = ("ЧАСТЬ 2", "СЛЕДУЮЩИЙ ПОЕЗД")

MAX = dict(body=(230, 180, 40))         # yellow hoodie — main hero
TIM = dict(body=(60, 110, 200))         # blue jacket — friend


def max_(s, x, y, mood="calm", scale=1.0, look=0):
    f.hood_person(s, x, y, mood=mood, scale=scale, look=look, **MAX)


def tim(s, x, y, mood="calm", scale=1.0, look=0):
    f.person(s, x, y, hair=(30, 25, 25), mood=mood, scale=scale, look=look, **TIM)


def eyes_crowd(s):
    for i, x in enumerate((150, 330, 520, 700, 880)):
        f.shadow(s, x, 700 + (i % 2) * 20, 0.75, 235)


STORY = [
    ("Если вы ^слышите поезд в закрытом метро — ^не садитесь в него.",
     [f.metro_entrance, lambda s: max_(s, 140, 1040, "scared", 0.8), lambda s: tim(s, 940, 1040, "scared", 0.8), f.Scene.vignette], "in"),
    ("Станцию «Заводская» закрыли ^двадцать лет назад. Вход заварили, а со схемы её просто ^стёрли.",
     [lambda s: f.metro_entrance(s, "ЗАКРЫТО"), lambda s: f.hud(s, 60, 880, "ЗАКРЫТА", "20 ЛЕТ"), f.Scene.vignette], "out"),
    ("Но Тим нашёл в сети видео. Ночью внизу ^горит свет.",
     [lambda s: f.phone_msg(s, "ВИДЕО · 03:12", ("Заводская. Ночью.", "Внизу кто-то есть?")), ], "in"),
    ("Вы спускаетесь в два часа ночи. ^Сорок две ступени. Внизу пахнет мокрым бетоном.",
     [f.stairwell, lambda s: max_(s, 420, 900, "calm", 0.9), lambda s: tim(s, 640, 800, "calm", 0.85),
      lambda s: f.flashlight(s, 520, 650, 300), lambda s: f.hud(s, 60, 880, "СТУПЕНЕЙ", "42")], "left"),
    ("Платформа ^пустая. Но лампы горят. Все до одной. Хотя ^электричество отключили двадцать лет назад.",
     [f.platform, lambda s: max_(s, 400, 760, "scared", 0.85), lambda s: tim(s, 620, 760, "calm", 0.85), f.Scene.vignette], "in"),
    ("На колонне кто-то написал краской: ^не жди поезд.",
     [f.platform, lambda s: f.graffiti(s, "НЕ ЖДИ ПОЕЗД", 540, 420, 6, (230, 70, 100), 76),
      lambda s: f.flashlight(s, 540, 430, 330, 170)], "in"),
    ("Тим смеётся и снимает сторис. А потом из тоннеля ^дует ветер. Тёплый.",
     [f.platform, lambda s: tim(s, 540, 760, "happy", 1.0), lambda s: f.sound_marks(s, 900, 860, (200, 220, 255)), f.Scene.vignette], "out"),
    ("Так дует, когда ^подъезжает поезд.",
     [f.tunnel, lambda s: s.glow(540, 560, 140, (255, 240, 200), 160), f.Scene.vignette], "in"),
    ("Из темноты выходит ^старый вагон. Внутри горит свет, и двери ^открываются сами.",
     [lambda s: f.wagon(s, lit=True), lambda s: s.glow(540, 330, 400, (255, 230, 170), 60), f.Scene.vignette], "left"),
    ("В вагоне сидят люди. Человек десять. Они ^не двигаются. Они смотрят ^прямо на вас.",
     [lambda s: f.wagon(s, lit=True), eyes_crowd, f.Scene.vignette], "in"),
    ("Тим делает ^шаг к дверям. Вы хватаете его за куртку в ^последнюю секунду.",
     [f.platform, lambda s: tim(s, 560, 760, "calm", 1.0, look=2), lambda s: max_(s, 320, 760, "scared", 1.0), f.Scene.vignette], "in"),
    ("Двери закрываются. Поезд уходит в тоннель ^без звука.",
     [lambda s: f.tunnel(s, 9), f.Scene.vignette], "out"),
    ("И тут у Тима вибрирует телефон. Сообщение с ^неизвестного номера.",
     [lambda s: f.phone_msg(s)], "in"),
    ("Зря ты его ^остановил. Следующий поезд — ^за тобой.",
     [lambda s: f.phone_msg(s, lines=("Зря ты его остановил.", "Следующий поезд —", "за тобой."))], "in"),
    ("Продолжение — во второй части.", "END", "none"),
]


def clean(t):
    return t.replace("^", "")


def chunks(t):
    """Split into on-screen groups of up to 3 words / ~18 chars, breaking after punctuation."""
    out, cur = [], []
    for w in t.split():
        cur.append(w)
        plain = " ".join(x.replace("^", "") for x in cur)
        if len(cur) == 3 or len(plain) >= 16 or re.search(r"[.,!?:—…]$", w.replace("^", "")):
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def write_subs(segs, path):
    lines = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "", "[V4+ Styles]",
             "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, "
             "Outline, Shadow, Alignment, MarginL, MarginR, MarginV",
             f"Style: S,Montserrat Black,88,&H00FFFFFF,&H00101010,&H8C000000,1,1,7,4,5,60,60,0",
             "", "[Events]", "Format: Layer, Start, End, Style, Text"]
    for start, dur, text in segs:
        if text is None:
            continue
        groups = chunks(text)
        speak = dur - 0.3
        weights = [sum(len(w) for w in g) + 2 * len(g) for g in groups]
        t = start
        for g, wt in zip(groups, weights):
            d = speak * wt / sum(weights)
            words = []
            for w in g:
                if w.startswith("^"):
                    words.append("{\\c&H3C3CE6&}" + w[1:].upper() + "{\\c&HFFFFFF&}")
                else:
                    words.append(w.upper())
            pos = f"{{\\an5\\pos({W // 2},{SUB_Y})\\fscx112\\fscy112\\t(0,80,\\fscx100\\fscy100)}}"
            lines.append(f"Dialogue: 0,{ass_time(t)},{ass_time(t + d)},S,{pos}{' '.join(words)}")
            t += d
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def end_card(path):
    s = f.Scene(False)
    s.rect([0, 0, 1080, 1080], (0, 0, 0))
    f.text(s, 540, 470, NEXT[0], 34, (170, 170, 180))
    f.text(s, 540, 540, NEXT[1], 70, (245, 245, 245))
    s.save(path)


def frame_mask(path):
    """Black frame around the square scene with soft fades on its top/bottom edges."""
    m = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(m)
    d.rectangle([0, SCENE_Y, W, SCENE_Y + 1080], fill=(0, 0, 0, 0))
    fade = 140
    for i in range(fade):
        a = int(255 * (1 - i / fade) ** 1.6)
        d.line([(0, SCENE_Y + i), (W, SCENE_Y + i)], fill=(0, 0, 0, a))
        d.line([(0, SCENE_Y + 1079 - i), (W, SCENE_Y + 1079 - i)], fill=(0, 0, 0, a))
    m.save(path)


def main():
    ap = argparse.ArgumentParser()
    for k in ("out", "banner", "voice", "font"):
        ap.add_argument(f"--{k}", required=True)
    ap.add_argument("--pitch", type=float, default=1.0, help="<1 lowers the voice, e.g. 0.917 = -1.5 semitones")
    a = ap.parse_args()
    f.FONT_PATH = a.font
    tmp = tempfile.mkdtemp(prefix="metro_")
    fonts_dir = os.path.dirname(os.path.abspath(a.font))

    clips, wavs, segs, t = [], [], [], 0.0
    for i, (text, layers, move) in enumerate(STORY):
        wav = os.path.join(tmp, f"s{i:02d}.wav")
        dur = tts(clean(text), a.voice, wav, length_scale=1.12, silence=0.12) + 0.15
        png = os.path.join(tmp, f"s{i:02d}.png")
        if layers == "END":
            end_card(png); dur += 1.0
            run(["ffmpeg", "-y", "-loop", "1", "-i", png, "-t", f"{dur:.3f}", "-r", str(FPS),
                 "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                 os.path.join(tmp, f"s{i:02d}.mp4")])
            segs.append((t, dur, None))
        else:
            s = f.Scene(False)
            for layer in layers:
                layer(s)
            s.save(png)
            ken_burns(png, dur, move, os.path.join(tmp, f"s{i:02d}.mp4"))
            segs.append((t, dur, text))
        clips.append(os.path.join(tmp, f"s{i:02d}.mp4")); wavs.append(wav); t += dur
        print(f"scene {i + 1}/{len(STORY)} {dur:.1f}s", flush=True)
    total = t

    with open(os.path.join(tmp, "v.txt"), "w") as fh:
        fh.writelines(f"file '{c}'\n" for c in clips)
    scenes = os.path.join(tmp, "scenes.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "v.txt"), "-c", "copy", scenes])
    voice = os.path.join(tmp, "voice.wav")
    run(["ffmpeg", "-y", *sum([["-i", w] for w in wavs], []), "-filter_complex",
         "".join(f"[{i}]apad=whole_dur={segs[i][1]:.3f}[a{i}];" for i in range(len(wavs)))
         + "".join(f"[a{i}]" for i in range(len(wavs))) + f"concat=n={len(wavs)}:v=0:a=1", voice])

    # Optional pitch shift (tempo kept) + quiet dark ambient bed, like the reference.
    mixed = os.path.join(tmp, "mix.wav")
    run(["ffmpeg", "-y", "-i", voice,
         "-f", "lavfi", "-i", f"anoisesrc=color=brown:amplitude=0.5:d={total:.3f}",
         "-f", "lavfi", "-i", f"sine=frequency=55:d={total:.3f}",
         "-filter_complex",
         f"[0]aresample=44100,asetrate=44100*{a.pitch},aresample=44100,atempo={1 / a.pitch:.4f},"
         "equalizer=f=180:t=q:w=1:g=3,acompressor=threshold=0.1:ratio=3,volume=1.4[v];"
         "[1]lowpass=f=400,volume=0.10[n];[2]volume=0.05,tremolo=f=0.15:d=0.6[d];"
         "[n][d]amix=inputs=2:normalize=0,afade=t=in:d=2[bed];"
         "[v][bed]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5[out]",
         "-map", "[out]", "-ar", "44100", "-ac", "2", mixed])
    voice = mixed
    subs = os.path.join(tmp, "subs.ass"); write_subs(segs, subs)
    mask = os.path.join(tmp, "mask.png"); frame_mask(mask)
    fc = (f"color=c=black:s={W}x{H}:r={FPS}[bg];"
          f"[bg][0]overlay=0:{SCENE_Y}:shortest=1[v0];"
          f"[v0][3]overlay=0:0[v1];"
          f"[1]fps={FPS},scale={W}:-1,format=rgba[ban];"
          f"[v1][ban]overlay=0:{BANNER_Y}:enable='gte(t,{BANNER_FROM})'[v2];"
          f"[v2]ass={subs}:fontsdir={fonts_dir},format=yuv420p[v]")
    run(["ffmpeg", "-y", "-i", scenes, "-stream_loop", "-1", "-i", a.banner, "-i", voice, "-loop", "1", "-i", mask,
         "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", f"{total:.3f}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
         "-movflags", "+faststart", a.out])
    print(f"done {total:.1f}s", flush=True)


if __name__ == "__main__":
    main()
