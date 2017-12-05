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
from google.cloud.trace_v1.gapic import trace_service_client
from google.cloud.trace_v1.proto import trace_pb2
from google.gax import CallOptions
from google.gax import INITIAL_PAGE
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import ParseDict


class _TraceAPI(object):
    """
    Wrapper to help mapping trace-related APIs.

    See
    https://cloud.google.com/trace/docs/reference/v1/rpc/google.devtools.
    cloudtrace.v1

    Args:
        gax_api (~google.cloud.trace_v1.gapic.trace_service_client.
            TraceServiceClient): Required. API object used to make GAX
            requests.

        client (~google.cloud.trace.client.Client): The client that owns this
            API object.
    """
    def __init__(self, gax_api, client):
        self._gax_api = gax_api
        self.client = client

    def patch_traces(self, project_id, traces, options=None):
        """
        Sends new traces to Stackdriver Trace or updates existing traces.

        Args:
            project_id (Optional[str]): ID of the Cloud project where the trace
                data is stored.

            traces (dict): Required. The traces to be patched in the API call.

            options (Optional[~google.gax.CallOptions]): Overrides the default
                settings for this call, e.g, timeout, retries etc.
        """
        traces_pb = _traces_mapping_to_pb(traces)
        self._gax_api.patch_traces(project_id, traces_pb, options)

    def get_trace(self, project_id, trace_id, options=None):
        """
        Gets a single trace by its ID.

        Args:
            trace_id (str): ID of the trace to return.

            project_id (str): Required. ID of the Cloud project where the trace
                data is stored.

            options (Optional[~google.gax.CallOptions]): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A Trace dict.
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
        """
        Returns of a list of traces that match the filter conditions.

        Args:
            project_id (Optional[str]): ID of the Cloud project where the trace
                data is stored.

            view (Optional[~google.cloud.trace_v1.gapic.enums.
                ListTracesRequest.ViewType]): Type of data returned for traces
                in the list. Default is ``MINIMAL``.

            page_size (Optional[int]): Maximum number of traces to return. If
                not specified or <= 0, the implementation selects a reasonable
                value. The implementation may return fewer traces than the
                requested page size.

            start_time (Optional[~datetime.datetime]): Start of the time
                interval (inclusive) during which the trace data was collected
                from the application.

            end_time (Optional[~datetime.datetime]): End of the time interval
                (inclusive) during which the trace data was collected from the
                application.

            filter_ (Optional[str]): An optional filter for the request.

            order_by (Optional[str]): Field used to sort the returned traces.

            page_token (Optional[str]): opaque marker for the next "page" of
                entries. If not passed, the API will return the first page of
                entries.

        Returns:
            A  :class:`~google.api_core.page_iterator.Iterator` of traces that
            match the specified filter conditions.
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
    """
    Parse a ``Trace`` protobuf to a dictionary.

    Args:
        trace_pb (~google.cloud.trace_v1.proto.trace_pb2.Trace): A trace
            protobuf instance.

    Returns:
        The converted trace dict.
    """
    try:
        return MessageToDict(trace_pb)
    except TypeError:
        raise


def _item_to_mapping(iterator, trace_pb):
    """
    Helper callable function for the GAXIterator

    Args:
        iterator(~google.api_core.page_iterator.Iterator): The iterator that is
            currently in use.

        trace_pb(~google.cloud.trace_v1.proto.trace_pb2.Trace): A trace
            protobuf instance.
    """
    mapping = _parse_trace_pb(trace_pb)
    return mapping


def make_gax_trace_api(client):
    """
    Create an instance of the GAX Trace API.

    Args:
        client (~google.cloud.trace.client.Client): The client that holds
            configuration details.

    Returns:
        A :class:`~google.cloud.trace._gax._TraceAPI` instance with the proper
        configurations.
    """
    generated = trace_service_client.TraceServiceClient()
    return _TraceAPI(generated, client)


def _traces_mapping_to_pb(traces_mapping):
    """
    Convert a trace dict to protobuf.

    Args:
        traces_mapping (dict): A trace mapping.

    Returns:
        The converted protobuf type traces.
    """
    traces_pb = trace_pb2.Traces()
    ParseDict(traces_mapping, traces_pb)
    return traces_pb
