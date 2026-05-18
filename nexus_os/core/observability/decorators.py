from functools import wraps


def traced_node(name: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(state, *args, **kwargs):
            tracer = state.tracer
            if tracer is None:
                raise RuntimeError("Tracer not initialized")

            with tracer.span(name):
                return fn(state, *args, **kwargs)

        return wrapper
    return decorator
