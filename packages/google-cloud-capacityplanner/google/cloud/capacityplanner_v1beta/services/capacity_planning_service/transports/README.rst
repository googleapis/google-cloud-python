
transport inheritance structure
_______________________________

`CapacityPlanningServiceTransport` is the ABC for all transports.
- public child `CapacityPlanningServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `CapacityPlanningServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseCapacityPlanningServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `CapacityPlanningServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
