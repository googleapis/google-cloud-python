# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess
import json
import math
import sys

# Define weights for long-running packages to balance shard execution time.
# Default weight for any package not listed is 1.
PACKAGE_WEIGHTS = {
    "bigframes": 6,
    "google-ai-generativelanguage": 4
    "google-auth": 5,
    "google-cloud-compute": 12,
    "google-cloud-compute-v1beta": 12,
    "google-cloud-dialogflow": 6,
    "google-cloud-dialogflow-cx": 6,
    "google-cloud-discoveryengine": 8,
    "google-cloud-retail": 5,
    "google-shopping-merchant-accounts": 4,

}


def get_packages():
    subdirs = ['packages']
    packages = []
    for subdir in subdirs:
        if not os.path.exists(subdir):
            continue
        # Use the same sorting as the shell script
        pkg_dirs = [os.path.join(subdir, d) + '/' for d in os.listdir(subdir) if os.path.isdir(os.path.join(subdir, d))]
        packages.extend(sorted(pkg_dirs))
    return packages


def get_packages_to_test():
    build_type = os.environ.get('BUILD_TYPE', 'presubmit')
    target_branch = os.environ.get('TARGET_BRANCH', 'main')
    test_all_packages = os.environ.get('TEST_ALL_PACKAGES', 'false').lower() == 'true'

    all_packages = get_packages()

    if test_all_packages:
        return all_packages

    if build_type == 'presubmit':
        git_diff_arg = f"origin/{target_branch}..."
    elif build_type == 'continuous':
        git_diff_arg = "HEAD~.."
    else:
        return all_packages

    try:
        res = subprocess.check_output(['git', 'diff', '--name-only', git_diff_arg]).decode('utf-8')
        changed_files = res.splitlines()
    except subprocess.CalledProcessError:
        return all_packages

    to_test = []
    for pkg in all_packages:
        # Check if any changed file starts with the package path
        if any(f.startswith(pkg) for f in changed_files):
            to_test.append(pkg)

    return to_test


def group_packages(packages):
    if not packages:
        return []

    # Map packages to their weights
    package_weights = []
    total_weight = 0
    for pkg in packages:
        pkg_name = pkg.strip('/').split('/')[-1]
        weight = PACKAGE_WEIGHTS.get(pkg_name, 1)
        package_weights.append((pkg, weight))
        total_weight += weight

    # Determine number of shards based on total weight
    # 1. Base shard count on weight capacity of 10 per shard
    num_shards = math.ceil(total_weight / 10)

    # Ensure at least 1 shard if we have packages
    num_shards = max(1, num_shards)

    # 2. Top out at 16 shards
    num_shards = min(16, num_shards)

    # Initialize shards as empty lists of packages with their current total weight
    shard_buckets = [{"packages": [], "weight": 0} for _ in range(num_shards)]

    # Sort packages descending by weight (LPT heuristic)
    # If weights are equal, sort alphabetically for stability
    sorted_packages = sorted(package_weights, key=lambda x: (-x[1], x[0]))

    # Distribute greedily to the bucket with the minimum current weight
    for pkg, weight in sorted_packages:
        min_bucket = min(shard_buckets, key=lambda b: b["weight"])
        min_bucket["packages"].append(pkg)
        min_bucket["weight"] += weight

    # Construct the final shards output list
    shards = []
    index = 1
    for bucket in shard_buckets:
        shard_packages = bucket["packages"]
        if not shard_packages:
            continue
        name = f"Shard {index}"
        num_in_shard = len(shard_packages)

        # Sort packages alphabetically for a cleaner description
        sorted_shard_pkgs = sorted(shard_packages)
        if len(sorted_shard_pkgs) == 1:
            desc = sorted_shard_pkgs[0].strip('/').split('/')[-1]
        else:
            desc = f"{sorted_shard_pkgs[0].strip('/').split('/')[-1]}...{sorted_shard_pkgs[-1].strip('/').split('/')[-1]} ({num_in_shard} packages)"

        shards.append({
            "name": name,
            "index": index,
            "description": desc,
            "packages": " ".join(shard_packages),
            "is_sharded": True
        })
        index += 1

    # Set is_sharded dynamically based on the total number of shards
    total_shards = len(shards)
    for shard in shards:
        shard["is_sharded"] = total_shards > 1

    return shards


if __name__ == "__main__":
    packages = get_packages_to_test()
    shards = group_packages(packages)
    print(json.dumps(shards))
