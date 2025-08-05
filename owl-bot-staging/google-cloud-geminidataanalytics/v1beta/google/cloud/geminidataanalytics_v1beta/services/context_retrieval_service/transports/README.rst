
transport inheritance structure
_______________________________

`ContextRetrievalServiceTransport` is the ABC for all transports.
- public child `ContextRetrievalServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `ContextRetrievalServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseContextRetrievalServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `ContextRetrievalServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
