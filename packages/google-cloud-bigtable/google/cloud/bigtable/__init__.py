# Copyright 2015 Google LLC
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

"""Google Cloud Bigtable API package."""


from typing import Optional
import pkg_resources

from google.cloud.bigtable.client import Client

__version__: Optional[str]
try:
    __version__ = pkg_resources.get_distribution("google-cloud-bigtable").version
except pkg_resources.DistributionNotFound:
    __version__ = None


__all__ = ["__version__", "Client"]
