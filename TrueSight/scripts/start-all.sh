#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MODEL_DIR="$ROOT_DIR/ai-model"
MODEL_APP="$MODEL_DIR/app.py"
PY_BIN="${PYTHON_BIN:-python3.11}"

is_port_in_use() {
  local port="$1"
  lsof -iTCP:"$port" -sTCP:LISTEN -t >/dev/null 2>&1
}

pick_model_port() {
  local preferred="${MODEL_PORT:-5000}"
  local port="$preferred"

  while is_port_in_use "$port"; do
    port=$((port + 1))
    if [[ "$port" -gt 5010 ]]; then
      echo "Error: no free model port found between $preferred and 5010"
      exit 1
    fi
  done

  echo "$port"
}

pick_backend_port() {
  local preferred="${BACKEND_PORT:-8080}"
  local port="$preferred"

  while is_port_in_use "$port"; do
    port=$((port + 1))
    if [[ "$port" -gt 8090 ]]; then
      echo "Error: no free backend port found between $preferred and 8090"
      exit 1
    fi
  done

  echo "$port"
}

if ! command -v "$PY_BIN" >/dev/null 2>&1; then
  echo "Error: $PY_BIN not found. Install Python 3.11 or set PYTHON_BIN to a valid interpreter."
  exit 1
fi

if [[ ! -f "$MODEL_APP" ]]; then
  echo "Error: Model app not found at $MODEL_APP"
  exit 1
fi

MODEL_PATH_DEFAULT="$ROOT_DIR/../trained-model/model.keras"
MODEL_PATH_EFFECTIVE="${MODEL_PATH:-$MODEL_PATH_DEFAULT}"
MODEL_PORT_EFFECTIVE="$(pick_model_port)"
AI_MODEL_URL_EFFECTIVE="http://127.0.0.1:${MODEL_PORT_EFFECTIVE}/predict"
BACKEND_PORT_EFFECTIVE="$(pick_backend_port)"

if [[ ! -f "$MODEL_PATH_EFFECTIVE" ]]; then
  echo "Warning: model file not found at $MODEL_PATH_EFFECTIVE"
  echo "Set MODEL_PATH to your trained model file path if different."
fi

cleanup() {
  local exit_code=$?

  if [[ -n "${NODE_PID:-}" ]] && kill -0 "$NODE_PID" >/dev/null 2>&1; then
    kill "$NODE_PID" >/dev/null 2>&1 || true
  fi

  if [[ -n "${PY_PID:-}" ]] && kill -0 "$PY_PID" >/dev/null 2>&1; then
    kill "$PY_PID" >/dev/null 2>&1 || true
  fi

  wait >/dev/null 2>&1 || true
  exit "$exit_code"
}

trap cleanup INT TERM EXIT

(
  cd "$MODEL_DIR"
  MODEL_PATH="$MODEL_PATH_EFFECTIVE" MODEL_PORT="$MODEL_PORT_EFFECTIVE" "$PY_BIN" app.py
) &
PY_PID=$!

echo "AI model server started (PID: $PY_PID, port: $MODEL_PORT_EFFECTIVE)"

(
  cd "$ROOT_DIR"
  AI_MODEL_URL="$AI_MODEL_URL_EFFECTIVE" PORT="$BACKEND_PORT_EFFECTIVE" node backend/server.js
) &
NODE_PID=$!

echo "Backend server started (PID: $NODE_PID)"
echo "App URL: http://localhost:${BACKEND_PORT_EFFECTIVE}"
echo "AI model URL: $AI_MODEL_URL_EFFECTIVE"

while kill -0 "$PY_PID" >/dev/null 2>&1 && kill -0 "$NODE_PID" >/dev/null 2>&1; do
  sleep 1
done
