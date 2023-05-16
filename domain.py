from enum import Enum
from typing import TypedDict
from werkzeug.datastructures import FileStorage
from prompts import (
    chunks_prompt,
    academic_paper_prompt,
    pdf_prompt,
)


class PDF(FileStorage):
    pass


class FileExtension(str):
    pass


class MimeType(str):
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


class ChatModel(str, Enum):
    GPT_4: str = "gpt-4"
    GPT_3_5_TURBO: str = "gpt-3.5-turbo"


class ChatRole(str, Enum):
    SYSTEM: str = "system"
    USER: str = "user"
    ASSISTANT: str = "assistant"


class ChatMessage(TypedDict):
    role: ChatRole
    content: str


class ChatMessages(list[ChatMessage]):
    pass


class ChatPrompt(str):
    pass


class AcademicPaper(PDF):
    pass


class CharacterCount(int):
    pass


class TokenCount(int):
    pass


class ToNotesPrompt(ChatPrompt, Enum):
    ACADEMIC_PAPER: ChatPrompt = ChatPrompt(academic_paper_prompt)
    PDF: ChatPrompt = ChatPrompt(pdf_prompt)
    CHUNKS: ChatPrompt = ChatPrompt(chunks_prompt)
