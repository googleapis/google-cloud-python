
transport inheritance structure
_______________________________

`ResourceSettingsServiceTransport` is the ABC for all transports.
- public child `ResourceSettingsServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `ResourceSettingsServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseResourceSettingsServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `ResourceSettingsServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
