from queue import Queue
import time
import concurrent.futures
from typing import Optional, Union

from tokens import to_token_count
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
    Temperature,
    ToNotesPrompt,
    TokenCount,
)

import tokens

MAX_WORKERS = 10
TOKEN_COUNT = TokenCount(4000)
CHAT_MODEL = ChatModel.GPT_4


def process_chunk(index: int, chunk: Chunk, prompt: ChatPrompt, result_queue: Queue):
    tokens_in_chunk = to_token_count(CharacterCount(len(chunk.strip())))

    while True:
        time.sleep(1)

        with tokens.gpt_4_token_balance_lock:
            print("Tokens in Chunk: ", tokens_in_chunk)
            if tokens_in_chunk > tokens.gpt_4_token_balance:
                continue
            tokens.gpt_4_token_balance -= tokens_in_chunk

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

    print("Sending to GPT-4: ", messages)
    note_list = to_chat_completion(CHAT_MODEL, messages, Temperature(0.5)).split("\n")
    print("Note List: ", note_list)
    notes = Notes([Note(note.strip()) for note in note_list if note])
    result_queue.put((index, notes))


def to_notes_from_chunks(chunks: Chunks, prompt: ChatPrompt) -> Notes:
    result_queue: Queue = Queue()

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for i, chunk in enumerate(chunks):
            executor.submit(process_chunk, i, chunk, prompt, result_queue)

    notes_lists = [""] * len(chunks)
    for _ in range(len(chunks)):
        index, result = result_queue.get()
        notes_lists[index] = result

    return Notes(
        Note(note.strip())
        for notes_list in notes_lists
        for note in notes_list
        if note
    )


def to_notes(
    content: Union[AcademicPaper, PDF, Chunk, Chunks],
    prompt: Optional[ChatPrompt] = None,
) -> Notes:
    if isinstance(content, (AcademicPaper, PDF)):
        if prompt is None:
            prompt = ToNotesPrompt.ACADEMIC_PAPER.value if isinstance(content, AcademicPaper) else ToNotesPrompt.PDF.value
        chunks = to_chunks(content, chunk_length=TOKEN_COUNT)
        return to_notes_from_chunks(chunks, prompt)
    elif isinstance(content, Chunks):
        if prompt is None:
            prompt = ToNotesPrompt.CHUNKS.value
        return to_notes_from_chunks(content, prompt)
    else:
        raise ValueError(f"Unsupported type: {type(content)}")
