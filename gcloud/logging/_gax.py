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

"""GAX wrapper for Logging API requests."""

import json

# pylint: disable=import-error
from google.gax import CallOptions
from google.gax import INITIAL_PAGE
from google.gax.errors import GaxError
from google.gax.grpc import exc_to_code
from google.logging.type.log_severity_pb2 import LogSeverity
from google.logging.v2.logging_config_pb2 import LogSink
from google.logging.v2.logging_metrics_pb2 import LogMetric
from google.logging.v2.log_entry_pb2 import LogEntry
from google.protobuf.json_format import Parse
from grpc.beta.interfaces import StatusCode
# pylint: enable=import-error

from gcloud.exceptions import Conflict
from gcloud.exceptions import NotFound
from gcloud._helpers import _datetime_to_pb_timestamp
from gcloud._helpers import _datetime_to_rfc3339
from gcloud._helpers import _pb_timestamp_to_datetime


class _LoggingAPI(object):
    """Helper mapping logging-related APIs.

    :type gax_api:
        :class:`google.logging.v2.logging_service_v2_api.LoggingServiceV2Api`
    :param gax_api: API object used to make GAX requests.
    """
    def __init__(self, gax_api):
        self._gax_api = gax_api

    def list_entries(self, projects, filter_='', order_by='',
                     page_size=0, page_token=None):
        """Return a page of log entry resources.

        :type projects: list of strings
        :param projects: project IDs to include. If not passed,
                         defaults to the project bound to the API's client.

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
        options = _build_paging_options(page_token)
        page_iter = self._gax_api.list_log_entries(
            projects, filter_, order_by, page_size, options)
        entries = [_log_entry_pb_to_mapping(entry_pb)
                   for entry_pb in page_iter.next()]
        token = page_iter.page_token or None
        return entries, token

    def write_entries(self, entries, logger_name=None, resource=None,
                      labels=None):
        """API call:  log an entry resource via a POST request

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
        options = None
        partial_success = False
        entry_pbs = [_log_entry_mapping_to_pb(entry) for entry in entries]
        self._gax_api.write_log_entries(entry_pbs, logger_name, resource,
                                        labels, partial_success, options)

    def logger_delete(self, project, logger_name):
        """API call:  delete all entries in a logger via a DELETE request

        :type project: string
        :param project: ID of project containing the log entries to delete

        :type logger_name: string
        :param logger_name: name of logger containing the log entries to delete
        """
        options = None
        path = 'projects/%s/logs/%s' % (project, logger_name)
        self._gax_api.delete_log(path, options)


