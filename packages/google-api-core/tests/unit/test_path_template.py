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
    "request_obj, field, expected_result",
    [
        [{"field": "stringValue"}, "field", "stringValue"],
        [{"field": "stringValue"}, "nosuchfield", None],
        [{"field": "stringValue"}, "field.subfield", None],
        [{"field": {"subfield": "stringValue"}}, "field", None],
        [{"field": {"subfield": "stringValue"}}, "field.subfield", "stringValue"],
        [{"field": {"subfield": [1, 2, 3]}}, "field.subfield", [1, 2, 3]],
        [{"field": {"subfield": "stringValue"}}, "field", None],
        [{"field": {"subfield": "stringValue"}}, "field.nosuchfield", None],
        [
            {"field": {"subfield": {"subsubfield": "stringValue"}}},
            "field.subfield.subsubfield",
            "stringValue",
        ],
        ["string", "field", None],
    ],
)
def test_get_field(request_obj, field, expected_result):
    result = path_template.get_field(request_obj, field)
    assert result == expected_result


@pytest.mark.parametrize(
    "request_obj, field, expected_result",
    [
        [{"field": "stringValue"}, "field", {}],
        [{"field": "stringValue"}, "nosuchfield", {"field": "stringValue"}],
        [{"field": "stringValue"}, "field.subfield", {"field": "stringValue"}],
        [{"field": {"subfield": "stringValue"}}, "field.subfield", {"field": {}}],
        [
            {"field": {"subfield": "stringValue", "q": "w"}, "e": "f"},
            "field.subfield",
            {"field": {"q": "w"}, "e": "f"},
        ],
        [
            {"field": {"subfield": "stringValue"}},
            "field.nosuchfield",
            {"field": {"subfield": "stringValue"}},
        ],
        [
            {"field": {"subfield": {"subsubfield": "stringValue", "q": "w"}}},
            "field.subfield.subsubfield",
            {"field": {"subfield": {"q": "w"}}},
        ],
        ["string", "field", "string"],
        ["string", "field.subfield", "string"],
    ],
)
def test_delete_field(request_obj, field, expected_result):
    path_template.delete_field(request_obj, field)
    assert request_obj == expected_result


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


@pytest.mark.parametrize(
    "http_options, request_kwargs, expected_result",
    [
        [
            [["get", "/v1/no/template", ""]],
            {"foo": "bar"},
            ["get", "/v1/no/template", {}, {"foo": "bar"}],
        ],
        # Single templates
        [
            [["get", "/v1/{field}", ""]],
            {"field": "parent"},
            ["get", "/v1/parent", {}, {}],
        ],
        [
            [["get", "/v1/{field.sub}", ""]],
            {"field": {"sub": "parent"}, "foo": "bar"},
            ["get", "/v1/parent", {}, {"field": {}, "foo": "bar"}],
        ],
    ],
)
def test_transcode_base_case(http_options, request_kwargs, expected_result):
    http_options, expected_result = helper_test_transcode(http_options, expected_result)
    result = path_template.transcode(http_options, **request_kwargs)
    assert result == expected_result


@pytest.mark.parametrize(
    "http_options, request_kwargs, expected_result",
    [
        [
            [["get", "/v1/{field.subfield}", ""]],
            {"field": {"subfield": "parent"}, "foo": "bar"},
            ["get", "/v1/parent", {}, {"field": {}, "foo": "bar"}],
        ],
        [
            [["get", "/v1/{field.subfield.subsubfield}", ""]],
            {"field": {"subfield": {"subsubfield": "parent"}}, "foo": "bar"},
            ["get", "/v1/parent", {}, {"field": {"subfield": {}}, "foo": "bar"}],
        ],
        [
            [["get", "/v1/{field.subfield1}/{field.subfield2}", ""]],
            {"field": {"subfield1": "parent", "subfield2": "child"}, "foo": "bar"},
            ["get", "/v1/parent/child", {}, {"field": {}, "foo": "bar"}],
        ],
    ],
)
def test_transcode_subfields(http_options, request_kwargs, expected_result):
    http_options, expected_result = helper_test_transcode(http_options, expected_result)
    result = path_template.transcode(http_options, **request_kwargs)
    assert result == expected_result


