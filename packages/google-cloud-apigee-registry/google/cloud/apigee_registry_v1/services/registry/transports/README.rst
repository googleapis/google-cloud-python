
transport inheritance structure
_______________________________

`RegistryTransport` is the ABC for all transports.
- public child `RegistryGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `RegistryGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseRegistryRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `RegistryRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
