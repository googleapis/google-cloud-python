
transport inheritance structure
_______________________________

`CloudRedisTransport` is the ABC for all transports.
- public child `CloudRedisGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CloudRedisGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCloudRedisRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CloudRedisRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
