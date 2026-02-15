#!/usr/bin/env bash
# Run the MCP server, then the CLI bot.
# Usage: ./run_server_and_bot.sh
# When you exit the bot (quit), the server is stopped.

set -e
cd "$(dirname "$0")"

# Clean up port 8000 so the server can bind
if lsof -i :8000 -t >/dev/null 2>&1; then
  echo "Cleaning up port 8000 ..."
  for pid in $(lsof -i :8000 -t); do kill -9 "$pid" 2>/dev/null || true; done
  sleep 2
fi

echo "Starting MCP server ..."
uv run python server/tutorial.py &
SERVER_PID=$!

# Wait for server to be ready (port 8000 open)
for i in {1..15}; do
  if lsof -i :8000 -t >/dev/null 2>&1; then
    echo "MCP server ready at http://127.0.0.1:8000/sse"
    break
  fi
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "Server exited unexpectedly." >&2
    exit 1
  fi
  sleep 1
done

if ! lsof -i :8000 -t >/dev/null 2>&1; then
  kill "$SERVER_PID" 2>/dev/null || true
  echo "Server did not become ready in time." >&2
  exit 1
fi

# Run the bot in foreground; when it exits, kill the server
cleanup() {
  echo "Stopping MCP server (PID $SERVER_PID) ..."
  kill "$SERVER_PID" 2>/dev/null || true
  exit 0
}
trap cleanup EXIT INT TERM

uv run python ui/bot.py
