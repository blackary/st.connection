import pandas as pd
import streamlit as st

mongo_tab, snowflake_tab, etc = st.tabs(["Mongo", "Snowflake", "Etc"])

with mongo_tab:
    with st.echo("above"):
        from streamlit_connection import mongo

        conn = mongo.get_connection()

        st.write(conn.list_database_names())

with snowflake_tab:
    with st.echo("above"):
        from streamlit_connection import snowflake

        # from streamlit_connection.snowflake import get_connectio
        query = "SELECT LABEL, LAT, LON, COUNTRY FROM WIKIMEDIA.PUBLIC.CITIES LIMIT 10"

        df = snowflake.get_dataframe(query)

        st.write(df)
