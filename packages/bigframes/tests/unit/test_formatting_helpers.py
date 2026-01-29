# Copyright 2023 Google LLC
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

import unittest.mock as mock

import bigframes_vendored.constants as constants
import google.api_core.exceptions as api_core_exceptions
import google.cloud.bigquery as bigquery
import pytest

import bigframes.core.events as bfevents
import bigframes.formatting_helpers as formatting_helpers
import bigframes.version


def test_wait_for_query_job_error_includes_feedback_link():
    mock_query_job = mock.create_autospec(bigquery.QueryJob)
    mock_query_job.result.side_effect = api_core_exceptions.BadRequest(
        "Test message 123."
    )

    with pytest.raises(api_core_exceptions.BadRequest) as cap_exc:
        formatting_helpers.wait_for_job(mock_query_job)

    cap_exc.match("Test message 123.")
    cap_exc.match(constants.FEEDBACK_LINK)


def test_wait_for_job_error_includes_feedback_link():
    mock_job = mock.create_autospec(bigquery.LoadJob)
    mock_job.result.side_effect = api_core_exceptions.BadRequest("Test message 123.")

    with pytest.raises(api_core_exceptions.BadRequest) as cap_exc:
        formatting_helpers.wait_for_job(mock_job)

    cap_exc.match("Test message 123.")
    cap_exc.match(constants.FEEDBACK_LINK)


def test_wait_for_job_error_includes_version():
    mock_job = mock.create_autospec(bigquery.LoadJob)
    mock_job.result.side_effect = api_core_exceptions.BadRequest("Test message 123.")

    with pytest.raises(api_core_exceptions.BadRequest) as cap_exc:
        formatting_helpers.wait_for_job(mock_job)

    cap_exc.match("Test message 123.")
    cap_exc.match(bigframes.version.__version__)


@pytest.mark.parametrize(
    "test_input, expected", [(None, "N/A"), ("string", "N/A"), (100000, "100.0 kB")]
)
def test_get_formatted_bytes(test_input, expected):
    assert formatting_helpers.get_formatted_bytes(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected", [(None, None), ("string", "string"), (66000, "a minute")]
)
def test_get_formatted_time(test_input, expected):
    assert formatting_helpers.get_formatted_time(test_input) == expected


def test_render_bqquery_sent_event_html():
    event = bfevents.BigQuerySentEvent(
        query="SELECT * FROM my_table",
        job_id="my-job-id",
        location="us-central1",
        billing_project="my-project",
    )
    html = formatting_helpers.render_bqquery_sent_event_html(event)
    assert "SELECT * FROM my_table" in html
    assert "my-job-id" in html
    assert "us-central1" in html
    assert "my-project" in html
    assert "<details>" in html


def test_render_bqquery_sent_event_plaintext():
    event = bfevents.BigQuerySentEvent(
        query="SELECT * FROM my_table",
        job_id="my-job-id",
        location="us-central1",
        billing_project="my-project",
    )
    text = formatting_helpers.render_bqquery_sent_event_plaintext(event)
    assert "my-job-id" in text
    assert "us-central1" in text
    assert "my-project" in text
    assert "SELECT * FROM my_table" not in text


def test_render_bqquery_retry_event_html():
    event = bfevents.BigQueryRetryEvent(
        query="SELECT * FROM my_table",
        job_id="my-job-id",
        location="us-central1",
        billing_project="my-project",
    )
    html = formatting_helpers.render_bqquery_retry_event_html(event)
    assert "Retrying query" in html
    assert "SELECT * FROM my_table" in html
    assert "my-job-id" in html
    assert "us-central1" in html
    assert "my-project" in html
    assert "<details>" in html


def test_render_bqquery_retry_event_plaintext():
    event = bfevents.BigQueryRetryEvent(
        query="SELECT * FROM my_table",
        job_id="my-job-id",
        location="us-central1",
        billing_project="my-project",
    )
    text = formatting_helpers.render_bqquery_retry_event_plaintext(event)
    assert "Retrying query" in text
    assert "my-job-id" in text
    assert "us-central1" in text
    assert "my-project" in text
    assert "SELECT * FROM my_table" not in text


def test_render_bqquery_received_event_html():
    mock_plan_entry = mock.create_autospec(
        bigquery.job.query.QueryPlanEntry, instance=True
    )
    mock_plan_entry.__str__.return_value = "mocked plan"
    event = bfevents.BigQueryReceivedEvent(
        job_id="my-job-id",
        location="us-central1",
        billing_project="my-project",
        state="RUNNING",
        query_plan=[mock_plan_entry],
    )
    html = formatting_helpers.render_bqquery_received_event_html(event)
    assert "Query" in html
    assert "my-job-id" in html
    assert "is RUNNING" in html
    assert "<details>" in html
    assert "mocked plan" in html


def test_render_bqquery_received_event_plaintext():
    event = bfevents.BigQueryReceivedEvent(
        job_id="my-job-id",
        location="us-central1",
        billing_project="my-project",
        state="RUNNING",
        query_plan=[],
    )
    text = formatting_helpers.render_bqquery_received_event_plaintext(event)
    assert "Query" in text
    assert "my-job-id" in text
    assert "is RUNNING" in text
    assert "Query Plan" not in text


def test_render_bqquery_finished_event_html():
    event = bfevents.BigQueryFinishedEvent(
        job_id="my-job-id",
        location="us-central1",
        billing_project="my-project",
        total_bytes_processed=1000,
        slot_millis=2000,
    )
    html = formatting_helpers.render_bqquery_finished_event_html(event)
    assert "Query" in html
    assert "my-job-id" in html
    assert "processed 1.0 kB" in html
    assert "2 seconds of slot time" in html


def test_render_bqquery_finished_event_plaintext():
    event = bfevents.BigQueryFinishedEvent(
        job_id="my-job-id",
        location="us-central1",
        billing_project="my-project",
        total_bytes_processed=1000,
        slot_millis=2000,
    )
    text = formatting_helpers.render_bqquery_finished_event_plaintext(event)
    assert "Query" in text
    assert "my-job-id" in text
    assert "finished" in text
    assert "1.0 kB processed" in text
    assert "Slot time: 2 seconds" in text


def test_get_job_url():
    job_id = "my-job-id"
    location = "us-central1"
    project_id = "my-project"
    expected_url = (
        f"https://console.cloud.google.com/bigquery?project={project_id}"
        f"&j=bq:{location}:{job_id}&page=queryresults"
    )

    actual_url = formatting_helpers.get_job_url(
        job_id=job_id, location=location, project_id=project_id
    )
    assert actual_url == expected_url
