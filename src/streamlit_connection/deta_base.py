from typing import Optional

import pandas as pd
import streamlit as st
from deta import Deta


def get_connection(project_key: Optional[str] = None):
    if project_key is None:
        if "deta" in st.secrets and "project_key" in st.secrets["deta"]:
            project_key = st.secrets["deta"]["project_key"]

    try:
        deta = Deta(project_key)
        return deta
    except AssertionError:
        st.error(
            """
            Bad or missing project key. Please pass in the project key as a string,
            like this:

            ```python
            deta_base.get_dataframe("test", project_key="foo")
            ```

            Or put it in a `.streamlit/secrets.toml` file, like this:

            ```toml
            [deta]
            project_key = "foo"
            ```

            See https://docs.streamlit.io/knowledge-base/tutorials/databases/deta-base
            for more details
            """
        )
        st.stop()


def get_database(name: str, project_key: Optional[str] = None):
    deta = get_connection(project_key)
    return deta.Base(name)


def _get_dataframe(
    db_name: str,
    query: dict | list | None = None,
    limit: int = 1000,
    project_key: Optional[str] = None,
):
    db = get_database(db_name, project_key)
    return pd.DataFrame(db.fetch(query, limit=limit).items)


def get_dataframe(
    db_name: str,
    cache_minutes: float = 60,
    query: dict | list | None = None,
    limit: int = 1000,
    project_key: Optional[str] = None,
) -> pd.DataFrame:
    if cache_minutes > 0:
        return st.experimental_memo(_get_dataframe, ttl=cache_minutes * 60)(
            db_name, query, limit, project_key
        )
    else:
        return _get_dataframe(db_name, query, limit, project_key)
