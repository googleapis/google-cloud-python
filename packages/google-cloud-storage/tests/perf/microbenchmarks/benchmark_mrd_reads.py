import argparse
import asyncio
import os
import random
import statistics
import sys
import time

try:
    import google_crc32c
except ImportError:
    print("Error: google_crc32c package is not installed in the python environment.", file=sys.stderr)
    sys.exit(1)

from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage.asyncio.async_multi_range_downloader import AsyncMultiRangeDownloader
from google.cloud.storage.asyncio.async_appendable_object_writer import AsyncAppendableObjectWriter


class VoidBuffer:
    """A writeable file-like object that discards written data to save memory."""
    def __init__(self):
        self.size = 0

    def write(self, data: bytes) -> int:
        n = len(data)
        self.size += n
        return n

    def tell(self) -> int:
        return self.size


def parse_size(size_str: str) -> int:
    size_str = size_str.strip().upper()
    if size_str.endswith("KIB"):
        return int(float(size_str[:-3]) * 1024)
    elif size_str.endswith("MIB"):
        return int(float(size_str[:-3]) * 1024 * 1024)
    elif size_str.endswith("GIB"):
        return int(float(size_str[:-3]) * 1024 * 1024 * 1024)
    elif size_str.endswith("KB"):
        return int(float(size_str[:-2]) * 1000)
    elif size_str.endswith("MB"):
        return int(float(size_str[:-2]) * 1000 * 1000)
    elif size_str.endswith("GB"):
        return int(float(size_str[:-2]) * 1000 * 1000 * 1000)
    elif size_str.endswith("B"):
        return int(size_str[:-1])
    else:
        try:
            return int(size_str)
        except ValueError:
            raise ValueError(f"Unknown size format: {size_str}")


def format_time(seconds: float) -> str:
    if seconds < 1e-6:
        return f"{seconds * 1e9:.2f} ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.2f} \u03bcs"
    elif seconds < 1.0:
        return f"{seconds * 1e3:.2f} ms"
    else:
        return f"{seconds:.2f} s"


async def download_range(
    grpc_client: AsyncGrpcClient,
    bucket_name: str,
    object_name: str,
    start_byte: int,
    size: int,
    enable_checksum: bool,
) -> float:
    mrd = AsyncMultiRangeDownloader(grpc_client, bucket_name, object_name)
    try:
        await mrd.open()
        output_buffer = VoidBuffer()
        start = time.perf_counter()
        await mrd.download_ranges(
            [(start_byte, size, output_buffer)],
            enable_checksum=enable_checksum,
        )
        end = time.perf_counter()
        return end - start
    finally:
        if mrd.is_stream_open:
            await mrd.close()


async def upload_random_object(
    grpc_client: AsyncGrpcClient,
    bucket_name: str,
    object_name: str,
    total_size_bytes: int,
    chunk_size_bytes: int,
):
    print(f"Uploading a new random object of size {total_size_bytes} bytes to gs://{bucket_name}/{object_name}...")
    print(f"Upload chunk size: {chunk_size_bytes} bytes")
    
    writer = AsyncAppendableObjectWriter(
        client=grpc_client,
        bucket_name=bucket_name,
        object_name=object_name,
        generation=0,
    )
    
    await writer.open()
    
    uploaded_bytes = 0
    # Generate 10MiB of random buffer to slice from to avoid CPU urandom overhead
    buffer_size = min(10 * 1024 * 1024, total_size_bytes)
    random_buffer = os.urandom(buffer_size)
    
    while uploaded_bytes < total_size_bytes:
        bytes_to_write = min(chunk_size_bytes, total_size_bytes - uploaded_bytes)
        slice_start = (uploaded_bytes) % (buffer_size - bytes_to_write + 1)
        data = random_buffer[slice_start : slice_start + bytes_to_write]
        
        await writer.append(data)
        uploaded_bytes += bytes_to_write
        
    object_resource = await writer.finalize()
    print(f"Appendable object {object_name} created and finalized. Uploaded {uploaded_bytes} bytes.")


