from athena.capabilities.capability_descriptor import CapabilityDescriptor
from athena.capabilities.capability_registry import CapabilityRegistry


class CapabilityDiscovery:

    def __init__(self, registry: CapabilityRegistry):
        self.registry = registry

    def discover(self) -> list[CapabilityDescriptor]:
        return self.registry.descriptors()