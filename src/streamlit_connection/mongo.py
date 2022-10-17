import pandas as pd
import streamlit as st
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import (
    ConfigurationError,
    OperationFailure,
    ServerSelectionTimeoutError,
)


@st.experimental_singleton
def _get_connection(**kwargs) -> MongoClient:
    if not kwargs:
        if "mongo" in st.secrets:
            kwargs = st.secrets["mongo"]

    try:
        client: MongoClient = MongoClient(**kwargs)
        client.admin.command("ping")
        return client
    except (ConfigurationError, OperationFailure, ServerSelectionTimeoutError):
        st.error(
            f"""
            Connection to MongoDB failed. You passed the following kwargs:

            `{", ".join(kwargs.keys())}`

            You should either pass all of the connection details in the `host` string,
            like this:
            `host = 'mongodb+srv://username:password@host:port/'`

            Or pass them separately, like this:
            ```
            host = 'host'
            username = 'username'
            password = 'password'
            port = 'port'
            ```

            These values can either be set under a `mongo` key in a
            `.streamlit/secrets.toml` file, or passed directly to the
            `get_connection` function.

            See https://docs.streamlit.io/knowledge-base/tutorials/databases/mongodb
            for more details
        """
        )
        st.stop()


def get_connection(**kwargs) -> MongoClient:
    connection = _get_connection(**kwargs)
    return connection


def get_dataframe(db: str, collection: str, **kwargs) -> pd.DataFrame:
    connection = get_connection(**kwargs)
    _db: Database = connection[db]
    _collection = _db[collection]
    data = pd.DataFrame(list(_collection.find()))
    return data
