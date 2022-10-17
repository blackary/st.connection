import streamlit as st

connection = st.selectbox(
    "Connection",
    [
        "mongo",
        "snowflake",
        "sqlite",
        "bigquery",
        "google sheets",
        "s3",
        "postgres",
        "deta",
        "mysql (coming soon)",
    ],
)

bad_connection = st.checkbox("Simulate incorrect credentials")

if connection == "mongo":
    with st.echo("above"):
        from streamlit_connection import mongo

        if bad_connection:
            conn = mongo.get_connection(foo="bar")
        else:
            conn = mongo.get_connection()

        st.write(conn.list_database_names())

        collections = conn["foo"].list_collection_names()

        if not collections:
            conn["foo"]["bar"].insert_one({"test": "test"})

        df = mongo.get_dataframe("foo", "bar")

        # pyarrow gets mad about the default type of `_id`
        df["_id"] = df["_id"].astype(str)

        st.write(df)

elif connection == "snowflake":
    with st.echo("above"):
        from streamlit_connection import snowflake

        query = "SELECT LABEL, LAT, LON, COUNTRY FROM WIKIMEDIA.PUBLIC.CITIES LIMIT 10"

        if bad_connection:
            df = snowflake.get_dataframe(query, foo="bar")
        else:
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

        if bad_connection:
            df = bigquery.get_dataframe(query, foo="bar")
        else:
            df = bigquery.get_dataframe(query)

        st.write(df)

elif connection == "google sheets":
    with st.echo("above"):
        from streamlit_connection import gsheets

        query = "SELECT * FROM SHEET_URL"

        if bad_connection:
            url = "https://docs.google.com/spreadsheets/d/foo-bar/edit#gid=0"
            df = gsheets.get_dataframe(query, url=url)
        else:
            df = gsheets.get_dataframe(query)

        st.write(df)

elif connection == "s3":
    with st.echo("above"):
        from streamlit_connection import s3

        query = "SELECT * FROM S3_URL LIMIT 10"

        if bad_connection:
            df = s3.get_dataframe(
                query, aws_access_key_id="bar", aws_secret_access_key="foo"
            )
        else:
            df = s3.get_dataframe(query)

        st.write(df)

elif connection == "postgres":
    with st.echo("above"):
        from streamlit_connection import postgres

        query = "SELECT * FROM test LIMIT 10"

        if bad_connection:
            df = postgres.get_dataframe(query, host="foo", user="bar")
        else:
            df = postgres.get_dataframe(query)

        st.write(df)

elif connection == "mysql":
    st.write("# Coming soon")
