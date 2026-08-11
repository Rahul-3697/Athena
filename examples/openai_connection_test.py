import os

import openai
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def main():

    print("API key loaded:", bool(os.getenv("OPENAI_API_KEY")))
    print("HTTP_PROXY:", os.getenv("HTTP_PROXY"))
    print("HTTPS_PROXY:", os.getenv("HTTPS_PROXY"))
    print("ALL_PROXY:", os.getenv("ALL_PROXY"))
    print("NO_PROXY:", os.getenv("NO_PROXY"))

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        max_retries=0,
        timeout=20.0,
    )

    try:

        response = client.responses.create(
            model="gpt-4",
            input="Say hello.",
        )

        print("\nSUCCESS")
        print(response.output_text)

    except openai.APIConnectionError as exc:

        print("\nCONNECTION ERROR")
        print(exc)

        print("\nUNDERLYING CAUSE")
        print(repr(exc.__cause__))


if __name__ == "__main__":
    main()