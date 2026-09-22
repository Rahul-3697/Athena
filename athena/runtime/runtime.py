from uuid import uuid4

from athena.contracts.execution_plan import ExecutionPlan
from athena.contracts.tool_request import ToolRequest

from athena.contracts.execution_state_records.execution_event import (
    ExecutionEvent,
)
from athena.contracts.execution_state_records.execution_record import (
    ExecutionRecord,
)
from athena.contracts.execution_state_records.execution_result import (
    ExecutionResult,
)

from athena.tools.tool_executor import ToolExecutor
from athena.tools.tool_registry import ToolRegistry

from athena.capabilities.capability_registry import CapabilityRegistry
from athena.capabilities.capability_resolver import CapabilityResolver

from athena.context.context import Context


class Runtime:

    def __init__(
        self,
        registry: ToolRegistry,
        executor: ToolExecutor,
        capability_registry: CapabilityRegistry | None = None,
        capability_resolver: CapabilityResolver | None = None,
    ):
        # ----------------------------------------------------
        # Existing Tool Runtime
        # ----------------------------------------------------

        self.registry = registry
        self.executor = executor

        # ----------------------------------------------------
        # Capability Runtime
        # ----------------------------------------------------

        self.capability_registry = capability_registry

        if capability_resolver is not None:

            self.capability_resolver = capability_resolver

        elif capability_registry is not None:

            self.capability_resolver = CapabilityResolver(
                capability_registry
            )

        else:

            self.capability_resolver = None

    # ========================================================
    # Runtime Entry Point
    # ========================================================

    def execute(self, plan: ExecutionPlan):

        execution_id = f"execution-{uuid4().hex[:8]}"

        record = ExecutionRecord(
            execution_id=execution_id
        )

        # ----------------------------------------------------
        # Execution Started
        # ----------------------------------------------------

        record.add_event(
            ExecutionEvent(
                event_type="ExecutionStarted",
                execution_id=execution_id,
                status="running",
                metadata={
                    "steps": len(plan.steps),
                },
            )
        )

        print("\n" + "=" * 60)
        print("ATHENA RUNTIME")
        print("=" * 60)

        print(f"\nExecution ID: {execution_id}")

        print("\nExecution Plan:")
        print("-" * 60)

        for index, step in enumerate(plan.steps, start=1):

            print(f"\nStep {index}")
            print(f"  ID          : {step.step}")
            print(f"  Description : {step.description}")
            print(f"  Target      : {step.target}")
            print(f"  Arguments   : {step.arguments}")

        print("\n" + "-" * 60)
        print("EXECUTION")
        print("-" * 60)

        results = []

        for index, step in enumerate(
            plan.steps,
            start=1
        ):

            print(
                f"\n[{index}] Executing: {step.step}"
            )

            # ------------------------------------------------
            # Step Started
            # ------------------------------------------------

            record.add_event(
                ExecutionEvent(
                    event_type="StepStarted",
                    execution_id=execution_id,
                    step=step.step,
                    target=step.target,
                    status="running",
                )
            )

            # =================================================
            # CAPABILITY PATH
            # =================================================

            if (
                self.capability_registry is not None
                and self.capability_registry.has(step.target)
            ):

                print(
                    f"    Target '{step.target}' "
                    "resolved as CAPABILITY."
                )

                workflow_name = step.arguments.get(
                    "workflow"
                )

                if not workflow_name:

                    print(
                        "    FAILED: capability workflow "
                        "was not provided."
                    )

                    record.add_event(
                        ExecutionEvent(
                            event_type="StepFailed",
                            execution_id=execution_id,
                            step=step.step,
                            target=step.target,
                            status="failed",
                            metadata={
                                "reason": (
                                    "Capability workflow "
                                    "was not provided."
                                )
                            },
                        )
                    )

                    continue

                try:

                    workflow = self.capability_resolver.resolve(
                        capability_name=step.target,
                        workflow_name=workflow_name,
                    )

                except KeyError as error:

                    print(
                        f"    FAILED: {error}"
                    )

                    record.add_event(
                        ExecutionEvent(
                            event_type="StepFailed",
                            execution_id=execution_id,
                            step=step.step,
                            target=step.target,
                            status="failed",
                            metadata={
                                "error": str(error),
                            },
                        )
                    )

                    continue

                print(
                    f"    Workflow : {workflow.name}"
                )

                record.add_event(
                    ExecutionEvent(
                        event_type="CapabilityResolved",
                        execution_id=execution_id,
                        step=step.step,
                        target=step.target,
                        status="resolved",
                        metadata={
                            "workflow": workflow_name,
                        },
                    )
                )

                # ------------------------------------------------
                # Create Athena Context
                # ------------------------------------------------

                context = Context(
                    goal=step.description,
                    plan=plan,
                    metadata={
                        "capability": step.target,
                        "workflow": workflow_name,
                        "arguments": step.arguments,
                    },
                )

                print(
                    "    Context  : created"
                )

                record.add_event(
                    ExecutionEvent(
                        event_type="WorkflowStarted",
                        execution_id=execution_id,
                        step=step.step,
                        target=step.target,
                        status="running",
                        metadata={
                            "workflow": workflow_name,
                        },
                    )
                )

                # ------------------------------------------------
                # Execute existing Workflow abstraction
                # ------------------------------------------------

                result = workflow.run(context)

                print(
                    "    Success  : workflow executed"
                )

                print(
                    f"    Context  : {result.metadata}"
                )

                record.add_event(
                    ExecutionEvent(
                        event_type="WorkflowCompleted",
                        execution_id=execution_id,
                        step=step.step,
                        target=step.target,
                        status="completed",
                        metadata={
                            "workflow": workflow_name,
                        },
                    )
                )

                record.add_event(
                    ExecutionEvent(
                        event_type="StepCompleted",
                        execution_id=execution_id,
                        step=step.step,
                        target=step.target,
                        status="completed",
                    )
                )

                results.append(result)

                continue

            # =================================================
            # EXISTING TOOL PATH
            # =================================================

            if not self.registry.has(step.target):

                print(
                    f"    FAILED: target '{step.target}' "
                    "is not registered."
                )

                record.add_event(
                    ExecutionEvent(
                        event_type="StepFailed",
                        execution_id=execution_id,
                        step=step.step,
                        target=step.target,
                        status="failed",
                        metadata={
                            "reason": (
                                "Target is not registered."
                            )
                        },
                    )
                )

                continue

            record.add_event(
                ExecutionEvent(
                    event_type="ToolResolved",
                    execution_id=execution_id,
                    step=step.step,
                    target=step.target,
                    status="resolved",
                )
            )

            request = ToolRequest(
                tool_name=step.target,
                arguments=step.arguments,
            )

            print(
                f"    Target: {request.tool_name}"
            )

            print(
                f"    Args  : {request.arguments}"
            )

            record.add_event(
                ExecutionEvent(
                    event_type="ToolStarted",
                    execution_id=execution_id,
                    step=step.step,
                    target=step.target,
                    status="running",
                )
            )

            # ------------------------------------------------
            # Existing Runtime → Tool Executor
            # ------------------------------------------------

            result = self.executor.execute(
                request
            )

            print(
                f"    Success: {result.success}"
            )

            if result.data is not None:

                print(
                    f"    Result : {result.data}"
                )

            if result.error is not None:

                print(
                    f"    Error  : {result.error}"
                )

            if result.success:

                record.add_event(
                    ExecutionEvent(
                        event_type="ToolCompleted",
                        execution_id=execution_id,
                        step=step.step,
                        target=step.target,
                        status="completed",
                    )
                )

                record.add_event(
                    ExecutionEvent(
                        event_type="StepCompleted",
                        execution_id=execution_id,
                        step=step.step,
                        target=step.target,
                        status="completed",
                    )
                )

            else:

                record.add_event(
                    ExecutionEvent(
                        event_type="ToolFailed",
                        execution_id=execution_id,
                        step=step.step,
                        target=step.target,
                        status="failed",
                        metadata={
                            "error": result.error,
                        },
                    )
                )

                record.add_event(
                    ExecutionEvent(
                        event_type="StepFailed",
                        execution_id=execution_id,
                        step=step.step,
                        target=step.target,
                        status="failed",
                    )
                )

            results.append(result)

        # ----------------------------------------------------
        # Complete Execution Record
        # ----------------------------------------------------

        record.complete()

        record.add_event(
            ExecutionEvent(
                event_type="ExecutionCompleted",
                execution_id=execution_id,
                status="completed",
                metadata={
                    "result_count": len(results),
                },
            )
        )

        # ----------------------------------------------------
        # Execution Result
        # ----------------------------------------------------

        execution_result = ExecutionResult(
            execution_id=execution_id,
            status="completed",
            output=results,
            metadata={
                "steps": len(plan.steps),
            },
        )

        print("\n" + "-" * 60)

        print("EXECUTION EVENTS")
        print("-" * 60)

        for index, event in enumerate(
            record.events,
            start=1
        ):

            print(
                f"{index:02d}. "
                f"{event.event_type}"
                f" | target={event.target}"
                f" | status={event.status}"
            )

        print("\n" + "=" * 60)
        print("RUNTIME COMPLETE")
        print("=" * 60)

        return execution_result, record