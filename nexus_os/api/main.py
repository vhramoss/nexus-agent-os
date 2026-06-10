import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from nexus_os.api.routes import dlq, events, health, replay, run
from nexus_os.api.routes.events import streamer
from nexus_os.observability.event_bus import event_bus
from nexus_os.runtime.resilience.recovery import recovery_loop


# -----------------------------
# Lifespan (startup/shutdown)
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ STARTUP

    # conecta streaming ao event bus ✅
    event_bus.subscribe("*", streamer.handle)

    # inicia recovery loop ✅
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
app.include_router(events.router)
