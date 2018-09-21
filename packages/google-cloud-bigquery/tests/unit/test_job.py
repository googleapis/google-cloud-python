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
import unittest

import mock
from six.moves import http_client
try:
    import pandas
except (ImportError, AttributeError):  # pragma: NO COVER
    pandas = None


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_client(project='test-project', connection=None):
    from google.cloud.bigquery.client import Client

    if connection is None:
        connection = _make_connection()

    client = Client(
        project=project, credentials=_make_credentials(), _http=object())
    client._connection = connection
    return client


def _make_connection(*responses):
    import google.cloud.bigquery._http
    from google.cloud.exceptions import NotFound

    mock_conn = mock.create_autospec(google.cloud.bigquery._http.Connection)
    mock_conn.api_request.side_effect = list(responses) + [NotFound('miss')]
    return mock_conn


class Test__error_result_to_exception(unittest.TestCase):

    def _call_fut(self, *args, **kwargs):
        from google.cloud.bigquery import job

        return job._error_result_to_exception(*args, **kwargs)

    def test_simple(self):
        error_result = {
            'reason': 'invalid',
            'message': 'bad request'
        }
        exception = self._call_fut(error_result)
        self.assertEqual(exception.code, http_client.BAD_REQUEST)
        self.assertTrue(exception.message.startswith('bad request'))
        self.assertIn(error_result, exception.errors)

    def test_missing_reason(self):
        error_result = {}
        exception = self._call_fut(error_result)
        self.assertEqual(exception.code, http_client.INTERNAL_SERVER_ERROR)


class Test_JobReference(unittest.TestCase):
    JOB_ID = 'job-id'
    PROJECT = 'test-project-123'
    LOCATION = 'us-central'

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

        self.assertEqual(job_ref._to_api_repr(), {
            'jobId': self.JOB_ID,
            'projectId': self.PROJECT,
            'location': self.LOCATION,
        })

    def test_from_api_repr(self):
        api_repr = {
            'jobId': self.JOB_ID,
            'projectId': self.PROJECT,
            'location': self.LOCATION,
        }

        job_ref = self._get_target_class()._from_api_repr(api_repr)

        self.assertEqual(job_ref.job_id, self.JOB_ID)
        self.assertEqual(job_ref.project, self.PROJECT)
        self.assertEqual(job_ref.location, self.LOCATION)


