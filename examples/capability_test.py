from athena.capabilities import BaseCapability, CapabilityRegistry
from athena.workflow.workflow import Workflow


class ExampleCapability(BaseCapability):

    @property
    def name(self) -> str:
        return "example"

    @property
    def description(self) -> str:
        return "Example capability for validating Athena capability discovery."

    @property
    def workflows(self) -> dict[str, Workflow]:
        return {
            "example_workflow": Workflow("Example Workflow"),
        }


registry = CapabilityRegistry()

capability = ExampleCapability()

registry.register(capability)

print("Capabilities:")
print(registry.list_capabilities())

print("\nCapability:")
print(registry.get("example").name)

print("\nWorkflows:")
print(registry.get("example").workflows.keys())