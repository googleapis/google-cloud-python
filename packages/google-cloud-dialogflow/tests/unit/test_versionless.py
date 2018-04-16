# Copyright 2017, Google LLC
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

import dialogflow
import dialogflow_v2


def test_versionless():
    """Establish that the versioned import maps to the versionless one."""

    for key in dir(dialogflow):
        if key.startswith('_'):
            continue
        assert getattr(dialogflow_v2, key) is getattr(dialogflow, key)
