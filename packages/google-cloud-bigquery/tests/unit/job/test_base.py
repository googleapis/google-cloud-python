# Copyright 2015 Google LLC
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

import copy
import http
import unittest

from google.api_core import exceptions
import google.api_core.retry
import mock
import pytest

from .helpers import _make_client
from .helpers import _make_connection
from .helpers import _make_retriable_exception
from .helpers import _make_job_resource


class Test__error_result_to_exception(unittest.TestCase):
    def _call_fut(self, *args, **kwargs):
        from google.cloud.bigquery import job

        return job._error_result_to_exception(*args, **kwargs)

    def test_simple(self):
        error_result = {"reason": "invalid", "message": "bad request"}
        exception = self._call_fut(error_result)
        self.assertEqual(exception.code, http.client.BAD_REQUEST)
        self.assertTrue(exception.message.startswith("bad request"))
        self.assertIn(error_result, exception.errors)

    def test_missing_reason(self):
        error_result = {}
        exception = self._call_fut(error_result)
        self.assertEqual(exception.code, http.client.INTERNAL_SERVER_ERROR)


class Test_JobReference(unittest.TestCase):
    JOB_ID = "job-id"
    PROJECT = "test-project-123"
    LOCATION = "us-central"

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery import job

        return job._JobReference

    def _make_one(self, job_id, project, location):
        return self._get_target_class()(job_id, project, location)

    def test_ctor(self):
        job_ref = self._make_one(self.JOB_ID, self.PROJECT, self.LOCATION)

        self.assertEqual(job_ref.job_id, self.JOB_ID)
        self.assertEqual(job_ref.project, self.PROJECT)
        self.assertEqual(job_ref.location, self.LOCATION)

    def test__to_api_repr(self):
        job_ref = self._make_one(self.JOB_ID, self.PROJECT, self.LOCATION)

        self.assertEqual(
            job_ref._to_api_repr(),
            {
                "jobId": self.JOB_ID,
                "projectId": self.PROJECT,
                "location": self.LOCATION,
            },
        )

    def test_from_api_repr(self):
        api_repr = {
            "jobId": self.JOB_ID,
            "projectId": self.PROJECT,
            "location": self.LOCATION,
        }

        job_ref = self._get_target_class()._from_api_repr(api_repr)

        self.assertEqual(job_ref.job_id, self.JOB_ID)
        self.assertEqual(job_ref.project, self.PROJECT)
        self.assertEqual(job_ref.location, self.LOCATION)


