#!/bin/bash
Xvfb :99 -screen 0 1280x720x24 &
exec tail -f /dev/null
