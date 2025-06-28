FROM python:3.10-slim

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg xvfb pulseaudio x11-utils wget unzip curl \
    libxext6 libxrender1 libxtst6 libnss3 libasound2 \
    && apt-get clean

# Set display for Xvfb
ENV DISPLAY=:99.0

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
WORKDIR /app
COPY . .

# Start Xvfb + Pulse + FastAPI
CMD bash -c "\
    pulseaudio --start && \
    Xvfb :99 -screen 0 1280x720x24 & \
    uvicorn main:app --host 0.0.0.0 --port 8000"
