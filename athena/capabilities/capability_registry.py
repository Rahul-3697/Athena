from athena.capabilities.base_capability import BaseCapability
from athena.capabilities.capability_descriptor import CapabilityDescriptor


class CapabilityRegistry:

    def __init__(self):
        self._capabilities: dict[str, BaseCapability] = {}

    def register(self, capability: BaseCapability) -> None:

        if capability.name in self._capabilities:
            raise ValueError(
                f"Capability '{capability.name}' is already registered."
            )

        self._capabilities[capability.name] = capability

    def get(self, name: str) -> BaseCapability:

        if name not in self._capabilities:
            raise KeyError(
                f"Capability '{name}' is not registered."
            )

        return self._capabilities[name]

    def has(self, name: str) -> bool:
        return name in self._capabilities

    def list_capabilities(self) -> list[str]:
        return list(self._capabilities.keys())
    
    def descriptors(self) -> list[CapabilityDescriptor]:
        """
        Get a list of capability descriptors.
        """
        return [
            CapabilityDescriptor(
                name=capability.name,
                description=capability.description,
                workflows=list(capability.workflows.keys()),
                metadata=capability.metadata,
            )
            for capability in self._capabilities.values()
        ]