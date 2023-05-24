from typing import Union
from domain import PDF, AcademicPaper, Sentences
from text import to_text

import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")

def to_sentences(content: Union[AcademicPaper, PDF]) -> Sentences:
    text = to_text(content)
    sentences = sent_tokenize(text)

    return Sentences(sentences)