class Test_AsyncJob(unittest.TestCase):
    JOB_ID = 'job-id'
    PROJECT = 'test-project-123'
    LOCATION = 'us-central'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery import job

        return job._AsyncJob

    def _make_one(self, job_id, client):
        return self._get_target_class()(job_id, client)

    def _make_derived_class(self):
        class Derived(self._get_target_class()):
            _JOB_TYPE = 'derived'

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
            {
                'jobReference': {
                    'projectId': self.PROJECT,
                    'jobId': self.JOB_ID,
                },
            }
        )
        self.assertIsInstance(job._completion_lock, type(threading.Lock()))
        self.assertEqual(
            job.path,
            '/projects/{}/jobs/{}'.format(self.PROJECT, self.JOB_ID))

    def test_ctor_w_job_ref(self):
        import threading

        other_project = 'other-project-234'
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
                'jobReference': {
                    'projectId': self.PROJECT,
                    'location': self.LOCATION,
                    'jobId': self.JOB_ID,
                },
            }
        )
        self.assertFalse(job._result_set)
        self.assertIsInstance(job._completion_lock, type(threading.Lock()))
        self.assertEqual(
            job.path,
            '/projects/{}/jobs/{}'.format(self.PROJECT, self.JOB_ID))

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

        self.assertEqual(derived.job_type, 'derived')

    def test_labels_miss(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertEqual(job.labels, {})

    def test_labels_update_in_place(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        labels = job.labels
        labels['foo'] = 'bar'  # update in place
        self.assertEqual(job.labels, {'foo': 'bar'})

    def test_labels_hit(self):
        labels = {
            'foo': 'bar',
        }
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties['labels'] = labels
        self.assertEqual(job.labels, labels)

    def test_etag(self):
        etag = 'ETAG-123'
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.etag)
        job._properties['etag'] = etag
        self.assertEqual(job.etag, etag)

    def test_self_link(self):
        self_link = 'https://api.example.com/123'
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.self_link)
        job._properties['selfLink'] = self_link
        self.assertEqual(job.self_link, self_link)

    def test_user_email(self):
        user_email = 'user@example.com'
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.user_email)
        job._properties['user_email'] = user_email
        self.assertEqual(job.user_email, user_email)

    @staticmethod
    def _datetime_and_millis():
        import datetime
        import pytz
        from google.cloud._helpers import _millis
        now = datetime.datetime.utcnow().replace(
            microsecond=123000,  # stats timestamps have ms precision
            tzinfo=pytz.UTC)
        return now, _millis(now)

    def test_created(self):
        now, millis = self._datetime_and_millis()
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.created)
        stats = job._properties['statistics'] = {}
        self.assertIsNone(job.created)
        stats['creationTime'] = millis
        self.assertEqual(job.created, now)

    def test_started(self):
        now, millis = self._datetime_and_millis()
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.started)
        stats = job._properties['statistics'] = {}
        self.assertIsNone(job.started)
        stats['startTime'] = millis
        self.assertEqual(job.started, now)

    def test_ended(self):
        now, millis = self._datetime_and_millis()
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.ended)
        stats = job._properties['statistics'] = {}
        self.assertIsNone(job.ended)
        stats['endTime'] = millis
        self.assertEqual(job.ended, now)

    def test__job_statistics(self):
        statistics = {'foo': 'bar'}
        client = _make_client(project=self.PROJECT)
        derived = self._make_derived(self.JOB_ID, client)
        self.assertEqual(derived._job_statistics(), {})
        stats = derived._properties['statistics'] = {}
        self.assertEqual(derived._job_statistics(), {})
        stats['derived'] = statistics
        self.assertEqual(derived._job_statistics(), statistics)

    def test_error_result(self):
        error_result = {
            'debugInfo': 'DEBUG INFO',
            'location': 'LOCATION',
            'message': 'MESSAGE',
            'reason': 'REASON'
        }
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.error_result)
        status = job._properties['status'] = {}
        self.assertIsNone(job.error_result)
        status['errorResult'] = error_result
        self.assertEqual(job.error_result, error_result)

    def test_errors(self):
        errors = [{
            'debugInfo': 'DEBUG INFO',
            'location': 'LOCATION',
            'message': 'MESSAGE',
            'reason': 'REASON'
        }]
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.errors)
        status = job._properties['status'] = {}
        self.assertIsNone(job.errors)
        status['errors'] = errors
        self.assertEqual(job.errors, errors)

    def test_state(self):
        state = 'STATE'
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        self.assertIsNone(job.state)
        status = job._properties['status'] = {}
        self.assertIsNone(job.state)
        status['state'] = state
        self.assertEqual(job.state, state)

    def test__scrub_local_properties(self):
        before = {'foo': 'bar'}
        resource = before.copy()
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._scrub_local_properties(resource)  # no raise
        self.assertEqual(resource, before)

    def test__copy_configuration_properties(self):
        before = {'foo': 'bar'}
        resource = before.copy()
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        with self.assertRaises(NotImplementedError):
            job._copy_configuration_properties(resource)
        self.assertEqual(resource, before)

    def _set_properties_job(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._scrub_local_properties = mock.Mock()
        job._copy_configuration_properties = mock.Mock()
        job._set_future_result = mock.Mock()
        job._properties = {
            'jobReference': job._properties['jobReference'],
            'foo': 'bar',
        }
        return job

    def test__set_properties_no_stats(self):
        config = {
            'test': True,
        }
        resource = {
            'configuration': config,
        }
        job = self._set_properties_job()

        job._set_properties(resource)

        self.assertEqual(job._properties, resource)

        job._scrub_local_properties.assert_called_once_with(resource)
        job._copy_configuration_properties.assert_called_once_with(config)

    def test__set_properties_w_creation_time(self):
        now, millis = self._datetime_and_millis()
        config = {
            'test': True,
        }
        stats = {
            'creationTime': str(millis),
        }
        resource = {
            'configuration': config,
            'statistics': stats,
        }
        job = self._set_properties_job()

        job._set_properties(resource)

        cleaned = copy.deepcopy(resource)
        cleaned['statistics']['creationTime'] = float(millis)
        self.assertEqual(job._properties, cleaned)

        job._scrub_local_properties.assert_called_once_with(resource)
        job._copy_configuration_properties.assert_called_once_with(config)

    def test__set_properties_w_start_time(self):
        now, millis = self._datetime_and_millis()
        config = {
            'test': True,
        }
        stats = {
            'startTime': str(millis),
        }
        resource = {
            'configuration': config,
            'statistics': stats,
        }
        job = self._set_properties_job()

        job._set_properties(resource)

        cleaned = copy.deepcopy(resource)
        cleaned['statistics']['startTime'] = float(millis)
        self.assertEqual(job._properties, cleaned)

        job._scrub_local_properties.assert_called_once_with(resource)
        job._copy_configuration_properties.assert_called_once_with(config)

    def test__set_properties_w_end_time(self):
        now, millis = self._datetime_and_millis()
        config = {
            'test': True,
        }
        stats = {
            'endTime': str(millis),
        }
        resource = {
            'configuration': config,
            'statistics': stats,
        }
        job = self._set_properties_job()

        job._set_properties(resource)

        cleaned = copy.deepcopy(resource)
        cleaned['statistics']['endTime'] = float(millis)
        self.assertEqual(job._properties, cleaned)

        job._scrub_local_properties.assert_called_once_with(resource)
        job._copy_configuration_properties.assert_called_once_with(config)

    def test__get_resource_config_missing_job_ref(self):
        resource = {}
        klass = self._make_derived_class()

        with self.assertRaises(KeyError):
            klass._get_resource_config(resource)

    def test__get_resource_config_missing_job_id(self):
        resource = {
            'jobReference': {},
        }
        klass = self._make_derived_class()

        with self.assertRaises(KeyError):
            klass._get_resource_config(resource)

    def test__get_resource_config_missing_configuration(self):
        resource = {
            'jobReference': {'jobId': self.JOB_ID},
        }
        klass = self._make_derived_class()

        with self.assertRaises(KeyError):
            klass._get_resource_config(resource)

    def test__get_resource_config_missing_config_type(self):
        resource = {
            'jobReference': {'jobId': self.JOB_ID},
            'configuration': {},
        }
        klass = self._make_derived_class()

        with self.assertRaises(KeyError):
            klass._get_resource_config(resource)

    def test__get_resource_config_ok(self):
        derived_config = {'foo': 'bar'}
        resource = {
            'jobReference': {'jobId': self.JOB_ID},
            'configuration': {
                'derived': derived_config,
            },
        }
        klass = self._make_derived_class()

        job_id, config = klass._get_resource_config(resource)

        self.assertEqual(job_id, self.JOB_ID)
        self.assertEqual(config, {'derived': derived_config})

    def test__build_resource(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        with self.assertRaises(NotImplementedError):
            job._build_resource()

    def test__begin_already(self):
        job = self._set_properties_job()
        job._properties['status'] = {'state': 'WHATEVER'}

        with self.assertRaises(ValueError):
            job._begin()

    def test__begin_defaults(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        resource = {
            'jobReference': {
                'jobId': self.JOB_ID,
                'projectId': self.PROJECT,
                'location': None,
            },
            'configuration': {
                'test': True,
            }
        }
        job = self._set_properties_job()
        builder = job._build_resource = mock.Mock()
        builder.return_value = resource
        call_api = job._client._call_api = mock.Mock()
        call_api.return_value = resource

        job._begin()

        call_api.assert_called_once_with(
            DEFAULT_RETRY,
            method='POST',
            path='/projects/{}/jobs'.format(self.PROJECT),
            data=resource,
        )
        self.assertEqual(job._properties, resource)

    def test__begin_explicit(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        other_project = 'other-project-234'
        resource = {
            'jobReference': {
                'jobId': self.JOB_ID,
                'projectId': self.PROJECT,
                'location': None,
            },
            'configuration': {
                'test': True,
            }
        }
        job = self._set_properties_job()
        builder = job._build_resource = mock.Mock()
        builder.return_value = resource
        client = _make_client(project=other_project)
        call_api = client._call_api = mock.Mock()
        call_api.return_value = resource
        retry = DEFAULT_RETRY.with_deadline(1)

        job._begin(client=client, retry=retry)

        call_api.assert_called_once_with(
            retry,
            method='POST',
            path='/projects/{}/jobs'.format(self.PROJECT),
            data=resource,
        )
        self.assertEqual(job._properties, resource)

    def test_exists_defaults_miss(self):
        from google.cloud.exceptions import NotFound
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        job = self._set_properties_job()
        job._properties['jobReference']['location'] = self.LOCATION
        call_api = job._client._call_api = mock.Mock()
        call_api.side_effect = NotFound('testing')

        self.assertFalse(job.exists())

        call_api.assert_called_once_with(
            DEFAULT_RETRY,
            method='GET',
            path='/projects/{}/jobs/{}'.format(self.PROJECT, self.JOB_ID),
            query_params={
                'fields': 'id',
                'location': self.LOCATION,
            }
        )

    def test_exists_explicit_hit(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        other_project = 'other-project-234'
        resource = {
            'jobReference': {
                'jobId': self.JOB_ID,
                'projectId': self.PROJECT,
                'location': None,
            },
            'configuration': {
                'test': True,
            }
        }
        job = self._set_properties_job()
        client = _make_client(project=other_project)
        call_api = client._call_api = mock.Mock()
        call_api.return_value = resource
        retry = DEFAULT_RETRY.with_deadline(1)

        self.assertTrue(job.exists(client=client, retry=retry))

        call_api.assert_called_once_with(
            retry,
            method='GET',
            path='/projects/{}/jobs/{}'.format(self.PROJECT, self.JOB_ID),
            query_params={'fields': 'id'}
        )

    def test_reload_defaults(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        resource = {
            'jobReference': {
                'jobId': self.JOB_ID,
                'projectId': self.PROJECT,
                'location': None,
            },
            'configuration': {
                'test': True,
            }
        }
        job = self._set_properties_job()
        job._properties['jobReference']['location'] = self.LOCATION
        call_api = job._client._call_api = mock.Mock()
        call_api.return_value = resource

        job.reload()

        call_api.assert_called_once_with(
            DEFAULT_RETRY,
            method='GET',
            path='/projects/{}/jobs/{}'.format(self.PROJECT, self.JOB_ID),
            query_params={'location': self.LOCATION},
        )
        self.assertEqual(job._properties, resource)

    def test_reload_explicit(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        other_project = 'other-project-234'
        resource = {
            'jobReference': {
                'jobId': self.JOB_ID,
                'projectId': self.PROJECT,
                'location': None,
            },
            'configuration': {
                'test': True,
            }
        }
        job = self._set_properties_job()
        client = _make_client(project=other_project)
        call_api = client._call_api = mock.Mock()
        call_api.return_value = resource
        retry = DEFAULT_RETRY.with_deadline(1)

        job.reload(client=client, retry=retry)

        call_api.assert_called_once_with(
            retry,
            method='GET',
            path='/projects/{}/jobs/{}'.format(self.PROJECT, self.JOB_ID),
            query_params={},
        )
        self.assertEqual(job._properties, resource)

    def test_cancel_defaults(self):
        resource = {
            'jobReference': {
                'jobId': self.JOB_ID,
                'projectId': self.PROJECT,
                'location': None,
            },
            'configuration': {
                'test': True,
            }
        }
        response = {'job': resource}
        job = self._set_properties_job()
        job._properties['jobReference']['location'] = self.LOCATION
        connection = job._client._connection = _make_connection(response)

        self.assertTrue(job.cancel())

        connection.api_request.assert_called_once_with(
            method='POST',
            path='/projects/{}/jobs/{}/cancel'.format(
                self.PROJECT, self.JOB_ID),
            query_params={'location': self.LOCATION},
        )
        self.assertEqual(job._properties, resource)

    def test_cancel_explicit(self):
        other_project = 'other-project-234'
        resource = {
            'jobReference': {
                'jobId': self.JOB_ID,
                'projectId': self.PROJECT,
                'location': None,
            },
            'configuration': {
                'test': True,
            }
        }
        response = {'job': resource}
        job = self._set_properties_job()
        client = _make_client(project=other_project)
        connection = client._connection = _make_connection(response)

        self.assertTrue(job.cancel(client=client))

        connection.api_request.assert_called_once_with(
            method='POST',
            path='/projects/{}/jobs/{}/cancel'.format(
                self.PROJECT, self.JOB_ID),
            query_params={},
        )
        self.assertEqual(job._properties, resource)

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
        job._properties['status'] = {'state': 'DONE'}
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
        job._properties['status'] = {
            'state': 'DONE',
            'errorResult': {
                'reason': 'notFound',
                'message': 'testing'
            }
        }
        set_exception = job.set_exception = mock.Mock()
        set_result = job.set_result = mock.Mock()

        job._set_future_result()

        set_exception.assert_called_once()
        args, kw = set_exception.call_args
        exception, = args
        self.assertIsInstance(exception, NotFound)
        self.assertEqual(exception.message, 'testing')
        self.assertEqual(kw, {})
        set_result.assert_not_called()

    def test__set_future_result_w_done_wo_result_set_wo_error(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties['status'] = {'state': 'DONE'}
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

        reload_.assert_called_once_with(retry=DEFAULT_RETRY)

    def test_done_explicit_wo_state(self):
        from google.cloud.bigquery.retry import DEFAULT_RETRY

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        reload_ = job.reload = mock.Mock()
        retry = DEFAULT_RETRY.with_deadline(1)

        self.assertFalse(job.done(retry=retry))

        reload_.assert_called_once_with(retry=retry)

    def test_done_already(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties['status'] = {'state': 'DONE'}

        self.assertTrue(job.done())

    @mock.patch('google.api_core.future.polling.PollingFuture.result')
    def test_result_default_wo_state(self, result):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        begin = job._begin = mock.Mock()

        self.assertIs(job.result(), result.return_value)

        begin.assert_called_once()
        result.assert_called_once_with(timeout=None)

    @mock.patch('google.api_core.future.polling.PollingFuture.result')
    def test_result_explicit_w_state(self, result):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties['status'] = {'state': 'DONE'}
        begin = job._begin = mock.Mock()
        timeout = 1

        self.assertIs(job.result(timeout=timeout), result.return_value)

        begin.assert_not_called()
        result.assert_called_once_with(timeout=timeout)

    def test_cancelled_wo_error_result(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)

        self.assertFalse(job.cancelled())

    def test_cancelled_w_error_result_not_stopped(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties['status'] = {
            'errorResult': {
                'reason': 'other',
            }
        }

        self.assertFalse(job.cancelled())

    def test_cancelled_w_error_result_w_stopped(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, client)
        job._properties['status'] = {
            'errorResult': {
                'reason': 'stopped',
            }
        }

        self.assertTrue(job.cancelled())


class Test_JobConfig(unittest.TestCase):
    JOB_TYPE = 'testing'

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

    @mock.patch('google.cloud.bigquery._helpers._get_sub_prop')
    def test__get_sub_prop_wo_default(self, _get_sub_prop):
        job_config = self._make_one()
        key = 'key'
        self.assertIs(
            job_config._get_sub_prop(key), _get_sub_prop.return_value)
        _get_sub_prop.assert_called_once_with(
            job_config._properties, [self.JOB_TYPE, key], default=None)

    @mock.patch('google.cloud.bigquery._helpers._get_sub_prop')
    def test__get_sub_prop_w_default(self, _get_sub_prop):
        job_config = self._make_one()
        key = 'key'
        default = 'default'
        self.assertIs(
            job_config._get_sub_prop(key, default=default),
            _get_sub_prop.return_value)
        _get_sub_prop.assert_called_once_with(
            job_config._properties, [self.JOB_TYPE, key], default=default)

    @mock.patch('google.cloud.bigquery._helpers._set_sub_prop')
    def test__set_sub_prop(self, _set_sub_prop):
        job_config = self._make_one()
        key = 'key'
        value = 'value'
        job_config._set_sub_prop(key, value)
        _set_sub_prop.assert_called_once_with(
            job_config._properties, [self.JOB_TYPE, key], value)

    def test_to_api_repr(self):
        job_config = self._make_one()
        expected = job_config._properties = {
            self.JOB_TYPE: {
                'foo': 'bar',
            }
        }
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
        labels['foo'] = 'bar'  # update in place
        self.assertEqual(job_config.labels, {'foo': 'bar'})

    def test_labels_hit(self):
        labels = {
            'foo': 'bar',
        }
        job_config = self._make_one()
        job_config._properties['labels'] = labels
        self.assertEqual(job_config.labels, labels)

    def test_labels_setter_invalid(self):
        labels = object()
        job_config = self._make_one()
        with self.assertRaises(ValueError):
            job_config.labels = labels

    def test_labels_setter(self):
        labels = {
            'foo': 'bar',
        }
        job_config = self._make_one()
        job_config.labels = labels
        self.assertEqual(job_config._properties['labels'], labels)


class _Base(object):
    from google.cloud.bigquery.dataset import DatasetReference
    from google.cloud.bigquery.table import TableReference

    PROJECT = 'project'
    SOURCE1 = 'http://example.com/source1.csv'
    DS_ID = 'dataset_id'
    DS_REF = DatasetReference(PROJECT, DS_ID)
    TABLE_ID = 'table_id'
    TABLE_REF = TableReference(DS_REF, TABLE_ID)
    JOB_ID = 'JOB_ID'
    KMS_KEY_NAME = 'projects/1/locations/global/keyRings/1/cryptoKeys/1'

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _setUpConstants(self):
        import datetime
        from google.cloud._helpers import UTC

        self.WHEN_TS = 1437767599.006
        self.WHEN = datetime.datetime.utcfromtimestamp(self.WHEN_TS).replace(
            tzinfo=UTC)
        self.ETAG = 'ETAG'
        self.FULL_JOB_ID = '%s:%s' % (self.PROJECT, self.JOB_ID)
        self.RESOURCE_URL = 'http://example.com/path/to/resource'
        self.USER_EMAIL = 'phred@example.com'

    def _table_ref(self, table_id):
        from google.cloud.bigquery.table import TableReference

        return TableReference(self.DS_REF, table_id)

    def _make_resource(self, started=False, ended=False):
        self._setUpConstants()
        resource = {
            'configuration': {
                self.JOB_TYPE: {
                },
            },
            'statistics': {
                'creationTime': self.WHEN_TS * 1000,
                self.JOB_TYPE: {
                }
            },
            'etag': self.ETAG,
            'id': self.FULL_JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'selfLink': self.RESOURCE_URL,
            'user_email': self.USER_EMAIL,
        }

        if started or ended:
            resource['statistics']['startTime'] = self.WHEN_TS * 1000

        if ended:
            resource['statistics']['endTime'] = (self.WHEN_TS + 1000) * 1000

        if self.JOB_TYPE == 'query':
            resource['configuration']['query']['destinationTable'] = {
                'projectId': self.PROJECT,
                'datasetId': '_temp_dataset',
                'tableId': '_temp_table',
            }

        return resource

    def _verifyInitialReadonlyProperties(self, job):
        # root elements of resource
        self.assertIsNone(job.etag)
        self.assertIsNone(job.self_link)
        self.assertIsNone(job.user_email)

        # derived from resource['statistics']
        self.assertIsNone(job.created)
        self.assertIsNone(job.started)
        self.assertIsNone(job.ended)

        # derived from resource['status']
        self.assertIsNone(job.error_result)
        self.assertIsNone(job.errors)
        self.assertIsNone(job.state)

    def _verifyReadonlyResourceProperties(self, job, resource):
        from datetime import timedelta

        statistics = resource.get('statistics', {})

        if 'creationTime' in statistics:
            self.assertEqual(job.created, self.WHEN)
        else:
            self.assertIsNone(job.created)

        if 'startTime' in statistics:
            self.assertEqual(job.started, self.WHEN)
        else:
            self.assertIsNone(job.started)

        if 'endTime' in statistics:
            self.assertEqual(job.ended, self.WHEN + timedelta(seconds=1000))
        else:
            self.assertIsNone(job.ended)

        if 'etag' in resource:
            self.assertEqual(job.etag, self.ETAG)
        else:
            self.assertIsNone(job.etag)

        if 'selfLink' in resource:
            self.assertEqual(job.self_link, self.RESOURCE_URL)
        else:
            self.assertIsNone(job.self_link)

        if 'user_email' in resource:
            self.assertEqual(job.user_email, self.USER_EMAIL)
        else:
            self.assertIsNone(job.user_email)


class TestLoadJobConfig(unittest.TestCase, _Base):
    JOB_TYPE = 'load'

    def _make_resource(self, started=False, ended=False):
        resource = super(TestLoadJobConfig, self)._make_resource(
            started, ended)
        config = resource['configuration']['load']
        config['sourceUris'] = [self.SOURCE1]
        config['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_ID,
            'tableId': self.TABLE_ID,
        }
        config['destinationEncryptionConfiguration'] = {
            'kmsKeyName': self.KMS_KEY_NAME}

        return resource

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import LoadJobConfig
        return LoadJobConfig

    def test_schema(self):
        from google.cloud.bigquery.schema import SchemaField
        config = self._get_target_class()()
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        config.schema = [full_name, age]
        self.assertEqual(config.schema, [full_name, age])

    def test_time_partitioning(self):
        from google.cloud.bigquery import table

        time_partitioning = table.TimePartitioning(
            type_=table.TimePartitioningType.DAY, field='name')
        config = self._get_target_class()()
        config.time_partitioning = time_partitioning
        # TimePartitioning should be configurable after assigning
        time_partitioning.expiration_ms = 10000
        self.assertEqual(
            config.time_partitioning.type_,
            table.TimePartitioningType.DAY)
        self.assertEqual(config.time_partitioning.field, 'name')
        self.assertEqual(config.time_partitioning.expiration_ms, 10000)

        config.time_partitioning = None
        self.assertIsNone(config.time_partitioning)

    def test_clustering_fields(self):
        fields = ['email', 'postal_code']
        config = self._get_target_class()()
        config.clustering_fields = fields
        self.assertEqual(config.clustering_fields, fields)

        config.clustering_fields = None
        self.assertIsNone(config.clustering_fields)

    def test_api_repr(self):
        resource = self._make_resource()
        config = self._get_target_class().from_api_repr(resource)
        self.assertEqual(config.to_api_repr(), resource)

    def test_to_api_repr_with_encryption(self):
        from google.cloud.bigquery.table import EncryptionConfiguration

        config = self._make_one()
        config.destination_encryption_configuration = EncryptionConfiguration(
            kms_key_name=self.KMS_KEY_NAME)
        resource = config.to_api_repr()
        self.assertEqual(
            resource,
            {
                'load': {
                    'destinationEncryptionConfiguration': {
                        'kmsKeyName': self.KMS_KEY_NAME,
                    },
                },
            })

    def test_to_api_repr_with_encryption_none(self):
        config = self._make_one()
        config.destination_encryption_configuration = None
        resource = config.to_api_repr()
        self.assertEqual(
            resource,
            {
                'load': {
                    'destinationEncryptionConfiguration': None,
                },
            })


class TestLoadJob(unittest.TestCase, _Base):
    JOB_TYPE = 'load'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import LoadJob

        return LoadJob

    def _setUpConstants(self):
        super(TestLoadJob, self)._setUpConstants()
        self.INPUT_FILES = 2
        self.INPUT_BYTES = 12345
        self.OUTPUT_BYTES = 23456
        self.OUTPUT_ROWS = 345

    def _make_resource(self, started=False, ended=False):
        resource = super(TestLoadJob, self)._make_resource(
            started, ended)
        config = resource['configuration']['load']
        config['sourceUris'] = [self.SOURCE1]
        config['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_ID,
            'tableId': self.TABLE_ID,
        }

        if ended:
            resource['status'] = {'state': 'DONE'}
            resource['statistics']['load']['inputFiles'] = self.INPUT_FILES
            resource['statistics']['load']['inputFileBytes'] = self.INPUT_BYTES
            resource['statistics']['load']['outputBytes'] = self.OUTPUT_BYTES
            resource['statistics']['load']['outputRows'] = self.OUTPUT_ROWS

        return resource

    def _verifyBooleanConfigProperties(self, job, config):
        if 'allowJaggedRows' in config:
            self.assertEqual(job.allow_jagged_rows,
                             config['allowJaggedRows'])
        else:
            self.assertIsNone(job.allow_jagged_rows)
        if 'allowQuotedNewlines' in config:
            self.assertEqual(job.allow_quoted_newlines,
                             config['allowQuotedNewlines'])
        else:
            self.assertIsNone(job.allow_quoted_newlines)
        if 'autodetect' in config:
            self.assertEqual(
                job.autodetect, config['autodetect'])
        else:
            self.assertIsNone(job.autodetect)
        if 'ignoreUnknownValues' in config:
            self.assertEqual(job.ignore_unknown_values,
                             config['ignoreUnknownValues'])
        else:
            self.assertIsNone(job.ignore_unknown_values)

    def _verifyEnumConfigProperties(self, job, config):
        if 'createDisposition' in config:
            self.assertEqual(job.create_disposition,
                             config['createDisposition'])
        else:
            self.assertIsNone(job.create_disposition)
        if 'encoding' in config:
            self.assertEqual(job.encoding,
                             config['encoding'])
        else:
            self.assertIsNone(job.encoding)
        if 'sourceFormat' in config:
            self.assertEqual(job.source_format,
                             config['sourceFormat'])
        else:
            self.assertIsNone(job.source_format)
        if 'writeDisposition' in config:
            self.assertEqual(job.write_disposition,
                             config['writeDisposition'])
        else:
            self.assertIsNone(job.write_disposition)
        if 'schemaUpdateOptions' in config:
            self.assertEqual(
                job.schema_update_options, config['schemaUpdateOptions'])
        else:
            self.assertIsNone(job.schema_update_options)

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)

        config = resource.get('configuration', {}).get('load')

        self._verifyBooleanConfigProperties(job, config)
        self._verifyEnumConfigProperties(job, config)

        self.assertEqual(job.source_uris, config['sourceUris'])

        table_ref = config['destinationTable']
        self.assertEqual(job.destination.project, table_ref['projectId'])
        self.assertEqual(job.destination.dataset_id, table_ref['datasetId'])
        self.assertEqual(job.destination.table_id, table_ref['tableId'])

        if 'fieldDelimiter' in config:
            self.assertEqual(job.field_delimiter,
                             config['fieldDelimiter'])
        else:
            self.assertIsNone(job.field_delimiter)
        if 'maxBadRecords' in config:
            self.assertEqual(job.max_bad_records,
                             config['maxBadRecords'])
        else:
            self.assertIsNone(job.max_bad_records)
        if 'nullMarker' in config:
            self.assertEqual(job.null_marker,
                             config['nullMarker'])
        else:
            self.assertIsNone(job.null_marker)
        if 'quote' in config:
            self.assertEqual(job.quote_character,
                             config['quote'])
        else:
            self.assertIsNone(job.quote_character)
        if 'skipLeadingRows' in config:
            self.assertEqual(str(job.skip_leading_rows),
                             config['skipLeadingRows'])
        else:
            self.assertIsNone(job.skip_leading_rows)

        if 'destinationEncryptionConfiguration' in config:
            self.assertIsNotNone(job.destination_encryption_configuration)
            self.assertEqual(
                job.destination_encryption_configuration.kms_key_name,
                config['destinationEncryptionConfiguration']['kmsKeyName'])
        else:
            self.assertIsNone(job.destination_encryption_configuration)

    def test_ctor(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client)
        self.assertIs(job.destination, self.TABLE_REF)
        self.assertEqual(list(job.source_uris), [self.SOURCE1])
        self.assertIs(job._client, client)
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID))

        self._verifyInitialReadonlyProperties(job)

        # derived from resource['statistics']['load']
        self.assertIsNone(job.input_file_bytes)
        self.assertIsNone(job.input_files)
        self.assertIsNone(job.output_bytes)
        self.assertIsNone(job.output_rows)

        # set/read from resource['configuration']['load']
        self.assertIsNone(job.schema)
        self.assertIsNone(job.allow_jagged_rows)
        self.assertIsNone(job.allow_quoted_newlines)
        self.assertIsNone(job.autodetect)
        self.assertIsNone(job.create_disposition)
        self.assertIsNone(job.encoding)
        self.assertIsNone(job.field_delimiter)
        self.assertIsNone(job.ignore_unknown_values)
        self.assertIsNone(job.max_bad_records)
        self.assertIsNone(job.null_marker)
        self.assertIsNone(job.quote_character)
        self.assertIsNone(job.skip_leading_rows)
        self.assertIsNone(job.source_format)
        self.assertIsNone(job.write_disposition)
        self.assertIsNone(job.destination_encryption_configuration)
        self.assertIsNone(job.time_partitioning)
        self.assertIsNone(job.clustering_fields)
        self.assertIsNone(job.schema_update_options)

    def test_ctor_w_config(self):
        from google.cloud.bigquery.schema import SchemaField
        from google.cloud.bigquery.job import LoadJobConfig

        client = _make_client(project=self.PROJECT)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        config = LoadJobConfig()
        config.schema = [full_name, age]
        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client, config)
        self.assertEqual(job.schema, [full_name, age])

    def test_ctor_w_job_reference(self):
        from google.cloud.bigquery import job

        client = _make_client(project=self.PROJECT)
        job_ref = job._JobReference(self.JOB_ID, 'alternative-project', 'US')
        load_job = self._make_one(
            job_ref, [self.SOURCE1], self.TABLE_REF, client)
        self.assertEqual(load_job.project, 'alternative-project')
        self.assertEqual(load_job.location, 'US')

    def test_done(self):
        client = _make_client(project=self.PROJECT)
        resource = self._make_resource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)
        self.assertTrue(job.done())

    def test_result(self):
        client = _make_client(project=self.PROJECT)
        resource = self._make_resource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)

        result = job.result()

        self.assertIs(result, job)

    def test_result_invokes_begin(self):
        begun_resource = self._make_resource()
        done_resource = copy.deepcopy(begun_resource)
        done_resource['status'] = {'state': 'DONE'}
        connection = _make_connection(begun_resource, done_resource)
        client = _make_client(self.PROJECT)
        client._connection = connection

        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client)
        job.result()

        self.assertEqual(len(connection.api_request.call_args_list), 2)
        begin_request, reload_request = connection.api_request.call_args_list
        self.assertEqual(begin_request[1]['method'], 'POST')
        self.assertEqual(reload_request[1]['method'], 'GET')

    def test_schema_setter_non_list(self):
        from google.cloud.bigquery.job import LoadJobConfig

        config = LoadJobConfig()
        with self.assertRaises(TypeError):
            config.schema = object()

    def test_schema_setter_invalid_field(self):
        from google.cloud.bigquery.job import LoadJobConfig
        from google.cloud.bigquery.schema import SchemaField

        config = LoadJobConfig()
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        with self.assertRaises(ValueError):
            config.schema = [full_name, object()]

    def test_schema_setter(self):
        from google.cloud.bigquery.job import LoadJobConfig
        from google.cloud.bigquery.schema import SchemaField

        config = LoadJobConfig()
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        config.schema = [full_name, age]
        self.assertEqual(config.schema, [full_name, age])

    def test_props_set_by_server(self):
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _millis

        CREATED = datetime.datetime(2015, 8, 11, 12, 13, 22, tzinfo=UTC)
        STARTED = datetime.datetime(2015, 8, 11, 13, 47, 15, tzinfo=UTC)
        ENDED = datetime.datetime(2015, 8, 11, 14, 47, 15, tzinfo=UTC)
        FULL_JOB_ID = '%s:%s' % (self.PROJECT, self.JOB_ID)
        URL = 'http://example.com/projects/%s/jobs/%s' % (
            self.PROJECT, self.JOB_ID)
        EMAIL = 'phred@example.com'
        ERROR_RESULT = {'debugInfo': 'DEBUG',
                        'location': 'LOCATION',
                        'message': 'MESSAGE',
                        'reason': 'REASON'}

        client = _make_client(project=self.PROJECT)
        job = self._make_one(
            self.JOB_ID, [self.SOURCE1], self.TABLE_REF, client)
        job._properties['etag'] = 'ETAG'
        job._properties['id'] = FULL_JOB_ID
        job._properties['selfLink'] = URL
        job._properties['user_email'] = EMAIL

        statistics = job._properties['statistics'] = {}
        statistics['creationTime'] = _millis(CREATED)
        statistics['startTime'] = _millis(STARTED)
        statistics['endTime'] = _millis(ENDED)
        load_stats = statistics['load'] = {}
        load_stats['inputFileBytes'] = 12345
        load_stats['inputFiles'] = 1
        load_stats['outputBytes'] = 23456
        load_stats['outputRows'] = 345

        self.assertEqual(job.etag, 'ETAG')
        self.assertEqual(job.self_link, URL)
        self.assertEqual(job.user_email, EMAIL)

        self.assertEqual(job.created, CREATED)
        self.assertEqual(job.started, STARTED)
        self.assertEqual(job.ended, ENDED)

        self.assertEqual(job.input_file_bytes, 12345)
        self.assertEqual(job.input_files, 1)
        self.assertEqual(job.output_bytes, 23456)
        self.assertEqual(job.output_rows, 345)

        status = job._properties['status'] = {}

        self.assertIsNone(job.error_result)
        self.assertIsNone(job.errors)
        self.assertIsNone(job.state)

        status['errorResult'] = ERROR_RESULT
        status['errors'] = [ERROR_RESULT]
        status['state'] = 'STATE'

        self.assertEqual(job.error_result, ERROR_RESULT)
        self.assertEqual(job.errors, [ERROR_RESULT])
        self.assertEqual(job.state, 'STATE')

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_missing_config(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.JOB_ID),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            }
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.FULL_JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'load': {
                    'sourceUris': [self.SOURCE1],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.TABLE_ID,
                    },
                }
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_with_encryption(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.FULL_JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'load': {
                    'sourceUris': [self.SOURCE1],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.TABLE_ID,
                    },
                    'destinationEncryptionConfiguration': {
                        'kmsKeyName': self.KMS_KEY_NAME
                    }
                }
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_properties(self):
        from google.cloud.bigquery.job import CreateDisposition

        client = _make_client(project=self.PROJECT)
        RESOURCE = self._make_resource()
        load_config = RESOURCE['configuration']['load']
        load_config['createDisposition'] = CreateDisposition.CREATE_IF_NEEDED
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_already_running(self):
        conn = _make_connection()
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client)
        job._properties['status'] = {'state': 'RUNNING'}

        with self.assertRaises(ValueError):
            job._begin()

    def test_begin_w_bound_client(self):
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        conn = _make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client)

        job._begin()

        conn.api_request.assert_called_once_with(
            method='POST',
            path='/projects/{}/jobs'.format(self.PROJECT),
            data={
                'jobReference': {
                    'projectId': self.PROJECT,
                    'jobId': self.JOB_ID,
                },
                'configuration': {
                    'load': {
                        'sourceUris': [self.SOURCE1],
                        'destinationTable': {
                            'projectId': self.PROJECT,
                            'datasetId': self.DS_ID,
                            'tableId': self.TABLE_ID,
                        },
                    },
                },
            })
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_autodetect(self):
        from google.cloud.bigquery.job import LoadJobConfig

        path = '/projects/{}/jobs'.format(self.PROJECT)
        resource = self._make_resource()
        resource['configuration']['load']['autodetect'] = True
        # Ensure None for missing server-set props
        del resource['statistics']['creationTime']
        del resource['etag']
        del resource['selfLink']
        del resource['user_email']
        conn = _make_connection(resource)
        client = _make_client(project=self.PROJECT, connection=conn)
        config = LoadJobConfig()
        config.autodetect = True
        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client, config)
        job._begin()

        sent = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'load': {
                    'sourceUris': [self.SOURCE1],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.TABLE_ID,
                    },
                    'autodetect': True
                },
            },
        }
        conn.api_request.assert_called_once_with(
            method='POST',
            path=path,
            data=sent)
        self._verifyResourceProperties(job, resource)

    def test_begin_w_alternate_client(self):
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import LoadJobConfig
        from google.cloud.bigquery.job import SchemaUpdateOption
        from google.cloud.bigquery.job import WriteDisposition
        from google.cloud.bigquery.schema import SchemaField

        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._make_resource(ended=True)
        LOAD_CONFIGURATION = {
            'sourceUris': [self.SOURCE1],
            'destinationTable': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.TABLE_ID,
            },
            'allowJaggedRows': True,
            'allowQuotedNewlines': True,
            'createDisposition': CreateDisposition.CREATE_NEVER,
            'encoding': 'ISO-8559-1',
            'fieldDelimiter': '|',
            'ignoreUnknownValues': True,
            'maxBadRecords': 100,
            'nullMarker': r'\N',
            'quote': "'",
            'skipLeadingRows': '1',
            'sourceFormat': 'CSV',
            'writeDisposition': WriteDisposition.WRITE_TRUNCATE,
            'schema': {'fields': [
                {
                    'name': 'full_name',
                    'type': 'STRING',
                    'mode': 'REQUIRED',
                    'description': None,
                },
                {
                    'name': 'age',
                    'type': 'INTEGER',
                    'mode': 'REQUIRED',
                    'description': None,
                },
            ]},
            'schemaUpdateOptions': [
                SchemaUpdateOption.ALLOW_FIELD_ADDITION,
            ],
        }
        RESOURCE['configuration']['load'] = LOAD_CONFIGURATION
        conn1 = _make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _make_connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        config = LoadJobConfig()
        config.schema = [full_name, age]
        job = self._make_one(self.JOB_ID, [self.SOURCE1], self.TABLE_REF,
                             client1, config)
        config.allow_jagged_rows = True
        config.allow_quoted_newlines = True
        config.create_disposition = CreateDisposition.CREATE_NEVER
        config.encoding = 'ISO-8559-1'
        config.field_delimiter = '|'
        config.ignore_unknown_values = True
        config.max_bad_records = 100
        config.null_marker = r'\N'
        config.quote_character = "'"
        config.skip_leading_rows = 1
        config.source_format = 'CSV'
        config.write_disposition = WriteDisposition.WRITE_TRUNCATE
        config.schema_update_options = [
            SchemaUpdateOption.ALLOW_FIELD_ADDITION,
        ]

        job._begin(client=client2)

        conn1.api_request.assert_not_called()
        self.assertEqual(len(conn2.api_request.call_args_list), 1)
        req = conn2.api_request.call_args_list[0]
        self.assertEqual(req[1]['method'], 'POST')
        self.assertEqual(req[1]['path'], PATH)
        SENT = {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'load': LOAD_CONFIGURATION,
            },
        }
        self.maxDiff = None
        self.assertEqual(req[1]['data'], SENT)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_job_reference(self):
        from google.cloud.bigquery import job

        resource = self._make_resource()
        resource['jobReference']['projectId'] = 'alternative-project'
        resource['jobReference']['location'] = 'US'
        job_ref = job._JobReference(self.JOB_ID, 'alternative-project', 'US')
        conn = _make_connection(resource)
        client = _make_client(project=self.PROJECT, connection=conn)
        load_job = self._make_one(
            job_ref, [self.SOURCE1], self.TABLE_REF, client)

        load_job._begin()

        conn.api_request.assert_called_once()
        _, request = conn.api_request.call_args
        self.assertEqual(request['method'], 'POST')
        self.assertEqual(
            request['path'], '/projects/alternative-project/jobs')
        self.assertEqual(
            request['data']['jobReference']['projectId'],
            'alternative-project')
        self.assertEqual(request['data']['jobReference']['location'], 'US')
        self.assertEqual(request['data']['jobReference']['jobId'], self.JOB_ID)

    def test_exists_miss_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn = _make_connection()
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(
            self.JOB_ID, [self.SOURCE1], self.TABLE_REF, client)

        self.assertFalse(job.exists())

        conn.api_request.assert_called_once_with(
            method='GET',
            path=PATH,
            query_params={'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn1 = _make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _make_connection({})
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        job = self._make_one(
            self.JOB_ID, [self.SOURCE1], self.TABLE_REF, client1)

        self.assertTrue(job.exists(client=client2))

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method='GET',
            path=PATH,
            query_params={'fields': 'id'})

    def test_exists_miss_w_job_reference(self):
        from google.cloud.bigquery import job

        job_ref = job._JobReference('my-job-id', 'other-project', 'US')
        conn = _make_connection()
        client = _make_client(project=self.PROJECT, connection=conn)
        load_job = self._make_one(
            job_ref, [self.SOURCE1], self.TABLE_REF, client)

        self.assertFalse(load_job.exists())

        conn.api_request.assert_called_once_with(
            method='GET',
            path='/projects/other-project/jobs/my-job-id',
            query_params={'fields': 'id', 'location': 'US'})

    def test_reload_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._make_resource()
        conn = _make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(
            self.JOB_ID, [self.SOURCE1], self.TABLE_REF, client)

        job.reload()

        conn.api_request.assert_called_once_with(
            method='GET',
            path=PATH,
            query_params={})
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._make_resource()
        conn1 = _make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _make_connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        job = self._make_one(
            self.JOB_ID, [self.SOURCE1], self.TABLE_REF, client1)

        job.reload(client=client2)

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method='GET',
            path=PATH,
            query_params={})
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_job_reference(self):
        from google.cloud.bigquery import job

        resource = self._make_resource(ended=True)
        resource['jobReference']['projectId'] = 'alternative-project'
        resource['jobReference']['location'] = 'US'
        job_ref = job._JobReference(self.JOB_ID, 'alternative-project', 'US')
        conn = _make_connection(resource)
        client = _make_client(project=self.PROJECT, connection=conn)
        load_job = self._make_one(
            job_ref, [self.SOURCE1], self.TABLE_REF, client)

        load_job.reload()

        conn.api_request.assert_called_once_with(
            method='GET',
            path='/projects/alternative-project/jobs/{}'.format(
                self.JOB_ID),
            query_params={'location': 'US'})

    def test_cancel_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s/cancel' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._make_resource(ended=True)
        RESPONSE = {'job': RESOURCE}
        conn = _make_connection(RESPONSE)
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(
            self.JOB_ID, [self.SOURCE1], self.TABLE_REF, client)

        job.cancel()

        conn.api_request.assert_called_once_with(
            method='POST',
            path=PATH,
            query_params={})
        self._verifyResourceProperties(job, RESOURCE)

    def test_cancel_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s/cancel' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._make_resource(ended=True)
        RESPONSE = {'job': RESOURCE}
        conn1 = _make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _make_connection(RESPONSE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        job = self._make_one(
            self.JOB_ID, [self.SOURCE1], self.TABLE_REF, client1)

        job.cancel(client=client2)

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method='POST',
            path=PATH,
            query_params={})
        self._verifyResourceProperties(job, RESOURCE)

    def test_cancel_w_job_reference(self):
        from google.cloud.bigquery import job

        resource = self._make_resource(ended=True)
        resource['jobReference']['projectId'] = 'alternative-project'
        resource['jobReference']['location'] = 'US'
        job_ref = job._JobReference(self.JOB_ID, 'alternative-project', 'US')
        conn = _make_connection({'job': resource})
        client = _make_client(project=self.PROJECT, connection=conn)
        load_job = self._make_one(
            job_ref, [self.SOURCE1], self.TABLE_REF, client)

        load_job.cancel()

        conn.api_request.assert_called_once_with(
            method='POST',
            path='/projects/alternative-project/jobs/{}/cancel'.format(
                self.JOB_ID),
            query_params={'location': 'US'})


