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
    assert 0 <= start < end <= 60, "Clip duration must be between 0–60s"

    filename = f"clip_{uuid.uuid4().hex[:8]}.mp4"
    await record_youtube_clip(url, start, end, filename)

    response = FileResponse(
        path=filename,
        media_type="video/mp4",
        filename="clip.mp4",
        headers={"Content-Disposition": "inline; filename=clip.mp4"}
    )

    return response
