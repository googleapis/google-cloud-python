import argparse
import sys
import time
import grpc
from concurrent import futures
import storage_pb2_grpc
import storage_pb2
from google.cloud import storage

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

parser = argparse.ArgumentParser()

# if os.environ.get("STORAGE_EMULATOR_HOST") is None:
#     sys.exit(
#         "This benchmarking server only works when connected to an emulator. Please set STORAGE_EMULATOR_HOST."
#     )

parser.add_argument("--port", help="The port to run on.")

args = parser.parse_args()

if args.port is None:
    sys.exit("Usage: python3 main.py --port 8081")

# client = storage.Client.create_anonymous_client()
client = storage.Client()


class StorageBenchWrapperServicer(storage_pb2_grpc.StorageBenchWrapperServicer):
    def Write(self, request, context):
        # TODO(deklerk): implement this
        return storage_pb2.EmptyResponse()

    def Read(self, request, context):
        bucket = client.bucket(request.bucketName)
        blob = storage.Blob(request.objectName, bucket)
        blob.download_as_string()
        return storage_pb2.EmptyResponse()


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
storage_pb2_grpc.add_StorageBenchWrapperServicer_to_server(
    StorageBenchWrapperServicer(), server
)

print("listening on localhost:" + args.port)
server.add_insecure_port("[::]:" + args.port)
server.start()
try:
    while True:
        time.sleep(_ONE_DAY_IN_SECONDS)
except KeyboardInterrupt:
    server.stop(0)
