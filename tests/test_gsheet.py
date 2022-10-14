import pandas as pd

from streamlit_connection import gsheets


def test_connection():
    conn = gsheets.get_connection()
    assert conn is not None


def test_dataframe():
    query = """SELECT * FROM SHEET_URL"""
    df = gsheets.get_dataframe(query)
    assert type(df) == pd.DataFrame
