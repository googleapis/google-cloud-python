
transport inheritance structure
_______________________________

``BlockchainNodeEngineTransport`` is the ABC for all transports.

- public child ``BlockchainNodeEngineGrpcTransport`` for sync gRPC transport (defined in ``grpc.py``).
- public child ``BlockchainNodeEngineGrpcAsyncIOTransport`` for async gRPC transport (defined in ``grpc_asyncio.py``).
- private child ``_BaseBlockchainNodeEngineRestTransport`` for base REST transport with inner classes ``_BaseMETHOD`` (defined in ``rest_base.py``).
- public child ``BlockchainNodeEngineRestTransport`` for sync REST transport with inner classes ``METHOD`` derived from the parent's corresponding ``_BaseMETHOD`` classes (defined in ``rest.py``).
