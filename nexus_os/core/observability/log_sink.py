def print_event(event: dict):    
    print(
            f"[{event['event_type']}] "
            f"{event['component']} "
            f"{event['status']} | "
            f"trace_id={event['trace_id']} "
            f"{event.get('metadata', {})}"
        )
