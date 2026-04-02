import argparse
import asyncio
import time
from google.cloud.spanner_v1._async.client import Client
from benchmark.async_bench.metrics_utils import BenchmarkMetrics

PROJECT_ID = "span-cloud-testing"
INSTANCE_ID = "suvham-testing"
DATABASE_ID = "benchmark_db_async"
TABLE_NAME = "AsyncBenchmarkTable"


async def stream_worker(database, metrics, operation_count, worker_id):
    """A worker that retrieves large result sets via streaming."""
    print(f"Worker {worker_id} started.")
    for _ in range(operation_count):
        start_op = time.perf_counter()
        
        # Test large query
        async with database.snapshot() as snapshot:
            # We select all 100,000 rows, or just limit it to 100k. Since we populated 100k, we can just do 'LIMIT 100000' or select all.
            results = await snapshot.execute_sql(f"SELECT * FROM {TABLE_NAME} LIMIT 100000")
            async for _ in results:
                pass  # Consuming the stream quickly
                
        end_op = time.perf_counter()
        # Measure total latency for retrieval of the whole set
        metrics.record_latency((end_op - start_op) * 1000.0)

    print(f"Worker {worker_id} finished.")


async def main():
    parser = argparse.ArgumentParser(description="Benchmark Streaming Reads")
    parser.add_argument("--concurrency", type=int, default=1, help="Number of concurrent workers (usually 1 for large streams)")
    parser.add_argument("--operations", type=int, default=1, help="Number of times to run per worker")
    args = parser.parse_args()

    client = Client(project=PROJECT_ID)
    instance = client.instance(INSTANCE_ID)
    database = await instance.database(DATABASE_ID)

    metrics = BenchmarkMetrics()
    metrics.start()

    tasks = [stream_worker(database, metrics, args.operations, i) for i in range(args.concurrency)]
    await asyncio.gather(*tasks)

    metrics.stop()
    metrics.report("Scenario C (Streaming)")


if __name__ == "__main__":
    asyncio.run(main())
