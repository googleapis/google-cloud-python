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

import os

import pytest

from google.api_core import exceptions
from google.cloud import kms
from . import _helpers

keyring_name = "gcs-test"
default_key_name = "gcs-test"
alt_key_name = "gcs-test-alternate"
_key_name_format = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}"


def _kms_key_name(client, bucket, key_name):
    return _key_name_format.format(
        client.project,
        bucket.location.lower(),
        keyring_name,
        key_name,
    )


@pytest.fixture(scope="session")
def kms_bucket_name():
    return _helpers.unique_name("gcp-systest-kms")


@pytest.fixture(scope="session")
def kms_bucket(storage_client, kms_bucket_name, no_mtls):
    bucket = _helpers.retry_429_503(storage_client.create_bucket)(kms_bucket_name)

    yield bucket

    _helpers.delete_bucket(bucket)


@pytest.fixture(scope="session")
def kms_client():
    return kms.KeyManagementServiceClient()


@pytest.fixture(scope="function")
def keyring(storage_client, kms_bucket, kms_client):
    project = storage_client.project
    location = kms_bucket.location.lower()
    purpose = kms.enums.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT

    # If the keyring doesn't exist create it.
    keyring_path = kms_client.key_ring_path(project, location, keyring_name)

    try:
        kms_client.get_key_ring(keyring_path)
    except exceptions.NotFound:
        parent = kms_client.location_path(project, location)
        kms_client.create_key_ring(parent, keyring_name, {})

        # Mark this service account as an owner of the new keyring
        service_account_email = storage_client.get_service_account_email()
        policy = {
            "bindings": [
                {
                    "role": "roles/cloudkms.cryptoKeyEncrypterDecrypter",
                    "members": ["serviceAccount:" + service_account_email],
                }
            ]
        }
        kms_client.set_iam_policy(keyring_path, policy)

    # Populate the keyring with the keys we use in the tests
    key_names = [
        "gcs-test",
        "gcs-test-alternate",
        "explicit-kms-key-name",
        "default-kms-key-name",
        "override-default-kms-key-name",
        "alt-default-kms-key-name",
    ]
    for key_name in key_names:
        key_path = kms_client.crypto_key_path(project, location, keyring_name, key_name)
        try:
            kms_client.get_crypto_key(key_path)
        except exceptions.NotFound:
            key = {"purpose": purpose}
            kms_client.create_crypto_key(keyring_path, key_name, key)


@pytest.fixture(scope="session")
def kms_key_name(storage_client, kms_bucket):
    return _kms_key_name(storage_client, kms_bucket, default_key_name)


@pytest.fixture(scope="session")
def alt_kms_key_name(storage_client, kms_bucket):
    return _kms_key_name(storage_client, kms_bucket, alt_key_name)


def test_blob_w_explicit_kms_key_name(
    kms_bucket, blobs_to_delete, kms_key_name, file_data
):
    blob_name = "explicit-kms-key-name"
    info = file_data["simple"]
    blob = kms_bucket.blob(blob_name, kms_key_name=kms_key_name)
    blob.upload_from_filename(info["path"])
    blobs_to_delete.append(blob)

    with open(info["path"], "rb") as file_obj:
        assert blob.download_as_bytes() == file_obj.read()

    # We don't know the current version of the key.
    assert blob.kms_key_name.startswith(kms_key_name)

    (listed,) = list(kms_bucket.list_blobs())
    assert listed.kms_key_name.startswith(kms_key_name)


