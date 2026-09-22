from athena.capabilities.base_capability import BaseCapability
from athena.capabilities.capability_registry import CapabilityRegistry
from athena.workflow.workflow import Workflow


class CapabilityResolver:

    def __init__(self, registry: CapabilityRegistry):
        self.registry = registry

    def resolve(
        self,
        capability_name: str,
        workflow_name: str,
    ) -> Workflow:

        capability = self.registry.get(capability_name)

        if workflow_name not in capability.workflows:
            raise KeyError(
                f"Workflow '{workflow_name}' is not available "
                f"in capability '{capability_name}'."
            )

        return capability.workflows[workflow_name]