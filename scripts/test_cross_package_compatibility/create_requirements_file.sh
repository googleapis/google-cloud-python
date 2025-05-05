# Copyright 2025 Google LLC
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
#

SCRIPT_ROOT=$(realpath $(dirname "${BASH_SOURCE[0]}"))
REPO_ROOT=${SCRIPT_ROOT/%'/scripts/test_cross_package_compatibility'}

output=''
# Create a requirements.txt file with all packages in this repo
for package in $REPO_ROOT/packages/*/ ; do
    distribution_name=$(basename $package)
    # Replace `-` with `_`
    distribution_name_wheel=$(echo ${distribution_name} | sed -E 's/\-/_/g')
    output+="${distribution_name} @ file://localhost${REPO_ROOT}/packages/${distribution_name}/dist/${distribution_name_wheel}-0.0.0-py3-none-any.whl\n"
done
output+="# Remove pin below once https://github.com/googleapis/google-cloud-python/issues/13874 is fixed\n"
output+="protobuf<6"

# Save the output to a requirements.txt
echo -e $output > requirements.txt
