FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    chromium xvfb x11-utils libxext6 libxrender1 libxtst6 \
    libnss3 libasound2 libatk-bridge2.0-0 libgtk-3-0 libxss1 \
    && apt-get clean

ENV DISPLAY=:99.0

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
