# Copied largely from https://github.com/sfc-gh-brianhess/st_snow
import pandas as pd
import snowflake.connector
import streamlit as st


class _SnowflakeConnectionWrapper:
    def __init__(self):
        self._connection = None

    def get_connection(self, **kwargs) -> snowflake.connector.SnowflakeConnection:
        if not self._validate_connection():
            self._connection = self._create_connection(**kwargs)
        return self._connection

    def _validate_connection(self) -> bool:
        if self._connection is None:
            return False
        if self._connection.is_closed():
            return False
        return True

    def _create_connection(self, **kwargs) -> snowflake.connector.SnowflakeConnection:
        return snowflake.connector.connect(**kwargs)


def get_connection(**kwargs) -> snowflake.connector.SnowflakeConnection:
    if not kwargs:
        if "snowflake" in st.secrets:
            kwargs = st.secrets["snowflake"]

    @st.experimental_singleton
    def get_connection(**kwargs) -> _SnowflakeConnectionWrapper:
        return _SnowflakeConnectionWrapper()

    try:
        return get_connection(**kwargs).get_connection(**kwargs)
    except snowflake.connector.errors.ProgrammingError:
        st.error(
            f"""
            Connection to Snowflake failed.
            You passed the following kwargs:

            `{", ".join(kwargs.keys())}`

            Please pass in a `username` and `password` and
            `account`


            These values can either be set under a `snowflake` key in a
            `.streamlit/secrets.toml` file, or passed directly to the
            `get_connection` function.

            See https://docs.streamlit.io/knowledge-base/tutorials/databases/snowflake
            for more details
            """
        )
        st.stop()


def get_cursor(**kwargs) -> snowflake.connector.cursor.SnowflakeCursor:
    return get_connection(**kwargs).cursor(snowflake.connector.DictCursor)


def _get_dataframe(query: str, **kwargs) -> pd.DataFrame:
    data = pd.read_sql(query, get_connection(**kwargs))
    return data


def get_dataframe(query: str, cache_minutes: float = 60, **kwargs) -> pd.DataFrame:
    if cache_minutes > 0:
        return st.experimental_memo(_get_dataframe, ttl=cache_minutes * 60)(
            query, **kwargs
        )
    else:
        return _get_dataframe(query, **kwargs)
