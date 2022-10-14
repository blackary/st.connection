from typing import Optional

import pandas as pd
import streamlit as st
from shillelagh.backends.apsw.db import connect


def get_connection():
    if "gsheet" in st.secrets:
        if "service_account" in st.secrets["gsheet"]:
            service_account = st.secrets["gsheet"]["service_account"]
            connection = connect(
                ":memory:",
                adapter_kwargs={
                    "gsheetsapi": {"service_account_info": service_account}
                },
            )
            return connection
    else:
        connection = connect(
            ":memory:",
            adapter_kwargs={"gsheetsapi": {}},
        )
    return connection


def get_cursor():
    conn = get_connection()
    return conn.cursor()


def run_query(query: str, to_replace: str = "SHEET_URL", url: Optional[str] = None):
    if to_replace not in query:
        raise ValueError(f"Query must contain a placeholder for the URL: {to_replace}")
    conn = get_connection()
    if url is None:
        url = st.secrets["gsheet"]["url"]

    query = query.replace(to_replace, f'"{url}"')
    conn.execute(query)


def get_dataframe(
    query: str, to_replace: str = "SHEET_URL", url: Optional[str] = None
) -> pd.DataFrame:
    """
    Get a dataframe from a SQL query run against a Google Sheets URL.
    If you don't specify a url, it will look for a secret called "url" inside a
    section called "ghsheets"
    You must pass a query with a placeholder for the URL. For example:
    SELECT * FROM SHEET_URL
    And the placeholder will be replaced with the URL.
    """
    if to_replace not in query:
        raise ValueError(f"Query must contain a placeholder for the URL: {to_replace}")
    conn = get_connection()
    if url is None:
        url = st.secrets["gsheet"]["url"]

    query = query.replace(to_replace, f'"{url}"')
    rows = conn.execute(query)
    rows = rows.fetchall()
    return pd.DataFrame(rows)
