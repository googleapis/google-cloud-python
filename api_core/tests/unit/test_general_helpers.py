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

import functools

from google.api_core import general_helpers


def test_wraps_normal_func():
    def func():
        return 42

    @general_helpers.wraps(func)
    def replacement():
        return func()

    assert replacement() == 42


def test_wraps_partial():
    def func():
        return 42

    partial = functools.partial(func)

    @general_helpers.wraps(partial)
    def replacement():
        return func()

    assert replacement() == 42
