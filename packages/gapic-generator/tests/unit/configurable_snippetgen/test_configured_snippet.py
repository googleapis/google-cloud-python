# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from pathlib import Path

from google.protobuf import json_format
from google.protobuf.compiler import plugin_pb2
import libcst
import pytest

from gapic import utils
from gapic.configurable_snippetgen import configured_snippet
from gapic.configurable_snippetgen import snippet_config_language_pb2
from gapic.schema import api


CURRENT_DIRECTORY = Path(__file__).parent.absolute()
SPEECH_V1_REQUEST_PATH = CURRENT_DIRECTORY / \
    "resources" / "speech" / "request.desc"
CONFIG_JSON_PATH = (
    CURRENT_DIRECTORY / "resources" / "speech" / "speech_createCustomClass.json"
)


def _load_api_schema(request_path: Path) -> api.API:
    with open(request_path, "rb") as f:
        request_bytes = f.read()

    req = plugin_pb2.CodeGeneratorRequest.FromString(request_bytes)

    # From gapic/cli/generator.py.
    opts = utils.Options.build(req.parameter)
    api_schema = api.API.build(
        req.proto_file,
        opts=opts,
        package="google.cloud.speech.v1",
    )

    return api_schema


def _load_snippet_config(
    config_path: Path,
) -> snippet_config_language_pb2.SnippetConfig:
    with open(config_path, "r") as f:
        config_json = f.read()

    snippet_config = json_format.Parse(
        config_json, snippet_config_language_pb2.SnippetConfig()
    )

    return snippet_config


def _make_configured_snippet(
    request_path: Path, config_path: Path, api_version: str, is_sync: bool
) -> configured_snippet.ConfiguredSnippet:
    api_schema = _load_api_schema(request_path)
    snippet_config = _load_snippet_config(config_path)

    return configured_snippet.ConfiguredSnippet(
        api_schema, snippet_config, api_version, is_sync
    )


@pytest.fixture
def snippet():
    return _make_configured_snippet(
        SPEECH_V1_REQUEST_PATH, CONFIG_JSON_PATH, api_version="v1", is_sync=True
    )


def test_gapic_module_name(snippet):
    assert snippet.gapic_module_name == "speech_v1"


@pytest.mark.parametrize(
    "is_sync,expected",
    [
        (True, "speech_v1_config_Adaptation_CreateCustomClass_Basic_sync"),
        (False, "speech_v1_config_Adaptation_CreateCustomClass_Basic_async"),
    ],
)
def test_region_tag(is_sync, expected):
    snippet = _make_configured_snippet(
        SPEECH_V1_REQUEST_PATH, CONFIG_JSON_PATH, api_version="v1", is_sync=is_sync
    )
    assert snippet.region_tag == expected


def test_sample_function_name(snippet):
    assert snippet.sample_function_name == "sample_create_custom_class_Basic"


@pytest.mark.parametrize(
    "is_sync,expected",
    [
        (True, "AdaptationClient"),
        (False, "AdaptationAsyncClient"),
    ],
)
def test_client_class_name(is_sync, expected):
    snippet = _make_configured_snippet(
        SPEECH_V1_REQUEST_PATH, CONFIG_JSON_PATH, api_version="v1", is_sync=is_sync
    )
    assert snippet.client_class_name == expected


@pytest.mark.parametrize(
    "is_sync,expected",
    [
        (True, "speech_v1_generated_Adaptation_create_custom_class_Basic_sync.py"),
        (False, "speech_v1_generated_Adaptation_create_custom_class_Basic_async.py"),
    ],
)
def test_filename(is_sync, expected):
    snippet = _make_configured_snippet(
        SPEECH_V1_REQUEST_PATH, CONFIG_JSON_PATH, api_version="v1", is_sync=is_sync
    )
    assert snippet.filename == expected


def test_AppendToSampleFunctionBody():
    # Start with a function def with nonempty body to we can be sure the
    # transformer appends the statement.
    function_def = libcst.parse_statement("def f():\n    'hello'")
    statement = libcst.parse_statement("'world'")
    transformer = configured_snippet._AppendToSampleFunctionBody(statement)
    updated_function_def = function_def.visit(transformer)
    expected_function_def = libcst.parse_statement(
        "def f():\n    'hello'\n    'world'")
    assert updated_function_def.deep_equals(expected_function_def)


def test_code(snippet):
    snippet.generate()

    # https://github.com/googleapis/gapic-generator-python/issues/1522
    # Placeholder code.  We will gradually add to the ConfiguredSnippet class
    # until the generated code is the same as that of the golden file.
    expected_code = """def sample_create_custom_class_Basic(parent = "projects/[PROJECT]/locations/us", custom_class_id = "passengerships"):
    \"\"
    client = speech_v1.AdaptationClient()
"""
    assert snippet.code == expected_code
