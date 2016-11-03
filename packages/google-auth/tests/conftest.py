# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

import mock
import pytest


@pytest.fixture
def mock_non_existent_module(monkeypatch):
    """Mocks a non-existing module in sys.modules.

    Additionally mocks any non-existing modules specified in the dotted path.
    """
    def _mock_non_existent_module(path):
        parts = path.split('.')
        partial = []
        for part in parts:
            partial.append(part)
            current_module = '.'.join(partial)
            if current_module not in sys.modules:
                monkeypatch.setitem(
                    sys.modules, current_module, mock.MagicMock())

    return _mock_non_existent_module
