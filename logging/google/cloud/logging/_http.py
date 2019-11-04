# Copyright 2016 Google LLC
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

"""Interact with Stackdriver Logging via JSON-over-HTTP."""

import functools

from google.api_core import page_iterator
from google.cloud import _http

from google.cloud.logging import __version__
from google.cloud.logging._helpers import entry_from_resource
from google.cloud.logging.sink import Sink
from google.cloud.logging.metric import Metric


class Connection(_http.JSONConnection):
    """A connection to Google Stackdriver Logging via the JSON REST API.

    :type client: :class:`~google.cloud.logging.client.Client`
    :param client: The client that owns the current connection.

    :type client_info: :class:`~google.api_core.client_info.ClientInfo`
    :param client_info: (Optional) instance used to generate user agent.

    :type client_options: :class:`~google.api_core.client_options.ClientOptions`
    :param client_options (Optional) Client options used to set user options
        on the client. API Endpoint should be set through client_options.
    """

    DEFAULT_API_ENDPOINT = "https://logging.googleapis.com"

    def __init__(self, client, client_info=None, api_endpoint=DEFAULT_API_ENDPOINT):
        super(Connection, self).__init__(client, client_info)
        self.API_BASE_URL = api_endpoint
        self._client_info.gapic_version = __version__
        self._client_info.client_library_version = __version__

    API_VERSION = "v2"
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = "{api_base_url}/{api_version}{path}"
    """A template for the URL of a particular API call."""


class _LoggingAPI(object):
    """Helper mapping logging-related APIs.

    See
    https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries
    https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.logs

    :type client: :class:`~google.cloud.logging.client.Client`
    :param client: The client used to make API requests.
    """

    def __init__(self, client):
        self._client = client
        self.api_request = client._connection.api_request

    def list_entries(
        self, projects, filter_=None, order_by=None, page_size=None, page_token=None
    ):
        """Return a page of log entry resources.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/list

        :type projects: list of strings
        :param projects: project IDs to include. If not passed,
                            defaults to the project bound to the client.

        :type filter_: str
        :param filter_:
            a filter expression. See
            https://cloud.google.com/logging/docs/view/advanced_filters

        :type order_by: str
        :param order_by: One of :data:`~google.cloud.logging.ASCENDING`
                         or :data:`~google.cloud.logging.DESCENDING`.

        :type page_size: int
        :param page_size: maximum number of entries to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of entries. If not
                           passed, the API will return the first page of
                           entries.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of :class:`~google.cloud.logging.entries._BaseEntry`
                  accessible to the current API.
        """
        extra_params = {"projectIds": projects}

        if filter_ is not None:
            extra_params["filter"] = filter_

        if order_by is not None:
            extra_params["orderBy"] = order_by

        if page_size is not None:
            extra_params["pageSize"] = page_size

        path = "/entries:list"
        # We attach a mutable loggers dictionary so that as Logger
        # objects are created by entry_from_resource, they can be
        # re-used by other log entries from the same logger.
        loggers = {}
        item_to_value = functools.partial(_item_to_entry, loggers=loggers)
        iterator = page_iterator.HTTPIterator(
            client=self._client,
            api_request=self._client._connection.api_request,
            path=path,
            item_to_value=item_to_value,
            items_key="entries",
            page_token=page_token,
            extra_params=extra_params,
        )
        # This method uses POST to make a read-only request.
        iterator._HTTP_METHOD = "POST"
        return iterator

    def write_entries(self, entries, logger_name=None, resource=None, labels=None):
        """API call:  log an entry resource via a POST request

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/write

        :type entries: sequence of mapping
        :param entries: the log entry resources to log.

        :type logger_name: str
        :param logger_name: name of default logger to which to log the entries;
                            individual entries may override.

        :type resource: mapping
        :param resource: default resource to associate with entries;
                         individual entries may override.

        :type labels: mapping
        :param labels: default labels to associate with entries;
                       individual entries may override.
        """
        data = {"entries": list(entries)}

        if logger_name is not None:
            data["logName"] = logger_name

        if resource is not None:
            data["resource"] = resource

        if labels is not None:
            data["labels"] = labels

        self.api_request(method="POST", path="/entries:write", data=data)

    def logger_delete(self, project, logger_name):
        """API call:  delete all entries in a logger via a DELETE request

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.logs/delete

        :type project: str
        :param project: ID of project containing the log entries to delete

        :type logger_name: str
        :param logger_name: name of logger containing the log entries to delete
        """
        path = "/projects/%s/logs/%s" % (project, logger_name)
        self.api_request(method="DELETE", path=path)


