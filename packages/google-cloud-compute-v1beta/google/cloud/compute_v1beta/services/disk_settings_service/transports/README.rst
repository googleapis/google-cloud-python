
transport inheritance structure
_______________________________

`DiskSettingsServiceTransport` is the ABC for all transports.
- public child `DiskSettingsServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `DiskSettingsServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseDiskSettingsServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `DiskSettingsServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
