import asyncio
from pyppeteer import launch
import subprocess
import os

async def record_youtube_clip(url: str, start: float, end: float, output_path: str):
    duration = end - start
    abs_output = os.path.abspath(output_path)

    browser = await launch(
        executablePath="/usr/bin/chromium",  # Use system Chromium
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--mute-audio",
            "--window-size=1280,720",
        ]
    )
    page = await browser.newPage()
    await page.setViewport({"width": 1280, "height": 720})
    await page.goto(url)
    await page.waitForSelector("video")

    await page.evaluate(f"""
        const video = document.querySelector("video");
        video.currentTime = {start};
        video.muted = false;
        video.play();
    """)

    await asyncio.sleep(3)  # Let video load and render

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-loglevel", "error",
        "-probesize", "50M",
        "-f", "x11grab",
        "-video_size", "1280x720",
        "-i", os.environ.get("DISPLAY", ":99.0"),
        "-f", "pulse",
        "-i", "default",
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-c:a", "aac",
        "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        abs_output
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    await browser.close()

    if not os.path.exists(abs_output):
        raise RuntimeError("Recording failed: clip not created")
