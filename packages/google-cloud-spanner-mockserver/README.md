# Google Cloud Spanner Mockserver

> **NOTICE:** This is an internal library that can make breaking changes without prior notice.

## Introduction
The `google-cloud-spanner-mockserver` is a lightweight in-memory mock server for Google Cloud Spanner.


## Installation

To install the library, use pip:

```bash
pip install google-cloud-spanner-mockserver
```

## Usage

Here is a simple example of how to use the mock server to test your Spanner application.

### 1. Start the Mock Server

```python
from spannermockserver import start_mock_server

# Start the server
server, spanner_servicer, database_admin_servicer, port = start_mock_server()
```

### 2. Configure Your Client

Configure your Spanner client to connect to the mock server.

```python
import os
from google.cloud import spanner
from google.auth.credentials import AnonymousCredentials

# Set environment variable to use the emulator/mock server
os.environ["SPANNER_EMULATOR_HOST"] = f"localhost:{port}"

# Create a client with anonymous credentials
client = spanner.Client(
    project="test-project",
    credentials=AnonymousCredentials()
)
instance = client.instance("test-instance")
database = instance.database("test-database")
```

### 3. Mock Results

Use `spanner_servicer.mock_spanner` to define the results for your queries.

```python
from google.cloud.spanner_v1.types import ResultSet, ResultSetMetadata, StructType, Type, TypeCode

# Define the SQL you expect
sql = "SELECT 1"

# Create a mock result set with schema definition
metadata = ResultSetMetadata(
    row_type=StructType(
        fields=[
            StructType.Field(
                name="Result",
                type=Type(code=TypeCode.INT64)
            )
        ]
    )
)
result = ResultSet(metadata=metadata)
result.rows.append(["1"])

# Add the result to the mock spanner
spanner_servicer.mock_spanner.add_result(sql, result)
```

### 4. Run Your Code

Execute your application code that queries Spanner.

```python
with database.snapshot() as snapshot:
    results = snapshot.execute_sql(sql)
    for row in results:
        print(f"Row: {row}")
```

### 5. Verify Requests (Optional)

You can inspect `spanner_servicer.requests` to verify that your code made the expected calls.

```python
print(f"Total requests received: {len(spanner_servicer.requests)}")
```

### 6. Stop the Server

```python
server.stop(None)
```

## API Reference

### `start_mock_server()`
Starts the gRPC server and returns a tuple containing:
- `server`: The gRPC server instance.
- `spanner_servicer`: The `SpannerServicer` instance.
- `database_admin_servicer`: The `DatabaseAdminServicer` instance.
- `port`: The port number the server is listening on.

### `SpannerServicer`
The implementation of the Spanner gRPC service.
- **`mock_spanner`**: Access the `MockSpanner` instance to configure behavior.
- **`requests`**: A list of all request objects received by the servicer.
- **`clear_requests()`**: Clears the list of received requests.

### `MockSpanner`
Handles the in-memory state and responses.
- **`add_result(sql, result)`**: Maps a SQL string to a `ResultSet` response.
- **`add_error(method, error)`**: Maps a gRPC method name (e.g., "ExecuteSql") to an error (an instance of `grpc_status.rpc_status._Status`) to simulate failures.
