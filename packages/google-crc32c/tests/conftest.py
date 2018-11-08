# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""py.test shared testing configuration.

This

* Monkey-patches ``mock`` as ``unittest.mock`` for Python 2.7.
"""

import sys
import unittest

import six

if six.PY2:
    import mock

    unittest.mock = mock
    sys.modules["unittest.mock"] = unittest.mock
