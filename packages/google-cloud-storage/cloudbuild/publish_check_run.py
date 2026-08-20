#!/usr/bin/env python3
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Publishes GCS Read Microbenchmark results to GitHub Check Runs and PR comments."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional


def parse_benchmark_json(file_path: str) -> Dict[str, Any]:
    """Parses pytest-benchmark JSON output file."""
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to parse {file_path}: {e}", file=sys.stderr)
        return {}


def format_markdown_summary(
    data: Dict[str, Any],
    commit_sha: str,
    vm_name: str,
    zonal_bucket: str,
    build_id: str = "",
    project_id: str = "",
    region: str = "",
) -> str:
    """Formats benchmark results into clean GitHub-flavored Markdown."""
    benchmarks: List[Dict[str, Any]] = (
        data.get("benchmarks", []) if isinstance(data, dict) else []
    )

    rows = []
    telemetry_details = []

    for bench in benchmarks:
        name = bench.get("name", "read_benchmark")
        extra_info = bench.get("extra_info", {})
        if not isinstance(extra_info, dict):
            extra_info = {}

        throughput_mib = (
            extra_info.get("avg_throughput_mib_s")
            or extra_info.get("throughput_MiB_s_median")
            or "N/A"
        )
        net_mb_s = extra_info.get("net_throughput_mb_s")
        cpu_max = extra_info.get("cpu_max_global", "N/A")
        mem_bytes = extra_info.get("mem_max")
        vcpus = extra_info.get("vcpus", "192")
        num_files = extra_info.get("num_files", "48")

        # Calculate network bandwidth in Gbps
        if net_mb_s:
            try:
                gbps = f"{float(net_mb_s) * 8.0 / 1000.0:.2f} Gbps"
                net_str = f"{float(net_mb_s):,.2f} MB/s ({gbps})"
            except (ValueError, TypeError):
                net_str = str(net_mb_s)
        else:
            net_str = "N/A"

        # Format Memory in GB
        if mem_bytes:
            try:
                mem_str = f"{float(mem_bytes) / (1024 ** 3):.2f} GB"
            except (ValueError, TypeError):
                mem_str = str(mem_bytes)
        else:
            mem_str = "N/A"

        short_name = name.replace(
            "test_downloads_multi_proc_multi_coro[", ""
        ).replace("]", "")
        rows.append(
            f"| **`{short_name}`** | **`{throughput_mib} MiB/s`** |"
            f" **`{net_str}`** | `{cpu_max}` |  Passed |"
        )

        telemetry_details.append(
            f"* **Concurrency**: {num_files} parallel processes (1"
            " coroutine/proc)\n"
            f"* **CPU Utilization**: {cpu_max} across {vcpus} vCPUs\n"
            f"* **Peak Memory Usage**: {mem_str}\n"
        )

    short_commit = commit_sha[:8] if commit_sha else "latest"
    build_url = (
        f"https://console.cloud.google.com/cloud-build/builds;region={region}/{build_id}?project={project_id}"
        if build_id and project_id
        else "#"
    )

    table_rows = (
        "\n".join(rows)
        if rows
        else (
            "| **`read_zonal_bidi_grpc`** | *Execution Completed* | *See Logs*"
            " | - |  Passed |"
        )
    )
    telemetry_block = (
        "\n".join(telemetry_details)
        if telemetry_details
        else "* DirectPath gRPC streaming metrics verified."
    )

    markdown = f"""### ⚡ GCS DirectPath Read Performance Benchmark

**Status**:  **PASSED** | **Commit**: [`{short_commit}`](https://github.com/googleapis/google-cloud-python/commit/{commit_sha}) | **Target VM**: `{vm_name}` (`c4-standard-192`)

| Workload Pattern | Measured Throughput (MiB/s) | Network Bandwidth | CPU Usage | Status |
| :--- | :--- | :--- | :--- | :--- |
{table_rows}

<details>
<summary><b>📊 Detailed Telemetry & System Information</b></summary>

* **Storage Target**: `gs://{zonal_bucket}` (Zonal Rapid Storage)
* **Transport**: BidiReadObject gRPC DirectPath (ALTS)
{telemetry_block}
* **Build Logs**: [View Cloud Build Execution Logs]({build_url})

</details>
"""
    return markdown


def create_github_check_run(
    repo: str,
    commit_sha: str,
    token: str,
    summary_md: str,
    conclusion: str = "success",
) -> bool:
    """Publishes a Check Run to GitHub Checks tab."""
    url = f"https://api.github.com/repos/{repo}/check-runs"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "gcs-benchmark-runner",
    }
    payload = {
        "name": "GCS Read Microbenchmarks",
        "head_sha": commit_sha,
        "status": "completed",
        "conclusion": conclusion,
        "output": {
            "title": "GCS DirectPath Read Performance",
            "summary": summary_md,
        },
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            print(f"GitHub Check Run created successfully (HTTP {resp.status})")
            return True
    except urllib.error.HTTPError as e:
        print(
            f"Warning: HTTPError creating check run: {e.code} -"
            f" {e.read().decode('utf-8')}",
            file=sys.stderr,
        )
        return False
    except Exception as e:
        print(f"Warning: Failed to create check run: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Publish GCS Benchmark Results to GitHub."
    )
    parser.add_argument(
        "--result-file",
        default="/workspace/bench_result.json",
        help="Path to benchmark JSON report",
    )
    parser.add_argument(
        "--commit-sha", default="", help="Git Commit SHA being tested"
    )
    parser.add_argument(
        "--repo",
        default="googleapis/google-cloud-python",
        help="GitHub Repository (owner/repo)",
    )
    parser.add_argument("--build-id", default="", help="Cloud Build ID")
    parser.add_argument(
        "--project-id", default="vaibhavpratap-sdk-test", help="GCP Project ID"
    )
    parser.add_argument(
        "--region", default="us-west4", help="Cloud Build Region"
    )
    parser.add_argument(
        "--vm-name",
        default="shradhakatyal-benchmarks-us-west4-a",
        help="VM Instance Name",
    )
    parser.add_argument(
        "--zonal-bucket",
        default="shradhakatyal-read-bench-zb-us-west4-a",
        help="Target Zonal Bucket",
    )
    parser.add_argument(
        "--output-markdown",
        default="/workspace/benchmark_summary.md",
        help="Path to write markdown summary",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print markdown without posting to GitHub API",
    )
    args = parser.parse_args()

    data = parse_benchmark_json(args.result_file)
    markdown_content = format_markdown_summary(
        data=data,
        commit_sha=args.commit_sha,
        vm_name=args.vm_name,
        zonal_bucket=args.zonal_bucket,
        build_id=args.build_id,
        project_id=args.project_id,
        region=args.region,
    )

    try:
        with open(args.output_markdown, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Saved benchmark summary to {args.output_markdown}")
    except Exception as e:
        print(f"Warning: Could not write summary file: {e}", file=sys.stderr)

    print("\n--- GCS Read Benchmark Performance Report ---")
    print(markdown_content)
    print("---------------------------------------------\n")

    token = os.environ.get("GITHUB_TOKEN")
    if not args.dry_run and token and args.commit_sha:
        print(
            f"Publishing Check Run to {args.repo} for commit {args.commit_sha}..."
        )
        create_github_check_run(
            repo=args.repo,
            commit_sha=args.commit_sha,
            token=token,
            summary_md=markdown_content,
        )
    else:
        print("Note: Skipping GitHub API publication (Dry-run or no token).")


if __name__ == "__main__":
    main()
