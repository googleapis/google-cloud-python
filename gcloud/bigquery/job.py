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
from gcloud.bigquery.dataset import Dataset
from gcloud.bigquery.table import SchemaField
from gcloud.bigquery.table import Table
from gcloud.bigquery.table import _build_schema_resource
from gcloud.bigquery.table import _parse_schema_resource
from gcloud.bigquery._helpers import _rows_from_json


class _ConfigurationProperty(object):
    """Base property implementation.

    Values will be stored on a `_configuration` helper attribute of the
    property's job instance.

    :type name: string
    :param name:  name of the property
    """

    def __init__(self, name):
        self.name = name
        self._backing_name = '_%s' % (self.name,)

    def __get__(self, instance, owner):
        """Descriptor protocal:  accesstor"""
        if instance is None:
            return self
        return getattr(instance._configuration, self._backing_name)

    def _validate(self, value):
        """Subclasses override to impose validation policy."""
        pass

    def __set__(self, instance, value):
        """Descriptor protocal:  mutator"""
        self._validate(value)
        setattr(instance._configuration, self._backing_name, value)

    def __delete__(self, instance):
        """Descriptor protocal:  deleter"""
        delattr(instance._configuration, self._backing_name)


class _TypedProperty(_ConfigurationProperty):
    """Property implementation:  validates based on value type.

    :type name: string
    :param name:  name of the property

    :type property_type: type or sequence of types
    :param property_type: type to be validated
    """
    def __init__(self, name, property_type):
        super(_TypedProperty, self).__init__(name)
        self.property_type = property_type

    def _validate(self, value):
        if not isinstance(value, self.property_type):
            raise ValueError('Required type: %s' % (self.property_type,))


class _EnumProperty(_ConfigurationProperty):
    """Psedo-enumeration class.

    Subclasses must define ``ALLOWED`` as a class-level constant:  it must
    be a sequence of strings.

    :type name: string
    :param name:  name of the property
    """
    def _validate(self, value):
        """Check that ``value`` is one of the allowed values.

        :raises: ValueError if value is not allowed.
        """
        if value not in self.ALLOWED:
            raise ValueError('Pass one of: %s' ', '.join(self.ALLOWED))


class Compression(_EnumProperty):
    """Pseudo-enum for ``compression`` properties."""
    GZIP = 'GZIP'
    NONE = 'NONE'
    ALLOWED = (GZIP, NONE)


class CreateDisposition(_EnumProperty):
    """Pseudo-enum for ``create_disposition`` properties."""
    CREATE_IF_NEEDED = 'CREATE_IF_NEEDED'
    CREATE_NEVER = 'CREATE_NEVER'
    ALLOWED = (CREATE_IF_NEEDED, CREATE_NEVER)


class DestinationFormat(_EnumProperty):
    """Pseudo-enum for ``destination_format`` properties."""
    CSV = 'CSV'
    NEWLINE_DELIMITED_JSON = 'NEWLINE_DELIMITED_JSON'
    AVRO = 'AVRO'
    ALLOWED = (CSV, NEWLINE_DELIMITED_JSON, AVRO)


class Encoding(_EnumProperty):
    """Pseudo-enum for ``encoding`` properties."""
    UTF_8 = 'UTF-8'
    ISO_8559_1 = 'ISO-8559-1'
    ALLOWED = (UTF_8, ISO_8559_1)


class QueryPriority(_EnumProperty):
    """Pseudo-enum for ``RunAsyncQueryJob.priority`` property."""
    INTERACTIVE = 'INTERACTIVE'
    BATCH = 'BATCH'
    ALLOWED = (INTERACTIVE, BATCH)


class SourceFormat(_EnumProperty):
    """Pseudo-enum for ``source_format`` properties."""
    CSV = 'CSV'
    DATASTORE_BACKUP = 'DATASTORE_BACKUP'
    NEWLINE_DELIMITED_JSON = 'NEWLINE_DELIMITED_JSON'
    ALLOWED = (CSV, DATASTORE_BACKUP, NEWLINE_DELIMITED_JSON)


class WriteDisposition(_EnumProperty):
    """Pseudo-enum for ``write_disposition`` properties."""
    WRITE_APPEND = 'WRITE_APPEND'
    WRITE_TRUNCATE = 'WRITE_TRUNCATE'
    WRITE_EMPTY = 'WRITE_EMPTY'
    ALLOWED = (WRITE_APPEND, WRITE_TRUNCATE, WRITE_EMPTY)


