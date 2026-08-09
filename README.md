# Week 5 — MCP Server, Multi-Agent System & Tracing

A robust implementation of a custom **Model Context Protocol (MCP)** server, an in-memory MCP client, a **Supervisor-Worker** multi-agent architecture, and a real-time **Tracing Layer** for execution graph auditability.

## 📌 Overview

This repository demonstrates an end-to-end Agentic AI workflow. The system coordinates specialized worker agents under a supervisor model, routes user tasks dynamically, and invokes custom Model Context Protocol (MCP) server tools while logging full execution graphs and timing metrics to both stdout and a structured JSON file.

## ✨ Features

* **Custom MCP Server**: Developed using `FastMCP` exposing app resources and text analysis tools.
* **MCP Client**: Standardized client connection capable of querying server schemas, reading resources, and calling tools.
* **Supervisor-Worker Multi-Agent System**:

  * **SupervisorAgent**: Intelligently inspects task intent and routes execution to appropriate downstream workers.
  * **SearchWorker**: Executes quick lookup and knowledge retrieval operations.
  * **TextProcessorWorker**: Communicates directly with the MCP Server to perform deep text analysis.
* **Execution Tracing Layer**: `@trace_tool` decorator logging execution latency, inputs, status (`SUCCESS`/`FAILED`), outputs, and exact timestamps across all graph nodes.
* **JSON Audit Trail**: Writes all execution trace logs asynchronously to `trace_log.json`.

## 🏗️ System Architecture

```text
                            ┌───────────────────┐
                            │     User Task     │
                            └─────────┬─────────┘
                                      │
                                      ▼
                            ┌───────────────────┐
                            │  SupervisorAgent  │
                            └─────────┬─────────┘
                                      │
                   ┌──────────────────┴──────────────────┐
                   ▼                                     ▼
          ┌─────────────────┐                  ┌───────────────────┐
          │  SearchWorker   │                  │TextProcessorWorker│
          └─────────────────┘                  └─────────┬─────────┘
                                                         │
                                                         ▼
                                                   ┌───────────┐
                                                   │MCP Client │
                                                   └─────┬─────┘
                                                         │
                                                         ▼
                                                   ┌───────────┐
                                                   │MCP Server │
                                                   └─────┬─────┘
                                                         │
                                                         ▼
                                                 analyze_text Tool
```

## 📁 Project Structure

```text
Week_5/
│
├── main.py                    # Multi-agent orchestrator & entry point
├── requirements.txt           # Project dependencies
├── trace_log.json              # Persistent output store for tracing data
│
├── mcp_server/
│   ├── __init__.py
│   ├── server.py              # FastMCP server definition (Tools & Resources)
│   └── client.py              # Custom MCP Client execution logic
│
├── multi_agent/
│   ├── __init__.py
│   └── worker_agents.py       # SearchWorker & TextProcessorWorker definitions
│
└── tracing/
    ├── __init__.py
    └── tracer.py              # Decorators and logging utilities for tracing
```

## ⚙️ Component Breakdown

### 1. Custom MCP Server (`mcp_server/server.py`)

Exposes resources and tools adhering to the Model Context Protocol standard:

* **Resource (`config://app-status`)**: Returns application health state, project phase, and target phase status.
* **Tool (`analyze_text`)**: Accepts raw string inputs and calculates word count, character count, and sentence counts.

### 2. Custom MCP Client (`mcp_server/client.py`)

Handles connection lifecycle:

* Connects directly to the server instance.
* Dynamically discovers exposed tools and resources.
* Safely evaluates resources and invokes tool methods.

### 3. Multi-Agent Pipeline (`multi_agent/worker_agents.py` & `main.py`)

Demonstrates task delegation:

* **Supervisor**: Evaluates incoming query types (`search` vs `text_processing`).
* **Workers**: Encapsulate operational logic. `TextProcessorWorker` seamlessly bridges worker tasks with MCP server capabilities.

### 4. Tracing & Telemetry (`tracing/tracer.py`)

* Provides high-resolution execution timing ($ms$).
* Standardizes cross-platform output (UTF-8 console compliance + JSON sink).

## 🚀 Getting Started

### Prerequisites

* **Python 3.10+**
* Virtual environment tool (`venv` or `conda`)

### Installation & Setup

1. **Clone the repository and enter the directory**:

   Bash

   ```bash
   cd Week_5
   ```

2. **Create and activate a virtual environment**:

   * **Windows (CMD/PowerShell)**:

     DOS

     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

   * **macOS/Linux**:

     Bash

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies**:

   Bash

   ```bash
   pip install -r requirements.txt
   ```

## 🧪 Verification & Testing

### 1. Inspect MCP Server

Verify tool and resource exposure on the FastMCP server:

DOS

```bash
fastmcp inspect mcp_server/server.py
```

### 2. Test Standalone MCP Client

Run the client module to verify connection, resource fetching, and tool calls:

DOS

```bash
python -m mcp_server.client
```

### 3. Execute Multi-Agent Graph & Tracing

Run the supervisor pipeline to process task workflows and stream real-time traces:

DOS

```bash
python main.py
```

### 4. Verify Log Persistence

Check logged trace events stored in `trace_log.json`:

DOS

```bash
python -c "import json; logs=json.load(open('trace_log.json')); print('Total logged events:', len(logs))"
```

## 📊 Sample Output

Plaintext

```text
==========================================
 Running Supervisor + Worker Pipeline
==========================================

[TRACE 2026-08-09T19:20:35] Worker_Search | Action: execute_search | Status: SUCCESS
  |- Duration: 0.01ms
  |- Output: Match found for 'mcp': Model Context Protocol (MCP) standardizes agent tool and resource exposure.

[TRACE 2026-08-09T19:20:35] MCP_Tool_AnalyzeText | Action: analyze_text | Status: SUCCESS
  |- Duration: 0.03ms
  |- Inputs: {'kwargs': {'content': 'MCP connects agents with tools.'}}
  |- Output: {'word_count': 5, 'char_count': 31, 'sentence_count': 1}
```

## 🛠️ Tech Stack

* **Language**: Python 3.14 / 3.10+
* **Protocol**: Model Context Protocol (MCP)
* **Framework**: FastMCP
* **Concurrency**: `asyncio`
* **Data Exchange**: JSON / Standard Streams
