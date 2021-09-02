# Copyright 2021 Google LLC
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

"""Conformance tests for retry. Verifies correct behavior around retryable errors, idempotency and preconditions."""

import os
import requests
import tempfile
import uuid
import logging
import functools
import pytest

from google.cloud import storage
from google.auth.credentials import AnonymousCredentials

from . import _read_local_json


_CONFORMANCE_TESTS = _read_local_json("retry_strategy_test_data.json")[
    "retryStrategyTests"
]

_STORAGE_EMULATOR_ENV_VAR = "STORAGE_EMULATOR_HOST"
"""Environment variable defining host for Storage testbench emulator."""

_CONF_TEST_PROJECT_ID = "my-project-id"
_CONF_TEST_SERVICE_ACCOUNT_EMAIL = (
    "my-service-account@my-project-id.iam.gserviceaccount.com"
)

_STRING_CONTENT = "hello world"
_BYTE_CONTENT = b"12345678"


########################################################################################################################################
### Library methods for mapping ########################################################################################################
########################################################################################################################################


def bucket_get_blob(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    object = resources.get("object")
    bucket = client.bucket(bucket.name)
    bucket.get_blob(object.name)


def blob_exists(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    object = resources.get("object")
    blob = client.bucket(bucket.name).blob(object.name)
    blob.exists()


def blob_download_as_bytes(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    object = resources.get("object")
    blob = client.bucket(bucket.name).blob(object.name)
    blob.download_as_bytes()


def blob_download_as_text(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    object = resources.get("object")
    blob = client.bucket(bucket.name).blob(object.name)
    blob.download_as_text()


def blob_download_to_filename(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    object = resources.get("object")
    blob = client.bucket(bucket.name).blob(object.name)
    with tempfile.NamedTemporaryFile() as temp_f:
        blob.download_to_filename(temp_f.name)


def client_download_blob_to_file(client, _preconditions, **resources):
    object = resources.get("object")
    with tempfile.NamedTemporaryFile() as temp_f:
        with open(temp_f.name, "wb") as file_obj:
            client.download_blob_to_file(object, file_obj)


def blobreader_read(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    object = resources.get("object")
    blob = client.bucket(bucket.name).blob(object.name)
    with blob.open() as reader:
        reader.read()


def client_list_blobs(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    blobs = client.list_blobs(bucket.name)
    for b in blobs:
        pass


def bucket_list_blobs(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    blobs = client.bucket(bucket.name).list_blobs()
    for b in blobs:
        pass


def bucket_delete(client, _preconditions, **resources):
    bucket = client.bucket(resources.get("bucket").name)
    bucket.delete(force=True)


def bucket_reload(client, _preconditions, **resources):
    bucket = client.bucket(resources.get("bucket").name)
    bucket.reload()


def client_get_bucket(client, _preconditions, **resources):
    client.get_bucket(resources.get("bucket").name)


def client_lookup_bucket(client, _preconditions, **resources):
    client.lookup_bucket(resources.get("bucket").name)


def bucket_exists(client, _preconditions, **resources):
    bucket = client.bucket(resources.get("bucket").name)
    bucket.exists()


def client_create_bucket(client, _preconditions, **_):
    bucket = client.bucket(uuid.uuid4().hex)
    client.create_bucket(bucket)


def bucket_create(client, _preconditions, **_):
    bucket = client.bucket(uuid.uuid4().hex)
    bucket.create()


def client_list_buckets(client, _preconditions, **_):
    buckets = client.list_buckets()
    for b in buckets:
        pass


def bucket_get_iam_policy(client, _preconditions, **resources):
    bucket = client.bucket(resources.get("bucket").name)
    bucket.get_iam_policy()


def bucket_test_iam_permissions(client, _preconditions, **resources):
    bucket = client.bucket(resources.get("bucket").name)
    permissions = ["storage.buckets.get", "storage.buckets.create"]
    bucket.test_iam_permissions(permissions)


def bucket_lock_retention_policy(client, _preconditions, **resources):
    bucket = client.bucket(resources.get("bucket").name)
    bucket.retention_period = 60
    bucket.patch()
    bucket.lock_retention_policy()


def notification_create(client, _preconditions, **resources):
    bucket = client.get_bucket(resources.get("bucket").name)
    notification = bucket.notification()
    notification.create()


def bucket_list_notifications(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    notifications = client.bucket(bucket.name).list_notifications()
    for n in notifications:
        pass


def bucket_get_notification(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    notification = resources.get("notification")
    client.bucket(bucket.name).get_notification(notification.notification_id)


def notification_reload(client, _preconditions, **resources):
    notification = client.bucket(resources.get("bucket").name).notification(
        notification_id=resources.get("notification").notification_id
    )
    notification.reload()


def notification_exists(client, _preconditions, **resources):
    notification = client.bucket(resources.get("bucket").name).notification(
        notification_id=resources.get("notification").notification_id
    )
    notification.exists()


def notification_delete(client, _preconditions, **resources):
    notification = client.bucket(resources.get("bucket").name).notification(
        notification_id=resources.get("notification").notification_id
    )
    notification.delete()


def client_list_hmac_keys(client, _preconditions, **_):
    hmac_keys = client.list_hmac_keys()
    for k in hmac_keys:
        pass


def client_get_service_account_email(client, _preconditions, **_):
    client.get_service_account_email()


def bucket_patch(client, _preconditions, **resources):
    bucket = client.get_bucket(resources.get("bucket").name)
    metageneration = bucket.metageneration
    bucket.storage_class = "COLDLINE"
    if _preconditions:
        bucket.patch(if_metageneration_match=metageneration)
    else:
        bucket.patch()


def bucket_update(client, _preconditions, **resources):
    bucket = client.get_bucket(resources.get("bucket").name)
    metageneration = bucket.metageneration
    bucket._properties = {"storageClass": "STANDARD"}
    if _preconditions:
        bucket.update(if_metageneration_match=metageneration)
    else:
        bucket.update()


def bucket_set_iam_policy(client, _preconditions, **resources):
    bucket = client.get_bucket(resources.get("bucket").name)
    role = "roles/storage.objectViewer"
    member = _CONF_TEST_SERVICE_ACCOUNT_EMAIL

    policy = bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append({"role": role, "members": {member}})
    if _preconditions:
        bucket.set_iam_policy(policy)
    else:
        # IAM policies have no metageneration:  clear ETag to avoid checking that it matches.
        policy.etag = None
        bucket.set_iam_policy(policy)


def bucket_delete_blob(client, _preconditions, **resources):
    object = resources.get("object")
    bucket = client.bucket(resources.get("bucket").name)
    if _preconditions:
        generation = object.generation
        bucket.delete_blob(object.name, if_generation_match=generation)
    else:
        bucket.delete_blob(object.name)


def bucket_delete_blobs(client, _preconditions, **resources):
    object = resources.get("object")
    bucket = client.bucket(resources.get("bucket").name)
    sources = [object]
    source_generations = [object.generation]
    if _preconditions:
        bucket.delete_blobs(sources, if_generation_match=source_generations)
    else:
        bucket.delete_blobs(sources)


def blob_delete(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    object = resources.get("object")
    blob = client.bucket(bucket.name).blob(object.name)
    if _preconditions:
        blob.delete(if_generation_match=object.generation)
    else:
        blob.delete()


def blob_patch(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    object = resources.get("object")
    blob = client.bucket(bucket.name).blob(object.name)
    blob.metadata = {"foo": "bar"}
    if _preconditions:
        blob.patch(if_metageneration_match=object.metageneration)
    else:
        blob.patch()


def blob_update(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    object = resources.get("object")
    blob = client.bucket(bucket.name).blob(object.name)
    blob.metadata = {"foo": "bar"}
    if _preconditions:
        blob.update(if_metageneration_match=object.metageneration)
    else:
        blob.update()


def bucket_copy_blob(client, _preconditions, **resources):
    object = resources.get("object")
    bucket = client.bucket(resources.get("bucket").name)
    destination = client.create_bucket(uuid.uuid4().hex)
    if _preconditions:
        bucket.copy_blob(
            object, destination, new_name=uuid.uuid4().hex, if_generation_match=0
        )
    else:
        bucket.copy_blob(object, destination)


def bucket_rename_blob(client, _preconditions, **resources):
    object = resources.get("object")
    bucket = client.bucket(resources.get("bucket").name)
    blob = bucket.blob(resources.get("object").name)
    new_name = uuid.uuid4().hex
    if _preconditions:
        bucket.rename_blob(
            blob,
            new_name,
            if_generation_match=0,
            if_source_generation_match=object.generation,
        )
    else:
        bucket.rename_blob(blob, new_name)


def blob_rewrite(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    object = resources.get("object")
    new_blob = client.bucket(bucket.name).blob(uuid.uuid4().hex)
    new_blob.metadata = {"foo": "bar"}
    if _preconditions:
        new_blob.rewrite(object, if_generation_match=0)
    else:
        new_blob.rewrite(object)


def blob_update_storage_class(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    object = resources.get("object")
    blob = client.bucket(bucket.name).blob(object.name)
    storage_class = "STANDARD"
    if _preconditions:
        blob.update_storage_class(storage_class, if_generation_match=object.generation)
    else:
        blob.update_storage_class(storage_class)


def blob_compose(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    object = resources.get("object")
    blob = client.bucket(bucket.name).blob(object.name)
    blob_2 = bucket.blob(uuid.uuid4().hex)
    blob_2.upload_from_string(_STRING_CONTENT)
    sources = [blob_2]
    if _preconditions:
        blob.compose(sources, if_generation_match=object.generation)
    else:
        blob.compose(sources)


def blob_upload_from_string(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    blob = client.bucket(bucket.name).blob(uuid.uuid4().hex)
    if _preconditions:
        blob.upload_from_string(_STRING_CONTENT, if_generation_match=0)
    else:
        blob.upload_from_string(_STRING_CONTENT)


def blob_upload_from_file(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    blob = client.bucket(bucket.name).blob(uuid.uuid4().hex)
    with tempfile.NamedTemporaryFile() as temp_f:
        if _preconditions:
            blob.upload_from_file(temp_f, if_generation_match=0)
        else:
            blob.upload_from_file(temp_f)


def blob_upload_from_filename(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    blob = client.bucket(bucket.name).blob(uuid.uuid4().hex)

    with tempfile.NamedTemporaryFile() as temp_f:
        if _preconditions:
            blob.upload_from_filename(temp_f.name, if_generation_match=0)
        else:
            blob.upload_from_filename(temp_f.name)


def blobwriter_write(client, _preconditions, **resources):
    chunk_size = 256 * 1024
    bucket = resources.get("bucket")
    blob = client.bucket(bucket.name).blob(uuid.uuid4().hex)
    if _preconditions:
        with blob.open("wb", chunk_size=chunk_size, if_generation_match=0) as writer:
            writer.write(_BYTE_CONTENT)
    else:
        with blob.open("wb", chunk_size=chunk_size) as writer:
            writer.write(_BYTE_CONTENT)


def blob_create_resumable_upload_session(client, _preconditions, **resources):
    bucket = resources.get("bucket")
    blob = client.bucket(bucket.name).blob(uuid.uuid4().hex)
    if _preconditions:
        blob.create_resumable_upload_session(if_generation_match=0)
    else:
        blob.create_resumable_upload_session()


########################################################################################################################################
### Method Invocation Mapping ##########################################################################################################
########################################################################################################################################

# Method invocation mapping is a map whose keys are a string describing a standard
# API call (e.g. storage.objects.get) and values are a list of functions which
# wrap library methods that implement these calls. There may be multiple values
# because multiple library methods may use the same call (e.g. get could be a
# read or just a metadata get).

method_mapping = {
    "storage.buckets.delete": [bucket_delete],  # S1 start
    "storage.buckets.get": [
        client_get_bucket,
        bucket_reload,
        client_lookup_bucket,
        bucket_exists,
    ],
    "storage.buckets.getIamPolicy": [bucket_get_iam_policy],
    "storage.buckets.insert": [client_create_bucket, bucket_create],
    "storage.buckets.list": [client_list_buckets],
    "storage.buckets.lockRetentionPolicy": [bucket_lock_retention_policy],
    "storage.buckets.testIamPermissions": [bucket_test_iam_permissions],
    "storage.notifications.delete": [notification_delete],
    "storage.notifications.get": [
        bucket_get_notification,
        notification_exists,
        notification_reload,
    ],
    "storage.notifications.list": [bucket_list_notifications],
    "storage.objects.get": [
        bucket_get_blob,
        blob_exists,
        client_download_blob_to_file,
        blob_download_to_filename,
        blob_download_as_bytes,
        blob_download_as_text,
        blobreader_read,
    ],
    "storage.objects.list": [
        client_list_blobs,
        bucket_list_blobs,
        bucket_delete,
    ],  # S1 end
    "storage.buckets.patch": [bucket_patch],  # S2/S3 start
    "storage.buckets.setIamPolicy": [bucket_set_iam_policy],
    "storage.buckets.update": [bucket_update],
    "storage.objects.compose": [blob_compose],
    "storage.objects.copy": [bucket_copy_blob, bucket_rename_blob],
    "storage.objects.delete": [
        bucket_delete_blob,
        bucket_delete_blobs,
        blob_delete,
        bucket_rename_blob,
    ],
    "storage.objects.insert": [
        blob_upload_from_string,
        blob_upload_from_file,
        blob_upload_from_filename,
        blobwriter_write,
        blob_create_resumable_upload_session,
    ],
    "storage.objects.patch": [blob_patch],
    "storage.objects.rewrite": [blob_rewrite, blob_update_storage_class],
    "storage.objects.update": [blob_update],  # S2/S3 end
}


########################################################################################################################################
### Pytest Fixtures to Populate Resources ##############################################################################################
########################################################################################################################################


@pytest.fixture
def client():
    host = os.environ.get(_STORAGE_EMULATOR_ENV_VAR)
    client = storage.Client(
        project=_CONF_TEST_PROJECT_ID,
        credentials=AnonymousCredentials(),
        client_options={"api_endpoint": host},
    )
    return client


@pytest.fixture
def bucket(client):
    bucket = client.bucket(uuid.uuid4().hex)
    client.create_bucket(bucket)
    yield bucket
    try:
        bucket.delete(force=True)
    except Exception:
        # in cases where resources are deleted within the test
        # TODO(cathyo@): narrow except to NotFound once the emulator response issue is resolved
        pass


@pytest.fixture
def object(client, bucket):
    blob = client.bucket(bucket.name).blob(uuid.uuid4().hex)
    blob.upload_from_string(_STRING_CONTENT)
    blob.reload()
    yield blob
    try:
        blob.delete()
    except Exception:  # in cases where resources are deleted within the test
        pass


@pytest.fixture
def notification(client, bucket):
    notification = client.bucket(bucket.name).notification()
    notification.create()
    notification.reload()
    yield notification
    try:
        notification.delete()
    except Exception:  # in cases where resources are deleted within the test
        pass


@pytest.fixture
def hmac_key(client):
    hmac_key, _secret = client.create_hmac_key(
        service_account_email=_CONF_TEST_SERVICE_ACCOUNT_EMAIL,
        project_id=_CONF_TEST_PROJECT_ID,
    )
    yield hmac_key
    try:
        hmac_key.state = "INACTIVE"
        hmac_key.update()
        hmac_key.delete()
    except Exception:  # in cases where resources are deleted within the test
        pass


########################################################################################################################################
### Helper Methods for Testbench Retry Test API ########################################################################################
########################################################################################################################################


"""
The Retry Test API in the testbench is used to run the retry conformance tests. It offers a mechanism to describe more complex
retry scenarios while sending a single, constant header through all the HTTP requests from a test program. The Retry Test API
can be accessed by adding the path "/retry-test" to the host. See also: https://github.com/googleapis/storage-testbench
"""


def _create_retry_test(host, method_name, instructions):
    """
    For each test case, initialize a Retry Test resource by loading a set of
    instructions to the testbench host. The instructions include an API method
    and a list of errors. An unique id is created for each Retry Test resource.
    """
    import json

    retry_test_uri = host + "/retry_test"
    headers = {
        "Content-Type": "application/json",
    }
    data_dict = {"instructions": {method_name: instructions}}
    data = json.dumps(data_dict)
    r = requests.post(retry_test_uri, headers=headers, data=data)
    return r.json()


def _get_retry_test(host, id):
    """
    Retrieve the state of the Retry Test resource, including the unique id,
    instructions, and a boolean status "completed". This can be used to verify
    if all instructions were used as expected.
    """
    get_retry_test_uri = "{base}{retry}/{id}".format(
        base=host, retry="/retry_test", id=id
    )
    r = requests.get(get_retry_test_uri)
    return r.json()


def _run_retry_test(
    host, id, lib_func, _preconditions, bucket, object, notification, hmac_key
):
    """
    To execute tests against the list of instrucions sent to the Retry Test API,
    create a client to send the retry test ID using the x-retry-test-id header
    in each request. For incoming requests that match the test ID and API method,
    the testbench will pop off the next instruction from the list and force the
    listed failure case.
    """
    client = storage.Client(
        project=_CONF_TEST_PROJECT_ID,
        credentials=AnonymousCredentials(),
        client_options={"api_endpoint": host},
    )
    client._http.headers.update({"x-retry-test-id": id})
    lib_func(
        client,
        _preconditions,
        bucket=bucket,
        object=object,
        notification=notification,
        hmac_key=hmac_key,
    )


def _delete_retry_test(host, id):
    """
    Delete the Retry Test resource by id.
    """
    get_retry_test_uri = "{base}{retry}/{id}".format(
        base=host, retry="/retry_test", id=id
    )
    requests.delete(get_retry_test_uri)


########################################################################################################################################
### Run Test Case for Retry Strategy ###################################################################################################
########################################################################################################################################


def run_test_case(
    scenario_id, method, case, lib_func, host, bucket, object, notification, hmac_key
):
    scenario = _CONFORMANCE_TESTS[scenario_id - 1]
    expect_success = scenario["expectSuccess"]
    precondition_provided = scenario["preconditionProvided"]
    method_name = method["name"]
    instructions = case["instructions"]

    try:
        r = _create_retry_test(host, method_name, instructions)
        id = r["id"]
    except Exception as e:
        raise Exception(
            "Error creating retry test for {}: {}".format(method_name, e)
        ).with_traceback(e.__traceback__)

    # Run retry tests on library methods.
    try:
        _run_retry_test(
            host,
            id,
            lib_func,
            precondition_provided,
            bucket,
            object,
            notification,
            hmac_key,
        )
    except Exception as e:
        logging.exception(
            "Caught an exception while running retry instructions\n {}".format(e)
        )
        success_results = False
    else:
        success_results = True

    # Assert expected success for each scenario.
    assert (
        expect_success == success_results
    ), "Retry API call expected_success was {}, should be {}".format(
        success_results, expect_success
    )

    # Verify that all instructions were used up during the test
    # (indicates that the client sent the correct requests).
    status_response = _get_retry_test(host, id)
    assert (
        status_response["completed"] is True
    ), "Retry test not completed; unused instructions:{}".format(
        status_response["instructions"]
    )

    # Clean up and close out test in testbench.
    _delete_retry_test(host, id)


########################################################################################################################################
### Run Conformance Tests for Retry Strategy ###########################################################################################
########################################################################################################################################

for scenario in _CONFORMANCE_TESTS:
    host = os.environ.get(_STORAGE_EMULATOR_ENV_VAR)
    if host is None:
        logging.error(
            "This test must use the testbench emulator; set STORAGE_EMULATOR_HOST to run."
        )
        break

    id = scenario["id"]
    methods = scenario["methods"]
    cases = scenario["cases"]
    for c in cases:
        for m in methods:
            method_name = m["name"]
            if method_name not in method_mapping:
                logging.info("No tests for operation {}".format(method_name))
                continue

            for lib_func in method_mapping[method_name]:
                test_name = "test-S{}-{}-{}".format(id, method_name, lib_func.__name__)
                globals()[test_name] = functools.partial(
                    run_test_case, id, m, c, lib_func, host
                )
