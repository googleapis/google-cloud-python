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

import base64
import datetime
import hashlib
import os
import time

import requests

from google.api_core import path_template
from google.cloud import iam_credentials_v1
from . import _helpers


def _morph_expiration(version, expiration):
    if expiration is not None:
        return expiration

    if version == "v2":
        return int(time.time()) + 10

    return 10


def _create_signed_list_blobs_url_helper(
    client, bucket, version, expiration=None, method="GET"
):
    expiration = _morph_expiration(version, expiration)

    signed_url = bucket.generate_signed_url(
        expiration=expiration, method=method, client=client, version=version
    )

    response = requests.get(signed_url)
    assert response.status_code == 200


def test_create_signed_list_blobs_url_v2(storage_client, signing_bucket, no_mtls):
    _create_signed_list_blobs_url_helper(
        storage_client,
        signing_bucket,
        version="v2",
    )


def test_create_signed_list_blobs_url_v2_w_expiration(
    storage_client, signing_bucket, no_mtls
):
    now = datetime.datetime.utcnow()
    delta = datetime.timedelta(seconds=10)

    _create_signed_list_blobs_url_helper(
        storage_client,
        signing_bucket,
        expiration=now + delta,
        version="v2",
    )


def test_create_signed_list_blobs_url_v4(storage_client, signing_bucket, no_mtls):
    _create_signed_list_blobs_url_helper(
        storage_client,
        signing_bucket,
        version="v4",
    )


def test_create_signed_list_blobs_url_v4_w_expiration(
    storage_client, signing_bucket, no_mtls
):
    now = datetime.datetime.utcnow()
    delta = datetime.timedelta(seconds=10)
    _create_signed_list_blobs_url_helper(
        storage_client,
        signing_bucket,
        expiration=now + delta,
        version="v4",
    )


def _create_signed_read_url_helper(
    client,
    bucket,
    blob_name="LogoToSign.jpg",
    method="GET",
    version="v2",
    payload=None,
    expiration=None,
    encryption_key=None,
    service_account_email=None,
    access_token=None,
):
    expiration = _morph_expiration(version, expiration)

    if payload is not None:
        blob = bucket.blob(blob_name, encryption_key=encryption_key)
        blob.upload_from_string(payload)
    else:
        blob = bucket.get_blob("README.txt")

    signed_url = blob.generate_signed_url(
        expiration=expiration,
        method=method,
        client=client,
        version=version,
        service_account_email=service_account_email,
        access_token=access_token,
    )

    headers = {}

    if encryption_key is not None:
        headers["x-goog-encryption-algorithm"] = "AES256"
        encoded_key = base64.b64encode(encryption_key).decode("utf-8")
        headers["x-goog-encryption-key"] = encoded_key
        key_hash = hashlib.sha256(encryption_key).digest()
        key_hash = base64.b64encode(key_hash).decode("utf-8")
        headers["x-goog-encryption-key-sha256"] = key_hash

    response = requests.get(signed_url, headers=headers)
    assert response.status_code == 200

    if payload is not None:
        assert response.content == payload
    else:
        assert response.content == _helpers.signing_blob_content


def test_create_signed_read_url_v2(storage_client, signing_bucket, no_mtls):
    _create_signed_read_url_helper(storage_client, signing_bucket)


def test_create_signed_read_url_v4(storage_client, signing_bucket, no_mtls):
    _create_signed_read_url_helper(
        storage_client,
        signing_bucket,
        version="v4",
    )


def test_create_signed_read_url_v2_w_expiration(
    storage_client, signing_bucket, no_mtls
):
    now = datetime.datetime.utcnow()
    delta = datetime.timedelta(seconds=10)

    _create_signed_read_url_helper(
        storage_client, signing_bucket, expiration=now + delta
    )


def test_create_signed_read_url_v4_w_expiration(
    storage_client, signing_bucket, no_mtls
):
    now = datetime.datetime.utcnow()
    delta = datetime.timedelta(seconds=10)
    _create_signed_read_url_helper(
        storage_client, signing_bucket, expiration=now + delta, version="v4"
    )


