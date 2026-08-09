import sys
from pathlib import Path

project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastmcp import FastMCP
from tracing.tracer import trace_tool

mcp = FastMCP("ArbisoftDemoServer")


@mcp.resource("config://app-status")
def get_system_status() -> str:
    return "Status: Active | Phase: Phase 2 Agentic AI | Target: Week 5 First Half"


@mcp.tool()
@trace_tool("MCP_Tool_AnalyzeText")
def analyze_text(content: str) -> dict:
    words = len(content.split())
    chars = len(content)
    sentences = content.count(".") + content.count("!") + content.count("?")

    return {
        "word_count": words,
        "char_count": chars,
        "sentence_count": max(sentences, 1) if content else 0,
    }


if __name__ == "__main__":
    mcp.run()