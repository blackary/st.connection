import pandas as pd
import pytest
from pymongo import MongoClient
from streamlit import StopException


def test_connection():
    from streamlit_connection import mongo

    conn = mongo.get_connection()

    assert type(conn) == MongoClient

    db = conn["test"]
    db.command("ping")


def test_kwargs():
    from streamlit_connection import mongo

    with pytest.raises(StopException):
        mongo.get_connection(test="test")


def test_get_dataframe():
    from streamlit_connection import mongo

    df = mongo.get_dataframe("test", "test")

    assert type(df) == pd.DataFrame
