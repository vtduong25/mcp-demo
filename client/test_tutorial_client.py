"""
Test client for tutorial.py MCP server.

Usage:
  1. In one terminal: uv run python tutorial.py
  2. In another:     uv run python test_tutorial_client.py
"""

import asyncio
from fastmcp import Client

# Server must use /sse path for FastMCP SSE transport
SERVER_URL = "http://127.0.0.1:8000/sse"
client = Client(SERVER_URL)


async def main():
    print("Connecting to", SERVER_URL)
    async with client:
        tools = await client.list_tools()
        print("Tools:", [t.name for t in tools], "\n")

        r = await client.call_tool("greet", {"name": "World"})
        print("greet('World'):", r.data)

        r = await client.call_tool("add_numbers", {"a": 3, "b": 7})
        print("add_numbers(3, 7):", r.data)

        r = await client.call_tool("get_server_info", {})
        print("get_server_info():", r.data)


if __name__ == "__main__":
    asyncio.run(main())
