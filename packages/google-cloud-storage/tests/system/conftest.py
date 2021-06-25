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

import contextlib
import os

import pytest

from google.cloud.storage._helpers import _base64_md5hash
from . import _helpers


dirname = os.path.realpath(os.path.dirname(__file__))
data_dirname = os.path.abspath(os.path.join(dirname, "..", "data"))
_filenames = [
    ("logo", "CloudPlatform_128px_Retina.png"),
    ("big", "five-point-one-mb-file.zip"),
    ("simple", "simple.txt"),
]
_file_data = {
    key: {"path": os.path.join(data_dirname, file_name)}
    for key, file_name in _filenames
}

_listable_filenames = ["CloudLogo1", "CloudLogo2", "CloudLogo3", "CloudLogo4"]
_hierarchy_filenames = [
    "file01.txt",
    "parent/",
    "parent/file11.txt",
    "parent/child/file21.txt",
    "parent/child/file22.txt",
    "parent/child/grand/file31.txt",
    "parent/child/other/file32.txt",
]


@pytest.fixture(scope="session")
def storage_client():
    from google.cloud.storage import Client

    client = Client()
    with contextlib.closing(client):
        yield client


@pytest.fixture(scope="session")
def user_project():
    if _helpers.user_project is None:
        pytest.skip("USER_PROJECT not set in environment.")
    return _helpers.user_project


@pytest.fixture(scope="session")
def no_mtls():
    if _helpers.testing_mtls:
        pytest.skip("Test incompatible with mTLS.")


@pytest.fixture(scope="session")
def service_account(storage_client):
    from google.oauth2.service_account import Credentials

    if not isinstance(storage_client._credentials, Credentials):
        pytest.skip("These tests require a service account credential")
    return storage_client._credentials


@pytest.fixture(scope="session")
def shared_bucket_name():
    return _helpers.unique_name("gcp-systest")


@pytest.fixture(scope="session")
def shared_bucket(storage_client, shared_bucket_name):
    bucket = storage_client.bucket(shared_bucket_name)
    bucket.versioning_enabled = True
    _helpers.retry_429_503(bucket.create)()

    yield bucket

    _helpers.delete_bucket(bucket)


@pytest.fixture(scope="session")
def listable_bucket_name():
    return _helpers.unique_name("gcp-systest-listable")


@pytest.fixture(scope="session")
def listable_bucket(storage_client, listable_bucket_name, file_data):
    bucket = storage_client.bucket(listable_bucket_name)
    _helpers.retry_429_503(bucket.create)()

    info = file_data["logo"]
    source_blob = bucket.blob(_listable_filenames[0])
    source_blob.upload_from_filename(info["path"])

    for filename in _listable_filenames[1:]:
        _helpers.retry_bad_copy(bucket.copy_blob)(
            source_blob, bucket, filename,
        )

    yield bucket

    _helpers.delete_bucket(bucket)


@pytest.fixture(scope="session")
def listable_filenames():
    return _listable_filenames


@pytest.fixture(scope="session")
def hierarchy_bucket_name():
    return _helpers.unique_name("gcp-systest-hierarchy")


@pytest.fixture(scope="session")
def hierarchy_bucket(storage_client, hierarchy_bucket_name, file_data):
    bucket = storage_client.bucket(hierarchy_bucket_name)
    _helpers.retry_429_503(bucket.create)()

    simple_path = _file_data["simple"]["path"]
    for filename in _hierarchy_filenames:
        blob = bucket.blob(filename)
        blob.upload_from_filename(simple_path)

    yield bucket

    _helpers.delete_bucket(bucket)


@pytest.fixture(scope="session")
def hierarchy_filenames():
    return _hierarchy_filenames


@pytest.fixture(scope="session")
def signing_bucket_name():
    return _helpers.unique_name("gcp-systest-signing")


@pytest.fixture(scope="session")
def signing_bucket(storage_client, signing_bucket_name):
    bucket = storage_client.bucket(signing_bucket_name)
    _helpers.retry_429_503(bucket.create)()
    blob = bucket.blob("README.txt")
    blob.upload_from_string(_helpers.signing_blob_content)

    yield bucket

    _helpers.delete_bucket(bucket)


@pytest.fixture(scope="function")
def buckets_to_delete():
    buckets_to_delete = []

    yield buckets_to_delete

    for bucket in buckets_to_delete:
        _helpers.delete_bucket(bucket)


@pytest.fixture(scope="function")
def blobs_to_delete():
    blobs_to_delete = []

    yield blobs_to_delete

    for blob in blobs_to_delete:
        _helpers.delete_blob(blob)


@pytest.fixture(scope="session")
def file_data():
    for file_data in _file_data.values():
        with open(file_data["path"], "rb") as file_obj:
            file_data["hash"] = _base64_md5hash(file_obj)

    return _file_data
