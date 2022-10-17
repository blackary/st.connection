from contextlib import contextmanager

import pandas as pd
import psycopg
import streamlit as st
from psycopg import OperationalError, ProgrammingError


def get_creds(**credentials) -> dict:
    if not credentials:
        if "postgres" in st.secrets:
            credentials = st.secrets["postgres"]
            if set(credentials.keys()) == {"host"}:
                credentials = {"conninfo": credentials["host"]}
    return credentials


def error(**credentials):
    st.error(
        f"""
        Failed to connect to Postgres after passing in the following kwargs:
        `{", ".join(credentials.keys())}`

        Please pass all of the connection details in the `host` string,
        like this:

        ```toml
        host = 'postgres://username:password@host:port/'
        ```

        This value can either be set under a `postgres` key in a
        `.streamlit/secrets.toml` file, or passed directly to the
        `get_connection` function.

        See https://docs.streamlit.io/knowledge-base/tutorials/databases/postgres
        for more details
        """
    )
    st.stop()


@contextmanager
def get_connection(**credentials):
    credentials = get_creds(**credentials)

    try:
        connection = psycopg.connect(**credentials)
    except (OperationalError, ProgrammingError):
        error(**credentials)

    try:
        yield connection
    finally:
        connection.close()


@contextmanager
def get_cursor(**credentials):
    with get_connection(**credentials) as conn:
        yield conn.cursor()


def _get_dataframe(query, **credentials):
    with get_connection(**credentials) as conn:
        return pd.read_sql(query, con=conn)


def get_dataframe(
    query: str,
    cache_minutes: float = 60,
    **credentials,
) -> pd.DataFrame:
    if cache_minutes > 0:
        return st.experimental_memo(_get_dataframe, ttl=cache_minutes * 60)(
            query, **credentials
        )
    else:
        return _get_dataframe(query, **credentials)
