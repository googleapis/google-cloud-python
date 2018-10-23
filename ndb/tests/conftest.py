# Copyright 2018 Google LLC
#
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

This defines fixtures (expected to be) shared across different test
modules.
"""

from google.cloud.ndb import model

import pytest


@pytest.fixture
def property_clean_cache():
    """Reset the ``_find_methods_cache`` class attribute on ``Property``

    This property is set at runtime (with calls to ``_find_methods()``), so
    this fixture allows resetting the class to its original state.
    """
    try:
        yield
    finally:
        del model.Property._find_methods_cache
