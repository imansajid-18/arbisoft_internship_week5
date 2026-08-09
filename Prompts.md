1)Setup and configure the required environment

2)Setup virtual environment

3)Make .gitignore for this project.

4)Make requirements.txt

5)Build a custom MCP server exposing one app resource and one tool

6)I ran my server but I am getting this error:ModuleNotFoundError: No module named 'mcp.server.fastmcp'.I have mcp version 2.0.0 installed. I checked it with pip show mcp and pip list.Please help me fix the import according to the version I actually have installed instead of making me install random packages.

7)MCP server is not running,what is wrong with it?
--> Some of the imports were wrong.

8)Now the next task to perform is Connect the MCP server to a client (Claude Code or a custom client)

9)Implement a supervisor + worker agent that routes tasks to ≥2 sub-agents.I want two workers:
1. SearchWorker for search and lookup tasks
2. TextProcessorWorker for text processing tasks

10)I also need to add a tracing layer that logs every tool call across the agent graph.I want the trace to show things like the agent or tool name, action, status, execution time, inputs and output and create a simple tracer that I can use as a decorator such as @trace_tool("Worker_Search").

11)I already have tracing for my supervisor and worker agents.Now I also want the MCP analyze_text tool itself to be traced.Can I use the trace_tool decorator with the MCP @mcp.tool() decorator?show me how to do it without changing the rest of my working server.

12)These are my four Week 5 first-half tasks:
1. Build a custom MCP server exposing one app resource and one tool.
2. Connect the MCP server to a client.
3. Implement a supervisor + worker agent that routes tasks to at least two sub-agents.
4. Add a tracing layer that logs every tool call across the agent graph.
I have implemented all of these and tested the MCP client and main.py.Check my code and tell me which requirements are actually completed, which are only partially completed, and what I still need to do.

13)I have completed the Week 5 first-half implementation.
Please review my code for:
- correctness
- efficiency
- unnecessary complexity
- clean project structure
- whether it satisfies the Week 5 requirements
Please don't suggest unnecessary architectural changes if the current implementation already satisfies the requirements.