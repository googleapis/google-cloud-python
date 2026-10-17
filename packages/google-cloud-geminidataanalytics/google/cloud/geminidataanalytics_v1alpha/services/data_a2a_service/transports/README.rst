
transport inheritance structure
_______________________________

``DataA2AServiceTransport`` is the ABC for all transports.

- public child ``DataA2AServiceGrpcTransport`` for sync gRPC transport (defined in ``grpc.py``).
- public child ``DataA2AServiceGrpcAsyncIOTransport`` for async gRPC transport (defined in ``grpc_asyncio.py``).
- private child ``_BaseDataA2AServiceRestTransport`` for base REST transport with inner classes ``_BaseMETHOD`` (defined in ``rest_base.py``).
- public child ``DataA2AServiceRestTransport`` for sync REST transport with inner classes ``METHOD`` derived from the parent's corresponding ``_BaseMETHOD`` classes (defined in ``rest.py``).
