import pandas as pd
import pytest
from streamlit import StopException

from streamlit_connection import s3


def test_connection():
    conn = s3.get_connection()
    assert conn is not None


def test_bad_connection():
    with pytest.raises(StopException):
        s3.get_dataframe(
            "SELECT * FROM S3_URL LIMIT 10",
            aws_access_key_id="bad",
            aws_secret_access_key="bad",
        )


def test_dataframe():
    query = """SELECT * FROM S3_URL LIMIT 10"""
    df = s3.get_dataframe(query)
    assert type(df) == pd.DataFrame
