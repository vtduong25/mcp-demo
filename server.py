"""MCP server - runs over HTTP on port 8000."""

from fastmcp import FastMCP

mcp = FastMCP("MCP Demo Server")


@mcp.tool
def greet(name: str) -> str:
    """Greet a person by their name."""
    return f"Hello, {name}! Welcome to the MCP server."


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


app = mcp.http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
