import os

from fastapi import APIRouter

router = APIRouter()

MAX_CONCURRENT = int(os.getenv("NEXUS_MAX_CONCURRENT", "3"))
USE_REDIS = os.getenv("NEXUS_USE_REDIS", "false").lower() == "true"


@router.get("/health")
def health():
    return {
        "status": "ok",
        "mode": "redis" if USE_REDIS else "local",
        "max_concurrent": MAX_CONCURRENT,
    }