class _SinksAPI(object):
    """Helper mapping sink-related APIs.

    See
    https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.sinks

    :type client: :class:`~google.cloud.logging.client.Client`
    :param client: The client used to make API requests.
    """

    def __init__(self, client):
        self._client = client
        self.api_request = client._connection.api_request

    def list_sinks(self, project, page_size=None, page_token=None):
        """List sinks for the project associated with this client.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.sinks/list

        :type project: str
        :param project: ID of the project whose sinks are to be listed.

        :type page_size: int
        :param page_size: maximum number of sinks to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of sinks. If not
                           passed, the API will return the first page of
                           sinks.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of
                  :class:`~google.cloud.logging.sink.Sink`
                  accessible to the current API.
        """
        extra_params = {}

        if page_size is not None:
            extra_params["pageSize"] = page_size

        path = "/projects/%s/sinks" % (project,)
        return page_iterator.HTTPIterator(
            client=self._client,
            api_request=self._client._connection.api_request,
            path=path,
            item_to_value=_item_to_sink,
            items_key="sinks",
            page_token=page_token,
            extra_params=extra_params,
        )

    def sink_create(
        self, project, sink_name, filter_, destination, unique_writer_identity=False
    ):
        """API call:  create a sink resource.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.sinks/create

        :type project: str
        :param project: ID of the project in which to create the sink.

        :type sink_name: str
        :param sink_name: the name of the sink

        :type filter_: str
        :param filter_: the advanced logs filter expression defining the
                        entries exported by the sink.

        :type destination: str
        :param destination: destination URI for the entries exported by
                            the sink.

        :type unique_writer_identity: bool
        :param unique_writer_identity: (Optional) determines the kind of
                                       IAM identity returned as
                                       writer_identity in the new sink.

        :rtype: dict
        :returns: The returned (created) resource.
        """
        target = "/projects/%s/sinks" % (project,)
        data = {"name": sink_name, "filter": filter_, "destination": destination}
        query_params = {"uniqueWriterIdentity": unique_writer_identity}
        return self.api_request(
            method="POST", path=target, data=data, query_params=query_params
        )

    def sink_get(self, project, sink_name):
        """API call:  retrieve a sink resource.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.sinks/get

        :type project: str
        :param project: ID of the project containing the sink.

        :type sink_name: str
        :param sink_name: the name of the sink

        :rtype: dict
        :returns: The JSON sink object returned from the API.
        """
        target = "/projects/%s/sinks/%s" % (project, sink_name)
        return self.api_request(method="GET", path=target)

    def sink_update(
        self, project, sink_name, filter_, destination, unique_writer_identity=False
    ):
        """API call:  update a sink resource.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.sinks/update

        :type project: str
        :param project: ID of the project containing the sink.

        :type sink_name: str
        :param sink_name: the name of the sink

        :type filter_: str
        :param filter_: the advanced logs filter expression defining the
                        entries exported by the sink.

        :type destination: str
        :param destination: destination URI for the entries exported by
                            the sink.

        :type unique_writer_identity: bool
        :param unique_writer_identity: (Optional) determines the kind of
                                       IAM identity returned as
                                       writer_identity in the new sink.

        :rtype: dict
        :returns: The returned (updated) resource.
        """
        target = "/projects/%s/sinks/%s" % (project, sink_name)
        data = {"name": sink_name, "filter": filter_, "destination": destination}
        query_params = {"uniqueWriterIdentity": unique_writer_identity}
        return self.api_request(
            method="PUT", path=target, query_params=query_params, data=data
        )

    def sink_delete(self, project, sink_name):
        """API call:  delete a sink resource.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.sinks/delete

        :type project: str
        :param project: ID of the project containing the sink.

        :type sink_name: str
        :param sink_name: the name of the sink
        """
        target = "/projects/%s/sinks/%s" % (project, sink_name)
        self.api_request(method="DELETE", path=target)


