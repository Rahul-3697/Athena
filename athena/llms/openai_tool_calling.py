import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from athena.contracts.tool_call import ToolCall
from athena.contracts.tool_descriptor import ToolDescriptor
from athena.contracts.tool_result import ToolResult

from athena.llms.tool_calling import BaseToolCallingLLM
from athena.tools.formatters.openai_formatter import (
    OpenAIToolFormatter,
)


load_dotenv()


class OpenAIToolCallingLLM(BaseToolCallingLLM):
    """
    OpenAI Responses API adapter for Athena Tool calling.
    """

    def __init__(
        self,
        model: str = "gpt-4",
    ):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.model = model
        self.formatter = OpenAIToolFormatter()

        self._input = []
        self._tools = []

    def generate(
        self,
        prompt: str,
        tools: list[ToolDescriptor],
    ):

        self._tools = [
            self.formatter.format(tool)
            for tool in tools
        ]

        self._input = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        response = self.client.responses.create(
            model=self.model,
            input=self._input,
            tools=self._tools,
        )

        self._input.extend(response.output)

        return self._parse_response(response)

    def continue_with_tool_results(
        self,
        results: list[tuple[ToolCall, ToolResult]],
    ):

        for call, result in results:

            self._input.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": self._serialize_result(
                        result
                    ),
                }
            )

        response = self.client.responses.create(
            model=self.model,
            input=self._input,
            tools=self._tools,
        )

        self._input.extend(response.output)

        return self._parse_response(response)

    def _parse_response(self, response):

        tool_calls = []

        for item in response.output:

            if item.type == "function_call":

                arguments = json.loads(
                    item.arguments
                )

                tool_calls.append(
                    ToolCall(
                        call_id=item.call_id,
                        tool_name=item.name,
                        arguments=arguments,
                    )
                )

        if tool_calls:
            return None, tool_calls

        return response.output_text, []

    @staticmethod
    def _serialize_result(
        result: ToolResult
    ) -> str:

        payload = {
            "success": result.success,
            "data": result.data,
            "error": result.error,
        }

        return json.dumps(
            payload,
            default=str,
        )