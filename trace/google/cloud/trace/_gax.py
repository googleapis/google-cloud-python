# Copyright 2017 Google Inc.
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

"""GAX Wrapper for interacting with the Stackdriver Trace API."""

from google.cloud.gapic.trace.v1.trace_service_client import (
    TraceServiceClient)
from google.cloud.proto.devtools.cloudtrace.v1.trace_pb2 import (
    TraceSpan, Trace, Traces)

from google.cloud._helpers import make_secure_channel
from google.cloud._http import DEFAULT_USER_AGENT


class _TraceAPI(object):
    """Wrapper to help mapping trace-related APIs.
    
    See
    https://cloud.google.com/trace/docs/reference/v1/rpc/google.devtools.
    cloudtrace.v1
    
    :type gax_api:
        :class:`~google.cloud.gapic.trace.v1.trace_service_client.TraceServiceClient`
    :param gax_api: API object used to make GAX requests.
    
    :type client: :class:`~google.cloud.trace.client.Client`
    :param client: The client that owns this API object.
    """
    def __init__(self, gax_api, client):
        self._gax_api = gax_api
        self.client = client

    def patch_traces(self, project_id, traces, options=None):
        """Sends new traces to Stackdriver Trace or updates existing traces.

        :type project_id: str
        :param project_id: ID of the Cloud project where the trace data is stored.
        
        :type traces: dict
        :param traces: The traces to be patched in the API call.
        
        :type options: :class:`~google.gax.CallOptions`
        :param options: (Optional) Overrides the default settings for this call,
                        e.g, timeout, retries etc.
        """
        traces_pb = _trace_mapping_to_pb(traces)
        self._gax_api.patch_traces(project_id, traces_pb, options)

    def get_trace(self, project_id, trace_id, options=None):
        """Gets a single trace by its ID.

        :type project_id: str
        :param project_id: ID of the Cloud project where the trace data is stored.

        :type trace_id: str
        :param trace_id: ID of the trace to return.

        :type options: :class:`~google.gax.CallOptions`
        :param options: (Optional) Overrides the default settings for this call,
                        e.g, timeout, retries etc.
        
        :rtype: :dict
        :returns: A Trace dict.
        """
        trace_pb = self._gax_api.get_trace(project_id, trace_id, options)
        trace_mapping = _trace_pb_to_mapping(trace_pb)
        return trace_mapping

    def list_traces(
            self,
            project_id,
            view=None,
            page_size=None,
            start_time=None,
            end_time=None,
            filter_=None,
            order_by=None,
            options=None):
        """Returns of a list of traces that match the specified filter conditions.
        
        :type project_id: str
        :param project_id: ID of the Cloud project where the trace data is stored.

        :type view: :class:`google.cloud.gapic.trace.v1.enums.ListTracesRequest.ViewType`
        :param view: (Optional) Type of data returned for traces in the list. 
                     Default is ``MINIMAL``.
        
        :type page_size: int
        :param page_size: (Optional) Maximum number of traces to return. If not specified
                          or <= 0, the implementation selects a reasonable value.
                          The implementation may return fewer traces than the requested
                          page size.
        
        :type start_time: :class:`google.protobuf.timestamp_pb2.Timestamp`
        :param start_time: (Optional) Start of the time interval (inclusive) during which
                           the trace data was collected from the application.
        
        :type end_time: :class:`google.protobuf.timestamp_pb2.Timestamp`
        :param end_time: (Optional) End of the time interval (inclusive) during which
                         the trace data was collected from the application.
        
        :type filter: str
        :param filter_: (Optional) An optional filter for the request.
        
        :type order_by: str
        :param order_by: (Optional) Field used to sort the returned traces.

        :type options: :class:`google.gax.CallOptions`
        :param options: Overrides the default settings for this call.
                        e.g, timeout, retries etc.

        :rtype: dict
        :returns: Traces that match the specified filter conditions.
        """
        page_iter = self._gax_api.list_traces(
            project_id,
            view,
            page_size,
            start_time,
            end_time,
            filter_,
            order_by,
            options)
        traces = [_trace_pb_to_mapping(trace_pb)
                  for trace_pb in page_iter]
        return traces


def _trace_pb_to_mapping(trace_pb):
    """Convert a trace protobuf to dict.
    
    :type trace_pb: class:`google.cloud.proto.devtools.cloudtrace.v1.trace_pb2.Trace`
    :param trace_pb: A trace protobuf instance.

    :rtype: dict
    :return: The converted trace dict.
    """
    mapping = {
        'project_id': trace_pb.project_id,
        'trace_id': trace_pb.trace_id,
    }

    spans = []

    for span_pb in trace_pb.spans:
        span = {
            'span_id': span_pb.span_id,
            'kind': span_pb.kind,
            'name': span_pb.name,
            'parent_span_id': span_pb.parent_span_id,
        }

        # Convert the Timestamp protobuf to dict.
        time_keys = ['start_time', 'end_time']

        for time_key in time_keys:
            time_pb = getattr(span_pb, time_key)
            time_mapping = {
                'seconds': time_pb.seconds,
                'nanos': time_pb.nanos,
            }
            span[time_key] = time_mapping

        labels = {}

        for key, value in span_pb.labels.items():
            labels[key] = value

        span['labels'] = labels
        spans.append(span)

    mapping['spans'] = spans

    return mapping


def _trace_mapping_to_pb(mapping):
    """Convert a trace dict to protobuf.
    
    :type mapping: dict
    :param mapping: A trace mapping.

    :rtype: class:`google.cloud.proto.devtools.cloudtrace.v1.trace_pb2.Trace`
    :return: The converted protobuf type trace.
    """
    # Mapping from the key name in dict to key name in protobuf in a span.
    span_scalar_keys = {
        'spanId': 'span_id',
        'kind': 'kind',
        'name': 'name',
        'parentSpanId': 'parent_span_id',
        'labels': 'labels',
    }

    # Mapping from the key name in dict to key name in protobuf in a trace.
    trace_scalar_keys = {
        'traceId': 'trace_id',
        'projectId': 'project_id',
    }

    traces = []

    for trace in mapping['traces']:
        spans = []

        # Build the protobuf for TraceSpan.
        # Protobuf type attributes cannot be set by setattr.
        for span in trace['spans']:
            span_pb = TraceSpan(start_time=span['startTime'], end_time=span['endTime'])

            for key, pb_name in span_scalar_keys.items():

                if key in span:
                    setattr(span_pb, pb_name, span[key])

            spans.append(span_pb)

        # Build the protobuf for Trace.
        trace_pb = Trace(spans=spans)

        for key, pb_name in trace_scalar_keys.items():

            if key in trace:
                setattr(trace_pb, pb_name, trace[key])

        traces.append(trace_pb)

    # Build the protobuf for Traces.
    traces_pb = Traces(traces=traces)

    return traces_pb


def make_gax_trace_api(client):
    """Create an instance of the GAX Trace API.

    :type client: :class:`~google.cloud.trace.client.Client`
    :param client: The client that holds configuration details.

    :rtype: :class:`~google.cloud.trace._gax._TraceAPI`
    :return: A Trace API instance with the proper configurations.
    """
    channel = make_secure_channel(
        client._credentials,
        DEFAULT_USER_AGENT,
        TraceServiceClient.SERVICE_ADDRESS)
    generated = TraceServiceClient(channel=channel, lib_name='gccl')
    return _TraceAPI(generated, client)
