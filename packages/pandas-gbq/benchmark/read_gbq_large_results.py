import pandas_gbq

# Select 163 MB worth of data, to time how long it takes to download large
# result sets.
df = pandas_gbq.read_gbq(
    "SELECT * FROM `bigquery-public-data.usa_names.usa_1910_2013`",
    dialect="standard",
)
