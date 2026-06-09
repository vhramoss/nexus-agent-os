import asyncio
import time

from nexus_os.state.execution_store import ExecutionStore

store = ExecutionStore()


async def recovery_loop(interval: float = 5.0, timeout: float = 10.0):
    while True:
        data = store._read()

        now = time.monotonic()

        for execution_id, record in data.items():
            if record.get("status") != "running":
                continue

            last_heartbeat = record.get("heartbeat")

            if not last_heartbeat:
                continue

            if now - last_heartbeat > timeout:
                # ✅ mark as failed (ou requeue futuramente)
                record["status"] = "failed"
                store.save(execution_id, record)

        await asyncio.sleep(interval)
