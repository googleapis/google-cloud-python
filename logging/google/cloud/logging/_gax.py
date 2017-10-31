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

"""GAX wrapper for Logging API requests."""

import functools

from google.api_core import page_iterator
from google.cloud.gapic.logging.v2.config_service_v2_client import (
    ConfigServiceV2Client)
from google.cloud.gapic.logging.v2.logging_service_v2_client import (
    LoggingServiceV2Client)
from google.cloud.gapic.logging.v2.metrics_service_v2_client import (
    MetricsServiceV2Client)
from google.gax import CallOptions
from google.gax import INITIAL_PAGE
from google.gax.errors import GaxError
from google.gax.grpc import exc_to_code
from google.cloud.proto.logging.v2.logging_config_pb2 import LogSink
from google.cloud.proto.logging.v2.logging_metrics_pb2 import LogMetric
from google.cloud.proto.logging.v2.log_entry_pb2 import LogEntry
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import ParseDict
from grpc import StatusCode

from google.cloud._helpers import make_secure_channel
from google.cloud._http import DEFAULT_USER_AGENT
from google.cloud.exceptions import Conflict
from google.cloud.exceptions import NotFound
from google.cloud.logging import __version__
from google.cloud.logging._helpers import entry_from_resource
from google.cloud.logging.sink import Sink
from google.cloud.logging.metric import Metric


