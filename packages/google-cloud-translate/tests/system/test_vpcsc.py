# -*- coding: utf-8 -*-
#
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
"""Unit tests for VPC-SC."""

import pytest

from google.api_core import exceptions
from google.cloud import translate_v3beta1
from test_utils.vpcsc_config import vpcsc_config

_VPCSC_PROHIBITED_MESSAGE = "Request is prohibited by organization's policy"


@pytest.fixture(scope="module")
def client():
    return translate_v3beta1.TranslationServiceClient()


@pytest.fixture(scope="module")
def parent_inside(client):
    return client.location_path(vpcsc_config.project_inside, "us-central1")


@pytest.fixture(scope="module")
def parent_outside(client):
    return client.location_path(vpcsc_config.project_outside, "us-central1")


@pytest.fixture(scope="module")
def glossary_name_inside(client):
    return client.glossary_path(
        vpcsc_config.project_inside, "us-central1", "fake_glossary"
    )


@pytest.fixture(scope="module")
def glossary_name_outside(client):
    return client.glossary_path(
        vpcsc_config.project_outside, "us-central1", "fake_glossary"
    )


def _make_glossary(name):
    return {
        "name": name,
        "language_codes_set": {"language_codes": ["en", "ja"]},
        "input_config": {
            "gcs_source": {"input_uri": "gs://fake-bucket/fake_glossary.csv"}
        },
    }


@pytest.fixture(scope="module")
def glossary_inside(glossary_name_inside):
    return _make_glossary(glossary_name_inside)


@pytest.fixture(scope="module")
def glossary_outside(glossary_name_outside):
    return _make_glossary(glossary_name_outside)


@vpcsc_config.skip_unless_inside_vpcsc
def test_create_glossary_w_inside(client, parent_inside, glossary_inside):
    client.create_glossary(parent_inside, glossary_inside)


@vpcsc_config.skip_unless_inside_vpcsc
def test_create_glossary_w_outside(client, parent_outside, glossary_outside):
    with pytest.raises(exceptions.PermissionDenied) as exc:
        client.create_glossary(parent_outside, glossary_outside)

    assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)


@vpcsc_config.skip_unless_inside_vpcsc
def test_list_glossaries_w_inside(client, parent_inside):
    list(client.list_glossaries(parent_inside))


@vpcsc_config.skip_unless_inside_vpcsc
def test_list_glossaries_w_outside(client, parent_outside):
    with pytest.raises(exceptions.PermissionDenied) as exc:
        list(client.list_glossaries(parent_outside))

    assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)


@vpcsc_config.skip_unless_inside_vpcsc
def test_get_glossary_w_inside(client, glossary_name_inside):
    try:
        client.get_glossary(glossary_name_inside)
    except exceptions.NotFound:  # no perms issue
        pass


@vpcsc_config.skip_unless_inside_vpcsc
def test_get_glossary_w_outside(client, glossary_name_outside):
    with pytest.raises(exceptions.PermissionDenied) as exc:
        client.get_glossary(glossary_name_outside)

    assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)


@vpcsc_config.skip_unless_inside_vpcsc
def test_delete_glossary_w_inside(client, glossary_name_inside):
    try:
        client.delete_glossary(glossary_name_inside)
    except exceptions.NotFound:  # no perms issue
        pass


@vpcsc_config.skip_unless_inside_vpcsc
def test_delete_glossary_w_outside(client, glossary_name_outside):
    with pytest.raises(exceptions.PermissionDenied) as exc:
        client.delete_glossary(glossary_name_outside)

    assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)


@vpcsc_config.skip_unless_inside_vpcsc
def test_batch_translate_text_w_inside(client, parent_inside):
    source_language_code = "en"
    target_language_codes = ["es"]
    input_configs = [{"gcs_source": {"input_uri": "gs://fake-bucket/*"}}]
    output_config = {
        "gcs_destination": {"output_uri_prefix": "gs://fake-bucket/output/"}
    }
    client.batch_translate_text(  # no perms issue
        parent_inside,
        source_language_code,
        target_language_codes,
        input_configs,
        output_config,
    )


@vpcsc_config.skip_unless_inside_vpcsc
def test_batch_translate_text_w_outside(client, parent_outside):
    source_language_code = "en"
    target_language_codes = ["es"]
    input_configs = [{"gcs_source": {"input_uri": "gs://fake-bucket/*"}}]
    output_config = {
        "gcs_destination": {"output_uri_prefix": "gs://fake-bucket/output/"}
    }
    with pytest.raises(exceptions.PermissionDenied) as exc:
        client.batch_translate_text(
            parent_outside,
            source_language_code,
            target_language_codes,
            input_configs,
            output_config,
        )

    assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)
