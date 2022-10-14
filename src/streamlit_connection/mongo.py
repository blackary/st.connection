import pandas as pd
import streamlit as st
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConfigurationError


@st.experimental_singleton
def _get_connection(**kwargs) -> MongoClient:
    if not kwargs:
        if "mongo" in st.secrets:
            kwargs = st.secrets["mongo"]

    try:
        return MongoClient(**kwargs)
    except ConfigurationError:
        st.error(
            f"""
            Connection to MongoDB failed. You passed the following kwargs:

            `{", ".join(kwargs.keys())}`

            The following kwargs are allowed:

            `host, port, document_class, tz_aware, connect`

            For more details, see:
            https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient
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
