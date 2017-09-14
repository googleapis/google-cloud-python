# Copyright 2015 Google Inc.
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

import google.api.core.future.polling
from google.cloud import exceptions
from google.cloud.exceptions import NotFound
from google.cloud._helpers import _datetime_from_microseconds
from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.dataset import DatasetReference
from google.cloud.bigquery.schema import SchemaField
from google.cloud.bigquery.table import Table
from google.cloud.bigquery.table import TableReference
from google.cloud.bigquery.table import _build_schema_resource
from google.cloud.bigquery.table import _parse_schema_resource
from google.cloud.bigquery._helpers import ArrayQueryParameter
from google.cloud.bigquery._helpers import QueryParametersProperty
from google.cloud.bigquery._helpers import ScalarQueryParameter
from google.cloud.bigquery._helpers import StructQueryParameter
from google.cloud.bigquery._helpers import UDFResource
from google.cloud.bigquery._helpers import UDFResourcesProperty
from google.cloud.bigquery._helpers import _EnumApiResourceProperty
from google.cloud.bigquery._helpers import _EnumProperty
from google.cloud.bigquery._helpers import _query_param_from_api_repr
from google.cloud.bigquery._helpers import _TypedApiResourceProperty
from google.cloud.bigquery._helpers import _TypedProperty

_DONE_STATE = 'DONE'
_STOPPED_REASON = 'stopped'

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


def _bool_or_none(value):
    """Helper: deserialize boolean value from JSON string."""
    if isinstance(value, bool):
        return value
    if value is not None:
        return value.lower() in ['t', 'true', '1']


def _int_or_none(value):
    """Helper: deserialize int value from JSON string."""
    if isinstance(value, int):
        return value
    if value is not None:
        return int(value)


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


class AutoDetectSchema(_TypedProperty):
    """Typed Property for ``autodetect`` properties.

    :raises ValueError: on ``set`` operation if ``instance.schema``
                        is already defined.
    """
    def __set__(self, instance, value):
        self._validate(value)
        if instance.schema:
            raise ValueError('A schema should not be already defined '
                             'when using schema auto-detection')
        setattr(instance._configuration, self._backing_name, value)


class Compression(_EnumApiResourceProperty):
    """Pseudo-enum for ``compression`` properties."""
    GZIP = 'GZIP'
    NONE = 'NONE'


class CreateDisposition(_EnumProperty):
    """Pseudo-enum for ``create_disposition`` properties."""
    CREATE_IF_NEEDED = 'CREATE_IF_NEEDED'
    CREATE_NEVER = 'CREATE_NEVER'


class DestinationFormat(_EnumApiResourceProperty):
    """Pseudo-enum for ``destination_format`` properties."""
    CSV = 'CSV'
    NEWLINE_DELIMITED_JSON = 'NEWLINE_DELIMITED_JSON'
    AVRO = 'AVRO'


class Encoding(_EnumProperty):
    """Pseudo-enum for ``encoding`` properties."""
    UTF_8 = 'UTF-8'
    ISO_8559_1 = 'ISO-8559-1'


class QueryPriority(_EnumProperty):
    """Pseudo-enum for ``QueryJob.priority`` property."""
    INTERACTIVE = 'INTERACTIVE'
    BATCH = 'BATCH'


class SourceFormat(_EnumProperty):
    """Pseudo-enum for ``source_format`` properties."""
    CSV = 'CSV'
    DATASTORE_BACKUP = 'DATASTORE_BACKUP'
    NEWLINE_DELIMITED_JSON = 'NEWLINE_DELIMITED_JSON'
    AVRO = 'AVRO'


class WriteDisposition(_EnumProperty):
    """Pseudo-enum for ``write_disposition`` properties."""
    WRITE_APPEND = 'WRITE_APPEND'
    WRITE_TRUNCATE = 'WRITE_TRUNCATE'
    WRITE_EMPTY = 'WRITE_EMPTY'