class TestCopyJobConfig(unittest.TestCase, _Base):
    JOB_TYPE = 'copy'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import CopyJobConfig
        return CopyJobConfig

    def test_to_api_repr_with_encryption(self):
        from google.cloud.bigquery.table import EncryptionConfiguration

        config = self._make_one()
        config.destination_encryption_configuration = EncryptionConfiguration(
            kms_key_name=self.KMS_KEY_NAME)
        resource = config.to_api_repr()
        self.assertEqual(
            resource,
            {
                'copy': {
                    'destinationEncryptionConfiguration': {
                        'kmsKeyName': self.KMS_KEY_NAME,
                    },
                },
            })

    def test_to_api_repr_with_encryption_none(self):
        config = self._make_one()
        config.destination_encryption_configuration = None
        resource = config.to_api_repr()
        self.assertEqual(
            resource,
            {
                'copy': {
                    'destinationEncryptionConfiguration': None,
                },
            })


class TestCopyJob(unittest.TestCase, _Base):
    JOB_TYPE = 'copy'
    SOURCE_TABLE = 'source_table'
    DESTINATION_TABLE = 'destination_table'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import CopyJob

        return CopyJob

    def _make_resource(self, started=False, ended=False):
        resource = super(TestCopyJob, self)._make_resource(
            started, ended)
        config = resource['configuration']['copy']
        config['sourceTables'] = [{
            'projectId': self.PROJECT,
            'datasetId': self.DS_ID,
            'tableId': self.SOURCE_TABLE,
        }]
        config['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_ID,
            'tableId': self.DESTINATION_TABLE,
        }

        return resource

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)

        config = resource.get('configuration', {}).get('copy')

        table_ref = config['destinationTable']
        self.assertEqual(job.destination.project, table_ref['projectId'])
        self.assertEqual(job.destination.dataset_id, table_ref['datasetId'])
        self.assertEqual(job.destination.table_id, table_ref['tableId'])

        sources = config.get('sourceTables')
        if sources is None:
            sources = [config['sourceTable']]
        self.assertEqual(len(sources), len(job.sources))
        for table_ref, table in zip(sources, job.sources):
            self.assertEqual(table.project, table_ref['projectId'])
            self.assertEqual(table.dataset_id, table_ref['datasetId'])
            self.assertEqual(table.table_id, table_ref['tableId'])

        if 'createDisposition' in config:
            self.assertEqual(job.create_disposition,
                             config['createDisposition'])
        else:
            self.assertIsNone(job.create_disposition)

        if 'writeDisposition' in config:
            self.assertEqual(job.write_disposition,
                             config['writeDisposition'])
        else:
            self.assertIsNone(job.write_disposition)

        if 'destinationEncryptionConfiguration' in config:
            self.assertIsNotNone(job.destination_encryption_configuration)
            self.assertEqual(
                job.destination_encryption_configuration.kms_key_name,
                config['destinationEncryptionConfiguration']['kmsKeyName'])
        else:
            self.assertIsNone(job.destination_encryption_configuration)

    def test_ctor(self):
        client = _make_client(project=self.PROJECT)
        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_ID, [source], destination, client)
        self.assertIs(job.destination, destination)
        self.assertEqual(job.sources, [source])
        self.assertIs(job._client, client)
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID))

        self._verifyInitialReadonlyProperties(job)

        # set/read from resource['configuration']['copy']
        self.assertIsNone(job.create_disposition)
        self.assertIsNone(job.write_disposition)
        self.assertIsNone(job.destination_encryption_configuration)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_missing_config(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.DS_ID),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            }
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'copy': {
                    'sourceTables': [{
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.SOURCE_TABLE,
                    }],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.DESTINATION_TABLE,
                    },
                }
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_with_encryption(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'copy': {
                    'sourceTables': [{
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.SOURCE_TABLE,
                    }],
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.DESTINATION_TABLE,
                    },
                    'destinationEncryptionConfiguration': {
                        'kmsKeyName': self.KMS_KEY_NAME
                    }
                }
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_sourcetable(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'copy': {
                    'sourceTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.SOURCE_TABLE,
                    },
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.DESTINATION_TABLE,
                    },
                }
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_wo_sources(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'copy': {
                    'destinationTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.DESTINATION_TABLE,
                    },
                }
            },
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_w_properties(self):
        from google.cloud.bigquery.job import CreateDisposition
        client = _make_client(project=self.PROJECT)
        RESOURCE = self._make_resource()
        copy_config = RESOURCE['configuration']['copy']
        copy_config['createDisposition'] = CreateDisposition.CREATE_IF_NEEDED
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_bound_client(self):
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        conn = _make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_ID, [source], destination, client)

        job._begin()

        conn.api_request.assert_called_once_with(
            method='POST',
            path=PATH,
            data={
                'jobReference': {
                    'projectId': self.PROJECT,
                    'jobId': self.JOB_ID,
                },
                'configuration': {
                    'copy': {
                        'sourceTables': [{
                            'projectId': self.PROJECT,
                            'datasetId': self.DS_ID,
                            'tableId': self.SOURCE_TABLE
                        }],
                        'destinationTable': {
                            'projectId': self.PROJECT,
                            'datasetId': self.DS_ID,
                            'tableId': self.DESTINATION_TABLE,
                        },
                    },
                },
            })
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_alternate_client(self):
        from google.cloud.bigquery.job import CopyJobConfig

        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import WriteDisposition
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._make_resource(ended=True)
        COPY_CONFIGURATION = {
            'sourceTables': [{
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.SOURCE_TABLE,
            }],
            'destinationTable': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.DESTINATION_TABLE,
            },
            'createDisposition': CreateDisposition.CREATE_NEVER,
            'writeDisposition': WriteDisposition.WRITE_TRUNCATE,
        }
        RESOURCE['configuration']['copy'] = COPY_CONFIGURATION
        conn1 = _make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _make_connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        config = CopyJobConfig()
        config.create_disposition = CreateDisposition.CREATE_NEVER
        config.write_disposition = WriteDisposition.WRITE_TRUNCATE
        job = self._make_one(self.JOB_ID, [source], destination, client1,
                             config)
        job._begin(client=client2)

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method='POST',
            path=PATH,
            data={
                'jobReference': {
                    'projectId': self.PROJECT,
                    'jobId': self.JOB_ID,
                },
                'configuration': {
                    'copy': COPY_CONFIGURATION,
                },
            })
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn = _make_connection()
        client = _make_client(project=self.PROJECT, connection=conn)

        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_ID, [source], destination, client)

        self.assertFalse(job.exists())

        conn.api_request.assert_called_once_with(
            method='GET',
            path=PATH,
            query_params={'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn1 = _make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _make_connection({})
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_ID, [source], destination, client1)

        self.assertTrue(job.exists(client=client2))

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method='GET',
            path=PATH,
            query_params={'fields': 'id'})

    def test_reload_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._make_resource()
        conn = _make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_ID, [source], destination, client)

        job.reload()

        conn.api_request.assert_called_once_with(
            method='GET',
            path=PATH,
            query_params={})
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._make_resource()
        conn1 = _make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _make_connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        source = self._table_ref(self.SOURCE_TABLE)
        destination = self._table_ref(self.DESTINATION_TABLE)
        job = self._make_one(self.JOB_ID, [source], destination, client1)

        job.reload(client=client2)

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method='GET',
            path=PATH,
            query_params={})
        self._verifyResourceProperties(job, RESOURCE)


