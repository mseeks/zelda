from typing import overload, Union

from domain import PDF, AcademicPaper, Sentences
from text import to_text

import nltk
from nltk.tokenize import sent_tokenize


nltk.download("punkt")


@overload
def to_sentences(content: AcademicPaper) -> Sentences:
    ...


@overload
def to_sentences(content: PDF) -> Sentences:
    ...


@overload
def to_sentences(content: str) -> Sentences:
    ...


def to_sentences(content: Union[str, AcademicPaper, PDF]) -> Sentences:
    if isinstance(content, (AcademicPaper, PDF)):
        text = to_text(content)
        return to_sentences(text)
    elif isinstance(content, str):
        sentences = sent_tokenize(content)
        return Sentences(sentences)
    else:
        raise ValueError(f"Unsupported type: {type(content)}")
