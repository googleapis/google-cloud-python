
transport inheritance structure
_______________________________

``ComplianceTransport`` is the ABC for all transports.

- public child ``ComplianceGrpcTransport`` for sync gRPC transport (defined in ``grpc.py``).
- public child ``ComplianceGrpcAsyncIOTransport`` for async gRPC transport (defined in ``grpc_asyncio.py``).
- private child ``_BaseComplianceRestTransport`` for base REST transport with inner classes ``_BaseMETHOD`` (defined in ``rest_base.py``).
- public child ``ComplianceRestTransport`` for sync REST transport with inner classes ``METHOD`` derived from the parent's corresponding ``_BaseMETHOD`` classes (defined in ``rest.py``).
