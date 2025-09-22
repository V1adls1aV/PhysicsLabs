import logging

import pytest


@pytest.fixture(autouse=True, scope="session")
def mute_streamlit_warnings() -> None:
    logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(
        logging.ERROR
    )
