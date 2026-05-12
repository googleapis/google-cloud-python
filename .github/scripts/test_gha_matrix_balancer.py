import pytest
from unittest.mock import patch
from gha_matrix_balancer import (
    get_valid_packages,
    distribute_packages,
    build_github_actions_jobs,
    HEAVY_LIFTERS
)

@patch("os.path.isfile")
def test_get_valid_packages(mock_isfile):
    # Mock isfile to only return True for the exact valid path
    mock_isfile.side_effect = lambda path: path == "packages/valid-pkg/noxfile.py"

    dirs = ["packages/valid-pkg", "packages/invalid-pkg"]
    result = get_valid_packages(dirs)
    
    assert result == ["packages/valid-pkg"]

def test_distribute_packages_isolates_heavy_lifters():
    # Mix 1 heavy lifter with 5 normal packages
    heavy_lifter = list(HEAVY_LIFTERS)[0] # Grab one of the defined heavy lifters dynamically
    
    packages = [
        "packages/google-cloud-vision",
        "packages/google-cloud-storage",
        f"packages/{heavy_lifter}",
        "packages/google-cloud-logging",
        "packages/google-cloud-pubsub",
        "packages/google-cloud-kms",
    ]
    
    # Request 3 buckets
    buckets = distribute_packages(packages, max_buckets=3)
    
    assert len(buckets) == 3
    
    # Find the bucket containing the heavy lifter
    heavy_bucket = next(b for b in buckets if f"packages/{heavy_lifter}" in b)
    
    # Because it adds 9999 weight, it should be the ONLY package in its bucket
    assert len(heavy_bucket) == 1
    assert heavy_bucket[0] == f"packages/{heavy_lifter}"

def test_distribute_packages_max_bucket_limit():
    # 5 packages, but we only allow 2 buckets
    packages = [f"pkg-{i}" for i in range(5)]
    buckets = distribute_packages(packages, max_buckets=2)
    
    assert len(buckets) == 2
    # Packages should be distributed (3 in one, 2 in the other)
    assert len(buckets[0]) + len(buckets[1]) == 5

def test_distribute_packages_more_buckets_than_packages():
    # 2 packages, but we allow up to 10 buckets
    packages = ["pkg-1", "pkg-2"]
    buckets = distribute_packages(packages, max_buckets=10)
    
    # It should only create 2 buckets, not 10
    assert len(buckets) == 2

def test_build_github_actions_jobs():
    buckets = [
        ["packages/google-cloud-spanner"], # Single item
        ["packages/google-cloud-vision", "packages/google-cloud-storage", "packages/google-cloud-pubsub"] # Multiple items
    ]
    
    jobs = build_github_actions_jobs(buckets)
    
    assert len(jobs) == 2
    
    # Test single-item label stripping
    assert jobs[0]["id"] == "spanner"
    assert jobs[0]["packages"] == "packages/google-cloud-spanner"
    
    # Test multi-item label generation (+ N logic)
    assert jobs[1]["id"] == "vision + 2"
    assert jobs[1]["packages"] == "packages/google-cloud-vision packages/google-cloud-storage packages/google-cloud-pubsub"
