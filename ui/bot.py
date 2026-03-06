"""
Simple CLI bot that calls the tutorial MCP server tools.

Start the MCP server first, then run the bot:

  Terminal 1: uv run python tutorial.py
  Terminal 2: uv run python bot.py

Commands:
  greet <name>     — e.g. greet Alice
  add <a> <b>      — e.g. add 3 7
  info             — server info
  tools            — list tools
  quit / exit      — exit
"""

import asyncio
import shlex
import sys

from fastmcp import Client

MCP_URL = "http://127.0.0.1:8000/mcp"
client = Client(MCP_URL)


async def run_bot():
    print("Connecting to MCP server at", MCP_URL, "...")
    async with client:
        print("Connected. Commands: greet <name> | add <a> <b> | info | tools | quit\n")

        while True:
            try:
                line = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not line:
                continue

            parts = shlex.split(line)
            cmd = (parts[0] or "").lower()
            args = parts[1:]

            try:
                if cmd in ("quit", "exit", "q"):
                    break
                if cmd == "greet":
                    name = args[0] if args else "World"
                    r = await client.call_tool("greet", {"name": name})
                    print(r.data)
                elif cmd == "add":
                    a, b = int(args[0]), int(args[1]) if len(args) >= 2 else (0, 0)
                    r = await client.call_tool("add_numbers", {"a": a, "b": b})
                    print(r.data)
                elif cmd == "info":
                    r = await client.call_tool("get_server_info", {})
                    print(r.data)
                elif cmd == "tools":
                    tools = await client.list_tools()
                    for t in tools:
                        print(f"  {t.name}: {t.description}")
                else:
                    print("Unknown command. Use: greet <name> | add <a> <b> | info | tools | quit")
            except Exception as e:
                print("Error:", e)

        print("Bye.")


if __name__ == "__main__":
    asyncio.run(run_bot())
    sys.exit(0)
