FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium ffmpeg xvfb pulseaudio x11-utils wget unzip curl \
    libxext6 libxrender1 libxtst6 libnss3 libasound2 \
    fonts-liberation libatk-bridge2.0-0 libgtk-3-0 libxss1 \
    libdbus-glib-1-2 libdrm2 libgbm1 libxcomposite1 \
    && apt-get clean

# Set display
ENV DISPLAY=:99.0

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
WORKDIR /app
COPY . .

# Use system Chromium path
ENV PYPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Launch all services
CMD bash -c "\
    pulseaudio --start && \
    Xvfb :99 -screen 0 1280x720x24 & \
    uvicorn main:app --host 0.0.0.0 --port 8000"
