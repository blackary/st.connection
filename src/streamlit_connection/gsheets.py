from typing import Optional

import pandas as pd
import streamlit as st
from shillelagh.backends.apsw.db import Cursor, connect
from shillelagh.exceptions import ProgrammingError


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


def run_query(
    query: str, to_replace: str = "SHEET_URL", url: Optional[str] = None
) -> Cursor:
    if to_replace not in query:
        raise ValueError(f"Query must contain a placeholder for the URL: {to_replace}")
    conn = get_connection()
    if url is None:
        url = st.secrets["gsheet"]["url"]

    query = query.replace(to_replace, f'"{url}"')
    try:
        resp = conn.execute(query)
        return resp
    except ProgrammingError:
        st.error(
            """Failed to connect to url. Make sure the URL is a public Google Sheet,
            which you can either pass in by setting a secret called "url" in a section
            called "gsheet", like this:

            ```toml
            # .streamlit/secrets.toml
            [gsheet]
            url = "https://docs.google.com/spreadsheets/d/foo-bar/edit#gid=0"
            ```
            or by passing it in as a parameter to the function.
            """
        )
        st.stop()


def _get_dataframe(
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
    resp = run_query(query, to_replace, url)
    rows = resp.fetchall()
    return pd.DataFrame(rows)


def get_dataframe(
    query: str,
    cache_minutes: float = 60,
    to_replace: str = "SHEET_URL",
    url: Optional[str] = None,
) -> pd.DataFrame:
    if cache_minutes > 0:
        return st.experimental_memo(_get_dataframe, ttl=cache_minutes * 60)(
            query, to_replace, url
        )
    else:
        return _get_dataframe(query, to_replace, url)
