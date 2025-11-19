#!/usr/bin/env sh
set -e

echo "🚀 Starting infinexpense API container"

# Wait for DB by retrying alembic quietly
echo "🔧 Waiting for database & running Alembic migrations..."

while true; do
  if alembic upgrade head >/tmp/alembic.log 2>&1; then
    echo "✅ Alembic migrations applied."
    break
  else
    echo "⏳ DB not ready yet, retrying in 3s..."
    sleep 3
  fi
done

echo "📄 Generating sample.json..."
python -m src.scripts.load_json_to_db --generate sample.json --products 200 --receipts 20

echo "📥 Loading sample.json..."
python -m src.scripts.load_json_to_db sample.json

echo "✅ DB ready, starting uvicorn..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
