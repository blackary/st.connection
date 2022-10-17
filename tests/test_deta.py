import pandas as pd
import pytest
from streamlit import StopException

from streamlit_connection import deta_base


def test_deta_base_get_dataframe():
    df = deta_base.get_dataframe("test")
    assert type(df) == pd.DataFrame


def test_edit():
    db = deta_base.get_database("_pytest")

    db.insert({"name": "Geordi", "title": "Chief Engineer"})

    fetch_res = db.fetch({"name": "Geordi"})

    for item in fetch_res.items:
        db.delete(item["key"])


def test_bad_project_key():
    with pytest.raises(StopException):
        deta_base.get_connection(project_key="fake")
