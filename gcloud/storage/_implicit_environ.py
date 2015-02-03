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

"""Module to provide implicit behavior based on enviroment.

Acts as a mutable namespace to allow the datastore package to
infer the current dataset ID and connection from the enviroment.
"""


PROJECT = None
"""Module global to allow persistent implied project from enviroment."""

BUCKET = None
"""Module global to allow persistent implied bucket from enviroment."""

CONNECTION = None
"""Module global to allow persistent implied connection from enviroment."""
