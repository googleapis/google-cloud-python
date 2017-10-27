from google.cloud import bigquery
from datetime import datetime
import json
import sys

if len(sys.argv) < 2:
    raise Exception('need query file, usage: python {0} <queries.json>'.format(sys.argv[0]))

with open(sys.argv[1], 'r') as f:
    queries = json.loads(f.read())

client = bigquery.Client()

for query in queries:
    start_time = datetime.now()
    job = client.query(query)
    rows = job.result()

    num_rows = 0
    num_cols = None
    first_byte_time = None

    for row in rows:
        if num_rows == 0:
            num_cols = len(row)
            first_byte_time = datetime.now() - start_time
        elif num_cols != len(row):
            raise Exception('found {0} columsn, expected {1}'.format(len(row), num_cols))
        num_rows += 1
    total_time = datetime.now() - start_time
    print "query {0}: {1} rows, {2} cols, first byte {3} sec, total {4} sec"\
        .format(query, num_rows, num_cols, first_byte_time.total_seconds(), total_time.total_seconds())
