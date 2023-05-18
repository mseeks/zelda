directive_notes = "You are a learning assistant writing notes. Here are some context and rules to follow:"
directive_english = "Write in English."
directive_latin_chars = "Only use Latin characters."
directive_ignore_citations = "Ignore cititations."
directive_ignore_meta_info = "Ignore document meta information like the title of the document, the author, affiliations, page numbers, and the date of publication."
directive_ignore_images = "Ignore any diagrams and images."
directive_ignore_irrelevant_text = "Ignore any text that is not relevant to the main content topic."
directive_ignore_references = "Ignore references."
directive_ignore_tables = "Ignore tables."
directive_academic_paper = "The content is from an academic paper."
directive_pdf = "The content is text scraped from a PDF file."
directive_familiarity = "Write for someone relatively familiar with the topic."
directive_importance = "Only include the most important and relevant notes."
directive_conciseness = "Be short and concise."
directive_own_words = "Write in your own words."
directive_error_free = "Write without spelling and grammatical errors."
directive_notes_format = """
Each note should be on it's own line without any preceeding dash, bullet, or number.

Format:
This is the first note.
This is the second note.
""".strip()

chunks_prompt = "\n".join(
    [
        directive_notes,
        directive_english,
        directive_latin_chars,
        directive_ignore_images,
        directive_ignore_irrelevant_text,
        directive_ignore_tables,
        directive_familiarity,
        directive_importance,
        directive_conciseness,
        directive_own_words,
        directive_error_free,
        directive_notes_format,
    ]
).strip()

academic_paper_prompt = "\n".join(
    [
        directive_notes,
        directive_academic_paper,
        directive_pdf,
        directive_english,
        directive_latin_chars,
        directive_ignore_citations,
        directive_ignore_references,
        directive_ignore_meta_info,
        directive_ignore_images,
        directive_ignore_irrelevant_text,
        directive_ignore_tables,
        directive_familiarity,
        directive_importance,
        directive_conciseness,
        directive_own_words,
        directive_error_free,
        directive_notes_format,
    ]
).strip()

pdf_prompt = "\n".join(
    [
        directive_notes,
        directive_pdf,
        directive_english,
        directive_latin_chars,
        directive_ignore_citations,
        directive_ignore_references,
        directive_ignore_meta_info,
        directive_ignore_images,
        directive_ignore_irrelevant_text,
        directive_ignore_tables,
        directive_familiarity,
        directive_importance,
        directive_conciseness,
        directive_own_words,
        directive_error_free,
        directive_notes_format,
    ]
).strip()
