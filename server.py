from fastmcp import FastMCP
import json

mcp = FastMCP("Rebrickable MCP")

# ---------------------------
# Hello World, v0
# ---------------------------
@mcp.tool
def hello(name: str) -> str:
    return f"Hey! What's up {name}?"

@mcp.resource("greeting://{name}", description="Read-only greeting resource")
def greeting_resource(name: str) -> str:
    return f"Hey! Resource says {name} was here!"

# ---------------------------
# ASGI app initialization
# ---------------------------
app = mcp.http_app()

if __name__ == "__main__":
    import uvicorn
    # -- local STDIO v0
    #mcp.run()
    # local server running on port 8000 v1
    #mcp.run(transport="http", host="127.0.0.1", port=8000)
    # -- https ASGI Streamable v2
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)
    
    