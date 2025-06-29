from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from record import record_youtube_clip
import uuid
import os

app = FastAPI()

@app.get("/record_clip")
async def record_clip(
    url: str = Query(...),
    start: float = Query(...),
    end: float = Query(...)
):
    output_file = f"clip_{uuid.uuid4().hex[:8]}.mp4"
    await record_youtube_clip(url, start, end, output_file)

    return FileResponse(path=output_file, filename="clip.mp4", media_type="video/mp4")
