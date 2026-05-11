import os
import json
import argparse
from typing import List, Dict

# ---------------------------------------------------------
# THE VIP LIST: These will get their own dedicated isolated VMs
# ---------------------------------------------------------
MAMMOTH_OVERRIDES = {
    "google-cloud-spanner": 9999,
    "google-cloud-bigquery": 9999,
    "google-cloud-storage": 9999,
    "google-cloud-aiplatform": 9999,
    "pandas-gbq": 9999,
    "google-cloud-compute": 9999,
    "google-cloud-compute-v1": 9999,
    "google-cloud-compute-v1beta": 9999,
    "google-cloud-discoveryengine": 9999
}

def calculate_package_weight(pkg_path: str) -> int:
    pkg_name = os.path.basename(os.path.normpath(pkg_path))
    if pkg_name in MAMMOTH_OVERRIDES:
        return MAMMOTH_OVERRIDES[pkg_name]

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
    if os.path.isdir(test_dir):
        for root, _, files in os.walk(test_dir):
            base_weight += sum(1 for f in files if f.endswith(".py"))
            
    return base_weight

def create_balanced_buckets(packages: List[str], max_buckets: int) -> List[Dict]:
    valid_pkgs = [p for p in packages if os.path.isfile(os.path.join(p, "noxfile.py"))]
    if not valid_pkgs:
        return []
        
    pkg_weights = [(pkg, calculate_package_weight(pkg)) for pkg in valid_pkgs]
    pkg_weights.sort(key=lambda x: x[1], reverse=True)
    
    num_buckets = min(len(valid_pkgs), max_buckets)
    buckets = [{"id": i + 1, "packages": [], "total_weight": 0} for i in range(num_buckets)]
    
    for pkg, weight in pkg_weights:
        lightest = min(buckets, key=lambda b: b["total_weight"])
        lightest["packages"].append(pkg)
        lightest["total_weight"] += weight
        
    # Build the final output payload
    final_output = []
    for b in buckets:
        if not b["packages"]:
            continue
            
        # Clean UI labels for isolated VIPs
        first_pkg_name = os.path.basename(os.path.normpath(b["packages"][0]))
        if first_pkg_name in MAMMOTH_OVERRIDES:
            ui_label = first_pkg_name.replace("google-cloud-", "")
        else:
            ui_label = f"Bucket {b['id']}"
            
        final_output.append({
            "id": ui_label, 
            "packages": " ".join(b["packages"])
        })
        
    return final_output

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-multiplier", type=int, required=True)
    parser.add_argument("--max-vms", type=int, default=40)
    args = parser.parse_args()

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