def test_create_signed_read_url_v2_lowercase_method(
    storage_client, signing_bucket, no_mtls
):
    _create_signed_read_url_helper(storage_client, signing_bucket, method="get")


def test_create_signed_read_url_v4_lowercase_method(
    storage_client, signing_bucket, no_mtls
):
    _create_signed_read_url_helper(
        storage_client, signing_bucket, method="get", version="v4"
    )


def test_create_signed_read_url_v2_w_non_ascii_name(
    storage_client, signing_bucket, no_mtls
):
    _create_signed_read_url_helper(
        storage_client,
        signing_bucket,
        blob_name="Caf\xe9.txt",
        payload=b"Test signed URL for blob w/ non-ASCII name",
    )


def test_create_signed_read_url_v4_w_non_ascii_name(
    storage_client, signing_bucket, no_mtls
):
    _create_signed_read_url_helper(
        storage_client,
        signing_bucket,
        blob_name="Caf\xe9.txt",
        payload=b"Test signed URL for blob w/ non-ASCII name",
        version="v4",
    )


def test_create_signed_read_url_v2_w_csek(storage_client, signing_bucket, no_mtls):
    encryption_key = os.urandom(32)
    _create_signed_read_url_helper(
        storage_client,
        signing_bucket,
        blob_name="v2-w-csek.txt",
        payload=b"Test signed URL for blob w/ CSEK",
        encryption_key=encryption_key,
    )


def test_create_signed_read_url_v4_w_csek(storage_client, signing_bucket, no_mtls):
    encryption_key = os.urandom(32)
    _create_signed_read_url_helper(
        storage_client,
        signing_bucket,
        blob_name="v2-w-csek.txt",
        payload=b"Test signed URL for blob w/ CSEK",
        encryption_key=encryption_key,
        version="v4",
    )


def test_create_signed_read_url_v2_w_access_token(
    storage_client, signing_bucket, service_account, no_mtls
):
    client = iam_credentials_v1.IAMCredentialsClient()
    service_account_email = service_account.service_account_email
    name = path_template.expand(
        "projects/{project}/serviceAccounts/{service_account}",
        project="-",
        service_account=service_account_email,
    )
    scope = [
        "https://www.googleapis.com/auth/devstorage.read_write",
        "https://www.googleapis.com/auth/iam",
    ]
    response = client.generate_access_token(name=name, scope=scope)

    _create_signed_read_url_helper(
        storage_client,
        signing_bucket,
        service_account_email=service_account_email,
        access_token=response.access_token,
    )


def test_create_signed_read_url_v4_w_access_token(
    storage_client, signing_bucket, service_account, no_mtls
):
    client = iam_credentials_v1.IAMCredentialsClient()
    service_account_email = service_account.service_account_email
    name = path_template.expand(
        "projects/{project}/serviceAccounts/{service_account}",
        project="-",
        service_account=service_account_email,
    )
    scope = [
        "https://www.googleapis.com/auth/devstorage.read_write",
        "https://www.googleapis.com/auth/iam",
    ]
    response = client.generate_access_token(name=name, scope=scope)

    _create_signed_read_url_helper(
        storage_client,
        signing_bucket,
        version="v4",
        service_account_email=service_account_email,
        access_token=response.access_token,
    )


def _create_signed_delete_url_helper(client, bucket, version="v2", expiration=None):
    expiration = _morph_expiration(version, expiration)

    blob = bucket.blob("DELETE_ME.txt")
    blob.upload_from_string(b"DELETE ME!")

    signed_delete_url = blob.generate_signed_url(
        expiration=expiration,
        method="DELETE",
        client=client,
        version=version,
    )

    response = requests.request("DELETE", signed_delete_url)

    assert response.status_code == 204
    assert response.content == b""
    assert not blob.exists()


def test_create_signed_delete_url_v2(storage_client, signing_bucket, no_mtls):
    _create_signed_delete_url_helper(storage_client, signing_bucket)


def test_create_signed_delete_url_v4(storage_client, signing_bucket, no_mtls):
    _create_signed_delete_url_helper(storage_client, signing_bucket, version="v4")