class _LoggingAPI(object):
    """Helper mapping logging-related APIs.

    :type gax_api:
        :class:`.logging_service_v2_client.LoggingServiceV2Client`
    :param gax_api: API object used to make GAX requests.

    :type client: :class:`~google.cloud.logging.client.Client`
    :param client: The client that owns this API object.
    """
    def __init__(self, gax_api, client):
        self._gax_api = gax_api
        self._client = client

    def list_entries(self, projects, filter_='', order_by='',
                     page_size=0, page_token=None):
        """Return a page of log entry resources.

        :type projects: list of strings
        :param projects: project IDs to include. If not passed,
                         defaults to the project bound to the API's client.

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
        if page_token is None:
            page_token = INITIAL_PAGE
        options = CallOptions(page_token=page_token)
        page_iter = self._gax_api.list_log_entries(
            [], project_ids=projects, filter_=filter_, order_by=order_by,
            page_size=page_size, options=options)

        # We attach a mutable loggers dictionary so that as Logger
        # objects are created by entry_from_resource, they can be
        # re-used by other log entries from the same logger.
        loggers = {}
        item_to_value = functools.partial(
            _item_to_entry, loggers=loggers)
        return page_iterator._GAXIterator(
            self._client, page_iter, item_to_value)

    def write_entries(self, entries, logger_name=None, resource=None,
                      labels=None):
        """API call:  log an entry resource via a POST request

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
        options = None
        partial_success = False
        entry_pbs = [_log_entry_mapping_to_pb(entry) for entry in entries]
        self._gax_api.write_log_entries(
            entry_pbs, log_name=logger_name, resource=resource, labels=labels,
            partial_success=partial_success, options=options)

    def logger_delete(self, project, logger_name):
        """API call:  delete all entries in a logger via a DELETE request

        :type project: str
        :param project: ID of project containing the log entries to delete

        :type logger_name: str
        :param logger_name: name of logger containing the log entries to delete
        """
        options = None
        path = 'projects/%s/logs/%s' % (project, logger_name)
        try:
            self._gax_api.delete_log(path, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(path)
            raise


class _SinksAPI(object):
    """Helper mapping sink-related APIs.

    :type gax_api:
        :class:`.config_service_v2_client.ConfigServiceV2Client`
    :param gax_api: API object used to make GAX requests.

    :type client: :class:`~google.cloud.logging.client.Client`
    :param client: The client that owns this API object.
    """
    def __init__(self, gax_api, client):
        self._gax_api = gax_api
        self._client = client

    def list_sinks(self, project, page_size=0, page_token=None):
        """List sinks for the project associated with this client.

        :type project: str
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
        if page_token is None:
            page_token = INITIAL_PAGE
        options = CallOptions(page_token=page_token)
        path = 'projects/%s' % (project,)
        page_iter = self._gax_api.list_sinks(path, page_size=page_size,
                                             options=options)
        return page_iterator._GAXIterator(
            self._client, page_iter, _item_to_sink)

    def sink_create(self, project, sink_name, filter_, destination):
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
        """
        options = None
        parent = 'projects/%s' % (project,)
        sink_pb = LogSink(name=sink_name, filter=filter_,
                          destination=destination)
        try:
            self._gax_api.create_sink(parent, sink_pb, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.FAILED_PRECONDITION:
                path = 'projects/%s/sinks/%s' % (project, sink_name)
                raise Conflict(path)
            raise

    def sink_get(self, project, sink_name):
        """API call:  retrieve a sink resource.

        :type project: str
        :param project: ID of the project containing the sink.

        :type sink_name: str
        :param sink_name: the name of the sink

        :rtype: dict
        :returns: The sink object returned from the API (converted from a
                  protobuf to a dictionary).
        """
        options = None
        path = 'projects/%s/sinks/%s' % (project, sink_name)
        try:
            sink_pb = self._gax_api.get_sink(path, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(path)
            raise
        # NOTE: LogSink message type does not have an ``Any`` field
        #       so `MessageToDict`` can safely be used.
        return MessageToDict(sink_pb)

    def sink_update(self, project, sink_name, filter_, destination):
        """API call:  update a sink resource.

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

        :rtype: dict
        :returns: The sink object returned from the API (converted from a
                  protobuf to a dictionary).
        """
        options = None
        path = 'projects/%s/sinks/%s' % (project, sink_name)
        sink_pb = LogSink(name=path, filter=filter_, destination=destination)
        try:
            sink_pb = self._gax_api.update_sink(path, sink_pb, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(path)
            raise
        # NOTE: LogSink message type does not have an ``Any`` field
        #       so `MessageToDict`` can safely be used.
        return MessageToDict(sink_pb)

    def sink_delete(self, project, sink_name):
        """API call:  delete a sink resource.

        :type project: str
        :param project: ID of the project containing the sink.

        :type sink_name: str
        :param sink_name: the name of the sink
        """
        options = None
        path = 'projects/%s/sinks/%s' % (project, sink_name)
        try:
            self._gax_api.delete_sink(path, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(path)
            raise


class _MetricsAPI(object):
    """Helper mapping sink-related APIs.

    :type gax_api:
        :class:`.metrics_service_v2_client.MetricsServiceV2Client`

    :param gax_api: API object used to make GAX requests.

    :type client: :class:`~google.cloud.logging.client.Client`
    :param client: The client that owns this API object.
    """
    def __init__(self, gax_api, client):
        self._gax_api = gax_api
        self._client = client

    def list_metrics(self, project, page_size=0, page_token=None):
        """List metrics for the project associated with this client.

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
        if page_token is None:
            page_token = INITIAL_PAGE
        options = CallOptions(page_token=page_token)
        path = 'projects/%s' % (project,)
        page_iter = self._gax_api.list_log_metrics(
            path, page_size=page_size, options=options)
        return page_iterator._GAXIterator(
            self._client, page_iter, _item_to_metric)

    def metric_create(self, project, metric_name, filter_, description):
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
        options = None
        parent = 'projects/%s' % (project,)
        metric_pb = LogMetric(name=metric_name, filter=filter_,
                              description=description)
        try:
            self._gax_api.create_log_metric(parent, metric_pb, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.FAILED_PRECONDITION:
                path = 'projects/%s/metrics/%s' % (project, metric_name)
                raise Conflict(path)
            raise

    def metric_get(self, project, metric_name):
        """API call:  retrieve a metric resource.

        :type project: str
        :param project: ID of the project containing the metric.

        :type metric_name: str
        :param metric_name: the name of the metric

        :rtype: dict
        :returns: The metric object returned from the API (converted from a
                  protobuf to a dictionary).
        """
        options = None
        path = 'projects/%s/metrics/%s' % (project, metric_name)
        try:
            metric_pb = self._gax_api.get_log_metric(path, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(path)
            raise
        # NOTE: LogMetric message type does not have an ``Any`` field
        #       so `MessageToDict`` can safely be used.
        return MessageToDict(metric_pb)

    def metric_update(self, project, metric_name, filter_, description):
        """API call:  update a metric resource.

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
        :returns: The metric object returned from the API (converted from a
                  protobuf to a dictionary).
        """
        options = None
        path = 'projects/%s/metrics/%s' % (project, metric_name)
        metric_pb = LogMetric(name=path, filter=filter_,
                              description=description)
        try:
            metric_pb = self._gax_api.update_log_metric(
                path, metric_pb, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(path)
            raise
        # NOTE: LogMetric message type does not have an ``Any`` field
        #       so `MessageToDict`` can safely be used.
        return MessageToDict(metric_pb)

    def metric_delete(self, project, metric_name):
        """API call:  delete a metric resource.

        :type project: str
        :param project: ID of the project containing the metric.

        :type metric_name: str
        :param metric_name: the name of the metric
        """
        options = None
        path = 'projects/%s/metrics/%s' % (project, metric_name)
        try:
            self._gax_api.delete_log_metric(path, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(path)
            raise


def _parse_log_entry(entry_pb):
    """Special helper to parse ``LogEntry`` protobuf into a dictionary.

    The ``proto_payload`` field in ``LogEntry`` is of type ``Any``. This
    can be problematic if the type URL in the payload isn't in the
    ``google.protobuf`` registry. To help with parsing unregistered types,
    this function will remove ``proto_payload`` before parsing.

    :type entry_pb: :class:`.log_entry_pb2.LogEntry`
    :param entry_pb: Log entry protobuf.

    :rtype: dict
    :returns: The parsed log entry. The ``protoPayload`` key may contain
              the raw ``Any`` protobuf from ``entry_pb.proto_payload`` if
              it could not be parsed.
    """
    try:
        return MessageToDict(entry_pb)
    except TypeError:
        if entry_pb.HasField('proto_payload'):
            proto_payload = entry_pb.proto_payload
            entry_pb.ClearField('proto_payload')
            entry_mapping = MessageToDict(entry_pb)
            entry_mapping['protoPayload'] = proto_payload
            return entry_mapping
        else:
            raise


def _log_entry_mapping_to_pb(mapping):
    """Helper for :meth:`write_entries`, et aliae

    Performs "impedance matching" between the protobuf attrs and
    the keys expected in the JSON API.
    """
    entry_pb = LogEntry()
    # NOTE: We assume ``mapping`` was created in ``Batch.commit``
    #       or ``Logger._make_entry_resource``. In either case, if
    #       the ``protoPayload`` key is present, we assume that the
    #       type URL is registered with ``google.protobuf`` and will
    #       not cause any issues in the JSON->protobuf conversion
    #       of the corresponding ``proto_payload`` in the log entry
    #       (it is an ``Any`` field).
    ParseDict(mapping, entry_pb)
    return entry_pb


def _item_to_entry(iterator, entry_pb, loggers):
    """Convert a log entry protobuf to the native object.

    .. note::

        This method does not have the correct signature to be used as
        the ``item_to_value`` argument to
        :class:`~google.api_core.page_iterator.Iterator`. It is intended to be
        patched with a mutable ``loggers`` argument that can be updated
        on subsequent calls. For an example, see how the method is
        used above in :meth:`_LoggingAPI.list_entries`.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type entry_pb: :class:`.log_entry_pb2.LogEntry`
    :param entry_pb: Log entry protobuf returned from the API.

    :type loggers: dict
    :param loggers:
        A mapping of logger fullnames -> loggers.  If the logger
        that owns the entry is not in ``loggers``, the entry
        will have a newly-created logger.

    :rtype: :class:`~google.cloud.logging.entries._BaseEntry`
    :returns: The next log entry in the page.
    """
    resource = _parse_log_entry(entry_pb)
    return entry_from_resource(resource, iterator.client, loggers)


def _item_to_sink(iterator, log_sink_pb):
    """Convert a sink protobuf to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type log_sink_pb:
        :class:`.logging_config_pb2.LogSink`
    :param log_sink_pb: Sink protobuf returned from the API.

    :rtype: :class:`~google.cloud.logging.sink.Sink`
    :returns: The next sink in the page.
    """
    # NOTE: LogSink message type does not have an ``Any`` field
    #       so `MessageToDict`` can safely be used.
    resource = MessageToDict(log_sink_pb)
    return Sink.from_api_repr(resource, iterator.client)


def _item_to_metric(iterator, log_metric_pb):
    """Convert a metric protobuf to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type log_metric_pb:
        :class:`.logging_metrics_pb2.LogMetric`
    :param log_metric_pb: Metric protobuf returned from the API.

    :rtype: :class:`~google.cloud.logging.metric.Metric`
    :returns: The next metric in the page.
    """
    # NOTE: LogMetric message type does not have an ``Any`` field
    #       so `MessageToDict`` can safely be used.
    resource = MessageToDict(log_metric_pb)
    return Metric.from_api_repr(resource, iterator.client)


def make_gax_logging_api(client):
    """Create an instance of the GAX Logging API.

    :type client: :class:`~google.cloud.logging.client.Client`
    :param client: The client that holds configuration details.

    :rtype: :class:`_LoggingAPI`
    :returns: A metrics API instance with the proper credentials.
    """
    channel = make_secure_channel(
        client._credentials, DEFAULT_USER_AGENT,
        LoggingServiceV2Client.SERVICE_ADDRESS)
    generated = LoggingServiceV2Client(
        channel=channel, lib_name='gccl', lib_version=__version__)
    return _LoggingAPI(generated, client)


def make_gax_metrics_api(client):
    """Create an instance of the GAX Metrics API.

    :type client: :class:`~google.cloud.logging.client.Client`
    :param client: The client that holds configuration details.

    :rtype: :class:`_MetricsAPI`
    :returns: A metrics API instance with the proper credentials.
    """
    channel = make_secure_channel(
        client._credentials, DEFAULT_USER_AGENT,
        MetricsServiceV2Client.SERVICE_ADDRESS)
    generated = MetricsServiceV2Client(
        channel=channel, lib_name='gccl', lib_version=__version__)
    return _MetricsAPI(generated, client)


def make_gax_sinks_api(client):
    """Create an instance of the GAX Sinks API.

    :type client: :class:`~google.cloud.logging.client.Client`
    :param client: The client that holds configuration details.

    :rtype: :class:`_SinksAPI`
    :returns: A metrics API instance with the proper credentials.
    """
    channel = make_secure_channel(
        client._credentials, DEFAULT_USER_AGENT,
        ConfigServiceV2Client.SERVICE_ADDRESS)
    generated = ConfigServiceV2Client(
        channel=channel, lib_name='gccl', lib_version=__version__)
    return _SinksAPI(generated, client)
