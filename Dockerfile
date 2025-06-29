FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium ffmpeg xvfb pulseaudio x11-utils curl \
    libxext6 libxrender1 libxtst6 libnss3 libasound2 \
    libatk-bridge2.0-0 libgtk-3-0 libxss1 \
    libdbus-glib-1-2 libdrm2 libgbm1 libxcomposite1 \
    && apt-get clean

# Set env variables
ENV DISPLAY=:99.0
ENV PYPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Copy code
WORKDIR /app
COPY . .
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Launch services and FastAPI
CMD bash -c "\
    pulseaudio --system --disallow-exit --disable-shm & \
    sleep 2 && \
    Xvfb :99 -screen 0 1280x720x24 & \
    sleep 2 && \
    uvicorn main:app --host 0.0.0.0 --port 8000"