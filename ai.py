import os
import openai

from domain import ChatMessages, ChatModel, Temperature

openai.api_key = os.getenv("OPENAI_API_KEY")

class NoChoicesException(Exception):
    pass

class EmptyChoicesException(Exception):
    pass

def extract_message_content(completion: dict) -> str:
    if "choices" not in completion:
        raise NoChoicesException("No choices in completion.")

    choices = completion["choices"]

    if len(choices) == 0:
        raise EmptyChoicesException("Choices are empty.")

    return choices[0]["message"]["content"]

def to_chat_completion(
    model: ChatModel, messages: ChatMessages, temperature: Temperature = Temperature(1.0)
) -> str:
    print("Temperature: ", temperature.value)
    completion = openai.ChatCompletion.create(
        model=model,
        temperature=temperature.value,
        messages=messages,
    )
    print("Completion: ", completion)

    return extract_message_content(completion) # type: ignore
