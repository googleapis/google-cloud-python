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


async def update_row_callback(transaction, row_id):
    """Callback for read-write transaction."""
    # Read the row
    results = await transaction.execute_sql(f"SELECT * FROM {TABLE_NAME} WHERE id = @id", 
                                        params={"id": row_id},
                                        param_types={"id": "STRING"})
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


async def main():
    parser = argparse.ArgumentParser(description="Benchmark Transactions")
    parser.add_argument("--concurrency", type=int, default=5, help="Number of concurrent workers")
    parser.add_argument("--operations", type=int, default=50, help="Number of operations per worker")
    args = parser.parse_args()

    client = Client(project=PROJECT_ID)
    instance = client.instance(INSTANCE_ID)
    database = await instance.database(DATABASE_ID)

    metrics = BenchmarkMetrics()
    metrics.start()

    tasks = [transaction_worker(database, metrics, args.operations, i) for i in range(args.concurrency)]
    await asyncio.gather(*tasks)

    metrics.stop()
    metrics.report("Scenario B (Transactions)")


if __name__ == "__main__":
    asyncio.run(main())
