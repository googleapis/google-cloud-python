
transport inheritance structure
_______________________________

`EncryptionSpecServiceTransport` is the ABC for all transports.
- public child `EncryptionSpecServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `EncryptionSpecServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseEncryptionSpecServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `EncryptionSpecServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
