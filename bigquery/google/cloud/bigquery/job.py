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

"""Define API Jobs."""

import copy
import threading

from six.moves import http_client

import google.api_core.future.polling
from google.cloud import exceptions
from google.cloud.exceptions import NotFound
from google.cloud.bigquery.dataset import DatasetReference
from google.cloud.bigquery.external_config import ExternalConfig
from google.cloud.bigquery.query import _query_param_from_api_repr
from google.cloud.bigquery.query import ArrayQueryParameter
from google.cloud.bigquery.query import ScalarQueryParameter
from google.cloud.bigquery.query import StructQueryParameter
from google.cloud.bigquery.query import UDFResource
from google.cloud.bigquery.retry import DEFAULT_RETRY
from google.cloud.bigquery.schema import SchemaField
from google.cloud.bigquery.table import _EmptyRowIterator
from google.cloud.bigquery.table import EncryptionConfiguration
from google.cloud.bigquery.table import TableReference
from google.cloud.bigquery.table import Table
from google.cloud.bigquery.table import TimePartitioning
from google.cloud.bigquery import _helpers

_DONE_STATE = 'DONE'
_STOPPED_REASON = 'stopped'
_TIMEOUT_BUFFER_SECS = 0.1

_ERROR_REASON_TO_EXCEPTION = {
    'accessDenied': http_client.FORBIDDEN,
    'backendError': http_client.INTERNAL_SERVER_ERROR,
    'billingNotEnabled': http_client.FORBIDDEN,
    'billingTierLimitExceeded': http_client.BAD_REQUEST,
    'blocked': http_client.FORBIDDEN,
    'duplicate': http_client.CONFLICT,
    'internalError': http_client.INTERNAL_SERVER_ERROR,
    'invalid': http_client.BAD_REQUEST,
    'invalidQuery': http_client.BAD_REQUEST,
    'notFound': http_client.NOT_FOUND,
    'notImplemented': http_client.NOT_IMPLEMENTED,
    'quotaExceeded': http_client.FORBIDDEN,
    'rateLimitExceeded': http_client.FORBIDDEN,
    'resourceInUse': http_client.BAD_REQUEST,
    'resourcesExceeded': http_client.BAD_REQUEST,
    'responseTooLarge': http_client.FORBIDDEN,
    'stopped': http_client.OK,
    'tableUnavailable': http_client.BAD_REQUEST,
}


def _error_result_to_exception(error_result):
    """Maps BigQuery error reasons to an exception.

    The reasons and their matching HTTP status codes are documented on
    the `troubleshooting errors`_ page.

    .. _troubleshooting errors: https://cloud.google.com/bigquery\
        /troubleshooting-errors

    :type error_result: Mapping[str, str]
    :param error_result: The error result from BigQuery.

    :rtype google.cloud.exceptions.GoogleCloudError:
    :returns: The mapped exception.
    """
    reason = error_result.get('reason')
    status_code = _ERROR_REASON_TO_EXCEPTION.get(
        reason, http_client.INTERNAL_SERVER_ERROR)
    return exceptions.from_http_status(
        status_code, error_result.get('message', ''), errors=[error_result])


class Compression(object):
    """The compression type to use for exported files. The default value is
    :attr:`NONE`.

    :attr:`DEFLATE` and :attr:`SNAPPY` are
    only supported for Avro.
    """

    GZIP = 'GZIP'
    """Specifies GZIP format."""

    DEFLATE = 'DEFLATE'
    """Specifies DEFLATE format."""

    SNAPPY = 'SNAPPY'
    """Specifies SNAPPY format."""

    NONE = 'NONE'
    """Specifies no compression."""


class CreateDisposition(object):
    """Specifies whether the job is allowed to create new tables. The default
    value is :attr:`CREATE_IF_NEEDED`.

    Creation, truncation and append actions occur as one atomic update
    upon job completion.
    """

    CREATE_IF_NEEDED = 'CREATE_IF_NEEDED'
    """If the table does not exist, BigQuery creates the table."""

    CREATE_NEVER = 'CREATE_NEVER'
    """The table must already exist. If it does not, a 'notFound' error is
    returned in the job result."""


class DestinationFormat(object):
    """The exported file format. The default value is :attr:`CSV`.

    Tables with nested or repeated fields cannot be exported as CSV.
    """

    CSV = 'CSV'
    """Specifies CSV format."""

    NEWLINE_DELIMITED_JSON = 'NEWLINE_DELIMITED_JSON'
    """Specifies newline delimited JSON format."""

    AVRO = 'AVRO'
    """Specifies Avro format."""


class Encoding(object):
    """The character encoding of the data. The default is :attr:`UTF_8`.

    BigQuery decodes the data after the raw, binary data has been
    split using the values of the quote and fieldDelimiter properties.
    """

    UTF_8 = 'UTF-8'
    """Specifies UTF-8 encoding."""

    ISO_8859_1 = 'ISO-8859-1'
    """Specifies ISO-8859-1 encoding."""


class QueryPriority(object):
    """Specifies a priority for the query. The default value is
    :attr:`INTERACTIVE`.
    """

    INTERACTIVE = 'INTERACTIVE'
    """Specifies interactive priority."""

    BATCH = 'BATCH'
    """Specifies batch priority."""


class SourceFormat(object):
    """The format of the data files. The default value is :attr:`CSV`.

    Note that the set of allowed values for loading data is different
    than the set used for external data sources (see
    :class:`~google.cloud.bigquery.external_config.ExternalSourceFormat`).
    """

    CSV = 'CSV'
    """Specifies CSV format."""

    DATASTORE_BACKUP = 'DATASTORE_BACKUP'
    """Specifies datastore backup format"""

    NEWLINE_DELIMITED_JSON = 'NEWLINE_DELIMITED_JSON'
    """Specifies newline delimited JSON format."""

    AVRO = 'AVRO'
    """Specifies Avro format."""

    PARQUET = 'PARQUET'
    """Specifies Parquet format."""

    ORC = 'ORC'
    """Specifies Orc format."""


class WriteDisposition(object):
    """Specifies the action that occurs if destination table already exists.

    The default value is :attr:`WRITE_APPEND`.

    Each action is atomic and only occurs if BigQuery is able to complete
    the job successfully. Creation, truncation and append actions occur as one
    atomic update upon job completion.
    """

    WRITE_APPEND = 'WRITE_APPEND'
    """If the table already exists, BigQuery appends the data to the table."""

    WRITE_TRUNCATE = 'WRITE_TRUNCATE'
    """If the table already exists, BigQuery overwrites the table data."""

    WRITE_EMPTY = 'WRITE_EMPTY'
    """If the table already exists and contains data, a 'duplicate' error is
    returned in the job result."""


class SchemaUpdateOption(object):
    """Specifies an update to the destination table schema as a side effect of
    a load job.
    """

    ALLOW_FIELD_ADDITION = 'ALLOW_FIELD_ADDITION'
    """Allow adding a nullable field to the schema."""

    ALLOW_FIELD_RELAXATION = 'ALLOW_FIELD_RELAXATION'
    """Allow relaxing a required field in the original schema to nullable."""


class _JobReference(object):
    """A reference to a job.

    Arguments:
        job_id (str): ID of the job to run.
        project (str): ID of the project where the job runs.
        location (str): Location of where the job runs.
    """

    def __init__(self, job_id, project, location):
        self._properties = {
            'jobId': job_id,
            'projectId': project,
        }
        # The location field must not be populated if it is None.
        if location:
            self._properties['location'] = location

    @property
    def job_id(self):
        """str: ID of the job."""
        return self._properties.get('jobId')

    @property
    def project(self):
        """str: ID of the project where the job runs."""
        return self._properties.get('projectId')

    @property
    def location(self):
        """str: Location where the job runs."""
        return self._properties.get('location')

    def _to_api_repr(self):
        """Returns the API resource representation of the job reference."""
        return copy.deepcopy(self._properties)

    @classmethod
    def _from_api_repr(cls, resource):
        """Returns a job reference for an API resource representation."""
        job_id = resource.get('jobId')
        project = resource.get('projectId')
        location = resource.get('location')
        job_ref = cls(job_id, project, location)
        return job_ref


