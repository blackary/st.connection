import pandas as pd

from streamlit_connection import bigquery


def test_connection():
    conn = bigquery.get_connection()
    assert conn is not None


def test_dataframe():
    query = """
    select 'hello' as test
    union all
    select 'world' as test
    """
    df = bigquery.get_dataframe(query)
    assert type(df) == pd.DataFrame
