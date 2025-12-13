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

from gapic.utils import cache


def test_cached_property():
    class Foo:
        def __init__(self):
            self.call_count = 0

        @cache.cached_property
        def bar(self):
            self.call_count += 1
            return 42

    foo = Foo()
    assert foo.call_count == 0
    assert foo.bar == 42
    assert foo.call_count == 1
    assert foo.bar == 42
    assert foo.call_count == 1
