
transport inheritance structure
_______________________________

`SecurityCenterTransport` is the ABC for all transports.
- public child `SecurityCenterGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `SecurityCenterGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseSecurityCenterRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `SecurityCenterRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