class TestExtractJobConfig(unittest.TestCase, _Base):
    JOB_TYPE = 'extract'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import ExtractJobConfig
        return ExtractJobConfig

    def test_to_api_repr(self):
        from google.cloud.bigquery import job
        config = self._make_one()
        config.compression = job.Compression.SNAPPY
        config.destination_format = job.DestinationFormat.AVRO
        config.field_delimiter = 'ignored for avro'
        config.print_header = False
        config._properties['extract']['someNewField'] = 'some-value'
        resource = config.to_api_repr()
        self.assertEqual(
            resource,
            {
                'extract': {
                    'compression': 'SNAPPY',
                    'destinationFormat': 'AVRO',
                    'fieldDelimiter': 'ignored for avro',
                    'printHeader': False,
                    'someNewField': 'some-value',
                },
            })

    def test_from_api_repr(self):
        cls = self._get_target_class()
        config = cls.from_api_repr(
            {
                'extract': {
                    'compression': 'NONE',
                    'destinationFormat': 'CSV',
                    'fieldDelimiter': '\t',
                    'printHeader': True,
                    'someNewField': 'some-value',
                },
            })
        self.assertEqual(config.compression, 'NONE')
        self.assertEqual(config.destination_format, 'CSV')
        self.assertEqual(config.field_delimiter, '\t')
        self.assertEqual(config.print_header, True)
        self.assertEqual(
            config._properties['extract']['someNewField'], 'some-value')


