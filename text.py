import tempfile
from typing import Union, overload
from pdfminer.high_level import extract_text
from domain import PDF, AcademicPaper


@overload
def to_text(file: AcademicPaper) -> str:
    ...


@overload
def to_text(file: PDF) -> str:
    ...


def to_text(file: Union[AcademicPaper, PDF]) -> str:
    if isinstance(file, (AcademicPaper, PDF)):
        with tempfile.NamedTemporaryFile() as temp_file:
            file.save(temp_file)
            text = extract_text(temp_file.name)
        return text
    else:
        raise ValueError(f"Unsupported type: {type(file)}")
