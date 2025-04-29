# Copyright 2024 Google LLC
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

import argparse
import datetime
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
from typing import Dict, List, Tuple, Union

import numpy as np
import pandas as pd
import pandas_gbq

LOGGING_NAME_ENV_VAR = "BIGFRAMES_PERFORMANCE_LOG_NAME"
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()


def run_benchmark_subprocess(args, log_env_name_var, file_path=None, region=None):
    """
    Runs a benchmark subprocess with configured environment variables. Adjusts PYTHONPATH,
    sets region-specific BigQuery location, and logs environment variables.

    This function terminates the benchmark session if the subprocess exits with an error,
    due to `check=True` in subprocess.run, which raises CalledProcessError on non-zero
    exit status.
    """
    env = os.environ.copy()
    current_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        os.path.join(os.getcwd(), "tests") + os.pathsep + current_pythonpath
    )

    if region:
        env["BIGQUERY_LOCATION"] = region
    env[LOGGING_NAME_ENV_VAR] = log_env_name_var
    try:
        if file_path:  # Notebooks
            duration_pattern = re.compile(r"(\d+\.\d+)s call")
            process = subprocess.Popen(args, env=env, stdout=subprocess.PIPE, text=True)
            assert process.stdout is not None
            for line in process.stdout:
                print(line, end="")
                match = duration_pattern.search(line)
                if match:
                    duration = match.group(1)
                    with open(f"{file_path}.local_exec_time_seconds", "w") as f:
                        f.write(f"{duration}\n")
            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, args)
        else:  # Benchmarks
            file_path = log_env_name_var
            subprocess.run(args, env=env, check=True)
    except Exception:
        directory = pathlib.Path(file_path).parent
        for file in directory.glob(f"{pathlib.Path(file_path).name}.*"):
            if file.suffix != ".backup":
                print(f"Benchmark failed, deleting: {file}")
                file.unlink()
        error_file = directory / f"{pathlib.Path(file_path).name}.error"
        error_file.touch()


