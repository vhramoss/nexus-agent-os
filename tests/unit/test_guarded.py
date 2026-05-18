import pytest
from nexus_os.core.security.guarded import guarded
from nexus_os.core.security.capabilities import Capability, CapabilitySet
from nexus_os.core.security.sandbox import SandboxViolation


def make_state(caps):
    state = type("State", (), {})()
    state.capabilities = caps
    return state


def test_guarded_blocks_when_capability_missing():
    @guarded(Capability.USE_LLM)
    def node(state):
        return "ok"

    state = make_state(CapabilitySet(set()))

    with pytest.raises(SandboxViolation):
        node(state)


def test_guarded_allows_when_capability_present():
    @guarded(Capability.USE_LLM)
    def node(state):
        return "ok"

    state = make_state(CapabilitySet({Capability.USE_LLM}))

    result = node(state)

    assert result == "ok"


@pytest.mark.asyncio
async def test_guarded_supports_async_functions():
    @guarded(Capability.USE_LLM)
    async def node(state):
        return "ok"

    state = make_state(CapabilitySet({Capability.USE_LLM}))

    result = await node(state)

    assert result == "ok"


def test_guarded_error_contains_function_name():
    @guarded(Capability.USE_LLM)
    def my_node(state):
        return "ok"

    state = make_state(CapabilitySet(set()))

    with pytest.raises(SandboxViolation) as exc:
        my_node(state)

    assert "my_node" in str(exc.value)