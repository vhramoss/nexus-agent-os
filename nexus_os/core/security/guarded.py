import inspect
from functools import wraps

from nexus_os.core.security.sandbox import SandboxViolation, enforce


def guarded(capability):
    """
    Decorator factory for enforcing capabilities on agent nodes.
    Supports both sync and async functions.
    """

    def decorator(fn):

        if inspect.iscoroutinefunction(fn):

            @wraps(fn)
            async def async_wrapper(state, *args, **kwargs):
                try:
                    enforce(state.capabilities, capability)
                except SandboxViolation as e:
                    raise SandboxViolation(f"{fn.__name__}: {str(e)}") from e

                return await fn(state, *args, **kwargs)

            return async_wrapper

        else:

            @wraps(fn)
            def sync_wrapper(state, *args, **kwargs):
                try:
                    enforce(state.capabilities, capability)
                except SandboxViolation as e:
                    raise SandboxViolation(f"{fn.__name__}: {str(e)}") from e

                return fn(state, *args, **kwargs)

            return sync_wrapper

    return decorator