def collect_benchmark_result(
    benchmark_path: str, iterations: int
) -> Tuple[pd.DataFrame, Union[str, None]]:
    """Generate a DataFrame report on HTTP queries, bytes processed, slot time and execution time from log files."""
    path = pathlib.Path(benchmark_path)
    try:
        results_dict: Dict[str, List[Union[int, float, None]]] = {}
        bytes_files = sorted(path.rglob("*.bytesprocessed"))
        millis_files = sorted(path.rglob("*.slotmillis"))
        bq_seconds_files = sorted(path.rglob("*.bq_exec_time_seconds"))
        local_seconds_files = sorted(path.rglob("*.local_exec_time_seconds"))
        query_char_count_files = sorted(path.rglob("*.query_char_count"))

        error_files = sorted(path.rglob("*.error"))

        if not (
            len(millis_files)
            == len(bq_seconds_files)
            <= len(bytes_files)
            == len(query_char_count_files)
            == len(local_seconds_files)
        ):
            raise ValueError(
                "Mismatch in the number of report files for bytes, millis, seconds and query char count."
            )

        has_full_metrics = len(bq_seconds_files) == len(local_seconds_files)

        for idx in range(len(local_seconds_files)):
            query_char_count_file = query_char_count_files[idx]
            local_seconds_file = local_seconds_files[idx]
            bytes_file = bytes_files[idx]
            filename = query_char_count_file.relative_to(path).with_suffix("")
            if filename != local_seconds_file.relative_to(path).with_suffix(
                ""
            ) or filename != bytes_file.relative_to(path).with_suffix(""):
                raise ValueError(
                    "File name mismatch among query_char_count, bytes and seconds reports."
                )

            with open(query_char_count_file, "r") as file:
                lines = file.read().splitlines()
                query_char_count = sum(int(line) for line in lines) / iterations
                query_count = len(lines) / iterations

            with open(local_seconds_file, "r") as file:
                lines = file.read().splitlines()
                local_seconds = sum(float(line) for line in lines) / iterations

            with open(bytes_file, "r") as file:
                lines = file.read().splitlines()
                total_bytes = sum(int(line) for line in lines) / iterations

            if not has_full_metrics:
                total_slot_millis = None
                bq_seconds = None
            else:
                millis_file = millis_files[idx]
                bq_seconds_file = bq_seconds_files[idx]
                if filename != millis_file.relative_to(path).with_suffix(
                    ""
                ) or filename != bq_seconds_file.relative_to(path).with_suffix(""):
                    raise ValueError(
                        "File name mismatch among query_char_count, bytes, millis, and seconds reports."
                    )

                with open(millis_file, "r") as file:
                    lines = file.read().splitlines()
                    total_slot_millis = sum(int(line) for line in lines) / iterations

                with open(bq_seconds_file, "r") as file:
                    lines = file.read().splitlines()
                    bq_seconds = sum(float(line) for line in lines) / iterations

            results_dict[str(filename)] = [
                query_count,
                total_bytes,
                total_slot_millis,
                local_seconds,
                bq_seconds,
                query_char_count,
            ]
    finally:
        for files_to_remove in (
            path.rglob("*.bytesprocessed"),
            path.rglob("*.slotmillis"),
            path.rglob("*.local_exec_time_seconds"),
            path.rglob("*.bq_exec_time_seconds"),
            path.rglob("*.query_char_count"),
            path.rglob("*.error"),
        ):
            for log_file in files_to_remove:
                log_file.unlink()

    columns = [
        "Query_Count",
        "Bytes_Processed",
        "Slot_Millis",
        "Local_Execution_Time_Sec",
        "BigQuery_Execution_Time_Sec",
        "Query_Char_Count",
    ]

    benchmark_metrics = pd.DataFrame.from_dict(
        results_dict,
        orient="index",
        columns=columns,
    )

    report_title = (
        "---BIGQUERY USAGE REPORT---"
        if iterations == 1
        else f"---BIGQUERY USAGE REPORT (Averages over {iterations} Iterations)---"
    )
    print(report_title)
    for index, row in benchmark_metrics.iterrows():
        formatted_local_exec_time = (
            f"{round(row['Local_Execution_Time_Sec'], 1)} seconds"
            if not pd.isna(row["Local_Execution_Time_Sec"])
            else "N/A"
        )
        print(
            f"{index} - query count: {row['Query_Count']},"
            + f" query char count: {row['Query_Char_Count']},"
            + f" bytes processed sum: {row['Bytes_Processed']},"
            + (f" slot millis sum: {row['Slot_Millis']}," if has_full_metrics else "")
            + f" local execution time: {formatted_local_exec_time} seconds"
            + (
                f", bigquery execution time: {round(row['BigQuery_Execution_Time_Sec'], 1)} seconds"
                if has_full_metrics
                else ""
            )
        )

    geometric_mean_queries = geometric_mean_excluding_zeros(
        benchmark_metrics["Query_Count"]
    )
    geometric_mean_query_char_count = geometric_mean_excluding_zeros(
        benchmark_metrics["Query_Char_Count"]
    )
    geometric_mean_bytes = geometric_mean_excluding_zeros(
        benchmark_metrics["Bytes_Processed"]
    )
    geometric_mean_slot_millis = geometric_mean_excluding_zeros(
        benchmark_metrics["Slot_Millis"]
    )
    geometric_mean_local_seconds = geometric_mean_excluding_zeros(
        benchmark_metrics["Local_Execution_Time_Sec"]
    )
    geometric_mean_bq_seconds = geometric_mean_excluding_zeros(
        benchmark_metrics["BigQuery_Execution_Time_Sec"]
    )

    print(
        f"---Geometric mean of queries: {geometric_mean_queries},"
        + f" Geometric mean of queries char counts: {geometric_mean_query_char_count},"
        + f" Geometric mean of bytes processed: {geometric_mean_bytes},"
        + (
            f" Geometric mean of slot millis: {geometric_mean_slot_millis},"
            if has_full_metrics
            else ""
        )
        + f" Geometric mean of local execution time: {geometric_mean_local_seconds} seconds"
        + (
            f", Geometric mean of BigQuery execution time: {geometric_mean_bq_seconds} seconds---"
            if has_full_metrics
            else ""
        )
    )

    error_message = (
        "\n"
        + "\n".join(
            [
                f"Failed: {error_file.relative_to(path).with_suffix('')}"
                for error_file in error_files
            ]
        )
        if error_files
        else None
    )
    return (
        benchmark_metrics.reset_index().rename(columns={"index": "Benchmark_Name"}),
        error_message,
    )


