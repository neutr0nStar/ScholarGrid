from enum import Enum


class Converters(Enum):
    PYMUPDF4LLM = 1


class PDF2MD:

    def __init__(self, converter: Converters = Converters.PYMUPDF4LLM):
        self.converter = converter

    def convert(self, pdf_path: str) -> str:
        """
        Convert the given pdf file to markdown.
        Args:
            pdf_path: path to the pdf file

        Returns:
            Markdown content
        """
        if self.converter == Converters.PYMUPDF4LLM:
            import pymupdf4llm

            return pymupdf4llm.to_markdown(pdf_path)
        else:
            raise ValueError("Invalid converter")
