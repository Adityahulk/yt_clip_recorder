import asyncio
from pyppeteer import launch
import subprocess
import os

async def record_youtube_clip(url: str, start: float, end: float, output_path: str):
    duration = end - start
    abs_output = os.path.abspath(output_path)

    browser = await launch(
        executablePath="/usr/bin/chromium",
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--window-size=1280,720",
            "--autoplay-policy=no-user-gesture-required",
        ]
    )
    try:
        page = await browser.newPage()
        await page.setViewport({"width": 1280, "height": 720})
        await page.setUserAgent("Mozilla/5.0")

        await page.goto(url, {"timeout": 60000, "waitUntil": "networkidle2"})
        await asyncio.sleep(2)
        await page.waitForSelector("video")

        await page.evaluate(f"""
            const video = document.querySelector("video");
            video.currentTime = {start};
            video.muted = false;
            video.play();
        """)

        await asyncio.sleep(2)  # Buffer time

        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-f", "x11grab",
            "-video_size", "1280x720",
            "-i", os.environ.get("DISPLAY", ":99.0"),
            "-f", "pulse",
            "-i", "dummy.monitor",
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            abs_output
        ]

        proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        await asyncio.sleep(duration + 2)
        proc.terminate()
        stdout, stderr = proc.communicate()

        if not os.path.exists(abs_output):
            raise RuntimeError(f"Recording failed: clip not created\n\nFFmpeg Error:\n{stderr.decode()}")

    finally:
        await browser.close()