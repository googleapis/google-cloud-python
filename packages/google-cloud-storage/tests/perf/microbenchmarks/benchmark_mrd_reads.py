import argparse
import asyncio
import logging
import os
import random
import statistics
import sys
import time
import uuid

try:
    import google_crc32c
except ImportError:
    print(
        "Error: google_crc32c package is not installed in the python environment.",
        file=sys.stderr,
    )
    sys.exit(1)

from google.cloud.storage.asyncio.async_appendable_object_writer import (
    AsyncAppendableObjectWriter,
)
from google.cloud.storage.asyncio.async_grpc_client import AsyncGrpcClient
from google.cloud.storage.asyncio.async_multi_range_downloader import (
    AsyncMultiRangeDownloader,
)


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
    logging.debug(
        f"Uploading a new random object of size {total_size_bytes} bytes to gs://{bucket_name}/{object_name}..."
    )
    logging.debug(f"Upload chunk size: {chunk_size_bytes} bytes")

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

    await writer.finalize()
    logging.debug(
        f"Appendable object {object_name} created and finalized. Uploaded {uploaded_bytes} bytes."
    )


async def run_benchmark():
    parser = argparse.ArgumentParser(
        description="Benchmark GCS Object Range Downloads using MRD."
    )
    parser.add_argument(
        "--bucket", type=str, default="chandrasiri-benchmarks-zb", help="Bucket name"
    )
    parser.add_argument(
        "--sizes",
        type=str,
        default="1KiB,100KiB,1MiB,16MiB,100MiB,1GiB",
        help="Sizes to benchmark",
    )
    parser.add_argument(
        "--iterations", type=int, default=5, help="Number of iterations per size"
    )
    parser.add_argument(
        "--upload-chunk-size",
        type=str,
        default="2MiB",
        help="Chunk size for the upload (default: 2MiB, max: 100MiB)",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Print debug/progress logs"
    )
    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(
        level=log_level, format="%(asctime)s [%(levelname)s] %(message)s"
    )

    impl = getattr(google_crc32c, "implementation", None)
    logging.info(f"google_crc32c implementation: {impl}")
    if impl != "c":
        logging.error(f"Error: google_crc32c implementation is '{impl}', expected 'c'")
        sys.exit(1)

    sizes_to_test = []
    for s in args.sizes.split(","):
        try:
            sizes_to_test.append((s.strip(), parse_size(s)))
        except ValueError as e:
            logging.error(f"Error parsing size '{s}': {e}")
            sys.exit(1)

    try:
        upload_chunk_size_bytes = parse_size(args.upload_chunk_size)
    except ValueError as e:
        logging.error(
            f"Error parsing upload-chunk-size '{args.upload_chunk_size}': {e}"
        )
        sys.exit(1)

    if upload_chunk_size_bytes > 100 * 1024 * 1024:
        logging.error("Error: max upload-chunk-size is 100MiB")
        sys.exit(1)

    grpc_client = AsyncGrpcClient()

    print(
        f"Benchmarking MRD Reads on gs://{args.bucket}/checksum_benchmarking_<size>_<random> with {args.iterations} iterations:"
    )
    print("-" * 161)
    print(
        f"{'Size (String)':<15} | {'Checksum':<10} | {'Size (Bytes)':<12} | {'Min':<12} | {'Max':<12} | {'Mean':<12} | {'Median':<12} | {'Avg Throughput (± StdDev)':<26} | {'% Chk-Disabled Change':<22}"
    )
    print("-" * 161)

    for size_str, size_bytes in sizes_to_test:
        enabled_throughput_full = None
        enabled_throughput_minus_1 = None

        for enable_chk in [True, False]:
            object_name = f"checksum_benchmarking_{size_str}_{uuid.uuid4().hex[:12]}"

            try:
                chunk_size = min(upload_chunk_size_bytes, size_bytes)
                await upload_random_object(
                    grpc_client,
                    args.bucket,
                    object_name,
                    size_bytes,
                    chunk_size,
                )
            except Exception as e:
                logging.error(f"Upload failed for size {size_str}: {e}")
                sys.exit(1)

            try:
                chk_label = "Enabled" if enable_chk else "Disabled"

                # Warmup phase using the uploaded object
                logging.info(
                    f"Warming up for 10 seconds using object {object_name} (Checksum {chk_label})..."
                )
                warmup_start = time.perf_counter()
                warmup_downloads = 0
                warmup_chunk_size = min(10 * 1024 * 1024, size_bytes)
                while time.perf_counter() - warmup_start < 10.0:
                    if size_bytes > warmup_chunk_size:
                        start_byte = random.randint(0, size_bytes - warmup_chunk_size)
                    else:
                        start_byte = 0
                    try:
                        await download_range(
                            grpc_client,
                            args.bucket,
                            object_name,
                            start_byte,
                            warmup_chunk_size,
                            enable_checksum=enable_chk,
                        )
                        warmup_downloads += 1
                    except Exception:
                        pass
                logging.info(
                    f"Warmup complete. Completed {warmup_downloads} warmup downloads."
                )

                durations_full = []
                durations_minus_1 = []

                for i in range(args.iterations):
                    # Download entire object
                    try:
                        duration = await download_range(
                            grpc_client,
                            args.bucket,
                            object_name,
                            0,
                            size_bytes,
                            enable_checksum=enable_chk,
                        )
                        durations_full.append(duration)
                        logging.debug(
                            f"  [{size_str} (Full) - Checksum {chk_label}] Iteration {i + 1}/{args.iterations}: Done in {format_time(duration)}"
                        )
                    except Exception as e:
                        logging.error(
                            f"  [{size_str} (Full) - Checksum {chk_label}] Iteration {i + 1}/{args.iterations}: Failed: {e}"
                        )

                    # Download entire object - 1 byte
                    if size_bytes > 1 and enable_chk:
                        try:
                            duration = await download_range(
                                grpc_client,
                                args.bucket,
                                object_name,
                                0,
                                size_bytes - 1,
                                enable_checksum=enable_chk,
                            )
                            durations_minus_1.append(duration)
                            logging.debug(
                                f"  [{size_str} (Full-1) - Checksum {chk_label}] Iteration {i + 1}/{args.iterations}: Done in {format_time(duration)}"
                            )
                        except Exception as e:
                            logging.error(
                                f"  [{size_str} (Full-1) - Checksum {chk_label}] Iteration {i + 1}/{args.iterations}: Failed: {e}"
                            )

                # Reporting for Full
                if not durations_full:
                    print(
                        f"{f'{size_str} (Full)':<15} | {chk_label:<10} | {size_bytes:<12} | {'FAILED':<12} | {'FAILED':<12} | {'FAILED':<12} | {'FAILED':<12} | {'N/A':<26} | {'N/A':<22}"
                    )
                else:
                    min_time = min(durations_full)
                    max_time = max(durations_full)
                    mean_time = statistics.mean(durations_full)
                    median_time = statistics.median(durations_full)
                    throughputs = [
                        (size_bytes / (1024 * 1024)) / d for d in durations_full
                    ]
                    avg_throughput = (size_bytes / (1024 * 1024)) / mean_time
                    std_dev = (
                        statistics.stdev(throughputs) if len(throughputs) >= 2 else 0.0
                    )
                    throughput_str = f"{avg_throughput:.2f} \u00b1 {std_dev:.2f} MiB/s"

                    percent_diff_str = ""
                    if enable_chk:
                        enabled_throughput_full = avg_throughput
                        percent_diff_str = "N/A"
                    else:
                        if (
                            enabled_throughput_full is not None
                            and enabled_throughput_full > 0
                        ):
                            percent_increase = (
                                (avg_throughput - enabled_throughput_full)
                                / enabled_throughput_full
                            ) * 100
                            percent_diff_str = f"{percent_increase:+.2f}%"
                        else:
                            percent_diff_str = "N/A"

                    print(
                        f"{f'{size_str} (Full)':<15} | {chk_label:<10} | {size_bytes:<12} | "
                        f"{format_time(min_time):<12} | {format_time(max_time):<12} | "
                        f"{format_time(mean_time):<12} | {format_time(median_time):<12} | "
                        f"{throughput_str:<26} | "
                        f"{percent_diff_str:<22}"
                    )

                # Reporting for Full-1
                if size_bytes > 1 and enable_chk:
                    if not durations_minus_1:
                        print(
                            f"{f'{size_str} (Full-1)':<15} | {chk_label:<10} | {size_bytes - 1:<12} | {'FAILED':<12} | {'FAILED':<12} | {'FAILED':<12} | {'FAILED':<12} | {'N/A':<26} | {'N/A':<22}"
                        )
                    else:
                        min_time = min(durations_minus_1)
                        max_time = max(durations_minus_1)
                        mean_time = statistics.mean(durations_minus_1)
                        median_time = statistics.median(durations_minus_1)
                        throughputs = [
                            ((size_bytes - 1) / (1024 * 1024)) / d
                            for d in durations_minus_1
                        ]
                        avg_throughput = ((size_bytes - 1) / (1024 * 1024)) / mean_time
                        std_dev = (
                            statistics.stdev(throughputs)
                            if len(throughputs) >= 2
                            else 0.0
                        )
                        throughput_str = (
                            f"{avg_throughput:.2f} \u00b1 {std_dev:.2f} MiB/s"
                        )

                        percent_diff_str = ""
                        if enable_chk:
                            enabled_throughput_minus_1 = avg_throughput
                            if (
                                enabled_throughput_full is not None
                                and enabled_throughput_full > 0
                            ):
                                percent_increase = (
                                    (
                                        enabled_throughput_minus_1
                                        - enabled_throughput_full
                                    )
                                    / enabled_throughput_full
                                ) * 100
                                percent_diff_str = f"{percent_increase:+.2f}%"
                            else:
                                percent_diff_str = "N/A"
                        else:
                            if (
                                enabled_throughput_minus_1 is not None
                                and enabled_throughput_minus_1 > 0
                            ):
                                percent_increase = (
                                    (avg_throughput - enabled_throughput_minus_1)
                                    / enabled_throughput_minus_1
                                ) * 100
                                percent_diff_str = f"{percent_increase:+.2f}%"
                            else:
                                percent_diff_str = "N/A"

                        print(
                            f"{f'{size_str} (Full-1)':<15} | {chk_label:<10} | {size_bytes - 1:<12} | "
                            f"{format_time(min_time):<12} | {format_time(max_time):<12} | "
                            f"{format_time(mean_time):<12} | {format_time(median_time):<12} | "
                            f"{throughput_str:<26} | "
                            f"{percent_diff_str:<22}"
                        )

                print("-" * 161)
            finally:
                try:
                    logging.info(
                        f"Cleaning up object gs://{args.bucket}/{object_name}..."
                    )
                    await grpc_client.delete_object(args.bucket, object_name)
                    logging.info("Cleanup complete.")
                except Exception as e:
                    logging.warning(
                        f"Warning: failed to delete test object {object_name}: {e}"
                    )


def main():
    asyncio.run(run_benchmark())


if __name__ == "__main__":
    main()
