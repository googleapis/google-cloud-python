# Copyright 2014 Google Inc. All rights reserved.
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

"""Shared datastore testing utilities."""

from gcloud._testing import _Monkey
from gcloud.datastore import _implicit_environ
from gcloud.datastore._implicit_environ import _DefaultsContainer


def _monkey_defaults(*args, **kwargs):
    mock_defaults = _DefaultsContainer(*args, **kwargs)
    return _Monkey(_implicit_environ, _DEFAULTS=mock_defaults)


def _setup_defaults(test_case):
    test_case._replaced_defaults = _implicit_environ._DEFAULTS
    _implicit_environ._DEFAULTS = _DefaultsContainer()


def _tear_down_defaults(test_case):
    _implicit_environ._DEFAULTS = test_case._replaced_defaults
