# Copyright 2017 Google LLC
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

from __future__ import unicode_literals

import mock
import pytest

from google.api_core import path_template


@pytest.mark.parametrize(
    "tmpl, args, kwargs, expected_result",
    [
        # Basic positional params
        ["/v1/*", ["a"], {}, "/v1/a"],
        ["/v1/**", ["a/b"], {}, "/v1/a/b"],
        ["/v1/*/*", ["a", "b"], {}, "/v1/a/b"],
        ["/v1/*/*/**", ["a", "b", "c/d"], {}, "/v1/a/b/c/d"],
        # Basic named params
        ["/v1/{name}", [], {"name": "parent"}, "/v1/parent"],
        ["/v1/{name=**}", [], {"name": "parent/child"}, "/v1/parent/child"],
        # Named params with a sub-template
        ["/v1/{name=parent/*}", [], {"name": "parent/child"}, "/v1/parent/child"],
        [
            "/v1/{name=parent/**}",
            [],
            {"name": "parent/child/object"},
            "/v1/parent/child/object",
        ],
        # Combining positional and named params
        ["/v1/*/{name}", ["a"], {"name": "parent"}, "/v1/a/parent"],
        ["/v1/{name}/*", ["a"], {"name": "parent"}, "/v1/parent/a"],
        [
            "/v1/{parent}/*/{child}/*",
            ["a", "b"],
            {"parent": "thor", "child": "thorson"},
            "/v1/thor/a/thorson/b",
        ],
        ["/v1/{name}/**", ["a/b"], {"name": "parent"}, "/v1/parent/a/b"],
        # Combining positional and named params with sub-templates.
        [
            "/v1/{name=parent/*}/*",
            ["a"],
            {"name": "parent/child"},
            "/v1/parent/child/a",
        ],
        [
            "/v1/*/{name=parent/**}",
            ["a"],
            {"name": "parent/child/object"},
            "/v1/a/parent/child/object",
        ],
    ],
)
def test_expand_success(tmpl, args, kwargs, expected_result):
    result = path_template.expand(tmpl, *args, **kwargs)
    assert result == expected_result
    assert path_template.validate(tmpl, result)


@pytest.mark.parametrize(
    "tmpl, args, kwargs, exc_match",
    [
        # Missing positional arg.
        ["v1/*", [], {}, "Positional"],
        # Missing named arg.
        ["v1/{name}", [], {}, "Named"],
    ],
)
def test_expanded_failure(tmpl, args, kwargs, exc_match):
    with pytest.raises(ValueError, match=exc_match):
        path_template.expand(tmpl, *args, **kwargs)


@pytest.mark.parametrize(
    "tmpl, path",
    [
        # Single segment template, but multi segment value
        ["v1/*", "v1/a/b"],
        ["v1/*/*", "v1/a/b/c"],
        # Single segement named template, but multi segment value
        ["v1/{name}", "v1/a/b"],
        ["v1/{name}/{value}", "v1/a/b/c"],
        # Named value with a sub-template but invalid value
        ["v1/{name=parent/*}", "v1/grandparent/child"],
    ],
)
def test_validate_failure(tmpl, path):
    assert not path_template.validate(tmpl, path)


def test__expand_variable_match_unexpected():
    match = mock.Mock(spec=["group"])
    match.group.return_value = None
    with pytest.raises(ValueError, match="Unknown"):
        path_template._expand_variable_match([], {}, match)


def test__replace_variable_with_pattern():
    match = mock.Mock(spec=["group"])
    match.group.return_value = None
    with pytest.raises(ValueError, match="Unknown"):
        path_template._replace_variable_with_pattern(match)
