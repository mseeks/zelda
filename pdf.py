import tempfile
from werkzeug.datastructures import FileStorage
from domain import PDF

class NoFilenameException(Exception):
    pass

class InvalidExtensionException(Exception):
    pass

def get_file_extension(filename: str) -> str:
    return filename.split(".")[-1]

def validate_file_extension(filename: str) -> None:
    file_extension = get_file_extension(filename)
    if file_extension != "pdf":
        raise InvalidExtensionException(f"Invalid file extension: {file_extension}")

def to_pdf(file: FileStorage) -> PDF:
    if file.filename is None:
        raise NoFilenameException("Filename is missing.")

    validate_file_extension(file.filename)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file.save(temp_file.name)

    return PDF(
        file=temp_file.file,
        name=temp_file.name,
        delete=False,
    )
