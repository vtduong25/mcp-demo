from fastmcp import FastMCP

mcp = FastMCP("Tutorial MCP Server")

@mcp.tool
def greet(name: str) -> str:
    """Greet a person by their name."""
    return f"Hello, {name}! Welcome to the FastMCP tutorial."

@mcp.tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def get_server_info() -> dict:
    """Get information about the MCP server."""
    return {
        "name": mcp.name,
        "version": mcp.version
    }

# ASGI app for gunicorn/uvicorn: gunicorn -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 server.tutorial:app
app = mcp.http_app()

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