class TestExtractJob(unittest.TestCase, _Base):
    JOB_TYPE = 'extract'
    SOURCE_TABLE = 'source_table'
    DESTINATION_URI = 'gs://bucket_name/object_name'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import ExtractJob

        return ExtractJob

    def _make_resource(self, started=False, ended=False):
        resource = super(TestExtractJob, self)._make_resource(
            started, ended)
        config = resource['configuration']['extract']
        config['sourceTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_ID,
            'tableId': self.SOURCE_TABLE,
        }
        config['destinationUris'] = [self.DESTINATION_URI]
        return resource

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)

        config = resource.get('configuration', {}).get('extract')

        self.assertEqual(job.destination_uris, config['destinationUris'])

        table_ref = config['sourceTable']
        self.assertEqual(job.source.project, table_ref['projectId'])
        self.assertEqual(job.source.dataset_id, table_ref['datasetId'])
        self.assertEqual(job.source.table_id, table_ref['tableId'])

        if 'compression' in config:
            self.assertEqual(
                job.compression, config['compression'])
        else:
            self.assertIsNone(job.compression)

        if 'destinationFormat' in config:
            self.assertEqual(
                job.destination_format, config['destinationFormat'])
        else:
            self.assertIsNone(job.destination_format)

        if 'fieldDelimiter' in config:
            self.assertEqual(
                job.field_delimiter, config['fieldDelimiter'])
        else:
            self.assertIsNone(job.field_delimiter)

        if 'printHeader' in config:
            self.assertEqual(
                job.print_header, config['printHeader'])
        else:
            self.assertIsNone(job.print_header)

    def test_ctor(self):
        from google.cloud.bigquery.table import Table

        client = _make_client(project=self.PROJECT)
        source = Table(self.TABLE_REF)
        job = self._make_one(
            self.JOB_ID, source, [self.DESTINATION_URI], client)
        self.assertEqual(job.source.project, self.PROJECT)
        self.assertEqual(job.source.dataset_id, self.DS_ID)
        self.assertEqual(job.source.table_id, self.TABLE_ID)
        self.assertEqual(job.destination_uris, [self.DESTINATION_URI])
        self.assertIs(job._client, client)
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID))

        self._verifyInitialReadonlyProperties(job)

        # set/read from resource['configuration']['extract']
        self.assertIsNone(job.compression)
        self.assertIsNone(job.destination_format)
        self.assertIsNone(job.field_delimiter)
        self.assertIsNone(job.print_header)

    def test_destination_uri_file_counts(self):
        file_counts = 23
        client = _make_client(project=self.PROJECT)
        job = self._make_one(
            self.JOB_ID, self.TABLE_REF, [self.DESTINATION_URI], client)
        self.assertIsNone(job.destination_uri_file_counts)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.destination_uri_file_counts)

        extract_stats = statistics['extract'] = {}
        self.assertIsNone(job.destination_uri_file_counts)

        extract_stats['destinationUriFileCounts'] = [str(file_counts)]
        self.assertEqual(job.destination_uri_file_counts, [file_counts])

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_missing_config(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.DS_ID),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            }
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'extract': {
                    'sourceTable': {
                        'projectId': self.PROJECT,
                        'datasetId': self.DS_ID,
                        'tableId': self.SOURCE_TABLE,
                    },
                    'destinationUris': [self.DESTINATION_URI],
                }
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_properties(self):
        from google.cloud.bigquery.job import Compression
        client = _make_client(project=self.PROJECT)
        RESOURCE = self._make_resource()
        extract_config = RESOURCE['configuration']['extract']
        extract_config['compression'] = Compression.GZIP
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_bound_client(self):
        from google.cloud.bigquery.dataset import DatasetReference

        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        conn = _make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        source_dataset = DatasetReference(self.PROJECT, self.DS_ID)
        source = source_dataset.table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_ID, source, [self.DESTINATION_URI],
                             client)

        job._begin()

        conn.api_request.assert_called_once_with(
            method='POST',
            path=PATH,
            data={
                'jobReference': {
                    'projectId': self.PROJECT,
                    'jobId': self.JOB_ID,
                },
                'configuration': {
                    'extract': {
                        'sourceTable': {
                            'projectId': self.PROJECT,
                            'datasetId': self.DS_ID,
                            'tableId': self.SOURCE_TABLE
                        },
                        'destinationUris': [self.DESTINATION_URI],
                    },
                },
            })
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_alternate_client(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.job import Compression
        from google.cloud.bigquery.job import DestinationFormat
        from google.cloud.bigquery.job import ExtractJobConfig

        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._make_resource(ended=True)
        EXTRACT_CONFIGURATION = {
            'sourceTable': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
                'tableId': self.SOURCE_TABLE,
            },
            'destinationUris': [self.DESTINATION_URI],
            'compression': Compression.GZIP,
            'destinationFormat': DestinationFormat.NEWLINE_DELIMITED_JSON,
            'fieldDelimiter': '|',
            'printHeader': False,
        }
        RESOURCE['configuration']['extract'] = EXTRACT_CONFIGURATION
        conn1 = _make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _make_connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        source_dataset = DatasetReference(self.PROJECT, self.DS_ID)
        source = source_dataset.table(self.SOURCE_TABLE)
        config = ExtractJobConfig()
        config.compression = Compression.GZIP
        config.destination_format = DestinationFormat.NEWLINE_DELIMITED_JSON
        config.field_delimiter = '|'
        config.print_header = False
        job = self._make_one(self.JOB_ID, source, [self.DESTINATION_URI],
                             client1, config)

        job._begin(client=client2)

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method='POST',
            path=PATH,
            data={
                'jobReference': {
                    'projectId': self.PROJECT,
                    'jobId': self.JOB_ID,
                },
                'configuration': {
                    'extract': EXTRACT_CONFIGURATION,
                },
            })
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn = _make_connection()
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(
            self.JOB_ID, self.TABLE_REF, [self.DESTINATION_URI], client)

        self.assertFalse(job.exists())

        conn.api_request.assert_called_once_with(
            method='GET',
            path=PATH,
            query_params={'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn1 = _make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _make_connection({})
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        job = self._make_one(
            self.JOB_ID, self.TABLE_REF, [self.DESTINATION_URI], client1)

        self.assertTrue(job.exists(client=client2))

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method='GET',
            path=PATH,
            query_params={'fields': 'id'})

    def test_reload_w_bound_client(self):
        from google.cloud.bigquery.dataset import DatasetReference

        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._make_resource()
        conn = _make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        source_dataset = DatasetReference(self.PROJECT, self.DS_ID)
        source = source_dataset.table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_ID, source, [self.DESTINATION_URI],
                             client)

        job.reload()

        conn.api_request.assert_called_once_with(
            method='GET', path=PATH, query_params={})
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        from google.cloud.bigquery.dataset import DatasetReference

        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        RESOURCE = self._make_resource()
        conn1 = _make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _make_connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        source_dataset = DatasetReference(self.PROJECT, self.DS_ID)
        source = source_dataset.table(self.SOURCE_TABLE)
        job = self._make_one(self.JOB_ID, source, [self.DESTINATION_URI],
                             client1)

        job.reload(client=client2)

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method='GET', path=PATH, query_params={})
        self._verifyResourceProperties(job, RESOURCE)


class TestQueryJobConfig(unittest.TestCase, _Base):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import QueryJobConfig

        return QueryJobConfig

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        config = self._make_one()
        self.assertEqual(config._properties, {'query': {}})

    def test_ctor_w_none(self):
        config = self._make_one()
        config.default_dataset = None
        config.destination = None
        self.assertIsNone(config.default_dataset)
        self.assertIsNone(config.destination)

    def test_time_partitioning(self):
        from google.cloud.bigquery import table

        time_partitioning = table.TimePartitioning(
            type_=table.TimePartitioningType.DAY, field='name')
        config = self._make_one()
        config.time_partitioning = time_partitioning
        # TimePartitioning should be configurable after assigning
        time_partitioning.expiration_ms = 10000

        self.assertEqual(
            config.time_partitioning.type_, table.TimePartitioningType.DAY)
        self.assertEqual(config.time_partitioning.field, 'name')
        self.assertEqual(config.time_partitioning.expiration_ms, 10000)

        config.time_partitioning = None
        self.assertIsNone(config.time_partitioning)

    def test_clustering_fields(self):
        fields = ['email', 'postal_code']
        config = self._get_target_class()()
        config.clustering_fields = fields
        self.assertEqual(config.clustering_fields, fields)

        config.clustering_fields = None
        self.assertIsNone(config.clustering_fields)

    def test_from_api_repr_empty(self):
        klass = self._get_target_class()
        config = klass.from_api_repr({})
        self.assertIsNone(config.dry_run)
        self.assertIsNone(config.use_legacy_sql)
        self.assertIsNone(config.default_dataset)
        self.assertIsNone(config.destination)
        self.assertIsNone(config.destination_encryption_configuration)

    def test_from_api_repr_normal(self):
        from google.cloud.bigquery.dataset import DatasetReference

        resource = {
            'query': {
                'useLegacySql': True,
                'query': 'no property for me',
                'defaultDataset': {
                    'projectId': 'someproject',
                    'datasetId': 'somedataset',
                },
                'someNewProperty': 'I should be saved, too.',
            },
            'dryRun': True,
        }
        klass = self._get_target_class()

        config = klass.from_api_repr(resource)

        self.assertTrue(config.use_legacy_sql)
        self.assertEqual(
            config.default_dataset,
            DatasetReference('someproject', 'somedataset'))
        self.assertTrue(config.dry_run)
        # Make sure unknown properties propagate.
        self.assertEqual(
            config._properties['query']['query'], 'no property for me')
        self.assertEqual(
            config._properties['query']['someNewProperty'],
            'I should be saved, too.')

    def test_to_api_repr_normal(self):
        from google.cloud.bigquery.dataset import DatasetReference

        config = self._make_one()
        config.use_legacy_sql = True
        config.default_dataset = DatasetReference(
            'someproject', 'somedataset')
        config.dry_run = False
        config._properties['someNewProperty'] = 'Woohoo, alpha stuff.'

        resource = config.to_api_repr()

        self.assertFalse(resource['dryRun'])
        self.assertTrue(resource['query']['useLegacySql'])
        self.assertEqual(
            resource['query']['defaultDataset']['projectId'], 'someproject')
        self.assertEqual(
            resource['query']['defaultDataset']['datasetId'], 'somedataset')
        # Make sure unknown properties propagate.
        self.assertEqual(
            resource['someNewProperty'], 'Woohoo, alpha stuff.')

    def test_to_api_repr_with_encryption(self):
        from google.cloud.bigquery.table import EncryptionConfiguration

        config = self._make_one()
        config.destination_encryption_configuration = EncryptionConfiguration(
            kms_key_name=self.KMS_KEY_NAME)
        resource = config.to_api_repr()
        self.assertEqual(
            resource, {
                'query': {
                    'destinationEncryptionConfiguration': {
                        'kmsKeyName': self.KMS_KEY_NAME,
                    },
                },
            })

    def test_to_api_repr_with_encryption_none(self):
        config = self._make_one()
        config.destination_encryption_configuration = None
        resource = config.to_api_repr()
        self.assertEqual(
            resource,
            {
                'query': {
                    'destinationEncryptionConfiguration': None,
                },
            })

    def test_from_api_repr_with_encryption(self):
        resource = {
            'query': {
                'destinationEncryptionConfiguration': {
                    'kmsKeyName': self.KMS_KEY_NAME,
                },
            },
        }
        klass = self._get_target_class()
        config = klass.from_api_repr(resource)
        self.assertEqual(
            config.destination_encryption_configuration.kms_key_name,
            self.KMS_KEY_NAME)


