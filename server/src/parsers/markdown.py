from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from parsers.base import Chunk
from config import settings

HEADERS = [("#", "h1"), ("##", "h2"), ("###", "h3")]

def parse(content: bytes, source_file: str) -> list[Chunk]:
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"{source_file} is not valid UTF-8 markdown")
    
    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS)
    header_docs = header_splitter.split_text(text=text)

    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )

    chunks: list[Chunk] = []
    for doc in header_docs:
        header_path = [doc.metadata[k] for k in ("h1", "h2", "h3") if k in doc.metadata]
        pieces = recursive_splitter.split_text(doc.page_content)
        for piece in pieces:
            chunks.append(Chunk(
                text=piece,
                source_file=source_file,
                chunk_index=len(chunks),
                metadata={
                    "header_path": header_path
                }
            ))

    return chunks