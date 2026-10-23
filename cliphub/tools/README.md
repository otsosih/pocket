# Генератор роликов ClipHub (без ИИ-кредитов)

Рисует сцены в блочном стиле кодом (Pillow), двигает камеру (zoompan), озвучивает офлайн (Piper),
добавляет субтитры по слову (ASS) и баннер ClipHub по макету из `../STYLE.md`.

## Что нужно
- ffmpeg с libass, Python 3, `pip install pillow piper-tts`
- Голос: https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-ru-irinia-medium.tar.gz
- Шрифт: https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-Black.ttf
- Баннер: `ClipHub_games.mov` (с прозрачностью) из папки ClipHub

## Запуск
```
python3 make_video.py --out out.mp4 --banner ClipHub_games.mov --voice ru-irinia-medium.onnx --font Montserrat-Black.ttf
```
История задаётся списком `(текст, функция-сцена, движение камеры)` — см. `DEMO_STORY`.
Ролики для ClipHub должны быть не короче 24 сек.

## Мужские голоса (Piper, зеркало на GitHub)
```
https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-ru_RU-denis-medium.tar.bz2
https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-ru_RU-ruslan-medium.tar.bz2
https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-ru_RU-dmitri-medium.tar.bz2
```
Основной голос сериала — denis (≈147 Гц, ближе всего к референсу). ruslan ниже (≈120 Гц).
`story_metro.py --pitch 0.917` дополнительно понижает голос, по умолчанию без сдвига.
