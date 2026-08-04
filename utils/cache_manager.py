import streamlit as st

from utils.logger import logger

# =====================================================
# CLEAR STREAMLIT CACHE
# =====================================================

def clear_cache():
    """
    Clear all Streamlit cached data.

    Call this after any INSERT, UPDATE or DELETE
    operation so users immediately see fresh data.
    """

    try:

        st.cache_data.clear()

        logger.info(
            "Streamlit cache cleared."
        )

    except Exception:

        logger.exception(
            "Unable to clear Streamlit cache."
        )