def _create_signed_resumable_upload_url_helper(
    client, bucket, version="v2", expiration=None
):
    expiration = _morph_expiration(version, expiration)
    blob = bucket.blob("cruddy.txt")
    payload = b"DEADBEEF"

    # Initiate the upload using a signed URL.
    signed_resumable_upload_url = blob.generate_signed_url(
        expiration=expiration,
        method="RESUMABLE",
        client=client,
        version=version,
    )

    post_headers = {"x-goog-resumable": "start"}
    post_response = requests.post(signed_resumable_upload_url, headers=post_headers)
    assert post_response.status_code == 201

    # Finish uploading the body.
    location = post_response.headers["Location"]
    put_headers = {"content-length": str(len(payload))}
    put_response = requests.put(location, headers=put_headers, data=payload)
    assert put_response.status_code == 200

    # Download using a signed URL and verify.
    signed_download_url = blob.generate_signed_url(
        expiration=expiration, method="GET", client=client, version=version
    )

    get_response = requests.get(signed_download_url)
    assert get_response.status_code == 200
    assert get_response.content == payload

    # Finally, delete the blob using a signed URL.
    signed_delete_url = blob.generate_signed_url(
        expiration=expiration,
        method="DELETE",
        client=client,
        version=version,
    )

    delete_response = requests.delete(signed_delete_url)
    assert delete_response.status_code == 204


def test_create_signed_resumable_upload_url_v2(storage_client, signing_bucket, no_mtls):
    _create_signed_resumable_upload_url_helper(
        storage_client,
        signing_bucket,
        version="v2",
    )


def test_create_signed_resumable_upload_url_v4(storage_client, signing_bucket, no_mtls):
    _create_signed_resumable_upload_url_helper(
        storage_client,
        signing_bucket,
        version="v4",
    )


def test_generate_signed_post_policy_v4(
    storage_client, buckets_to_delete, blobs_to_delete, service_account, no_mtls
):
    bucket_name = _helpers.unique_name("post_policy")
    bucket = _helpers.retry_429_503(storage_client.create_bucket)(bucket_name)
    buckets_to_delete.append(bucket)

    blob_name = "post_policy_obj.txt"
    payload = b"DEADBEEF"
    with open(blob_name, "wb") as f:
        f.write(payload)

    policy = storage_client.generate_signed_post_policy_v4(
        bucket_name,
        blob_name,
        conditions=[
            {"bucket": bucket_name},
            ["starts-with", "$Content-Type", "text/pla"],
        ],
        expiration=datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        fields={"content-type": "text/plain"},
    )
    with open(blob_name, "r") as f:
        files = {"file": (blob_name, f)}
        response = requests.post(policy["url"], data=policy["fields"], files=files)

    os.remove(blob_name)
    assert response.status_code == 204

    blob = bucket.get_blob(blob_name)
    assert blob.download_as_bytes() == payload


def test_generate_signed_post_policy_v4_invalid_field(
    storage_client, buckets_to_delete, blobs_to_delete, service_account, no_mtls
):
    bucket_name = _helpers.unique_name("post_policy-invalid")
    bucket = _helpers.retry_429_503(storage_client.create_bucket)(bucket_name)
    buckets_to_delete.append(bucket)

    blob_name = "post_policy_obj.txt"
    payload = b"DEADBEEF"
    with open(blob_name, "wb") as f:
        f.write(payload)

    policy = storage_client.generate_signed_post_policy_v4(
        bucket_name,
        blob_name,
        conditions=[
            {"bucket": bucket_name},
            ["starts-with", "$Content-Type", "text/pla"],
        ],
        expiration=datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        fields={"x-goog-random": "invalid_field", "content-type": "text/plain"},
    )
    with open(blob_name, "r") as f:
        files = {"file": (blob_name, f)}
        response = requests.post(policy["url"], data=policy["fields"], files=files)

    os.remove(blob_name)
    assert response.status_code == 400

    assert list(bucket.list_blobs()) == []
