# Copyright 2017 Google LLC
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

"""This module is used to configure gcp-devrel-py-tools run-pylint."""

import copy

from gcp_devrel.tools import pylint

# Library configuration

# library_additions = {}
library_replacements = copy.deepcopy(pylint.DEFAULT_LIBRARY_RC_REPLACEMENTS)
library_replacements['MASTER']['ignore'].append('_generated')

# Test configuration

# test_additions = copy.deepcopy(library_additions)
# test_replacements = copy.deepcopy(library_replacements)
