from typing import Optional

from domain import AcademicPaper
from werkzeug.datastructures import FileStorage

from pdf import to_pdf


def to_academic_paper(file: FileStorage) -> Optional[AcademicPaper]:
    pdf = to_pdf(file)

    if pdf is None:
        return None

    return AcademicPaper(
        stream=pdf.stream,
        filename=pdf.filename,
        name=pdf.name,
        content_type=pdf.content_type,
        content_length=pdf.content_length,
        headers=pdf.headers,
    )
