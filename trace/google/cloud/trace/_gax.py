# Copyright 2017 Google LLC
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

from google.api_core import page_iterator
from google.cloud.gapic.trace.v1 import trace_service_client
from google.cloud.proto.devtools.cloudtrace.v1 import trace_pb2
from google.gax import CallOptions
from google.gax import INITIAL_PAGE
from google.cloud._helpers import make_secure_channel
from google.cloud._http import DEFAULT_USER_AGENT
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import ParseDict


class _TraceAPI(object):
    """Wrapper to help mapping trace-related APIs.

    See
    https://cloud.google.com/trace/docs/reference/v1/rpc/google.devtools.
    cloudtrace.v1

    :type gax_api:
        :class:`~google.cloud.gapic.trace.v1.trace_service_client.
               TraceServiceClient`
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
        :param project_id: ID of the Cloud project where the trace data is
                           stored.

        :type traces: dict
        :param traces: The traces to be patched in the API call.

        :type options: :class:`~google.gax.CallOptions`
        :param options: (Optional) Overrides the default settings for this
                        call, e.g, timeout, retries etc.
        """
        traces_pb = _traces_mapping_to_pb(traces)
        self._gax_api.patch_traces(project_id, traces_pb, options)

    def get_trace(self, project_id, trace_id, options=None):
        """Gets a single trace by its ID.

        :type project_id: str
        :param project_id: ID of the Cloud project where the trace data is
                           stored.

        :type trace_id: str
        :param trace_id: ID of the trace to return.

        :type options: :class:`~google.gax.CallOptions`
        :param options: (Optional) Overrides the default settings for this
                        call, e.g, timeout, retries etc.

        :rtype: :dict
        :returns: A Trace dict.
        """
        trace_pb = self._gax_api.get_trace(project_id, trace_id, options)
        trace_mapping = _parse_trace_pb(trace_pb)
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
            page_token=None):
        """Returns of a list of traces that match the specified filter
        conditions.

        :type project_id: str
        :param project_id: ID of the Cloud project where the trace data is
                           stored.

        :type view: :class:`google.cloud.gapic.trace.v1.enums.
                           ListTracesRequest.ViewType`
        :param view: (Optional) Type of data returned for traces in the list.
                     Default is ``MINIMAL``.

        :type page_size: int
        :param page_size: (Optional) Maximum number of traces to return.
                          If not specified or <= 0, the implementation selects
                          a reasonable value. The implementation may return
                          fewer traces than the requested page size.

        :type start_time: :class:`google.protobuf.timestamp_pb2.Timestamp`
        :param start_time: (Optional) Start of the time interval (inclusive)
                           during which the trace data was collected from the
                           application.

        :type end_time: :class:`google.protobuf.timestamp_pb2.Timestamp`
        :param end_time: (Optional) End of the time interval (inclusive)
                         during which the trace data was collected from the
                         application.

        :type filter_: str
        :param filter_: (Optional) An optional filter for the request.

        :type order_by: str
        :param order_by: (Optional) Field used to sort the returned traces.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of entries. If not
                           passed, the API will return the first page of
                           entries.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Traces that match the specified filter conditions.
        """
        if page_token is None:
            page_token = INITIAL_PAGE
        options = CallOptions(page_token=page_token)
        page_iter = self._gax_api.list_traces(
            project_id=project_id,
            view=view,
            page_size=page_size,
            start_time=start_time,
            end_time=end_time,
            filter_=filter_,
            order_by=order_by,
            options=options)
        item_to_value = _item_to_mapping
        return page_iterator._GAXIterator(
            self.client, page_iter, item_to_value)


def _parse_trace_pb(trace_pb):
    """Parse a ``Trace`` protobuf to a dictionary.

    :type trace_pb: :class:`google.cloud.proto.devtools.cloudtrace.v1.
                            trace_pb2.Trace`
    :param trace_pb: A trace protobuf instance.

    :rtype: dict
    :returns: The converted trace dict.
    """
    try:
        return MessageToDict(trace_pb)
    except TypeError:
        raise


def _item_to_mapping(iterator, trace_pb):
    """Helper callable function for the GAXIterator

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type trace_pb: :class:`google.cloud.proto.devtools.cloudtrace.v1.
                            trace_pb2.Trace`
    :param trace_pb: A trace protobuf instance.
    """
    mapping = _parse_trace_pb(trace_pb)
    return mapping


def make_gax_trace_api(client):
    """Create an instance of the GAX Trace API.

    :type client: :class:`~google.cloud.trace.client.Client`
    :param client: The client that holds configuration details.

    :rtype: :class:`~google.cloud.trace._gax._TraceAPI`
    :returns: A Trace API instance with the proper configurations.
    """
    channel = make_secure_channel(
        client._credentials,
        DEFAULT_USER_AGENT,
        trace_service_client.TraceServiceClient.SERVICE_ADDRESS)
    generated = trace_service_client.TraceServiceClient(
        channel=channel,
        lib_name='gccl')
    return _TraceAPI(generated, client)


def _traces_mapping_to_pb(traces_mapping):
    """Convert a trace dict to protobuf.

    :type traces_mapping: dict
    :param traces_mapping: A trace mapping.

    :rtype: class:`google.cloud.proto.devtools.cloudtrace.v1.trace_pb2.Traces`
    :returns: The converted protobuf type traces.
    """
    traces_pb = trace_pb2.Traces()
    ParseDict(traces_mapping, traces_pb)
    return traces_pb