class _SinksAPI(object):
    """Helper mapping sink-related APIs.

    :type gax_api:
        :class:`google.logging.v2.config_service_v2_api.ConfigServiceV2Api`
    :param gax_api: API object used to make GAX requests.
    """
    def __init__(self, gax_api):
        self._gax_api = gax_api

    def list_sinks(self, project, page_size=0, page_token=None):
        """List sinks for the project associated with this client.

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
        options = _build_paging_options(page_token)
        page_iter = self._gax_api.list_sinks(project, page_size, options)
        sinks = [_log_sink_pb_to_mapping(log_sink_pb)
                 for log_sink_pb in page_iter.next()]
        token = page_iter.page_token or None
        return sinks, token

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
        options = None
        parent = 'projects/%s' % (project,)
        sink_pb = LogSink(name=sink_name, filter=filter_,
                          destination=destination)
        try:
            self._gax_api.create_sink(parent, sink_pb, options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.FAILED_PRECONDITION:
                path = 'projects/%s/sinks/%s' % (project, sink_name)
                raise Conflict(path)
            raise

    def sink_get(self, project, sink_name):
        """API call:  retrieve a sink resource.

        :type project: string
        :param project: ID of the project containing the sink.

        :type sink_name: string
        :param sink_name: the name of the sink
        """
        options = None
        path = 'projects/%s/sinks/%s' % (project, sink_name)
        try:
            sink_pb = self._gax_api.get_sink(path, options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(path)
            raise
        return _log_sink_pb_to_mapping(sink_pb)

    def sink_update(self, project, sink_name, filter_, destination):
        """API call:  update a sink resource.

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
        options = None
        path = 'projects/%s/sinks/%s' % (project, sink_name)
        sink_pb = LogSink(name=path, filter=filter_, destination=destination)
        try:
            self._gax_api.update_sink(path, sink_pb, options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(path)
            raise
        return _log_sink_pb_to_mapping(sink_pb)

    def sink_delete(self, project, sink_name):
        """API call:  delete a sink resource.

        :type project: string
        :param project: ID of the project containing the sink.

        :type sink_name: string
        :param sink_name: the name of the sink
        """
        options = None
        path = 'projects/%s/sinks/%s' % (project, sink_name)
        try:
            self._gax_api.delete_sink(path, options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(path)
            raise


class _MetricsAPI(object):
    """Helper mapping sink-related APIs.

    :type gax_api:
        :class:`google.logging.v2.metrics_service_v2_api.MetricsServiceV2Api`
    :param gax_api: API object used to make GAX requests.
    """
    def __init__(self, gax_api):
        self._gax_api = gax_api

    def list_metrics(self, project, page_size=0, page_token=None):
        """List metrics for the project associated with this client.

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
        options = _build_paging_options(page_token)
        page_iter = self._gax_api.list_log_metrics(project, page_size, options)
        metrics = [_log_metric_pb_to_mapping(log_metric_pb)
                   for log_metric_pb in page_iter.next()]
        token = page_iter.page_token or None
        return metrics, token

    def metric_create(self, project, metric_name, filter_, description):
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
        options = None
        parent = 'projects/%s' % (project,)
        metric_pb = LogMetric(name=metric_name, filter=filter_,
                              description=description)
        try:
            self._gax_api.create_log_metric(parent, metric_pb, options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.FAILED_PRECONDITION:
                path = 'projects/%s/metrics/%s' % (project, metric_name)
                raise Conflict(path)
            raise

    def metric_get(self, project, metric_name):
        """API call:  retrieve a metric resource.

        :type project: string
        :param project: ID of the project containing the metric.

        :type metric_name: string
        :param metric_name: the name of the metric
        """
        options = None
        path = 'projects/%s/metrics/%s' % (project, metric_name)
        try:
            metric_pb = self._gax_api.get_log_metric(path, options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(path)
            raise
        return _log_metric_pb_to_mapping(metric_pb)

    def metric_update(self, project, metric_name, filter_, description):
        """API call:  update a metric resource.

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
        options = None
        path = 'projects/%s/metrics/%s' % (project, metric_name)
        metric_pb = LogMetric(name=path, filter=filter_,
                              description=description)
        try:
            self._gax_api.update_log_metric(path, metric_pb, options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(path)
            raise
        return _log_metric_pb_to_mapping(metric_pb)

    def metric_delete(self, project, metric_name):
        """API call:  delete a metric resource.

        :type project: string
        :param project: ID of the project containing the metric.

        :type metric_name: string
        :param metric_name: the name of the metric
        """
        options = None
        path = 'projects/%s/metrics/%s' % (project, metric_name)
        try:
            self._gax_api.delete_log_metric(path, options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(path)
            raise


def _build_paging_options(page_token=None):
    """Helper for :meth:'_PublisherAPI.list_topics' et aliae."""
    if page_token is None:
        page_token = INITIAL_PAGE
    options = {'page_token': page_token}
    return CallOptions(**options)


def _mon_resource_pb_to_mapping(resource_pb):
    """Helper for  :func:_log_entry_pb_to_mapping"""
    mapping = {
        'type': resource_pb.type,
    }
    if resource_pb.labels:
        mapping['labels'] = resource_pb.labels
    return mapping


def _pb_timestamp_to_rfc3339(timestamp_pb):
    """Helper for  :func:_log_entry_pb_to_mapping"""
    timestamp = _pb_timestamp_to_datetime(timestamp_pb)
    return _datetime_to_rfc3339(timestamp)


def _log_entry_pb_to_mapping(entry_pb):
    """Helper for :meth:`list_entries`, et aliae

    Ideally, would use a function from :mod:`protobuf.json_format`, but
    the right one isn't public.  See:
    https://github.com/google/protobuf/issues/1351
    """
    mapping = {
        'logName': entry_pb.log_name,
        'resource': _mon_resource_pb_to_mapping(entry_pb.resource),
        'severity': entry_pb.severity,
        'insertId': entry_pb.insert_id,
        'timestamp': _pb_timestamp_to_rfc3339(entry_pb.timestamp),
        'labels': entry_pb.labels,
        'textPayload': entry_pb.text_payload,
        'jsonPayload': entry_pb.json_payload,
        'protoPayload': entry_pb.proto_payload,
    }

    if entry_pb.http_request:
        request = entry_pb.http_request
        mapping['httpRequest'] = {
            'request_method': request.request_method,
            'request_url': request.request_url,
            'status': request.status,
            'referer': request.referer,
            'user_agent': request.user_agent,
            'cache_hit': request.cache_hit,
            'request_size': request.request_size,
            'response_size': request.response_size,
            'remote_ip': request.remote_ip,
        }

    if entry_pb.operation:
        operation = entry_pb.operation
        mapping['operation'] = {
            'producer': operation.producer,
            'id': operation.id,
            'first': operation.first,
            'last': operation.last,
        }

    return mapping


def _http_request_mapping_to_pb(info, request):
    """Helper for _log_entry_mapping_to_pb"""
    optional_request_keys = {
        'requestMethod': 'request_method',
        'requestUrl': 'request_url',
        'status': 'status',
        'referer': 'referer',
        'userAgent': 'user_agent',
        'cacheHit': 'cache_hit',
        'requestSize': 'request_size',
        'responseSize': 'response_size',
        'remoteIp': 'remote_ip',
    }
    for key, pb_name in optional_request_keys.items():
        if key in info:
            setattr(request, pb_name, info[key])


def _log_operation_mapping_to_pb(info, operation):
    """Helper for _log_entry_mapping_to_pb"""
    operation.producer = info['producer']
    operation.id = info['id']

    if 'first' in info:
        operation.first = info['first']

    if 'last' in info:
        operation.last = info['last']


def _log_entry_mapping_to_pb(mapping):
    """Helper for :meth:`write_entries`, et aliae

    Ideally, would use a function from :mod:`protobuf.json_format`, but
    the right one isn't public.  See:
    https://github.com/google/protobuf/issues/1351
    """
    # pylint: disable=too-many-branches
    entry_pb = LogEntry()

    optional_scalar_keys = {
        'logName': 'log_name',
        'insertId': 'insert_id',
        'textPayload': 'text_payload',
    }

    for key, pb_name in optional_scalar_keys.items():
        if key in mapping:
            setattr(entry_pb, pb_name, mapping[key])

    if 'resource' in mapping:
        entry_pb.resource.type = mapping['resource']['type']

    if 'severity' in mapping:
        severity = mapping['severity']
        if isinstance(severity, str):
            severity = LogSeverity.Value(severity)
        entry_pb.severity = severity

    if 'timestamp' in mapping:
        timestamp = _datetime_to_pb_timestamp(mapping['timestamp'])
        entry_pb.timestamp.CopyFrom(timestamp)

    if 'labels' in mapping:
        for key, value in mapping['labels'].items():
            entry_pb.labels[key] = value

    if 'jsonPayload' in mapping:
        for key, value in mapping['jsonPayload'].items():
            entry_pb.json_payload[key] = value

    if 'protoPayload' in mapping:
        Parse(json.dumps(mapping['protoPayload']), entry_pb.proto_payload)

    if 'httpRequest' in mapping:
        _http_request_mapping_to_pb(
            mapping['httpRequest'], entry_pb.http_request)

    if 'operation' in mapping:
        _log_operation_mapping_to_pb(
            mapping['operation'], entry_pb.operation)

    return entry_pb
    # pylint: enable=too-many-branches


def _log_sink_pb_to_mapping(sink_pb):
    """Helper for :meth:`list_sinks`, et aliae

    Ideally, would use a function from :mod:`protobuf.json_format`, but
    the right one isn't public.  See:
    https://github.com/google/protobuf/issues/1351
    """
    return {
        'name': sink_pb.name,
        'destination': sink_pb.destination,
        'filter': sink_pb.filter,
    }


def _log_metric_pb_to_mapping(metric_pb):
    """Helper for :meth:`list_metrics`, et aliae

    Ideally, would use a function from :mod:`protobuf.json_format`, but
    the right one isn't public.  See:
    https://github.com/google/protobuf/issues/1351
    """
    return {
        'name': metric_pb.name,
        'description': metric_pb.description,
        'filter': metric_pb.filter,
    }