class _BaseJob(object):
    """Base class for jobs.

    :type client: :class:`gcloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).
    """
    def __init__(self, client):
        self._client = client
        self._properties = {}

    @property
    def project(self):
        """Project bound to the job.

        :rtype: string
        :returns: the project (derived from the client).
        """
        return self._client.project

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


class _AsyncJob(_BaseJob):
    """Base class for asynchronous jobs.

    :type name: string
    :param name: the name of the job

    :type client: :class:`gcloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).
    """
    def __init__(self, name, client):
        super(_AsyncJob, self).__init__(client)
        self.name = name

    @property
    def path(self):
        """URL path for the job's APIs.

        :rtype: string
        :returns: the path based on project and job name.
        """
        return '/projects/%s/jobs/%s' % (self.project, self.name)

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

        :rtype: string, or ``NoneType``
        :returns: the state (None until set from the server).
        """
        status = self._properties.get('status')
        if status is not None:
            return status.get('state')

    def _scrub_local_properties(self, cleaned):
        """Helper:  handle subclass properties in cleaned."""
        pass

    def _set_properties(self, api_response):
        """Update properties from resource in body of ``api_response``

        :type api_response: httplib2.Response
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
            method='POST', path='%s/cancel' % (self.path,))
        self._set_properties(api_response)


class _LoadConfiguration(object):
    """User-settable configuration options for load jobs.

    Values which are ``None`` -> server defaults.
    """
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


class LoadTableFromStorageJob(_AsyncJob):
    """Asynchronous job for loading data into a table from CloudStorage.

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
        super(LoadTableFromStorageJob, self).__init__(name, client)
        self.destination = destination
        self.source_uris = source_uris
        self.schema = schema
        self._configuration = _LoadConfiguration()

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

    allow_jagged_rows = _TypedProperty('allow_jagged_rows', bool)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load.allowJaggedRows
    """

    allow_quoted_newlines = _TypedProperty('allow_quoted_newlines', bool)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load.allowQuotedNewlines
    """

    create_disposition = CreateDisposition('create_disposition')
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load.createDisposition
    """

    encoding = Encoding('encoding')
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load.encoding
    """

    field_delimiter = _TypedProperty('field_delimiter', six.string_types)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load.fieldDelimiter
    """

    ignore_unknown_values = _TypedProperty('ignore_unknown_values', bool)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load.ignoreUnknownValues
    """

    max_bad_records = _TypedProperty('max_bad_records', six.integer_types)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load.maxBadRecords
    """

    quote_character = _TypedProperty('quote_character', six.string_types)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load.quote
    """

    skip_leading_rows = _TypedProperty('skip_leading_rows', six.integer_types)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load.skipLeadingRows
    """

    source_format = SourceFormat('source_format')
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load.sourceFormat
    """

    write_disposition = WriteDisposition('write_disposition')
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load.writeDisposition
    """

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
        """Generate a resource for :meth:`begin`."""
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

    def _scrub_local_properties(self, cleaned):
        """Helper:  handle subclass properties in cleaned."""
        schema = cleaned.pop('schema', {'fields': ()})
        self.schema = _parse_schema_resource(schema)


class _CopyConfiguration(object):
    """User-settable configuration options for copy jobs.

    Values which are ``None`` -> server defaults.
    """
    _create_disposition = None
    _write_disposition = None


