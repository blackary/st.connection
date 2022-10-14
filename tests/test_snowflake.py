import pandas as pd

from streamlit_connection import snowflake


def test_connection():
    conn = snowflake.get_connection()
    assert conn is not None


def test_cursor():
    cursor = snowflake.get_cursor()
    assert cursor is not None


def test_using_cursor():
    cursor = snowflake.get_cursor()
    query = """
    select 'hello' as test
    union all
    select 'world' as test
    """
    res = cursor.execute(query).fetchall()

    assert pd.DataFrame(res) is not None


def test_using_dataframe():
    query = """
    select 'hello' as test
    union all
    select 'world' as test
    """
    df = snowflake.get_dataframe(query)
    assert type(df) == pd.DataFrame
