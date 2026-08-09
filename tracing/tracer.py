import asyncio
import functools
import json
import sys
import time
from datetime import datetime
from typing import Any, Callable

TRACE_LOG_FILE = "trace_log.json"


def log_trace(event: dict):
    """Write log events to stderr (using standard ASCII symbols) and append to trace_log.json."""
    print(
        f"\n[TRACE {event['timestamp']}] {event['agent_or_tool']} | Action: {event['action']} | Status: {event['status']}",
        file=sys.stderr,
    )
    if "duration_ms" in event:
        print(f"  |- Duration: {event['duration_ms']:.2f}ms", file=sys.stderr)
    if "inputs" in event:
        print(f"  |- Inputs: {event['inputs']}", file=sys.stderr)
    if "output" in event:
        print(f"  |- Output: {event['output']}", file=sys.stderr)

    try:
        try:
            with open(TRACE_LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []

        logs.append(event)
        with open(TRACE_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"Error saving trace log: {e}", file=sys.stderr)


def trace_tool(tool_name: str):
    """Decorator supporting both sync and async functions to log execution metrics."""

    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                start_time = time.time()
                timestamp = datetime.now().isoformat()
                inputs = {"args": [str(a) for a in args], "kwargs": kwargs}
                try:
                    result = await func(*args, **kwargs)
                    duration = (time.time() - start_time) * 1000
                    log_trace(
                        {
                            "timestamp": timestamp,
                            "agent_or_tool": tool_name,
                            "action": func.__name__,
                            "status": "SUCCESS",
                            "duration_ms": duration,
                            "inputs": inputs,
                            "output": str(result),
                        }
                    )
                    return result
                except Exception as e:
                    duration = (time.time() - start_time) * 1000
                    log_trace(
                        {
                            "timestamp": timestamp,
                            "agent_or_tool": tool_name,
                            "action": func.__name__,
                            "status": "FAILED",
                            "duration_ms": duration,
                            "inputs": inputs,
                            "error": str(e),
                        }
                    )
                    raise e

            return async_wrapper
        else:

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs) -> Any:
                start_time = time.time()
                timestamp = datetime.now().isoformat()
                inputs = {"args": [str(a) for a in args], "kwargs": kwargs}
                try:
                    result = func(*args, **kwargs)
                    duration = (time.time() - start_time) * 1000
                    log_trace(
                        {
                            "timestamp": timestamp,
                            "agent_or_tool": tool_name,
                            "action": func.__name__,
                            "status": "SUCCESS",
                            "duration_ms": duration,
                            "inputs": inputs,
                            "output": str(result),
                        }
                    )
                    return result
                except Exception as e:
                    duration = (time.time() - start_time) * 1000
                    log_trace(
                        {
                            "timestamp": timestamp,
                            "agent_or_tool": tool_name,
                            "action": func.__name__,
                            "status": "FAILED",
                            "duration_ms": duration,
                            "inputs": inputs,
                            "error": str(e),
                        }
                    )
                    raise e

            return sync_wrapper

    return decorator