# Spanner DBAPI Driver

ALPHA: This library is still in development. It is not yet ready for production use.

Python DBAPI 2.0 compliant driver for Google Cloud Spanner. This library implements the standard Python DBAPI 2.0 interfaces and exposes an API that is similar to other SQL database drivers.

## Usage

Create a connection using a connection string:

```python
from google.cloud.spanner_driver import connect

connection_string = "projects/my-project/instances/my-instance/databases/my-database"

with connect(connection_string) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 'Hello World' as Message")
        row = cursor.fetchone()
        print(f"Greeting from Spanner: {row[0]}")
```

## Emulator

The driver can also connect to the Spanner Emulator. The easiest way to do this is to set `auto_config_emulator=true` in the connection string. This instructs the driver to connect to the Emulator on `localhost:9010` and to automatically create the Spanner instance and database in the connection string if these do not already exist.

```python
from google.cloud.spanner_driver import connect

# Setting auto_config_emulator=true instructs the driver to connect to the Spanner emulator on 'localhost:9010',
# and to create the instance and database on the emulator if these do not already exist.
connection_string = "projects/my-project/instances/my-instance/databases/my-database;auto_config_emulator=true"

with connect(connection_string) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 'Hello World' as Message")
        row = cursor.fetchone()
        print(f"Greeting from Spanner: {row[0]}")
```

## Examples

See the [`samples`](./samples) directory for ready-to-run examples for how to use various Spanner features with this driver.
