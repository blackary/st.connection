import pandas as pd
import pytest
from streamlit import StopException

from streamlit_connection import gsheets


def test_connection():
    conn = gsheets.get_connection()
    assert conn is not None


def test_dataframe():
    query = """SELECT * FROM SHEET_URL"""
    df = gsheets.get_dataframe(query)
    assert type(df) == pd.DataFrame


def test_bad_url():
    query = """SELECT * FROM SHEET_URL"""
    with pytest.raises(StopException):
        gsheets.get_dataframe(
            query, url="https://docs.google.com/spreadsheets/d/foo-bar/edit#gid=0"
        )
