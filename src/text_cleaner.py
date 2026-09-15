"""Small text-cleaning helpers used before resume analysis."""

import re


def clean_text(text: str) -> str:
    """Return text with PDF line breaks and repeated spaces normalized.

    PDF extraction can produce separate line breaks and repeated spaces.
    Normalizing whitespace makes later matching more consistent.
    """
    return re.sub(r"\s+", " ", text).strip()
