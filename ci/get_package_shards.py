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

    # Dynamically determine target weight to balance across max 16 shards.
    # 1. Base shard count has a target weight capacity of 10 per shard.
    # 2. To avoid exceeding 16 shards, we scale the target weight dynamically
    #    based on the total workload.
    max_shards = 16
    target_weight = max(10, math.ceil(total_weight / max_shards))

    shards_list = []
    current_shard_packages = []
    current_shard_weight = 0

    # Pack packages alphabetically and contiguously.
    for pkg, weight in package_weights:
        # Check if adding this package would exceed the target weight
        if current_shard_packages and (current_shard_weight + weight > target_weight):
            shards_list.append(current_shard_packages)
            current_shard_packages = [pkg]
            current_shard_weight = weight
        else:
            current_shard_packages.append(pkg)
            current_shard_weight += weight

    if current_shard_packages:
        shards_list.append(current_shard_packages)

    # Construct the final shards output list
    shards = []
    for i, shard_packages in enumerate(shards_list):
        index = i + 1
        name = f"Shard {index}"
        num_in_shard = len(shard_packages)
        
        # Calculate contiguous range description
        if len(shard_packages) == 1:
            desc = shard_packages[0].strip('/').split('/')[-1]
        else:
            desc = f"{shard_packages[0].strip('/').split('/')[-1]}...{shard_packages[-1].strip('/').split('/')[-1]} ({num_in_shard} packages)"

        shards.append({
            "name": name,
            "index": index,
            "description": desc,
            "packages": " ".join(shard_packages),
            "is_sharded": True
        })

    # Set is_sharded dynamically based on the total number of shards
    total_shards = len(shards)
    for shard in shards:
        shard["is_sharded"] = total_shards > 1

    return shards


if __name__ == "__main__":
    packages = get_packages_to_test()
    shards = group_packages(packages)
    print(json.dumps(shards))
