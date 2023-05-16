from functools import reduce
from typing import Union, overload
from characters import to_character_count

from domain import (
    PDF,
    AcademicPaper,
    CharacterCount,
    Chunks,
    Sentence,
    Sentences,
    Chunk,
    TokenCount,
)
from sentences import to_sentences


def split_sentence(sentence: Sentence, chunk_length: CharacterCount) -> list[str]:
    return [
        sentence[i : i + chunk_length] for i in range(0, len(sentence), chunk_length)
    ]


@overload
def to_chunks(
    content: AcademicPaper, chunk_length: Union[CharacterCount, TokenCount]
) -> Chunks:
    ...


@overload
def to_chunks(content: PDF, chunk_length: Union[CharacterCount, TokenCount]) -> Chunks:
    ...


@overload
def to_chunks(
    content: Sentences, chunk_length: Union[CharacterCount, TokenCount]
) -> Chunks:
    ...


def to_chunks(
    content: Union[AcademicPaper, PDF, Sentences],
    chunk_length: Union[CharacterCount, TokenCount] = TokenCount(2000),
) -> Chunks:
    if isinstance(content, (AcademicPaper, PDF)):
        sentences = to_sentences(content)
        return to_chunks(sentences, chunk_length)
    elif isinstance(content, Sentences):
        if isinstance(chunk_length, TokenCount):
            chunk_length = to_character_count(chunk_length)

        def reducer(acc, sentence):
            if len(sentence) > chunk_length:
                split_sentences = split_sentence(sentence, chunk_length)
                acc[-1] += " " + split_sentences[0]
                acc.extend(split_sentences[1:])
            elif len(acc[-1]) + len(sentence) > chunk_length:
                acc.append(sentence)
            else:
                acc[-1] += " " + sentence
            return acc

        chunk_strs = reduce(reducer, content, [""])
        chunks = [Chunk(chunk_str) for chunk_str in chunk_strs if chunk_str.strip()]

        return Chunks(chunks)
    else:
        raise ValueError(f"Unsupported type: {type(content)}")
