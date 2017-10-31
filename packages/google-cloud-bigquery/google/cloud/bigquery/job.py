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

import six
from six.moves import http_client

import google.api_core.future.polling
from google.cloud import exceptions
from google.cloud.exceptions import NotFound
from google.cloud._helpers import _datetime_from_microseconds
from google.cloud.bigquery.dataset import DatasetReference
from google.cloud.bigquery.external_config import ExternalConfig
from google.cloud.bigquery.query import _AbstractQueryParameter
from google.cloud.bigquery.query import _query_param_from_api_repr
from google.cloud.bigquery.query import ArrayQueryParameter
from google.cloud.bigquery.query import ScalarQueryParameter
from google.cloud.bigquery.query import StructQueryParameter
from google.cloud.bigquery.query import UDFResource
from google.cloud.bigquery.schema import SchemaField
from google.cloud.bigquery.table import TableReference
from google.cloud.bigquery.table import _build_schema_resource
from google.cloud.bigquery.table import _parse_schema_resource
from google.cloud.bigquery._helpers import _EnumApiResourceProperty
from google.cloud.bigquery._helpers import _ListApiResourceProperty
from google.cloud.bigquery._helpers import _TypedApiResourceProperty
from google.cloud.bigquery._helpers import DEFAULT_RETRY
from google.cloud.bigquery._helpers import _int_or_none

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


class Compression(_EnumApiResourceProperty):
    """Pseudo-enum for ``compression`` properties."""
    GZIP = 'GZIP'
    NONE = 'NONE'


class CreateDisposition(_EnumApiResourceProperty):
    """Pseudo-enum for ``create_disposition`` properties."""
    CREATE_IF_NEEDED = 'CREATE_IF_NEEDED'
    CREATE_NEVER = 'CREATE_NEVER'


class DestinationFormat(_EnumApiResourceProperty):
    """Pseudo-enum for ``destination_format`` properties."""
    CSV = 'CSV'
    NEWLINE_DELIMITED_JSON = 'NEWLINE_DELIMITED_JSON'
    AVRO = 'AVRO'


class Encoding(_EnumApiResourceProperty):
    """Pseudo-enum for ``encoding`` properties."""
    UTF_8 = 'UTF-8'
    ISO_8559_1 = 'ISO-8559-1'


class QueryPriority(_EnumApiResourceProperty):
    """Pseudo-enum for ``QueryJob.priority`` property."""
    INTERACTIVE = 'INTERACTIVE'
    BATCH = 'BATCH'


class SourceFormat(_EnumApiResourceProperty):
    """Pseudo-enum for ``source_format`` properties."""
    CSV = 'CSV'
    DATASTORE_BACKUP = 'DATASTORE_BACKUP'
    NEWLINE_DELIMITED_JSON = 'NEWLINE_DELIMITED_JSON'
    AVRO = 'AVRO'


class WriteDisposition(_EnumApiResourceProperty):
    """Pseudo-enum for ``write_disposition`` properties."""
    WRITE_APPEND = 'WRITE_APPEND'
    WRITE_TRUNCATE = 'WRITE_TRUNCATE'
    WRITE_EMPTY = 'WRITE_EMPTY'


class AutoDetectSchema(_TypedApiResourceProperty):
    """Property for ``autodetect`` properties.

    :raises ValueError: on ``set`` operation if ``instance.schema``
                        is already defined.
    """
    def __set__(self, instance, value):
        self._validate(value)
        instance._properties[self.resource_name] = value


class _AsyncJob(google.api_core.future.polling.PollingFuture):
    """Base class for asynchronous jobs.

    :type job_id: str
    :param job_id: the job's ID in the project associated with the client.

    :type client: :class:`google.cloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration.
    """
    def __init__(self, job_id, client):
        super(_AsyncJob, self).__init__()
        self.job_id = job_id
        self._client = client
        self._properties = {}
        self._result_set = False
        self._completion_lock = threading.Lock()

    @property
    def project(self):
        """Project bound to the job.

        :rtype: str
        :returns: the project (derived from the client).
        """
        return self._client.project

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
                return _datetime_from_microseconds(millis * 1000.0)

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
                return _datetime_from_microseconds(millis * 1000.0)

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
                return _datetime_from_microseconds(millis * 1000.0)

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
        configuration = cleaned['configuration'][self._JOB_TYPE]
        self._copy_configuration_properties(configuration)

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
        config = resource['configuration'][cls._JOB_TYPE]
        return job_id, config

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

        try:
            client._call_api(retry,
                             method='GET', path=self.path,
                             query_params={'fields': 'id'})
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

        api_response = client._call_api(retry, method='GET', path=self.path)
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

        api_response = client._connection.api_request(
            method='POST', path='%s/cancel' % (self.path,))
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