def geometric_mean_excluding_zeros(data):
    """
    Calculate the geometric mean of a dataset, excluding any zero values.
    Returns NaN if the dataset is empty, contains only NaN values, or if
    all non-NaN values are zeros.

    The result is rounded to one decimal place.
    """
    data = data.dropna()
    data = data[data != 0]
    if len(data) == 0:
        return np.nan
    log_data = np.log(data)
    return round(np.exp(log_data.mean()), 1)


def get_repository_status():
    current_directory = os.getcwd()
    subprocess.run(
        ["git", "config", "--global", "--add", "safe.directory", current_directory],
        check=True,
    )

    git_hash = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"], text=True
    ).strip()
    bigframes_version = subprocess.check_output(
        ["python", "-c", "import bigframes; print(bigframes.__version__)"], text=True
    ).strip()
    release_version = (
        f"{bigframes_version}dev{datetime.datetime.now().strftime('%Y%m%d')}+{git_hash}"
    )

    return {
        "benchmark_start_time": datetime.datetime.now().isoformat(),
        "git_hash": git_hash,
        "bigframes_version": bigframes_version,
        "release_version": release_version,
        "python_version": sys.version,
    }


def find_config(start_path):
    """
    Searches for a 'config.jsonl' file starting from the given path and moving up to parent
    directories.

    This function ascends from the initial directory specified by `start_path` up to 3
    levels or until it reaches a directory named 'benchmark'. The search moves upwards
    because if there are multiple 'config.jsonl' files in the path hierarchy, the closest
    configuration to the starting directory (the lowest level) is expected to take effect.
    It checks each directory for the presence of 'config.jsonl'. If found, it returns the
    path to the configuration file. If not found within the limit or upon reaching
    the 'benchmark' directory, it returns None.
    """
    target_file = "config.jsonl"
    current_path = pathlib.Path(start_path).resolve()
    if current_path.is_file():
        current_path = current_path.parent

    levels_checked = 0
    while current_path.name != "benchmark" and levels_checked < 3:
        config_path = current_path / target_file
        if config_path.exists():
            return config_path
        if current_path.parent == current_path:
            break
        current_path = current_path.parent
        levels_checked += 1

    return None


def publish_to_bigquery(dataframe, notebook, project_name="bigframes-metrics"):
    bigquery_table = (
        f"{project_name}.benchmark_report.notebook_benchmark"
        if notebook
        else f"{project_name}.benchmark_report.benchmark"
    )

    repo_status = get_repository_status()
    for idx, col in enumerate(repo_status.keys()):
        dataframe.insert(idx, col, repo_status[col])

    pandas_gbq.to_gbq(
        dataframe=dataframe,
        destination_table=bigquery_table,
        if_exists="append",
    )
    print(f"Results have been successfully uploaded to {bigquery_table}.")


def run_benchmark_from_config(benchmark: str, iterations: int):
    print(benchmark)
    config_path = find_config(benchmark)

    if config_path:
        benchmark_configs = []
        with open(config_path, "r") as f:
            for line in f:
                if line.strip():
                    config = json.loads(line)
                    python_args = [f"--{key}={value}" for key, value in config.items()]
                    suffix = (
                        config["benchmark_suffix"]
                        if "benchmark_suffix" in config
                        else "_".join(f"{key}_{value}" for key, value in config.items())
                    )
                    benchmark_configs.append((suffix, python_args))
    else:
        benchmark_configs = [(None, [])]

    for _ in range(iterations):
        for benchmark_config in benchmark_configs:
            args = ["python", str(benchmark)]
            args.extend(benchmark_config[1])
            log_env_name_var = str(benchmark)
            if benchmark_config[0] is not None:
                log_env_name_var += f"_{benchmark_config[0]}"
            run_benchmark_subprocess(args=args, log_env_name_var=log_env_name_var)


