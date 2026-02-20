# Generated gRPC Code

This directory contains gRPC client and server classes generated from Google Cloud Spanner protobuf definitions.

## How to Generate

These files are generated using the `generate_grpc` nox session:

```bash
nox -s generate_grpc
```

This session performs the following steps:
1.  Clones the `googleapis/googleapis` repository.
2.  Generates Python gRPC code from the Spanner protobuf definitions using `grpcio-tools`.
3.  Copies the generated `*_grpc.py` files to this directory.
4.  Post-processes the generated files.

## Post-processing

The generated files are post-processed by the `post_process_generated_files` function in `noxfile.py`. This step is crucial because:

1.  **Type Compatibility**: The standard `protoc` generation produces code that uses standard Python protobuf classes. However, the `google-cloud-spanner` Python client library uses `proto-plus` wrappers for these types. The post-processing step modifies the imports to use the `google.cloud.spanner_v1.types` and `google.cloud.spanner_admin_database_v1.types` modules, ensuring that the mock server interacts correctly with the client library's objects.
2.  **Serialization Methods**: `proto-plus` objects use `.serialize()` and `.deserialize()` (or `.to_json()`/`.from_json()`) methods, whereas standard protobuf objects use `.SerializeToString()` and `.FromString()`. The post-processing step updates these method calls to match the `proto-plus` interface.

This ensures that the mock server can seamlessly handle requests and responses using the same objects as the official Spanner client library.

## Generated Files

The following files are generated and stored in this directory:

*   `spanner_pb2_grpc.py`: Contains the gRPC client and server classes for the Cloud Spanner API (`google.spanner.v1`).
*   `spanner_database_admin_pb2_grpc.py`: Contains the gRPC client and server classes for the Cloud Spanner Database Admin API (`google.spanner.admin.database.v1`).

## Manual Generation Command

While we recommend using `nox`, the underlying command executed to generate these files (assuming you have the `googleapis` repo cloned) is similar to:

```bash
python -m grpc_tools.protoc \
    -I . \
    --python_out=. \
    --pyi_out=. \
    --grpc_python_out=. \
    google/spanner/v1/*.proto \
    google/spanner/admin/database/v1/*.proto
```
