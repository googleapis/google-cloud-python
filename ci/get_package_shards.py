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

# Define set of long-running unit tests to run in isolated shard
ISOLATED_PACKAGES = {
    "google-cloud-compute",
    "google-cloud-compute-v1beta",
    "google-cloud-dialogflow",
    "google-cloud-dialogflow-cx",
    "google-cloud-retail",
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

    isolated_to_test = []
    normal_to_test = []

    for pkg in packages:
        pkg_name = pkg.strip('/').split('/')[-1]
        if pkg_name in ISOLATED_PACKAGES:
            isolated_to_test.append(pkg)
        else:
            normal_to_test.append(pkg)

    shards = []
    index = 1

    # Add isolated packages to their own shards
    for pkg in isolated_to_test:
        pkg_name = pkg.strip('/').split('/')[-1]
        clean_name = pkg_name.replace("google-cloud-", "")
        shards.append({
            "name": clean_name,
            "index": index,
            "description": pkg_name,
            "packages": pkg,
            "is_sharded": True
        })
        index += 1

    # Group the remaining packages
    if normal_to_test:
        num_packages = len(normal_to_test)
        
        # 1. Only shard if > 10 packages are being touched
        # 2. Only add a new shard if any shard would have > 10 packages.
        # To guarantee that no shard contains more than 10 packages (when distributed evenly),
        # we need S >= N / 10, which means S = ceil(N / 10).
        num_shards = math.ceil(num_packages / 10)
        
        # Ensure at least 1 shard if we have packages
        num_shards = max(1, num_shards)
        
        # 3. Top out at 16 shards
        num_shards = min(16, num_shards)
        
        # Distribute packages between them as evenly as possible
        shard_size = math.ceil(num_packages / num_shards)

        for i in range(num_shards):
            start = i * shard_size
            end = min((i + 1) * shard_size, num_packages)
            if start >= num_packages:
                break
            shard_packages = normal_to_test[start:end]
            name = f"Shard {index}"
            num_in_shard = len(shard_packages)
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
