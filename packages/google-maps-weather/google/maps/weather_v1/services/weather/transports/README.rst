
transport inheritance structure
_______________________________

`WeatherTransport` is the ABC for all transports.
- public child `WeatherGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `WeatherGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseWeatherRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `WeatherRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