class LoadJobConfig(object):
    """Configuration options for load jobs.

    All properties in this class are optional. Values which are ``None`` ->
    server defaults.
    """

    def __init__(self):
        self._properties = {}
        self._schema = ()

    allow_jagged_rows = _TypedApiResourceProperty(
        'allow_jagged_rows', 'allowJaggedRows', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.allowJaggedRows
    """

    allow_quoted_newlines = _TypedApiResourceProperty(
        'allow_quoted_newlines', 'allowQuotedNewlines', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.allowQuotedNewlines
    """

    autodetect = AutoDetectSchema('autodetect', 'autodetect', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.autodetect
    """

    create_disposition = CreateDisposition('create_disposition',
                                           'createDisposition')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.createDisposition
    """

    encoding = Encoding('encoding', 'encoding')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.encoding
    """

    field_delimiter = _TypedApiResourceProperty(
        'field_delimiter', 'fieldDelimiter', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.fieldDelimiter
    """

    ignore_unknown_values = _TypedApiResourceProperty(
        'ignore_unknown_values', 'ignoreUnknownValues', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.ignoreUnknownValues
    """

    max_bad_records = _TypedApiResourceProperty(
        'max_bad_records', 'maxBadRecords', six.integer_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.maxBadRecords
    """

    null_marker = _TypedApiResourceProperty(
        'null_marker', 'nullMarker', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.nullMarker
    """

    quote_character = _TypedApiResourceProperty(
        'quote_character', 'quote', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.quote
    """

    skip_leading_rows = _TypedApiResourceProperty(
        'skip_leading_rows', 'skipLeadingRows', six.integer_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.skipLeadingRows
    """

    source_format = SourceFormat('source_format', 'sourceFormat')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.sourceFormat
    """

    write_disposition = WriteDisposition('write_disposition',
                                         'writeDisposition')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.writeDisposition
    """

    @property
    def schema(self):
        """See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.schema
        """
        return list(self._schema)

    @schema.setter
    def schema(self, value):
        if not all(isinstance(field, SchemaField) for field in value):
            raise ValueError('Schema items must be fields')
        self._schema = tuple(value)

    def to_api_repr(self):
        """Build an API representation of the load job config.

        :rtype: dict
        :returns: A dictionary in the format used by the BigQuery API.
        """
        config = copy.deepcopy(self._properties)
        if len(self.schema) > 0:
            config['schema'] = {'fields': _build_schema_resource(self.schema)}
        # skipLeadingRows is a string because it's defined as an int64, which
        # can't be represented as a JSON number.
        slr = config.get('skipLeadingRows')
        if slr is not None:
            config['skipLeadingRows'] = str(slr)
        return config

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a job configuration given its API representation

        :type resource: dict
        :param resource:
            An extract job configuration in the same representation as is
            returned from the API.

        :rtype: :class:`google.cloud.bigquery.job.LoadJobConfig`
        :returns: Configuration parsed from ``resource``.
        """
        schema = resource.pop('schema', {'fields': ()})
        slr = resource.pop('skipLeadingRows', None)
        config = cls()
        config._properties = copy.deepcopy(resource)
        config.schema = _parse_schema_resource(schema)
        config.skip_leading_rows = _int_or_none(slr)


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

    :type destination: :class:`google.cloud.bigquery.TableReference`
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
    def input_file_bytes(self):
        """Count of bytes loaded from source files.

        :rtype: int, or ``NoneType``
        :returns: the count (None until set from the server).
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
        """Generate a resource for :meth:`begin`."""
        configuration = self._configuration.to_api_repr()
        if self.source_uris is not None:
            configuration['sourceUris'] = self.source_uris
        configuration['destinationTable'] = self.destination.to_api_repr()

        return {
            'jobReference': {
                'projectId': self.project,
                'jobId': self.job_id,
            },
            'configuration': {
                self._JOB_TYPE: configuration,
            },
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
        job_id, config_resource = cls._get_resource_config(resource)
        config = LoadJobConfig.from_api_repr(config_resource)
        dest_config = config_resource['destinationTable']
        ds_ref = DatasetReference(dest_config['projectId'],
                                  dest_config['datasetId'],)
        destination = TableReference(ds_ref, dest_config['tableId'])
        # sourceUris will be absent if this is a file upload.
        source_uris = config_resource.get('sourceUris')
        job = cls(job_id, source_uris, destination, client, config)
        job._set_properties(resource)
        return job


class CopyJobConfig(object):
    """Configuration options for copy jobs.

    All properties in this class are optional. Values which are ``None`` ->
    server defaults.
    """

    def __init__(self):
        self._properties = {}

    create_disposition = CreateDisposition('create_disposition',
                                           'createDisposition')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.copy.createDisposition
    """

    write_disposition = WriteDisposition('write_disposition',
                                         'writeDisposition')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.copy.writeDisposition
    """

    def to_api_repr(self):
        """Build an API representation of the copy job config.

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

        :rtype: :class:`google.cloud.bigquery.job.CopyJobConfig`
        :returns: Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        return config


class CopyJob(_AsyncJob):
    """Asynchronous job: copy data into a table from other tables.

    :type job_id: str
    :param job_id: the job's ID, within the project belonging to ``client``.

    :type sources: list of :class:`google.cloud.bigquery.TableReference`
    :param sources: Table into which data is to be loaded.

    :type destination: :class:`google.cloud.bigquery.TableReference`
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

    def _build_resource(self):
        """Generate a resource for :meth:`begin`."""

        source_refs = [{
            'projectId': table.project,
            'datasetId': table.dataset_id,
            'tableId': table.table_id,
        } for table in self.sources]

        configuration = self._configuration.to_api_repr()
        configuration['sourceTables'] = source_refs
        configuration['destinationTable'] = {
            'projectId': self.destination.project,
            'datasetId': self.destination.dataset_id,
            'tableId': self.destination.table_id,
        }

        return {
            'jobReference': {
                'projectId': self.project,
                'jobId': self.job_id,
            },
            'configuration': {
                self._JOB_TYPE: configuration,
            },
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
        destination = TableReference.from_api_repr(
            config_resource['destinationTable'])
        sources = []
        source_configs = config_resource.get('sourceTables')
        if source_configs is None:
            single = config_resource.get('sourceTable')
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


class ExtractJobConfig(object):
    """Configuration options for extract jobs.

    All properties in this class are optional. Values which are ``None`` ->
    server defaults.
    """

    def __init__(self):
        self._properties = {}

    compression = Compression('compression', 'compression')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.extract.compression
    """

    destination_format = DestinationFormat(
        'destination_format', 'destinationFormat')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.extract.destinationFormat
    """

    field_delimiter = _TypedApiResourceProperty(
        'field_delimiter', 'fieldDelimiter', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.extract.fieldDelimiter
    """

    print_header = _TypedApiResourceProperty(
        'print_header', 'printHeader', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.extract.printHeader
    """

    def to_api_repr(self):
        """Build an API representation of the extract job config.

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

        :rtype: :class:`google.cloud.bigquery.job.ExtractJobConfig`
        :returns: Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        return config


class ExtractJob(_AsyncJob):
    """Asynchronous job: extract data from a table into Cloud Storage.

    :type job_id: str
    :param job_id: the job's ID

    :type source: :class:`google.cloud.bigquery.TableReference`
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

        :rtype: int or None
        :returns: number of DML rows affectd by the job, or None if job is not
                  yet complete.
        """
        result = self._job_statistics().get('destinationUriFileCounts')
        if result is not None:
            result = int(result)
        return result

    def _build_resource(self):
        """Generate a resource for :meth:`begin`."""

        source_ref = {
            'projectId': self.source.project,
            'datasetId': self.source.dataset_id,
            'tableId': self.source.table_id,
        }

        configuration = self._configuration.to_api_repr()
        configuration['sourceTable'] = source_ref
        configuration['destinationUris'] = self.destination_uris

        resource = {
            'jobReference': {
                'projectId': self.project,
                'jobId': self.job_id,
            },
            'configuration': {
                self._JOB_TYPE: configuration,
            },
        }

        return resource

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
        source_config = config_resource['sourceTable']
        dataset = DatasetReference(
            source_config['projectId'], source_config['datasetId'])
        source = dataset.table(source_config['tableId'])
        destination_uris = config_resource['destinationUris']

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


class QueryJobConfig(object):
    """Configuration options for query jobs.

    All properties in this class are optional. Values which are ``None`` ->
    server defaults.
    """

    _QUERY_PARAMETERS_KEY = 'queryParameters'
    _UDF_RESOURCES_KEY = 'userDefinedFunctionResources'

    def __init__(self):
        self._properties = {}

    def to_api_repr(self):
        """Build an API representation of the copy job config.

        :rtype: dict
        :returns: A dictionary in the format used by the BigQuery API.
        """
        resource = copy.deepcopy(self._properties)

        # Query parameters have an addition property associated with them
        # to indicate if the query is using named or positional parameters.
        query_parameters = resource.get(self._QUERY_PARAMETERS_KEY)
        if query_parameters:
            if query_parameters[0].name is None:
                resource['parameterMode'] = 'POSITIONAL'
            else:
                resource['parameterMode'] = 'NAMED'

        for prop, convert in self._NESTED_PROPERTIES.items():
            _, to_resource = convert
            nested_resource = resource.get(prop)
            if nested_resource is not None:
                resource[prop] = to_resource(nested_resource)

        return resource

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a job configuration given its API representation

        :type resource: dict
        :param resource:
            An extract job configuration in the same representation as is
            returned from the API.

        :rtype: :class:`google.cloud.bigquery.job.QueryJobConfig`
        :returns: Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)

        for prop, convert in cls._NESTED_PROPERTIES.items():
            from_resource, _ = convert
            nested_resource = resource.get(prop)
            if nested_resource is not None:
                config._properties[prop] = from_resource(nested_resource)

        return config

    allow_large_results = _TypedApiResourceProperty(
        'allow_large_results', 'allowLargeResults', bool)
    """bool: Allow large query results tables (legacy SQL, only)

    See
    https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.allowLargeResults
    """

    create_disposition = CreateDisposition(
        'create_disposition', 'createDisposition')
    """See
    https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.createDisposition
    """

    default_dataset = _TypedApiResourceProperty(
        'default_dataset', 'defaultDataset', DatasetReference)
    """See
    https://g.co/cloud/bigquery/docs/reference/v2/jobs#configuration.query.defaultDataset
    """

    destination = _TypedApiResourceProperty(
        'destination', 'destinationTable', TableReference)
    """
    google.cloud.bigquery.table.TableReference: table where results are written

    See
    https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.destinationTable
    """

    dry_run = _TypedApiResourceProperty('dry_run', 'dryRun', bool)
    """
    bool: ``True`` if this query should be a dry run to estimate costs.

    See
    https://g.co/cloud/bigquery/docs/reference/v2/jobs#configuration.dryRun
    """

    flatten_results = _TypedApiResourceProperty(
        'flatten_results', 'flattenResults', bool)
    """See
    https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.flattenResults
    """

    maximum_billing_tier = _TypedApiResourceProperty(
        'maximum_billing_tier', 'maximumBillingTier', int)
    """See
    https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.maximumBillingTier
    """

    maximum_bytes_billed = _TypedApiResourceProperty(
        'maximum_bytes_billed', 'maximumBytesBilled', int)
    """See
    https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.maximumBytesBilled
    """

    priority = QueryPriority('priority', 'priority')
    """See
    https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.priority
    """

    query_parameters = _ListApiResourceProperty(
        'query_parameters', _QUERY_PARAMETERS_KEY, _AbstractQueryParameter)
    """
    A list of
    :class:`google.cloud.bigquery.ArrayQueryParameter`,
    :class:`google.cloud.bigquery.ScalarQueryParameter`, or
    :class:`google.cloud.bigquery.StructQueryParameter`
    (empty by default)

    See:
    https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.queryParameters
    """

    udf_resources = _ListApiResourceProperty(
        'udf_resources', _UDF_RESOURCES_KEY, UDFResource)
    """
    A list of :class:`google.cloud.bigquery.UDFResource` (empty
    by default)

    See:
    https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.userDefinedFunctionResources
    """

    use_legacy_sql = _TypedApiResourceProperty(
        'use_legacy_sql', 'useLegacySql', bool)
    """See
    https://g.co/cloud/bigquery/docs/reference/v2/jobs#configuration.query.useLegacySql
    """

    use_query_cache = _TypedApiResourceProperty(
        'use_query_cache', 'useQueryCache', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.useQueryCache
    """

    write_disposition = WriteDisposition(
        'write_disposition', 'writeDisposition')
    """See
    https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.writeDisposition
    """

    table_definitions = _TypedApiResourceProperty(
        'table_definitions', 'tableDefinitions', dict)
    """
    Definitions for external tables. A dictionary from table names (strings)
    to :class:`google.cloud.bigquery.ExternalConfig`.

    See
    https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions
    """

    _maximum_billing_tier = None
    _maximum_bytes_billed = None

    _NESTED_PROPERTIES = {
        'defaultDataset': (
            DatasetReference.from_api_repr, DatasetReference.to_api_repr),
        'destinationTable': (
            TableReference.from_api_repr, TableReference.to_api_repr),
        'maximumBytesBilled': (int, str),
        'tableDefinitions': (_from_api_repr_table_defs,
                             _to_api_repr_table_defs),
        _QUERY_PARAMETERS_KEY: (
            _from_api_repr_query_parameters, _to_api_repr_query_parameters),
        _UDF_RESOURCES_KEY: (
            _from_api_repr_udf_resources, _to_api_repr_udf_resources),
    }


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

    def _build_resource(self):
        """Generate a resource for :meth:`begin`."""
        configuration = self._configuration.to_api_repr()

        resource = {
            'jobReference': {
                'projectId': self.project,
                'jobId': self.job_id,
            },
            'configuration': {
                self._JOB_TYPE: configuration,
            },
        }

        # The dryRun property only applies to query jobs, but it is defined at
        # a level higher up. We need to remove it from the query config.
        if 'dryRun' in configuration:
            dry_run = configuration['dryRun']
            del configuration['dryRun']
            resource['configuration']['dryRun'] = dry_run

        configuration['query'] = self.query

        return resource

    def _scrub_local_properties(self, cleaned):
        """Helper:  handle subclass properties in cleaned.

        .. note:

           This method assumes that the project found in the resource matches
           the client's project.
        """
        configuration = cleaned['configuration']['query']
        self.query = configuration['query']

        # The dryRun property only applies to query jobs, but it is defined at
        # a level higher up. We need to copy it to the query config.
        self._configuration.dry_run = cleaned['configuration'].get('dryRun')

    def _copy_configuration_properties(self, configuration):
        """Helper:  assign subclass configuration properties in cleaned."""
        # The dryRun property only applies to query jobs, but it is defined at
        # a level higher up. We need to copy it to the query config.
        # It should already be correctly set by the _scrub_local_properties()
        # method.
        dry_run = self.dry_run
        self._configuration = QueryJobConfig.from_api_repr(configuration)
        self._configuration.dry_run = dry_run

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
        query = config['query']
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
        """Return billing tier from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.cacheHit

        :rtype: bool or None
        :returns: whether the query results were returned from cache, or None
                  if job is not yet complete.
        """
        return self._job_statistics().get('cacheHit')

    @property
    def num_dml_affected_rows(self):
        """Return total bytes billed from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.numDmlAffectedRows

        :rtype: int or None
        :returns: number of DML rows affectd by the job, or None if job is not
                  yet complete.
        """
        result = self._job_statistics().get('numDmlAffectedRows')
        if result is not None:
            result = int(result)
        return result

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
    def undeclared_query_paramters(self):
        """Return undeclared query parameters from job statistics, if present.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#statistics.query.undeclaredQueryParamters

        :rtype:
            list of
            :class:`~google.cloud.bigquery.ArrayQueryParameter`,
            :class:`~google.cloud.bigquery.ScalarQueryParameter`, or
            :class:`~google.cloud.bigquery.StructQueryParameter`
        :returns: undeclared parameters, or an empty list if the query has
                  not yet completed.
        """
        parameters = []
        undeclared = self._job_statistics().get('undeclaredQueryParamters', ())

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

    def query_results(self, retry=DEFAULT_RETRY):
        """Construct a QueryResults instance, bound to this job.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`~google.cloud.bigquery.QueryResults`
        :returns: results instance
        """
        if not self._query_results:
            self._query_results = self._client._get_query_results(
                self.job_id, retry, project=self.project)
        return self._query_results

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
                project=self.project, timeout_ms=timeout_ms)

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

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns:
            Iterator of row data :class:`tuple`s. During each page, the
            iterator will have the ``total_rows`` attribute set, which counts
            the total number of rows **in the result set** (this is distinct
            from the total number of rows in the current page:
            ``iterator.page.num_items``).

        :raises:
            :class:`~google.cloud.exceptions.GoogleCloudError` if the job
            failed or :class:`concurrent.futures.TimeoutError` if the job did
            not complete in the given timeout.
        """
        super(QueryJob, self).result(timeout=timeout)
        # Return an iterator instead of returning the job.
        schema = self.query_results().schema
        dest_table = self.destination
        return self._client.list_rows(dest_table, selected_fields=schema,
                                      retry=retry)


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
    """Map a single entry in a query plan.

    :type name: str
    :param name: name of the entry

    :type entry_id: int
    :param entry_id: ID of the entry

    :type wait_ratio_avg: float
    :param wait_ratio_avg: average wait ratio

    :type wait_ratio_max: float
    :param wait_ratio_avg: maximum wait ratio

    :type read_ratio_avg: float
    :param read_ratio_avg: average read ratio

    :type read_ratio_max: float
    :param read_ratio_avg: maximum read ratio

    :type copute_ratio_avg: float
    :param copute_ratio_avg: average copute ratio

    :type copute_ratio_max: float
    :param copute_ratio_avg: maximum copute ratio

    :type write_ratio_avg: float
    :param write_ratio_avg: average write ratio

    :type write_ratio_max: float
    :param write_ratio_avg: maximum write ratio

    :type records_read: int
    :param records_read: number of records read

    :type records_written: int
    :param records_written: number of records written

    :type status: str
    :param status: entry status

    :type steps: List(QueryPlanEntryStep)
    :param steps: steps in the entry
    """
    def __init__(self,
                 name,
                 entry_id,
                 wait_ratio_avg,
                 wait_ratio_max,
                 read_ratio_avg,
                 read_ratio_max,
                 compute_ratio_avg,
                 compute_ratio_max,
                 write_ratio_avg,
                 write_ratio_max,
                 records_read,
                 records_written,
                 status,
                 steps):
        self.name = name
        self.entry_id = entry_id
        self.wait_ratio_avg = wait_ratio_avg
        self.wait_ratio_max = wait_ratio_max
        self.read_ratio_avg = read_ratio_avg
        self.read_ratio_max = read_ratio_max
        self.compute_ratio_avg = compute_ratio_avg
        self.compute_ratio_max = compute_ratio_max
        self.write_ratio_avg = write_ratio_avg
        self.write_ratio_max = write_ratio_max
        self.records_read = records_read
        self.records_written = records_written
        self.status = status
        self.steps = steps

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct instance from the JSON repr.

        :type resource: dict
        :param resource: JSON representation of the entry

        :rtype: :class:`QueryPlanEntry`
        :return: new instance built from the resource
        """
        records_read = resource.get('recordsRead')
        if records_read is not None:
            records_read = int(records_read)

        records_written = resource.get('recordsWritten')
        if records_written is not None:
            records_written = int(records_written)

        return cls(
            name=resource.get('name'),
            entry_id=resource.get('id'),
            wait_ratio_avg=resource.get('waitRatioAvg'),
            wait_ratio_max=resource.get('waitRatioMax'),
            read_ratio_avg=resource.get('readRatioAvg'),
            read_ratio_max=resource.get('readRatioMax'),
            compute_ratio_avg=resource.get('computeRatioAvg'),
            compute_ratio_max=resource.get('computeRatioMax'),
            write_ratio_avg=resource.get('writeRatioAvg'),
            write_ratio_max=resource.get('writeRatioMax'),
            records_read=records_read,
            records_written=records_written,
            status=resource.get('status'),
            steps=[QueryPlanEntryStep.from_api_repr(step)
                   for step in resource.get('steps', ())],
        )
