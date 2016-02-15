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
from gcloud.bigquery._helpers import _EnumProperty
from gcloud.bigquery._helpers import _TypedProperty


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
    """Pseudo-enum for ``QueryJob.priority`` property."""
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
    def job_type(self):
        """Type of job

        :rtype: string
        :returns: one of 'load', 'copy', 'extract', 'query'
        """
        return self._JOB_TYPE

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

    @classmethod
    def _get_resource_config(cls, resource):
        """Helper for :meth:`from_api_repr`

        :type resource: dict
        :param resource: resource for the job

        :rtype: dict
        :returns: tuple (string, dict), where the first element is the
                  job name and the second contains job-specific configuration.
        :raises: :class:`KeyError` if the resource has no identifier, or
                 is missing the appropriate configuration.
        """
        if ('jobReference' not in resource or
                'jobId' not in resource['jobReference']):
            raise KeyError('Resource lacks required identity information: '
                           '["jobReference"]["jobId"]')
        name = resource['jobReference']['jobId']
        if ('configuration' not in resource or
                cls._JOB_TYPE not in resource['configuration']):
            raise KeyError('Resource lacks required configuration: '
                           '["configuration"]["%s"]' % cls._JOB_TYPE)
        config = resource['configuration'][cls._JOB_TYPE]
        return name, config

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
    :param source_uris: URIs of one or more data files to be loaded, in
                        format ``gs://<bucket_name>/<object_name_or_glob>``.

    :type client: :class:`gcloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).

    :type schema: list of :class:`gcloud.bigquery.table.SchemaField`
    :param schema: The job's schema
    """

    _schema = None
    _JOB_TYPE = 'load'

    def __init__(self, name, destination, source_uris, client, schema=()):
        super(LoadTableFromStorageJob, self).__init__(name, client)
        self.destination = destination
        self.source_uris = source_uris
        # Let the @property do validation.
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
                self._JOB_TYPE: {
                    'sourceUris': self.source_uris,
                    'destinationTable': {
                        'projectId': self.destination.project,
                        'datasetId': self.destination.dataset_name,
                        'tableId': self.destination.name,
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

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a job given its API representation

        .. note:

           This method assumes that the project found in the resource matches
           the client's project.

        :type resource: dict
        :param resource: dataset job representation returned from the API

        :type client: :class:`gcloud.bigquery.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the dataset.

        :rtype: :class:`gcloud.bigquery.job.LoadTableFromStorageJob`
        :returns: Job parsed from ``resource``.
        """
        name, config = cls._get_resource_config(resource)
        dest_config = config['destinationTable']
        dataset = Dataset(dest_config['datasetId'], client)
        destination = Table(dest_config['tableId'], dataset)
        source_urls = config.get('sourceUris', ())
        job = cls(name, destination, source_urls, client=client)
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

    _JOB_TYPE = 'copy'

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
                self._JOB_TYPE: {
                    'sourceTables': source_refs,
                    'destinationTable': {
                        'projectId': self.destination.project,
                        'datasetId': self.destination.dataset_name,
                        'tableId': self.destination.name,
                    },
                },
            },
        }
        configuration = resource['configuration'][self._JOB_TYPE]
        self._populate_config_resource(configuration)

        return resource

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a job given its API representation

        .. note:

           This method assumes that the project found in the resource matches
           the client's project.

        :type resource: dict
        :param resource: dataset job representation returned from the API

        :type client: :class:`gcloud.bigquery.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the dataset.

        :rtype: :class:`gcloud.bigquery.job.CopyJob`
        :returns: Job parsed from ``resource``.
        """
        name, config = cls._get_resource_config(resource)
        dest_config = config['destinationTable']
        dataset = Dataset(dest_config['datasetId'], client)
        destination = Table(dest_config['tableId'], dataset)
        sources = []
        for source_config in config['sourceTables']:
            dataset = Dataset(source_config['datasetId'], client)
            sources.append(Table(source_config['tableId'], dataset))
        job = cls(name, destination, sources, client=client)
        job._set_properties(resource)
        return job


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
                             extracted data will be written, in format
                             ``gs://<bucket_name>/<object_name_or_glob>``.

    :type client: :class:`gcloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).
    """
    _JOB_TYPE = 'extract'

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
                self._JOB_TYPE: {
                    'sourceTable': source_ref,
                    'destinationUris': self.destination_uris,
                },
            },
        }
        configuration = resource['configuration'][self._JOB_TYPE]
        self._populate_config_resource(configuration)

        return resource

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a job given its API representation

        .. note:

           This method assumes that the project found in the resource matches
           the client's project.

        :type resource: dict
        :param resource: dataset job representation returned from the API

        :type client: :class:`gcloud.bigquery.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the dataset.

        :rtype: :class:`gcloud.bigquery.job.ExtractTableToStorageJob`
        :returns: Job parsed from ``resource``.
        """
        name, config = cls._get_resource_config(resource)
        source_config = config['sourceTable']
        dataset = Dataset(source_config['datasetId'], client)
        source = Table(source_config['tableId'], dataset)
        destination_uris = config['destinationUris']
        job = cls(name, source, destination_uris, client=client)
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
    _write_disposition = None


class QueryJob(_AsyncJob):
    """Asynchronous job: query tables.

    :type name: string
    :param name: the name of the job

    :type query: string
    :param query: SQL query string

    :type client: :class:`gcloud.bigquery.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the dataset (which requires a project).
    """
    _JOB_TYPE = 'query'

    def __init__(self, name, query, client):
        super(QueryJob, self).__init__(name, client)
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

    destination = _TypedProperty('destination', Table)
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
        if self.destination is not None:
            return {
                'projectId': self.destination.project,
                'datasetId': self.destination.dataset_name,
                'tableId': self.destination.name,
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
        if self.destination is not None:
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
                self._JOB_TYPE: {
                    'query': self.query,
                },
            },
        }
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
        dest_remote = configuration.get('destinationTable')

        if dest_remote is None:
            if self.destination is not None:
                del self.destination
        else:
            dest_local = self._destination_table_resource()
            if dest_remote != dest_local:
                dataset = self._client.dataset(dest_remote['datasetId'])
                self.destination = dataset.table(dest_remote['tableId'])

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a job given its API representation

        :type resource: dict
        :param resource: dataset job representation returned from the API

        :type client: :class:`gcloud.bigquery.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the dataset.

        :rtype: :class:`gcloud.bigquery.job.RunAsyncQueryJob`
        :returns: Job parsed from ``resource``.
        """
        name, config = cls._get_resource_config(resource)
        query = config['query']
        job = cls(name, query, client=client)
        job._set_properties(resource)
        return job
