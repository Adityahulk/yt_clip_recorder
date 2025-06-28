FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    xvfb \
    pulseaudio \
    x11-utils \
    libx11-dev \
    libasound2 \
    fonts-liberation \
    curl \
    wget \
    unzip \
    && apt-get clean

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x start.sh
CMD ["./start.sh"]
