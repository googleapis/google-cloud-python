# Copyright (c) 2017 The PyBigQuery Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

bq mk test_pybigquery
bq mk --data_location=asia-northeast1 test_pybigquery_location
bq mk test_pybigquery_alt

bq rm -f -t test_pybigquery.sample
bq rm -f -t test_pybigquery_alt.sample_alt
bq rm -f -t test_pybigquery.sample_one_row
bq rm -f -t test_pybigquery.sample_dml
bq rm -f -t test_pybigquery.sample_view
bq rm -f -t test_pybigquery_location.sample_one_row

bq mk --table --schema=$(dirname $0)/schema.json --time_partitioning_field timestamp --clustering_fields integer,string --description 'A sample table containing most data types.' test_pybigquery.sample
bq mk --table --schema=$(dirname $0)/schema.json --time_partitioning_field timestamp --clustering_fields integer,string test_pybigquery_alt.sample_alt
bq load --source_format=NEWLINE_DELIMITED_JSON --schema=$(dirname $0)/schema.json test_pybigquery.sample $(dirname $0)/sample.json

bq mk --table --schema=$(dirname $0)/schema.json --time_partitioning_field timestamp --clustering_fields integer,string test_pybigquery.sample_one_row
bq load --source_format=NEWLINE_DELIMITED_JSON --schema=$(dirname $0)/schema.json test_pybigquery.sample_one_row $(dirname $0)/sample_one_row.json

bq --location=asia-northeast1 load --source_format=NEWLINE_DELIMITED_JSON --schema=$(dirname $0)/schema.json test_pybigquery_location.sample_one_row $(dirname $0)/sample_one_row.json
bq mk --schema=$(dirname $0)/schema.json -t test_pybigquery.sample_dml

bq mk --use_legacy_sql=false --view 'SELECT string FROM test_pybigquery.sample' test_pybigquery.sample_view
