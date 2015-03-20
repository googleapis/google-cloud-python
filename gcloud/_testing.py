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

"""Shared testing utilities."""

from gcloud import _helpers
from gcloud._helpers import _DefaultsContainer


class _Monkey(object):
    # context-manager for replacing module names in the scope of a test.

    def __init__(self, module, **kw):
        self.module = module
        self.to_restore = dict([(key, getattr(module, key)) for key in kw])
        for key, value in kw.items():
            setattr(module, key, value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for key, value in self.to_restore.items():
            setattr(self.module, key, value)


def _monkey_defaults(*args, **kwargs):
    mock_defaults = _DefaultsContainer(*args, **kwargs)
    return _Monkey(_helpers, _DEFAULTS=mock_defaults)


def _setup_defaults(test_case, *args, **kwargs):
    test_case._replaced_defaults = _helpers._DEFAULTS
    _helpers._DEFAULTS = _DefaultsContainer(*args, **kwargs)


def _tear_down_defaults(test_case):
    _helpers._DEFAULTS = test_case._replaced_defaults
