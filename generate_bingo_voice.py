# -*- coding: utf-8 -*-
"""
يولّد 75 مقطع صوتي (صوت رجال جهوري وواضح) للعبة بينغو: 1.mp3 ... 75.mp3
التشغيل (مرة وحدة، على جهازك أو السيرفر، لازم إنترنت):

    pip install edge-tts
    python generate_bingo_voice.py            (الصوت الافتراضي)
    python generate_bingo_voice.py en-US-GuyNeural   (أو أي صوت من voice_samples.py)

بيطلع مجلد باسم bingo_voice. ارفعه على GitHub بنفس مكان bingo.html
(يعني: siiiifo.github.io/loom/bingo_voice/1.mp3 ...)
"""
import asyncio, os, shutil, subprocess, sys
import edge_tts

VOICE  = sys.argv[1] if len(sys.argv) > 1 else "en-US-ChristopherNeural"   # مثال: python generate_bingo_voice.py en-US-GuyNeural
RATE   = "-8%"                       # أبطأ شوي = أوضح
PITCH  = "-6Hz"                      # أغلظ بدون ما يصير مخنوق
VOLUME = "+30%"
OUT    = "bingo_voice"
WORD   = {"B": "Bee", "I": "Eye", "N": "Enn", "G": "Gee", "O": "Oh"}


def letter(n):
    return "BINGO"[min(4, (n - 1) // 15)]


async def make(n):
    path = os.path.join(OUT, f"{n}.mp3")
    text = f"{WORD[letter(n)]}. {n}."
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH, volume=VOLUME).save(path)
            return
        except Exception as e:
            print(f"  محاولة {attempt + 1} فشلت للرقم {n}: {e}")
            await asyncio.sleep(2)
    print(f"✗ تعذّر توليد {n}")


def boost(path):
    """رفع علوّ الصوت وتوحيده (اختياري، يحتاج ffmpeg)."""
    tmp = path + ".tmp.mp3"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path,
                        "-af", "loudnorm=I=-14:TP=-1:LRA=7", "-b:a", "96k", tmp])
    if r.returncode == 0 and os.path.exists(tmp):
        os.replace(tmp, path)


async def main():
    os.makedirs(OUT, exist_ok=True)
    for n in range(1, 76):
        await make(n)
        print(f"✓ {n}/75", flush=True)
    if shutil.which("ffmpeg"):
        print("رفع وتوحيد علوّ الصوت...")
        for n in range(1, 76):
            p = os.path.join(OUT, f"{n}.mp3")
            if os.path.exists(p):
                boost(p)
    print(f"خلاص! ارفع مجلد {OUT} بجانب bingo.html")


asyncio.run(main())
