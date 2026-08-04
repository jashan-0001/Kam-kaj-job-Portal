import streamlit as st
import traceback

from utils.logger import logger


def handle_exception(
    exception,
    user_message="Something went wrong."
):
    """
    Log exception and display full traceback during development.
    """

    logger.exception(str(exception))

    st.error(user_message)

    st.exception(exception)

    st.code(traceback.format_exc())