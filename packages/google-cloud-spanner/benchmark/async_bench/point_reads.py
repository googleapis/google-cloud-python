import argparse
import asyncio
import random
import time
from google.cloud.spanner_v1._async.client import Client as AsyncClient
from google.cloud import spanner as sync_spanner
from benchmark.async_bench.metrics_utils import BenchmarkMetrics
import concurrent.futures

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


def sync_read_worker(database, metrics, operation_count, worker_id):
    """A worker that performs point reads synchronously."""
    print(f"Sync Worker {worker_id} started.")
    for _ in range(operation_count):
        row_id = f"user-{random.randint(0, 99999)}"
        start_op = time.perf_counter()
        
        with database.snapshot() as snapshot:
            results = snapshot.execute_sql("SELECT * FROM {} WHERE id = @id".format(TABLE_NAME), 
                                                params={"id": row_id})
            for _ in results:
                pass
                
        end_op = time.perf_counter()
        metrics.record_latency((end_op - start_op) * 1000.0)

    print(f"Sync Worker {worker_id} finished.")


async def main():
    parser = argparse.ArgumentParser(description="Benchmark Point Reads (Sync vs Async)")
    parser.add_argument("--concurrency", type=int, default=10, help="Number of concurrent workers")
    parser.add_argument("--operations", type=int, default=100, help="Number of operations per worker")
    args = parser.parse_args()

    # --- Sync Part ---
    print("\n--- Running Synchronous Benchmark ---")
    sync_client = sync_spanner.Client(project=PROJECT_ID)
    sync_instance = sync_client.instance(INSTANCE_ID)
    sync_database = sync_instance.database(DATABASE_ID)

    # Warmup Sync
    print("Warming up Synchronous Client (10 operations)...")
    sync_read_worker(sync_database, BenchmarkMetrics(), 10, "warmup")

    sync_metrics = BenchmarkMetrics()
    sync_metrics.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = [executor.submit(sync_read_worker, sync_database, sync_metrics, args.operations, i) for i in range(args.concurrency)]
        concurrent.futures.wait(futures)

    sync_metrics.stop()
    sync_metrics.report("Scenario A (Sync Point Reads)")

    # --- Async Part ---
    print("\n--- Running Asynchronous Benchmark ---")
    async_client = AsyncClient(project=PROJECT_ID)
    async_instance = async_client.instance(INSTANCE_ID)
    async_database = await async_instance.database(DATABASE_ID)

    # Warmup Async
    print("Warming up Asynchronous Client (10 operations)...")
    await read_worker(async_database, BenchmarkMetrics(), 10, "warmup")

    async_metrics = BenchmarkMetrics()
    async_metrics.start()

    tasks = [read_worker(async_database, async_metrics, args.operations, i) for i in range(args.concurrency)]
    await asyncio.gather(*tasks)

    async_metrics.stop()
    async_metrics.report("Scenario A (Async Point Reads)")

    # --- Comparison ---
    print("\n--- Comparison (Async vs Sync) ---")
    sync_qps = float(args.concurrency * args.operations) / (sync_metrics.end_time - sync_metrics.start_time)
    async_qps = float(args.concurrency * args.operations) / (async_metrics.end_time - async_metrics.start_time)
    print(f"Sync Throughput: {sync_qps:.2f} QPS")
    print(f"Async Throughput: {async_qps:.2f} QPS")
    print(f"Throughput Ratio (Async/Sync): {async_qps / sync_qps:.2f}x")


if __name__ == "__main__":
    asyncio.run(main())