async def run_benchmark():
    parser = argparse.ArgumentParser(description="Benchmark GCS Object Range Downloads using MRD.")
    parser.add_argument("--bucket", type=str, default="chandrasiri-benchmarks-zb", help="Bucket name")
    parser.add_argument("--object", type=str, default="large_20260507_10737418240", help="Object name (10GiB size)")
    parser.add_argument("--sizes", type=str, default="1KiB,2MiB,10MiB,100MiB,1GiB", help="Sizes to benchmark")
    parser.add_argument("--iterations", type=int, default=5, help="Number of iterations per size")
    parser.add_argument("--object-size", type=str, default="10GiB", help="Size of the target GCS object (default: '10GiB')")
    parser.add_argument("--upload", action="store_true", help="Upload a new random object before running the benchmark")
    parser.add_argument("--upload-chunk-size", type=str, default="2MiB", help="Chunk size for the upload (default: 2MiB, max: 100MiB)")
    args = parser.parse_args()

    impl = getattr(google_crc32c, "implementation", None)
    print(f"google_crc32c implementation: {impl}")
    if impl != "c":
        print(f"Error: google_crc32c implementation is '{impl}', expected 'c'", file=sys.stderr)
        sys.exit(1)

    sizes_to_test = []
    for s in args.sizes.split(","):
        s_clean = s.strip().upper()
        if s_clean == "FULL":
            sizes_to_test.append(("full", 0))
        else:
            try:
                sizes_to_test.append((s.strip(), parse_size(s)))
            except ValueError as e:
                print(f"Error parsing size '{s}': {e}", file=sys.stderr)
                sys.exit(1)

    try:
        object_size_bytes = parse_size(args.object_size)
    except ValueError as e:
        print(f"Error parsing object-size '{args.object_size}': {e}", file=sys.stderr)
        sys.exit(1)

    try:
        upload_chunk_size_bytes = parse_size(args.upload_chunk_size)
    except ValueError as e:
        print(f"Error parsing upload-chunk-size '{args.upload_chunk_size}': {e}", file=sys.stderr)
        sys.exit(1)

    if upload_chunk_size_bytes > 100 * 1024 * 1024:
        print("Error: max upload-chunk-size is 100MiB", file=sys.stderr)
        sys.exit(1)

    grpc_client = AsyncGrpcClient()

    if args.upload:
        try:
            await upload_random_object(
                grpc_client,
                args.bucket,
                args.object,
                object_size_bytes,
                upload_chunk_size_bytes,
            )
        except Exception as e:
            print(f"Upload failed: {e}", file=sys.stderr)
            sys.exit(1)

    # Warmup phase
    print("Warming up for 10 seconds to establish connections...")
    warmup_start = time.perf_counter()
    warmup_downloads = 0
    while time.perf_counter() - warmup_start < 10.0:
        # download a small chunk (10MiB) to warm up channels
        start_byte = random.randint(0, object_size_bytes - 10 * 1024 * 1024)
        try:
            await download_range(
                grpc_client,
                args.bucket,
                args.object,
                start_byte,
                10 * 1024 * 1024,
                enable_checksum=True,
            )
            warmup_downloads += 1
        except Exception:
            pass
    print(f"Warmup complete. Completed {warmup_downloads} warmup downloads.")
    print()

    print(f"Benchmarking MRD Reads on gs://{args.bucket}/{args.object} with {args.iterations} iterations:")
    print("-" * 150)
    print(f"{'Size (String)':<15} | {'Checksum':<10} | {'Size (Bytes)':<12} | {'Min':<12} | {'Max':<12} | {'Mean':<12} | {'Median':<12} | {'Avg Throughput':<15} | {'% Chk-Disabled Change':<22}")
    print("-" * 150)

    for size_str, size_bytes in sizes_to_test:
        # Pre-generate random offsets so that both Enabled and Disabled configurations run on the exact same offsets
        if size_bytes == 0:
            offsets = [0 for _ in range(args.iterations)]
        else:
            offsets = [random.randint(0, object_size_bytes - size_bytes) for _ in range(args.iterations)]
        enabled_throughput = None

        for enable_chk in [True, False]:
            chk_label = "Enabled" if enable_chk else "Disabled"
            durations = []
            
            for i, start_byte in enumerate(offsets):
                print(f"  [{size_str} - Checksum {chk_label}] Iteration {i+1}/{args.iterations}: Downloading from offset {start_byte}...", end="", flush=True)
                
                try:
                    duration = await download_range(grpc_client, args.bucket, args.object, start_byte, size_bytes, enable_checksum=enable_chk)
                    durations.append(duration)
                    print(f" Done in {format_time(duration)}")
                except Exception as e:
                    print(f" Failed: {e}")
                    continue

            if not durations:
                print(f"{size_str:<15} | {chk_label:<10} | {size_bytes:<12} | {'FAILED':<12} | {'FAILED':<12} | {'FAILED':<12} | {'FAILED':<12} | {'N/A':<15} | {'N/A':<22}")
                continue

            min_time = min(durations)
            max_time = max(durations)
            mean_time = statistics.mean(durations)
            median_time = statistics.median(durations)
            
            # Throughput in MiB/s
            actual_size = object_size_bytes if size_bytes == 0 else size_bytes
            avg_throughput = (actual_size / (1024 * 1024)) / mean_time

            percent_diff_str = ""
            if enable_chk:
                enabled_throughput = avg_throughput
                percent_diff_str = "N/A"
            else:
                if enabled_throughput is not None and enabled_throughput > 0:
                    percent_increase = ((avg_throughput - enabled_throughput) / enabled_throughput) * 100
                    percent_diff_str = f"{percent_increase:+.2f}%"
                else:
                    percent_diff_str = "N/A"

            print(
                f"{size_str:<15} | {chk_label:<10} | {size_bytes:<12} | "
                f"{format_time(min_time):<12} | {format_time(max_time):<12} | "
                f"{format_time(mean_time):<12} | {format_time(median_time):<12} | "
                f"{avg_throughput:.2f} MiB/s | "
                f"{percent_diff_str:<22}"
            )
        print("-" * 150)


def main():
    asyncio.run(run_benchmark())


if __name__ == "__main__":
    main()
