from werkzeug.datastructures import FileStorage
from domain import AcademicPaper

from pdf import to_pdf, NoFilenameException, InvalidExtensionException

class ConversionFailedException(Exception):
    pass

def to_academic_paper(file: FileStorage) -> AcademicPaper:
    try:
        pdf = to_pdf(file)
    except (NoFilenameException, InvalidExtensionException) as e:
        raise ConversionFailedException("Conversion to academic paper failed.") from e

    return AcademicPaper(
        file=pdf.file,
        name=pdf.name,
        delete=False,
    )
