import pandas as pd
import pytest
from streamlit import StopException

from streamlit_connection import postgres


def test_connection():
    with postgres.get_connection() as conn:
        assert conn is not None


def test_cursor():
    with postgres.get_cursor() as cursor:
        assert cursor is not None


def test_using_cursor():
    with postgres.get_cursor() as cursor:
        query = """
        select * from test
        """
        res = cursor.execute(query).fetchall()

        assert pd.DataFrame(res) is not None


def test_using_dataframe():
    query = """
    select * from test
    """
    df = postgres.get_dataframe(query)
    assert type(df) == pd.DataFrame


def test_kwargs():
    with pytest.raises(StopException):
        with postgres.get_connection(test="test"):
            pass