@_helpers.retry_failures
def test_bucket_w_default_kms_key_name(
    kms_bucket,
    blobs_to_delete,
    kms_key_name,
    alt_kms_key_name,
    file_data,
):
    blob_name = "default-kms-key-name"
    override_blob_name = "override-default-kms-key-name"
    alt_blob_name = "alt-default-kms-key-name"
    cleartext_blob_name = "cleartext"

    info = file_data["simple"]

    with open(info["path"], "rb") as file_obj:
        payload = file_obj.read()

    kms_bucket.default_kms_key_name = kms_key_name
    kms_bucket.patch()
    assert kms_bucket.default_kms_key_name == kms_key_name

    defaulted_blob = kms_bucket.blob(blob_name)
    defaulted_blob.upload_from_filename(info["path"])
    blobs_to_delete.append(defaulted_blob)

    assert defaulted_blob.download_as_bytes() == payload
    _helpers.retry_429_harder(_helpers.retry_has_kms_key_name(defaulted_blob.reload))()
    # We don't know the current version of the key.
    assert defaulted_blob.kms_key_name.startswith(kms_key_name)

    override_blob = kms_bucket.blob(override_blob_name, kms_key_name=alt_kms_key_name)
    override_blob.upload_from_filename(info["path"])
    blobs_to_delete.append(override_blob)

    assert override_blob.download_as_bytes() == payload
    # We don't know the current version of the key.
    assert override_blob.kms_key_name.startswith(alt_kms_key_name)

    kms_bucket.default_kms_key_name = alt_kms_key_name
    kms_bucket.patch()

    alt_blob = kms_bucket.blob(alt_blob_name)
    alt_blob.upload_from_filename(info["path"])
    blobs_to_delete.append(alt_blob)

    assert alt_blob.download_as_bytes() == payload
    # We don't know the current version of the key.
    assert alt_blob.kms_key_name.startswith(alt_kms_key_name)

    kms_bucket.default_kms_key_name = None
    kms_bucket.patch()

    cleartext_blob = kms_bucket.blob(cleartext_blob_name)
    cleartext_blob.upload_from_filename(info["path"])
    blobs_to_delete.append(cleartext_blob)

    assert cleartext_blob.download_as_bytes() == payload
    assert cleartext_blob.kms_key_name is None


def test_blob_rewrite_rotate_csek_to_cmek(
    kms_bucket,
    blobs_to_delete,
    kms_key_name,
    file_data,
):
    blob_name = "rotating-keys"
    source_key = os.urandom(32)
    info = file_data["simple"]

    source = kms_bucket.blob(blob_name, encryption_key=source_key)
    source.upload_from_filename(info["path"])
    blobs_to_delete.append(source)
    source_data = source.download_as_bytes()

    # We can't verify it, but ideally we would check that the following
    # URL was resolvable with our credentials
    # KEY_URL = 'https://cloudkms.googleapis.com/v1/{}'.format(
    #     kms_key_name)

    dest = kms_bucket.blob(blob_name, kms_key_name=kms_key_name)
    token, rewritten, total = dest.rewrite(source)

    while token is not None:
        token, rewritten, total = dest.rewrite(source, token=token)

    # Not adding 'dest' to 'self.case_blobs_to_delete':  it is the
    # same object as 'source'.

    assert token is None
    assert rewritten == len(source_data)
    assert total == len(source_data)

    assert dest.download_as_bytes() == source_data

    # Test existing kmsKeyName version is ignored in the rewrite request
    dest = kms_bucket.get_blob(blob_name)
    source = kms_bucket.get_blob(blob_name)
    token, rewritten, total = dest.rewrite(source)

    while token is not None:
        token, rewritten, total = dest.rewrite(source, token=token)

    assert rewritten == len(source_data)
    assert dest.download_as_bytes() == source_data


def test_blob_upload_w_bucket_cmek_enabled(
    kms_bucket,
    blobs_to_delete,
    kms_key_name,
    file_data,
):
    blob_name = "test-blob"
    payload = b"DEADBEEF"
    alt_payload = b"NEWDEADBEEF"

    kms_bucket.default_kms_key_name = kms_key_name
    kms_bucket.patch()
    assert kms_bucket.default_kms_key_name == kms_key_name

    blob = kms_bucket.blob(blob_name)
    blob.upload_from_string(payload)
    blobs_to_delete.append(blob)

    _helpers.retry_429_harder(_helpers.retry_has_kms_key_name(blob.reload))()
    # We don't know the current version of the key.
    assert blob.kms_key_name.startswith(kms_key_name)

    blob.upload_from_string(alt_payload, if_generation_match=blob.generation)

    assert blob.download_as_bytes() == alt_payload

    kms_bucket.default_kms_key_name = None
    _helpers.retry_429_harder(kms_bucket.patch)()

    assert kms_bucket.default_kms_key_name is None
