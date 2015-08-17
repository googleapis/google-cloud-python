# Copyright 2015 Google Inc. All rights reserved.
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

import six

from gcloud.exceptions import NotFound
from gcloud._helpers import _datetime_from_microseconds
from gcloud.bigquery.table import SchemaField
from gcloud.bigquery.table import _build_schema_resource
from gcloud.bigquery.table import _parse_schema_resource


class _Enum(object):
    """Psedo-enumeration class.

    Subclasses must define ``ALLOWED`` as a class-level constant:  it must
    be a sequence of strings.
    """
    @classmethod
    def validate(cls, value):
        """Check that ``value`` is one of the allowed values.

        :raises: ValueError if value is not allowed.
        """
        if value not in cls.ALLOWED:
            raise ValueError('Pass one of: %s' ', '.join(cls.ALLOWED))


class CreateDisposition(_Enum):
    """Pseudo-enum for allowed values for ``create_disposition`` properties.
    """
    CREATE_IF_NEEDED = 'CREATE_IF_NEEDED'
    CREATE_NEVER = 'CREATE_NEVER'
    ALLOWED = (CREATE_IF_NEEDED, CREATE_NEVER)


class Encoding(_Enum):
    """Pseudo-enum for allowed values for ``encoding`` properties."""
    UTF_8 = 'UTF-8'
    ISO_8559_1 = 'ISO-8559-1'
    ALLOWED = (UTF_8, ISO_8559_1)


class SourceFormat(_Enum):
    """Pseudo-enum for allowed values for ``source_format`` properties."""
    CSV = 'CSV'
    DATASTORE_BACKUP = 'DATASTORE_BACKUP'
    NEWLINE_DELIMITED_JSON = 'NEWLINE_DELIMITED_JSON'
    ALLOWED = (CSV, DATASTORE_BACKUP, NEWLINE_DELIMITED_JSON)


class WriteDisposition(_Enum):
    """Pseudo-enum for allowed values for ``write_disposition`` properties."""
    WRITE_APPEND = 'WRITE_APPEND'
    WRITE_TRUNCATE = 'WRITE_TRUNCATE'
    WRITE_EMPTY = 'WRITE_EMPTY'
    ALLOWED = (WRITE_APPEND, WRITE_TRUNCATE, WRITE_EMPTY)


class _LoadConfiguration(object):
    """User-settable configuration options for load jobs."""
    # None -> use server default.
    _allow_jagged_rows = None
    _allow_quoted_newlines = None
    _create_disposition = None
    _encoding = None
    _field_delimiter = None
    _ignore_unknown_values = None
    _max_bad_records = None
    _quote_character = None
    _skip_leading_rows = None
    _source_format = None
    _write_disposition = None


