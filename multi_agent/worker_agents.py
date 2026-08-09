from typing import Any
from fastmcp import Client
from mcp_server.server import mcp
from tracing.tracer import trace_tool


@trace_tool("MCP_Client")
async def call_mcp_tool(client: Client, tool_name: str, arguments: dict) -> Any:
    """Explicitly traced wrapper around MCP client tool invocations."""
    return await client.call_tool(tool_name, arguments)


class SearchWorker:
    """Worker sub-agent 1: Handles mock data search and lookup operations."""

    @trace_tool("Worker_Search")
    def execute_search(self, query: str) -> str:
        data_store = {
            "mcp": "Model Context Protocol (MCP) standardizes agent tool and resource exposure.",
            "supervisor": "Supervisor routing pattern distributes sub-tasks across worker agents.",
            "tracing": "Tracing logs tool call graphs with timestamps for execution replay.",
        }

        for key, info in data_store.items():
            if key in query.lower():
                return f"Match found for '{key}': {info}"

        return f"No exact match found in database for query: '{query}'"


class TextProcessorWorker:
    """Worker sub-agent 2: Uses the FastMCP client to analyze text via MCP server."""

    @trace_tool("Worker_TextProcessor")
    async def process_text(self, text: str) -> dict:
        """Calls the MCP analyze_text tool through the FastMCP client."""
        async with Client(mcp) as client:
            result = await call_mcp_tool(
                client,
                "analyze_text",
                {"content": text},
            )

            mcp_analysis = result.data if hasattr(result, "data") else result

            return {
                "raw_text": text,
                "mcp_analysis": mcp_analysis,
                "uppercase_version": text.upper(),
            }