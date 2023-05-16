from typing import Optional

from domain import PDF
from werkzeug.datastructures import FileStorage


def to_pdf(file: FileStorage) -> Optional[PDF]:
    if file is None or file.filename is None:
        return None

    file_extension = file.filename.split(".")[-1]

    if file_extension != "pdf":
        return None

    return PDF(
        stream=file.stream,
        filename=file.filename,
        name=file.name,
        content_type=file.content_type,
        content_length=file.content_length,
        headers=file.headers,
    )
