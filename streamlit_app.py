import streamlit as st

connection = st.selectbox(
    "Connection",
    [
        "mongo",
        "snowflake",
        "sqlite",
        "bigquery",
        "google sheets",
        "postgres",
        "mysql",
    ],
)

if connection == "mongo":
    with st.echo("above"):
        from streamlit_connection import mongo

        df = mongo.get_dataframe("foo", "bar")

        st.write(df)

        conn = mongo.get_connection()

        st.write(conn.list_database_names())

elif connection == "snowflake":
    with st.echo("above"):
        from streamlit_connection import snowflake

        query = "SELECT LABEL, LAT, LON, COUNTRY FROM WIKIMEDIA.PUBLIC.CITIES LIMIT 10"

        df = snowflake.get_dataframe(query)

        st.write(df)

elif connection == "sqlite":
    with st.echo("above"):
        from streamlit_connection import sqlite

        conn = sqlite.get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id integer, name text)")
        cursor.execute("INSERT INTO test VALUES (1, 'foo')")
        cursor.execute("INSERT INTO test VALUES (2, 'bar')")

        query = "select * from test"

        df = sqlite.get_dataframe(query, conn=conn)

        st.write(df)
elif connection == "bigquery":
    with st.echo("above"):
        from streamlit_connection import bigquery

        query = """
        select 'hello' as test
        union all
        select 'world' as test
        """

        df = bigquery.get_dataframe(query)

        st.write(df)
