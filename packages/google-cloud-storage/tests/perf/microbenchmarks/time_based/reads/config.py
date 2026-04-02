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
import itertools
import os
from typing import Dict, List

import yaml

try:
    from tests.perf.microbenchmarks.time_based.reads.parameters import (
        TimeBasedReadParameters,
    )
except ModuleNotFoundError:
    from reads.parameters import TimeBasedReadParameters


def _get_params() -> Dict[str, List[TimeBasedReadParameters]]:
    """Generates a dictionary of benchmark parameters for time based read operations."""
    params: Dict[str, List[TimeBasedReadParameters]] = {}
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    common_params = config["common"]
    bucket_types = common_params["bucket_types"]
    file_sizes_mib = common_params["file_sizes_mib"]
    chunk_sizes_kib = common_params["chunk_sizes_kib"]
    num_ranges = common_params["num_ranges"]
    rounds = common_params["rounds"]
    duration = common_params["duration"]
    warmup_duration = common_params["warmup_duration"]

    bucket_map = {
        "zonal": os.environ.get(
            "DEFAULT_RAPID_ZONAL_BUCKET",
            config["defaults"]["DEFAULT_RAPID_ZONAL_BUCKET"],
        ),
        "regional": os.environ.get(
            "DEFAULT_STANDARD_BUCKET", config["defaults"]["DEFAULT_STANDARD_BUCKET"]
        ),
    }

    for workload in config["workload"]:
        workload_name = workload["name"]
        params[workload_name] = []
        pattern = workload["pattern"]
        processes = workload["processes"]
        coros = workload["coros"]

        # Create a product of all parameter combinations
        product = itertools.product(
            bucket_types,
            file_sizes_mib,
            chunk_sizes_kib,
            num_ranges,
            processes,
            coros,
        )

        for (
            bucket_type,
            file_size_mib,
            chunk_size_kib,
            num_ranges_val,
            num_processes,
            num_coros,
        ) in product:
            file_size_bytes = file_size_mib * 1024 * 1024
            chunk_size_bytes = chunk_size_kib * 1024
            bucket_name = bucket_map[bucket_type]

            num_files = num_processes * num_coros

            # Create a descriptive name for the parameter set
            name = f"{pattern}_{bucket_type}_{num_processes}p_{file_size_mib}MiB_{chunk_size_kib}KiB_{num_ranges_val}ranges"

            params[workload_name].append(
                TimeBasedReadParameters(
                    name=name,
                    workload_name=workload_name,
                    pattern=pattern,
                    bucket_name=bucket_name,
                    bucket_type=bucket_type,
                    num_coros=num_coros,
                    num_processes=num_processes,
                    num_files=num_files,
                    rounds=rounds,
                    chunk_size_bytes=chunk_size_bytes,
                    file_size_bytes=file_size_bytes,
                    duration=duration,
                    warmup_duration=warmup_duration,
                    num_ranges=num_ranges_val,
                )
            )
    return params
