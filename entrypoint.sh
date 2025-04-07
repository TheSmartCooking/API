#!/bin/sh

set -e  # Exit if any command fails

KEY_DIR="/app/keys"
PRIVATE_KEY="$KEY_DIR/private_key.pem"
PUBLIC_KEY="$KEY_DIR/public_key.pem"

mkdir -p "$KEY_DIR"

if [ ! -f "$PRIVATE_KEY" ] || [ ! -f "$PUBLIC_KEY" ]; then
  echo "🔐 Generating RSA key pair..."
  openssl genpkey -algorithm RSA -out "$PRIVATE_KEY" -pkeyopt rsa_keygen_bits:2048
  openssl rsa -pubout -in "$PRIVATE_KEY" -out "$PUBLIC_KEY"
else
  echo "✅ Keys already exist. Skipping generation."
fi

# Start your Python app
exec python3 app.py
