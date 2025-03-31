
transport inheritance structure
_______________________________

`WorkloadIdentityPoolsTransport` is the ABC for all transports.
- public child `WorkloadIdentityPoolsGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `WorkloadIdentityPoolsGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseWorkloadIdentityPoolsRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `WorkloadIdentityPoolsRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
