"""«Я слепая и живу одна» — full ~5 min video + Shorts parts with ClipHub banner.

Usage: python3 story_blind.py --outdir DIR --banner ClipHub_services.mov --voice ru.onnx --font Montserrat-Black.ttf
"""
import argparse
import os
import subprocess
import tempfile

import flat as f
from make_video import FPS, W, H, SCENE_Y, BANNER_Y, BANNER_FROM, SUB_Y, run, tts, ken_burns, write_ass, ass_time


def sc(night=False, *layers):
    def draw(s):
        for layer in layers:
            layer(s)
    return night, draw


V = f.vera
STORY = [
    # part 1
    ("Меня зовут Вера. Я не вижу с семи лет. И я точно знаю, что в моей квартире живёт кто-то ещё.", sc(True, f.room, lambda s: V(s, 420, 900, "scared"), lambda s: f.shadow(s, 860, 880, 0.9, 120), f.Scene.vignette), "in"),
    ("Три года я живу одна. Я знаю свой дом наизусть. Четырнадцать шагов от двери до кухни. Шесть — от кухни до кровати.", sc(False, f.room, lambda s: V(s, 460, 900, "calm")), "left"),
    ("Всё началось с кружки. Вечером я всегда оставляю её на краю стола, у правой руки.", sc(False, f.kitchen, lambda s: f.table(s, 600, 900, cup=180), lambda s: V(s, 250, 900, "calm")), "in"),
    ("А утром она стояла ровно в центре. Я не ставлю её в центр. Никогда.", sc(False, f.kitchen, lambda s: f.table(s, 540, 900, cup=0), f.Scene.vignette), "in"),
    # part 2
    ("Я решила, что просто устала. Но через неделю тапочки у кровати стояли носками к стене. А я всегда ставлю их к двери.", sc(True, f.bedroom, lambda s: V(s, 830, 900, "sad", 0.9)), "out"),
    ("Потом появился запах. В коридоре пахло чужим одеколоном. Резким, мужским. Я живу одна. Ко мне никто не приходит.", sc(True, f.hallway, lambda s: V(s, 540, 900, "scared")), "in"),
    ("Я позвонила подруге Лене. Она рассмеялась и сказала, что я просто слишком много слушаю страшных подкастов.", sc(False, lambda s: f.phone_screen(s)), "out"),
    ("Я тоже посмеялась. А ночью проснулась от звука. Скрипнула половица на кухне. Третья от окна. Я знаю этот скрип.", sc(True, f.kitchen, lambda s: f.sound_marks(s, 760, 520), lambda s: f.shadow(s, 760, 900, 0.9, 200), f.Scene.vignette), "in"),
    # part 3
    ("Я села на кровати и спросила в темноту: кто здесь? Никто не ответил. Но скрип прекратился. Как будто кто-то замер.", sc(True, f.bedroom, lambda s: V(s, 420, 860, "scared", 1.0), f.Scene.vignette), "in"),
    ("Утром я развесила на всех дверях колокольчики. Если кто-то откроет дверь, я услышу.", sc(False, f.front_door, lambda s: f.bell(s, 540, 160), lambda s: V(s, 200, 1000, "calm", 0.8)), "left"),
    ("Две ночи было тихо. А на третью колокольчик на кухне звякнул. Один раз. Тихо, как будто его придержали рукой.", sc(True, f.kitchen, lambda s: f.bell(s, 300, 240, ring=True), lambda s: f.shadow(s, 700, 900), f.Scene.vignette), "in"),
    # part 4
    ("Я вызвала полицию. Приехала женщина-полицейский. Она проверила окна, замки, балкон. Всё было закрыто изнутри.", sc(False, f.front_door, lambda s: f.police(s, 760, 1000, "calm", 0.9), lambda s: V(s, 280, 1000, "sad", 0.9)), "out"),
    ("Она сказала очень мягко: может быть, вам показалось? Вы же одна, вам тревожно. Это нормально.", sc(False, f.room, lambda s: f.police(s, 700, 900, "calm"), lambda s: V(s, 360, 900, "sad")), "in"),
    ("Но мне не показалось. Когда она ушла, я поняла, что в коридоре снова пахнет тем одеколоном. Хотя дверь только что закрылась.", sc(True, f.hallway, lambda s: V(s, 540, 920, "scared"), f.Scene.vignette), "in"),
    # part 5
    ("На лестнице я встретила соседа, дядю Колю. Он живёт здесь сорок лет и знает про дом всё.", sc(False, f.stairwell, lambda s: f.neighbor(s, 700, 820, "calm", 0.9), lambda s: V(s, 380, 1000, "calm", 0.9)), "left"),
    ("Он сказал: до тебя в этой квартире жил мужчина. Тихий, одинокий. А потом он пропал. Квартиру продали очень быстро.", sc(False, f.stairwell, lambda s: f.neighbor(s, 600, 900, "sad", 1.1)), "in"),
    ("Его так и не нашли, сказал дядя Коля. Ни его, ни его вещей. Просто однажды он перестал выходить.", sc(True, f.stairwell, lambda s: f.shadow(s, 540, 760, 0.8, 150), f.Scene.vignette), "out"),
    # part 6
    ("Перестал выходить. Эти слова не выходили у меня из головы. Я вернулась домой и начала считать шаги. Заново.", sc(False, f.room, lambda s: V(s, 540, 900, "calm")), "left"),
    ("От двери до кухни — четырнадцать. От кухни до спальни — шесть. А коридор с кладовкой оказался на полметра короче, чем снаружи.", sc(False, f.hallway, lambda s: V(s, 540, 920, "scared")), "in"),
    ("Я открыла шкаф в кладовке, раздвинула одежду и постучала по задней стенке. Звук был пустой. Там была не стена.", sc(True, lambda s: f.closet(s, open_=True), lambda s: V(s, 180, 1000, "scared", 0.8), f.Scene.vignette), "in"),
    # part 7
    ("Я позвонила Лене и попросила приехать. Сразу. Не объясняя. Она приехала через двадцать минут.", sc(False, lambda s: f.phone_screen(s)), "out"),
    ("Лена отодвинула вешалки и замолчала. Потом сказала шёпотом: Вера, тут дверца. Маленькая. И из-под неё идёт свет.", sc(True, lambda s: f.closet(s, open_=True, hidden=True), lambda s: f.lena(s, 860, 1000, "shock", 0.8)), "in"),
    ("Мы открыли её вместе. Лена закричала. А я просто стояла и слушала, как она плачет и не может сказать ни слова.", sc(True, f.secret_room, lambda s: f.lena(s, 860, 1000, "shock", 0.9)), "in"),
    # part 8
    ("Там была узкая комната. Матрас, лампа, вода, консервы. А на стенах — сотни фотографий.", sc(True, f.secret_room), "left"),
    ("На всех фотографиях была я. Как я сплю. Как я готовлю. Как я стою у окна. Три года.", sc(True, f.secret_room, lambda s: V(s, 540, 1000, "shock", 0.9), f.Scene.vignette), "in"),
    ("Полиция нашла его через два часа. Он прятался на чердаке. Тот самый мужчина, который пропал три года назад.", sc(False, f.stairwell, lambda s: f.police(s, 380, 1000, "calm", 0.9), lambda s: f.stranger(s, 720, 840, 0.9)), "out"),
    # part 9
    ("Он не пытался убежать. Он сказал только одно: это моя квартира. Я просто не хотел уходить.", sc(True, f.room, lambda s: f.stranger(s, 540, 900, 1.1), f.Scene.vignette), "in"),
    ("Он жил за стеной всё это время. Ел мою еду, когда я спала. Переставлял кружку. Слушал, как я разговариваю сама с собой.", sc(True, f.kitchen, lambda s: f.table(s, 540, 900, cup=0), lambda s: f.shadow(s, 860, 900, 0.9, 180), f.Scene.vignette), "left"),
    ("Я переехала через неделю. Новая квартира, новые замки, новые соседи. Я снова выучила все шаги.", sc(False, f.room, lambda s: V(s, 420, 900, "happy"), lambda s: f.lena(s, 720, 900, "happy")), "out"),
    # part 10
    ("Но вчера утром я пришла на кухню и протянула руку к краю стола. Кружки там не было.", sc(False, f.kitchen, lambda s: f.table(s, 600, 900), lambda s: V(s, 250, 900, "scared")), "in"),
    ("Она стояла ровно в центре.", sc(True, f.kitchen, lambda s: f.table(s, 540, 900, cup=0), f.Scene.vignette), "in"),
    ("Как вы думаете, кто её переставил? Пишите в комментариях. И подпишитесь, чтобы не пропустить новую историю.", sc(True, f.room, lambda s: V(s, 420, 900, "scared"), lambda s: f.shadow(s, 860, 880, 0.9, 200), f.Scene.vignette), "out"),
]
PART_STARTS = [0, 4, 7, 10, 13, 16, 19, 22, 25, 28]   # segment index where each Short begins (each part >= 24 s)   # segment index where each Short begins
TITLE = "Я слепая и живу одна"


