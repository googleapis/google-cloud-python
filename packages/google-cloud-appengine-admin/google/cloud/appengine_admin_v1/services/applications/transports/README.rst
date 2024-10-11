
transport inheritance structure
_______________________________

`ApplicationsTransport` is the ABC for all transports.
- public child `ApplicationsGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `ApplicationsGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseApplicationsRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `ApplicationsRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
