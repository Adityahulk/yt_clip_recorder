from fastapi import FastAPI, Query, HTTPException
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
    if not (0 <= start < end <= 60):
        raise HTTPException(status_code=400, detail="Clip duration must be between 0–60s")

    filename = f"/tmp/clip_{uuid.uuid4().hex[:8]}.mp4"

    try:
        await record_youtube_clip(url, start, end, filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recording failed: {str(e)}")

    if not os.path.exists(filename):
        raise HTTPException(status_code=500, detail="Recording failed: clip not created")

    return FileResponse(
        path=filename,
        media_type="video/mp4",
        filename="clip.mp4",
        headers={"Content-Disposition": "inline; filename=clip.mp4"}
    )