class LoadFromStorageJob(object):
    """Asynchronous job for loading data into a BQ table from CloudStorage.

    :type name: string
    :param name: the name of the job

    :type destination: :class:`gcloud.bigquery.table.Table`
    :param destination: Table into which data is to be loaded.

    :type source_uris: sequence of string
    :param source_uris: URIs of data files to be loaded.

    :type client: :class:`gcloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).

    :type schema: list of :class:`gcloud.bigquery.table.SchemaField`
    :param schema: The job's schema
    """
    def __init__(self, name, destination, source_uris, client, schema=()):
        self.name = name
        self.destination = destination
        self._client = client
        self.source_uris = source_uris
        self.schema = schema
        self._properties = {}
        self._configuration = _LoadConfiguration()

    @property
    def project(self):
        """Project bound to the job.

        :rtype: string
        :returns: the project (derived from the client).
        """
        return self._client.project

    @property
    def path(self):
        """URL path for the job's APIs.

        :rtype: string
        :returns: the path based on project and job name.
        """
        return '/projects/%s/jobs/%s' % (self.project, self.name)

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

        :raises: TypeError if 'value' is not a sequence, or ValueError if
                 any item in the sequence is not a SchemaField
        """
        if not all(isinstance(field, SchemaField) for field in value):
            raise ValueError('Schema items must be fields')
        self._schema = tuple(value)

    @property
    def etag(self):
        """ETag for the job resource.

        :rtype: string, or ``NoneType``
        :returns: the ETag (None until set from the server).
        """
        return self._properties.get('etag')

    @property
    def job_id(self):
        """ID for the job resource.

        :rtype: string, or ``NoneType``
        :returns: the ID (None until set from the server).
        """
        return self._properties.get('id')

    @property
    def self_link(self):
        """URL for the job resource.

        :rtype: string, or ``NoneType``
        :returns: the URL (None until set from the server).
        """
        return self._properties.get('selfLink')

    @property
    def user_email(self):
        """E-mail address of user who submitted the job.

        :rtype: string, or ``NoneType``
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

    @property
    def input_file_bytes(self):
        """Count of bytes loaded from source files.

        :rtype: integer, or ``NoneType``
        :returns: the count (None until set from the server).
        """
        statistics = self._properties.get('statistics')
        if statistics is not None:
            return int(statistics['load']['inputFileBytes'])

    @property
    def input_files(self):
        """Count of source files.

        :rtype: integer, or ``NoneType``
        :returns: the count (None until set from the server).
        """
        statistics = self._properties.get('statistics')
        if statistics is not None:
            return int(statistics['load']['inputFiles'])

    @property
    def output_bytes(self):
        """Count of bytes saved to destination table.

        :rtype: integer, or ``NoneType``
        :returns: the count (None until set from the server).
        """
        statistics = self._properties.get('statistics')
        if statistics is not None:
            return int(statistics['load']['outputBytes'])

    @property
    def output_rows(self):
        """Count of rows saved to destination table.

        :rtype: integer, or ``NoneType``
        :returns: the count (None until set from the server).
        """
        statistics = self._properties.get('statistics')
        if statistics is not None:
            return int(statistics['load']['outputRows'])

    @property
    def error_result(self):
        """Error information about the job as a whole.

        :rtype: mapping, or ``NoneType``
        :returns: the error information (None until set from the server).
        """
        status = self._properties.get('status')
        if status is not None:
            return status['errorResult']

    @property
    def errors(self):
        """Information about individual errors generated by the job.

        :rtype: list of mappings, or ``NoneType``
        :returns: the error information (None until set from the server).
        """
        status = self._properties.get('status')
        if status is not None:
            return status['errors']

    @property
    def state(self):
        """Status of the job.

        :rtype: string, or ``NoneType``
        :returns: the state (None until set from the server).
        """
        status = self._properties.get('status')
        if status is not None:
            return status['state']

    @property
    def allow_jagged_rows(self):
        """Allow rows with missing trailing commas for optional fields.

        :rtype: boolean, or ``NoneType``
        :returns: The value as set by the user, or None (the default).
        """
        return self._configuration._allow_jagged_rows

    @allow_jagged_rows.setter
    def allow_jagged_rows(self, value):
        """Update allow_jagged_rows.

        :type value: boolean
        :param value: new allow_jagged_rows

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, bool):
            raise ValueError("Pass a boolean")
        self._configuration._allow_jagged_rows = value

    @allow_jagged_rows.deleter
    def allow_jagged_rows(self):
        """Delete allow_jagged_rows."""
        del self._configuration._allow_jagged_rows

    @property
    def allow_quoted_newlines(self):
        """Allow rows with quoted newlines.

        :rtype: boolean, or ``NoneType``
        :returns: The value as set by the user, or None (the default).
        """
        return self._configuration._allow_quoted_newlines

    @allow_quoted_newlines.setter
    def allow_quoted_newlines(self, value):
        """Update allow_quoted_newlines.

        :type value: boolean
        :param value: new allow_quoted_newlines

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, bool):
            raise ValueError("Pass a boolean")
        self._configuration._allow_quoted_newlines = value

    @allow_quoted_newlines.deleter
    def allow_quoted_newlines(self):
        """Delete allow_quoted_newlines."""
        del self._configuration._allow_quoted_newlines

    @property
    def create_disposition(self):
        """Handling for missing destination table.

        :rtype: string, or ``NoneType``
        :returns: The value as set by the user, or None (the default).
        """
        return self._configuration._create_disposition

    @create_disposition.setter
    def create_disposition(self, value):
        """Update create_disposition.

        :type value: string
        :param value: allowed values for :class:`CreateDisposition`.
        """
        CreateDisposition.validate(value)   # raises ValueError if invalid
        self._configuration._create_disposition = value

    @create_disposition.deleter
    def create_disposition(self):
        """Delete create_disposition."""
        del self._configuration._create_disposition

    @property
    def encoding(self):
        """Encoding for source data.

        :rtype: string, or ``NoneType``
        :returns: The value as set by the user, or None (the default).
        """
        return self._configuration._encoding

    @encoding.setter
    def encoding(self, value):
        """Update encoding.

        :type value: string
        :param value: allowed values for :class:`Encoding`.
        """
        Encoding.validate(value)    # raises ValueError if invalid
        self._configuration._encoding = value

    @encoding.deleter
    def encoding(self):
        """Delete encoding."""
        del self._configuration._encoding

    @property
    def field_delimiter(self):
        """Allow rows with missing trailing commas for optional fields.

        :rtype: string, or ``NoneType``
        :returns: The value as set by the user, or None (the default).
        """
        return self._configuration._field_delimiter

    @field_delimiter.setter
    def field_delimiter(self, value):
        """Update field_delimiter.

        :type value: string
        :param value: new field delimiter

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types):
            raise ValueError("Pass a string")
        self._configuration._field_delimiter = value

    @field_delimiter.deleter
    def field_delimiter(self):
        """Delete field_delimiter."""
        del self._configuration._field_delimiter

    @property
    def ignore_unknown_values(self):
        """Ignore rows with extra columns beyond those specified by the schema.

        :rtype: boolean, or ``NoneType``
        :returns: The value as set by the user, or None (the default).
        """
        return self._configuration._ignore_unknown_values

    @ignore_unknown_values.setter
    def ignore_unknown_values(self, value):
        """Update ignore_unknown_values.

        :type value: boolean
        :param value: new ignore_unknown_values

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, bool):
            raise ValueError("Pass a boolean")
        self._configuration._ignore_unknown_values = value

    @ignore_unknown_values.deleter
    def ignore_unknown_values(self):
        """Delete ignore_unknown_values."""
        del self._configuration._ignore_unknown_values

    @property
    def max_bad_records(self):
        """Max number of bad records to be ignored.

        :rtype: integer, or ``NoneType``
        :returns: The value as set by the user, or None (the default).
        """
        return self._configuration._max_bad_records

    @max_bad_records.setter
    def max_bad_records(self, value):
        """Update max_bad_records.

        :type value: integer
        :param value: new max_bad_records

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.integer_types):
            raise ValueError("Pass an integer")
        self._configuration._max_bad_records = value

    @max_bad_records.deleter
    def max_bad_records(self):
        """Delete max_bad_records."""
        del self._configuration._max_bad_records

    @property
    def quote_character(self):
        """Character used to quote values.

        :rtype: string, or ``NoneType``
        :returns: The value as set by the user, or None (the default).
        """
        return self._configuration._quote_character

    @quote_character.setter
    def quote_character(self, value):
        """Update quote_character.

        :type value: string
        :param value: new quote_character

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types):
            raise ValueError("Pass a string")
        self._configuration._quote_character = value

    @quote_character.deleter
    def quote_character(self):
        """Delete quote_character."""
        del self._configuration._quote_character

    @property
    def skip_leading_rows(self):
        """Count of leading rows to be skipped.

        :rtype: integer, or ``NoneType``
        :returns: The value as set by the user, or None (the default).
        """
        return self._configuration._skip_leading_rows

    @skip_leading_rows.setter
    def skip_leading_rows(self, value):
        """Update skip_leading_rows.

        :type value: integer
        :param value: new skip_leading_rows

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.integer_types):
            raise ValueError("Pass a boolean")
        self._configuration._skip_leading_rows = value

    @skip_leading_rows.deleter
    def skip_leading_rows(self):
        """Delete skip_leading_rows."""
        del self._configuration._skip_leading_rows

    @property
    def source_format(self):
        """Format of source data files.

        :rtype: string, or ``NoneType``
        :returns: The value as set by the user, or None (the default).
        """
        return self._configuration._source_format

    @source_format.setter
    def source_format(self, value):
        """Update source_format.

        :type value: string
        :param value: valid values for :class:`SourceFormat`.
        """
        SourceFormat.validate(value)    # raises ValueError if invalid
        self._configuration._source_format = value

    @source_format.deleter
    def source_format(self):
        """Delete source_format."""
        del self._configuration._source_format

    @property
    def write_disposition(self):
        """Allow rows with missing trailing commas for optional fields.

        :rtype: boolean, or ``NoneType``
        :returns: The value as set by the user, or None (the default).
        """
        return self._configuration._write_disposition

    @write_disposition.setter
    def write_disposition(self, value):
        """Update write_disposition.

        :type value: string
        :param value: valid values for :class:`WriteDisposition`.
        """
        WriteDisposition.validate(value)  # raises ValueError if invalid
        self._configuration._write_disposition = value

    @write_disposition.deleter
    def write_disposition(self):
        """Delete write_disposition."""
        del self._configuration._write_disposition

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: :class:`gcloud.bigquery.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    def _populate_config_resource(self, configuration):
        """Helper for _build_resource: copy config properties to resource"""
        if self.allow_jagged_rows is not None:
            configuration['allowJaggedRows'] = self.allow_jagged_rows
        if self.allow_quoted_newlines is not None:
            configuration['allowQuotedNewlines'] = self.allow_quoted_newlines
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
        if self.quote_character is not None:
            configuration['quote'] = self.quote_character
        if self.skip_leading_rows is not None:
            configuration['skipLeadingRows'] = self.skip_leading_rows
        if self.source_format is not None:
            configuration['sourceFormat'] = self.source_format
        if self.write_disposition is not None:
            configuration['writeDisposition'] = self.write_disposition

    def _build_resource(self):
        """Generate a resource for ``begin``."""
        resource = {
            'jobReference': {
                'projectId': self.project,
                'jobId': self.name,
            },
            'configuration': {
                'load': {
                    'sourceUris': self.source_uris,
                    'destinationTable': {
                        'projectId': self.destination.project,
                        'datasetId': self.destination.dataset_name,
                        'tableId': self.destination.name,
                    },
                },
            },
        }
        configuration = resource['configuration']['load']
        self._populate_config_resource(configuration)

        if len(self.schema) > 0:
            configuration['schema'] = {
                'fields': _build_schema_resource(self.schema)}

        return resource

    def _set_properties(self, api_response):
        """Update properties from resource in body of ``api_response``

        :type api_response: httplib2.Response
        :param api_response: response returned from an API call
        """
        self._properties.clear()
        cleaned = api_response.copy()
        schema = cleaned.pop('schema', {'fields': ()})
        self.schema = _parse_schema_resource(schema)

        statistics = cleaned.get('statistics', {})
        if 'creationTime' in statistics:
            statistics['creationTime'] = float(statistics['creationTime'])
        if 'startTime' in statistics:
            statistics['startTime'] = float(statistics['startTime'])
        if 'endTime' in statistics:
            statistics['endTime'] = float(statistics['endTime'])

        self._properties.update(cleaned)

    def begin(self, client=None):
        """API call:  begin the job via a POST request

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/insert

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        path = '/projects/%s/jobs' % (self.project,)
        api_response = client.connection.api_request(
            method='POST', path=path, data=self._build_resource())
        self._set_properties(api_response)

    def exists(self, client=None):
        """API call:  test for the existence of the job via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/get

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)

        try:
            client.connection.api_request(method='GET', path=self.path,
                                          query_params={'fields': 'id'})
        except NotFound:
            return False
        else:
            return True

    def reload(self, client=None):
        """API call:  refresh job properties via a GET request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/get

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)

        api_response = client.connection.api_request(
            method='GET', path=self.path)
        self._set_properties(api_response)

    def cancel(self, client=None):
        """API call:  cancel job via a POST request

        See
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/cancel

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)

        api_response = client.connection.api_request(
            method='POST', path='%s/cancel' % self.path)
        self._set_properties(api_response)
