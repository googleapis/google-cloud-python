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

    # Check if ci/ changed
    try:
        subprocess.check_call(['git', 'diff', '--quiet', git_diff_arg, 'ci'])
        ci_changed = False
    except subprocess.CalledProcessError:
        ci_changed = True
    
    if ci_changed:
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

def group_packages(packages, max_packages_per_shard=50, max_total_shards=10):
    if not packages:
        return []
    
    num_packages = len(packages)
    
    # Calculate number of shards based on packages per shard
    num_shards = math.ceil(num_packages / max_packages_per_shard)
    
    # Cap the total number of shards
    num_shards = min(num_shards, max_total_shards)
    
    # Recalculate shard size to be as even as possible given the capped shards
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
        
        shards.append({
            "name": name,
            "index": index,
            "packages": " ".join(shard_packages)
        })
    return shards

if __name__ == "__main__":
    packages = get_packages_to_test()
    # Shard into groups of ~50 libraries, up to 10 parallel jobs
    shards = group_packages(packages, max_packages_per_shard=50, max_total_shards=10)
    print(json.dumps(shards))
