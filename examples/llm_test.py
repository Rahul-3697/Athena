from athena.llms.factory import LLMFactory

llm = LLMFactory.openai()

response = llm.invoke(
    "Say hello from Athena in one sentence."
)

print(response)