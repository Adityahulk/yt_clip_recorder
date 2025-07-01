import os
import subprocess
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/")
async def download_full_video():
    yt_url = os.getenv("YT_URL")

    if not yt_url:
        return {"error": "Missing required environment variable: YT_URL"}

    try:
        output_template = "/tmp/video.%(ext)s"
        
        # Step 1: Download video
        subprocess.run(["yt-dlp", "-f", "best", "-o", output_template, yt_url], check=True)

        # Step 2: Detect actual downloaded file
        downloaded_file = None
        for ext in ["mp4", "webm", "mkv"]:
            path = f"/tmp/video.{ext}"
            if os.path.exists(path):
                downloaded_file = path
                break

        if not downloaded_file:
            raise Exception("Downloaded video file not found.")

        # Step 3: Open file stream and return
        def iterfile():
            with open(downloaded_file, mode="rb") as file:
                while chunk := file.read(1024 * 1024):  # 1MB chunks
                    yield chunk

        return StreamingResponse(iterfile(), media_type="video/mp4", headers={
            "Content-Disposition": 'attachment; filename="video.mp4"'
        })

    except subprocess.CalledProcessError as e:
        return {"error": f"Download failed: {e}"}
    except Exception as e:
        return {"error": str(e)}
