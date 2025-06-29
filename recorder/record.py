import asyncio
from pyppeteer import launch
import subprocess
import os

async def record_youtube_clip(url: str, start: float, end: float, output_path: str):
    duration = end - start

    browser = await launch({
        "executablePath": "/usr/bin/chromium",
        "headless": True,
        "args": [
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--autoplay-policy=no-user-gesture-required",
            "--window-size=1280,720"
        ]
    })

    try:
        page = await browser.newPage()
        await page.goto(url)
        await page.waitForSelector('video')
        await page.evaluate(f'''
            const video = document.querySelector('video');
            video.currentTime = {start};
            video.play();
        ''')
        await asyncio.sleep(3)

        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-f", "x11grab",
            "-video_size", "1280x720",
            "-i", os.environ.get("DISPLAY", ":99.0"),
            "-t", str(duration),
            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            output_path
        ]

        proc = subprocess.Popen(ffmpeg_cmd)
        await asyncio.sleep(duration + 2)
        proc.terminate()

        if not os.path.exists(output_path):
            raise Exception("Recording failed")

    finally:
        await browser.close()
