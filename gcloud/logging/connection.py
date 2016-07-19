# Copyright 2016 Google Inc. All rights reserved.
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

"""Create / interact with Stackdriver Logging connections."""

from gcloud import connection as base_connection


class Connection(base_connection.JSONConnection):
    """A connection to Google Stackdriver Logging via the JSON REST API.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        connection.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: (Optional) HTTP object to make requests.

    :type api_base_url: string
    :param api_base_url: The base of the API call URL. Defaults to the value
                         :attr:`Connection.API_BASE_URL`.
    """

    API_BASE_URL = 'https://logging.googleapis.com'
    """The base of the API call URL."""

    API_VERSION = 'v2beta1'
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = '{api_base_url}/{api_version}{path}'
    """A template for the URL of a particular API call."""

    SCOPE = ('https://www.googleapis.com/auth/logging.read',
             'https://www.googleapis.com/auth/logging.write',
             'https://www.googleapis.com/auth/logging.admin',
             'https://www.googleapis.com/auth/cloud-platform')
    """The scopes required for authenticating as a Logging consumer."""


class _LoggingAPI(object):
    """Helper mapping logging-related APIs.

    See:
    https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/entries
    https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.logs

    :type connection: :class:`gcloud.logging.connection.Connection`
    :param connection: the connection used to make API requests.
    """
    def __init__(self, connection):
        self._connection = connection

    def list_entries(self, projects, filter_=None, order_by=None,
                     page_size=None, page_token=None):
        """Return a page of log entry resources.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/entries/list

        :type projects: list of strings
        :param projects: project IDs to include. If not passed,
                            defaults to the project bound to the client.

        :type filter_: str
        :param filter_: a filter expression. See:
                        https://cloud.google.com/logging/docs/view/advanced_filters

        :type order_by: str
        :param order_by: One of :data:`gcloud.logging.ASCENDING` or
                         :data:`gcloud.logging.DESCENDING`.

        :type page_size: int
        :param page_size: maximum number of entries to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of entries. If not
                           passed, the API will return the first page of
                           entries.

        :rtype: tuple, (list, str)
        :returns: list of mappings, plus a "next page token" string:
                  if not None, indicates that more entries can be retrieved
                  with another call (pass that value as ``page_token``).
        """
        params = {'projectIds': projects}

        if filter_ is not None:
            params['filter'] = filter_

        if order_by is not None:
            params['orderBy'] = order_by

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        resp = self._connection.api_request(
            method='POST', path='/entries:list', data=params)

        return resp.get('entries', ()), resp.get('nextPageToken')

    def write_entries(self, entries, logger_name=None, resource=None,
                      labels=None):
        """API call:  log an entry resource via a POST request

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/entries/write

        :type entries: sequence of mapping
        :param entries: the log entry resources to log.

        :type logger_name: string
        :param logger_name: name of default logger to which to log the entries;
                            individual entries may override.

        :type resource: mapping
        :param resource: default resource to associate with entries;
                         individual entries may override.

        :type labels: mapping
        :param labels: default labels to associate with entries;
                       individual entries may override.
        """
        data = {'entries': list(entries)}

        if logger_name is not None:
            data['logName'] = logger_name

        if resource is not None:
            data['resource'] = resource

        if labels is not None:
            data['labels'] = labels

        self._connection.api_request(method='POST', path='/entries:write',
                                     data=data)

    def logger_delete(self, project, logger_name):
        """API call:  delete all entries in a logger via a DELETE request

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.logs/delete

        :type project: string
        :param project: ID of project containing the log entries to delete

        :type logger_name: string
        :param logger_name: name of logger containing the log entries to delete
        """
        path = '/projects/%s/logs/%s' % (project, logger_name)
        self._connection.api_request(method='DELETE', path=path)


