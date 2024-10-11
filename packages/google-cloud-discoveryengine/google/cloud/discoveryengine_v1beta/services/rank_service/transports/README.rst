
transport inheritance structure
_______________________________

`RankServiceTransport` is the ABC for all transports.
- public child `RankServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `RankServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseRankServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `RankServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