def run_notebook_benchmark(benchmark_file: str, region: str):
    export_file = f"{benchmark_file}_{region}" if region else benchmark_file
    log_env_name_var = os.path.basename(export_file)
    # TODO(shobs): For some reason --retries arg masks exceptions occurred in
    # notebook failures, and shows unhelpful INTERNALERROR. Investigate that
    # and enable retries if we can find a way to surface the real exception
    # bacause the notebook is running against real GCP and something may fail
    # due to transient issues.
    pytest_command = [
        "py.test",
        "--nbmake",
        "--nbmake-timeout=900",  # 15 minutes
        "--durations=0",
        "--color=yes",
    ]
    benchmark_args = (*pytest_command, benchmark_file)

    run_benchmark_subprocess(
        args=benchmark_args,
        log_env_name_var=log_env_name_var,
        file_path=export_file,
        region=region,
    )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run benchmarks for different scenarios."
    )
    parser.add_argument(
        "--notebook",
        action="store_true",
        help="Set this flag to run the benchmark as a notebook. If not set, it assumes a Python (.py) file.",
    )

    parser.add_argument(
        "--benchmark-path",
        type=str,
        default=None,
        help="Specify the file path to the benchmark script, either a Jupyter notebook or a Python script.",
    )

    parser.add_argument(
        "--region",
        type=str,
        default=None,
        help="Specify the region where the benchmark will be executed or where the data resides. This parameter is optional.",
    )

    parser.add_argument(
        "--publish-benchmarks",
        type=str,
        default=None,
        help="Set the benchmarks to be published to BigQuery.",
    )

    parser.add_argument(
        "--iterations",
        type=int,
        default=1,
        help="Number of iterations to run each benchmark.",
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default=None,
        help="Determines whether to output results to a CSV file. If no location is provided, a temporary location is automatically generated.",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.publish_benchmarks:
        benchmark_metrics, error_message = collect_benchmark_result(
            args.publish_benchmarks, args.iterations
        )
        # Output results to CSV without specifying a location
        if args.output_csv == "True":
            current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            temp_file = tempfile.NamedTemporaryFile(
                prefix=f"benchmark_{current_time}_", delete=False, suffix=".csv"
            )
            benchmark_metrics.to_csv(temp_file.name, index=False)
            print(
                f"Benchmark result is saved to a temporary location: {temp_file.name}"
            )
            temp_file.close()
        # Output results to CSV with specified a custom location
        elif args.output_csv != "False":
            benchmark_metrics.to_csv(args.output_csv, index=False)
            print(f"Benchmark result is saved to: {args.output_csv}")

        # Publish the benchmark metrics to BigQuery under the 'bigframes-metrics' project.
        # The 'BENCHMARK_AND_PUBLISH' environment variable should be set to 'true' only
        # in specific Kokoro sessions.
        if os.getenv("BENCHMARK_AND_PUBLISH", "false") == "true":
            publish_to_bigquery(benchmark_metrics, args.notebook)
        # If the 'GCLOUD_BENCH_PUBLISH_PROJECT' environment variable is set, publish the
        # benchmark metrics to a specified BigQuery table in the provided project. This is
        # intended for local testing where the default behavior is not to publish results.
        elif project := os.getenv("GCLOUD_BENCH_PUBLISH_PROJECT", ""):
            publish_to_bigquery(benchmark_metrics, args.notebook, project)

        if error_message:
            raise Exception(error_message)
    elif args.notebook:
        run_notebook_benchmark(args.benchmark_path, args.region)
    else:
        run_benchmark_from_config(args.benchmark_path, args.iterations)


if __name__ == "__main__":
    main()
