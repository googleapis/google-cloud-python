import argparse
import asyncio
import random
import time
from google.cloud.spanner_v1._async.client import Client
from benchmark.async_bench.metrics_utils import BenchmarkMetrics

PROJECT_ID = "span-cloud-testing"
INSTANCE_ID = "suvham-testing"
DATABASE_ID = "benchmark_db_async"
TABLE_NAME = "AsyncBenchmarkTable"


async def read_worker(database, metrics, operation_count, worker_id):
    """A worker that performs point reads."""
    print(f"Worker {worker_id} started.")
    for _ in range(operation_count):
        row_id = f"user-{random.randint(0, 99999)}"
        start_op = time.perf_counter()
        
        # Test execute_sql
        async with database.snapshot() as snapshot:
            results = await snapshot.execute_sql(f"SELECT * FROM {TABLE_NAME} WHERE id = @id", 
                                                params={"id": row_id})
            async for _ in results:
                pass  # Just iterate
                
        end_op = time.perf_counter()
        metrics.record_latency((end_op - start_op) * 1000.0)

    print(f"Worker {worker_id} finished.")


async def main():
    parser = argparse.ArgumentParser(description="Benchmark Point Reads")
    parser.add_argument("--concurrency", type=int, default=10, help="Number of concurrent workers")
    parser.add_argument("--operations", type=int, default=100, help="Number of operations per worker")
    args = parser.parse_args()

    client = Client(project=PROJECT_ID)
    instance = client.instance(INSTANCE_ID)
    database = await instance.database(DATABASE_ID)

    metrics = BenchmarkMetrics()
    metrics.start()

    tasks = [read_worker(database, metrics, args.operations, i) for i in range(args.concurrency)]
    await asyncio.gather(*tasks)

    metrics.stop()
    metrics.report("Scenario A (Point Reads)")


if __name__ == "__main__":
    asyncio.run(main())
