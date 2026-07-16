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

# Packages that take significantly longer to run tests.
# These will always be assigned to their own dedicated runner.
ISOLATED_PACKAGES = [
    "google-cloud-compute",
    "google-cloud-compute-v1beta",
    "google-cloud-dialogflow",
    "google-cloud-dialogflow-cx",
    "google-cloud-retail",
]

def get_batches():
    """Splits packages into dedicated isolated batches and evenly chunked standard batches."""
    raw_paths = sorted(glob.glob("packages/*"))
    package_paths = [p for p in raw_paths if os.path.isdir(p)]
    
    batches = []
    standard_packages = []
    
    for path in package_paths:
        pkg_name = os.path.basename(path)
        
        if pkg_name in ISOLATED_PACKAGES:
            # Put heavy packages into their own standalone batches immediately
            batches.append([path])
        else:
            standard_packages.append(path)
            
    # Chunk the remaining standard packages by BATCH_SIZE
    num_standard_packages = len(standard_packages)
    num_standard_batches = math.ceil(num_standard_packages / BATCH_SIZE)
    
    if num_standard_batches == 0 and not batches:
        num_standard_batches = 1
        
    for i in range(num_standard_batches):
        start_idx = i * BATCH_SIZE
        chunk = standard_packages[start_idx : start_idx + BATCH_SIZE]
        if chunk:
            batches.append(chunk)
            
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
