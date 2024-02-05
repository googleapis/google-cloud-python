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

from gapic.utils import lines


def test_sort_lines():
    assert lines.sort_lines(
        'import foo\nimport bar',
    ) == 'import bar\nimport foo'


def test_sort_lines_keeps_leading_newline():
    assert lines.sort_lines(
        '\nimport foo\nimport bar',
    ) == '\nimport bar\nimport foo'


def test_sort_lines_keeps_trailing_newline():
    assert lines.sort_lines(
        'import foo\nimport bar\n',
    ) == 'import bar\nimport foo\n'


def test_sort_lines_eliminates_blank_lines():
    assert lines.sort_lines(
        'import foo\n\n\nimport bar',
    ) == 'import bar\nimport foo'


def test_sort_lines_dedupe():
    assert lines.sort_lines(
        'import foo\nimport bar\nimport foo',
    ) == 'import bar\nimport foo'


def test_sort_lines_no_dedupe():
    assert lines.sort_lines(
        'import foo\nimport bar\nimport foo',
        dedupe=False,
    ) == 'import bar\nimport foo\nimport foo'


def test_wrap_noop():
    assert lines.wrap('foo bar baz', width=80) == 'foo bar baz'


def test_wrap_empty_text():
    assert lines.wrap('', width=80) == ''


def test_wrap_simple():
    assert lines.wrap('foo bar baz', width=5) == 'foo\nbar\nbaz'


def test_wrap_strips():
    assert lines.wrap('foo bar baz  ', width=80) == 'foo bar baz'


def test_wrap_subsequent_offset():
    assert lines.wrap('foo bar baz',
        width=5, offset=0, indent=2,
                      ) == 'foo\n  bar\n  baz'


def test_wrap_initial_offset():
    assert lines.wrap(
        'The hail in Wales falls mainly on the snails.',
        width=20, offset=12, indent=0,
    ) == 'The hail\nin Wales falls\nmainly on the\nsnails.'


def test_wrap_indent_short():
    assert lines.wrap('foo bar', width=30, indent=10) == 'foo bar'


def test_wrap_short_line_preserved():
    assert lines.wrap('foo\nbar\nbaz', width=80) == 'foo\nbar\nbaz'


def test_wrap_does_not_break_hyphenated_word():
    assert lines.wrap('do-not-break', width=5) == 'do-not-break'
