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

import pkg_resources


def test___version__():
    # NOTE: The ``__version__`` is hard-coded in ``__init__.py``.
    import google.cloud.ndb

    hardcoded_version = google.cloud.ndb.__version__
    installed_version = pkg_resources.get_distribution(
        "google-cloud-ndb"
    ).version
    assert hardcoded_version == installed_version
