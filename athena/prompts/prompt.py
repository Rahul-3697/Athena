def build(goal: str):

    return f"""
You are Athena's Planning Engine.

Create a plan for this goal.

Goal:
{goal}

Return ONLY JSON.

Schema:

{{
    "steps":[
        {{
            "id":1,
            "title":"..."
        }}
    ]
}}
"""