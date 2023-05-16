from queue import Queue
from typing import Optional, overload, Union
import tokens
from ai import to_chat_completion
from chunks import to_chunks

from domain import (
    PDF,
    AcademicPaper,
    CharacterCount,
    ChatMessage,
    ChatMessages,
    ChatModel,
    ChatPrompt,
    ChatRole,
    Chunks,
    Note,
    Notes,
    Chunk,
    ToNotesPrompt,
    TokenCount,
)

import time
import concurrent.futures

from tokens import to_token_count

# Constants
MAX_WORKERS = 10  # Maximum number of threads
TOKEN_COUNT = TokenCount(8000)
CHAT_MODEL = ChatModel.GPT_4


def process_chunk(index: int, chunk: Chunk, prompt: ChatPrompt, result_queue: Queue):
    tokens_in_chunk = to_token_count(CharacterCount(len(chunk.strip())))

    while True:
        time.sleep(1)  # Sleep for 1 second

        with tokens.gpt_4_token_balance_lock:
            if tokens_in_chunk > tokens.gpt_4_token_balance:
                continue
            tokens.gpt_4_token_balance = tokens.gpt_4_token_balance - tokens_in_chunk

        break

    messages = ChatMessages(
        [
            ChatMessage(
                {
                    "role": ChatRole.SYSTEM,
                    "content": prompt,
                }
            ),
            ChatMessage({"role": ChatRole.USER, "content": chunk.strip()}),
        ]
    )

    note_list = to_chat_completion(CHAT_MODEL, messages).split("\n")
    print("Generated note list:", note_list)
    notes = Notes([Note(note.strip()) for note in note_list if note != ""])
    print("Generated notes:", notes)
    result_queue.put((index, notes))


@overload
def to_notes(content: AcademicPaper, prompt: Optional[ChatPrompt]) -> Notes:
    ...


@overload
def to_notes(content: PDF, prompt: Optional[ChatPrompt]) -> Notes:
    ...


@overload
def to_notes(content: Chunks, prompt: Optional[ChatPrompt]) -> Notes:
    ...


def to_notes(
    content: Union[AcademicPaper, PDF, Chunk, Chunks],
    prompt: Optional[ChatPrompt] = None,
) -> Notes:
    if isinstance(content, AcademicPaper):
        if prompt is None:
            prompt = ToNotesPrompt.ACADEMIC_PAPER.value

        chunks = to_chunks(content, chunk_length=TOKEN_COUNT)
        notes = to_notes(chunks, prompt)

        return notes
    elif isinstance(content, PDF):
        if prompt is None:
            prompt = ToNotesPrompt.PDF.value
        chunks = to_chunks(content, chunk_length=TOKEN_COUNT)
        notes = to_notes(chunks, prompt)

        return notes
    elif isinstance(content, Chunks):
        if prompt is None:
            prompt = ToNotesPrompt.CHUNKS.value

        result_queue: Queue = Queue()

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for i, chunk in enumerate(content):
                executor.submit(process_chunk, i, chunk, prompt, result_queue)
            executor.shutdown(wait=True)

        # Retrieve the results from the queue in the correct order
        notes_lists: list[str] = [""] * len(content)
        for _ in range(len(content)):
            index, result = result_queue.get()
            notes_lists[index] = result

        notes = Notes(
            [
                Note(note.strip())
                for notes_list in notes_lists
                for note in notes_list
                if note != ""
            ]
        )

        return notes
    else:
        raise ValueError(f"Unsupported type: {type(content)}")
