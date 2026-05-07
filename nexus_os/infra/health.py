def check_system_health():
    return {
        "status": "ok",
        "components": {
            "memory": "ready",
            "graph": "ready",
            "agents": "idle",
        },
    }
