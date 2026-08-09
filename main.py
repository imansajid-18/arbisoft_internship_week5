import asyncio
from multi_agent.worker_agents import SearchWorker, TextProcessorWorker
from tracing.tracer import trace_tool


class SupervisorAgent:
    """Orchestrator agent that inspects query intent and routes to sub-agents."""

    def __init__(self):
        self.search_worker = SearchWorker()
        self.text_worker = TextProcessorWorker()

    @trace_tool("SupervisorAgent")
    async def route_and_execute(self, user_query: str, task_type: str) -> dict:
        """Determines routing destination based on task category."""
        if task_type == "search":
            result = self.search_worker.execute_search(user_query)
            return {"routed_to": "SearchWorker", "result": result}
        elif task_type == "text_processing":
            result = await self.text_worker.process_text(user_query)
            return {"routed_to": "TextProcessorWorker", "result": result}
        else:
            raise ValueError(f"Unknown task_type '{task_type}' provided to Supervisor.")


async def run_pipeline():
    supervisor = SupervisorAgent()

    print("==========================================")
    print(" Running Supervisor + Worker Pipeline")
    print("==========================================")

    # Task 1: Search Query
    res1 = await supervisor.route_and_execute(
        user_query="Tell me about MCP architecture",
        task_type="search"
    )
    print("\nResult 1:", res1)

    res2 = await supervisor.route_and_execute(
        user_query="MCP connects agents with tools.",
        task_type="text_processing"
    )
    print("\nResult 2:", res2)


if __name__ == "__main__":
    asyncio.run(run_pipeline())