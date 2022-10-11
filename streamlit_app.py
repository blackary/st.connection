import streamlit as st

mongo_tab, etc = st.tabs(["Mongo", "Etc"])

with mongo_tab:
    with st.echo("above"):
        from streamlit_connection import mongo

        conn = mongo.get_connection()

        st.write(conn.list_database_names())
