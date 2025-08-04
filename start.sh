#!/bin/bash
set -e
export PORT=${PORT:-3000}

echo "🔧 Exporting Reflex production build..."
reflex export --env prod

echo "🚀 Starting Reflex production server on port $PORT..."
python .web/main.py --port $PORT --host 0.0.0.0
