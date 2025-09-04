
transport inheritance structure
_______________________________

`BigQueryReadTransport` is the ABC for all transports.
- public child `BigQueryReadGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `BigQueryReadGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseBigQueryReadRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `BigQueryReadRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
