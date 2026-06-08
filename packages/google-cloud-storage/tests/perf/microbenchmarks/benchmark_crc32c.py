import argparse
import os
import statistics
import sys
import time

try:
    import google_crc32c
except ImportError:
    print("Error: google_crc32c package is not installed in the python environment.", file=sys.stderr)
    sys.exit(1)


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


def main():
    parser = argparse.ArgumentParser(description="Benchmark google_crc32c.value execution time.")
    parser.add_argument(
        "--sizes",
        type=str,
        default="1KiB,100KiB,2MiB",
        help="Comma-separated list of sizes (e.g. '1KiB,100KiB,2MiB')"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=100,
        help="Number of iterations for benchmark (default: 100)"
    )
    args = parser.parse_args()

    # Ensure google_crc32c uses accelerated C code
    impl = getattr(google_crc32c, "implementation", None)
    print(f"google_crc32c implementation: {impl}")
    if impl != "c":
        print(f"Error: google_crc32c is not using the accelerated C code (got '{impl}').", file=sys.stderr)
        sys.exit(1)

    sizes_to_test = []
    for s in args.sizes.split(","):
        try:
            sizes_to_test.append((s.strip(), parse_size(s)))
        except ValueError as e:
            print(f"Error parsing size '{s}': {e}", file=sys.stderr)
            sys.exit(1)

    print(f"Benchmarking google_crc32c.value(data) with {args.iterations} iterations:")
    print("-" * 80)
    print(f"{'Size (String)':<15} | {'Size (Bytes)':<12} | {'Min':<10} | {'Max':<10} | {'Mean':<10} | {'Median':<10}")
    print("-" * 80)

    for size_str, size_bytes in sizes_to_test:
        data = os.urandom(size_bytes)

        durations = []
        for _ in range(args.iterations):
            start = time.perf_counter()
            _ = google_crc32c.value(data)
            end = time.perf_counter()
            durations.append(end - start)

        min_time = min(durations)
        max_time = max(durations)
        mean_time = statistics.mean(durations)
        median_time = statistics.median(durations)

        print(
            f"{size_str:<15} | {size_bytes:<12} | "
            f"{format_time(min_time):<10} | {format_time(max_time):<10} | "
            f"{format_time(mean_time):<10} | {format_time(median_time):<10}"
        )


if __name__ == "__main__":
    main()
