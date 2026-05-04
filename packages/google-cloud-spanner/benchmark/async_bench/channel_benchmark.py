import argparse
import asyncio
import time
from typing import List
from google.cloud.spanner_v1._async.client import Client
from google.cloud.spanner_v1 import AsyncBurstyPool
from benchmark.async_bench.metrics_utils import BenchmarkMetrics

PROJECT_ID = "span-cloud-testing"
INSTANCE_ID = "suvham-testing"
DATABASE_ID = "benchmark_db_async"

async def query_worker(database, metrics, operation_count):
    """Worker that performs lightweight SELECT 1 queries."""
    for _ in range(operation_count):
        start_op = time.perf_counter()
        try:
            async with database.snapshot() as snapshot:
                results = await snapshot.execute_sql("SELECT 1")
                async for row in results:
                    pass
            end_op = time.perf_counter()
            metrics.record_latency((end_op - start_op) * 1000.0)
        except Exception as e:
            print(f"Query failed: {e}")

async def run_benchmark_case(case_name: str, concurrency: int, num_channels: int, ops_per_worker: int, project_id: str, instance_id: str, database_id: str):
    """Runs a single benchmark scenario with emulated channel count."""
    print(f"\n>>> Running Scenario: {case_name} (Channels: {num_channels}, Concurrency: {concurrency})")
    
    clients = []
    databases = []
    
    # Large enough pool to avoid any session waiting skewing results
    pool_size = max(100, int(concurrency * 1.2 / num_channels)) 
    
    try:
        # 1. Initialize independent clients/channels
        print(f"   Initializing {num_channels} independent channel(s)...")
        for i in range(num_channels):
            client = Client(project=project_id)
            clients.append(client)
            instance = client.instance(instance_id)
            # Each gets its own BurstyPool
            pool = AsyncBurstyPool(target_size=pool_size)
            db = await instance.database(database_id, pool=pool)
            databases.append(db)
            
        # Warmup all channels concurrently to prime connection
        print("   Warming up channels...")
        warmup_tasks = []
        for db in databases:
            # Warmup 5 ops
            warmup_tasks.append(query_worker(db, BenchmarkMetrics(), 5))
        await asyncio.gather(*warmup_tasks)
        
        # 2. Setup tracking
        metrics = BenchmarkMetrics()
        
        # 3. Distribute workers across channels round-robin
        tasks = []
        for i in range(concurrency):
            assigned_db = databases[i % num_channels]
            tasks.append(query_worker(assigned_db, metrics, ops_per_worker))
            
        # 4. Execute
        print(f"   Executing {len(tasks)} async tasks...")
        metrics.start()
        await asyncio.gather(*tasks)
        metrics.stop()
        
        res = metrics.report(case_name)
        return res
        
    finally:
        # 5. Cleanup clients
        for client in clients:
            try:
                # Safely attempt transport closure if available
                if hasattr(client, "spanner_api") and hasattr(client.spanner_api, "transport"):
                    await client.spanner_api.transport.close()
            except:
                pass

def print_comparison_table(results_summary):
    """Prints beautiful terminal comparative table."""
    print("\n" + "="*80)
    print(f"{'CONCURRENCY':<12} | {'1-CH QPS':<10} | {'4-CH QPS':<10} | {'P95 1-CH':<10} | {'P95 4-CH':<10} | {'DELTA QPS'}")
    print("-" * 80)
    
    for c in sorted(results_summary.keys()):
        dat = results_summary[c]
        qps1 = dat.get(1, {}).get("throughput_qps", 0)
        qps4 = dat.get(4, {}).get("throughput_qps", 0)
        p95_1 = dat.get(1, {}).get("latency_p95_ms", 0)
        p95_4 = dat.get(4, {}).get("latency_p95_ms", 0)
        
        delta_pct = ((qps4 - qps1) / qps1 * 100) if qps1 > 0 else 0
        
        print(f"{c:<12} | {qps1:<10.1f} | {qps4:<10.1f} | {p95_1:<10.2f} | {p95_4:<10.2f} | {delta_pct:+.1f}%")
    print("="*80 + "\n")

async def main():
    parser = argparse.ArgumentParser(description="Compare Single vs Emulated Multi-Channel Throughput")
    parser.add_argument("--ops", type=int, default=50, help="Operations per concurrency loop worker")
    parser.add_argument("--project", default=PROJECT_ID)
    parser.add_argument("--instance", default=INSTANCE_ID)
    parser.add_argument("--database", default=DATABASE_ID)
    parser.add_argument("--concurrencies", default="50,100,250,500", help="Comma-separated concurrencies list")
    args = parser.parse_args()
    
    concurrency_levels = [int(x.strip()) for x in args.concurrencies.split(",")]
    summary = {}
    
    for concurrency in concurrency_levels:
        summary[concurrency] = {}
        
        # Run Single-Channel
        res1 = await run_benchmark_case(
            f"Concurrency_{concurrency}_1CH", 
            concurrency=concurrency, 
            num_channels=1, 
            ops_per_worker=args.ops,
            project_id=args.project,
            instance_id=args.instance,
            database_id=args.database
        )
        summary[concurrency][1] = res1
        
        # Cool down slightly
        await asyncio.sleep(2)
        
        # Run Multi-Channel (4)
        res4 = await run_benchmark_case(
            f"Concurrency_{concurrency}_4CH", 
            concurrency=concurrency, 
            num_channels=4, 
            ops_per_worker=args.ops,
            project_id=args.project,
            instance_id=args.instance,
            database_id=args.database
        )
        summary[concurrency][4] = res4
        
        await asyncio.sleep(2)

    print_comparison_table(summary)

if __name__ == "__main__":
    asyncio.run(main())
