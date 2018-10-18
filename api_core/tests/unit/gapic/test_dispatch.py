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

import pytest
import six

from google.api_core.gapic_v2.dispatch import dispatch


@pytest.mark.skipif(six.PY2, reason='dispatch only works on Python 3.')
def test_dispatch():
    class Foo(object):
        @dispatch
        def bar(self, number, letter):
            return 'Brought by the letter {} and the number {}.'.format(
                letter, number,
            )

        @bar.register(str)
        def _bar_with_string(self, letter):
            return self.bar(11, letter)

    foo = Foo()
    assert foo.bar(8, 'L') == 'Brought by the letter L and the number 8.'
    assert foo.bar('Z') == 'Brought by the letter Z and the number 11.'
