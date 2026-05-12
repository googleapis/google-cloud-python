import os
import json
import argparse

# Complex, handwritten libraries with long-running test suites.
# The load balancer isolates these onto dedicated VMs to prevent bottlenecks.
HEAVY_LIFTERS = {
    "google-cloud-spanner", 
    "google-cloud-compute",
    "google-cloud-compute-v1beta", 
    "google-cloud-discoveryengine"
}

def get_valid_packages(directories):
    """Filters a list of directories, returning only those containing a noxfile.py."""
    return [p for p in directories if os.path.isfile(os.path.join(p, "noxfile.py"))]

def distribute_packages(packages, max_buckets):
    """Distributes packages into load-balanced buckets, isolating heavy lifters."""
    if not packages:
        return []

    # Heavy lifters jump to the front of the line
    packages.sort(key=lambda p: os.path.basename(p) not in HEAVY_LIFTERS)
    
    # Create the requested number of buckets (or fewer, if we have fewer packages than buckets)
    actual_buckets = min(len(packages), max_buckets)
    buckets = [{"weight": 0, "pkgs": []} for _ in range(actual_buckets)]

    for pkg in packages:
        # Find the bucket with the lowest weight, add the package, and update its weight
        lightest = min(buckets, key=lambda b: b["weight"])
        lightest["pkgs"].append(pkg)
        lightest["weight"] += 9999 if os.path.basename(pkg) in HEAVY_LIFTERS else 1

    return [b["pkgs"] for b in buckets]

def build_github_actions_jobs(buckets):
    """Formats the buckets into the specific JSON schema required by GitHub Actions."""
    jobs = []
    for bucket in buckets:
        base_name = os.path.basename(bucket[0]).replace("google-cloud-", "")
        job_label = f"{base_name} + {len(bucket) - 1}" if len(bucket) > 1 else base_name
        jobs.append({"id": job_label, "packages": " ".join(bucket)})
    return jobs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-multiplier", type=int, required=True)
    parser.add_argument("--max-vms", type=int, default=20)
    args = parser.parse_args()

    changed_dirs = os.environ.get("CHANGED_DIRS", "").split()
    packages = get_valid_packages(changed_dirs)
    
    if not packages:
        return

    # Protect against GitHub's 256-job hard limit
    max_buckets = min(250 // args.matrix_multiplier, args.max_vms)
    buckets = distribute_packages(packages, max_buckets)
    
    jobs_json = json.dumps(build_github_actions_jobs(buckets))

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"buckets={jobs_json}\n")
    else:
        print(jobs_json)

if __name__ == "__main__":
    main()
