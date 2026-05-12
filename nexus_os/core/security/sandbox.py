from nexus_os.core.security.capabilities import Capability


class SandboxViolation(Exception):
    pass


def enforce(capabilities, required: str):
    if not capabilities.allows(required):
        raise SandboxViolation(
            f"Capability '{required}' not allowed"
        )
