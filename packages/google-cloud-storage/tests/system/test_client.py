# Copyright 2021 Google LLC
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

import io
import re
import tempfile

import pytest

from google.cloud import exceptions
from test_utils.vpcsc_config import vpcsc_config
from . import _helpers


public_bucket = "gcp-public-data-landsat"


@vpcsc_config.skip_if_inside_vpcsc
def test_anonymous_client_access_to_public_bucket():
    from google.cloud.storage.client import Client

    anonymous_client = Client.create_anonymous_client()
    bucket = anonymous_client.bucket(public_bucket)
    (blob,) = _helpers.retry_429_503(anonymous_client.list_blobs)(
        bucket,
        max_results=1,
    )
    with tempfile.TemporaryFile() as stream:
        _helpers.retry_429_503(blob.download_to_file)(stream)


def test_get_service_account_email(storage_client, service_account):
    domain = "gs-project-accounts.iam.gserviceaccount.com"
    email = storage_client.get_service_account_email()

    new_style = re.compile(r"service-(?P<projnum>[^@]+)@{}".format(domain))
    old_style = re.compile(r"{}@{}".format(storage_client.project, domain))
    patterns = [new_style, old_style]
    matches = [pattern.match(email) for pattern in patterns]

    assert any(match for match in matches if match is not None)


def test_create_bucket_simple(storage_client, buckets_to_delete):
    new_bucket_name = _helpers.unique_name("a-new-bucket")

    with pytest.raises(exceptions.NotFound):
        storage_client.get_bucket(new_bucket_name)

    created = _helpers.retry_429_503(storage_client.create_bucket)(new_bucket_name)
    buckets_to_delete.append(created)

    assert created.name == new_bucket_name


def test_create_bucket_dual_region(storage_client, buckets_to_delete):
    from google.cloud.storage.constants import DUAL_REGION_LOCATION_TYPE

    new_bucket_name = _helpers.unique_name("dual-region-bucket")
    region_1 = "US-EAST1"
    region_2 = "US-WEST1"
    dual_region = f"{region_1}+{region_2}"

    with pytest.raises(exceptions.NotFound):
        storage_client.get_bucket(new_bucket_name)

    created = _helpers.retry_429_503(storage_client.create_bucket)(
        new_bucket_name, location=dual_region
    )
    buckets_to_delete.append(created)

    assert created.name == new_bucket_name
    assert created.location == dual_region
    assert created.location_type == DUAL_REGION_LOCATION_TYPE


def test_list_buckets(storage_client, buckets_to_delete):
    buckets_to_create = [
        _helpers.unique_name("new"),
        _helpers.unique_name("newer"),
        _helpers.unique_name("newest"),
    ]
    created_buckets = []

    for bucket_name in buckets_to_create:
        bucket = _helpers.retry_429_503(storage_client.create_bucket)(bucket_name)
        buckets_to_delete.append(bucket)

    all_buckets = storage_client.list_buckets()

    created_buckets = [
        bucket.name for bucket in all_buckets if bucket.name in buckets_to_create
    ]

    assert sorted(created_buckets) == sorted(buckets_to_create)


def test_download_blob_to_file_w_uri(
    storage_client,
    shared_bucket,
    blobs_to_delete,
    service_account,
):
    blob = shared_bucket.blob("MyBuffer")
    payload = b"Hello World"
    blob.upload_from_string(payload)
    blobs_to_delete.append(blob)

    with tempfile.NamedTemporaryFile() as temp_f:

        with open(temp_f.name, "wb") as file_obj:
            storage_client.download_blob_to_file(
                "gs://" + shared_bucket.name + "/MyBuffer", file_obj
            )

        with open(temp_f.name, "rb") as file_obj:
            stored_contents = file_obj.read()

    assert stored_contents == payload


def test_download_blob_to_file_w_etag(
    storage_client,
    shared_bucket,
    blobs_to_delete,
    service_account,
):
    filename = "kittens"
    blob = shared_bucket.blob(filename)
    payload = b"fluffy"
    blob.upload_from_string(payload)
    blobs_to_delete.append(blob)

    buffer = io.BytesIO()
    with pytest.raises(exceptions.NotModified):
        storage_client.download_blob_to_file(
            "gs://" + shared_bucket.name + "/" + filename,
            buffer,
            if_etag_not_match=blob.etag,
        )

    buffer = io.BytesIO()
    with pytest.raises(exceptions.PreconditionFailed):
        storage_client.download_blob_to_file(
            "gs://" + shared_bucket.name + "/" + filename,
            buffer,
            if_etag_match="kittens",
        )

    buffer = io.BytesIO()
    storage_client.download_blob_to_file(
        "gs://" + shared_bucket.name + "/" + filename,
        buffer,
        if_etag_not_match="kittens",
    )
    assert buffer.getvalue() == payload

    buffer = io.BytesIO()
    storage_client.download_blob_to_file(
        "gs://" + shared_bucket.name + "/" + filename,
        buffer,
        if_etag_match=blob.etag,
    )
    assert buffer.getvalue() == payload
