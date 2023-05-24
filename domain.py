from enum import Enum
import io
import tempfile
from typing import TypedDict
from prompts import (
    chunks_prompt,
    academic_paper_prompt,
    pdf_prompt,
)


class PDF(tempfile._TemporaryFileWrapper):
    pass


class AcademicPaper(PDF):
    pass


class Note(str):
    pass


class Notes(list[Note]):
    pass


class Chunk(str):
    pass


class Chunks(list[Chunk]):
    pass


class Sentence(str):
    pass


class Sentences(list[Sentence]):
    pass


class CharacterCount(int):
    pass


class TokenCount(int):
    pass


class ChatModel(str, Enum):
    GPT_4 = "gpt-4"
    GPT_3_5_TURBO = "gpt-3.5-turbo"


class ChatRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(TypedDict):
    role: ChatRole
    content: str


class ChatMessages(list[ChatMessage]):
    pass


class ChatPrompt(str):
    pass


class ToNotesPrompt(ChatPrompt, Enum):
    ACADEMIC_PAPER = ChatPrompt(academic_paper_prompt)
    PDF = ChatPrompt(pdf_prompt)
    CHUNKS = ChatPrompt(chunks_prompt)


class Temperature:
    def __init__(self, value: float):
        if 0.0 <= value <= 2.0:
            self.value = value
        else:
            raise ValueError("Value must be a float between 0 and 2")

    def __float__(self):
        return self.value

