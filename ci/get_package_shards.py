import os
import subprocess
import json
import math
import sys

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

    all_packages = get_packages()

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

    num_packages = len(packages)

    # 1. Only shard if > 10 packages are being touched
    # 2. Only add a new shard if any shard would have > 10 packages.
    # To guarantee that no shard contains more than 10 packages (when distributed evenly),
    # we need S >= N / 10, which means S = ceil(N / 10).
    num_shards = math.ceil(num_packages / 10)

    # Ensure at least 1 shard if we have packages
    num_shards = max(1, num_shards)

    # 3. Top out at 10 shards
    num_shards = min(10, num_shards)

    # Distribute packages between them as evenly as possible
    shard_size = math.ceil(num_packages / num_shards)

    shards = []
    for i in range(num_shards):
        start = i * shard_size
        end = min((i + 1) * shard_size, num_packages)
        if start >= num_packages:
            break
        shard_packages = packages[start:end]
        index = i + 1
        name = f"Shard {index}"
        num_in_shard = len(shard_packages)
        # Calculate a descriptive range for step visibility
        if len(shard_packages) == 1:
            desc = shard_packages[0].strip('/').split('/')[-1]
        else:
            desc = f"{shard_packages[0].strip('/').split('/')[-1]}...{shard_packages[-1].strip('/').split('/')[-1]} ({num_in_shard})"

        shards.append({
            "name": name,
            "index": index,
            "description": desc,
            "packages": " ".join(shard_packages),
            "is_sharded": num_shards > 1
        })
    return shards

if __name__ == "__main__":
    packages = get_packages_to_test()
    shards = group_packages(packages)
    print(json.dumps(shards))
