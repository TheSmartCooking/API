#!/bin/sh
set -e

python3 -m utility.jwtoken.keys_rotation
exec python3 app.py