class _AsyncJob(google.api_core.future.polling.PollingFuture):
    """Base class for asynchronous jobs.

    Arguments:
        job_id (Union[str, _JobReference]):
            Job's ID in the project associated with the client or a
            fully-qualified job reference.
        client (google.cloud.bigquery.client.Client):
            Client which holds credentials and project configuration.
    """
    def __init__(self, job_id, client):
        super(_AsyncJob, self).__init__()

        # The job reference can be either a plain job ID or the full resource.
        # Populate the properties dictionary consistently depending on what has
        # been passed in.
        job_ref = job_id
        if not isinstance(job_id, _JobReference):
            job_ref = _JobReference(job_id, client.project, None)
        self._properties = {
            'jobReference': job_ref._to_api_repr(),
        }

        self._client = client
        self._result_set = False
        self._completion_lock = threading.Lock()

    @property
    def job_id(self):
        """str: ID of the job."""
        return _helpers._get_sub_prop(
            self._properties, ['jobReference', 'jobId'])

    @property
    def project(self):
        """Project bound to the job.

        :rtype: str
        :returns: the project (derived from the client).
        """
        return _helpers._get_sub_prop(
            self._properties, ['jobReference', 'projectId'])

    @property
    def location(self):
        """str: Location where the job runs."""
        return _helpers._get_sub_prop(
            self._properties, ['jobReference', 'location'])

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: :class:`google.cloud.bigquery.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    @property
    def job_type(self):
        """Type of job

        :rtype: str
        :returns: one of 'load', 'copy', 'extract', 'query'
        """
        return self._JOB_TYPE

    @property
    def path(self):
        """URL path for the job's APIs.

        :rtype: str
        :returns: the path based on project and job ID.
        """
        return '/projects/%s/jobs/%s' % (self.project, self.job_id)

    @property
    def labels(self):
        """Dict[str, str]: Labels for the job."""
        return self._properties.setdefault('labels', {})

    @property
    def etag(self):
        """ETag for the job resource.

        :rtype: str, or ``NoneType``
        :returns: the ETag (None until set from the server).
        """
        return self._properties.get('etag')

    @property
    def self_link(self):
        """URL for the job resource.

        :rtype: str, or ``NoneType``
        :returns: the URL (None until set from the server).
        """
        return self._properties.get('selfLink')

    @property
    def user_email(self):
        """E-mail address of user who submitted the job.

        :rtype: str, or ``NoneType``
        :returns: the URL (None until set from the server).
        """
        return self._properties.get('user_email')

    @property
    def created(self):
        """Datetime at which the job was created.

        :rtype: ``datetime.datetime``, or ``NoneType``
        :returns: the creation time (None until set from the server).
        """
        statistics = self._properties.get('statistics')
        if statistics is not None:
            millis = statistics.get('creationTime')
            if millis is not None:
                return _helpers._datetime_from_microseconds(millis * 1000.0)

    @property
    def started(self):
        """Datetime at which the job was started.

        :rtype: ``datetime.datetime``, or ``NoneType``
        :returns: the start time (None until set from the server).
        """
        statistics = self._properties.get('statistics')
        if statistics is not None:
            millis = statistics.get('startTime')
            if millis is not None:
                return _helpers._datetime_from_microseconds(millis * 1000.0)

    @property
    def ended(self):
        """Datetime at which the job finished.

        :rtype: ``datetime.datetime``, or ``NoneType``
        :returns: the end time (None until set from the server).
        """
        statistics = self._properties.get('statistics')
        if statistics is not None:
            millis = statistics.get('endTime')
            if millis is not None:
                return _helpers._datetime_from_microseconds(millis * 1000.0)

    def _job_statistics(self):
        """Helper for job-type specific statistics-based properties."""
        statistics = self._properties.get('statistics', {})
        return statistics.get(self._JOB_TYPE, {})

    @property
    def error_result(self):
        """Error information about the job as a whole.

        :rtype: mapping, or ``NoneType``
        :returns: the error information (None until set from the server).
        """
        status = self._properties.get('status')
        if status is not None:
            return status.get('errorResult')

    @property
    def errors(self):
        """Information about individual errors generated by the job.

        :rtype: list of mappings, or ``NoneType``
        :returns: the error information (None until set from the server).
        """
        status = self._properties.get('status')
        if status is not None:
            return status.get('errors')

    @property
    def state(self):
        """Status of the job.

        :rtype: str, or ``NoneType``
        :returns: the state (None until set from the server).
        """
        status = self._properties.get('status')
        if status is not None:
            return status.get('state')

    def _scrub_local_properties(self, cleaned):
        """Helper:  handle subclass properties in cleaned."""
        pass

    def _copy_configuration_properties(self, configuration):
        """Helper:  assign subclass configuration properties in cleaned."""
        raise NotImplementedError("Abstract")

    def _set_properties(self, api_response):
        """Update properties from resource in body of ``api_response``

        :type api_response: dict
        :param api_response: response returned from an API call
        """
        cleaned = api_response.copy()
        self._scrub_local_properties(cleaned)

        statistics = cleaned.get('statistics', {})
        if 'creationTime' in statistics:
            statistics['creationTime'] = float(statistics['creationTime'])
        if 'startTime' in statistics:
            statistics['startTime'] = float(statistics['startTime'])
        if 'endTime' in statistics:
            statistics['endTime'] = float(statistics['endTime'])

        self._properties.clear()
        self._properties.update(cleaned)
        self._copy_configuration_properties(cleaned.get('configuration', {}))

        # For Future interface
        self._set_future_result()

    @classmethod
    def _get_resource_config(cls, resource):
        """Helper for :meth:`from_api_repr`

        :type resource: dict
        :param resource: resource for the job

        :rtype: dict
        :returns: tuple (string, dict), where the first element is the
                  job ID and the second contains job-specific configuration.
        :raises: :class:`KeyError` if the resource has no identifier, or
                 is missing the appropriate configuration.
        """
        if ('jobReference' not in resource or
                'jobId' not in resource['jobReference']):
            raise KeyError('Resource lacks required identity information: '
                           '["jobReference"]["jobId"]')
        job_id = resource['jobReference']['jobId']
        if ('configuration' not in resource or
                cls._JOB_TYPE not in resource['configuration']):
            raise KeyError('Resource lacks required configuration: '
                           '["configuration"]["%s"]' % cls._JOB_TYPE)
        return job_id, resource['configuration']

    def _build_resource(self):
        """Helper:  Generate a resource for :meth:`_begin`."""
        raise NotImplementedError("Abstract")

    def _begin(self, client=None, retry=DEFAULT_RETRY):
        """API call:  begin the job via a POST request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :raises: :exc:`ValueError` if the job has already begin.
        """
        if self.state is not None:
            raise ValueError("Job already begun.")

        client = self._require_client(client)
        path = '/projects/%s/jobs' % (self.project,)

        # jobs.insert is idempotent because we ensure that every new
        # job has an ID.
        api_response = client._call_api(
            retry,
            method='POST', path=path, data=self._build_resource())
        self._set_properties(api_response)

    def exists(self, client=None, retry=DEFAULT_RETRY):
        """API call:  test for the existence of the job via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: bool
        :returns: Boolean indicating existence of the job.
        """
        client = self._require_client(client)

        extra_params = {'fields': 'id'}
        if self.location:
            extra_params['location'] = self.location

        try:
            client._call_api(retry,
                             method='GET', path=self.path,
                             query_params=extra_params)
        except NotFound:
            return False
        else:
            return True

    def reload(self, client=None, retry=DEFAULT_RETRY):
        """API call:  refresh job properties via a GET request.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.
        """
        client = self._require_client(client)

        extra_params = {}
        if self.location:
            extra_params['location'] = self.location

        api_response = client._call_api(
            retry, method='GET', path=self.path, query_params=extra_params)
        self._set_properties(api_response)

    def cancel(self, client=None):
        """API call:  cancel job via a POST request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/cancel

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: bool
        :returns: Boolean indicating that the cancel request was sent.
        """
        client = self._require_client(client)

        extra_params = {}
        if self.location:
            extra_params['location'] = self.location

        api_response = client._connection.api_request(
            method='POST', path='%s/cancel' % (self.path,),
            query_params=extra_params)
        self._set_properties(api_response['job'])
        # The Future interface requires that we return True if the *attempt*
        # to cancel was successful.
        return True

    # The following methods implement the PollingFuture interface. Note that
    # the methods above are from the pre-Future interface and are left for
    # compatibility. The only "overloaded" method is :meth:`cancel`, which
    # satisfies both interfaces.

    def _set_future_result(self):
        """Set the result or exception from the job if it is complete."""
        # This must be done in a lock to prevent the polling thread
        # and main thread from both executing the completion logic
        # at the same time.
        with self._completion_lock:
            # If the operation isn't complete or if the result has already been
            # set, do not call set_result/set_exception again.
            # Note: self._result_set is set to True in set_result and
            # set_exception, in case those methods are invoked directly.
            if self.state != _DONE_STATE or self._result_set:
                return

            if self.error_result is not None:
                exception = _error_result_to_exception(self.error_result)
                self.set_exception(exception)
            else:
                self.set_result(self)

    def done(self, retry=DEFAULT_RETRY):
        """Refresh the job and checks if it is complete.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: bool
        :returns: True if the job is complete, False otherwise.
        """
        # Do not refresh is the state is already done, as the job will not
        # change once complete.
        if self.state != _DONE_STATE:
            self.reload(retry=retry)
        return self.state == _DONE_STATE

    def result(self, timeout=None):
        """Start the job and wait for it to complete and get the result.

        :type timeout: float
        :param timeout:
            How long (in seconds) to wait for job to complete before raising
            a :class:`concurrent.futures.TimeoutError`.

        :rtype: _AsyncJob
        :returns: This instance.

        :raises:
            :class:`~google.cloud.exceptions.GoogleCloudError` if the job
            failed or :class:`concurrent.futures.TimeoutError` if the job did
            not complete in the given timeout.
        """
        if self.state is None:
            self._begin()
        # TODO: modify PollingFuture so it can pass a retry argument to done().
        return super(_AsyncJob, self).result(timeout=timeout)

    def cancelled(self):
        """Check if the job has been cancelled.

        This always returns False. It's not possible to check if a job was
        cancelled in the API. This method is here to satisfy the interface
        for :class:`google.api_core.future.Future`.

        :rtype: bool
        :returns: False
        """
        return (self.error_result is not None
                and self.error_result.get('reason') == _STOPPED_REASON)


class _JobConfig(object):
    """Abstract base class for job configuration objects.

    Arguments:
        job_type (str): The key to use for the job configuration.
    """

    def __init__(self, job_type):
        self._job_type = job_type
        self._properties = {job_type: {}}

    @property
    def labels(self):
        """Dict[str, str]: Labels for the job.

        This method always returns a dict. To change a job's labels,
        modify the dict, then call ``Client.update_job``. To delete a
        label, set its value to :data:`None` before updating.

        Raises:
            ValueError: If ``value`` type is invalid.
        """
        return self._properties.setdefault('labels', {})

    @labels.setter
    def labels(self, value):
        if not isinstance(value, dict):
            raise ValueError("Pass a dict")
        self._properties['labels'] = value

    def _get_sub_prop(self, key, default=None):
        """Get a value in the ``self._properties[self._job_type]`` dictionary.

        Most job properties are inside the dictionary related to the job type
        (e.g. 'copy', 'extract', 'load', 'query'). Use this method to access
        those properties::

            self._get_sub_prop('destinationTable')

        This is equivalent to using the ``_helpers._get_sub_prop`` function::

            _helpers._get_sub_prop(
                self._properties, ['query', 'destinationTable'])

        Arguments:
            key (str):
                 Key for the value to get in the
                 ``self._properties[self._job_type]`` dictionary.
            default (object):
                (Optional) Default value to return if the key is not found.
                Defaults to ``None``.

        Returns:
            object: The value if present or the default.
        """
        return _helpers._get_sub_prop(
            self._properties, [self._job_type, key], default=default)

    def _set_sub_prop(self, key, value):
        """Set a value in the ``self._properties[self._job_type]`` dictionary.

        Most job properties are inside the dictionary related to the job type
        (e.g. 'copy', 'extract', 'load', 'query'). Use this method to set
        those properties::

            self._set_sub_prop('useLegacySql', False)

        This is equivalent to using the ``_helper._set_sub_prop`` function::

            _helper._set_sub_prop(
                self._properties, ['query', 'useLegacySql'], False)

        Arguments:
            key (str):
                 Key to set in the ``self._properties[self._job_type]``
                 dictionary.
            value (object): Value to set.
        """
        _helpers._set_sub_prop(self._properties, [self._job_type, key], value)

    def _del_sub_prop(self, key):
        """Reove ``key`` from the ``self._properties[self._job_type]`` dict.

        Most job properties are inside the dictionary related to the job type
        (e.g. 'copy', 'extract', 'load', 'query'). Use this method to clear
        those properties::

            self._del_sub_prop('useLegacySql')

        This is equivalent to using the ``_helper._del_sub_prop`` function::

            _helper._del_sub_prop(
                self._properties, ['query', 'useLegacySql'])

        Arguments:
            key (str):
                 Key to remove in the ``self._properties[self._job_type]``
                 dictionary.
        """
        _helpers._del_sub_prop(self._properties, [self._job_type, key])

    def to_api_repr(self):
        """Build an API representation of the job config.

        :rtype: dict
        :returns: A dictionary in the format used by the BigQuery API.
        """
        return copy.deepcopy(self._properties)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a job configuration given its API representation

        :type resource: dict
        :param resource:
            An extract job configuration in the same representation as is
            returned from the API.

        :rtype: :class:`google.cloud.bigquery.job._JobConfig`
        :returns: Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        return config


class LoadJobConfig(_JobConfig):
    """Configuration options for load jobs.

    All properties in this class are optional. Values which are ``None`` ->
    server defaults.
    """

    def __init__(self):
        super(LoadJobConfig, self).__init__('load')

    @property
    def allow_jagged_rows(self):
        """bool: Allow missing trailing optional columns (CSV only).

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.allowJaggedRows
        """
        return self._get_sub_prop('allowJaggedRows')

    @allow_jagged_rows.setter
    def allow_jagged_rows(self, value):
        self._set_sub_prop('allowJaggedRows', value)

    @property
    def allow_quoted_newlines(self):
        """bool: Allow quoted data containing newline characters (CSV only).

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.allowQuotedNewlines
        """
        return self._get_sub_prop('allowQuotedNewlines')

    @allow_quoted_newlines.setter
    def allow_quoted_newlines(self, value):
        self._set_sub_prop('allowQuotedNewlines', value)

    @property
    def autodetect(self):
        """bool: Automatically infer the schema from a sample of the data.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.autodetect
        """
        return self._get_sub_prop('autodetect')

    @autodetect.setter
    def autodetect(self, value):
        self._set_sub_prop('autodetect', value)

    @property
    def create_disposition(self):
        """google.cloud.bigquery.job.CreateDisposition: Specifies behavior
        for creating tables.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.createDisposition
        """
        return self._get_sub_prop('createDisposition')

    @create_disposition.setter
    def create_disposition(self, value):
        self._set_sub_prop('createDisposition', value)

    @property
    def encoding(self):
        """google.cloud.bigquery.job.Encoding: The character encoding of the
        data.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.encoding
        """
        return self._get_sub_prop('encoding')

    @encoding.setter
    def encoding(self, value):
        self._set_sub_prop('encoding', value)

    @property
    def field_delimiter(self):
        """str: The separator for fields in a CSV file.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.fieldDelimiter
        """
        return self._get_sub_prop('fieldDelimiter')

    @field_delimiter.setter
    def field_delimiter(self, value):
        self._set_sub_prop('fieldDelimiter', value)

    @property
    def ignore_unknown_values(self):
        """bool: Ignore extra values not represented in the table schema.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.ignoreUnknownValues
        """
        return self._get_sub_prop('ignoreUnknownValues')

    @ignore_unknown_values.setter
    def ignore_unknown_values(self, value):
        self._set_sub_prop('ignoreUnknownValues', value)

    @property
    def max_bad_records(self):
        """int: Number of invalid rows to ignore.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.maxBadRecords
        """
        return self._get_sub_prop('maxBadRecords')

    @max_bad_records.setter
    def max_bad_records(self, value):
        self._set_sub_prop('maxBadRecords', value)

    @property
    def null_marker(self):
        """str: Represents a null value (CSV only).

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.nullMarker
        """
        return self._get_sub_prop('nullMarker')

    @null_marker.setter
    def null_marker(self, value):
        self._set_sub_prop('nullMarker', value)

    @property
    def quote_character(self):
        """str: Character used to quote data sections (CSV only).

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.quote
        """
        return self._get_sub_prop('quote')

    @quote_character.setter
    def quote_character(self, value):
        self._set_sub_prop('quote', value)

    @property
    def skip_leading_rows(self):
        """int: Number of rows to skip when reading data (CSV only).

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.skipLeadingRows
        """
        return _helpers._int_or_none(self._get_sub_prop('skipLeadingRows'))

    @skip_leading_rows.setter
    def skip_leading_rows(self, value):
        self._set_sub_prop('skipLeadingRows', str(value))

    @property
    def source_format(self):
        """google.cloud.bigquery.job.SourceFormat: File format of the data.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.sourceFormat
        """
        return self._get_sub_prop('sourceFormat')

    @source_format.setter
    def source_format(self, value):
        self._set_sub_prop('sourceFormat', value)

    @property
    def write_disposition(self):
        """google.cloud.bigquery.job.WriteDisposition: Action that occurs if
        the destination table already exists.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.writeDisposition
        """
        return self._get_sub_prop('writeDisposition')

    @write_disposition.setter
    def write_disposition(self, value):
        self._set_sub_prop('writeDisposition', value)

    @property
    def schema(self):
        """List[google.cloud.bigquery.schema.SchemaField]: Schema of the
        destination table.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.schema
        """
        schema = _helpers._get_sub_prop(
            self._properties, ['load', 'schema', 'fields'])
        if schema is None:
            return
        return [SchemaField.from_api_repr(field) for field in schema]

    @schema.setter
    def schema(self, value):
        if not all(hasattr(field, 'to_api_repr') for field in value):
            raise ValueError('Schema items must be fields')
        _helpers._set_sub_prop(
            self._properties,
            ['load', 'schema', 'fields'],
            [field.to_api_repr() for field in value])

    @property
    def destination_encryption_configuration(self):
        """google.cloud.bigquery.table.EncryptionConfiguration: Custom
        encryption configuration for the destination table.

        Custom encryption configuration (e.g., Cloud KMS keys) or ``None``
        if using default encryption.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.destinationEncryptionConfiguration
        """
        prop = self._get_sub_prop('destinationEncryptionConfiguration')
        if prop is not None:
            prop = EncryptionConfiguration.from_api_repr(prop)
        return prop

    @destination_encryption_configuration.setter
    def destination_encryption_configuration(self, value):
        api_repr = value
        if value is not None:
            api_repr = value.to_api_repr()
        self._set_sub_prop('destinationEncryptionConfiguration', api_repr)

    @property
    def time_partitioning(self):
        """google.cloud.bigquery.table.TimePartitioning: Specifies time-based
        partitioning for the destination table.
        """
        prop = self._get_sub_prop('timePartitioning')
        if prop is not None:
            prop = TimePartitioning.from_api_repr(prop)
        return prop

    @time_partitioning.setter
    def time_partitioning(self, value):
        api_repr = value
        if value is not None:
            api_repr = value.to_api_repr()
        self._set_sub_prop('timePartitioning', api_repr)

    @property
    def clustering_fields(self):
        """Union[List[str], None]: Fields defining clustering for the table

        (Defaults to :data:`None`).

        Clustering fields are immutable after table creation.

        .. note::

           As of 2018-06-29, clustering fields cannot be set on a table
           which does not also have time partioning defined.
        """
        prop = self._get_sub_prop('clustering')
        if prop is not None:
            return list(prop.get('fields', ()))

    @clustering_fields.setter
    def clustering_fields(self, value):
        """Union[List[str], None]: Fields defining clustering for the table

        (Defaults to :data:`None`).
        """
        if value is not None:
            self._set_sub_prop('clustering', {'fields': value})
        else:
            self._del_sub_prop('clustering')

    @property
    def schema_update_options(self):
        """List[google.cloud.bigquery.job.SchemaUpdateOption]: Specifies
        updates to the destination table schema to allow as a side effect of
        the load job.
        """
        return self._get_sub_prop('schemaUpdateOptions')

    @schema_update_options.setter
    def schema_update_options(self, values):
        self._set_sub_prop('schemaUpdateOptions', values)


class LoadJob(_AsyncJob):
    """Asynchronous job for loading data into a table.

    Can load from Google Cloud Storage URIs or from a file.

    :type job_id: str
    :param job_id: the job's ID

    :type source_uris: sequence of string or ``NoneType``
    :param source_uris:
        URIs of one or more data files to be loaded.  See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.sourceUris
        for supported URI formats. Pass None for jobs that load from a file.

    :type destination: :class:`google.cloud.bigquery.table.TableReference`
    :param destination: reference to table into which data is to be loaded.

    :type client: :class:`google.cloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).
    """

    _JOB_TYPE = 'load'

    def __init__(self, job_id, source_uris, destination, client,
                 job_config=None):
        super(LoadJob, self).__init__(job_id, client)

        if job_config is None:
            job_config = LoadJobConfig()

        self.source_uris = source_uris
        self.destination = destination
        self._configuration = job_config

    @property
    def allow_jagged_rows(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.allow_jagged_rows`.
        """
        return self._configuration.allow_jagged_rows

    @property
    def allow_quoted_newlines(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.allow_quoted_newlines`.
        """
        return self._configuration.allow_quoted_newlines

    @property
    def autodetect(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.autodetect`.
        """
        return self._configuration.autodetect

    @property
    def create_disposition(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.create_disposition`.
        """
        return self._configuration.create_disposition

    @property
    def encoding(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.encoding`.
        """
        return self._configuration.encoding

    @property
    def field_delimiter(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.field_delimiter`.
        """
        return self._configuration.field_delimiter

    @property
    def ignore_unknown_values(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.ignore_unknown_values`.
        """
        return self._configuration.ignore_unknown_values

    @property
    def max_bad_records(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.max_bad_records`.
        """
        return self._configuration.max_bad_records

    @property
    def null_marker(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.null_marker`.
        """
        return self._configuration.null_marker

    @property
    def quote_character(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.quote_character`.
        """
        return self._configuration.quote_character

    @property
    def skip_leading_rows(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.skip_leading_rows`.
        """
        return self._configuration.skip_leading_rows

    @property
    def source_format(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.source_format`.
        """
        return self._configuration.source_format

    @property
    def write_disposition(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.write_disposition`.
        """
        return self._configuration.write_disposition

    @property
    def schema(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.schema`.
        """
        return self._configuration.schema

    @property
    def destination_encryption_configuration(self):
        """google.cloud.bigquery.table.EncryptionConfiguration: Custom
        encryption configuration for the destination table.

        Custom encryption configuration (e.g., Cloud KMS keys)
        or ``None`` if using default encryption.

        See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.destination_encryption_configuration`.
        """
        return self._configuration.destination_encryption_configuration

    @property
    def time_partitioning(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.time_partitioning`.
        """
        return self._configuration.time_partitioning

    @property
    def clustering_fields(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.clustering_fields`.
        """
        return self._configuration.clustering_fields

    @property
    def schema_update_options(self):
        """See
        :attr:`google.cloud.bigquery.job.LoadJobConfig.schema_update_options`.
        """
        return self._configuration.schema_update_options

    @property
    def input_file_bytes(self):
        """Count of bytes loaded from source files.

        :rtype: int, or ``NoneType``
        :returns: the count (None until set from the server).
        :raises: ValueError for invalid value types.
        """
        statistics = self._properties.get('statistics')
        if statistics is not None:
            return int(statistics['load']['inputFileBytes'])

    @property
    def input_files(self):
        """Count of source files.

        :rtype: int, or ``NoneType``
        :returns: the count (None until set from the server).
        """
        statistics = self._properties.get('statistics')
        if statistics is not None:
            return int(statistics['load']['inputFiles'])

    @property
    def output_bytes(self):
        """Count of bytes saved to destination table.

        :rtype: int, or ``NoneType``
        :returns: the count (None until set from the server).
        """
        statistics = self._properties.get('statistics')
        if statistics is not None:
            return int(statistics['load']['outputBytes'])

    @property
    def output_rows(self):
        """Count of rows saved to destination table.

        :rtype: int, or ``NoneType``
        :returns: the count (None until set from the server).
        """
        statistics = self._properties.get('statistics')
        if statistics is not None:
            return int(statistics['load']['outputRows'])

    def _build_resource(self):
        """Generate a resource for :meth:`_begin`."""
        configuration = self._configuration.to_api_repr()
        if self.source_uris is not None:
            _helpers._set_sub_prop(
                configuration, ['load', 'sourceUris'], self.source_uris)
        _helpers._set_sub_prop(
            configuration,
            ['load', 'destinationTable'],
            self.destination.to_api_repr())

        return {
            'jobReference': self._properties['jobReference'],
            'configuration': configuration,
        }

    def _copy_configuration_properties(self, configuration):
        """Helper:  assign subclass configuration properties in cleaned."""
        self._configuration._properties = copy.deepcopy(configuration)

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a job given its API representation

        .. note:

           This method assumes that the project found in the resource matches
           the client's project.

        :type resource: dict
        :param resource: dataset job representation returned from the API

        :type client: :class:`google.cloud.bigquery.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the dataset.

        :rtype: :class:`google.cloud.bigquery.job.LoadJob`
        :returns: Job parsed from ``resource``.
        """
        config_resource = resource.get('configuration', {})
        config = LoadJobConfig.from_api_repr(config_resource)
        # A load job requires a destination table.
        dest_config = config_resource['load']['destinationTable']
        ds_ref = DatasetReference(
            dest_config['projectId'], dest_config['datasetId'])
        destination = TableReference(ds_ref, dest_config['tableId'])
        # sourceUris will be absent if this is a file upload.
        source_uris = _helpers._get_sub_prop(
            config_resource, ['load', 'sourceUris'])
        job_ref = _JobReference._from_api_repr(resource['jobReference'])
        job = cls(job_ref, source_uris, destination, client, config)
        job._set_properties(resource)
        return job


class CopyJobConfig(_JobConfig):
    """Configuration options for copy jobs.

    All properties in this class are optional. Values which are ``None`` ->
    server defaults.
    """

    def __init__(self):
        super(CopyJobConfig, self).__init__('copy')

    @property
    def create_disposition(self):
        """google.cloud.bigquery.job.CreateDisposition: Specifies behavior
        for creating tables.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.copy.createDisposition
        """
        return self._get_sub_prop('createDisposition')

    @create_disposition.setter
    def create_disposition(self, value):
        self._set_sub_prop('createDisposition', value)

    @property
    def write_disposition(self):
        """google.cloud.bigquery.job.WriteDisposition: Action that occurs if
        the destination table already exists.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.copy.writeDisposition
        """
        return self._get_sub_prop('writeDisposition')

    @write_disposition.setter
    def write_disposition(self, value):
        self._set_sub_prop('writeDisposition', value)

    @property
    def destination_encryption_configuration(self):
        """google.cloud.bigquery.table.EncryptionConfiguration: Custom
        encryption configuration for the destination table.

        Custom encryption configuration (e.g., Cloud KMS keys) or ``None``
        if using default encryption.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.copy.destinationEncryptionConfiguration
        """
        prop = self._get_sub_prop('destinationEncryptionConfiguration')
        if prop is not None:
            prop = EncryptionConfiguration.from_api_repr(prop)
        return prop

    @destination_encryption_configuration.setter
    def destination_encryption_configuration(self, value):
        api_repr = value
        if value is not None:
            api_repr = value.to_api_repr()
        self._set_sub_prop('destinationEncryptionConfiguration', api_repr)


class CopyJob(_AsyncJob):
    """Asynchronous job: copy data into a table from other tables.

    :type job_id: str
    :param job_id: the job's ID, within the project belonging to ``client``.

    :type sources: list of :class:`google.cloud.bigquery.table.TableReference`
    :param sources: Table from which data is to be loaded.

    :type destination: :class:`google.cloud.bigquery.table.TableReference`
    :param destination: Table into which data is to be loaded.

    :type client: :class:`google.cloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).

    :type job_config: :class:`~google.cloud.bigquery.job.CopyJobConfig`
    :param job_config:
        (Optional) Extra configuration options for the copy job.
    """
    _JOB_TYPE = 'copy'

    def __init__(self, job_id, sources, destination, client, job_config=None):
        super(CopyJob, self).__init__(job_id, client)

        if job_config is None:
            job_config = CopyJobConfig()

        self.destination = destination
        self.sources = sources
        self._configuration = job_config

    @property
    def create_disposition(self):
        """See
        :attr:`google.cloud.bigquery.job.CopyJobConfig.create_disposition`.
        """
        return self._configuration.create_disposition

    @property
    def write_disposition(self):
        """See
        :attr:`google.cloud.bigquery.job.CopyJobConfig.write_disposition`.
        """
        return self._configuration.write_disposition

    @property
    def destination_encryption_configuration(self):
        """google.cloud.bigquery.table.EncryptionConfiguration: Custom
        encryption configuration for the destination table.

        Custom encryption configuration (e.g., Cloud KMS keys) or ``None``
        if using default encryption.

        See
        :attr:`google.cloud.bigquery.job.CopyJobConfig.destination_encryption_configuration`.
        """
        return self._configuration.destination_encryption_configuration

    def _build_resource(self):
        """Generate a resource for :meth:`_begin`."""

        source_refs = [{
            'projectId': table.project,
            'datasetId': table.dataset_id,
            'tableId': table.table_id,
        } for table in self.sources]

        configuration = self._configuration.to_api_repr()
        _helpers._set_sub_prop(
            configuration, ['copy', 'sourceTables'], source_refs)
        _helpers._set_sub_prop(
            configuration,
            ['copy', 'destinationTable'],
            {
                'projectId': self.destination.project,
                'datasetId': self.destination.dataset_id,
                'tableId': self.destination.table_id,
            })

        return {
            'jobReference': self._properties['jobReference'],
            'configuration': configuration,
        }

    def _copy_configuration_properties(self, configuration):
        """Helper:  assign subclass configuration properties in cleaned."""
        self._configuration._properties = copy.deepcopy(configuration)

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a job given its API representation

        .. note:

           This method assumes that the project found in the resource matches
           the client's project.

        :type resource: dict
        :param resource: dataset job representation returned from the API

        :type client: :class:`google.cloud.bigquery.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the dataset.

        :rtype: :class:`google.cloud.bigquery.job.CopyJob`
        :returns: Job parsed from ``resource``.
        """
        job_id, config_resource = cls._get_resource_config(resource)
        config = CopyJobConfig.from_api_repr(config_resource)
        # Copy required fields to the job.
        copy_resource = config_resource['copy']
        destination = TableReference.from_api_repr(
            copy_resource['destinationTable'])
        sources = []
        source_configs = copy_resource.get('sourceTables')
        if source_configs is None:
            single = copy_resource.get('sourceTable')
            if single is None:
                raise KeyError(
                    "Resource missing 'sourceTables' / 'sourceTable'")
            source_configs = [single]
        for source_config in source_configs:
            table_ref = TableReference.from_api_repr(source_config)
            sources.append(table_ref)
        job = cls(
            job_id, sources, destination, client=client, job_config=config)
        job._set_properties(resource)
        return job


class ExtractJobConfig(_JobConfig):
    """Configuration options for extract jobs.

    All properties in this class are optional. Values which are ``None`` ->
    server defaults.
    """

    def __init__(self):
        super(ExtractJobConfig, self).__init__('extract')

    @property
    def compression(self):
        """google.cloud.bigquery.job.Compression: Compression type to use for
        exported files.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.extract.compression
        """
        return self._get_sub_prop('compression')

    @compression.setter
    def compression(self, value):
        self._set_sub_prop('compression', value)

    @property
    def destination_format(self):
        """google.cloud.bigquery.job.DestinationFormat: Exported file format.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.extract.destinationFormat
        """
        return self._get_sub_prop('destinationFormat')

    @destination_format.setter
    def destination_format(self, value):
        self._set_sub_prop('destinationFormat', value)

    @property
    def field_delimiter(self):
        """str: Delimiter to use between fields in the exported data.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.extract.fieldDelimiter
        """
        return self._get_sub_prop('fieldDelimiter')

    @field_delimiter.setter
    def field_delimiter(self, value):
        self._set_sub_prop('fieldDelimiter', value)

    @property
    def print_header(self):
        """bool: Print a header row in the exported data.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.extract.printHeader
        """
        return self._get_sub_prop('printHeader')

    @print_header.setter
    def print_header(self, value):
        self._set_sub_prop('printHeader', value)


class ExtractJob(_AsyncJob):
    """Asynchronous job: extract data from a table into Cloud Storage.

    :type job_id: str
    :param job_id: the job's ID

    :type source: :class:`google.cloud.bigquery.table.TableReference`
    :param source: Table into which data is to be loaded.

    :type destination_uris: list of string
    :param destination_uris:
        URIs describing where the extracted data will be written in Cloud
        Storage, using the format ``gs://<bucket_name>/<object_name_or_glob>``.

    :type client: :class:`google.cloud.bigquery.client.Client`
    :param client:
        A client which holds credentials and project configuration.

    :type job_config: :class:`~google.cloud.bigquery.job.ExtractJobConfig`
    :param job_config:
        (Optional) Extra configuration options for the extract job.
    """
    _JOB_TYPE = 'extract'

    def __init__(
            self, job_id, source, destination_uris, client, job_config=None):
        super(ExtractJob, self).__init__(job_id, client)

        if job_config is None:
            job_config = ExtractJobConfig()

        self.source = source
        self.destination_uris = destination_uris
        self._configuration = job_config

    @property
    def compression(self):
        """See
        :attr:`google.cloud.bigquery.job.ExtractJobConfig.compression`.
        """
        return self._configuration.compression

    @property
    def destination_format(self):
        """See
        :attr:`google.cloud.bigquery.job.ExtractJobConfig.destination_format`.
        """
        return self._configuration.destination_format

    @property
    def field_delimiter(self):
        """See
        :attr:`google.cloud.bigquery.job.ExtractJobConfig.field_delimiter`.
        """
        return self._configuration.field_delimiter

    @property
    def print_header(self):
        """See
        :attr:`google.cloud.bigquery.job.ExtractJobConfig.print_header`.
        """
        return self._configuration.print_header

    @property
    def destination_uri_file_counts(self):
        """Return file counts from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.extract.destinationUriFileCounts

        Returns:
            a list of integer counts, each representing the number of files
            per destination URI or URI pattern specified in the extract
            configuration. These values will be in the same order as the URIs
            specified in the 'destinationUris' field.  Returns None if job is
            not yet complete.
        """
        counts = self._job_statistics().get('destinationUriFileCounts')
        if counts is not None:
            return [int(count) for count in counts]
        return None

    def _build_resource(self):
        """Generate a resource for :meth:`_begin`."""

        source_ref = {
            'projectId': self.source.project,
            'datasetId': self.source.dataset_id,
            'tableId': self.source.table_id,
        }

        configuration = self._configuration.to_api_repr()
        _helpers._set_sub_prop(
            configuration, ['extract', 'sourceTable'], source_ref)
        _helpers._set_sub_prop(
            configuration,
            ['extract', 'destinationUris'],
            self.destination_uris)

        return {
            'jobReference': self._properties['jobReference'],
            'configuration': configuration,
        }

    def _copy_configuration_properties(self, configuration):
        """Helper:  assign subclass configuration properties in cleaned."""
        self._configuration._properties = copy.deepcopy(configuration)

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a job given its API representation

        .. note:

           This method assumes that the project found in the resource matches
           the client's project.

        :type resource: dict
        :param resource: dataset job representation returned from the API

        :type client: :class:`google.cloud.bigquery.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the dataset.

        :rtype: :class:`google.cloud.bigquery.job.ExtractJob`
        :returns: Job parsed from ``resource``.
        """
        job_id, config_resource = cls._get_resource_config(resource)
        config = ExtractJobConfig.from_api_repr(config_resource)
        source_config = _helpers._get_sub_prop(
            config_resource, ['extract', 'sourceTable'])
        dataset = DatasetReference(
            source_config['projectId'], source_config['datasetId'])
        source = dataset.table(source_config['tableId'])
        destination_uris = _helpers._get_sub_prop(
            config_resource, ['extract', 'destinationUris'])

        job = cls(
            job_id, source, destination_uris, client=client, job_config=config)
        job._set_properties(resource)
        return job


def _from_api_repr_query_parameters(resource):
    return [
        _query_param_from_api_repr(mapping)
        for mapping in resource
    ]


def _to_api_repr_query_parameters(value):
    return [
        query_parameter.to_api_repr()
        for query_parameter in value
    ]


def _from_api_repr_udf_resources(resource):
    udf_resources = []
    for udf_mapping in resource:
        for udf_type, udf_value in udf_mapping.items():
            udf_resources.append(UDFResource(udf_type, udf_value))
    return udf_resources


def _to_api_repr_udf_resources(value):
    return [
        {udf_resource.udf_type: udf_resource.value}
        for udf_resource in value
    ]


def _from_api_repr_table_defs(resource):
    return {k: ExternalConfig.from_api_repr(v) for k, v in resource.items()}


def _to_api_repr_table_defs(value):
    return {k: ExternalConfig.to_api_repr(v) for k, v in value.items()}


class QueryJobConfig(_JobConfig):
    """Configuration options for query jobs.

    All properties in this class are optional. Values which are ``None`` ->
    server defaults.
    """

    def __init__(self):
        super(QueryJobConfig, self).__init__('query')

    @property
    def destination_encryption_configuration(self):
        """google.cloud.bigquery.table.EncryptionConfiguration: Custom
        encryption configuration for the destination table.

        Custom encryption configuration (e.g., Cloud KMS keys) or ``None``
        if using default encryption.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.destinationEncryptionConfiguration
        """
        prop = self._get_sub_prop('destinationEncryptionConfiguration')
        if prop is not None:
            prop = EncryptionConfiguration.from_api_repr(prop)
        return prop

    @destination_encryption_configuration.setter
    def destination_encryption_configuration(self, value):
        api_repr = value
        if value is not None:
            api_repr = value.to_api_repr()
        self._set_sub_prop('destinationEncryptionConfiguration', api_repr)

    @property
    def allow_large_results(self):
        """bool: Allow large query results tables (legacy SQL, only)

        See
        https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.allowLargeResults
        """
        return self._get_sub_prop('allowLargeResults')

    @allow_large_results.setter
    def allow_large_results(self, value):
        self._set_sub_prop('allowLargeResults', value)

    @property
    def create_disposition(self):
        """google.cloud.bigquery.job.CreateDisposition: Specifies behavior
        for creating tables.

        See
        https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.createDisposition
        """
        return self._get_sub_prop('createDisposition')

    @create_disposition.setter
    def create_disposition(self, value):
        self._set_sub_prop('createDisposition', value)

    @property
    def default_dataset(self):
        """google.cloud.bigquery.dataset.DatasetReference: the default dataset
        to use for unqualified table names in the query or ``None`` if not set.

        See
        https://g.co/cloud/bigquery/docs/reference/v2/jobs#configuration.query.defaultDataset
        """
        prop = self._get_sub_prop('defaultDataset')
        if prop is not None:
            prop = DatasetReference.from_api_repr(prop)
        return prop

    @default_dataset.setter
    def default_dataset(self, value):
        resource = None
        if value is not None:
            resource = value.to_api_repr()
        self._set_sub_prop('defaultDataset', resource)

    @property
    def destination(self):
        """google.cloud.bigquery.table.TableReference: table where results are
        written or ``None`` if not set.

        See
        https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.destinationTable
        """
        prop = self._get_sub_prop('destinationTable')
        if prop is not None:
            prop = TableReference.from_api_repr(prop)
        return prop

    @destination.setter
    def destination(self, value):
        resource = None
        if value is not None:
            resource = value.to_api_repr()
        self._set_sub_prop('destinationTable', resource)

    @property
    def dry_run(self):
        """bool: ``True`` if this query should be a dry run to estimate costs.

        See
        https://g.co/cloud/bigquery/docs/reference/v2/jobs#configuration.dryRun
        """
        return self._properties.get('dryRun')

    @dry_run.setter
    def dry_run(self, value):
        self._properties['dryRun'] = value

    @property
    def flatten_results(self):
        """bool: Flatten nested/repeated fields in results. (Legacy SQL only)

        See
        https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.flattenResults
        """
        return self._get_sub_prop('flattenResults')

    @flatten_results.setter
    def flatten_results(self, value):
        self._set_sub_prop('flattenResults', value)

    @property
    def maximum_billing_tier(self):
        """int: Deprecated. Changes the billing tier to allow high-compute
        queries.

        See
        https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.maximumBillingTier
        """
        return self._get_sub_prop('maximumBillingTier')

    @maximum_billing_tier.setter
    def maximum_billing_tier(self, value):
        self._set_sub_prop('maximumBillingTier', value)

    @property
    def maximum_bytes_billed(self):
        """int: Maximum bytes to be billed for this job or ``None`` if not set.

        See
        https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.maximumBytesBilled
        """
        return _helpers._int_or_none(self._get_sub_prop('maximumBytesBilled'))

    @maximum_bytes_billed.setter
    def maximum_bytes_billed(self, value):
        self._set_sub_prop('maximumBytesBilled', str(value))

    @property
    def priority(self):
        """google.cloud.bigquery.job.QueryPriority: Priority of the query.

        See
        https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.priority
        """
        return self._get_sub_prop('priority')

    @priority.setter
    def priority(self, value):
        self._set_sub_prop('priority', value)

    @property
    def query_parameters(self):
        """List[Union[google.cloud.bigquery.query.ArrayQueryParameter, \
        google.cloud.bigquery.query.ScalarQueryParameter, \
        google.cloud.bigquery.query.StructQueryParameter]]: list of parameters
        for parameterized query (empty by default)

        See:
        https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.queryParameters
        """
        prop = self._get_sub_prop('queryParameters', default=[])
        return _from_api_repr_query_parameters(prop)

    @query_parameters.setter
    def query_parameters(self, values):
        self._set_sub_prop(
            'queryParameters', _to_api_repr_query_parameters(values))

    @property
    def udf_resources(self):
        """List[google.cloud.bigquery.query.UDFResource]: user
        defined function resources (empty by default)

        See:
        https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.userDefinedFunctionResources
        """
        prop = self._get_sub_prop('userDefinedFunctionResources', default=[])
        return _from_api_repr_udf_resources(prop)

    @udf_resources.setter
    def udf_resources(self, values):
        self._set_sub_prop(
            'userDefinedFunctionResources',
            _to_api_repr_udf_resources(values))

    @property
    def use_legacy_sql(self):
        """bool: Use legacy SQL syntax.

        See
        https://g.co/cloud/bigquery/docs/reference/v2/jobs#configuration.query.useLegacySql
        """
        return self._get_sub_prop('useLegacySql')

    @use_legacy_sql.setter
    def use_legacy_sql(self, value):
        self._set_sub_prop('useLegacySql', value)

    @property
    def use_query_cache(self):
        """bool: Look for the query result in the cache.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.useQueryCache
        """
        return self._get_sub_prop('useQueryCache')

    @use_query_cache.setter
    def use_query_cache(self, value):
        self._set_sub_prop('useQueryCache', value)

    @property
    def write_disposition(self):
        """google.cloud.bigquery.job.WriteDisposition: Action that occurs if
        the destination table already exists.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.writeDisposition
        """
        return self._get_sub_prop('writeDisposition')

    @write_disposition.setter
    def write_disposition(self, value):
        self._set_sub_prop('writeDisposition', value)

    @property
    def table_definitions(self):
        """Dict[str, google.cloud.bigquery.external_config.ExternalConfig]:
        Definitions for external tables or ``None`` if not set.

        See
        https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions
        """
        prop = self._get_sub_prop('tableDefinitions')
        if prop is not None:
            prop = _from_api_repr_table_defs(prop)
        return prop

    @table_definitions.setter
    def table_definitions(self, values):
        self._set_sub_prop(
            'tableDefinitions',  _to_api_repr_table_defs(values))

    @property
    def time_partitioning(self):
        """google.cloud.bigquery.table.TimePartitioning: Specifies time-based
        partitioning for the destination table.
        """
        prop = self._get_sub_prop('timePartitioning')
        if prop is not None:
            prop = TimePartitioning.from_api_repr(prop)
        return prop

    @time_partitioning.setter
    def time_partitioning(self, value):
        api_repr = value
        if value is not None:
            api_repr = value.to_api_repr()
        self._set_sub_prop('timePartitioning', api_repr)

    @property
    def clustering_fields(self):
        """Union[List[str], None]: Fields defining clustering for the table

        (Defaults to :data:`None`).

        Clustering fields are immutable after table creation.

        .. note::

           As of 2018-06-29, clustering fields cannot be set on a table
           which does not also have time partioning defined.
        """
        prop = self._get_sub_prop('clustering')
        if prop is not None:
            return list(prop.get('fields', ()))

    @clustering_fields.setter
    def clustering_fields(self, value):
        """Union[List[str], None]: Fields defining clustering for the table

        (Defaults to :data:`None`).
        """
        if value is not None:
            self._set_sub_prop('clustering', {'fields': value})
        else:
            self._del_sub_prop('clustering')

    @property
    def schema_update_options(self):
        """List[google.cloud.bigquery.job.SchemaUpdateOption]: Specifies
        updates to the destination table schema to allow as a side effect of
        the query job.
        """
        return self._get_sub_prop('schemaUpdateOptions')

    @schema_update_options.setter
    def schema_update_options(self, values):
        self._set_sub_prop('schemaUpdateOptions', values)

    def to_api_repr(self):
        """Build an API representation of the query job config.

        Returns:
            dict: A dictionary in the format used by the BigQuery API.
        """
        resource = copy.deepcopy(self._properties)

        # Query parameters have an addition property associated with them
        # to indicate if the query is using named or positional parameters.
        query_parameters = resource['query'].get('queryParameters')
        if query_parameters:
            if query_parameters[0].get('name') is None:
                resource['query']['parameterMode'] = 'POSITIONAL'
            else:
                resource['query']['parameterMode'] = 'NAMED'

        return resource


class QueryJob(_AsyncJob):
    """Asynchronous job: query tables.

    :type job_id: str
    :param job_id: the job's ID, within the project belonging to ``client``.

    :type query: str
    :param query: SQL query string

    :type client: :class:`google.cloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).

    :type job_config: :class:`~google.cloud.bigquery.job.QueryJobConfig`
    :param job_config:
        (Optional) Extra configuration options for the query job.
    """
    _JOB_TYPE = 'query'
    _UDF_KEY = 'userDefinedFunctionResources'

    def __init__(self, job_id, query, client, job_config=None):
        super(QueryJob, self).__init__(job_id, client)

        if job_config is None:
            job_config = QueryJobConfig()
        if job_config.use_legacy_sql is None:
            job_config.use_legacy_sql = False

        self.query = query
        self._configuration = job_config
        self._query_results = None
        self._done_timeout = None

    @property
    def allow_large_results(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.allow_large_results`.
        """
        return self._configuration.allow_large_results

    @property
    def create_disposition(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.create_disposition`.
        """
        return self._configuration.create_disposition

    @property
    def default_dataset(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.default_dataset`.
        """
        return self._configuration.default_dataset

    @property
    def destination(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.destination`.
        """
        return self._configuration.destination

    @property
    def destination_encryption_configuration(self):
        """google.cloud.bigquery.table.EncryptionConfiguration: Custom
        encryption configuration for the destination table.

        Custom encryption configuration (e.g., Cloud KMS keys) or ``None``
        if using default encryption.

        See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.destination_encryption_configuration`.
        """
        return self._configuration.destination_encryption_configuration

    @property
    def dry_run(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.dry_run`.
        """
        return self._configuration.dry_run

    @property
    def flatten_results(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.flatten_results`.
        """
        return self._configuration.flatten_results

    @property
    def priority(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.priority`.
        """
        return self._configuration.priority

    @property
    def query_parameters(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.query_parameters`.
        """
        return self._configuration.query_parameters

    @property
    def udf_resources(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.udf_resources`.
        """
        return self._configuration.udf_resources

    @property
    def use_legacy_sql(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.use_legacy_sql`.
        """
        return self._configuration.use_legacy_sql

    @property
    def use_query_cache(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.use_query_cache`.
        """
        return self._configuration.use_query_cache

    @property
    def write_disposition(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.write_disposition`.
        """
        return self._configuration.write_disposition

    @property
    def maximum_billing_tier(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.maximum_billing_tier`.
        """
        return self._configuration.maximum_billing_tier

    @property
    def maximum_bytes_billed(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.maximum_bytes_billed`.
        """
        return self._configuration.maximum_bytes_billed

    @property
    def table_definitions(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.table_definitions`.
        """
        return self._configuration.table_definitions

    @property
    def time_partitioning(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.time_partitioning`.
        """
        return self._configuration.time_partitioning

    @property
    def clustering_fields(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.clustering_fields`.
        """
        return self._configuration.clustering_fields

    @property
    def schema_update_options(self):
        """See
        :attr:`google.cloud.bigquery.job.QueryJobConfig.schema_update_options`.
        """
        return self._configuration.schema_update_options

    def _build_resource(self):
        """Generate a resource for :meth:`_begin`."""
        configuration = self._configuration.to_api_repr()

        resource = {
            'jobReference': self._properties['jobReference'],
            'configuration': configuration,
        }
        configuration['query']['query'] = self.query

        return resource

    def _copy_configuration_properties(self, configuration):
        """Helper:  assign subclass configuration properties in cleaned."""
        self._configuration._properties = copy.deepcopy(configuration)
        self.query = _helpers._get_sub_prop(configuration, ['query', 'query'])

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a job given its API representation

        :type resource: dict
        :param resource: dataset job representation returned from the API

        :type client: :class:`google.cloud.bigquery.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the dataset.

        :rtype: :class:`google.cloud.bigquery.job.QueryJob`
        :returns: Job parsed from ``resource``.
        """
        job_id, config = cls._get_resource_config(resource)
        query = config['query']['query']
        job = cls(job_id, query, client=client)
        job._set_properties(resource)
        return job

    @property
    def query_plan(self):
        """Return query plan from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.queryPlan

        :rtype: list of :class:`QueryPlanEntry`
        :returns: mappings describing the query plan, or an empty list
                  if the query has not yet completed.
        """
        plan_entries = self._job_statistics().get('queryPlan', ())
        return [QueryPlanEntry.from_api_repr(entry) for entry in plan_entries]

    @property
    def timeline(self):
        """List(TimelineEntry): Return the query execution timeline
        from job statistics.
        """
        raw = self._job_statistics().get('timeline', ())
        return [TimelineEntry.from_api_repr(entry) for entry in raw]

    @property
    def total_bytes_processed(self):
        """Return total bytes processed from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.totalBytesProcessed

        :rtype: int or None
        :returns: total bytes processed by the job, or None if job is not
                  yet complete.
        """
        result = self._job_statistics().get('totalBytesProcessed')
        if result is not None:
            result = int(result)
        return result

    @property
    def total_bytes_billed(self):
        """Return total bytes billed from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.totalBytesBilled

        :rtype: int or None
        :returns: total bytes processed by the job, or None if job is not
                  yet complete.
        """
        result = self._job_statistics().get('totalBytesBilled')
        if result is not None:
            result = int(result)
        return result

    @property
    def billing_tier(self):
        """Return billing tier from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.billingTier

        :rtype: int or None
        :returns: billing tier used by the job, or None if job is not
                  yet complete.
        """
        return self._job_statistics().get('billingTier')

    @property
    def cache_hit(self):
        """Return whether or not query results were served from cache.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.cacheHit

        :rtype: bool or None
        :returns: whether the query results were returned from cache, or None
                  if job is not yet complete.
        """
        return self._job_statistics().get('cacheHit')

    @property
    def ddl_operation_performed(self):
        """Optional[str]: Return the DDL operation performed.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.ddlOperationPerformed

        """
        return self._job_statistics().get('ddlOperationPerformed')

    @property
    def ddl_target_table(self):
        """Optional[TableReference]: Return the DDL target table, present
            for CREATE/DROP TABLE/VIEW queries.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.ddlTargetTable
        """
        prop = self._job_statistics().get('ddlTargetTable')
        if prop is not None:
            prop = TableReference.from_api_repr(prop)
        return prop

    @property
    def num_dml_affected_rows(self):
        """Return the number of DML rows affected by the job.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.numDmlAffectedRows

        :rtype: int or None
        :returns: number of DML rows affected by the job, or None if job is not
                  yet complete.
        """
        result = self._job_statistics().get('numDmlAffectedRows')
        if result is not None:
            result = int(result)
        return result

    @property
    def slot_millis(self):
        """Union[int, None]: Slot-milliseconds used by this query job."""
        return _helpers._int_or_none(self._job_statistics().get('totalSlotMs'))

    @property
    def statement_type(self):
        """Return statement type from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.statementType

        :rtype: str or None
        :returns: type of statement used by the job, or None if job is not
                  yet complete.
        """
        return self._job_statistics().get('statementType')

    @property
    def referenced_tables(self):
        """Return referenced tables from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.referencedTables

        :rtype: list of dict
        :returns: mappings describing the query plan, or an empty list
                  if the query has not yet completed.
        """
        tables = []
        datasets_by_project_name = {}

        for table in self._job_statistics().get('referencedTables', ()):

            t_project = table['projectId']

            ds_id = table['datasetId']
            t_dataset = datasets_by_project_name.get((t_project, ds_id))
            if t_dataset is None:
                t_dataset = DatasetReference(t_project, ds_id)
                datasets_by_project_name[(t_project, ds_id)] = t_dataset

            t_name = table['tableId']
            tables.append(t_dataset.table(t_name))

        return tables

    @property
    def undeclared_query_parameters(self):
        """Return undeclared query parameters from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.undeclaredQueryParameters

        :rtype:
            list of
            :class:`~google.cloud.bigquery.ArrayQueryParameter`,
            :class:`~google.cloud.bigquery.ScalarQueryParameter`, or
            :class:`~google.cloud.bigquery.StructQueryParameter`
        :returns: undeclared parameters, or an empty list if the query has
                  not yet completed.
        """
        parameters = []
        undeclared = self._job_statistics().get(
            'undeclaredQueryParameters', ())

        for parameter in undeclared:
            p_type = parameter['parameterType']

            if 'arrayType' in p_type:
                klass = ArrayQueryParameter
            elif 'structTypes' in p_type:
                klass = StructQueryParameter
            else:
                klass = ScalarQueryParameter

            parameters.append(klass.from_api_repr(parameter))

        return parameters

    @property
    def estimated_bytes_processed(self):
        """Return the estimated number of bytes processed by the query.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.estimatedBytesProcessed

        :rtype: int or None
        :returns: number of DML rows affected by the job, or None if job is not
                  yet complete.
        """
        result = self._job_statistics().get('estimatedBytesProcessed')
        if result is not None:
            result = int(result)
        return result

    def done(self, retry=DEFAULT_RETRY):
        """Refresh the job and checks if it is complete.

        :rtype: bool
        :returns: True if the job is complete, False otherwise.
        """
        # Since the API to getQueryResults can hang up to the timeout value
        # (default of 10 seconds), set the timeout parameter to ensure that
        # the timeout from the futures API is respected. See:
        # https://github.com/GoogleCloudPlatform/google-cloud-python/issues/4135
        timeout_ms = None
        if self._done_timeout is not None:
            # Subtract a buffer for context switching, network latency, etc.
            timeout = self._done_timeout - _TIMEOUT_BUFFER_SECS
            timeout = max(min(timeout, 10), 0)
            self._done_timeout -= timeout
            self._done_timeout = max(0, self._done_timeout)
            timeout_ms = int(timeout * 1000)

        # Do not refresh is the state is already done, as the job will not
        # change once complete.
        if self.state != _DONE_STATE:
            self._query_results = self._client._get_query_results(
                self.job_id, retry,
                project=self.project, timeout_ms=timeout_ms,
                location=self.location)

            # Only reload the job once we know the query is complete.
            # This will ensure that fields such as the destination table are
            # correctly populated.
            if self._query_results.complete:
                self.reload(retry=retry)

        return self.state == _DONE_STATE

    def _blocking_poll(self, timeout=None):
        self._done_timeout = timeout
        super(QueryJob, self)._blocking_poll(timeout=timeout)

    def result(self, timeout=None, retry=DEFAULT_RETRY):
        """Start the job and wait for it to complete and get the result.

        :type timeout: float
        :param timeout:
            How long (in seconds) to wait for job to complete before raising
            a :class:`concurrent.futures.TimeoutError`.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the call that retrieves rows.

        :rtype: :class:`~google.cloud.bigquery.table.RowIterator`
        :returns:
            Iterator of row data :class:`~google.cloud.bigquery.table.Row`-s.
            During each page, the iterator will have the ``total_rows``
            attribute set, which counts the total number of rows **in the
            result set** (this is distinct from the total number of rows in
            the current page: ``iterator.page.num_items``).

        :raises:
            :class:`~google.cloud.exceptions.GoogleCloudError` if the job
            failed or :class:`concurrent.futures.TimeoutError` if the job did
            not complete in the given timeout.
        """
        super(QueryJob, self).result(timeout=timeout)
        # Return an iterator instead of returning the job.
        if not self._query_results:
            self._query_results = self._client._get_query_results(
                self.job_id, retry, project=self.project,
                location=self.location)

        # If the query job is complete but there are no query results, this was
        # special job, such as a DDL query. Return an empty result set to
        # indicate success and avoid calling tabledata.list on a table which
        # can't be read (such as a view table).
        if self._query_results.total_rows is None:
            return _EmptyRowIterator()

        schema = self._query_results.schema
        dest_table_ref = self.destination
        dest_table = Table(dest_table_ref, schema=schema)
        return self._client.list_rows(dest_table, retry=retry)

    def to_dataframe(self):
        """Return a pandas DataFrame from a QueryJob

        Returns:
            A :class:`~pandas.DataFrame` populated with row data and column
            headers from the query results. The column headers are derived
            from the destination table's schema.

        Raises:
            ValueError: If the `pandas` library cannot be imported.
        """
        return self.result().to_dataframe()

    def __iter__(self):
        return iter(self.result())


class QueryPlanEntryStep(object):
    """Map a single step in a query plan entry.

    :type kind: str
    :param kind: step type

    :type substeps:
    :param substeps: names of substeps
    """
    def __init__(self, kind, substeps):
        self.kind = kind
        self.substeps = list(substeps)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct instance from the JSON repr.

        :type resource: dict
        :param resource: JSON representation of the entry

        :rtype: :class:`QueryPlanEntryStep`
        :return: new instance built from the resource
        """
        return cls(
            kind=resource.get('kind'),
            substeps=resource.get('substeps', ()),
        )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.kind == other.kind and self.substeps == other.substeps


class QueryPlanEntry(object):
    """QueryPlanEntry represents a single stage of a query execution plan.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs
    for the underlying API representation within query statistics.

    """

    def __init__(self):
        self._properties = {}

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct instance from the JSON repr.

        Args:
            resource(Dict[str: object]):
                ExplainQueryStage representation returned from API

        Returns:
            google.cloud.bigquery.QueryPlanEntry:
                Query plan entry parsed from ``resource``
        """
        entry = cls()
        entry._properties = resource
        return entry

    @property
    def name(self):
        """Union[str, None]: Human-readable name of the stage."""
        return self._properties.get('name')

    @property
    def entry_id(self):
        """Union[str, None]: Unique ID for the stage within the plan."""
        return self._properties.get('id')

    @property
    def start(self):
        """Union[Datetime, None]: Datetime when the stage started."""
        if self._properties.get('startMs') is None:
            return None
        return _helpers._datetime_from_microseconds(
                int(self._properties.get('startMs')) * 1000.0)

    @property
    def end(self):
        """Union[Datetime, None]: Datetime when the stage ended."""
        if self._properties.get('endMs') is None:
            return None
        return _helpers._datetime_from_microseconds(
                int(self._properties.get('endMs')) * 1000.0)

    @property
    def input_stages(self):
        """List(int): Entry IDs for stages that were inputs for this stage."""
        if self._properties.get('inputStages') is None:
            return []
        return [_helpers._int_or_none(entry)
                for entry in self._properties.get('inputStages')]

    @property
    def parallel_inputs(self):
        """Union[int, None]: Number of parallel input segments within
        the stage.
        """
        return _helpers._int_or_none(self._properties.get('parallelInputs'))

    @property
    def completed_parallel_inputs(self):
        """Union[int, None]: Number of parallel input segments completed."""
        return _helpers._int_or_none(
            self._properties.get('completedParallelInputs'))

    @property
    def wait_ms_avg(self):
        """Union[int, None]: Milliseconds the average worker spent waiting to
        be scheduled.
        """
        return _helpers._int_or_none(self._properties.get('waitMsAvg'))

    @property
    def wait_ms_max(self):
        """Union[int, None]: Milliseconds the slowest worker spent waiting to
        be scheduled.
        """
        return _helpers._int_or_none(self._properties.get('waitMsMax'))

    @property
    def wait_ratio_avg(self):
        """Union[float, None]: Ratio of time the average worker spent waiting
        to be scheduled, relative to the longest time spent by any worker in
        any stage of the overall plan.
        """
        return self._properties.get('waitRatioAvg')

    @property
    def wait_ratio_max(self):
        """Union[float, None]: Ratio of time the slowest worker spent waiting
        to be scheduled, relative to the longest time spent by any worker in
        any stage of the overall plan.
        """
        return self._properties.get('waitRatioMax')

    @property
    def read_ms_avg(self):
        """Union[int, None]: Milliseconds the average worker spent reading
        input.
        """
        return _helpers._int_or_none(self._properties.get('readMsAvg'))

    @property
    def read_ms_max(self):
        """Union[int, None]: Milliseconds the slowest worker spent reading
        input.
        """
        return _helpers._int_or_none(self._properties.get('readMsMax'))

    @property
    def read_ratio_avg(self):
        """Union[float, None]: Ratio of time the average worker spent reading
        input, relative to the longest time spent by any worker in any stage
        of the overall plan.
        """
        return self._properties.get('readRatioAvg')

    @property
    def read_ratio_max(self):
        """Union[float, None]: Ratio of time the slowest worker spent reading
        to be scheduled, relative to the longest time spent by any worker in
        any stage of the overall plan.
        """
        return self._properties.get('readRatioMax')

    @property
    def compute_ms_avg(self):
        """Union[int, None]: Milliseconds the average worker spent on CPU-bound
        processing.
        """
        return _helpers._int_or_none(self._properties.get('computeMsAvg'))

    @property
    def compute_ms_max(self):
        """Union[int, None]: Milliseconds the slowest worker spent on CPU-bound
        processing.
        """
        return _helpers._int_or_none(self._properties.get('computeMsMax'))

    @property
    def compute_ratio_avg(self):
        """Union[float, None]: Ratio of time the average worker spent on
        CPU-bound processing, relative to the longest time spent by any
        worker in any stage of the overall plan.
        """
        return self._properties.get('computeRatioAvg')

    @property
    def compute_ratio_max(self):
        """Union[float, None]: Ratio of time the slowest worker spent on
        CPU-bound processing, relative to the longest time spent by any
        worker in any stage of the overall plan.
        """
        return self._properties.get('computeRatioMax')

    @property
    def write_ms_avg(self):
        """Union[int, None]: Milliseconds the average worker spent writing
        output data.
        """
        return _helpers._int_or_none(self._properties.get('writeMsAvg'))

    @property
    def write_ms_max(self):
        """Union[int, None]: Milliseconds the slowest worker spent writing
        output data.
        """
        return _helpers._int_or_none(self._properties.get('writeMsMax'))

    @property
    def write_ratio_avg(self):
        """Union[float, None]: Ratio of time the average worker spent writing
        output data, relative to the longest time spent by any worker in any
        stage of the overall plan.
        """
        return self._properties.get('writeRatioAvg')

    @property
    def write_ratio_max(self):
        """Union[float, None]: Ratio of time the slowest worker spent writing
        output data, relative to the longest time spent by any worker in any
        stage of the overall plan.
        """
        return self._properties.get('writeRatioMax')

    @property
    def records_read(self):
        """Union[int, None]: Number of records read by this stage."""
        return _helpers._int_or_none(self._properties.get('recordsRead'))

    @property
    def records_written(self):
        """Union[int, None]: Number of records written by this stage."""
        return _helpers._int_or_none(self._properties.get('recordsWritten'))

    @property
    def status(self):
        """Union[str, None]: status of this stage."""
        return self._properties.get('status')

    @property
    def shuffle_output_bytes(self):
        """Union[int, None]: Number of bytes written by this stage to
        intermediate shuffle.
        """
        return _helpers._int_or_none(
            self._properties.get('shuffleOutputBytes'))

    @property
    def shuffle_output_bytes_spilled(self):
        """Union[int, None]: Number of bytes written by this stage to
        intermediate shuffle and spilled to disk.
        """
        return _helpers._int_or_none(
            self._properties.get('shuffleOutputBytesSpilled'))

    @property
    def steps(self):
        """List(QueryPlanEntryStep): List of step operations performed by
        each worker in the stage.
        """
        return [QueryPlanEntryStep.from_api_repr(step)
                for step in self._properties.get('steps', [])]


class TimelineEntry(object):
    """TimelineEntry represents progress of a query job at a particular
    point in time.

    See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs
    for the underlying API representation within query statistics.

    """

    def __init__(self):
        self._properties = {}

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct instance from the JSON repr.

        Args:
            resource(Dict[str: object]):
                QueryTimelineSample representation returned from API

        Returns:
            google.cloud.bigquery.TimelineEntry:
                Timeline sample parsed from ``resource``
        """
        entry = cls()
        entry._properties = resource
        return entry

    @property
    def elapsed_ms(self):
        """Union[int, None]: Milliseconds elapsed since start of query
        execution."""
        return _helpers._int_or_none(self._properties.get('elapsedMs'))

    @property
    def active_units(self):
        """Union[int, None]: Current number of input units being processed
        by workers, reported as largest value since the last sample."""
        return _helpers._int_or_none(self._properties.get('activeUnits'))

    @property
    def pending_units(self):
        """Union[int, None]: Current number of input units remaining for
        query stages active at this sample time."""
        return _helpers._int_or_none(self._properties.get('pendingUnits'))

    @property
    def completed_units(self):
        """Union[int, None]: Current number of input units completed by
        this query."""
        return _helpers._int_or_none(self._properties.get('completedUnits'))

    @property
    def slot_millis(self):
        """Union[int, None]: Cumulative slot-milliseconds consumed by
        this query."""
        return _helpers._int_or_none(self._properties.get('totalSlotMs'))


class UnknownJob(_AsyncJob):
    """A job whose type cannot be determined."""

    @classmethod
    def from_api_repr(cls, resource, client):
        """Construct an UnknownJob from the JSON representation.

        Args:
            resource (dict): JSON representation of a job.
            client (google.cloud.bigquery.client.Client):
                Client connected to BigQuery API.

        Returns:
            UnknownJob: Job corresponding to the resource.
        """
        job_ref_properties = resource.get(
            'jobReference', {'projectId': client.project})
        job_ref = _JobReference._from_api_repr(job_ref_properties)
        job = cls(job_ref, client)
        # Populate the job reference with the project, even if it has been
        # redacted, because we know it should equal that of the request.
        resource['jobReference'] = job_ref_properties
        job._properties = resource
        return job
