from athena.llms.openai import OpenAILLM


class LLMFactory:

    @staticmethod
    def openai():
        """Create an instance of the OpenAILLM."""
        return OpenAILLM()