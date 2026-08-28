from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    """Extract all available text from a PDF path."""
    reader = PdfReader(pdf_path)
    return "".join(page.extract_text() or "" for page in reader.pages)
