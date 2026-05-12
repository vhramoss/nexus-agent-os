import inspect
from functools import wraps
from nexus_os.core.security.sandbox import enforce, SandboxViolation


def guarded(fn, capability):
    """
    Wraps a node function with capability enforcement.
    Works for sync and async nodes.
    Preserves metadata for tracing and replay.
    """

    if inspect.iscoroutinefunction(fn):

        @wraps(fn)
        async def async_wrapper(state, *args, **kwargs):
            try:
                enforce(state.capabilities, capability)
            except SandboxViolation as e:
                raise SandboxViolation(
                    f"{fn.__name__}: {str(e)}"
                ) from e

            return await fn(state, *args, **kwargs)

        return async_wrapper

    else:

        @wraps(fn)
        def sync_wrapper(state, *args, **kwargs):
            try:
                enforce(state.capabilities, capability)
            except SandboxViolation as e:
                raise SandboxViolation(
                    f"{fn.__name__}: {str(e)}"
                ) from e

            return fn(state, *args, **kwargs)

        return sync_wrapper