class TestQueryJob(unittest.TestCase, _Base):
    JOB_TYPE = 'query'
    QUERY = 'select count(*) from persons'
    DESTINATION_TABLE = 'destination_table'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import QueryJob

        return QueryJob

    def _make_resource(self, started=False, ended=False):
        resource = super(TestQueryJob, self)._make_resource(
            started, ended)
        config = resource['configuration']['query']
        config['query'] = self.QUERY

        if ended:
            resource['status'] = {'state': 'DONE'}

        return resource

    def _verifyBooleanResourceProperties(self, job, config):

        if 'allowLargeResults' in config:
            self.assertEqual(job.allow_large_results,
                             config['allowLargeResults'])
        else:
            self.assertIsNone(job.allow_large_results)
        if 'flattenResults' in config:
            self.assertEqual(job.flatten_results,
                             config['flattenResults'])
        else:
            self.assertIsNone(job.flatten_results)
        if 'useQueryCache' in config:
            self.assertEqual(job.use_query_cache,
                             config['useQueryCache'])
        else:
            self.assertIsNone(job.use_query_cache)
        if 'useLegacySql' in config:
            self.assertEqual(job.use_legacy_sql,
                             config['useLegacySql'])
        else:
            self.assertIsNone(job.use_legacy_sql)

    def _verifyIntegerResourceProperties(self, job, config):
        if 'maximumBillingTier' in config:
            self.assertEqual(
                job.maximum_billing_tier, config['maximumBillingTier'])
        else:
            self.assertIsNone(job.maximum_billing_tier)
        if 'maximumBytesBilled' in config:
            self.assertEqual(
                str(job.maximum_bytes_billed), config['maximumBytesBilled'])
            self.assertIsInstance(job.maximum_bytes_billed, int)
        else:
            self.assertIsNone(job.maximum_bytes_billed)

    def _verify_udf_resources(self, job, config):
        udf_resources = config.get('userDefinedFunctionResources', ())
        self.assertEqual(len(job.udf_resources), len(udf_resources))
        for found, expected in zip(job.udf_resources, udf_resources):
            if 'resourceUri' in expected:
                self.assertEqual(found.udf_type, 'resourceUri')
                self.assertEqual(found.value, expected['resourceUri'])
            else:
                self.assertEqual(found.udf_type, 'inlineCode')
                self.assertEqual(found.value, expected['inlineCode'])

    def _verifyQueryParameters(self, job, config):
        query_parameters = config.get('queryParameters', ())
        self.assertEqual(len(job.query_parameters), len(query_parameters))
        for found, expected in zip(job.query_parameters, query_parameters):
            self.assertEqual(found.to_api_repr(), expected)

    def _verify_table_definitions(self, job, config):
        table_defs = config.get('tableDefinitions')
        if job.table_definitions is None:
            self.assertIsNone(table_defs)
        else:
            self.assertEqual(len(job.table_definitions), len(table_defs))
            for found_key, found_ec in job.table_definitions.items():
                expected_ec = table_defs.get(found_key)
                self.assertIsNotNone(expected_ec)
                self.assertEqual(found_ec.to_api_repr(), expected_ec)

    def _verify_configuration_properties(self, job, configuration):
        if 'dryRun' in configuration:
            self.assertEqual(job.dry_run,
                             configuration['dryRun'])
        else:
            self.assertIsNone(job.dry_run)

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)

        configuration = resource.get('configuration', {})
        self._verify_configuration_properties(job, configuration)

        query_config = resource.get('configuration', {}).get('query')
        self._verifyBooleanResourceProperties(job, query_config)
        self._verifyIntegerResourceProperties(job, query_config)
        self._verify_udf_resources(job, query_config)
        self._verifyQueryParameters(job, query_config)
        self._verify_table_definitions(job, query_config)

        self.assertEqual(job.query, query_config['query'])
        if 'createDisposition' in query_config:
            self.assertEqual(job.create_disposition,
                             query_config['createDisposition'])
        else:
            self.assertIsNone(job.create_disposition)
        if 'defaultDataset' in query_config:
            ds_ref = job.default_dataset
            ds_ref = {
                'projectId': ds_ref.project,
                'datasetId': ds_ref.dataset_id,
            }
            self.assertEqual(ds_ref, query_config['defaultDataset'])
        else:
            self.assertIsNone(job.default_dataset)
        if 'destinationTable' in query_config:
            table = job.destination
            tb_ref = {
                'projectId': table.project,
                'datasetId': table.dataset_id,
                'tableId': table.table_id
            }
            self.assertEqual(tb_ref, query_config['destinationTable'])
        else:
            self.assertIsNone(job.destination)
        if 'priority' in query_config:
            self.assertEqual(job.priority,
                             query_config['priority'])
        else:
            self.assertIsNone(job.priority)
        if 'writeDisposition' in query_config:
            self.assertEqual(job.write_disposition,
                             query_config['writeDisposition'])
        else:
            self.assertIsNone(job.write_disposition)
        if 'destinationEncryptionConfiguration' in query_config:
            self.assertIsNotNone(job.destination_encryption_configuration)
            self.assertEqual(
                job.destination_encryption_configuration.kms_key_name,
                query_config['destinationEncryptionConfiguration'][
                    'kmsKeyName'])
        else:
            self.assertIsNone(job.destination_encryption_configuration)
        if 'schemaUpdateOptions' in query_config:
            self.assertEqual(
                job.schema_update_options, query_config['schemaUpdateOptions'])
        else:
            self.assertIsNone(job.schema_update_options)

    def test_ctor_defaults(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.query, self.QUERY)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(
            job.path,
            '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID))

        self._verifyInitialReadonlyProperties(job)

        self.assertFalse(job.use_legacy_sql)

        # set/read from resource['configuration']['query']
        self.assertIsNone(job.allow_large_results)
        self.assertIsNone(job.create_disposition)
        self.assertIsNone(job.default_dataset)
        self.assertIsNone(job.destination)
        self.assertIsNone(job.flatten_results)
        self.assertIsNone(job.priority)
        self.assertIsNone(job.use_query_cache)
        self.assertIsNone(job.dry_run)
        self.assertIsNone(job.write_disposition)
        self.assertIsNone(job.maximum_billing_tier)
        self.assertIsNone(job.maximum_bytes_billed)
        self.assertIsNone(job.table_definitions)
        self.assertIsNone(job.destination_encryption_configuration)
        self.assertIsNone(job.time_partitioning)
        self.assertIsNone(job.clustering_fields)
        self.assertIsNone(job.schema_update_options)

    def test_ctor_w_udf_resources(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import UDFResource

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]
        client = _make_client(project=self.PROJECT)
        config = QueryJobConfig()
        config.udf_resources = udf_resources
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=config)
        self.assertEqual(job.udf_resources, udf_resources)

    def test_ctor_w_query_parameters(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter("foo", 'INT64', 123)]
        client = _make_client(project=self.PROJECT)
        config = QueryJobConfig()
        config.query_parameters = query_parameters
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=config)
        self.assertEqual(job.query_parameters, query_parameters)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_missing_config(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.DS_ID),
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            }
        }
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'query': {'query': self.QUERY},
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_with_encryption(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            'id': self.JOB_ID,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'configuration': {
                'query': {
                    'query': self.QUERY,
                    'destinationEncryptionConfiguration': {
                        'kmsKeyName': self.KMS_KEY_NAME
                    }
                },
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_properties(self):
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import SchemaUpdateOption
        from google.cloud.bigquery.job import WriteDisposition

        client = _make_client(project=self.PROJECT)
        RESOURCE = self._make_resource()
        query_config = RESOURCE['configuration']['query']
        query_config['createDisposition'] = CreateDisposition.CREATE_IF_NEEDED
        query_config['writeDisposition'] = WriteDisposition.WRITE_TRUNCATE
        query_config['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': self.DS_ID,
            'tableId': self.DESTINATION_TABLE,
        }
        query_config['schemaUpdateOptions'] = [
            SchemaUpdateOption.ALLOW_FIELD_ADDITION,
        ]
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_cancelled(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        job._properties['status'] = {
            'state': 'DONE',
            'errorResult': {
                'reason': 'stopped'
            }
        }

        self.assertTrue(job.cancelled())

    def test_done(self):
        client = _make_client(project=self.PROJECT)
        resource = self._make_resource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)
        self.assertTrue(job.done())

    def test_query_plan(self):
        from google.cloud._helpers import _RFC3339_MICROS
        from google.cloud.bigquery.job import QueryPlanEntry
        from google.cloud.bigquery.job import QueryPlanEntryStep

        plan_entries = [{
            'name': 'NAME',
            'id': '1234',
            'inputStages': ['88', '101'],
            'startMs': '1522540800000',
            'endMs':   '1522540804000',
            'parallelInputs': '1000',
            'completedParallelInputs': '5',
            'waitMsAvg': '33',
            'waitMsMax': '400',
            'waitRatioAvg': 2.71828,
            'waitRatioMax': 3.14159,
            'readMsAvg': '45',
            'readMsMax': '90',
            'readRatioAvg': 1.41421,
            'readRatioMax': 1.73205,
            'computeMsAvg': '55',
            'computeMsMax': '99',
            'computeRatioAvg': 0.69315,
            'computeRatioMax': 1.09861,
            'writeMsAvg': '203',
            'writeMsMax': '340',
            'writeRatioAvg': 3.32193,
            'writeRatioMax': 2.30258,
            'recordsRead': '100',
            'recordsWritten': '1',
            'status': 'STATUS',
            'shuffleOutputBytes': '1024',
            'shuffleOutputBytesSpilled': '1',
            'steps': [{
                'kind': 'KIND',
                'substeps': ['SUBSTEP1', 'SUBSTEP2'],
            }],
        }]
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.query_plan, [])

        statistics = job._properties['statistics'] = {}
        self.assertEqual(job.query_plan, [])

        query_stats = statistics['query'] = {}
        self.assertEqual(job.query_plan, [])

        query_stats['queryPlan'] = plan_entries

        self.assertEqual(len(job.query_plan), len(plan_entries))
        for found, expected in zip(job.query_plan, plan_entries):
            self.assertIsInstance(found, QueryPlanEntry)
            self.assertEqual(found.name, expected['name'])
            self.assertEqual(found.entry_id, expected['id'])
            self.assertEqual(
                    len(found.input_stages),
                    len(expected['inputStages']))
            for f_id in found.input_stages:
                self.assertIn(f_id, [int(e) for e in expected['inputStages']])
            self.assertEqual(
                found.start.strftime(_RFC3339_MICROS),
                '2018-04-01T00:00:00.000000Z')
            self.assertEqual(
                found.end.strftime(_RFC3339_MICROS),
                '2018-04-01T00:00:04.000000Z')
            self.assertEqual(
                    found.parallel_inputs,
                    int(expected['parallelInputs']))
            self.assertEqual(
                    found.completed_parallel_inputs,
                    int(expected['completedParallelInputs']))
            self.assertEqual(found.wait_ms_avg, int(expected['waitMsAvg']))
            self.assertEqual(found.wait_ms_max, int(expected['waitMsMax']))
            self.assertEqual(found.wait_ratio_avg, expected['waitRatioAvg'])
            self.assertEqual(found.wait_ratio_max, expected['waitRatioMax'])
            self.assertEqual(found.read_ms_avg, int(expected['readMsAvg']))
            self.assertEqual(found.read_ms_max, int(expected['readMsMax']))
            self.assertEqual(found.read_ratio_avg, expected['readRatioAvg'])
            self.assertEqual(found.read_ratio_max, expected['readRatioMax'])
            self.assertEqual(
                found.compute_ms_avg,
                int(expected['computeMsAvg']))
            self.assertEqual(
                found.compute_ms_max,
                int(expected['computeMsMax']))
            self.assertEqual(
                found.compute_ratio_avg, expected['computeRatioAvg'])
            self.assertEqual(
                found.compute_ratio_max, expected['computeRatioMax'])
            self.assertEqual(found.write_ms_avg, int(expected['writeMsAvg']))
            self.assertEqual(found.write_ms_max, int(expected['writeMsMax']))
            self.assertEqual(found.write_ratio_avg, expected['writeRatioAvg'])
            self.assertEqual(found.write_ratio_max, expected['writeRatioMax'])
            self.assertEqual(
                found.records_read, int(expected['recordsRead']))
            self.assertEqual(
                found.records_written, int(expected['recordsWritten']))
            self.assertEqual(found.status, expected['status'])
            self.assertEqual(
                    found.shuffle_output_bytes,
                    int(expected['shuffleOutputBytes']))
            self.assertEqual(
                    found.shuffle_output_bytes_spilled,
                    int(expected['shuffleOutputBytesSpilled']))

            self.assertEqual(len(found.steps), len(expected['steps']))
            for f_step, e_step in zip(found.steps, expected['steps']):
                self.assertIsInstance(f_step, QueryPlanEntryStep)
                self.assertEqual(f_step.kind, e_step['kind'])
                self.assertEqual(f_step.substeps, e_step['substeps'])

    def test_total_bytes_processed(self):
        total_bytes = 1234
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.total_bytes_processed)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.total_bytes_processed)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.total_bytes_processed)

        query_stats['totalBytesProcessed'] = str(total_bytes)
        self.assertEqual(job.total_bytes_processed, total_bytes)

    def test_total_bytes_billed(self):
        total_bytes = 1234
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.total_bytes_billed)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.total_bytes_billed)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.total_bytes_billed)

        query_stats['totalBytesBilled'] = str(total_bytes)
        self.assertEqual(job.total_bytes_billed, total_bytes)

    def test_billing_tier(self):
        billing_tier = 1
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.billing_tier)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.billing_tier)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.billing_tier)

        query_stats['billingTier'] = billing_tier
        self.assertEqual(job.billing_tier, billing_tier)

    def test_cache_hit(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.cache_hit)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.cache_hit)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.cache_hit)

        query_stats['cacheHit'] = True
        self.assertTrue(job.cache_hit)

    def test_ddl_operation_performed(self):
        op = 'SKIP'
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.ddl_operation_performed)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.ddl_operation_performed)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.ddl_operation_performed)

        query_stats['ddlOperationPerformed'] = op
        self.assertEqual(job.ddl_operation_performed, op)

    def test_ddl_target_table(self):
        from google.cloud.bigquery.table import TableReference

        ref_table = {
            'projectId': self.PROJECT,
            'datasetId': 'ddl_ds',
            'tableId': 'targettable',
        }
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.ddl_target_table)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.ddl_target_table)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.ddl_target_table)

        query_stats['ddlTargetTable'] = ref_table
        self.assertIsInstance(job.ddl_target_table, TableReference)
        self.assertEqual(job.ddl_target_table.table_id, 'targettable')
        self.assertEqual(job.ddl_target_table.dataset_id, 'ddl_ds')
        self.assertEqual(job.ddl_target_table.project, self.PROJECT)

    def test_num_dml_affected_rows(self):
        num_rows = 1234
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.num_dml_affected_rows)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.num_dml_affected_rows)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.num_dml_affected_rows)

        query_stats['numDmlAffectedRows'] = str(num_rows)
        self.assertEqual(job.num_dml_affected_rows, num_rows)

    def test_slot_millis(self):
        millis = 1234
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.slot_millis)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.slot_millis)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.slot_millis)

        query_stats['totalSlotMs'] = millis
        self.assertEqual(job.slot_millis, millis)

    def test_statement_type(self):
        statement_type = 'SELECT'
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.statement_type)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.statement_type)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.statement_type)

        query_stats['statementType'] = statement_type
        self.assertEqual(job.statement_type, statement_type)

    def test_referenced_tables(self):
        from google.cloud.bigquery.table import TableReference

        ref_tables_resource = [{
            'projectId': self.PROJECT,
            'datasetId': 'dataset',
            'tableId': 'local1',
        }, {

            'projectId': self.PROJECT,
            'datasetId': 'dataset',
            'tableId': 'local2',
        }, {

            'projectId': 'other-project-123',
            'datasetId': 'other-dataset',
            'tableId': 'other-table',
        }]
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.referenced_tables, [])

        statistics = job._properties['statistics'] = {}
        self.assertEqual(job.referenced_tables, [])

        query_stats = statistics['query'] = {}
        self.assertEqual(job.referenced_tables, [])

        query_stats['referencedTables'] = ref_tables_resource

        local1, local2, remote = job.referenced_tables

        self.assertIsInstance(local1, TableReference)
        self.assertEqual(local1.table_id, 'local1')
        self.assertEqual(local1.dataset_id, 'dataset')
        self.assertEqual(local1.project, self.PROJECT)

        self.assertIsInstance(local2, TableReference)
        self.assertEqual(local2.table_id, 'local2')
        self.assertEqual(local2.dataset_id, 'dataset')
        self.assertEqual(local2.project, self.PROJECT)

        self.assertIsInstance(remote, TableReference)
        self.assertEqual(remote.table_id, 'other-table')
        self.assertEqual(remote.dataset_id, 'other-dataset')
        self.assertEqual(remote.project, 'other-project-123')

    def test_timeline(self):
        timeline_resource = [{
            'elapsedMs': 1,
            'activeUnits': 22,
            'pendingUnits': 33,
            'completedUnits': 44,
            'totalSlotMs': 101,
        }]

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.timeline, [])

        statistics = job._properties['statistics'] = {}
        self.assertEqual(job.timeline, [])

        query_stats = statistics['query'] = {}
        self.assertEqual(job.timeline, [])

        query_stats['timeline'] = timeline_resource

        self.assertEqual(len(job.timeline), len(timeline_resource))
        self.assertEqual(job.timeline[0].elapsed_ms, 1)
        self.assertEqual(job.timeline[0].active_units, 22)
        self.assertEqual(job.timeline[0].pending_units, 33)
        self.assertEqual(job.timeline[0].completed_units, 44)
        self.assertEqual(job.timeline[0].slot_millis, 101)

    def test_undeclared_query_parameters(self):
        from google.cloud.bigquery.query import ArrayQueryParameter
        from google.cloud.bigquery.query import ScalarQueryParameter
        from google.cloud.bigquery.query import StructQueryParameter

        undeclared = [{
            'name': 'my_scalar',
            'parameterType': {
                'type': 'STRING',
            },
            'parameterValue': {
                'value': 'value',
            },
        }, {
            'name': 'my_array',
            'parameterType': {
                'type': 'ARRAY',
                'arrayType': {
                    'type': 'INT64',
                },
            },
            'parameterValue': {
                'arrayValues': [
                    {'value': '1066'},
                    {'value': '1745'},
                ],
            },
        }, {
            'name': 'my_struct',
            'parameterType': {
                'type': 'STRUCT',
                'structTypes': [{
                    'name': 'count',
                    'type': {
                        'type': 'INT64',
                    }
                }],
            },
            'parameterValue': {
                'structValues': {
                    'count': {
                        'value': '123',
                    },
                }
            },
        }]
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.undeclared_query_parameters, [])

        statistics = job._properties['statistics'] = {}
        self.assertEqual(job.undeclared_query_parameters, [])

        query_stats = statistics['query'] = {}
        self.assertEqual(job.undeclared_query_parameters, [])

        query_stats['undeclaredQueryParameters'] = undeclared

        scalar, array, struct = job.undeclared_query_parameters

        self.assertIsInstance(scalar, ScalarQueryParameter)
        self.assertEqual(scalar.name, 'my_scalar')
        self.assertEqual(scalar.type_, 'STRING')
        self.assertEqual(scalar.value, 'value')

        self.assertIsInstance(array, ArrayQueryParameter)
        self.assertEqual(array.name, 'my_array')
        self.assertEqual(array.array_type, 'INT64')
        self.assertEqual(array.values, [1066, 1745])

        self.assertIsInstance(struct, StructQueryParameter)
        self.assertEqual(struct.name, 'my_struct')
        self.assertEqual(struct.struct_types, {'count': 'INT64'})
        self.assertEqual(struct.struct_values, {'count': 123})

    def test_estimated_bytes_processed(self):
        est_bytes = 123456

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.estimated_bytes_processed)

        statistics = job._properties['statistics'] = {}
        self.assertIsNone(job.estimated_bytes_processed)

        query_stats = statistics['query'] = {}
        self.assertIsNone(job.estimated_bytes_processed)

        query_stats['estimatedBytesProcessed'] = str(est_bytes)
        self.assertEqual(job.estimated_bytes_processed, est_bytes)

    def test_result(self):
        query_resource = {
            'jobComplete': True,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'schema': {'fields': [{'name': 'col1', 'type': 'STRING'}]},
        }
        connection = _make_connection(query_resource, query_resource)
        client = _make_client(self.PROJECT, connection=connection)
        resource = self._make_resource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)

        result = job.result()

        self.assertEqual(list(result), [])

    def test_result_w_empty_schema(self):
        # Destination table may have no schema for some DDL and DML queries.
        query_resource = {
            'jobComplete': True,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'schema': {'fields': []},
        }
        connection = _make_connection(query_resource, query_resource)
        client = _make_client(self.PROJECT, connection=connection)
        resource = self._make_resource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)

        result = job.result()

        self.assertEqual(list(result), [])

    def test_result_invokes_begins(self):
        begun_resource = self._make_resource()
        incomplete_resource = {
            'jobComplete': False,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'schema': {'fields': [{'name': 'col1', 'type': 'STRING'}]},
        }
        query_resource = copy.deepcopy(incomplete_resource)
        query_resource['jobComplete'] = True
        done_resource = copy.deepcopy(begun_resource)
        done_resource['status'] = {'state': 'DONE'}
        connection = _make_connection(
            begun_resource, incomplete_resource, query_resource, done_resource,
            query_resource)
        client = _make_client(project=self.PROJECT, connection=connection)
        job = self._make_one(self.JOB_ID, self.QUERY, client)

        job.result()

        self.assertEqual(len(connection.api_request.call_args_list), 4)
        begin_request = connection.api_request.call_args_list[0]
        query_request = connection.api_request.call_args_list[2]
        reload_request = connection.api_request.call_args_list[3]
        self.assertEqual(begin_request[1]['method'], 'POST')
        self.assertEqual(query_request[1]['method'], 'GET')
        self.assertEqual(reload_request[1]['method'], 'GET')

    def test_result_w_timeout(self):
        begun_resource = self._make_resource()
        query_resource = {
            'jobComplete': True,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'schema': {'fields': [{'name': 'col1', 'type': 'STRING'}]},
        }
        done_resource = copy.deepcopy(begun_resource)
        done_resource['status'] = {'state': 'DONE'}
        connection = _make_connection(
            begun_resource, query_resource, done_resource)
        client = _make_client(project=self.PROJECT, connection=connection)
        job = self._make_one(self.JOB_ID, self.QUERY, client)

        job.result(timeout=1.0)

        self.assertEqual(len(connection.api_request.call_args_list), 3)
        begin_request = connection.api_request.call_args_list[0]
        query_request = connection.api_request.call_args_list[1]
        reload_request = connection.api_request.call_args_list[2]
        self.assertEqual(begin_request[1]['method'], 'POST')
        self.assertEqual(query_request[1]['method'], 'GET')
        self.assertEqual(
            query_request[1]['path'],
            '/projects/{}/queries/{}'.format(self.PROJECT, self.JOB_ID))
        self.assertEqual(query_request[1]['query_params']['timeoutMs'], 900)
        self.assertEqual(reload_request[1]['method'], 'GET')

    def test_result_error(self):
        from google.cloud import exceptions

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        error_result = {
            'debugInfo': 'DEBUG',
            'location': 'LOCATION',
            'message': 'MESSAGE',
            'reason': 'invalid'
        }
        job._properties['status'] = {
            'errorResult': error_result,
            'errors': [error_result],
            'state': 'DONE'
        }
        job._set_future_result()

        with self.assertRaises(exceptions.GoogleCloudError) as exc_info:
            job.result()

        self.assertIsInstance(exc_info.exception, exceptions.GoogleCloudError)
        self.assertEqual(exc_info.exception.code, http_client.BAD_REQUEST)

    def test_begin_w_bound_client(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.job import QueryJobConfig

        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        DS_ID = 'DATASET'
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        conn = _make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)

        config = QueryJobConfig()
        config.default_dataset = DatasetReference(self.PROJECT, DS_ID)
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=config)

        job._begin()

        self.assertIsNone(job.default_dataset)
        self.assertEqual(job.udf_resources, [])
        conn.api_request.assert_called_once_with(
            method='POST',
            path=PATH,
            data={
                'jobReference': {
                    'projectId': self.PROJECT,
                    'jobId': self.JOB_ID,
                },
                'configuration': {
                    'query': {
                        'query': self.QUERY,
                        'useLegacySql': False,
                        'defaultDataset': {
                            'projectId': self.PROJECT,
                            'datasetId': DS_ID,
                        },
                    },
                },
            })
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_alternate_client(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.job import QueryPriority
        from google.cloud.bigquery.job import SchemaUpdateOption
        from google.cloud.bigquery.job import WriteDisposition

        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        TABLE = 'TABLE'
        DS_ID = 'DATASET'
        RESOURCE = self._make_resource(ended=True)
        QUERY_CONFIGURATION = {
            'query': self.QUERY,
            'allowLargeResults': True,
            'createDisposition': CreateDisposition.CREATE_NEVER,
            'defaultDataset': {
                'projectId': self.PROJECT,
                'datasetId': DS_ID,
            },
            'destinationTable': {
                'projectId': self.PROJECT,
                'datasetId': DS_ID,
                'tableId': TABLE,
            },
            'flattenResults': True,
            'priority': QueryPriority.INTERACTIVE,
            'useQueryCache': True,
            'useLegacySql': True,
            'writeDisposition': WriteDisposition.WRITE_TRUNCATE,
            'maximumBillingTier': 4,
            'maximumBytesBilled': '123456',
            'schemaUpdateOptions': [
                SchemaUpdateOption.ALLOW_FIELD_RELAXATION,
            ]
        }
        RESOURCE['configuration']['query'] = QUERY_CONFIGURATION
        RESOURCE['configuration']['dryRun'] = True
        conn1 = _make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _make_connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        dataset_ref = DatasetReference(self.PROJECT, DS_ID)
        table_ref = dataset_ref.table(TABLE)

        config = QueryJobConfig()
        config.allow_large_results = True
        config.create_disposition = CreateDisposition.CREATE_NEVER
        config.default_dataset = dataset_ref
        config.destination = table_ref
        config.dry_run = True
        config.flatten_results = True
        config.maximum_billing_tier = 4
        config.priority = QueryPriority.INTERACTIVE
        config.use_legacy_sql = True
        config.use_query_cache = True
        config.write_disposition = WriteDisposition.WRITE_TRUNCATE
        config.maximum_bytes_billed = 123456
        config.schema_update_options = [
            SchemaUpdateOption.ALLOW_FIELD_RELAXATION,
        ]
        job = self._make_one(
            self.JOB_ID, self.QUERY, client1, job_config=config)

        job._begin(client=client2)

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method='POST',
            path=PATH,
            data={
                'jobReference': {
                    'projectId': self.PROJECT,
                    'jobId': self.JOB_ID,
                },
                'configuration': {
                    'dryRun': True,
                    'query': QUERY_CONFIGURATION,
                },
            })
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_udf(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import UDFResource

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        INLINE_UDF_CODE = 'var someCode = "here";'
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        RESOURCE['configuration']['query']['userDefinedFunctionResources'] = [
            {'resourceUri': RESOURCE_URI},
            {'inlineCode': INLINE_UDF_CODE},
        ]
        conn = _make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        udf_resources = [
            UDFResource("resourceUri", RESOURCE_URI),
            UDFResource("inlineCode", INLINE_UDF_CODE),
        ]
        config = QueryJobConfig()
        config.udf_resources = udf_resources
        config.use_legacy_sql = True
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=config)

        job._begin()

        self.assertEqual(job.udf_resources, udf_resources)
        conn.api_request.assert_called_once_with(
            method='POST',
            path=PATH,
            data={
                'jobReference': {
                    'projectId': self.PROJECT,
                    'jobId': self.JOB_ID,
                },
                'configuration': {
                    'query': {
                        'query': self.QUERY,
                        'useLegacySql': True,
                        'userDefinedFunctionResources': [
                            {'resourceUri': RESOURCE_URI},
                            {'inlineCode': INLINE_UDF_CODE},
                        ]
                    },
                },
            })
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_named_query_parameter(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter('foo', 'INT64', 123)]
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        config = RESOURCE['configuration']['query']
        config['parameterMode'] = 'NAMED'
        config['queryParameters'] = [
            {
                'name': 'foo',
                'parameterType': {
                    'type': 'INT64',
                },
                'parameterValue': {
                    'value': '123',
                },
            },
        ]
        conn = _make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        jconfig = QueryJobConfig()
        jconfig.query_parameters = query_parameters
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=jconfig)

        job._begin()

        self.assertEqual(job.query_parameters, query_parameters)
        conn.api_request.assert_called_once_with(
            method='POST',
            path=PATH,
            data={
                'jobReference': {
                    'projectId': self.PROJECT,
                    'jobId': self.JOB_ID,
                },
                'configuration': {
                    'query': {
                        'query': self.QUERY,
                        'useLegacySql': False,
                        'parameterMode': 'NAMED',
                        'queryParameters': config['queryParameters'],
                    },
                },
            })
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_positional_query_parameter(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter.positional('INT64', 123)]
        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        config = RESOURCE['configuration']['query']
        config['parameterMode'] = 'POSITIONAL'
        config['queryParameters'] = [
            {
                'parameterType': {
                    'type': 'INT64',
                },
                'parameterValue': {
                    'value': '123',
                },
            },
        ]
        conn = _make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        jconfig = QueryJobConfig()
        jconfig.query_parameters = query_parameters
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=jconfig)

        job._begin()

        self.assertEqual(job.query_parameters, query_parameters)
        conn.api_request.assert_called_once_with(
            method='POST',
            path=PATH,
            data={
                'jobReference': {
                    'projectId': self.PROJECT,
                    'jobId': self.JOB_ID,
                },
                'configuration': {
                    'query': {
                        'query': self.QUERY,
                        'useLegacySql': False,
                        'parameterMode': 'POSITIONAL',
                        'queryParameters': config['queryParameters'],
                    },
                },
            })
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_table_defs(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.external_config import ExternalConfig
        from google.cloud.bigquery.external_config import BigtableColumn
        from google.cloud.bigquery.external_config import BigtableColumnFamily

        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']

        bt_config = ExternalConfig('BIGTABLE')
        bt_config.ignore_unknown_values = True
        bt_config.options.read_rowkey_as_string = True
        cf = BigtableColumnFamily()
        cf.family_id = 'cf'
        col = BigtableColumn()
        col.field_name = 'fn'
        cf.columns = [col]
        bt_config.options.column_families = [cf]
        BT_CONFIG_RESOURCE = {
            'sourceFormat': 'BIGTABLE',
            'ignoreUnknownValues': True,
            'bigtableOptions': {
                'readRowkeyAsString': True,
                'columnFamilies': [{
                    'familyId': 'cf',
                    'columns': [{'fieldName': 'fn'}],
                }],
            },
        }
        CSV_CONFIG_RESOURCE = {
            'sourceFormat': 'CSV',
            'maxBadRecords': 8,
            'csvOptions': {
                'allowJaggedRows': True,
            },
        }
        csv_config = ExternalConfig('CSV')
        csv_config.max_bad_records = 8
        csv_config.options.allow_jagged_rows = True
        bt_table = 'bigtable-table'
        csv_table = 'csv-table'
        RESOURCE['configuration']['query']['tableDefinitions'] = {
            bt_table: BT_CONFIG_RESOURCE,
            csv_table: CSV_CONFIG_RESOURCE,
        }
        want_resource = copy.deepcopy(RESOURCE)
        conn = _make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        config = QueryJobConfig()
        config.table_definitions = {
            bt_table: bt_config,
            csv_table: csv_config,
        }
        config.use_legacy_sql = True
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=config)

        job._begin()

        conn.api_request.assert_called_once_with(
            method='POST',
            path=PATH,
            data={
                'jobReference': {
                    'projectId': self.PROJECT,
                    'jobId': self.JOB_ID,
                },
                'configuration': {
                    'query': {
                        'query': self.QUERY,
                        'useLegacySql': True,
                        'tableDefinitions': {
                            bt_table: BT_CONFIG_RESOURCE,
                            csv_table: CSV_CONFIG_RESOURCE,
                        },
                    },
                },
            })
        self._verifyResourceProperties(job, want_resource)

    def test_dry_run_query(self):
        from google.cloud.bigquery.job import QueryJobConfig

        PATH = '/projects/%s/jobs' % (self.PROJECT,)
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE['statistics']['creationTime']
        del RESOURCE['etag']
        del RESOURCE['selfLink']
        del RESOURCE['user_email']
        RESOURCE['configuration']['dryRun'] = True
        conn = _make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        config = QueryJobConfig()
        config.dry_run = True
        job = self._make_one(
            self.JOB_ID, self.QUERY, client, job_config=config)

        job._begin()
        self.assertEqual(job.udf_resources, [])
        conn.api_request.assert_called_once_with(
            method='POST',
            path=PATH,
            data={
                'jobReference': {
                    'projectId': self.PROJECT,
                    'jobId': self.JOB_ID,
                },
                'configuration': {
                    'query': {
                        'query': self.QUERY,
                        'useLegacySql': False,
                    },
                    'dryRun': True,
                },
            })
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn = _make_connection()
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_ID, self.QUERY, client)

        self.assertFalse(job.exists())

        conn.api_request.assert_called_once_with(
            method='GET',
            path=PATH,
            query_params={'fields': 'id'})

    def test_exists_hit_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        conn1 = _make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _make_connection({})
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        job = self._make_one(self.JOB_ID, self.QUERY, client1)

        self.assertTrue(job.exists(client=client2))

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method='GET',
            path=PATH,
            query_params={'fields': 'id'})

    def test_reload_w_bound_client(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.job import QueryJobConfig

        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        DS_ID = 'DATASET'
        DEST_TABLE = 'dest_table'
        RESOURCE = self._make_resource()
        conn = _make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        dataset_ref = DatasetReference(self.PROJECT, DS_ID)
        table_ref = dataset_ref.table(DEST_TABLE)
        config = QueryJobConfig()
        config.destination = table_ref
        job = self._make_one(self.JOB_ID, None, client, job_config=config)

        job.reload()

        self.assertNotEqual(job.destination, table_ref)

        conn.api_request.assert_called_once_with(
            method='GET', path=PATH, query_params={})
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = '/projects/%s/jobs/%s' % (self.PROJECT, self.JOB_ID)
        DS_ID = 'DATASET'
        DEST_TABLE = 'dest_table'
        RESOURCE = self._make_resource()
        q_config = RESOURCE['configuration']['query']
        q_config['destinationTable'] = {
            'projectId': self.PROJECT,
            'datasetId': DS_ID,
            'tableId': DEST_TABLE,
        }
        conn1 = _make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = _make_connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        job = self._make_one(self.JOB_ID, self.QUERY, client1)

        job.reload(client=client2)

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method='GET', path=PATH, query_params={})
        self._verifyResourceProperties(job, RESOURCE)

    @unittest.skipIf(pandas is None, 'Requires `pandas`')
    def test_to_dataframe(self):
        begun_resource = self._make_resource()
        query_resource = {
            'jobComplete': True,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'totalRows': '4',
            'schema': {
                'fields': [
                    {'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE'},
                    {'name': 'age', 'type': 'INTEGER', 'mode': 'NULLABLE'},
                ],
            },
            'rows': [
                {'f': [{'v': 'Phred Phlyntstone'}, {'v': '32'}]},
                {'f': [{'v': 'Bharney Rhubble'}, {'v': '33'}]},
                {'f': [{'v': 'Wylma Phlyntstone'}, {'v': '29'}]},
                {'f': [{'v': 'Bhettye Rhubble'}, {'v': '27'}]},
            ],
        }
        done_resource = copy.deepcopy(begun_resource)
        done_resource['status'] = {'state': 'DONE'}
        connection = _make_connection(
            begun_resource, query_resource, done_resource, query_resource)
        client = _make_client(project=self.PROJECT, connection=connection)
        job = self._make_one(self.JOB_ID, self.QUERY, client)

        df = job.to_dataframe()

        self.assertIsInstance(df, pandas.DataFrame)
        self.assertEqual(len(df), 4)  # verify the number of rows
        self.assertEqual(list(df), ['name', 'age'])  # verify the column names

    def test_iter(self):
        import types

        begun_resource = self._make_resource()
        query_resource = {
            'jobComplete': True,
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
            'totalRows': '0',
            'schema': {'fields': [{'name': 'col1', 'type': 'STRING'}]},
        }
        done_resource = copy.deepcopy(begun_resource)
        done_resource['status'] = {'state': 'DONE'}
        connection = _make_connection(
            begun_resource, query_resource, done_resource)
        client = _make_client(project=self.PROJECT, connection=connection)
        job = self._make_one(self.JOB_ID, self.QUERY, client)

        self.assertIsInstance(iter(job), types.GeneratorType)


