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

from api_factory.utils import lines


def test_wrap_noop():
    assert lines.wrap('foo bar baz', width=80) == 'foo bar baz'


def test_wrap_empty_text():
    assert lines.wrap('', width=80) == ''


def test_wrap_simple():
    assert lines.wrap('foo bar baz', width=5) == 'foo\nbar\nbaz'


def test_wrap_strips():
    assert lines.wrap('foo bar baz  ', width=80) == 'foo bar baz'


def test_wrap_subsequent_indent():
    assert lines.wrap(
        '# foo bar baz',
        width=5,
        subsequent_indent='# ',
    ) == '# foo\n# bar\n# baz'


def test_wrap_initial_width():
    assert lines.wrap(
        'The hail in Wales falls mainly on the snails.',
        width=20,
        initial_width=8,
    ) == 'The hail\nin Wales falls\nmainly on the\nsnails.'


def test_wrap_initial_width_short():
    assert lines.wrap('foo bar', width=30, initial_width=20) == 'foo bar'
