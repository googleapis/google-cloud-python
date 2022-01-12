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

from google.api_core import exceptions

from test_utils.retry import RetryErrors
from test_utils.retry import RetryInstanceState
from test_utils.system import unique_resource_id

retry_429 = RetryErrors(exceptions.TooManyRequests)
retry_429_harder = RetryErrors(exceptions.TooManyRequests, max_tries=10)
retry_429_503 = RetryErrors(
    [exceptions.TooManyRequests, exceptions.ServiceUnavailable], max_tries=10
)
retry_failures = RetryErrors(AssertionError)

user_project = os.environ.get("GOOGLE_CLOUD_TESTS_USER_PROJECT")
testing_mtls = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE") == "true"
signing_blob_content = b"This time for sure, Rocky!"


def _bad_copy(bad_request):
    """Predicate: pass only exceptions for a failed copyTo."""
    err_msg = bad_request.message
    return err_msg.startswith("No file found in request. (POST") and "copyTo" in err_msg


def _no_event_based_hold(blob):
    return not blob.event_based_hold


def _has_kms_key_name(blob):
    return blob.kms_key_name is not None


retry_bad_copy = RetryErrors(exceptions.BadRequest, error_predicate=_bad_copy)
retry_no_event_based_hold = RetryInstanceState(_no_event_based_hold)
retry_has_kms_key_name = RetryInstanceState(_has_kms_key_name)


def unique_name(prefix):
    return prefix + unique_resource_id("-")


def empty_bucket(bucket):
    for blob in list(bucket.list_blobs(versions=True)):
        try:
            blob.delete()
        except exceptions.NotFound:
            pass


def delete_blob(blob):
    errors = (exceptions.Conflict, exceptions.TooManyRequests)
    retry = RetryErrors(errors)
    try:
        retry(blob.delete)(timeout=120)  # seconds
    except exceptions.NotFound:  # race
        pass
    except exceptions.Forbidden:  # event-based hold
        blob.event_based_hold = False
        blob.patch()
        retry_no_event_based_hold(blob.reload)()
        retry(blob.delete)(timeout=120)  # seconds


def delete_bucket(bucket):
    errors = (exceptions.Conflict, exceptions.TooManyRequests)
    retry = RetryErrors(errors, max_tries=15)
    retry(empty_bucket)(bucket)
    retry(bucket.delete)(force=True)