class TestQueryPlanEntryStep(unittest.TestCase, _Base):
    KIND = 'KIND'
    SUBSTEPS = ('SUB1', 'SUB2')

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import QueryPlanEntryStep

        return QueryPlanEntryStep

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        step = self._make_one(self.KIND, self.SUBSTEPS)
        self.assertEqual(step.kind, self.KIND)
        self.assertEqual(step.substeps, list(self.SUBSTEPS))

    def test_from_api_repr_empty(self):
        klass = self._get_target_class()
        step = klass.from_api_repr({})
        self.assertIsNone(step.kind)
        self.assertEqual(step.substeps, [])

    def test_from_api_repr_normal(self):
        resource = {
            'kind': self.KIND,
            'substeps': self.SUBSTEPS,
        }
        klass = self._get_target_class()
        step = klass.from_api_repr(resource)
        self.assertEqual(step.kind, self.KIND)
        self.assertEqual(step.substeps, list(self.SUBSTEPS))

    def test___eq___mismatched_type(self):
        step = self._make_one(self.KIND, self.SUBSTEPS)
        self.assertNotEqual(step, object())

    def test___eq___mismatch_kind(self):
        step = self._make_one(self.KIND, self.SUBSTEPS)
        other = self._make_one('OTHER', self.SUBSTEPS)
        self.assertNotEqual(step, other)

    def test___eq___mismatch_substeps(self):
        step = self._make_one(self.KIND, self.SUBSTEPS)
        other = self._make_one(self.KIND, ())
        self.assertNotEqual(step, other)

    def test___eq___hit(self):
        step = self._make_one(self.KIND, self.SUBSTEPS)
        other = self._make_one(self.KIND, self.SUBSTEPS)
        self.assertEqual(step, other)

    def test___eq___wrong_type(self):
        step = self._make_one(self.KIND, self.SUBSTEPS)
        self.assertFalse(step == 'hello')


