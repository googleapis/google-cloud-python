import os
import json
import argparse
from typing import List, Dict, Tuple

def calculate_package_weight(pkg_path: str) -> int:
    """
    Dynamically profiles a package to determine its computational weight.
    GAPIC clients are lightweight. Handwritten clients are heavy (based on test count).
    """
    base_weight = 1
    
    meta_path = os.path.join(pkg_path, ".repo-metadata.json")
    if os.path.isfile(meta_path):
        try:
            with open(meta_path, 'r') as f:
                if json.load(f).get("library_type") == "GAPIC_AUTO":
                    return base_weight
        except Exception:
            pass 
            
    test_dir = os.path.join(pkg_path, "tests")
    test_file_count = 0
    if os.path.isdir(test_dir):
        for root, _, files in os.walk(test_dir):
            test_file_count += sum(1 for f in files if f.endswith(".py"))
            
    return base_weight + test_file_count

def create_balanced_buckets(packages: List[str], max_buckets: int) -> List[str]:
    """
    Distributes packages using the Longest Processing Time (LPT) algorithm.
    """
    valid_pkgs = [p for p in packages if os.path.isfile(os.path.join(p, "noxfile.py"))]
    if not valid_pkgs:
        return []
        
    pkg_weights: List[Tuple[str, int]] = []
    for pkg in valid_pkgs:
        pkg_weights.append((pkg, calculate_package_weight(pkg)))
        
    pkg_weights.sort(key=lambda x: x[1], reverse=True)
    
    # Do not spin up empty VMs if we have fewer packages than max_buckets
    num_buckets = min(len(valid_pkgs), max_buckets)
    buckets: List[Dict] = [{"packages": [], "total_weight": 0} for _ in range(num_buckets)]
    
    for pkg, weight in pkg_weights:
        lightest_bucket = min(buckets, key=lambda b: b["total_weight"])
        lightest_bucket["packages"].append(pkg)
        lightest_bucket["total_weight"] += weight
        
    return [" ".join(b["packages"]) for b in buckets]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-multiplier", type=int, required=True, 
                        help="Number of matrix permutations (e.g., 6 for Py versions)")
    parser.add_argument("--max-vms", type=int, default=40, 
                        help="Hard cap on VMs to protect the organization concurrency limit")
    args = parser.parse_args()

    # THE L8 MATH: Never exceed ~250 jobs per workflow run.
    safe_github_limit = 250 // args.matrix_multiplier
    max_allowed_buckets = min(safe_github_limit, args.max_vms)

    changed_dirs = os.environ.get("CHANGED_DIRS", "").split()
    buckets = create_balanced_buckets(changed_dirs, max_allowed_buckets)
    
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"buckets={json.dumps(buckets)}\n")
    else:
        print(json.dumps(buckets, indent=2))

if __name__ == "__main__":
    main()