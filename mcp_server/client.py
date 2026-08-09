import asyncio
from pathlib import Path

from fastmcp import Client


async def main() -> None:
    server_path = Path(__file__).with_name("server.py")

    async with Client(str(server_path)) as client:
        print("Connected to MCP server.")

        tools = await client.list_tools()
        resources = await client.list_resources()
        print("Tools:", tools)
        print("Resources:", resources)

        status = await client.read_resource("config://app-status")
        print("Resource result:", status)

        analysis = await client.call_tool(
            "analyze_text",
            {"content": "MCP is the protocol for tool and resource exposure."},
        )
        print("Tool result:", analysis)


if __name__ == "__main__":
    asyncio.run(main())