class TestQueryPlanEntry(unittest.TestCase, _Base):
    NAME = 'NAME'
    ENTRY_ID = 1234
    START_MS = 1522540800000
    END_MS = 1522540804000
    INPUT_STAGES = (88, 101)
    PARALLEL_INPUTS = 1000
    COMPLETED_PARALLEL_INPUTS = 5
    WAIT_MS_AVG = 33
    WAIT_MS_MAX = 400
    WAIT_RATIO_AVG = 2.71828
    WAIT_RATIO_MAX = 3.14159
    READ_MS_AVG = 45
    READ_MS_MAX = 90
    READ_RATIO_AVG = 1.41421
    READ_RATIO_MAX = 1.73205
    COMPUTE_MS_AVG = 55
    COMPUTE_MS_MAX = 99
    COMPUTE_RATIO_AVG = 0.69315
    COMPUTE_RATIO_MAX = 1.09861
    WRITE_MS_AVG = 203
    WRITE_MS_MAX = 340
    WRITE_RATIO_AVG = 3.32193
    WRITE_RATIO_MAX = 2.30258
    RECORDS_READ = 100
    RECORDS_WRITTEN = 1
    STATUS = 'STATUS'
    SHUFFLE_OUTPUT_BYTES = 1024
    SHUFFLE_OUTPUT_BYTES_SPILLED = 1

    START_RFC3339_MICROS = '2018-04-01T00:00:00.000000Z'
    END_RFC3339_MICROS = '2018-04-01T00:00:04.000000Z'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import QueryPlanEntry

        return QueryPlanEntry

    def test_from_api_repr_empty(self):
        klass = self._get_target_class()

        entry = klass.from_api_repr({})

        self.assertIsNone(entry.name)
        self.assertIsNone(entry.entry_id)
        self.assertEqual(entry.input_stages, [])
        self.assertIsNone(entry.start)
        self.assertIsNone(entry.end)
        self.assertIsNone(entry.parallel_inputs)
        self.assertIsNone(entry.completed_parallel_inputs)
        self.assertIsNone(entry.wait_ms_avg)
        self.assertIsNone(entry.wait_ms_max)
        self.assertIsNone(entry.wait_ratio_avg)
        self.assertIsNone(entry.wait_ratio_max)
        self.assertIsNone(entry.read_ms_avg)
        self.assertIsNone(entry.read_ms_max)
        self.assertIsNone(entry.read_ratio_avg)
        self.assertIsNone(entry.read_ratio_max)
        self.assertIsNone(entry.compute_ms_avg)
        self.assertIsNone(entry.compute_ms_max)
        self.assertIsNone(entry.compute_ratio_avg)
        self.assertIsNone(entry.compute_ratio_max)
        self.assertIsNone(entry.write_ms_avg)
        self.assertIsNone(entry.write_ms_max)
        self.assertIsNone(entry.write_ratio_avg)
        self.assertIsNone(entry.write_ratio_max)
        self.assertIsNone(entry.records_read)
        self.assertIsNone(entry.records_written)
        self.assertIsNone(entry.status)
        self.assertIsNone(entry.shuffle_output_bytes)
        self.assertIsNone(entry.shuffle_output_bytes_spilled)
        self.assertEqual(entry.steps, [])

    def test_from_api_repr_normal(self):
        from google.cloud.bigquery.job import QueryPlanEntryStep

        steps = [QueryPlanEntryStep(
            kind=TestQueryPlanEntryStep.KIND,
            substeps=TestQueryPlanEntryStep.SUBSTEPS)]
        resource = {
            'name': self.NAME,
            'id': self.ENTRY_ID,
            'inputStages': self.INPUT_STAGES,
            'startMs': self.START_MS,
            'endMs': self.END_MS,
            'waitMsAvg': self.WAIT_MS_AVG,
            'waitMsMax': self.WAIT_MS_MAX,
            'waitRatioAvg': self.WAIT_RATIO_AVG,
            'waitRatioMax': self.WAIT_RATIO_MAX,
            'readMsAvg': self.READ_MS_AVG,
            'readMsMax': self.READ_MS_MAX,
            'readRatioAvg': self.READ_RATIO_AVG,
            'readRatioMax': self.READ_RATIO_MAX,
            'computeMsAvg': self.COMPUTE_MS_AVG,
            'computeMsMax': self.COMPUTE_MS_MAX,
            'computeRatioAvg': self.COMPUTE_RATIO_AVG,
            'computeRatioMax': self.COMPUTE_RATIO_MAX,
            'writeMsAvg': self.WRITE_MS_AVG,
            'writeMsMax': self.WRITE_MS_MAX,
            'writeRatioAvg': self.WRITE_RATIO_AVG,
            'writeRatioMax': self.WRITE_RATIO_MAX,
            'recordsRead': self.RECORDS_READ,
            'recordsWritten': self.RECORDS_WRITTEN,
            'status': self.STATUS,
            'shuffleOutputBytes': self.SHUFFLE_OUTPUT_BYTES,
            'shuffleOutputBytesSpilled': self.SHUFFLE_OUTPUT_BYTES_SPILLED,
            'steps': [{
                'kind': TestQueryPlanEntryStep.KIND,
                'substeps': TestQueryPlanEntryStep.SUBSTEPS,
            }]
        }
        klass = self._get_target_class()

        entry = klass.from_api_repr(resource)
        self.assertEqual(entry.name, self.NAME)
        self.assertEqual(entry.entry_id, self.ENTRY_ID)
        self.assertEqual(entry.wait_ratio_avg, self.WAIT_RATIO_AVG)
        self.assertEqual(entry.wait_ratio_max, self.WAIT_RATIO_MAX)
        self.assertEqual(entry.read_ratio_avg, self.READ_RATIO_AVG)
        self.assertEqual(entry.read_ratio_max, self.READ_RATIO_MAX)
        self.assertEqual(entry.compute_ratio_avg, self.COMPUTE_RATIO_AVG)
        self.assertEqual(entry.compute_ratio_max, self.COMPUTE_RATIO_MAX)
        self.assertEqual(entry.write_ratio_avg, self.WRITE_RATIO_AVG)
        self.assertEqual(entry.write_ratio_max, self.WRITE_RATIO_MAX)
        self.assertEqual(entry.records_read, self.RECORDS_READ)
        self.assertEqual(entry.records_written, self.RECORDS_WRITTEN)
        self.assertEqual(entry.status, self.STATUS)
        self.assertEqual(entry.steps, steps)

    def test_start(self):
        from google.cloud._helpers import _RFC3339_MICROS

        klass = self._get_target_class()

        entry = klass.from_api_repr({})
        self.assertEqual(
            entry.start,
            None)

        entry._properties['startMs'] = self.START_MS
        self.assertEqual(
            entry.start.strftime(_RFC3339_MICROS),
            self.START_RFC3339_MICROS)

    def test_end(self):
        from google.cloud._helpers import _RFC3339_MICROS

        klass = self._get_target_class()

        entry = klass.from_api_repr({})
        self.assertEqual(
            entry.end,
            None)

        entry._properties['endMs'] = self.END_MS
        self.assertEqual(
            entry.end.strftime(_RFC3339_MICROS),
            self.END_RFC3339_MICROS)


class TestTimelineEntry(unittest.TestCase, _Base):
    ELAPSED_MS = 101
    ACTIVE_UNITS = 50
    PENDING_UNITS = 98
    COMPLETED_UNITS = 520
    SLOT_MILLIS = 12029

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import TimelineEntry
        return TimelineEntry

    def test_from_api_repr_empty(self):
        klass = self._get_target_class()
        entry = klass.from_api_repr({})
        self.assertIsNone(entry.elapsed_ms)
        self.assertIsNone(entry.active_units)
        self.assertIsNone(entry.pending_units)
        self.assertIsNone(entry.completed_units)
        self.assertIsNone(entry.slot_millis)

    def test_from_api_repr_normal(self):
        resource = {
            'elapsedMs': self.ELAPSED_MS,
            'activeUnits': self.ACTIVE_UNITS,
            'pendingUnits': self.PENDING_UNITS,
            'completedUnits': self.COMPLETED_UNITS,
            'totalSlotMs': self.SLOT_MILLIS,
        }
        klass = self._get_target_class()

        entry = klass.from_api_repr(resource)
        self.assertEqual(entry.elapsed_ms, self.ELAPSED_MS)
        self.assertEqual(entry.active_units, self.ACTIVE_UNITS)
        self.assertEqual(entry.pending_units, self.PENDING_UNITS)
        self.assertEqual(entry.completed_units, self.COMPLETED_UNITS)
        self.assertEqual(entry.slot_millis, self.SLOT_MILLIS)
