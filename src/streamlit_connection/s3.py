from typing import Optional

import pandas as pd
import streamlit as st
from botocore.exceptions import ClientError, PartialCredentialsError
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
    try:
        resp = conn.execute(query)
        return resp
    except (TypeError, PartialCredentialsError, ClientError):
        st.error(
            f"""
            Failed to connect to `{url}` after passing in the following kwargs:
            `{", ".join(credentials.keys())}`

            Make sure you are passing a valid `aws_access_key_id` and
            `aws_secret_access_key`.

            These can either be passed in as parameters to the function, or set as
            secrets in a section called "s3", like this:

            ```toml
            # .streamlit/secrets.toml
            [s3]
            aws_access_key_id = "foo"
            aws_secret_access_key = "bar"
            ```

            See https://docs.streamlit.io/knowledge-base/tutorials/databases/aws-s3
            for more details.
            """
        )
        st.stop()


def _get_dataframe(
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
    resp = run_query(query, to_replace, url, **credentials)
    rows = resp.fetchall()
    return pd.DataFrame(rows)


def get_dataframe(
    query: str,
    cache_minutes: float = 60,
    to_replace: str = "S3_URL",
    url: Optional[str] = None,
    **credentials,
) -> pd.DataFrame:
    if cache_minutes > 0:
        return st.experimental_memo(_get_dataframe, ttl=cache_minutes * 60)(
            query, to_replace, url, **credentials
        )
    else:
        return _get_dataframe(query, to_replace, url, **credentials)
