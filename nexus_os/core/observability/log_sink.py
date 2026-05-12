def print_event(event: dict):
    event_type = event.get("type", "unknown")
    payload = event.get("payload", {})
    trace_id = payload.get("trace_id", "n/a")

    print(f"[EVENT] {event_type} | trace_id={trace_id} | payload={payload}")