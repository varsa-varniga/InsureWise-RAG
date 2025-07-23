def clean_chunk(chunk: str) -> str:
    """
    Cleans a single text chunk by:
    - Replacing newline characters with spaces
    - Stripping leading/trailing whitespace
    """
    return chunk.replace('\n', ' ').strip()


def format_context_chunks(chunks: list[str]) -> str:
    """
    Takes a list of raw context chunks and returns a single formatted string.
    """
    cleaned_chunks = [clean_chunk(chunk) for chunk in chunks]
    return "\n\n".join(cleaned_chunks)
