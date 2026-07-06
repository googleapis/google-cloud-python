# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#!/usr/bin/env python3
import os
import glob
import math
import json
import sys

BATCH_SIZE = 10

# Large SDKs take significantly longer to run tests. Assigning higher weights 
# ensures these packages occupy more runner slots and load-balance effectively.
PACKAGE_WEIGHTS = {
    "google-cloud-compute": 5,
    "google-cloud-compute-v1beta": 5,
    "google-cloud-dialogflow": 5,
    "google-cloud-dialogflow-cx": 5,
    "google-cloud-retail": 5,
}

def get_weighted_package_list():
    """Audits the packages directory and expands the list based on weights."""
    raw_paths = sorted(glob.glob("packages/*"))
    package_paths = [p for p in raw_paths if os.path.isdir(p)]
    
    weighted_list = []
    for path in package_paths:
        pkg_name = os.path.basename(path)
        weight = PACKAGE_WEIGHTS.get(pkg_name, 1)
        
        for _ in range(weight):
            weighted_list.append(path)
            
    return weighted_list

def get_batch_indices():
    """Returns a JSON string of the array of batch indices for GitHub Actions matrix."""
    weighted_list = get_weighted_package_list()
    total_units = len(weighted_list)
    num_batches = math.ceil(total_units / BATCH_SIZE)

    if num_batches == 0:
        num_batches = 1

    return json.dumps(list(range(num_batches)))

def get_batch_slice(batch_index):
    """Returns a space-separated string of unique package paths for a specific batch index."""
    weighted_list = get_weighted_package_list()
    total_units = len(weighted_list)
    start_idx = batch_index * BATCH_SIZE
    
    if start_idx >= total_units:
        return ""
        
    slice_window = weighted_list[start_idx : start_idx + BATCH_SIZE]
    
    unique_packages = []
    for pkg in slice_window:
        if pkg not in unique_packages:
            unique_packages.append(pkg)
            
    return " ".join(unique_packages)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--count":
        print(get_batch_indices())
    elif len(sys.argv) > 2 and sys.argv[1] == "--slice":
        print(get_batch_slice(int(sys.argv[2])))
