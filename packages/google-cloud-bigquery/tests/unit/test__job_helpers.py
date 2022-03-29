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

from typing import Any, Dict, Optional
from unittest import mock

from google.api_core import retry as retries
import pytest

from google.cloud.bigquery.client import Client
from google.cloud.bigquery import _job_helpers
from google.cloud.bigquery.job.query import QueryJob, QueryJobConfig
from google.cloud.bigquery.query import ConnectionProperty, ScalarQueryParameter


def make_query_request(additional_properties: Optional[Dict[str, Any]] = None):
    request = {"useLegacySql": False, "formatOptions": {"useInt64Timestamp": True}}
    if additional_properties is not None:
        request.update(additional_properties)
    return request


def make_query_response(
    completed: bool = False,
    job_id: str = "abcd-efg-hijk-lmnop",
    location="US",
    project_id="test-project",
    errors=None,
) -> Dict[str, Any]:
    response = {
        "jobReference": {
            "projectId": project_id,
            "jobId": job_id,
            "location": location,
        },
        "jobComplete": completed,
    }
    if errors is not None:
        response["errors"] = errors
    return response


@pytest.mark.parametrize(
    ("job_config", "expected"),
    (
        (None, make_query_request()),
        (QueryJobConfig(), make_query_request()),
        (
            QueryJobConfig(default_dataset="my-project.my_dataset"),
            make_query_request(
                {
                    "defaultDataset": {
                        "projectId": "my-project",
                        "datasetId": "my_dataset",
                    }
                }
            ),
        ),
        (QueryJobConfig(dry_run=True), make_query_request({"dryRun": True})),
        (
            QueryJobConfig(use_query_cache=False),
            make_query_request({"useQueryCache": False}),
        ),
        (
            QueryJobConfig(use_legacy_sql=True),
            make_query_request({"useLegacySql": True}),
        ),
        (
            QueryJobConfig(
                query_parameters=[
                    ScalarQueryParameter("named_param1", "STRING", "param-value"),
                    ScalarQueryParameter("named_param2", "INT64", 123),
                ]
            ),
            make_query_request(
                {
                    "parameterMode": "NAMED",
                    "queryParameters": [
                        {
                            "name": "named_param1",
                            "parameterType": {"type": "STRING"},
                            "parameterValue": {"value": "param-value"},
                        },
                        {
                            "name": "named_param2",
                            "parameterType": {"type": "INT64"},
                            "parameterValue": {"value": "123"},
                        },
                    ],
                }
            ),
        ),
        (
            QueryJobConfig(
                query_parameters=[
                    ScalarQueryParameter(None, "STRING", "param-value"),
                    ScalarQueryParameter(None, "INT64", 123),
                ]
            ),
            make_query_request(
                {
                    "parameterMode": "POSITIONAL",
                    "queryParameters": [
                        {
                            "parameterType": {"type": "STRING"},
                            "parameterValue": {"value": "param-value"},
                        },
                        {
                            "parameterType": {"type": "INT64"},
                            "parameterValue": {"value": "123"},
                        },
                    ],
                }
            ),
        ),
        (
            QueryJobConfig(
                connection_properties=[
                    ConnectionProperty(key="time_zone", value="America/Chicago"),
                    ConnectionProperty(key="session_id", value="abcd-efgh-ijkl-mnop"),
                ]
            ),
            make_query_request(
                {
                    "connectionProperties": [
                        {"key": "time_zone", "value": "America/Chicago"},
                        {"key": "session_id", "value": "abcd-efgh-ijkl-mnop"},
                    ]
                }
            ),
        ),
        (
            QueryJobConfig(labels={"abc": "def"}),
            make_query_request({"labels": {"abc": "def"}}),
        ),
        (
            QueryJobConfig(maximum_bytes_billed=987654),
            make_query_request({"maximumBytesBilled": "987654"}),
        ),
    ),
)
def test__to_query_request(job_config, expected):
    result = _job_helpers._to_query_request(job_config)
    assert result == expected


def test__to_query_job_defaults():
    mock_client = mock.create_autospec(Client)
    response = make_query_response(
        job_id="test-job", project_id="some-project", location="asia-northeast1"
    )
    job: QueryJob = _job_helpers._to_query_job(mock_client, "query-str", None, response)
    assert job.query == "query-str"
    assert job._client is mock_client
    assert job.job_id == "test-job"
    assert job.project == "some-project"
    assert job.location == "asia-northeast1"
    assert job.error_result is None
    assert job.errors is None


def test__to_query_job_dry_run():
    mock_client = mock.create_autospec(Client)
    response = make_query_response(
        job_id="test-job", project_id="some-project", location="asia-northeast1"
    )
    job_config: QueryJobConfig = QueryJobConfig()
    job_config.dry_run = True
    job: QueryJob = _job_helpers._to_query_job(
        mock_client, "query-str", job_config, response
    )
    assert job.dry_run is True


