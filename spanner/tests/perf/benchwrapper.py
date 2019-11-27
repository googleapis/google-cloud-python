import argparse
import sys
import time
import grpc
import os
from concurrent import futures
import spanner_pb2_grpc
import spanner_pb2
from google.cloud import spanner

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

parser = argparse.ArgumentParser()

if os.environ.get("SPANNER_EMULATOR_HOST") is None:
    sys.exit(
        "This benchmarking server only works when connected to an emulator. Please set SPANNER_EMULATOR_HOST."
    )

parser.add_argument("--port", help="The port to run on.")

args = parser.parse_args()

if args.port is None:
    sys.exit("Usage: python3 benchwrapper.py --port 8081")

client = spanner.Client()


class SpannerBenchWrapperServicer(spanner_pb2_grpc.SpannerBenchWrapperServicer):
    def Read(self, request, context):
        instance = client.instance('some-instance')
        database = instance.database('some-database')
        result = snapshot.execute_sql(request.Query)
        for row in list(result):
            # no-op
            row = row
        return spanner_pb2.EmptyResponse()

    def Insert(self, request, context):
        # TODO(deklerk): implement this
        return spanner_pb2.EmptyResponse()

    def Update(self, request, context):
        # TODO(deklerk): implement this
        return spanner_pb2.EmptyResponse()


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
spanner_pb2_grpc.add_SpannerBenchWrapperServicer_to_server(
    SpannerBenchWrapperServicer(), server
)

print("listening on localhost:" + args.port)
server.add_insecure_port("[::]:" + args.port)
server.start()
try:
    while True:
        time.sleep(_ONE_DAY_IN_SECONDS)
except KeyboardInterrupt:
    server.stop(0)
