import os
import subprocess
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def clip_video():
    yt_url = os.environ.get("YT_URL")
    start = os.environ.get("START")
    end = os.environ.get("END")

    if not yt_url or not start or not end:
        return {"error": "Missing required environment variables (YT_URL, START, END)"}

    try:
        output_path = "/tmp/output.mp4"
        temp_path = "/tmp/temp.%(ext)s"

        # Step 1: Download the video
        subprocess.run(["yt-dlp", "-f", "best", "-o", temp_path, yt_url], check=True)

        # Detect the downloaded file
        downloaded_file = None
        for ext in ["mp4", "webm", "mkv"]:
            path = f"/tmp/temp.{ext}"
            if os.path.exists(path):
                downloaded_file = path
                break
        if not downloaded_file:
            raise Exception("Downloaded video file not found.")

        # Step 2: Clip using FFmpeg
        subprocess.run([
            "ffmpeg", "-y",
            "-ss", str(start), "-to", str(end),
            "-i", downloaded_file,
            "-c:v", "libx264", "-c:a", "aac",
            output_path
        ], check=True)

        # Return clip as response
        return FileResponse(output_path, media_type="video/mp4", filename="clip.mp4")

    except subprocess.CalledProcessError as e:
        return {"error": f"Subprocess failed: {e}"}
    except Exception as e:
        return {"error": str(e)}
