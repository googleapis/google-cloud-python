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

"""Cloud ResourceManager API wrapper.

The main concepts with this API are:

- :class:`gcloud.resource_manager.project.Project` represents
  a Google Cloud project.
"""

from gcloud.resource_manager.client import Client
from gcloud.resource_manager.connection import SCOPE
from gcloud.resource_manager.project import Project
