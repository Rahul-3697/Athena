from athena.context.context import Context
from athena.contracts.report import Report
from athena.skills.base_skill import BaseSkill


class ReportGeneratorSkill(BaseSkill):

    def invoke(self, context: Context) -> Context:

        report_lines = [
            "=" * 60,
            "ATHENA EXECUTION PLAN",
            "=" * 60,
            ""
        ]

        for step in context.plan.steps:
            report_lines.append(
                f"{step.id}. {step.title}"
            )

        context.report = Report(
            content="\n".join(report_lines)
        )

        return context