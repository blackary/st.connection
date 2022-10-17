from typing import Optional

import pandas as pd
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account


def get_connection(**credentials) -> bigquery.Client:
    """Get a connection to BigQuery

    Returns:
        bigquery.Client: BigQuery client
    """
    if not credentials:
        if "bigquery" in st.secrets:
            credentials = st.secrets["bigquery"]

    try:
        creds = service_account.Credentials.from_service_account_info(credentials)
        return bigquery.Client(credentials=creds)
    except ValueError:
        st.error(
            f"""
            Connection to BigQuery failed.
            You passed the following kwargs:

            `{", ".join(credentials.keys())}`

            Please pass in `type`, `project_id`, `private_key_id`, `private_key`,
            `client_email`, `client_id`, `auth_uri`, `token_uri`,
            `auth_provider_x509_cert_url` and `client_x509_cert_url`

            These values can either be set under a `bigquery` key in a
            `.streamlit/secrets.toml` file, or passed directly to the
            `get_connection` function.

            See https://docs.streamlit.io/knowledge-base/tutorials/databases/bigquery
            for more details
            """
        )
        st.stop()


def get_dataframe(
    query: str, connection: Optional[bigquery.Client] = None, **credentials
) -> pd.DataFrame:
    if connection is None:
        connection = get_connection(**credentials)
    return connection.query(query).to_dataframe()
