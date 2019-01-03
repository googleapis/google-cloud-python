# Copyright 2019 Google LLC
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

from unittest import mock
import warnings

from gapic.generator import options


def test_options_empty():
    opts = options.Options.build('')
    assert len(opts.templates) == 1
    assert opts.templates[0].endswith('gapic/templates')


def test_options_replace_templates():
    opts = options.Options.build('python-gapic-templates=/foo/')
    assert len(opts.templates) == 1
    assert opts.templates[0] == '/foo/'


def test_options_unrecognized():
    with mock.patch.object(warnings, 'warn') as warn:
        options.Options.build('python-gapic-abc=xyz')
    warn.assert_called_once_with('Unrecognized option: `python-gapic-abc`.')


def test_flags_unrecognized():
    with mock.patch.object(warnings, 'warn') as warn:
        options.Options.build('python-gapic-abc')
    warn.assert_called_once_with('Unrecognized option: `python-gapic-abc`.')


def test_options_unrecognized_likely_typo():
    with mock.patch.object(warnings, 'warn') as warn:
        options.Options.build('go-gapic-abc=xyz')
    assert len(warn.mock_calls) == 0
