# st.connection

<a href="https://st-connection.streamlitapp.com" title="View on Streamlit"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"></a>

# TODO

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

  - Could look at connections from snowsql: https://snowflake.slack.com/archives/C03AQAKE6E4/p1665602652453119

- ~~Add automatic in-streamlit documention if credentials are missing~~

- Add caching

- Convert to context manager styles for everything?
  - Or find another solution to connections being left open
