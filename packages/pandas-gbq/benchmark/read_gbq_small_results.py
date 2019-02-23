import pandas_gbq

# Select a few KB worth of data, to time downloading small result sets.
df = pandas_gbq.read_gbq(
    "SELECT * FROM `bigquery-public-data.utility_us.country_code_iso`",
    dialect="standard",
)
