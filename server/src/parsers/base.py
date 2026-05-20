"""
# Overview
    ## CONCEPT
    - Every parser produces the same shape(a list of Chunks) regardless of the file type
    - this uniformity lets embedding + storage become format-agnostic

    ## Flexibility
    - Each chunk has a common typed core, plus a flexible `metadata` bag
    - Each parser can have it's own metadata convention

    ## Contract
    - `ParserFn` formalises that any function `(bytes, str) -> list[Chunk]` is a parser

# Glossary
    ## @dataclass
    - used to generate boilerplate methods automatically, for classes that primarily store data
    - for example, `__init__`, `__repr__`, `__eq__` etc. methods

    ## frozen=True
    - makes Chunk immutable, preventing mutation bugs

    ## slots=True
    - saves memory when holding thousands of chunks

    ## Callable[[arg_type_1, arg_type_2], return_type]
    - type hint to indicate that the var should be a fn/method/object which can be called

"""

from dataclasses import dataclass
from typing import Any, Callable

@dataclass
class Chunk:
    text: str
    source_file: str
    chunk_index: int
    metadata: dict[str, Any]

    def for_embedding(self) -> str:
        """
        Text fed to the embedding model
        - prepends the structural location (header path / page / slide / timestamp)
        - retrieval model now sees 'where this chunk lives'
        """
        location = self._location_prefix()
        if location:
            return f"{location}\n\n{self.text}"
        return self.text
    
    def for_llm(self) -> str:
        """
        Text provided to llm at answer generation
        - currently identical to `text`
        - reserved for richer formatting later(code fence etc.)
        """
        return self.text

    def _location_prefix(self) -> str:
        meta = self.metadata
        if meta.get("header_path"):
            return "# " + " > ".join(meta["header_path"])
        if "page_number" in meta:
            return f"Page {meta['page_number']}"
        if "slide_number" in meta:
            return f"Slide {meta['slide_number']}"
        return ""


ParserFn = Callable[[bytes, str], list[Chunk]]

class UnsupportedFileTypeError(Exception):
    def __init__(self, extension: str):
        super().__init__(f"Unsupported file extension: {extension!r}")
        self.extension = extension