def part_overlay_ass(n, total_parts, dur, path):
    style = ("Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, "
             "Outline, Shadow, Alignment, MarginL, MarginR, MarginV")
    lines = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "", "[V4+ Styles]", style,
             f"Style: P,Montserrat Black,64,&H00FFFFFF,&H00000000,&H96000000,1,3,14,0,8,40,40,{SCENE_Y + 30}",
             f"Style: E,Montserrat Black,58,&H0000E5FF,&H00000000,&H96000000,1,3,14,0,8,40,40,{SCENE_Y + 30}",
             "", "[Events]", "Format: Layer, Start, End, Style, Text"]
    lines.append(f"Dialogue: 0,{ass_time(0)},{ass_time(2.5)},P,{TITLE.upper()}\\NЧАСТЬ {n}")
    if n < total_parts:
        lines.append(f"Dialogue: 0,{ass_time(max(0, dur - 2.0))},{ass_time(dur)},E,ПРОДОЛЖЕНИЕ — ЧАСТЬ {n + 1}")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser()
    for k in ("outdir", "banner", "voice", "font"):
        ap.add_argument(f"--{k}", required=True)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="blind_")
    fonts_dir = os.path.dirname(os.path.abspath(a.font))

    clips, wavs, segs, t = [], [], [], 0.0
    for i, (text, (night, draw), move) in enumerate(STORY):
        wav = os.path.join(tmp, f"s{i:02d}.wav")
        dur = tts(text, a.voice, wav) + 0.2
        s = f.Scene(night); draw(s)
        png = os.path.join(tmp, f"s{i:02d}.png"); s.save(png)
        clip = os.path.join(tmp, f"s{i:02d}.mp4"); ken_burns(png, dur, move, clip)
        clips.append(clip); wavs.append(wav); segs.append((t, dur, text)); t += dur
        print(f"scene {i + 1}/{len(STORY)} {dur:.1f}s", flush=True)
    total = t

    with open(os.path.join(tmp, "v.txt"), "w") as fh:
        fh.writelines(f"file '{c}'\n" for c in clips)
    scenes = os.path.join(tmp, "scenes.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "v.txt"), "-c", "copy", scenes])
    with open(os.path.join(tmp, "a.txt"), "w") as fh:
        for w, (_, dur, _) in zip(wavs, segs):
            fh.write(f"file '{w}'\nduration {dur:.3f}\n")
    voice = os.path.join(tmp, "voice.wav")
    run(["ffmpeg", "-y", *sum([["-i", w] for w in wavs], []), "-filter_complex",
         "".join(f"[{i}]apad=whole_dur={segs[i][1]:.3f}[a{i}];" for i in range(len(wavs)))
         + "".join(f"[a{i}]" for i in range(len(wavs))) + f"concat=n={len(wavs)}:v=0:a=1", voice])

    ass = os.path.join(tmp, "subs.ass")
    write_ass(segs, "Montserrat Black", ass)
    full = os.path.join(a.outdir, "full_5min.mp4")
    fc = (f"[0]split[sc][bgsrc];"
          f"[bgsrc]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30,eq=brightness=-0.2[bg];"
          f"[bg][sc]overlay=0:{SCENE_Y}[v1];"
          f"[1]fps={FPS},scale={W}:-1,format=rgba[ban];"
          f"[v1][ban]overlay=0:{BANNER_Y}:enable='gte(t,{BANNER_FROM})':shortest=1[v2];"
          f"[v2]ass={ass}:fontsdir={fonts_dir},format=yuv420p[v]")
    run(["ffmpeg", "-y", "-i", scenes, "-stream_loop", "-1", "-i", a.banner, "-i", voice,
         "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", f"{total:.3f}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
         "-movflags", "+faststart", full])
    print(f"full {total:.1f}s", flush=True)

    bounds = [segs[i][0] for i in PART_STARTS] + [total]
    for n in range(1, len(PART_STARTS) + 1):
        t0, t1 = bounds[n - 1], bounds[n]
        ov = os.path.join(tmp, f"p{n}.ass")
        part_overlay_ass(n, len(PART_STARTS), t1 - t0, ov)
        out = os.path.join(a.outdir, f"part_{n:02d}.mp4")
        run(["ffmpeg", "-y", "-ss", f"{t0:.3f}", "-i", full, "-t", f"{t1 - t0:.3f}",
             "-vf", f"ass={ov}:fontsdir={fonts_dir},format=yuv420p",
             "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
             "-movflags", "+faststart", out])
        print(f"part {n}: {t1 - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
