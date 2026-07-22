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

"""Script to group changed packages into balanced shards for CI testing.

This script identifies which packages have changed compared to a target branch
(or since the last commit) and groups them into a fixed number of shards.
It uses package weights (configured via environment variables) to balance the
execution time across shards while maintaining alphabetical order and
contiguous grouping.
"""

import os
import subprocess
import json
import math
import sys

def get_package_weights():
    """Parses package weights from the PACKAGE_WEIGHTS environment variable.
    Package weights represent the relative size of the test, where the weight
    approximately represents the minutes the test takes to run. This is used
    for distributing work properly across shards.

    The environment variable is expected to be a multiline string where each line
    is in the format 'package_name: weight'. Lines starting with '#' are ignored.

    Returns:
        dict: A mapping of package names to their integer weights.
    """
    weights = {}
    env_weights = os.environ.get("PACKAGE_WEIGHTS", "")
    for line in env_weights.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            try:
                pkg, weight = line.split(":", 1)
                weights[pkg.strip()] = int(weight.strip())
            except ValueError:
                continue
    return weights


def get_packages():
    """Lists all package directories in the repository.

    Returns:
        list: A sorted list of relative paths to all directories under 'packages/'.
    """
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
    """Determines the list of packages that need to be tested.

    This is based on git diffs against the target branch (presubmit) or the
    previous commit (continuous). If TEST_ALL_PACKAGES is set to true,
    all packages are returned.

    Returns:
        list: A list of package directory paths to be included in the test matrix.
    """
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
        # If change detection fails, fall back to all packages
        return all_packages

    to_test = []
    for pkg in all_packages:
        # Check if any changed file starts with the package path
        if any(f.startswith(pkg) for f in changed_files):
            to_test.append(pkg)

    return to_test


def group_packages(packages):
    """Groups the provided packages into balanced shards.

    The grouping respects the MAX_SHARDS limit. It uses a target weight per shard
    to distribute the workload. If the contiguous packing exceeds the shard limit,
    all remaining packages are added to the final shard.

    Args:
        packages (list): The list of package directory paths to group.

    Returns:
        list: A list of dictionaries, each representing a shard with its name,
              index, description, and the space-separated list of packages.
    """
    if not packages:
        return []

    # Map packages to their weights
    package_weights_map = get_package_weights()
    package_weights = []
    total_weight = 0
    for pkg in packages:
        pkg_name = pkg.strip('/').split('/')[-1]
        weight = package_weights_map.get(pkg_name, 1)
        package_weights.append((pkg, weight))
        total_weight += weight

    # Dynamically determine target weight to balance across max shards.
    max_shards = int(os.environ.get("MAX_SHARDS", 16))
    target_weight = max(10, math.ceil(total_weight / max_shards))

    shards_list = []
    current_shard_packages = []
    current_shard_weight = 0

    # Pack packages alphabetically and contiguously.
    for pkg, weight in package_weights:
        # If adding this package would exceed target weight AND we haven't reached the 
        # shard limit, start a new shard. Otherwise, keep "stuffing" the current one.
        if current_shard_packages and (current_shard_weight + weight > target_weight) and len(shards_list) < max_shards - 1:
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
