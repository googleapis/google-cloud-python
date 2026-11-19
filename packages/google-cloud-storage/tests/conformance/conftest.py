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

import atexit
import os
import random
import uuid
from typing import Optional

import pytest
from google.auth.credentials import AnonymousCredentials
from google.cloud.exceptions import NotFound

from google.cloud import storage

from ._utils import start_testbench, stop_testbench

"""Environment variable or default host for Storage testbench emulator."""
_HOST = os.environ.get("STORAGE_EMULATOR_HOST", "http://localhost:9000")
_TESTBENCH_CONTAINER: Optional[str] = None


def _cleanup_testbench() -> None:
    global _TESTBENCH_CONTAINER
    container = _TESTBENCH_CONTAINER
    if container:
        _TESTBENCH_CONTAINER = None
        stop_testbench(container)


def _running_retry_conformance(config) -> bool:
    args = [str(arg) for arg in (config.args or [])]
    if not args:
        return True
    return any("test_conformance" in arg or os.path.isdir(arg) for arg in args)


def pytest_configure(config) -> None:
    """Start a single shared storage-testbench container for retry conformance tests.

    Under pytest-xdist, only the controller starts and stops the container;
    workers inherit STORAGE_EMULATOR_HOST via os.environ.
    """
    global _TESTBENCH_CONTAINER
    if getattr(config.option, "help", False) or getattr(
        config.option, "collectonly", False
    ):
        return
    if hasattr(config, "workerinput"):
        return
    if os.environ.get("STORAGE_EMULATOR_HOST"):
        return
    if not _running_retry_conformance(config):
        return

    container_name = f"storage-conformance-{uuid.uuid4().hex[:8]}"
    http_endpoint, _ = start_testbench(container_name, host_http_port=9000)
    _TESTBENCH_CONTAINER = container_name
    atexit.register(_cleanup_testbench)
    os.environ["STORAGE_EMULATOR_HOST"] = http_endpoint


def pytest_unconfigure(config) -> None:
    _cleanup_testbench()


"""Emulated project information for the storage testbench."""
_CONF_TEST_PROJECT_ID = "my-project-id"
_CONF_TEST_SERVICE_ACCOUNT_EMAIL = (
    "my-service-account@my-project-id.iam.gserviceaccount.com"
)
_CONF_TEST_PUBSUB_TOPIC_NAME = "my-topic-name"


"""Create content payload in different sizes."""


def _create_block(desired_kib):
    line = "abcdefXYZ123456789ADDINGrandom#"  # len(line) = 31
    multiplier = int(desired_kib / (len(line) + 1))
    lines = "".join(
        line + str(random.randint(0, 9)) for _ in range(multiplier)
    )  # add random single digit integers
    return 1024 * lines


_STRING_CONTENT = "hello world"
_SIZE_9MB = 9216  # 9*1024 KiB


########################################################################################################################################
### Pytest Fixtures to Populate Retry Conformance Test Resources #######################################################################
########################################################################################################################################


@pytest.fixture
def client():
    host = os.environ.get("STORAGE_EMULATOR_HOST", _HOST)
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
    except NotFound:  # in cases where bucket is deleted within the test
        pass


@pytest.fixture
def object(client, bucket):
    blob = client.bucket(bucket.name).blob(uuid.uuid4().hex)
    blob.upload_from_string(_STRING_CONTENT)
    blob.reload()
    yield blob
    try:
        blob.delete()
    except NotFound:  # in cases where object is deleted within the test
        pass


@pytest.fixture
def notification(client, bucket):
    notification = client.bucket(bucket.name).notification(
        topic_name=_CONF_TEST_PUBSUB_TOPIC_NAME
    )
    notification.create()
    notification.reload()
    yield notification
    try:
        notification.delete()
    except NotFound:  # in cases where notification is deleted within the test
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
    except NotFound:  # in cases where hmac_key is deleted within the test
        pass


@pytest.fixture
def file_data(client, bucket):
    blob = client.bucket(bucket.name).blob(uuid.uuid4().hex)
    payload = _create_block(_SIZE_9MB)
    blob.upload_from_string(payload)
    yield blob, payload
    try:
        blob.delete()
    except NotFound:  # in cases where object is deleted within the test
        pass
