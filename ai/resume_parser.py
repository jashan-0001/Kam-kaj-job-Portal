from pathlib import Path

import fitz
import streamlit as st

from utils.logger import logger


# =====================================================
# CACHE MANAGEMENT
# =====================================================

def clear_resume_parser_cache():
    """
    Clear cached resume parsing results.
    """

    st.cache_data.clear()


# =====================================================
# RESUME PARSER
# =====================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def extract_resume_text(pdf_path):
    """
    Extract text from a PDF resume.

    Args:
        pdf_path (str | Path)

    Returns:
        str
    """

    if not pdf_path:

        logger.error(
            "No resume path provided."
        )

        return ""

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():

        logger.error(
            f"Resume file not found: {pdf_path}"
        )

        return ""

    if pdf_path.suffix.lower() != ".pdf":

        logger.error(
            f"Unsupported file format: {pdf_path.suffix}"
        )

        return ""

    # -------------------------------------------------
    # Optional File Size Validation (20 MB)
    # -------------------------------------------------

    max_size = 20 * 1024 * 1024

    if pdf_path.stat().st_size > max_size:

        logger.warning(
            f"Resume exceeds maximum allowed size: {pdf_path.name}"
        )

        return ""

    document = None

    try:

        logger.info(
            f"Parsing resume: {pdf_path.name}"
        )

        document = fitz.open(str(pdf_path))

        if document.is_encrypted:

            logger.error(
                f"Encrypted PDF cannot be parsed: {pdf_path.name}"
            )

            return ""

        pages = []

        for page in document:

            page_text = page.get_text("text").strip()

            if page_text:
                pages.append(page_text)

        extracted_text = "\n".join(pages).strip()

        if not extracted_text:

            logger.warning(
                f"No readable text found in {pdf_path.name}"
            )

            return ""

        logger.info(
            f"Resume parsed successfully ({document.page_count} pages): {pdf_path.name}"
        )

        return extracted_text

    except Exception:

        logger.exception(
            f"Failed to parse resume: {pdf_path.name}"
        )

        return ""

    finally:

        if document is not None:

            document.close()

            logger.debug(
                f"Closed resume file: {pdf_path.name}"
            )