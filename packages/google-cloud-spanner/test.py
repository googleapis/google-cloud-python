import base64
import time
from google.cloud import spanner
from google.auth.credentials import AnonymousCredentials

instance_id = 'test-instance'
database_id = 'test-db'

spanner_client = spanner.Client(
    project='test-project',
    client_options={"api_endpoint": 'localhost:9010'},
    credentials=AnonymousCredentials()
)

instance = spanner_client.instance(instance_id)
op = instance.create()
op.result()

database = instance.database(database_id, ddl_statements=[
    "CREATE TABLE Test (id STRING(36) NOT NULL, megafield BYTES(MAX)) PRIMARY KEY (id)"
])
op = database.create()
op.result()

# This must be large enough that the SDK will split the megafield payload across two query chunks
# and try to recombine them, causing the error:
data = base64.standard_b64encode(("a" * 1000000).encode("utf8"))

try:
    with database.batch() as batch:
        batch.insert(
            table="Test",
            columns=("id", "megafield"),
            values=[
                (1, data),
            ],
        )

    with database.snapshot() as snapshot:
        toc = time.time()
        results = snapshot.execute_sql(
            "SELECT * FROM Test"
        )
        tic = time.time()

        print("TIME: ", tic - toc)

        for row in results:
            print("Id: ", row[0])
            print("Megafield: ", row[1][:100])
finally:
    database.drop()
    instance.delete()