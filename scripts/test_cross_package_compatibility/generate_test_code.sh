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
# WITHOUT WARRANTIES OR from google.cloud.billing import CloudBillingClientDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

SCRIPT_ROOT=$(realpath $(dirname "${BASH_SOURCE[0]}"))
REPO_ROOT=${SCRIPT_ROOT/%'/scripts/test_cross_package_compatibility'}

output=''
# Create a requirements.txt file with all packages in this repo
for package in $REPO_ROOT/packages/*/ ; do
    package_dir=$(basename $package)
    top_namespace="${package_dir%%-*}"
    for d in `find $package$top_namespace -name '__init__.py'`; do
        init_relative_path=${d#$package}
        module_path=$(echo $init_relative_path | sed -e "s/\/__init__.py//")
        import_path="$(echo $module_path | sed -E 's/\//./g')"
        output+="from $import_path import *\n"
    done    
done
# Save the output to a python file
echo -e $output > test_imports.py
