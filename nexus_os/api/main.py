from fastapi import FastAPI
from nexus_os.api.routes import run, replay, health

app = FastAPI()

app.include_router(run.router)
app.include_router(replay.router)
app.include_router(health.router)
