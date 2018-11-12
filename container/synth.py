# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""
import synthtool as s
from synthtool import gcp

gapic = gcp.GAPICGenerator()


#----------------------------------------------------------------------------
# Generate container client
#----------------------------------------------------------------------------
library = gapic.py_library(
    'container',
    'v1',
    config_path='/google/container/artman_container_v1.yaml',
    artman_output_name='container-v1')

s.move(library / 'google/cloud/container_v1')

# Issues exist where python files should define the source encoding
# https://github.com/googleapis/gapic-generator/issues/2097
s.replace(
    'google/**/proto/*_pb2.py',
    r"(^.*$\n)*",
    r"# -*- coding: utf-8 -*-\n\g<0>")