class CopyJob(_AsyncJob):
    """Asynchronous job: copy data into a table from other tables.

    :type name: string
    :param name: the name of the job

    :type destination: :class:`gcloud.bigquery.table.Table`
    :param destination: Table into which data is to be loaded.

    :type sources: list of :class:`gcloud.bigquery.table.Table`
    :param sources: Table into which data is to be loaded.

    :type client: :class:`gcloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).
    """
    def __init__(self, name, destination, sources, client):
        super(CopyJob, self).__init__(name, client)
        self.destination = destination
        self.sources = sources
        self._configuration = _CopyConfiguration()

    create_disposition = CreateDisposition('create_disposition')
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.copy.createDisposition
    """

    write_disposition = WriteDisposition('write_disposition')
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.copy.writeDisposition
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
            'datasetId': table.dataset_name,
            'tableId': table.name,
        } for table in self.sources]

        resource = {
            'jobReference': {
                'projectId': self.project,
                'jobId': self.name,
            },
            'configuration': {
                'copy': {
                    'sourceTables': source_refs,
                    'destinationTable': {
                        'projectId': self.destination.project,
                        'datasetId': self.destination.dataset_name,
                        'tableId': self.destination.name,
                    },
                },
            },
        }
        configuration = resource['configuration']['copy']
        self._populate_config_resource(configuration)

        return resource


class _ExtractConfiguration(object):
    """User-settable configuration options for extract jobs.

    Values which are ``None`` -> server defaults.
    """
    _compression = None
    _destination_format = None
    _field_delimiter = None
    _print_header = None


class ExtractTableToStorageJob(_AsyncJob):
    """Asynchronous job: extract data from a table into Cloud Storage.

    :type name: string
    :param name: the name of the job

    :type source: :class:`gcloud.bigquery.table.Table`
    :param source: Table into which data is to be loaded.

    :type destination_uris: list of string
    :param destination_uris: URIs describing Cloud Storage blobs into which
                             extracted data will be written.

    :type client: :class:`gcloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).
    """
    def __init__(self, name, source, destination_uris, client):
        super(ExtractTableToStorageJob, self).__init__(name, client)
        self.source = source
        self.destination_uris = destination_uris
        self._configuration = _ExtractConfiguration()

    compression = Compression('compression')
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.extracted.compression
    """

    destination_format = DestinationFormat('destination_format')
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.extracted.destinationFormat
    """

    field_delimiter = _TypedProperty('field_delimiter', six.string_types)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.extracted.fieldDelimiter
    """

    print_header = _TypedProperty('print_header', bool)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.extracted.printHeader
    """

    def _populate_config_resource(self, configuration):
        """Helper for _build_resource: copy config properties to resource"""
        if self.compression is not None:
            configuration['compression'] = self.compression
        if self.destination_format is not None:
            configuration['destinationFormat'] = self.destination_format
        if self.field_delimiter is not None:
            configuration['fieldDelimiter'] = self.field_delimiter
        if self.print_header is not None:
            configuration['printHeader'] = self.print_header

    def _build_resource(self):
        """Generate a resource for :meth:`begin`."""

        source_ref = {
            'projectId': self.source.project,
            'datasetId': self.source.dataset_name,
            'tableId': self.source.name,
        }

        resource = {
            'jobReference': {
                'projectId': self.project,
                'jobId': self.name,
            },
            'configuration': {
                'extract': {
                    'sourceTable': source_ref,
                    'destinationUris': self.destination_uris,
                },
            },
        }
        configuration = resource['configuration']['extract']
        self._populate_config_resource(configuration)

        return resource


class _AsyncQueryConfiguration(object):
    """User-settable configuration options for asynchronous query jobs.

    Values which are ``None`` -> server defaults.
    """
    _allow_large_results = None
    _create_disposition = None
    _default_dataset = None
    _destination_table = None
    _flatten_results = None
    _priority = None
    _use_query_cache = None
    _write_disposition = None


class RunAsyncQueryJob(_AsyncJob):
    """Asynchronous job: query tables.

    :type name: string
    :param name: the name of the job

    :type query: string
    :param query: SQL query string

    :type client: :class:`gcloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).
    """
    def __init__(self, name, query, client):
        super(RunAsyncQueryJob, self).__init__(name, client)
        self.query = query
        self._configuration = _AsyncQueryConfiguration()

    allow_large_results = _TypedProperty('allow_large_results', bool)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.query.allowLargeResults
    """

    create_disposition = CreateDisposition('create_disposition')
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.query.createDisposition
    """

    default_dataset = _TypedProperty('default_dataset', Dataset)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.query.defaultDataset
    """

    destination_table = _TypedProperty('destination_table', Table)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.query.destinationTable
    """

    flatten_results = _TypedProperty('flatten_results', bool)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.query.flattenResults
    """

    priority = QueryPriority('priority')
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.query.priority
    """

    use_query_cache = _TypedProperty('use_query_cache', bool)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.query.useQueryCache
    """

    write_disposition = WriteDisposition('write_disposition')
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.query.writeDisposition
    """

    def _destination_table_resource(self):
        if self.destination_table is not None:
            return {
                'projectId': self.destination_table.project,
                'datasetId': self.destination_table.dataset_name,
                'tableId': self.destination_table.name,
            }

    def _populate_config_resource(self, configuration):
        """Helper for _build_resource: copy config properties to resource"""
        if self.allow_large_results is not None:
            configuration['allowLargeResults'] = self.allow_large_results
        if self.create_disposition is not None:
            configuration['createDisposition'] = self.create_disposition
        if self.default_dataset is not None:
            configuration['defaultDataset'] = {
                'projectId': self.default_dataset.project,
                'datasetId': self.default_dataset.name,
            }
        if self.destination_table is not None:
            table_res = self._destination_table_resource()
            configuration['destinationTable'] = table_res
        if self.flatten_results is not None:
            configuration['flattenResults'] = self.flatten_results
        if self.priority is not None:
            configuration['priority'] = self.priority
        if self.use_query_cache is not None:
            configuration['useQueryCache'] = self.use_query_cache
        if self.write_disposition is not None:
            configuration['writeDisposition'] = self.write_disposition

    def _build_resource(self):
        """Generate a resource for :meth:`begin`."""

        resource = {
            'jobReference': {
                'projectId': self.project,
                'jobId': self.name,
            },
            'configuration': {
                'query': {
                    'query': self.query,
                },
            },
        }
        configuration = resource['configuration']['query']
        self._populate_config_resource(configuration)

        return resource

    def _scrub_local_properties(self, cleaned):
        """Helper:  handle subclass properties in cleaned."""
        configuration = cleaned['configuration']['query']
        dest_remote = configuration.get('destinationTable')

        if dest_remote is None:
            if self.destination_table is not None:
                del self.destination_table
        else:
            dest_local = self._destination_table_resource()
            if dest_remote != dest_local:
                assert dest_remote['projectId'] == self.project
                dataset = self._client.dataset(dest_remote['datasetId'])
                self.destination_table = dataset.table(dest_remote['tableId'])


class _SyncQueryConfiguration(object):
    """User-settable configuration options for synchronous query jobs.

    Values which are ``None`` -> server defaults.
    """
    _default_dataset = None
    _max_results = None
    _timeout_ms = None
    _preserve_nulls = None
    _use_query_cache = None


class RunSyncQueryJob(_BaseJob):
    """Synchronous job: query tables.

    :type query: string
    :param query: SQL query string

    :type client: :class:`gcloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).
    """
    def __init__(self, query, client):
        super(RunSyncQueryJob, self).__init__(client)
        self.query = query
        self._configuration = _SyncQueryConfiguration()

    @property
    def cache_hit(self):
        """Query results served from cache.

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#cacheHit

        :rtype: boolean or ``NoneType``
        :returns: True if the query results were served from cache (None
                  until set by the server).
        """
        return self._properties.get('cacheHit')

    @property
    def complete(self):
        """Server completed query.

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#jobComplete

        :rtype: boolean or ``NoneType``
        :returns: True if the query completed on the server (None
                  until set by the server).
        """
        return self._properties.get('jobComplete')

    @property
    def errors(self):
        """Errors generated by the query.

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#errors

        :rtype: list of mapping, or ``NoneType``
        :returns: Mappings describing errors generated on the server (None
                  until set by the server).
        """
        return self._properties.get('errors')

    @property
    def name(self):
        """Job name, generated by the back-end.

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#jobReference

        :rtype: list of mapping, or ``NoneType``
        :returns: Mappings describing errors generated on the server (None
                  until set by the server).
        """
        return self._properties.get('jobReference', {}).get('jobId')

    @name.setter
    def name(self, value):
        """Update name of the query.

        :type value: string, or ``NoneType``
        :param value: new name

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['jobReference'] = {
            'projectId': self.project,
            'jobId': value,
        }

    @property
    def page_token(self):
        """Token for fetching next bach of results.

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#pageToken

        :rtype: string, or ``NoneType``
        :returns: Token generated on the server (None until set by the server).
        """
        return self._properties.get('pageToken')

    @property
    def total_rows(self):
        """Total number of rows returned by the query

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#totalRows

        :rtype: integer, or ``NoneType``
        :returns: Count generated on the server (None until set by the server).
        """
        return self._properties.get('totalRows')

    @property
    def total_bytes_processed(self):
        """Total number of bytes processed by the query

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#totalBytesProcessed

        :rtype: integer, or ``NoneType``
        :returns: Count generated on the server (None until set by the server).
        """
        return self._properties.get('totalBytesProcessed')

    @property
    def rows(self):
        """Query results.

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#rows

        :rtype: list of tuples of row values, or ``NoneType``
        :returns: fields describing the schema (None until set by the server).
        """
        return _rows_from_json(self._properties.get('rows', ()), self.schema)

    @property
    def schema(self):
        """Schema for query results.

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#schema

        :rtype: list of :class:`SchemaField`, or ``NoneType``
        :returns: fields describing the schema (None until set by the server).
        """
        return _parse_schema_resource(self._properties.get('schema', {}))

    default_dataset = _TypedProperty('default_dataset', Dataset)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#defaultDataset
    """

    max_results = _TypedProperty('max_results', six.integer_types)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#maxResults
    """

    preserve_nulls = _TypedProperty('preserve_nulls', bool)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#preserveNulls
    """

    timeout_ms = _TypedProperty('timeout_ms', six.integer_types)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#timeoutMs
    """

    use_query_cache = _TypedProperty('use_query_cache', bool)
    """See:
    https://cloud.google.com/bigquery/docs/reference/v2/jobs/query#useQueryCache
    """

    def _set_properties(self, api_response):
        """Update properties from resource in body of ``api_response``

        :type api_response: httplib2.Response
        :param api_response: response returned from an API call
        """
        self._properties.clear()
        self._properties.update(api_response)

    def _build_resource(self):
        """Generate a resource for :meth:`begin`."""
        resource = {'query': self.query}

        if self.default_dataset is not None:
            resource['defaultDataset'] = {
                'projectId': self.project,
                'datasetId': self.default_dataset.name,
            }

        if self.max_results is not None:
            resource['maxResults'] = self.max_results

        if self.preserve_nulls is not None:
            resource['preserveNulls'] = self.preserve_nulls

        if self.timeout_ms is not None:
            resource['timeoutMs'] = self.timeout_ms

        if self.use_query_cache is not None:
            resource['useQueryCache'] = self.use_query_cache

        return resource

    def run(self, client=None):
        """API call:  run the query via a POST request

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/query

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.
        """
        client = self._require_client(client)
        path = '/projects/%s/queries' % (self.project,)
        api_response = client.connection.api_request(
            method='POST', path=path, data=self._build_resource())
        self._set_properties(api_response)

    def fetch_data(self, max_results=None, page_token=None, start_index=None,
                   timeout_ms=None, client=None):
        """API call:  fetch a page of query result data via a GET request

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/getQueryResults

        :type max_results: integer or ``NoneType``
        :param max_results: maximum number of rows to return.

        :type page_token: string or ``NoneType``
        :param page_token: token representing a cursor into the table's rows.

        :type start_index: integer or ``NoneType``
        :param start_index: zero-based index of starting row

        :type timeout_ms: integer or ``NoneType``
        :param timeout_ms: timeout, in milliseconds, to wait for query to
                           complete

        :type client: :class:`gcloud.bigquery.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current dataset.

        :rtype: tuple
        :returns: ``(row_data, total_rows, page_token)``, where ``row_data``
                  is a list of tuples, one per result row, containing only
                  the values;  ``total_rows`` is a count of the total number
                  of rows in the table;  and ``page_token`` is an opaque
                  string which can be used to fetch the next batch of rows
                  (``None`` if no further batches can be fetched).
        :raises: ValueError if the query has not yet been executed.
        """
        if self.name is None:
            raise ValueError("Query not yet executed:  call 'run()'")

        client = self._require_client(client)
        params = {}

        if max_results is not None:
            params['maxResults'] = max_results

        if page_token is not None:
            params['pageToken'] = page_token

        if start_index is not None:
            params['startIndex'] = start_index

        if timeout_ms is not None:
            params['timeoutMs'] = timeout_ms

        path = '/projects/%s/queries/%s' % (self.project, self.name)
        response = client.connection.api_request(method='GET',
                                                 path=path,
                                                 query_params=params)
        self._set_properties(response)

        total_rows = response.get('totalRows')
        page_token = response.get('pageToken')
        rows_data = _rows_from_json(response.get('rows', ()), self.schema)

        return rows_data, total_rows, page_token
