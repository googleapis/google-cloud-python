# storage benchwrapp

main.py is a gRPC wrapper around the storage library for benchmarking purposes.

## Running

```
export STORAGE_EMULATOR_HOST=localhost:8080
pip install grpcio
cd storage
pip install -e . # install google.cloud.storage locally
cd test_utils
python3 benchwrapper.py --port 8081
```

## Re-generating protos

```
pip install grpcio-tools
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. *.proto
```