class _MetricsAPI(object):
    """Helper mapping sink-related APIs.

    See
    https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.metrics

    :type client: :class:`~google.cloud.logging.client.Client`
    :param client: The client used to make API requests.
    """

    def __init__(self, client):
        self._client = client
        self.api_request = client._connection.api_request

    def list_metrics(self, project, page_size=None, page_token=None):
        """List metrics for the project associated with this client.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.metrics/list

        :type project: str
        :param project: ID of the project whose metrics are to be listed.

        :type page_size: int
        :param page_size: maximum number of metrics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of metrics. If not
                           passed, the API will return the first page of
                           metrics.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of
                  :class:`~google.cloud.logging.metric.Metric`
                  accessible to the current API.
        """
        extra_params = {}

        if page_size is not None:
            extra_params["pageSize"] = page_size

        path = "/projects/%s/metrics" % (project,)
        return page_iterator.HTTPIterator(
            client=self._client,
            api_request=self._client._connection.api_request,
            path=path,
            item_to_value=_item_to_metric,
            items_key="metrics",
            page_token=page_token,
            extra_params=extra_params,
        )

    def metric_create(self, project, metric_name, filter_, description=None):
        """API call:  create a metric resource.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.metrics/create

        :type project: str
        :param project: ID of the project in which to create the metric.

        :type metric_name: str
        :param metric_name: the name of the metric

        :type filter_: str
        :param filter_: the advanced logs filter expression defining the
                        entries exported by the metric.

        :type description: str
        :param description: description of the metric.
        """
        target = "/projects/%s/metrics" % (project,)
        data = {"name": metric_name, "filter": filter_, "description": description}
        self.api_request(method="POST", path=target, data=data)

    def metric_get(self, project, metric_name):
        """API call:  retrieve a metric resource.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.metrics/get

        :type project: str
        :param project: ID of the project containing the metric.

        :type metric_name: str
        :param metric_name: the name of the metric

        :rtype: dict
        :returns: The JSON metric object returned from the API.
        """
        target = "/projects/%s/metrics/%s" % (project, metric_name)
        return self.api_request(method="GET", path=target)

    def metric_update(self, project, metric_name, filter_, description):
        """API call:  update a metric resource.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.metrics/update

        :type project: str
        :param project: ID of the project containing the metric.

        :type metric_name: str
        :param metric_name: the name of the metric

        :type filter_: str
        :param filter_: the advanced logs filter expression defining the
                        entries exported by the metric.

        :type description: str
        :param description: description of the metric.

        :rtype: dict
        :returns: The returned (updated) resource.
        """
        target = "/projects/%s/metrics/%s" % (project, metric_name)
        data = {"name": metric_name, "filter": filter_, "description": description}
        return self.api_request(method="PUT", path=target, data=data)

    def metric_delete(self, project, metric_name):
        """API call:  delete a metric resource.

        See
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.metrics/delete

        :type project: str
        :param project: ID of the project containing the metric.

        :type metric_name: str
        :param metric_name: the name of the metric.
        """
        target = "/projects/%s/metrics/%s" % (project, metric_name)
        self.api_request(method="DELETE", path=target)


def _item_to_entry(iterator, resource, loggers):
    """Convert a log entry resource to the native object.

    .. note::

        This method does not have the correct signature to be used as
        the ``item_to_value`` argument to
        :class:`~google.api_core.page_iterator.Iterator`. It is intended to be
        patched with a mutable ``loggers`` argument that can be updated
        on subsequent calls. For an example, see how the method is
        used above in :meth:`_LoggingAPI.list_entries`.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: Log entry JSON resource returned from the API.

    :type loggers: dict
    :param loggers:
        A mapping of logger fullnames -> loggers.  If the logger
        that owns the entry is not in ``loggers``, the entry
        will have a newly-created logger.

    :rtype: :class:`~google.cloud.logging.entries._BaseEntry`
    :returns: The next log entry in the page.
    """
    return entry_from_resource(resource, iterator.client, loggers)


def _item_to_sink(iterator, resource):
    """Convert a sink resource to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: Sink JSON resource returned from the API.

    :rtype: :class:`~google.cloud.logging.sink.Sink`
    :returns: The next sink in the page.
    """
    return Sink.from_api_repr(resource, iterator.client)


def _item_to_metric(iterator, resource):
    """Convert a metric resource to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: Metric JSON resource returned from the API.

    :rtype: :class:`~google.cloud.logging.metric.Metric`
    :returns: The next metric in the page.
    """
    return Metric.from_api_repr(resource, iterator.client)
