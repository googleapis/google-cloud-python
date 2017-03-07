# Copyright 2017 Google Inc.
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

"""Environment variables used by the package."""

APPENGINE_FLEXIBLE_ENV_VM = 'GAE_APPENGINE_HOSTNAME'
"""Environment variable set in App Engine when vm:true is set."""

APPENGINE_FLEXIBLE_ENV_FLEX = 'GAE_INSTANCE'
"""Environment variable set in App Engine when env:flex is set."""

CONTAINER_ENGINE_ENV = 'KUBERNETES_SERVICE'
"""Environment variable set in a Google Container Engine environment."""

GAE_SERVICE = 'GAE_SERVICE'
"""Environment variable in the App Engine Flex env that indicates version."""

GAE_VERSION = 'GAE_VERSION'
"""Environment variable in the App Engine Flex env that indicates version."""
