import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from nexus_os.api.routes import dlq, health, replay, run
from nexus_os.runtime.resilience.recovery import recovery_loop


# -----------------------------
# Lifespan (startup/shutdown)
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ STARTUP
    recovery_task = asyncio.create_task(recovery_loop())

    yield

    # ✅ SHUTDOWN
    recovery_task.cancel()


# -----------------------------
# App
# -----------------------------
app = FastAPI(lifespan=lifespan)

# -----------------------------
# Routes
# -----------------------------
app.include_router(run.router)
app.include_router(dlq.router)
app.include_router(replay.router)
app.include_router(health.router)
