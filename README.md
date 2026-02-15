# MCP Server Demo

A beginner-friendly demo of the **Model Context Protocol (MCP)** using [FastMCP](https://gofastmcp.com). This project runs a small MCP server that exposes three tools (`greet`, `add_numbers`, `get_server_info`) and shows how to call them from a test script, a CLI bot, and a web API.

## What is MCP?

**MCP (Model Context Protocol)** is a standard way for AI assistants and applications to talk to external tools and data. Think of it like this:

- **MCP server** — Exposes “tools” (functions) that can be run remotely. This project’s server is in `tutorial.py`.
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
| `tutorial.py` | **MCP server** — Defines the tools and runs the server on port 8000 (SSE). |
| `test_tutorial_client.py` | **One-off test** — Connects to the server and calls each tool once. |
| `bot.py` | **CLI bot** — Interactive prompt: type commands like `greet Alice` or `add 3 7`. |
| `app.py` | **Web API** — FastAPI app that exposes the same tools as HTTP endpoints. |

You always run the **server** first (`tutorial.py`). Then you run one or more **clients** (test script, bot, or web app) that connect to it.

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

## Running the MCP server

The server must be running before any client can use its tools.

1. **Start the server** (leave this terminal open):
   ```bash
   uv run python tutorial.py
   ```

2. You should see something like:
   ```text
   FastMCP 2.x.x
   Server: Tutorial MCP Server
   ... Starting MCP server ... with transport 'sse' on http://127.0.0.1:8000/sse
   INFO:     Started server process ...
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

3. **Important:** The server listens at **http://127.0.0.1:8000/sse**. Clients must use this full URL (including `/sse`) when connecting via SSE.

4. Leave this process running. Use a **second terminal** for the next steps.

## Testing the server

Pick one of the following. Each one is a **client** that talks to the server you started above.

### Option 1: One-off test script

Runs once, calls all three tools, and exits.

```bash
# In a second terminal (server still running in the first)
uv run python test_tutorial_client.py
```

Expected output (or similar):

```text
Connecting to http://127.0.0.1:8000/sse
Tools: ['greet', 'add_numbers', 'get_server_info']

greet('World'): Hello, World! Welcome to the FastMCP tutorial.
add_numbers(3, 7): 10
get_server_info(): {'name': 'Tutorial MCP Server', 'version': '2.14.5'}
```

### Option 2: CLI bot (interactive)

Lets you type commands that map to the server’s tools.

1. With the server still running, in another terminal:
   ```bash
   uv run python bot.py
   ```

2. At the `>` prompt you can run:
   - **Greet:** `greet Alice` → `Hello, Alice! Welcome to the FastMCP tutorial.`
   - **Add numbers:** `add 3 7` → `10`
   - **Server info:** `info` → name and version of the server
   - **List tools:** `tools` → lists available tools
   - **Exit:** `quit` or `exit`

3. Example session:
   ```text
   > greet Bob
   Hello, Bob! Welcome to the FastMCP tutorial.
   > add 10 20
   30
   > quit
   Bye.
   ```

### Option 3: Web API

Run a small FastAPI app that exposes the same tools as HTTP endpoints.

1. With the server still running, in another terminal:
   ```bash
   uv run uvicorn app:app --reload --port 8001
   ```

2. Open in a browser or call with curl:
   - **Swagger UI:** http://127.0.0.1:8001/docs  
   - **Greet:** http://127.0.0.1:8001/greet/Alice  
   - **Add:** http://127.0.0.1:8001/add?a=3&b=7  
   - **Server info:** http://127.0.0.1:8001/info  
   - **List tools:** http://127.0.0.1:8001/tools  

The web app keeps a single connection to the MCP server and uses it to call the tools for each request.

## Summary: two terminals

For any client to work, you need:

| Terminal 1 | Terminal 2 |
|------------|------------|
| `uv run python tutorial.py` (server) | `uv run python test_tutorial_client.py` **or** `uv run python bot.py` **or** `uv run uvicorn app:app --reload --port 8001` |

The server runs on port **8000**. The web app (if you use it) runs on port **8001** so it doesn’t conflict.

## Troubleshooting

- **“Address already in use” (port 8000)**  
  Another process is already using port 8000. Stop that process, or change the port in `tutorial.py` (e.g. `mcp.run(transport="sse", port=8001)`) and in clients use `http://127.0.0.1:8001/sse`.

- **“Session terminated” or connection errors from a client**  
  Make sure the client uses the full SSE URL: **`http://127.0.0.1:8000/sse`** (with `/sse` at the end). The FastMCP client needs this path to use the SSE transport.

- **Server not running**  
  Start `tutorial.py` first and leave it running before starting any client.

## Next steps

- Add more tools in `tutorial.py` with `@mcp.tool` and call them from `bot.py` or `app.py`.
- Use this server as an MCP backend in Cursor or another MCP-compatible client by pointing it at `http://127.0.0.1:8000/sse`.
- Read the [FastMCP docs](https://gofastmcp.com) for more transports (e.g. stdio) and features.
