from rich.console import Console

from athena.agent.agent import ResearchAgent

console = Console()

console.rule("[bold cyan]🚀 Project Athena")

agent = ResearchAgent()

goal = input("Enter research topic: ")

report = agent.run(goal)

console.print(report)