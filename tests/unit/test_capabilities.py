from nexus_os.core.security.capabilities import CapabilitySet, Capability


def test_capability_set_allows_granted_capability():
    # Arrange
    caps = CapabilitySet({Capability.USE_LLM})

    # Act & Assert
    assert caps.allows(Capability.USE_LLM) is True

def test_capability_set_denies_missing_capability():
    # Arrange
    caps = CapabilitySet(set())

    # Act & Assert
    assert caps.allows(Capability.USE_LLM) is False

import pytest
from nexus_os.core.security.sandbox import enforce, SandboxViolation


def test_enforce_raises_when_capability_missing():
    # Arrange
    caps = CapabilitySet(set())

    # Act & Assert
    with pytest.raises(SandboxViolation):
        enforce(caps, Capability.USE_LLM)

def test_enforce_passes_when_capability_granted():
    # Arrange
    caps = CapabilitySet({Capability.USE_LLM})

    # Act (não deve lançar erro)
    enforce(caps, Capability.USE_LLM)

