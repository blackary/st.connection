import sqlite3
from typing import Optional

import pandas as pd


def get_connection(database: str = ":memory:") -> sqlite3.Connection:
    return sqlite3.connect(database)


def get_dataframe(
    query: str, database: str = ":memory:", conn: Optional[sqlite3.Connection] = None
) -> pd.DataFrame:
    if conn is None:
        conn = get_connection(database)
    df = pd.read_sql_query(query, conn)
    return df