class Test_AsyncJob(unittest.TestCase):
    JOB_ID = "job-id"
    PROJECT = "test-project-123"
    LOCATION = "us-central"

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery import job

        return job._AsyncJob

    def _make_one(self, job_id, client):
        return self._get_target_class()(job_id, client)

    def _make_derived_class(self):
        class Derived(self._get_target_class()):
            _JOB_TYPE = "derived"

        return Derived

    def _make_derived(self, job_id, client):
        return self._make_derived_class()(job_id, client)

    @staticmethod
    def _job_reference(job_id, project, location):
        from google.cloud.bigquery import job

        return job._JobReference(job_id, project, location)

    def test_ctor_w_bare_job_id(self):
        import threading

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)

        self.assertEqual(job.job_id, self.JOB_ID)
        self.assertEqual(job.project, self.PROJECT)
        self.assertIsNone(job.location)
        self.assertIs(job._client, client)
        self.assertEqual(
            job._properties,
            {"jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID}},
        )
        self.assertIsInstance(job._completion_lock, type(threading.Lock()))
        self.assertEqual(
            job.path, "/projects/{}/jobs/{}".format(self.PROJECT, self.JOB_ID)
        )

    def test_ctor_w_job_ref(self):
        import threading

        other_project = "other-project-234"
        client = _make_client(project=other_project)
        job_ref = self._job_reference(self.JOB_ID, self.PROJECT, self.LOCATION)
        job = self._make_one(job_ref, client)

        self.assertEqual(job.job_id, self.JOB_ID)
        self.assertEqual(job.project, self.PROJECT)
        self.assertEqual(job.location, self.LOCATION)
        self.assertIs(job._client, client)
        self.assertEqual(
            job._properties,
            {
                "jobReference": {
                    "projectId": self.PROJECT,
                    "location": self.LOCATION,
                    "jobId": self.JOB_ID,
                }
            },
        )
        self.assertFalse(job._result_set)
        self.assertIsInstance(job._completion_lock, type(threading.Lock()))
        self.assertEqual(
            job.path, "/projects/{}/jobs/{}".format(self.PROJECT, self.JOB_ID)
        )

    def test__require_client_w_none(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)

        self.assertIs(job._require_client(None), client)

    def test__require_client_w_other(self):
        client = _make_client(project=self.PROJECT)
        other = object()
        job = self._make_one(self.JOB_ID, client)

        self.assertIs(job._require_client(other), other)

    def test_job_type(self):
        client = _make_client(project=self.PROJECT)
        derived = self._make_derived(self.JOB_ID, client)

        self.assertEqual(derived.job_type, "derived")

    def test_parent_job_id(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)

        self.assertIsNone(job.parent_job_id)
        job._properties["statistics"] = {"parentJobId": "parent-job-123"}
        self.assertEqual(job.parent_job_id, "parent-job-123")

    def test_script_statistics(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)

        self.assertIsNone(job.script_statistics)
        job._properties["statistics"] = {
            "scriptStatistics": {
                "evaluationKind": "EXPRESSION",
                "stackFrames": [
                    {
                        "startLine": 5,
                        "startColumn": 29,
                        "endLine": 9,
                        "endColumn": 14,
                        "text": "QUERY TEXT",
                    }
                ],
            }
        }
        script_stats = job.script_statistics
        self.assertEqual(script_stats.evaluation_kind, "EXPRESSION")
        stack_frames = script_stats.stack_frames
        self.assertEqual(len(stack_frames), 1)
        stack_frame = stack_frames[0]
        self.assertIsNone(stack_frame.procedure_id)
        self.assertEqual(stack_frame.start_line, 5)
        self.assertEqual(stack_frame.start_column, 29)
        self.assertEqual(stack_frame.end_line, 9)
        self.assertEqual(stack_frame.end_column, 14)
        self.assertEqual(stack_frame.text, "QUERY TEXT")

    def test_transaction_info(self):
        from google.cloud.bigquery.job.base import TransactionInfo

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        assert job.transaction_info is None

        statistics = job._properties["statistics"] = {}
        assert job.transaction_info is None

        statistics["transactionInfo"] = {"transactionId": "123-abc-xyz"}
        assert isinstance(job.transaction_info, TransactionInfo)
        assert job.transaction_info.transaction_id == "123-abc-xyz"

    def test_num_child_jobs(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)

        self.assertEqual(job.num_child_jobs, 0)
        job._properties["statistics"] = {"numChildJobs": "17"}
        self.assertEqual(job.num_child_jobs, 17)

    def test_labels_miss(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertEqual(job.labels, {})

    def test_labels_update_in_place(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        labels = job.labels
        labels["foo"] = "bar"  # update in place
        self.assertEqual(job.labels, {"foo": "bar"})

    def test_labels_hit(self):
        labels = {"foo": "bar"}
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties.setdefault("configuration", {})["labels"] = labels
        self.assertEqual(job.labels, labels)

    def test_etag(self):
        etag = "ETAG-123"
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.etag)
        job._properties["etag"] = etag
        self.assertEqual(job.etag, etag)

    def test_self_link(self):
        self_link = "https://api.example.com/123"
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.self_link)
        job._properties["selfLink"] = self_link
        self.assertEqual(job.self_link, self_link)

    def test_user_email(self):
        user_email = "user@example.com"
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.user_email)
        job._properties["user_email"] = user_email
        self.assertEqual(job.user_email, user_email)

    @staticmethod
    def _datetime_and_millis():
        import datetime
        from google.cloud._helpers import _millis

        now = datetime.datetime.utcnow().replace(
            microsecond=123000,
            tzinfo=datetime.timezone.utc,  # stats timestamps have ms precision
        )
        return now, _millis(now)

    def test_created(self):
        now, millis = self._datetime_and_millis()
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.created)
        stats = job._properties["statistics"] = {}
        self.assertIsNone(job.created)
        stats["creationTime"] = millis
        self.assertEqual(job.created, now)

    def test_started(self):
        now, millis = self._datetime_and_millis()
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.started)
        stats = job._properties["statistics"] = {}
        self.assertIsNone(job.started)
        stats["startTime"] = millis
        self.assertEqual(job.started, now)

    def test_ended(self):
        now, millis = self._datetime_and_millis()
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.ended)
        stats = job._properties["statistics"] = {}
        self.assertIsNone(job.ended)
        stats["endTime"] = millis
        self.assertEqual(job.ended, now)

    def test_reservation_usage_no_stats(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties["statistics"] = {}
        self.assertEqual(job.reservation_usage, [])

    def test_reservation_usage_stats_exist(self):
        from google.cloud.bigquery.job import ReservationUsage

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties["statistics"] = {
            "reservationUsage": [
                {"name": "slot_foo", "slotMs": "42"},
                {"name": "slot_bar", "slotMs": "123"},
            ],
        }

        expected = [
            ReservationUsage(name="slot_foo", slot_ms=42),
            ReservationUsage(name="slot_bar", slot_ms=123),
        ]
        self.assertEqual(job.reservation_usage, expected)

    def test__job_statistics(self):
        statistics = {"foo": "bar"}
        client = _make_client(project=self.PROJECT)
        derived = self._make_derived(self.JOB_ID, client)
        self.assertEqual(derived._job_statistics(), {})
        stats = derived._properties["statistics"] = {}
        self.assertEqual(derived._job_statistics(), {})
        stats["derived"] = statistics
        self.assertEqual(derived._job_statistics(), statistics)

    def test_error_result(self):
        error_result = {
            "debugInfo": "DEBUG INFO",
            "location": "LOCATION",
            "message": "MESSAGE",
            "reason": "REASON",
        }
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.error_result)
        status = job._properties["status"] = {}
        self.assertIsNone(job.error_result)
        status["errorResult"] = error_result
        self.assertEqual(job.error_result, error_result)

    def test_errors(self):
        errors = [
            {
                "debugInfo": "DEBUG INFO",
                "location": "LOCATION",
                "message": "MESSAGE",
                "reason": "REASON",
            }
        ]
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.errors)
        status = job._properties["status"] = {}
        self.assertIsNone(job.errors)
        status["errors"] = errors
        self.assertEqual(job.errors, errors)

    def test_state(self):
        state = "STATE"
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.state)
        status = job._properties["status"] = {}
        self.assertIsNone(job.state)
        status["state"] = state
        self.assertEqual(job.state, state)

    def _set_properties_job(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._set_future_result = mock.Mock()
        job._properties = {
            "jobReference": job._properties["jobReference"],
            "foo": "bar",
        }
        return job

    def test__set_properties_no_stats(self):
        config = {"test": True}
        resource = {"configuration": config}
        job = self._set_properties_job()

        job._set_properties(resource)

        self.assertEqual(job._properties, resource)

    def test__set_properties_w_creation_time(self):
        now, millis = self._datetime_and_millis()
        config = {"test": True}
        stats = {"creationTime": str(millis)}
        resource = {"configuration": config, "statistics": stats}
        job = self._set_properties_job()

        job._set_properties(resource)

        cleaned = copy.deepcopy(resource)
        cleaned["statistics"]["creationTime"] = float(millis)
        self.assertEqual(job._properties, cleaned)

    def test__set_properties_w_start_time(self):
        now, millis = self._datetime_and_millis()
        config = {"test": True}
        stats = {"startTime": str(millis)}
        resource = {"configuration": config, "statistics": stats}
        job = self._set_properties_job()

        job._set_properties(resource)

        cleaned = copy.deepcopy(resource)
        cleaned["statistics"]["startTime"] = float(millis)
        self.assertEqual(job._properties, cleaned)

    def test__set_properties_w_end_time(self):
        now, millis = self._datetime_and_millis()
        config = {"test": True}
        stats = {"endTime": str(millis)}
        resource = {"configuration": config, "statistics": stats}
        job = self._set_properties_job()

        job._set_properties(resource)

        cleaned = copy.deepcopy(resource)
        cleaned["statistics"]["endTime"] = float(millis)
        self.assertEqual(job._properties, cleaned)

    def test__check_resource_config_missing_job_ref(self):
        resource = {}
        klass = self._make_derived_class()

        with self.assertRaises(KeyError):
            klass._check_resource_config(resource)

    def test__check_resource_config_missing_job_id(self):
        resource = {"jobReference": {}}
        klass = self._make_derived_class()

        with self.assertRaises(KeyError):
            klass._check_resource_config(resource)

    def test__check_resource_config_missing_configuration(self):
        resource = {"jobReference": {"jobId": self.JOB_ID}}
        klass = self._make_derived_class()

        with self.assertRaises(KeyError):
            klass._check_resource_config(resource)

    def test__check_resource_config_missing_config_type(self):
        resource = {"jobReference": {"jobId": self.JOB_ID}, "configuration": {}}
        klass = self._make_derived_class()

        with self.assertRaises(KeyError):
            klass._check_resource_config(resource)

    def test__check_resource_config_ok(self):
        derived_config = {"foo": "bar"}
        resource = {
            "jobReference": {"jobId": self.JOB_ID},
            "configuration": {"derived": derived_config},
        }
        klass = self._make_derived_class()

        # Should not throw.
        klass._check_resource_config(resource)

    def test__build_resource(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        resource = job._build_resource()
        assert resource["jobReference"]["jobId"] == self.JOB_ID

    def test_to_api_repr(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        resource = job.to_api_repr()
        assert resource["jobReference"]["jobId"] == self.JOB_ID

    def test__begin_already(self):
        job = self._set_properties_job()
        job._properties["status"] = {"state": "WHATEVER"}

        with self.assertRaises(ValueError):
            job._begin()

    def test__begin_defaults(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        resource = {
            "jobReference": {
                "jobId": self.JOB_ID,
                "projectId": self.PROJECT,
                "location": None,
            },
            "configuration": {"test": True},
        }
        job = self._set_properties_job()
        builder = job.to_api_repr = mock.Mock()
        builder.return_value = resource
        call_api = job._client._call_api = mock.Mock()
        call_api.return_value = resource
        path = "/projects/{}/jobs".format(self.PROJECT)
        job._begin()

        call_api.assert_called_once_with(
            DEFAULT_RETRY,
            span_name="BigQuery.job.begin",
            span_attributes={"path": path},
            job_ref=job,
            method="POST",
            path=path,
            data=resource,
            timeout=None,
        )
        self.assertEqual(job._properties, resource)

    def test__begin_explicit(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        other_project = "other-project-234"
        resource = {
            "jobReference": {
                "jobId": self.JOB_ID,
                "projectId": self.PROJECT,
                "location": None,
            },
            "configuration": {"test": True},
        }
        job = self._set_properties_job()
        builder = job.to_api_repr = mock.Mock()
        builder.return_value = resource
        client = _make_client(project=other_project)
        call_api = client._call_api = mock.Mock()
        call_api.return_value = resource
        retry = DEFAULT_RETRY.with_deadline(1)
        path = "/projects/{}/jobs".format(self.PROJECT)
        job._begin(client=client, retry=retry, timeout=7.5)

        call_api.assert_called_once_with(
            retry,
            span_name="BigQuery.job.begin",
            span_attributes={"path": path},
            job_ref=job,
            method="POST",
            path=path,
            data=resource,
            timeout=7.5,
        )
        self.assertEqual(job._properties, resource)

    def test_exists_defaults_miss(self):
        from google.cloud.exceptions import NotFound
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        job = self._set_properties_job()
        job._properties["jobReference"]["location"] = self.LOCATION
        call_api = job._client._call_api = mock.Mock()
        call_api.side_effect = NotFound("testing")
        self.assertFalse(job.exists())

        call_api.assert_called_once_with(
            DEFAULT_RETRY,
            span_name="BigQuery.job.exists",
            span_attributes={
                "path": "/projects/{}/jobs/{}".format(self.PROJECT, self.JOB_ID)
            },
            job_ref=job,
            method="GET",
            path="/projects/{}/jobs/{}".format(self.PROJECT, self.JOB_ID),
            query_params={"fields": "id", "location": self.LOCATION},
            timeout=None,
        )

    def test_exists_explicit_hit(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        other_project = "other-project-234"
        resource = {
            "jobReference": {
                "jobId": self.JOB_ID,
                "projectId": self.PROJECT,
                "location": None,
            },
            "configuration": {"test": True},
        }
        job = self._set_properties_job()
        client = _make_client(project=other_project)
        call_api = client._call_api = mock.Mock()
        call_api.return_value = resource
        retry = DEFAULT_RETRY.with_deadline(1)
        self.assertTrue(job.exists(client=client, retry=retry))

        call_api.assert_called_once_with(
            retry,
            span_name="BigQuery.job.exists",
            span_attributes={
                "path": "/projects/{}/jobs/{}".format(self.PROJECT, self.JOB_ID)
            },
            job_ref=job,
            method="GET",
            path="/projects/{}/jobs/{}".format(self.PROJECT, self.JOB_ID),
            query_params={"fields": "id"},
            timeout=None,
        )

    def test_exists_w_timeout(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        PATH = "/projects/{}/jobs/{}".format(self.PROJECT, self.JOB_ID)
        job = self._set_properties_job()
        call_api = job._client._call_api = mock.Mock()
        job.exists(timeout=7.5)

        call_api.assert_called_once_with(
            DEFAULT_RETRY,
            span_name="BigQuery.job.exists",
            span_attributes={"path": PATH},
            job_ref=job,
            method="GET",
            path=PATH,
            query_params={"fields": "id"},
            timeout=7.5,
        )

    def test_reload_defaults(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        resource = {
            "jobReference": {
                "jobId": self.JOB_ID,
                "projectId": self.PROJECT,
                "location": None,
            },
            "configuration": {"test": True},
        }
        job = self._set_properties_job()
        job._properties["jobReference"]["location"] = self.LOCATION
        call_api = job._client._call_api = mock.Mock()
        call_api.return_value = resource
        job.reload()

        call_api.assert_called_once_with(
            DEFAULT_RETRY,
            span_name="BigQuery.job.reload",
            span_attributes={
                "path": "/projects/{}/jobs/{}".format(self.PROJECT, self.JOB_ID)
            },
            job_ref=job,
            method="GET",
            path="/projects/{}/jobs/{}".format(self.PROJECT, self.JOB_ID),
            query_params={"location": self.LOCATION},
            timeout=None,
        )
        self.assertEqual(job._properties, resource)

    def test_reload_explicit(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        other_project = "other-project-234"
        resource = {
            "jobReference": {
                "jobId": self.JOB_ID,
                "projectId": self.PROJECT,
                "location": None,
            },
            "configuration": {"test": True},
        }
        job = self._set_properties_job()
        client = _make_client(project=other_project)
        call_api = client._call_api = mock.Mock()
        call_api.return_value = resource
        retry = DEFAULT_RETRY.with_deadline(1)
        job.reload(client=client, retry=retry, timeout=4.2)

        call_api.assert_called_once_with(
            retry,
            span_name="BigQuery.job.reload",
            span_attributes={
                "path": "/projects/{}/jobs/{}".format(self.PROJECT, self.JOB_ID)
            },
            job_ref=job,
            method="GET",
            path="/projects/{}/jobs/{}".format(self.PROJECT, self.JOB_ID),
            query_params={},
            timeout=4.2,
        )
        self.assertEqual(job._properties, resource)

    def test_cancel_defaults(self):
        resource = {
            "jobReference": {
                "jobId": self.JOB_ID,
                "projectId": self.PROJECT,
                "location": None,
            },
            "configuration": {"test": True},
        }
        response = {"job": resource}
        job = self._set_properties_job()
        job._properties["jobReference"]["location"] = self.LOCATION
        connection = job._client._connection = _make_connection(response)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            self.assertTrue(job.cancel())

        final_attributes.assert_called()

        connection.api_request.assert_called_once_with(
            method="POST",
            path="/projects/{}/jobs/{}/cancel".format(self.PROJECT, self.JOB_ID),
            query_params={"location": self.LOCATION},
            timeout=None,
        )
        self.assertEqual(job._properties, resource)

    def test_cancel_explicit(self):
        other_project = "other-project-234"
        resource = {
            "jobReference": {
                "jobId": self.JOB_ID,
                "projectId": self.PROJECT,
                "location": None,
            },
            "configuration": {"test": True},
        }
        response = {"job": resource}
        job = self._set_properties_job()
        client = _make_client(project=other_project)
        connection = client._connection = _make_connection(response)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            self.assertTrue(job.cancel(client=client, timeout=7.5))

        final_attributes.assert_called_with(
            {"path": "/projects/{}/jobs/{}/cancel".format(self.PROJECT, self.JOB_ID)},
            client,
            job,
        )

        connection.api_request.assert_called_once_with(
            method="POST",
            path="/projects/{}/jobs/{}/cancel".format(self.PROJECT, self.JOB_ID),
            query_params={},
            timeout=7.5,
        )
        self.assertEqual(job._properties, resource)

    def test_cancel_w_custom_retry(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        api_path = "/projects/{}/jobs/{}/cancel".format(self.PROJECT, self.JOB_ID)
        resource = {
            "jobReference": {
                "jobId": self.JOB_ID,
                "projectId": self.PROJECT,
                "location": None,
            },
            "configuration": {"test": True},
        }
        response = {"job": resource}
        job = self._set_properties_job()

        api_request_patcher = mock.patch.object(
            job._client._connection, "api_request", side_effect=[ValueError, response]
        )
        retry = DEFAULT_RETRY.with_deadline(1).with_predicate(
            lambda exc: isinstance(exc, ValueError)
        )

        with api_request_patcher as fake_api_request:
            with mock.patch(
                "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
            ) as final_attributes:
                result = job.cancel(retry=retry, timeout=7.5)

            final_attributes.assert_called()

        self.assertTrue(result)
        self.assertEqual(job._properties, resource)
        self.assertEqual(
            fake_api_request.call_args_list,
            [
                mock.call(method="POST", path=api_path, query_params={}, timeout=7.5),
                mock.call(
                    method="POST", path=api_path, query_params={}, timeout=7.5
                ),  # was retried once
            ],
        )

    def test__set_future_result_wo_done(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        set_exception = job.set_exception = mock.Mock()
        set_result = job.set_result = mock.Mock()

        job._set_future_result()

        set_exception.assert_not_called()
        set_result.assert_not_called()

    def test__set_future_result_w_result_set(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties["status"] = {"state": "DONE"}
        job._result_set = True
        set_exception = job.set_exception = mock.Mock()
        set_result = job.set_result = mock.Mock()

        job._set_future_result()

        set_exception.assert_not_called()
        set_result.assert_not_called()

    def test__set_future_result_w_done_wo_result_set_w_error(self):
        from google.cloud.exceptions import NotFound

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties["status"] = {
            "state": "DONE",
            "errorResult": {"reason": "notFound", "message": "testing"},
        }
        set_exception = job.set_exception = mock.Mock()
        set_result = job.set_result = mock.Mock()

        job._set_future_result()

        set_exception.assert_called_once()
        args, kw = set_exception.call_args
        (exception,) = args
        self.assertIsInstance(exception, NotFound)
        self.assertEqual(exception.message, "testing")
        self.assertEqual(kw, {})
        set_result.assert_not_called()

    def test__set_future_result_w_done_wo_result_set_wo_error(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties["status"] = {"state": "DONE"}
        set_exception = job.set_exception = mock.Mock()
        set_result = job.set_result = mock.Mock()

        job._set_future_result()

        set_exception.assert_not_called()
        set_result.assert_called_once_with(job)

    def test_done_defaults_wo_state(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        reload_ = job.reload = mock.Mock()

        self.assertFalse(job.done())

        reload_.assert_called_once_with(retry=DEFAULT_RETRY, timeout=None)

    def test_done_explicit_wo_state(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        reload_ = job.reload = mock.Mock()
        retry = DEFAULT_RETRY.with_deadline(1)

        self.assertFalse(job.done(retry=retry, timeout=7.5))

        reload_.assert_called_once_with(retry=retry, timeout=7.5)

    def test_done_already(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties["status"] = {"state": "DONE"}

        self.assertTrue(job.done())

    def test_result_default_wo_state(self):
        begun_job_resource = _make_job_resource(
            job_id=self.JOB_ID, project_id=self.PROJECT, location="US", started=True
        )
        done_job_resource = _make_job_resource(
            job_id=self.JOB_ID,
            project_id=self.PROJECT,
            location="US",
            started=True,
            ended=True,
        )
        conn = _make_connection(
            _make_retriable_exception(),
            begun_job_resource,
            _make_retriable_exception(),
            done_job_resource,
        )
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_ID, client)

        self.assertIs(job.result(), job)

        begin_call = mock.call(
            method="POST",
            path=f"/projects/{self.PROJECT}/jobs",
            data={"jobReference": {"jobId": self.JOB_ID, "projectId": self.PROJECT}},
            timeout=None,
        )
        reload_call = mock.call(
            method="GET",
            path=f"/projects/{self.PROJECT}/jobs/{self.JOB_ID}",
            query_params={"location": "US"},
            timeout=None,
        )
        conn.api_request.assert_has_calls(
            [begin_call, begin_call, reload_call, reload_call]
        )

    def test_result_w_retry_wo_state(self):
        begun_job_resource = _make_job_resource(
            job_id=self.JOB_ID, project_id=self.PROJECT, location="EU", started=True
        )
        done_job_resource = _make_job_resource(
            job_id=self.JOB_ID,
            project_id=self.PROJECT,
            location="EU",
            started=True,
            ended=True,
        )
        conn = _make_connection(
            exceptions.NotFound("not normally retriable"),
            begun_job_resource,
            exceptions.NotFound("not normally retriable"),
            done_job_resource,
        )
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(
            self._job_reference(self.JOB_ID, self.PROJECT, "EU"), client
        )
        custom_predicate = mock.Mock()
        custom_predicate.return_value = True
        custom_retry = google.api_core.retry.Retry(
            predicate=custom_predicate, initial=0.001, maximum=0.001, deadline=0.1,
        )
        self.assertIs(job.result(retry=custom_retry), job)

        begin_call = mock.call(
            method="POST",
            path=f"/projects/{self.PROJECT}/jobs",
            data={
                "jobReference": {
                    "jobId": self.JOB_ID,
                    "projectId": self.PROJECT,
                    "location": "EU",
                }
            },
            timeout=None,
        )
        reload_call = mock.call(
            method="GET",
            path=f"/projects/{self.PROJECT}/jobs/{self.JOB_ID}",
            query_params={"location": "EU"},
            timeout=None,
        )
        conn.api_request.assert_has_calls(
            [begin_call, begin_call, reload_call, reload_call]
        )

    def test_result_explicit_w_state(self):
        conn = _make_connection()
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_ID, client)
        # Use _set_properties() instead of directly modifying _properties so
        # that the result state is set properly.
        job_resource = job._properties
        job_resource["status"] = {"state": "DONE"}
        job._set_properties(job_resource)
        timeout = 1

        self.assertIs(job.result(timeout=timeout), job)

        conn.api_request.assert_not_called()

    def test_cancelled_wo_error_result(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)

        self.assertFalse(job.cancelled())

    def test_cancelled_w_error_result_not_stopped(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties["status"] = {"errorResult": {"reason": "other"}}

        self.assertFalse(job.cancelled())

    def test_cancelled_w_error_result_w_stopped(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties["status"] = {"errorResult": {"reason": "stopped"}}

        self.assertTrue(job.cancelled())


class Test_JobConfig(unittest.TestCase):
    JOB_TYPE = "testing"

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery import job

        return job._JobConfig

    def _make_one(self, job_type=JOB_TYPE):
        return self._get_target_class()(job_type)

    def test_ctor(self):
        job_config = self._make_one()
        self.assertEqual(job_config._job_type, self.JOB_TYPE)
        self.assertEqual(job_config._properties, {self.JOB_TYPE: {}})

    def test_ctor_with_unknown_property_raises_error(self):
        error_text = "Property wrong_name is unknown for"
        with pytest.raises(AttributeError, match=error_text):
            config = self._make_one()
            config.wrong_name = None

    def test_fill_from_default(self):
        from google.cloud.bigquery import QueryJobConfig

        job_config = QueryJobConfig()
        job_config.dry_run = True
        job_config.maximum_bytes_billed = 1000

        default_job_config = QueryJobConfig()
        default_job_config.use_query_cache = True
        default_job_config.maximum_bytes_billed = 2000

        final_job_config = job_config._fill_from_default(default_job_config)
        self.assertTrue(final_job_config.dry_run)
        self.assertTrue(final_job_config.use_query_cache)
        self.assertEqual(final_job_config.maximum_bytes_billed, 1000)

    def test_fill_from_default_conflict(self):
        from google.cloud.bigquery import QueryJobConfig

        basic_job_config = QueryJobConfig()
        conflicting_job_config = self._make_one("conflicting_job_type")
        self.assertNotEqual(
            basic_job_config._job_type, conflicting_job_config._job_type
        )

        with self.assertRaises(TypeError):
            basic_job_config._fill_from_default(conflicting_job_config)

    @mock.patch("google.cloud.bigquery._helpers._get_sub_prop")
    def test__get_sub_prop_wo_default(self, _get_sub_prop):
        job_config = self._make_one()
        key = "key"
        self.assertIs(job_config._get_sub_prop(key), _get_sub_prop.return_value)
        _get_sub_prop.assert_called_once_with(
            job_config._properties, [self.JOB_TYPE, key], default=None
        )

    @mock.patch("google.cloud.bigquery._helpers._get_sub_prop")
    def test__get_sub_prop_w_default(self, _get_sub_prop):
        job_config = self._make_one()
        key = "key"
        default = "default"
        self.assertIs(
            job_config._get_sub_prop(key, default=default), _get_sub_prop.return_value
        )
        _get_sub_prop.assert_called_once_with(
            job_config._properties, [self.JOB_TYPE, key], default=default
        )

    @mock.patch("google.cloud.bigquery._helpers._set_sub_prop")
    def test__set_sub_prop(self, _set_sub_prop):
        job_config = self._make_one()
        key = "key"
        value = "value"
        job_config._set_sub_prop(key, value)
        _set_sub_prop.assert_called_once_with(
            job_config._properties, [self.JOB_TYPE, key], value
        )

    def test_to_api_repr(self):
        job_config = self._make_one()
        expected = job_config._properties = {self.JOB_TYPE: {"foo": "bar"}}
        found = job_config.to_api_repr()
        self.assertEqual(found, expected)
        self.assertIsNot(found, expected)  # copied

    # 'from_api_repr' cannot be tested on '_JobConfig', because it presumes
    # the ctor can be called w/o arguments

    def test_labels_miss(self):
        job_config = self._make_one()
        self.assertEqual(job_config.labels, {})

    def test_labels_update_in_place(self):
        job_config = self._make_one()
        labels = job_config.labels
        labels["foo"] = "bar"  # update in place
        self.assertEqual(job_config.labels, {"foo": "bar"})

    def test_labels_hit(self):
        labels = {"foo": "bar"}
        job_config = self._make_one()
        job_config._properties["labels"] = labels
        self.assertEqual(job_config.labels, labels)

    def test_labels_setter_invalid(self):
        labels = object()
        job_config = self._make_one()
        with self.assertRaises(ValueError):
            job_config.labels = labels

    def test_labels_setter(self):
        labels = {"foo": "bar"}
        job_config = self._make_one()
        job_config.labels = labels
        self.assertEqual(job_config._properties["labels"], labels)
