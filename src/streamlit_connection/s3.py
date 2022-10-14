from typing import Optional

import pandas as pd
import streamlit as st
from shillelagh.backends.apsw.db import connect


def get_connection(**credentials):
    if not credentials:
        credentials = {
            "aws_access_key_id": st.secrets["s3"]["access_key_id"],
            "aws_secret_access_key": st.secrets["s3"]["secret_access_key"],
        }
    connection = connect(
        ":memory:",
        adapter_kwargs={"s3selectapi": credentials},
    )
    return connection


def get_cursor(**credentials):
    conn = get_connection(**credentials)
    return conn.cursor()


def run_query(
    query: str, to_replace: str = "S3_URL", url: Optional[str] = None, **credentials
):
    if to_replace not in query:
        raise ValueError(f"Query must contain a placeholder for the URL: {to_replace}")
    conn = get_connection(**credentials)
    if url is None:
        url = st.secrets["s3"]["url"]

    query = query.replace(to_replace, f'"{url}"')
    return conn.execute(query)


def get_dataframe(
    query: str, to_replace: str = "S3_URL", url: Optional[str] = None, **credentials
) -> pd.DataFrame:
    """
    Get a dataframe from a SQL query run against a S3 URL.
    If you don't specify a url, it will look for a secret called "url" inside a
    section called "ghsheets"
    You must pass a query with a placeholder for the URL. For example:
    SELECT * FROM S3_URL
    And the placeholder will be replaced with the URL.
    """
    if to_replace not in query:
        raise ValueError(f"Query must contain a placeholder for the URL: {to_replace}")
    conn = get_connection(**credentials)
    if url is None:
        url = st.secrets["s3"]["url"]

    query = query.replace(to_replace, f'"{url}"')
    st.write(query)
    rows = conn.execute(query)
    rows = rows.fetchall()
    # st.write(rows)
    return pd.DataFrame(rows)
