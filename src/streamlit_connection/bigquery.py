from typing import Optional

import pandas as pd
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

# This is our connection to BigQuery


def get_connection(**credentials) -> bigquery.Client:
    """Get a connection to BigQuery

    Returns:
        bigquery.Client: BigQuery client
    """
    if not credentials:
        if "bigquery" in st.secrets:
            credentials = st.secrets["bigquery"]

    creds = service_account.Credentials.from_service_account_info(credentials)
    return bigquery.Client(credentials=creds)


def get_dataframe(
    query: str, connection: Optional[bigquery.Client] = None
) -> pd.DataFrame:
    if connection is None:
        connection = get_connection()
    return connection.query(query).to_dataframe()
