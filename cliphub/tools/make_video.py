"""Build a ClipHub Short: drawn scenes + Ken Burns + offline TTS + word subtitles + banner.

Usage: python3 make_video.py --out out.mp4 --banner ClipHub_games.mov --voice ru.onnx --font Montserrat-Black.ttf
"""
import argparse
import json
import os
import subprocess
import tempfile
import wave

import scenes as sc

W, H = 1080, 1920
SCENE_Y = 700          # top of the 1080x1080 scene area
BANNER_Y = 150
BANNER_FROM = 1.0      # ClipHub allows no banner only in the first 3 s
SUB_Y = 1420           # subtitle baseline, above the bottom UI zone
FPS = 30


def scene_greedy_friend(img):
    sc.sky(img); sc.ground(img); sc.house(img, 820, 780)
    sc.character(img, 330, 780, mood="normal")
    sc.character(img, 560, 780, shirt=(200, 60, 60), hair=(200, 160, 60), mood="angry")


def scene_found_chest(img):
    sc.sky(img); sc.ground(img)
    sc.chest(img, 600, 780, open_=True, s=1.4)
    for dx, dy in [(-60, -260), (0, -320), (60, -260), (-110, -330), (110, -330)]:
        sc.emerald(img, 600 + dx, 780 + dy)
    sc.character(img, 300, 780, mood="happy", wave=True)


def scene_night_theft(img):
    sc.sky(img, night=True); sc.ground(img, night=True); sc.house(img, 250, 780, night=True)
    sc.chest(img, 620, 780, night=True, s=1.2)
    sc.character(img, 800, 780, shirt=(200, 60, 60), hair=(200, 160, 60), mood="happy", night=True)


def scene_trap(img):
    sc.sky(img, night=True); sc.ground(img, night=True)
    sc.chest(img, 540, 780, open_=True, night=True, s=1.5)
    sc.exclamation(img, 540, 260)
    sc.character(img, 820, 780, shirt=(200, 60, 60), hair=(200, 160, 60), mood="shock", night=True)


def scene_outro(img):
    sc.sky(img); sc.ground(img)
    sc.character(img, 540, 780, mood="happy", wave=True, scale=1.3)
    sc.emerald(img, 300, 450); sc.emerald(img, 780, 450)


DEMO_STORY = [
    ("Мой друг Кирилл всегда говорил, что я жадный.", scene_greedy_friend, "in"),
    ("Однажды я нашёл сундук, полный изумрудов.", scene_found_chest, "out"),
    ("Ночью Кирилл тайком забрал их все.", scene_night_theft, "left"),
    ("Но он не знал, что этот сундук был ловушкой.", scene_trap, "in"),
    ("Подпишись, чтобы узнать, что было дальше!", scene_outro, "out"),
]


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def tts(text, voice, path, length_scale=1.0, silence=0.25):
    subprocess.run(["piper", "-m", voice, "-f", path, "--sentence_silence", str(silence),
                    "--length_scale", str(length_scale)],
                   input=text.encode(), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


def ken_burns(png, dur, move, path):
    # Upscale first so zoompan's integer crop steps stay invisible.
    n = max(2, round(dur * FPS))
    p = f"(on/{n - 1})"
    z, x, y = {
        "in": (f"1+0.25*{p}", "iw/2-iw/zoom/2", "ih/2-ih/zoom/2"),
        "out": (f"1.25-0.25*{p}", "iw/2-iw/zoom/2", "ih/2-ih/zoom/2"),
        "left": ("1.2", f"(iw-iw/zoom)*(1-{p})", "ih/2-ih/zoom/2"),
    }[move]
    vf = f"scale=4320:4320,zoompan=z='{z}':x='{x}':y='{y}':d={n}:s=1080x1080:fps={FPS},format=yuv420p"
    run(["ffmpeg", "-y", "-i", png, "-vf", vf, "-frames:v", str(n),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", path])


def ass_time(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def write_ass(segments, font_name, path):
    """One word on screen at a time, timed proportionally to word length."""
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, "
        "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV",
        f"Style: W,{font_name},96,&H00FFFFFF,&H00000000,&H64000000,1,1,8,3,2,40,40,{H - SUB_Y}",
        "", "[Events]", "Format: Layer, Start, End, Style, Text",
    ]
    for start, dur, text in segments:
        words = text.split()
        speak = dur - 0.3
        total = sum(len(w) + 2 for w in words)
        t = start
        for w in words:
            d = speak * (len(w) + 2) / total
            lines.append(f"Dialogue: 0,{ass_time(t)},{ass_time(t + d)},W,{{\\fscx115\\fscy115\\t(0,90,\\fscx100\\fscy100)}}{w.upper()}")
            t += d
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def build(story, out, banner, voice, font):
    tmp = tempfile.mkdtemp(prefix="cliphub_")
    clips, wavs, segments, t = [], [], [], 0.0
    for i, (text, draw, move) in enumerate(story):
        wav = os.path.join(tmp, f"s{i}.wav")
        dur = tts(text, voice, wav) + 0.15
        img = sc.new_canvas(); draw(img)
        png = os.path.join(tmp, f"s{i}.png"); img.convert("RGB").save(png)
        clip = os.path.join(tmp, f"s{i}.mp4"); ken_burns(png, dur, move, clip)
        clips.append(clip); wavs.append(wav); segments.append((t, dur, text)); t += dur
    total = t

    with open(os.path.join(tmp, "v.txt"), "w") as f:
        f.writelines(f"file '{c}'\n" for c in clips)
    scene_track = os.path.join(tmp, "scenes.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "v.txt"), "-c", "copy", scene_track])
    audio = os.path.join(tmp, "voice.wav")
    run(["ffmpeg", "-y", *sum([["-i", w] for w in wavs], []), "-filter_complex",
         "".join(f"[{i}]apad=pad_dur=0.15[a{i}];" for i in range(len(wavs)))
         + "".join(f"[a{i}]" for i in range(len(wavs))) + f"concat=n={len(wavs)}:v=0:a=1", audio])

    ass = os.path.join(tmp, "subs.ass")
    write_ass(segments, "Montserrat Black", ass)
    fonts_dir = os.path.dirname(os.path.abspath(font))
    fc = (
        f"[0]split[sc][bgsrc];"
        f"[bgsrc]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30,eq=brightness=-0.2[bg];"
        f"[bg][sc]overlay=0:{SCENE_Y}[v1];"
        f"[1]fps={FPS},scale={W}:-1,format=rgba[ban];"
        f"[v1][ban]overlay=0:{BANNER_Y}:enable='gte(t,{BANNER_FROM})':shortest=1[v2];"
        f"[v2]ass={ass}:fontsdir={fonts_dir},format=yuv420p[v]"
    )
    run(["ffmpeg", "-y", "-i", scene_track, "-stream_loop", "-1", "-i", banner, "-i", audio,
         "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", f"{total:.3f}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
         "-movflags", "+faststart", out])
    return total


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--banner", required=True)
    ap.add_argument("--voice", required=True)
    ap.add_argument("--font", required=True)
    a = ap.parse_args()
    print(json.dumps({"duration": round(build(DEMO_STORY, a.out, a.banner, a.voice, a.font), 2)}))
