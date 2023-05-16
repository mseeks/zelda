import os
import openai

from domain import ChatMessage, ChatModel

openai.api_key = os.getenv("OPENAI_API_KEY")


def to_chat_completion(
    model: ChatModel, messages: list[ChatMessage], temperature: float = 0.5
) -> str:
    completion = openai.ChatCompletion.create(
        model=model,
        temperature=temperature,
        messages=messages,
    )

    if "choices" not in completion:
        return ""

    choices = completion["choices"]
    if len(choices) == 0:
        return ""

    return choices[0]["message"]["content"]
