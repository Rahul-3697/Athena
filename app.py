"""
Athena - AI Engineering Framework

Application Entry Point
"""

from athena.agent.agent import Agent

from athena.workflow.workflow import Workflow

from athena.skills.planner_skill import PlannerSkill
from athena.skills.report_generator_skill import ReportGeneratorSkill

from athena.llms.factory import LLMFactory


def build_workflow(llm):
    """
    Build the default research workflow.
    """

    return (
        Workflow("Research Workflow")
        .add(PlannerSkill(llm))
        .add(ReportGeneratorSkill())
    )


def build_agent() -> Agent:
    """
    Create the default Athena agent.
    """

    llm = LLMFactory.openai()

    workflow = build_workflow(llm)

    return Agent(
        name="Research Agent",
        workflow=workflow
    )


def main():

    goal = """
    Explain LangGraph and compare it with LangChain.
    Include architecture, execution model, advantages and use cases.
    """

    agent = build_agent()

    result = agent.invoke(goal)

    print("\n")
    print("=" * 80)
    print("ATHENA OUTPUT")
    print("=" * 80)
    print(result)


if __name__ == "__main__":
    main()