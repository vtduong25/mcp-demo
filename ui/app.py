"""
Web server that uses the tutorial MCP server tools.

Start the MCP server first, then run this app:

  Terminal 1: uv run python tutorial.py
  Terminal 2: uv run uvicorn app:app --reload --port 8001

Then open:
  http://127.0.0.1:8001/docs          — Swagger UI
  http://127.0.0.1:8001/greet/Alice   — GET /greet/{name}
  http://127.0.0.1:8001/add?a=3&b=7  — GET /add
  http://127.0.0.1:8001/info          — GET /info
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

from fastmcp import Client

MCP_URL = "http://127.0.0.1:8000/mcp"
mcp_client = Client(MCP_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Connect to MCP server on startup, disconnect on shutdown."""
    async with mcp_client:
        yield


app = FastAPI(
    title="MCP Bot API",
    description="Test endpoints that call the tutorial MCP server tools.",
    lifespan=lifespan,
)


@app.get("/greet/{name}", response_class=PlainTextResponse)
async def greet(name: str) -> str:
    """Greet someone by name (uses MCP tool)."""
    result = await mcp_client.call_tool("greet", {"name": name})
    return str(result.data)


@app.get("/add", response_class=PlainTextResponse)
async def add(a: int, b: int) -> str:
    """Add two numbers (uses MCP tool)."""
    result = await mcp_client.call_tool("add_numbers", {"a": a, "b": b})
    return str(result.data)


@app.get("/info")
async def info() -> dict:
    """Return MCP server info (uses MCP tool)."""
    result = await mcp_client.call_tool("get_server_info", {})
    return result.data if isinstance(result.data, dict) else {"info": result.data}


@app.get("/tools")
async def list_tools() -> list[dict]:
    """List available MCP tools."""
    tools = await mcp_client.list_tools()
    return [{"name": t.name, "description": t.description} for t in tools]


@app.get("/health")
async def health() -> dict:
    """Health check (does not call MCP)."""
    return {"status": "ok"}
