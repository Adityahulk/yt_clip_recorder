FROM python:3.10-slim

# Install system dependencies, including Chromium and FFmpeg
RUN apt-get update && apt-get install -y \
    chromium \
    ffmpeg \
    xvfb \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    libasound2 \
    libnss3 \
    libxss1 \
    libxtst6 \
    curl \
    && apt-get clean

# Set Chromium path for pyppeteer
ENV PYPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code
COPY . .

# Set display for Xvfb
ENV DISPLAY=:99.0

# Start Xvfb and the recorder
CMD bash -c "\
    Xvfb :99 -screen 0 1280x720x24 & \
    python record.py"
