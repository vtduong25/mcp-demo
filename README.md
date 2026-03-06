# MCP Server Demo

A beginner-friendly demo of the **Model Context Protocol (MCP)** using [FastMCP](https://gofastmcp.com). This project runs a small MCP server that exposes three tools (`greet`, `add_numbers`, `get_server_info`) and shows how to call them from a test script, a CLI bot, and a web API.

## What is MCP?

**MCP (Model Context Protocol)** is a standard way for AI assistants and applications to talk to external tools and data. Think of it like this:

- **MCP server** — Exposes “tools” (functions) that can be run remotely. This project’s server is in `server/tutorial.py`.
- **MCP client** — Connects to a server and calls those tools. The test script, bot, and web app in this repo are all clients.

Your server runs in one process (e.g. one terminal). Your bot, web app, or another app runs in another process and connects to the server to use its tools.

## Prerequisites

- **Python 3.14+**  
  Check: `python3 --version`
- **uv** (Python package manager and runner)  
  Install: https://docs.astral.sh/uv/getting-started/installation/

Once `uv` is installed, you can use `uv run` to install dependencies and run scripts without manually creating a virtual environment.

## Project structure

| File | Purpose |
|------|--------|
| `main.py` | **All-in-one launcher** — Starts the MCP server, then shows a menu to run Bot, Web App, or test client. |
| `server/tutorial.py` | **MCP server** — Defines the tools and runs the server on port 8000 (SSE). |
| `client/test_tutorial_client.py` | **One-off test** — Connects to the server and calls each tool once. |
| `ui/bot.py` | **CLI bot** — Interactive prompt: type commands like `greet Alice` or `add 3 7`. |
| `ui/app.py` | **Web API** — FastAPI app that exposes the same tools as HTTP endpoints. |
| `run_server_and_bot.sh` | **Script** — Cleans port 8000, starts server, then runs the CLI bot. One terminal. |

You can run everything from **`main.py`**, use the **shell scripts** for server + bot or server + app, or run the **server** and **clients** manually in separate terminals.

## Setup (first time)

1. **Clone or open the project** and go into its directory:
   ```bash
   cd /path/to/mcp-server-demo
   ```

2. **Install dependencies** with uv (this creates a virtual environment and installs packages from `pyproject.toml`):
   ```bash
   uv sync
   ```
   You should see dependencies such as `fastmcp`, `mcp`, `fastapi`, and `uvicorn` being installed.

3. **Confirm Python version** (optional):
   ```bash
   uv run python --version
   ```
   The project expects Python 3.14 or newer.

## Quick start options

### Option A: main.py (menu)

One command starts the server and gives you a menu (Bot, Web App, test client, or Exit):

```bash
uv run python main.py
```

Choose **1** (Bot), **2** (Web App), **3** (test client), or **4** (Exit). When you exit the bot or stop the app, the menu returns. Choose **4** to stop the server.

### Option B: Shell scripts (server + bot or server + app)

**Server + CLI bot (one terminal):**
```bash
./run_server_and_bot.sh
```
Cleans port 8000, starts the server, then runs the bot. Type **`quit`** in the bot (or Ctrl+C) to exit; the server is stopped automatically.

**Server + Web app (one terminal):**
```bash
./run_server_and_app.sh
```
Cleans ports 8000 and 8001, starts the server, then runs the web app. Open http://127.0.0.1:8001/docs in your browser. Press **Ctrl+C** to stop the app and server.

### Option C: Manual (two terminals)

**Terminal 1 — start the server:**
```bash
uv run python server/tutorial.py
```

**Terminal 2 — run a client:**
```bash
uv run python client/test_tutorial_client.py   # one-off test
# or
uv run python ui/bot.py                        # CLI bot
# or
uv run uvicorn ui.app:app --reload --port 8001 # web app
```

## Running the MCP server manually

1. **Start the server** (leave this terminal open):
   ```bash
   uv run python server/tutorial.py
   ```

2. You should see something like:
   ```text
   FastMCP 2.x.x
   Server: Tutorial MCP Server
   ... Starting MCP server ... with transport 'sse' on http://127.0.0.1:8000/sse
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

3. The server listens at **http://127.0.0.1:8000/sse**. Clients must use this full URL (including `/sse`) when connecting via SSE.

## Testing the server

### One-off test script

```bash
uv run python client/test_tutorial_client.py
```

Expected output (or similar):

```text
Connecting to http://127.0.0.1:8000/sse
Tools: ['greet', 'add_numbers', 'get_server_info']

greet('World'): Hello, World! Welcome to the FastMCP tutorial.
add_numbers(3, 7): 10
get_server_info(): {'name': 'Tutorial MCP Server', 'version': '2.14.5'}
```

### CLI bot

```bash
uv run python ui/bot.py
```

At the `>` prompt: **`greet Alice`**, **`add 3 7`**, **`info`**, **`tools`**, **`quit`** or **`exit`**.

### Web API

```bash
uv run uvicorn ui.app:app --reload --port 8001
```

Then open: **http://127.0.0.1:8001/docs** (Swagger UI), **/greet/Alice**, **/add?a=3&b=7**, **/info**, **/tools**.

## Shutting down the MCP server

- **If you used main.py:** Choose **4 (Exit)** in the menu, or press **Ctrl+C**.
- **If you used a shell script:** Press **Ctrl+C** (or type **`quit`** in the bot); the script stops the server.
- **If you started the server in its own terminal:** Press **Ctrl+C** in that terminal.
- **Check if something is still on port 8000:** `lsof -i :8000`
- **Force-kill port 8000 (macOS/Linux):** `kill -9 $(lsof -t -i :8000)`

## Troubleshooting

- **“Address already in use” (port 8000 or 8001)**  
  Another process is using the port. Use the shell scripts (they clean ports first), or run `kill -9 $(lsof -t -i :8000)` (and same for 8001 if needed).

- **“Session terminated” or connection errors**  
  Use the full SSE URL: **`http://127.0.0.1:8000/sse`** (with `/sse`). Start the server before any client.

- **Server not running**  
  Start `server/tutorial.py` first (or use `main.py` or a shell script), then run a client.

- **httpx.ReadError / “Error in post_writer”**  
  The MCP server closed or crashed. Start the server again (ideally in a separate terminal to see errors).

## Next steps

- Add more tools in `server/tutorial.py` with `@mcp.tool` and call them from `ui/bot.py` or `ui/app.py`.
- Use this server as an MCP backend in Cursor or another MCP-compatible client at `http://127.0.0.1:8000/sse`.
- Read the [FastMCP docs](https://gofastmcp.com) for more transports and features.
