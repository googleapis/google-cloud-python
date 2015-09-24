# Copyright 2015 Google Inc. All rights reserved.
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

"""Checking that protobuf generated modules import correctly."""

from __future__ import print_function

import glob
import os


def main():
    """Import all PB2 files."""
    print('>>> import gcloud.bigtable._generated')
    _ = __import__('gcloud.bigtable._generated')
    pb2_files = sorted(glob.glob('gcloud/bigtable/_generated/*pb2.py'))
    for filename in pb2_files:
        basename = os.path.basename(filename)
        module_name, _ = os.path.splitext(basename)

        print('>>> from gcloud.bigtable._generated import ' + module_name)
        _ = __import__('gcloud.bigtable._generated', fromlist=[module_name])


if __name__ == '__main__':
    main()
