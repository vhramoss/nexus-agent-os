def retry_policy(failed: bool, retries: int, max_retries: int) -> str:
    if failed and retries < max_retries:
        return "retry"
    if failed:
        return "fallback"
    return "next"
