import argparse
import asyncio
import time
from google.cloud.spanner_v1._async.client import Client as AsyncClient
from google.cloud import spanner as sync_spanner
from benchmark.async_bench.metrics_utils import BenchmarkMetrics
import concurrent.futures

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


def sync_stream_worker(database, metrics, operation_count, worker_id):
    """A worker that retrieves large result sets via streaming synchronously."""
    print(f"Sync Worker {worker_id} started.")
    for _ in range(operation_count):
        start_op = time.perf_counter()
        
        with database.snapshot() as snapshot:
            results = snapshot.execute_sql("SELECT * FROM {} LIMIT 100000".format(TABLE_NAME))
            for _ in results:
                pass  # Consuming the stream quickly
                
        end_op = time.perf_counter()
        metrics.record_latency((end_op - start_op) * 1000.0)

    print(f"Sync Worker {worker_id} finished.")


async def main():
    parser = argparse.ArgumentParser(description="Benchmark Streaming Reads (Sync vs Async)")
    parser.add_argument("--concurrency", type=int, default=1, help="Number of concurrent workers (usually 1 for large streams)")
    parser.add_argument("--operations", type=int, default=1, help="Number of times to run per worker")
    args = parser.parse_args()

    # --- Sync Part ---
    print("\n--- Running Synchronous Benchmark ---")
    sync_client = sync_spanner.Client(project=PROJECT_ID)
    sync_instance = sync_client.instance(INSTANCE_ID)
    sync_database = sync_instance.database(DATABASE_ID)

    # Warmup Sync
    print("Warming up Synchronous Client (10 operations)...")
    sync_stream_worker(sync_database, BenchmarkMetrics(), 10, "warmup")

    sync_metrics = BenchmarkMetrics()
    sync_metrics.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = [executor.submit(sync_stream_worker, sync_database, sync_metrics, args.operations, i) for i in range(args.concurrency)]
        concurrent.futures.wait(futures)

    sync_metrics.stop()
    sync_metrics.report("Scenario C (Sync Streaming)")

    # --- Async Part ---
    print("\n--- Running Asynchronous Benchmark ---")
    async_client = AsyncClient(project=PROJECT_ID)
    async_instance = async_client.instance(INSTANCE_ID)
    async_database = await async_instance.database(DATABASE_ID)

    # Warmup Async
    print("Warming up Asynchronous Client (10 operations)...")
    await stream_worker(async_database, BenchmarkMetrics(), 10, "warmup")

    async_metrics = BenchmarkMetrics()
    async_metrics.start()

    tasks = [stream_worker(async_database, async_metrics, args.operations, i) for i in range(args.concurrency)]
    await asyncio.gather(*tasks)

    async_metrics.stop()
    async_metrics.report("Scenario C (Async Streaming)")

    # --- Comparison ---
    print("\n--- Comparison (Async vs Sync) ---")
    sync_qps = float(args.concurrency * args.operations) / (sync_metrics.end_time - sync_metrics.start_time)
    async_qps = float(args.concurrency * args.operations) / (async_metrics.end_time - async_metrics.start_time)
    print(f"Sync Throughput: {sync_qps:.2f} QPS")
    print(f"Async Throughput: {async_qps:.2f} QPS")
    print(f"Throughput Ratio (Async/Sync): {async_qps / sync_qps:.2f}x")


if __name__ == "__main__":
    asyncio.run(main())
