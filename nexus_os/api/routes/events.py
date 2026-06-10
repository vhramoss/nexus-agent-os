from fastapi import APIRouter, WebSocket

from nexus_os.observability.streaming import EventStreamer

router = APIRouter()

streamer = EventStreamer()


@router.websocket("/events/{execution_id}")
async def websocket_endpoint(ws: WebSocket, execution_id: str):
    await ws.accept()
    streamer.register(execution_id, ws)

    try:
        while True:
            await ws.receive_text()
    except Exception:
        streamer.unregister(execution_id, ws)
