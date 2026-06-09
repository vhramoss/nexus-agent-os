from fastapi import APIRouter

from nexus_os.application.execution_service import get_dlq_items

router = APIRouter()


@router.get("/dlq")
def get_dlq():
    return {"items": get_dlq_items()}
