# 🧠 Nexus Agent OS

> A structured runtime and observability layer for AI agents built with LangGraph, FastAPI, and RAG.

---

## 📌 Overview

Nexus Agent OS is a modular execution runtime for AI agents designed to provide:

- ✅ Deterministic execution flow (LangGraph)
- ✅ Full observability (Event Bus + Telemetry + Timeline)
- ✅ Retry and failure handling (Supervisor + DLQ)
- ✅ Execution replay and traceability
- ✅ Metrics extraction for runtime analysis

Unlike typical agent projects focused on prompt execution, this project focuses on **agent orchestration, execution modeling, and observability**.

---

## 🧱 Architecture

```text
API (FastAPI)
   ↓
Runtime Layer
   - Queue
   - Timeout
   - Supervisor (retry / dlq)
   ↓
Agent (NexusAgent)
   ↓
Execution Graph (LangGraph)
   ↓
Telemetry → EventBus → EventStore
   ↓
Replay / Timeline / Metrics

🔄 Execution Flow

1. User sends goal
2. Agent initializes state
3. Memory recall (semantic + episodic)
4. Planner decides next steps
5. Graph executes nodes
6. Results are stored and indexed
7. Events are emitted and persisted
8. Metrics and timeline reconstructed

📊 Observability Features

✅ Event System
Every action emits structured events:

agent.started
node.started
node.completed
retry.triggered
fallback.executed
agent.completed
✅ Timeline
Replay execution step-by-step:
{
  "component": "planner",
  "status": "completed",
  "duration_ms": 42
}
✅ Metrics
Extracted from events:
{
  "total_duration_ms": 128,
  "node_count": 3,
  "retry_count": 1,
  "failure": false
}
✅ Replay (Full Execution Trace)
{
  "trace_id": "...",
  "input": {...},
  "metrics": {...},
  "timeline": [...],
  "result": {...}
}

🧠 Memory System

Episodic memory (execution history)
Semantic memory (FAISS + embeddings)
Vector similarity search
Future support for persistent index

⚙️ Stack

FastAPI
LangGraph
LangChain
CrewAI
Sentence Transformers
FAISS
Redis (optional)
Python 3.11+

🚀 Running the Project

1. Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

2. Start API
uvicorn nexus_os.api.main:app

3. Run agent
curl -X POST http://127.0.0.1:8000/run \
  -H "Content-Type: application/json" \
  -d '{"goal":"example task"}'

4. Inspect execution
curl http://127.0.0.1:8000/replay/<trace_id>

🧪 Current Status
✅ Runtime completed
✅ Observability implemented
✅ Metrics extraction implemented
⚠️ Planner stability under improvement
⚠️ Memory system refinement ongoing

📍 Future Improvements

Structured ToolExecution contracts
Persistent vector index
Real-time metrics dashboard
Multi-agent coordination improvements
Workflow visualization UI

👤 Author
Victor Hugo Ramos
