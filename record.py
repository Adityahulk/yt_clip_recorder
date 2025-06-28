import asyncio
from pyppeteer import launch
import subprocess
import os

async def record_youtube_clip(url: str, start: float, end: float, output_path: str):
    duration = end - start

    browser = await launch(headless=True, args=['--no-sandbox', '--disable-gpu'])
    page = await browser.newPage()
    await page.setViewport({'width': 1280, 'height': 720})

    await page.goto(url)
    await page.waitForSelector('video')

    await page.evaluate(f"""
        const video = document.querySelector('video');
        video.currentTime = {start};
        video.play();
    """)

    await asyncio.sleep(2)

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-video_size", "1280x720",
        "-f", "x11grab",
        "-i", os.environ.get("DISPLAY", ":99.0"),
        "-f", "pulse",
        "-i", "default",
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-c:a", "aac",
        "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    proc = subprocess.Popen(ffmpeg_cmd)
    await asyncio.sleep(duration + 2)
    proc.terminate()
    await browser.close()
