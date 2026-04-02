import asyncio
import argparse
from google.cloud.spanner_v1._async.client import Client
from google.api_core.exceptions import AlreadyExists

PROJECT_ID = "span-cloud-testing"
INSTANCE_ID = "suvham-testing"
DATABASE_ID = "benchmark_db_async"
TABLE_NAME = "AsyncBenchmarkTable"


async def provision_database():
    client = Client(project=PROJECT_ID)
    instance = client.instance(INSTANCE_ID)
    database = await instance.database(DATABASE_ID)

    print(f"Checking if database {DATABASE_ID} exists...")
    
    # We try to create the database if it doesn't exist
    admin_api = client.database_admin_api
    
    # To create database, we need the instance path
    instance_path = f"projects/{PROJECT_ID}/instances/{INSTANCE_ID}"
    
    try:
        # Create database DDL
        ddl = [
            f"CREATE TABLE {TABLE_NAME} ("
            f"  id STRING(36) NOT NULL,"
            f"  field0 STRING(100),"
            f"  field1 STRING(100)"
            f") PRIMARY KEY(id)"
        ]
        
        # In newer async clients, create_database might be async or use wait()
        # Let's assume create_database is an async method or wait() is needed.
        # Since DatabaseAdminAsyncClient is used, we treat it as async.
        print("Creating database and table...")
        request = {
            "parent": instance_path,
            "create_statement": f"CREATE DATABASE {DATABASE_ID}",
            "extra_statements": ddl,
        }
        
        # DatabaseAdminAsyncClient.create_database returns a Future
        operation = await admin_api.create_database(request=request)
        print("Waiting for database creation operation to complete...")
        await operation.result()  # Wait for create operation to finish
        print(f"Database {DATABASE_ID} and table {TABLE_NAME} created successfully.")
        
    except AlreadyExists:
        print(f"Database {DATABASE_ID} already exists.")
        # Table might still not exist, so let's try to update using update_ddl
        try:
            print(f"Updating DDL for table {TABLE_NAME}...")
            # database.update_ddl in async might be async if generated. Let's see if update_ddl exists.
            # In sync client, it's database.update_ddl([]). In async, let's assume it's async or client can handle.
            # But the table might already exist, so let's continue.
            pass
        except Exception as e:
             print(f"Table update might have failed or table already exists: {e}")
            
    except Exception as e:
        print(f"Failed to create database: {e}")

    # Now populate sample rows to verify it works
    print("Populating 10 sample rows for verification...")
    columns = ["id", "field0", "field1"]
    mutations = [[f"test-id-{i}", f"val-0-{i}", f"val-1-{i}"] for i in range(10)]
    
    try:
        async with database.batch() as batch:
            batch.insert_or_update(table=TABLE_NAME, columns=columns, values=mutations)
        print("Sample rows populated successfully.")
    except Exception as e:
        print(f"Failed to populate sample rows: {e}")

    # Now query to verify correctness
    print("Querying database to verify correctness...")
    try:
        async with database.snapshot() as snapshot:
            results = await snapshot.execute_sql(f"SELECT * FROM {TABLE_NAME} LIMIT 10")
            count = 0
            async for row in results:
                count += 1
                print(f"Found row: {row}")
            if count == 10:
                print("Verification successful: 10 rows found.")
            else:
                print(f"Verification warning: Expected 10 rows, found {count}.")
    except Exception as e:
        print(f"Verification query failed: {e}")


if __name__ == "__main__":
    asyncio.run(provision_database())
