
transport inheritance structure
_______________________________

`PermissionServiceTransport` is the ABC for all transports.
- public child `PermissionServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `PermissionServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BasePermissionServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `PermissionServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
