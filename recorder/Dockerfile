FROM python:3.10-slim

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
    && apt-get clean

# Set environment variable so pyppeteer knows where Chromium is
ENV PYPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
