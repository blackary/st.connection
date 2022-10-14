import pandas as pd
from pandas.testing import assert_frame_equal

from streamlit_connection import sqlite


def test_sqlite():
    conn = sqlite.get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id integer, name text)")
    cursor.execute("INSERT INTO test VALUES (1, 'foo')")
    cursor.execute("INSERT INTO test VALUES (2, 'bar')")

    query = "select * from test"

    df = sqlite.get_dataframe(query, conn=conn)

    assert_frame_equal(df, pd.DataFrame({"id": [1, 2], "name": ["foo", "bar"]}))
