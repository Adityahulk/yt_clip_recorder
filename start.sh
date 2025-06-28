#!/bin/bash
Xvfb :99 -screen 0 1280x720x24 &
export DISPLAY=:99.0
pulseaudio --start
sleep 3
exec uvicorn main:app --host 0.0.0.0 --port 8000
