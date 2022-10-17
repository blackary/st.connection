# st.connection

<a href="https://st-connection.streamlitapp.com" title="View on Streamlit"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"></a>

## About

The general idea is to provide a general package streamlit_connection (eventually st.connection) which provides a number of submodules which all implement, at a minimum, `get_dataframe`, which allows you to pass in a query and return a pandas dataframe from that datasource, with a customizable cache (`cache_minutes` which defaults to `60`, but can be set to `0` to not cache, or any other value).

Each submodule also has a get_connection method, and those which expose a Cursor also have a get_cursor method

Each of these connections (other than sqlite) requires one or more credential to be able to connect. These are stored in .streamlit/secrets.toml, by default, in a section named after the submodule, like this:

```toml
# .streamlit/secrets.toml
[connection]
username = 'username'
password = 'password'

[other-connection]
host = 'my-host'
port = 1234
```

## Supported connection

| name          | submodule | host used          | notes                                                           | type  |
| ------------- | --------- | ------------------ | --------------------------------------------------------------- | ----- |
| mongo         | mongo     | mongodb.com Atlas  |                                                                 | NoSQL |
| snowflake     | snowflake | snowflake.com      |                                                                 | SQL   |
| sqlite        | sqlite    | in-memory database | Transient by default                                            | SQL   |
| bigquery      | bigquery  | bigquery           | SQL                                                             |
| google sheets | gsheets   | sheets.google.com  | Read-only with public sheets for now                            | SQL   |
| s3            | s3        | AWS S3             | Read-only, CSV/Parquet only currently (could also support json) | SQL   |
| postgresql    | postgres  | elephantsql.com    |                                                                 | SQL   |
| Deta Base     | deta_base | deta.sh            |                                                                 | NoSQL |

## TODO

- Add support for the following:
  - ~~mongodb~~
  - ~~snowflake~~
  - ~~sqlite~~
  - ~~bigquery~~
  - ~~google sheets~~
  - ~~S3~~
  - ~~postgresql~~
  - ~~deta~~
  - mysql (haven't found free host yet)
- Add some basic tests for each one
- Allow named connections (so multiple connections per db type are possible)?

  - Could look at connections from snowsql: https://docs.snowflake.com/en/user-guide/snowsql-start.html#configuring-default-connection-settings

- ~~Add automatic in-streamlit documention if credentials are missing~~

- Add caching

- Convert to context manager styles for everything?
  - Or find another solution to connections being left open