class _SinksAPI(object):
    """Helper mapping sink-related APIs.

    See:
    https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.sinks

    :type connection: :class:`gcloud.logging.connection.Connection`
    :param connection: the connection used to make API requests.
    """
    def __init__(self, connection):
        self._connection = connection

    def list_sinks(self, project, page_size=None, page_token=None):
        """List sinks for the project associated with this client.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.sinks/list

        :type project: string
        :param project: ID of the project whose sinks are to be listed.

        :type page_size: int
        :param page_size: maximum number of sinks to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of sinks. If not
                           passed, the API will return the first page of
                           sinks.

        :rtype: tuple, (list, str)
        :returns: list of mappings, plus a "next page token" string:
                  if not None, indicates that more sinks can be retrieved
                  with another call (pass that value as ``page_token``).
        """
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/projects/%s/sinks' % (project,)
        resp = self._connection.api_request(
            method='GET', path=path, query_params=params)
        sinks = resp.get('sinks', ())
        return sinks, resp.get('nextPageToken')

    def sink_create(self, project, sink_name, filter_, destination):
        """API call:  create a sink resource.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.sinks/create

        :type project: string
        :param project: ID of the project in which to create the sink.

        :type sink_name: string
        :param sink_name: the name of the sink

        :type filter_: string
        :param filter_: the advanced logs filter expression defining the
                        entries exported by the sink.

        :type destination: string
        :param destination: destination URI for the entries exported by
                            the sink.
        """
        target = '/projects/%s/sinks' % (project,)
        data = {
            'name': sink_name,
            'filter': filter_,
            'destination': destination,
        }
        self._connection.api_request(method='POST', path=target, data=data)

    def sink_get(self, project, sink_name):
        """API call:  retrieve a sink resource.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.sinks/get

        :type project: string
        :param project: ID of the project containing the sink.

        :type sink_name: string
        :param sink_name: the name of the sink

        :rtype: dict
        :returns: The JSON sink object returned from the API.
        """
        target = '/projects/%s/sinks/%s' % (project, sink_name)
        return self._connection.api_request(method='GET', path=target)

    def sink_update(self, project, sink_name, filter_, destination):
        """API call:  update a sink resource.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.sinks/update

        :type project: string
        :param project: ID of the project containing the sink.

        :type sink_name: string
        :param sink_name: the name of the sink

        :type filter_: string
        :param filter_: the advanced logs filter expression defining the
                        entries exported by the sink.

        :type destination: string
        :param destination: destination URI for the entries exported by
                            the sink.
        """
        target = '/projects/%s/sinks/%s' % (project, sink_name)
        data = {
            'name': sink_name,
            'filter': filter_,
            'destination': destination,
        }
        self._connection.api_request(method='PUT', path=target, data=data)

    def sink_delete(self, project, sink_name):
        """API call:  delete a sink resource.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.sinks/delete

        :type project: string
        :param project: ID of the project containing the sink.

        :type sink_name: string
        :param sink_name: the name of the sink
        """
        target = '/projects/%s/sinks/%s' % (project, sink_name)
        self._connection.api_request(method='DELETE', path=target)


class _MetricsAPI(object):
    """Helper mapping sink-related APIs.

    See:
    https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics

    :type connection: :class:`gcloud.logging.connection.Connection`
    :param connection: the connection used to make API requests.
    """
    def __init__(self, connection):
        self._connection = connection

    def list_metrics(self, project, page_size=None, page_token=None):
        """List metrics for the project associated with this client.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics/list

        :type project: string
        :param project: ID of the project whose metrics are to be listed.

        :type page_size: int
        :param page_size: maximum number of metrics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of metrics. If not
                           passed, the API will return the first page of
                           metrics.

        :rtype: tuple, (list, str)
        :returns: list of mappings, plus a "next page token" string:
                  if not None, indicates that more metrics can be retrieved
                  with another call (pass that value as ``page_token``).
        """
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/projects/%s/metrics' % (project,)
        resp = self._connection.api_request(
            method='GET', path=path, query_params=params)
        metrics = resp.get('metrics', ())
        return metrics, resp.get('nextPageToken')

    def metric_create(self, project, metric_name, filter_, description=None):
        """API call:  create a metric resource.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics/create

        :type project: string
        :param project: ID of the project in which to create the metric.

        :type metric_name: string
        :param metric_name: the name of the metric

        :type filter_: string
        :param filter_: the advanced logs filter expression defining the
                        entries exported by the metric.

        :type description: string
        :param description: description of the metric.
        """
        target = '/projects/%s/metrics' % (project,)
        data = {
            'name': metric_name,
            'filter': filter_,
            'description': description,
        }
        self._connection.api_request(method='POST', path=target, data=data)

    def metric_get(self, project, metric_name):
        """API call:  retrieve a metric resource.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics/get

        :type project: string
        :param project: ID of the project containing the metric.

        :type metric_name: string
        :param metric_name: the name of the metric

        :rtype: dict
        :returns: The JSON metric object returned from the API.
        """
        target = '/projects/%s/metrics/%s' % (project, metric_name)
        return self._connection.api_request(method='GET', path=target)

    def metric_update(self, project, metric_name, filter_, description):
        """API call:  update a metric resource.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics/update

        :type project: string
        :param project: ID of the project containing the metric.

        :type metric_name: string
        :param metric_name: the name of the metric

        :type filter_: string
        :param filter_: the advanced logs filter expression defining the
                        entries exported by the metric.

        :type description: string
        :param description: description of the metric.
        """
        target = '/projects/%s/metrics/%s' % (project, metric_name)
        data = {
            'name': metric_name,
            'filter': filter_,
            'description': description,
        }
        self._connection.api_request(method='PUT', path=target, data=data)

    def metric_delete(self, project, metric_name):
        """API call:  delete a metric resource.

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics/delete

        :type project: string
        :param project: ID of the project containing the metric.

        :type metric_name: string
        :param metric_name: the name of the metric
        """
        target = '/projects/%s/metrics/%s' % (project, metric_name)
        self._connection.api_request(method='DELETE', path=target)
