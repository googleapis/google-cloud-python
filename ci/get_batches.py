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

def get_batches():
    """Distributes packages into batches using a greedy load-balancing algorithm."""
    raw_paths = sorted(glob.glob("packages/*"))
    package_paths = [p for p in raw_paths if os.path.isdir(p)]
    
    packages_with_weights = []
    total_weight = 0
    for path in package_paths:
        pkg_name = os.path.basename(path)
        weight = PACKAGE_WEIGHTS.get(pkg_name, 1)
        packages_with_weights.append((path, weight))
        total_weight += weight
        
    num_batches = math.ceil(total_weight / BATCH_SIZE)
    if num_batches == 0:
        num_batches = 1
        
    # Sort packages by weight descending (Longest Processing Time first)
    packages_with_weights.sort(key=lambda x: x[1], reverse=True)
    
    batches = [[] for _ in range(num_batches)]
    batch_weights = [0] * num_batches
    
    for path, weight in packages_with_weights:
        # Greedily assign the package to the currently least-loaded batch
        min_idx = batch_weights.index(min(batch_weights))
        batches[min_idx].append(path)
        batch_weights[min_idx] += weight
        
    return batches

def get_batch_indices():
    """Returns a JSON string of the array of batch indices for GitHub Actions matrix."""
    batches = get_batches()
    return json.dumps(list(range(len(batches))))

def get_batch_slice(batch_index):
    """Returns a space-separated string of unique package paths for a specific batch index."""
    batches = get_batches()
    if batch_index < 0 or batch_index >= len(batches):
        return ""
    return " ".join(batches[batch_index])

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--count":
        print(get_batch_indices())
    elif len(sys.argv) > 2 and sys.argv[1] == "--slice":
        print(get_batch_slice(int(sys.argv[2])))
