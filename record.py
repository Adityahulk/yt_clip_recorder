import asyncio
from pyppeteer import launch
import subprocess
import os
import uuid

async def record_youtube_clip(url: str, start: float, end: float, output_path: str):
    duration = end - start
    abs_output = os.path.abspath(output_path)

    browser = await launch(
        headless=True,
        args=[
            '--no-sandbox',
            '--autoplay-policy=no-user-gesture-required',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--mute-audio'
        ]
    )
    page = await browser.newPage()
    await page.setViewport({'width': 1280, 'height': 720})

    await page.goto(url)
    await page.waitForSelector("video")

    # Seek and play
    await page.evaluate(f"""
        const video = document.querySelector("video");
        video.currentTime = {start};
        video.muted = true;
        video.play();
    """)

    # Wait to stabilize rendering
    await asyncio.sleep(2)

    # FFmpeg screen + audio recording
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-probesize", "50M",
        "-f", "x11grab",
        "-video_size", "1280x720",
        "-i", os.environ.get("DISPLAY", ":99.0"),
        "-f", "pulse",
        "-i", "default",
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        abs_output
    ]

    proc = subprocess.Popen(ffmpeg_cmd)

    # Wait for full duration to capture clip
    await asyncio.sleep(duration + 1)
    proc.terminate()

    await browser.close()

    if not os.path.exists(abs_output):
        raise RuntimeError("Recording failed: clip not created")
