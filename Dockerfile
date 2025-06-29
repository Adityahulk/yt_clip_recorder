FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium ffmpeg xvfb pulseaudio x11-utils curl \
    libxext6 libxrender1 libxtst6 libnss3 libasound2 \
    libatk-bridge2.0-0 libgtk-3-0 libxss1 \
    libdbus-glib-1-2 libdrm2 libgbm1 libxcomposite1 \
    && apt-get clean

# Set env variables
# Set env variables
ENV DISPLAY=:99.0
ENV PYPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

RUN mkdir -p /run/pulse
RUN apt-get install -y alsa-utils
RUN echo "load-module module-null-sink sink_name=dummy" >> /etc/pulse/default.pa
ENV PULSE_SERVER=unix:/run/pulse/native


# Copy code
WORKDIR /app
COPY . .
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Launch all services
CMD bash -c "\
  pulseaudio --start --exit-idle-time=-1 --system=true --disallow-exit --disable-shm --no-cpu-limit --verbose & \
  sleep 2 && \
  Xvfb :99 -screen 0 1280x720x24 & \
  sleep 2 && \
  uvicorn main:app --host 0.0.0.0 --port 8000"