@pytest.mark.parametrize(
    "http_options, request_kwargs, expected_result",
    [
        # Single segment wildcard
        [
            [["get", "/v1/{field=*}", ""]],
            {"field": "parent"},
            ["get", "/v1/parent", {}, {}],
        ],
        [
            [["get", "/v1/{field=a/*/b/*}", ""]],
            {"field": "a/parent/b/child", "foo": "bar"},
            ["get", "/v1/a/parent/b/child", {}, {"foo": "bar"}],
        ],
        # Double segment wildcard
        [
            [["get", "/v1/{field=**}", ""]],
            {"field": "parent/p1"},
            ["get", "/v1/parent/p1", {}, {}],
        ],
        [
            [["get", "/v1/{field=a/**/b/**}", ""]],
            {"field": "a/parent/p1/b/child/c1", "foo": "bar"},
            ["get", "/v1/a/parent/p1/b/child/c1", {}, {"foo": "bar"}],
        ],
        # Combined single and double segment wildcard
        [
            [["get", "/v1/{field=a/*/b/**}", ""]],
            {"field": "a/parent/b/child/c1"},
            ["get", "/v1/a/parent/b/child/c1", {}, {}],
        ],
        [
            [["get", "/v1/{field=a/**/b/*}/v2/{name}", ""]],
            {"field": "a/parent/p1/b/child", "name": "first", "foo": "bar"},
            ["get", "/v1/a/parent/p1/b/child/v2/first", {}, {"foo": "bar"}],
        ],
    ],
)
def test_transcode_with_wildcard(http_options, request_kwargs, expected_result):
    http_options, expected_result = helper_test_transcode(http_options, expected_result)
    result = path_template.transcode(http_options, **request_kwargs)
    assert result == expected_result


@pytest.mark.parametrize(
    "http_options, request_kwargs, expected_result",
    [
        # Single field body
        [
            [["post", "/v1/no/template", "data"]],
            {"data": {"id": 1, "info": "some info"}, "foo": "bar"},
            ["post", "/v1/no/template", {"id": 1, "info": "some info"}, {"foo": "bar"}],
        ],
        [
            [["post", "/v1/{field=a/*}/b/{name=**}", "data"]],
            {
                "field": "a/parent",
                "name": "first/last",
                "data": {"id": 1, "info": "some info"},
                "foo": "bar",
            },
            [
                "post",
                "/v1/a/parent/b/first/last",
                {"id": 1, "info": "some info"},
                {"foo": "bar"},
            ],
        ],
        # Wildcard body
        [
            [["post", "/v1/{field=a/*}/b/{name=**}", "*"]],
            {
                "field": "a/parent",
                "name": "first/last",
                "data": {"id": 1, "info": "some info"},
                "foo": "bar",
            },
            [
                "post",
                "/v1/a/parent/b/first/last",
                {"data": {"id": 1, "info": "some info"}, "foo": "bar"},
                {},
            ],
        ],
    ],
)
def test_transcode_with_body(http_options, request_kwargs, expected_result):
    http_options, expected_result = helper_test_transcode(http_options, expected_result)
    result = path_template.transcode(http_options, **request_kwargs)
    assert result == expected_result


@pytest.mark.parametrize(
    "http_options, request_kwargs, expected_result",
    [
        # Additional bindings
        [
            [
                ["post", "/v1/{field=a/*}/b/{name=**}", "extra_data"],
                ["post", "/v1/{field=a/*}/b/{name=**}", "*"],
            ],
            {
                "field": "a/parent",
                "name": "first/last",
                "data": {"id": 1, "info": "some info"},
                "foo": "bar",
            },
            [
                "post",
                "/v1/a/parent/b/first/last",
                {"data": {"id": 1, "info": "some info"}, "foo": "bar"},
                {},
            ],
        ],
        [
            [
                ["get", "/v1/{field=a/*}/b/{name=**}", ""],
                ["get", "/v1/{field=a/*}/b/first/last", ""],
            ],
            {"field": "a/parent", "foo": "bar"},
            ["get", "/v1/a/parent/b/first/last", {}, {"foo": "bar"}],
        ],
    ],
)
def test_transcode_with_additional_bindings(
    http_options, request_kwargs, expected_result
):
    http_options, expected_result = helper_test_transcode(http_options, expected_result)
    result = path_template.transcode(http_options, **request_kwargs)
    assert result == expected_result


@pytest.mark.parametrize(
    "http_options, request_kwargs",
    [
        [[["get", "/v1/{name}", ""]], {"foo": "bar"}],
        [[["get", "/v1/{name}", ""]], {"name": "first/last"}],
        [[["get", "/v1/{name=mr/*/*}", ""]], {"name": "first/last"}],
        [[["post", "/v1/{name}", "data"]], {"name": "first/last"}],
    ],
)
def test_transcode_fails(http_options, request_kwargs):
    http_options, _ = helper_test_transcode(http_options, range(4))
    with pytest.raises(ValueError):
        path_template.transcode(http_options, **request_kwargs)


def helper_test_transcode(http_options_list, expected_result_list):
    http_options = []
    for opt_list in http_options_list:
        http_option = {"method": opt_list[0], "uri": opt_list[1]}
        if opt_list[2]:
            http_option["body"] = opt_list[2]
        http_options.append(http_option)

    expected_result = {
        "method": expected_result_list[0],
        "uri": expected_result_list[1],
        "query_params": expected_result_list[3],
    }
    if expected_result_list[2]:
        expected_result["body"] = expected_result_list[2]

    return (http_options, expected_result)
