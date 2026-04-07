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


async def update_row_callback(transaction, row_id):
    """Callback for read-write transaction."""
    # Read the row
    results = await transaction.execute_sql(f"SELECT * FROM {TABLE_NAME} WHERE id = @id", 
                                        params={"id": row_id})
    async for _ in results:
        pass  # Just iterate to consume
        
    # Dummy computation
    new_val = "".join(random.choice("0123456789") for _ in range(10))
    
    # Update field0
    transaction.update(table=TABLE_NAME, columns=["id", "field0"], values=[[row_id, new_val]])


async def transaction_worker(database, metrics, operation_count, worker_id):
    """A worker that performs transactions."""
    print(f"Worker {worker_id} started.")
    for _ in range(operation_count):
        row_id = f"user-{random.randint(0, 99999)}"
        start_op = time.perf_counter()
        
        try:
            # Execute transaction
            await database.run_in_transaction(update_row_callback, row_id)
        except Exception as e:
            # Handle potential aborts or conflicts if run in parallel
            # The library usually handles standard abort retries, so if it reaches here, it's a real failure.
            print(f"Transaction failed in worker {worker_id}: {e}")
            
        end_op = time.perf_counter()
        metrics.record_latency((end_op - start_op) * 1000.0)

    print(f"Worker {worker_id} finished.")


import string

def sync_transaction_worker(database, metrics, operation_count, worker_id):
    """A worker that performs transactions synchronously."""
    print(f"Sync Worker {worker_id} started.")
    for _ in range(operation_count):
        row_id = f"user-{random.randint(0, 99999)}"
        start_op = time.perf_counter()
        
        try:
            def update_columns(transaction):
                results = transaction.execute_sql(
                    "SELECT field0 FROM {} WHERE id = @id".format(TABLE_NAME),
                    params={"id": row_id}
                )
                for _ in results:
                    pass
                
                transaction.update(
                    table=TABLE_NAME,
                    columns=["id", "field0"],
                    values=[(row_id, "".join(random.choice(string.ascii_letters) for _ in range(10)))]
                )

            database.run_in_transaction(update_columns)
            end_op = time.perf_counter()
            metrics.record_latency((end_op - start_op) * 1000.0)
            
        except Exception as e:
             print(f"Sync Transaction failed in worker {worker_id}: {e}")

    print(f"Sync Worker {worker_id} finished.")


async def main():
    parser = argparse.ArgumentParser(description="Benchmark Read-Write Transactions (Sync vs Async)")
    parser.add_argument("--concurrency", type=int, default=5, help="Number of concurrent workers")
    parser.add_argument("--operations", type=int, default=20, help="Number of operations per worker")
    args = parser.parse_args()

    # --- Sync Part ---
    print("\n--- Running Synchronous Benchmark ---")
    sync_client = sync_spanner.Client(project=PROJECT_ID)
    sync_instance = sync_client.instance(INSTANCE_ID)
    sync_database = sync_instance.database(DATABASE_ID)

    # Warmup Sync
    print("Warming up Synchronous Client (10 operations)...")
    sync_transaction_worker(sync_database, BenchmarkMetrics(), 10, "warmup")

    sync_metrics = BenchmarkMetrics()
    sync_metrics.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = [executor.submit(sync_transaction_worker, sync_database, sync_metrics, args.operations, i) for i in range(args.concurrency)]
        concurrent.futures.wait(futures)

    sync_metrics.stop()
    sync_metrics.report("Scenario B (Sync Transactions)")

    # --- Async Part ---
    print("\n--- Running Asynchronous Benchmark ---")
    async_client = AsyncClient(project=PROJECT_ID)
    async_instance = async_client.instance(INSTANCE_ID)
    async_database = await async_instance.database(DATABASE_ID)

    # Warmup Async
    print("Warming up Asynchronous Client (10 operations)...")
    await transaction_worker(async_database, BenchmarkMetrics(), 10, "warmup")

    async_metrics = BenchmarkMetrics()
    async_metrics.start()

    tasks = [transaction_worker(async_database, async_metrics, args.operations, i) for i in range(args.concurrency)]
    await asyncio.gather(*tasks)

    async_metrics.stop()
    async_metrics.report("Scenario B (Async Transactions)")

    # --- Comparison ---
    print("\n--- Comparison (Async vs Sync) ---")
    sync_qps = float(args.concurrency * args.operations) / (sync_metrics.end_time - sync_metrics.start_time)
    async_qps = float(args.concurrency * args.operations) / (async_metrics.end_time - async_metrics.start_time)
    print(f"Sync Throughput: {sync_qps:.2f} QPS")
    print(f"Async Throughput: {async_qps:.2f} QPS")
    print(f"Throughput Ratio (Async/Sync): {async_qps / sync_qps:.2f}x")


if __name__ == "__main__":
    asyncio.run(main())
