import streamlit as st
from pymongo import MongoClient


def _get_connection(**kwargs) -> MongoClient:
    if not kwargs:
        if "mongo" in st.secrets:
            kwargs = st.secrets["mongo"]

    kwarg_str = str(kwargs)

    if kwarg_str not in st.session_state:
        st.session_state[kwarg_str] = MongoClient(**kwargs)
        return st.session_state[kwarg_str]

    client = MongoClient(**kwargs)
    st.session_state[kwarg_str] = client
    return client


def get_connection(**kwargs) -> MongoClient:
    connection = _get_connection(**kwargs)
    return connection
