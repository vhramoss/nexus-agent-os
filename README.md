# 🧠 Nexus Agent OS

> A production-grade agent runtime system with distributed execution, observability, and fault tolerance.

---

## 🚀 Overview

Nexus Agent OS is a modular backend system designed to execute agent-based workflows with:

- ✅ Distributed execution with Redis
- ✅ Fault tolerance (retry + dead letter queue)
- ✅ Observability (event-based tracing + replay)
- ✅ Strong test coverage (~74%)
- ✅ Production-ready runtime and orchestration

---

## 🏗️ Architecture

```

API (FastAPI)
↓
Services (Execution layer)
↓
Runtime (QueueGate, Supervisor)
↓
Graph (Agent workflow)
↓
Core (Observability, Security, Memory)

````

---

## ⚙️ Features

### ✅ Runtime & Execution
- Controlled concurrency (Semaphore + RedisQueueGate)
- Atomic distributed locks using Redis + Lua scripts
- Supervisor-based fault handling (retry / dlq / abort)
- Dead Letter Queue (in-memory + Redis-backed)

---

### ✅ Observability
- EventBus (publish/subscribe)
- Tracer (execution lifecycle tracking)
- EventStore (persisted events)
- Replay endpoint for debugging executions

---

### ✅ Security
- Capability-based execution control
- `@guarded` decorator for runtime safety
- Sandbox enforcement

---

### ✅ Reliability
- Retry policies
- DLQ handling
- Timeout management
- Deterministic supervisor decisions

---

### ✅ Configuration
- Centralized settings via Pydantic (`Settings`)
- Environment-aware (`.env`)
- Type-safe configuration system

---

## 🧪 Testing

- ✅ Unit tests for core logic
- ✅ Integration tests for API
- ✅ Runtime and observability tests
- ✅ ~74% coverage

Run tests:

```bash
pytest
````

***

## 🐳 Running with Docker

### 🔹 Build & Run (single container)

```bash
docker build -t nexus-agent-os .
docker run -p 8000:8000 nexus-agent-os
```

***

### 🔹 Full Stack (with Redis)

```bash
docker compose up --build
```

***

### ✅ Health check

```bash
curl http://localhost:8000/health
```

Response:

```json
{
  "filesystem": { "status": "ok" },
  "redis": { "status": "ok" }
}
```

***

## 📡 API Endpoints

### `/health`

System health status

### `/run`

Execute agent

### `/replay`

Replay execution timeline

### `/dlq`

Dead letter queue inspection

***

## 🧠 Key Engineering Concepts

This project demonstrates:

* ✅ Distributed coordination (Redis)
* ✅ Concurrency control (Semaphore + atomic Lua)
* ✅ Fault-tolerant execution
* ✅ Event-driven observability
* ✅ Config-driven architecture
* ✅ Testable system design

***

## 📊 Project Maturity

| Area          | Status                |
| ------------- | --------------------- |
| Architecture  | ✅ Production-ready    |
| Tests         | ✅ Strong coverage     |
| Observability | ✅ Complete            |
| Security      | ✅ Enforced            |
| Runtime       | ✅ Distributed-ready   |
| CI/CD         | ✅ Implemented         |
| Docker        | ✅ Fully containerized |

***

## 🧩 Tech Stack

* FastAPI
* Redis
* LangGraph / LangChain / CrewAI
* FAISS (vector search)
* Pydantic / pydantic-settings
* Pytest
* Docker & Docker Compose

***

## 📉 Known Limitations

* No real LLM integration (mocked / local)
* No persistent external DB (only file/redis-based)
* No autoscaling (local environment)

***

## 🚀 Future Improvements

* Cloud deployment (AWS / Fly.io / Render)
* Real LLM provider integration
* Metrics (Prometheus / OpenTelemetry)
* Authentication layer
* UI dashboard

***

## 👤 Author

Victor Hugo Ramos