class _AsyncJob(google.api.core.future.polling.PollingFuture):
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

    def begin(self, client=None):
        """API call:  begin the job via a POST request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :raises: :exc:`ValueError` if the job has already begin.
        """
        if self.state is not None:
            raise ValueError("Job already begun.")

        client = self._require_client(client)
        path = '/projects/%s/jobs' % (self.project,)

        api_response = client._connection.api_request(
            method='POST', path=path, data=self._build_resource())
        self._set_properties(api_response)

    def exists(self, client=None):
        """API call:  test for the existence of the job via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: bool
        :returns: Boolean indicating existence of the job.
        """
        client = self._require_client(client)

        try:
            client._connection.api_request(method='GET', path=self.path,
                                           query_params={'fields': 'id'})
        except NotFound:
            return False
        else:
            return True

    def reload(self, client=None):
        """API call:  refresh job properties via a GET request.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get

        :type client: :class:`~google.cloud.bigquery.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)

        api_response = client._connection.api_request(
            method='GET', path=self.path)
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

    def done(self):
        """Refresh the job and checks if it is complete.

        :rtype: bool
        :returns: True if the job is complete, False otherwise.
        """
        # Do not refresh is the state is already done, as the job will not
        # change once complete.
        if self.state != _DONE_STATE:
            self.reload()
        return self.state == _DONE_STATE

    def result(self, timeout=None):
        """Start the job and wait for it to complete and get the result.

        :type timeout: int
        :param timeout: How long to wait for job to complete before raising
            a :class:`TimeoutError`.

        :rtype: _AsyncJob
        :returns: This instance.

        :raises: :class:`~google.cloud.exceptions.GoogleCloudError` if the job
            failed or  :class:`TimeoutError` if the job did not complete in the
            given timeout.
        """
        if self.state is None:
            self.begin()
        return super(_AsyncJob, self).result(timeout=timeout)

    def cancelled(self):
        """Check if the job has been cancelled.

        This always returns False. It's not possible to check if a job was
        cancelled in the API. This method is here to satisfy the interface
        for :class:`google.api.core.future.Future`.

        :rtype: bool
        :returns: False
        """
        return (self.error_result is not None
                and self.error_result.get('reason') == _STOPPED_REASON)


class _LoadConfiguration(object):
    """User-settable configuration options for load jobs.

    Values which are ``None`` -> server defaults.
    """
    _allow_jagged_rows = None
    _allow_quoted_newlines = None
    _autodetect = None
    _create_disposition = None
    _encoding = None
    _field_delimiter = None
    _ignore_unknown_values = None
    _max_bad_records = None
    _null_marker = None
    _quote_character = None
    _skip_leading_rows = None
    _source_format = None
    _write_disposition = None


class LoadJob(_AsyncJob):
    """Asynchronous job for loading data into a table from remote URI.

    :type job_id: str
    :param job_id:
        The job's ID, belonging to the project associated with the client.

    :type destination: :class:`google.cloud.bigquery.table.Table`
    :param destination: Table into which data is to be loaded.

    :type source_uris: sequence of string
    :param source_uris:
        URIs of one or more data files to be loaded.  See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.sourceUris
        for supported URI formats.

    :type client: :class:`google.cloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).

    :type schema: list of :class:`google.cloud.bigquery.table.SchemaField`
    :param schema: The job's schema
    """

    _schema = None
    _JOB_TYPE = 'load'

    def __init__(self, name, destination, source_uris, client, schema=()):
        super(LoadJob, self).__init__(name, client)
        self.destination = destination
        self.source_uris = source_uris
        self._configuration = _LoadConfiguration()
        # Let the @property do validation. This must occur after all other
        # attributes have been set.
        self.schema = schema

    @property
    def schema(self):
        """Table's schema.

        :rtype: list of :class:`SchemaField`
        :returns: fields describing the schema
        """
        return list(self._schema)

    @schema.setter
    def schema(self, value):
        """Update table's schema

        :type value: list of :class:`SchemaField`
        :param value: fields describing the schema

        :raises TypeError: If ``value`is not a sequence.
        :raises ValueError: If any item in the sequence is not
                            a ``SchemaField``.
        """
        if not value:
            self._schema = ()
        else:
            if not all(isinstance(field, SchemaField) for field in value):
                raise ValueError('Schema items must be fields')
            if self.autodetect:
                raise ValueError(
                    'Schema can not be set if `autodetect` property is True')

            self._schema = tuple(value)

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

    allow_jagged_rows = _TypedProperty('allow_jagged_rows', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.allowJaggedRows
    """

    allow_quoted_newlines = _TypedProperty('allow_quoted_newlines', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.allowQuotedNewlines
    """

    autodetect = AutoDetectSchema('autodetect', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.autodetect
    """

    create_disposition = CreateDisposition('create_disposition')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.createDisposition
    """

    encoding = Encoding('encoding')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.encoding
    """

    field_delimiter = _TypedProperty('field_delimiter', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.fieldDelimiter
    """

    ignore_unknown_values = _TypedProperty('ignore_unknown_values', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.ignoreUnknownValues
    """

    max_bad_records = _TypedProperty('max_bad_records', six.integer_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.maxBadRecords
    """

    null_marker = _TypedProperty('null_marker', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.nullMarker
    """

    quote_character = _TypedProperty('quote_character', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.quote
    """

    skip_leading_rows = _TypedProperty('skip_leading_rows', six.integer_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.skipLeadingRows
    """

    source_format = SourceFormat('source_format')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.sourceFormat
    """

    write_disposition = WriteDisposition('write_disposition')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.writeDisposition
    """

    def _populate_config_resource(self, configuration):
        """Helper for _build_resource: copy config properties to resource"""
        if self.allow_jagged_rows is not None:
            configuration['allowJaggedRows'] = self.allow_jagged_rows
        if self.allow_quoted_newlines is not None:
            configuration['allowQuotedNewlines'] = self.allow_quoted_newlines
        if self.autodetect is not None:
            configuration['autodetect'] = self.autodetect
        if self.create_disposition is not None:
            configuration['createDisposition'] = self.create_disposition
        if self.encoding is not None:
            configuration['encoding'] = self.encoding
        if self.field_delimiter is not None:
            configuration['fieldDelimiter'] = self.field_delimiter
        if self.ignore_unknown_values is not None:
            configuration['ignoreUnknownValues'] = self.ignore_unknown_values
        if self.max_bad_records is not None:
            configuration['maxBadRecords'] = self.max_bad_records
        if self.null_marker is not None:
            configuration['nullMarker'] = self.null_marker
        if self.quote_character is not None:
            configuration['quote'] = self.quote_character
        if self.skip_leading_rows is not None:
            configuration['skipLeadingRows'] = str(self.skip_leading_rows)
        if self.source_format is not None:
            configuration['sourceFormat'] = self.source_format
        if self.write_disposition is not None:
            configuration['writeDisposition'] = self.write_disposition

    def _build_resource(self):
        """Generate a resource for :meth:`begin`."""
        resource = {
            'jobReference': {
                'projectId': self.project,
                'jobId': self.job_id,
            },
            'configuration': {
                self._JOB_TYPE: {
                    'sourceUris': self.source_uris,
                    'destinationTable': {
                        'projectId': self.destination.project,
                        'datasetId': self.destination.dataset_id,
                        'tableId': self.destination.table_id,
                    },
                },
            },
        }
        configuration = resource['configuration'][self._JOB_TYPE]
        self._populate_config_resource(configuration)

        if len(self.schema) > 0:
            configuration['schema'] = {
                'fields': _build_schema_resource(self.schema)}

        return resource

    def _scrub_local_properties(self, cleaned):
        """Helper:  handle subclass properties in cleaned."""
        schema = cleaned.pop('schema', {'fields': ()})
        self.schema = _parse_schema_resource(schema)

    def _copy_configuration_properties(self, configuration):
        """Helper:  assign subclass configuration properties in cleaned."""
        self.allow_jagged_rows = _bool_or_none(
            configuration.get('allowJaggedRows'))
        self.allow_quoted_newlines = _bool_or_none(
            configuration.get('allowQuotedNewlines'))
        self.autodetect = _bool_or_none(
            configuration.get('autodetect'))
        self.create_disposition = configuration.get('createDisposition')
        self.encoding = configuration.get('encoding')
        self.field_delimiter = configuration.get('fieldDelimiter')
        self.ignore_unknown_values = _bool_or_none(
            configuration.get('ignoreUnknownValues'))
        self.max_bad_records = _int_or_none(
            configuration.get('maxBadRecords'))
        self.null_marker = configuration.get('nullMarker')
        self.quote_character = configuration.get('quote')
        self.skip_leading_rows = _int_or_none(
            configuration.get('skipLeadingRows'))
        self.source_format = configuration.get('sourceFormat')
        self.write_disposition = configuration.get('writeDisposition')

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
        job_id, config = cls._get_resource_config(resource)
        dest_config = config['destinationTable']
        dataset = Dataset(dest_config['datasetId'], client)
        table_ref = TableReference(dataset, dest_config['tableId'])
        destination = Table(table_ref, client=client)
        source_urls = config.get('sourceUris', ())
        job = cls(job_id, destination, source_urls, client=client)
        job._set_properties(resource)
        return job


class _CopyConfiguration(object):
    """User-settable configuration options for copy jobs.

    Values which are ``None`` -> server defaults.
    """
    _create_disposition = None
    _write_disposition = None


class CopyJob(_AsyncJob):
    """Asynchronous job: copy data into a table from other tables.

    :type job_id: str
    :param job_id: the job's ID, within the project belonging to ``client``.

    :type destination: :class:`google.cloud.bigquery.table.Table`
    :param destination: Table into which data is to be loaded.

    :type sources: list of :class:`google.cloud.bigquery.table.Table`
    :param sources: Table into which data is to be loaded.

    :type client: :class:`google.cloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).
    """

    _JOB_TYPE = 'copy'

    def __init__(self, job_id, destination, sources, client):
        super(CopyJob, self).__init__(job_id, client)
        self.destination = destination
        self.sources = sources
        self._configuration = _CopyConfiguration()

    create_disposition = CreateDisposition('create_disposition')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.copy.createDisposition
    """

    write_disposition = WriteDisposition('write_disposition')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.copy.writeDisposition
    """

    def _populate_config_resource(self, configuration):
        """Helper for _build_resource: copy config properties to resource"""
        if self.create_disposition is not None:
            configuration['createDisposition'] = self.create_disposition
        if self.write_disposition is not None:
            configuration['writeDisposition'] = self.write_disposition

    def _build_resource(self):
        """Generate a resource for :meth:`begin`."""

        source_refs = [{
            'projectId': table.project,
            'datasetId': table.dataset_id,
            'tableId': table.table_id,
        } for table in self.sources]

        resource = {
            'jobReference': {
                'projectId': self.project,
                'jobId': self.job_id,
            },
            'configuration': {
                self._JOB_TYPE: {
                    'sourceTables': source_refs,
                    'destinationTable': {
                        'projectId': self.destination.project,
                        'datasetId': self.destination.dataset_id,
                        'tableId': self.destination.table_id,
                    },
                },
            },
        }
        configuration = resource['configuration'][self._JOB_TYPE]
        self._populate_config_resource(configuration)

        return resource

    def _copy_configuration_properties(self, configuration):
        """Helper:  assign subclass configuration properties in cleaned."""
        self.create_disposition = configuration.get('createDisposition')
        self.write_disposition = configuration.get('writeDisposition')

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
        job_id, config = cls._get_resource_config(resource)
        dest_config = config['destinationTable']
        dataset = Dataset(dest_config['datasetId'], client)
        table_ref = TableReference(dataset, dest_config['tableId'])
        destination = Table(table_ref, client=client)
        sources = []
        source_configs = config.get('sourceTables')
        if source_configs is None:
            single = config.get('sourceTable')
            if single is None:
                raise KeyError(
                    "Resource missing 'sourceTables' / 'sourceTable'")
            source_configs = [single]
        for source_config in source_configs:
            dataset = Dataset(source_config['datasetId'], client)
            table_ref = TableReference(dataset, source_config['tableId'])
            sources.append(Table(table_ref, client=client))
        job = cls(job_id, destination, sources, client=client)
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
        """Build an API representation of the extact job config.

        :rtype: dict
        :returns: A dictionary in the format used by the BigQuery API.
        """
        resource = copy.deepcopy(self._properties)
        return resource

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
        :class:`~google.cloud.bigquery.job.ExtractJobConfig.compression`.
        """
        return self._configuration.compression

    @property
    def destination_format(self):
        """See
        :class:`~google.cloud.bigquery.job.ExtractJobConfig.destination_format`.
        """
        return self._configuration.destination_format

    @property
    def field_delimiter(self):
        """See
        :class:`~google.cloud.bigquery.job.ExtractJobConfig.field_delimiter`.
        """
        return self._configuration.field_delimiter

    @property
    def print_header(self):
        """See
        :class:`~google.cloud.bigquery.job.ExtractJobConfig.print_header`.
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
            'projectId': self.source.dataset.project_id,
            'datasetId': self.source.dataset.dataset_id,
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


class _AsyncQueryConfiguration(object):
    """User-settable configuration options for asynchronous query jobs.

    Values which are ``None`` -> server defaults.
    """
    _allow_large_results = None
    _create_disposition = None
    _default_dataset = None
    _destination = None
    _flatten_results = None
    _priority = None
    _use_query_cache = None
    _use_legacy_sql = None
    _dry_run = None
    _write_disposition = None
    _maximum_billing_tier = None
    _maximum_bytes_billed = None


class QueryJob(_AsyncJob):
    """Asynchronous job: query tables.

    :type job_id: str
    :param job_id: the job's ID, within the project belonging to ``client``.

    :type query: str
    :param query: SQL query string

    :type client: :class:`google.cloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).

    :type udf_resources: tuple
    :param udf_resources: An iterable of
                        :class:`google.cloud.bigquery._helpers.UDFResource`
                        (empty by default)

    :type query_parameters: tuple
    :param query_parameters:
        An iterable of
        :class:`google.cloud.bigquery._helpers.AbstractQueryParameter`
        (empty by default)
    """
    _JOB_TYPE = 'query'
    _UDF_KEY = 'userDefinedFunctionResources'
    _QUERY_PARAMETERS_KEY = 'queryParameters'

    def __init__(self, job_id, query, client,
                 udf_resources=(), query_parameters=()):
        super(QueryJob, self).__init__(job_id, client)
        self.query = query
        self.udf_resources = udf_resources
        self.query_parameters = query_parameters
        self._configuration = _AsyncQueryConfiguration()
        self._query_results = None

    allow_large_results = _TypedProperty('allow_large_results', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.allowLargeResults
    """

    create_disposition = CreateDisposition('create_disposition')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.createDisposition
    """

    default_dataset = _TypedProperty('default_dataset', Dataset)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.defaultDataset
    """

    destination = _TypedProperty('destination', Table)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.destinationTable
    """

    flatten_results = _TypedProperty('flatten_results', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.flattenResults
    """

    priority = QueryPriority('priority')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.priority
    """

    query_parameters = QueryParametersProperty()

    udf_resources = UDFResourcesProperty()

    use_query_cache = _TypedProperty('use_query_cache', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.useQueryCache
    """

    use_legacy_sql = _TypedProperty('use_legacy_sql', bool)
    """See
    https://cloud.google.com/bigquery/docs/\
    reference/v2/jobs#configuration.query.useLegacySql
    """

    dry_run = _TypedProperty('dry_run', bool)
    """See
    https://cloud.google.com/bigquery/docs/\
    reference/rest/v2/jobs#configuration.dryRun
    """

    write_disposition = WriteDisposition('write_disposition')
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.writeDisposition
    """

    maximum_billing_tier = _TypedProperty('maximum_billing_tier', int)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.maximumBillingTier
    """

    maximum_bytes_billed = _TypedProperty('maximum_bytes_billed', int)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.maximumBytesBilled
    """

    def _destination_table_resource(self):
        """Create a JSON resource for the destination table.

        Helper for :meth:`_populate_config_resource` and
        :meth:`_scrub_local_properties`
        """
        if self.destination is not None:
            return {
                'projectId': self.destination.project,
                'datasetId': self.destination.dataset_id,
                'tableId': self.destination.table_id,
            }

    def _populate_config_resource_booleans(self, configuration):
        """Helper for _populate_config_resource."""
        if self.allow_large_results is not None:
            configuration['allowLargeResults'] = self.allow_large_results
        if self.flatten_results is not None:
            configuration['flattenResults'] = self.flatten_results
        if self.use_query_cache is not None:
            configuration['useQueryCache'] = self.use_query_cache
        if self.use_legacy_sql is not None:
            configuration['useLegacySql'] = self.use_legacy_sql

    def _populate_config_resource(self, configuration):
        """Helper for _build_resource: copy config properties to resource"""
        self._populate_config_resource_booleans(configuration)

        if self.create_disposition is not None:
            configuration['createDisposition'] = self.create_disposition
        if self.default_dataset is not None:
            configuration['defaultDataset'] = {
                'projectId': self.default_dataset.project,
                'datasetId': self.default_dataset.dataset_id,
            }
        if self.destination is not None:
            table_res = self._destination_table_resource()
            configuration['destinationTable'] = table_res
        if self.priority is not None:
            configuration['priority'] = self.priority
        if self.write_disposition is not None:
            configuration['writeDisposition'] = self.write_disposition
        if self.maximum_billing_tier is not None:
            configuration['maximumBillingTier'] = self.maximum_billing_tier
        if self.maximum_bytes_billed is not None:
            configuration['maximumBytesBilled'] = str(
                self.maximum_bytes_billed)
        if len(self._udf_resources) > 0:
            configuration[self._UDF_KEY] = [
                {udf_resource.udf_type: udf_resource.value}
                for udf_resource in self._udf_resources
            ]
        if len(self._query_parameters) > 0:
            configuration[self._QUERY_PARAMETERS_KEY] = [
                query_parameter.to_api_repr()
                for query_parameter in self._query_parameters
            ]
            if self._query_parameters[0].name is None:
                configuration['parameterMode'] = 'POSITIONAL'
            else:
                configuration['parameterMode'] = 'NAMED'

    def _build_resource(self):
        """Generate a resource for :meth:`begin`."""

        resource = {
            'jobReference': {
                'projectId': self.project,
                'jobId': self.job_id,
            },
            'configuration': {
                self._JOB_TYPE: {
                    'query': self.query,
                },
            },
        }

        if self.dry_run is not None:
            resource['configuration']['dryRun'] = self.dry_run

        configuration = resource['configuration'][self._JOB_TYPE]
        self._populate_config_resource(configuration)

        return resource

    def _scrub_local_properties(self, cleaned):
        """Helper:  handle subclass properties in cleaned.

        .. note:

           This method assumes that the project found in the resource matches
           the client's project.
        """
        configuration = cleaned['configuration']['query']

        self.query = configuration['query']

    def _copy_configuration_properties(self, configuration):
        """Helper:  assign subclass configuration properties in cleaned."""
        self.allow_large_results = _bool_or_none(
            configuration.get('allowLargeResults'))
        self.flatten_results = _bool_or_none(
            configuration.get('flattenResults'))
        self.use_query_cache = _bool_or_none(
            configuration.get('useQueryCache'))
        self.use_legacy_sql = _bool_or_none(
            configuration.get('useLegacySql'))

        self.create_disposition = configuration.get('createDisposition')
        self.priority = configuration.get('priority')
        self.write_disposition = configuration.get('writeDisposition')
        self.maximum_billing_tier = configuration.get('maximumBillingTier')
        self.maximum_bytes_billed = _int_or_none(
            configuration.get('maximumBytesBilled'))

        dest_remote = configuration.get('destinationTable')

        if dest_remote is None:
            if self.destination is not None:
                del self.destination
        else:
            dest_local = self._destination_table_resource()
            if dest_remote != dest_local:
                project = dest_remote['projectId']
                dataset = Dataset(
                    dest_remote['datasetId'], self._client, project=project)
                self.destination = dataset.table(dest_remote['tableId'])

        def_ds = configuration.get('defaultDataset')
        if def_ds is None:
            if self.default_dataset is not None:
                del self.default_dataset
        else:
            project = def_ds['projectId']
            self.default_dataset = Dataset(def_ds['datasetId'], self._client)

        udf_resources = []
        for udf_mapping in configuration.get(self._UDF_KEY, ()):
            key_val, = udf_mapping.items()
            udf_resources.append(UDFResource(key_val[0], key_val[1]))
        self._udf_resources = udf_resources

        self._query_parameters = [
            _query_param_from_api_repr(mapping)
            for mapping in configuration.get(self._QUERY_PARAMETERS_KEY, ())
        ]

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a job given its API representation

        :type resource: dict
        :param resource: dataset job representation returned from the API

        :type client: :class:`google.cloud.bigquery.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the dataset.

        :rtype: :class:`google.cloud.bigquery.job.RunAsyncQueryJob`
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
        client = self._require_client(None)
        datasets_by_project_name = {}

        for table in self._job_statistics().get('referencedTables', ()):

            t_project = table['projectId']

            ds_name = table['datasetId']
            t_dataset = datasets_by_project_name.get((t_project, ds_name))
            if t_dataset is None:
                t_dataset = Dataset(ds_name, client, project=t_project)
                datasets_by_project_name[(t_project, ds_name)] = t_dataset

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
            :class:`~google.cloud.bigquery._helpers.AbstractQueryParameter`
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

    def query_results(self):
        """Construct a QueryResults instance, bound to this job.

        :rtype: :class:`~google.cloud.bigquery.query.QueryResults`
        :returns: results instance
        """
        if not self._query_results:
            self._query_results = self._client._get_query_results(self.job_id)
        return self._query_results

    def done(self):
        """Refresh the job and checks if it is complete.

        :rtype: bool
        :returns: True if the job is complete, False otherwise.
        """
        # Do not refresh is the state is already done, as the job will not
        # change once complete.
        if self.state != _DONE_STATE:
            self._query_results = self._client._get_query_results(self.job_id)

            # Only reload the job once we know the query is complete.
            # This will ensure that fields such as the destination table are
            # correctly populated.
            if self._query_results.complete:
                self.reload()

        return self.state == _DONE_STATE

    def result(self, timeout=None):
        """Start the job and wait for it to complete and get the result.

        :type timeout: int
        :param timeout:
            How long to wait for job to complete before raising a
            :class:`TimeoutError`.

        :rtype: :class:`~google.api.core.page_iterator.Iterator`
        :returns:
            Iterator of row data :class:`tuple`s. During each page, the
            iterator will have the ``total_rows`` attribute set, which counts
            the total number of rows **in the result set** (this is distinct
            from the total number of rows in the current page:
            ``iterator.page.num_items``).

        :raises: :class:`~google.cloud.exceptions.GoogleCloudError` if the job
            failed or  :class:`TimeoutError` if the job did not complete in the
            given timeout.
        """
        super(QueryJob, self).result(timeout=timeout)
        # Return an iterator instead of returning the job.
        return self.query_results().fetch_data()


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
