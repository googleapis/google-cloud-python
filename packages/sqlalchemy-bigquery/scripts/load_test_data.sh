bq mk test_pybigquery
bq rm -f -t test_pybigquery.sample
bq rm -f -t test_pybigquery.sample_one_row
bq load --source_format=NEWLINE_DELIMITED_JSON --schema=$(dirname $0)/schema.json test_pybigquery.sample $(dirname $0)/sample.json
bq load --source_format=NEWLINE_DELIMITED_JSON --schema=$(dirname $0)/schema.json test_pybigquery.sample_one_row $(dirname $0)/sample_one_row.json

