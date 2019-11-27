# spanner benchwrapper

benchwrapper.py is a gRPC wrapper around the spanner library for benchmarking purposes.

## Running

```bash
$ export SPANNER_EMULATOR_HOST=http://localhost:8080
$ pip install grpcio
$ cd spanner
$ pip install -e . # install google.cloud.spanner locally
$ cd tests/perf
$ python3 benchwrapper.py --port 8081
```

## Re-generating protos

```bash
$ pip install grpcio-tools
$ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. *.proto
```