@pytest.mark.parametrize(
    ("completed", "expected_state"),
    (
        (True, "DONE"),
        (False, "PENDING"),
    ),
)
def test__to_query_job_sets_state(completed, expected_state):
    mock_client = mock.create_autospec(Client)
    response = make_query_response(completed=completed)
    job: QueryJob = _job_helpers._to_query_job(mock_client, "query-str", None, response)
    assert job.state == expected_state


def test__to_query_job_sets_errors():
    mock_client = mock.create_autospec(Client)
    response = make_query_response(
        errors=[
            # https://cloud.google.com/bigquery/docs/reference/rest/v2/ErrorProto
            {"reason": "backendError", "message": "something went wrong"},
            {"message": "something else went wrong"},
        ]
    )
    job: QueryJob = _job_helpers._to_query_job(mock_client, "query-str", None, response)
    assert len(job.errors) == 2
    # If we got back a response instead of an HTTP error status code, most
    # likely the job didn't completely fail.
    assert job.error_result is None


def test_query_jobs_query_defaults():
    mock_client = mock.create_autospec(Client)
    mock_retry = mock.create_autospec(retries.Retry)
    mock_job_retry = mock.create_autospec(retries.Retry)
    mock_client._call_api.return_value = {
        "jobReference": {
            "projectId": "test-project",
            "jobId": "abc",
            "location": "asia-northeast1",
        }
    }
    _job_helpers.query_jobs_query(
        mock_client,
        "SELECT * FROM test",
        None,
        "asia-northeast1",
        "test-project",
        mock_retry,
        None,
        mock_job_retry,
    )

    assert mock_client._call_api.call_count == 1
    call_args, call_kwargs = mock_client._call_api.call_args
    assert call_args[0] is mock_retry
    # See: https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
    assert call_kwargs["path"] == "/projects/test-project/queries"
    assert call_kwargs["method"] == "POST"
    # See: https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#QueryRequest
    request = call_kwargs["data"]
    assert request["requestId"] is not None
    assert request["query"] == "SELECT * FROM test"
    assert request["location"] == "asia-northeast1"
    assert request["formatOptions"]["useInt64Timestamp"] is True
    assert "timeoutMs" not in request


def test_query_jobs_query_sets_format_options():
    """Since jobs.query can return results, ensure we use the lossless
    timestamp format.

    See: https://github.com/googleapis/python-bigquery/issues/395
    """
    mock_client = mock.create_autospec(Client)
    mock_retry = mock.create_autospec(retries.Retry)
    mock_job_retry = mock.create_autospec(retries.Retry)
    mock_client._call_api.return_value = {
        "jobReference": {"projectId": "test-project", "jobId": "abc", "location": "US"}
    }
    _job_helpers.query_jobs_query(
        mock_client,
        "SELECT * FROM test",
        None,
        "US",
        "test-project",
        mock_retry,
        None,
        mock_job_retry,
    )

    assert mock_client._call_api.call_count == 1
    _, call_kwargs = mock_client._call_api.call_args
    # See: https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#QueryRequest
    request = call_kwargs["data"]
    assert request["formatOptions"]["useInt64Timestamp"] is True


@pytest.mark.parametrize(
    ("timeout", "expected_timeout"),
    (
        (-1, 0),
        (0, 0),
        (1, 1000 - _job_helpers._TIMEOUT_BUFFER_MILLIS),
    ),
)
def test_query_jobs_query_sets_timeout(timeout, expected_timeout):
    mock_client = mock.create_autospec(Client)
    mock_retry = mock.create_autospec(retries.Retry)
    mock_job_retry = mock.create_autospec(retries.Retry)
    mock_client._call_api.return_value = {
        "jobReference": {"projectId": "test-project", "jobId": "abc", "location": "US"}
    }
    _job_helpers.query_jobs_query(
        mock_client,
        "SELECT * FROM test",
        None,
        "US",
        "test-project",
        mock_retry,
        timeout,
        mock_job_retry,
    )

    assert mock_client._call_api.call_count == 1
    _, call_kwargs = mock_client._call_api.call_args
    # See: https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#QueryRequest
    request = call_kwargs["data"]
    assert request["timeoutMs"] == expected_timeout


def test_make_job_id_wo_suffix():
    job_id = _job_helpers.make_job_id("job_id")
    assert job_id == "job_id"


def test_make_job_id_w_suffix():
    with mock.patch("uuid.uuid4", side_effect=["212345"]):
        job_id = _job_helpers.make_job_id(None, prefix="job_id")

    assert job_id == "job_id212345"


def test_make_job_id_random():
    with mock.patch("uuid.uuid4", side_effect=["212345"]):
        job_id = _job_helpers.make_job_id(None)

    assert job_id == "212345"


def test_make_job_id_w_job_id_overrides_prefix():
    job_id = _job_helpers.make_job_id("job_id", prefix="unused_prefix")
    assert job_id == "job_id"
