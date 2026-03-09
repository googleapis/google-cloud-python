from google.cloud import spanner
from gooogle.cloud.spanner_v1 import RequestOptions

client = spanner.Client()
instance = client.instance('test-instance')
database = instance.database('test-db')

with database.snapshot() as snapshot:
    results = snapshot.execute_sql("SELECT * in all_types LIMIT %s", )

database.drop()