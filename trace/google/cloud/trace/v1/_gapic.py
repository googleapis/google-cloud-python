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

"""Wrapper for interacting with the Stackdriver Trace API."""

from google.api_core.gapic_v1 import client_info
from google.cloud.trace import __version__
from google.cloud.trace_v1.gapic import trace_service_client
from google.cloud.trace_v1.proto import trace_pb2
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import ParseDict


_CLIENT_INFO = client_info.ClientInfo(client_library_version=__version__)


class _TraceAPI(object):
    """
    Wrapper to help mapping trace-related APIs.

    See
    https://cloud.google.com/trace/docs/reference/v1/rpc/google.devtools.
    cloudtrace.v1

    Args:
        gapic_api (~google.cloud.trace_v1.gapic.trace_service_client.
            TraceServiceClient): Required. API object used to make RPCs.
        client (~google.cloud.trace.client.Client): The client that owns this
            API object.
    """

    def __init__(self, gapic_api, client):
        self._gapic_api = gapic_api
        self.client = client

    def patch_traces(self, project_id, traces):
        """
        Sends new traces to Stackdriver Trace or updates existing traces.

        Args:
            project_id (Optional[str]): ID of the Cloud project where the trace
                data is stored.
            traces (dict): Required. The traces to be patched in the API call.
        """
        traces_pb = _traces_mapping_to_pb(traces)
        self._gapic_api.patch_traces(project_id, traces_pb)

    def get_trace(self, project_id, trace_id):
        """
        Gets a single trace by its ID.

        Args:
            trace_id (str): ID of the trace to return.
            project_id (str): Required. ID of the Cloud project where the trace
                data is stored.

        Returns:
            A Trace dict.
        """
        trace_pb = self._gapic_api.get_trace(project_id, trace_id)
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
        page_token=None,
    ):
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
        page_iter = self._gapic_api.list_traces(
            project_id=project_id,
            view=view,
            page_size=page_size,
            start_time=start_time,
            end_time=end_time,
            filter_=filter_,
            order_by=order_by,
        )
        page_iter.item_to_value = _item_to_mapping
        page_iter.next_page_token = page_token
        return page_iter


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
    Helper callable function for the page iterator

    Args:
        iterator(~google.api_core.page_iterator.Iterator): The iterator that is
            currently in use.

        trace_pb(~google.cloud.trace_v1.proto.trace_pb2.Trace): A trace
            protobuf instance.
    """
    mapping = _parse_trace_pb(trace_pb)
    return mapping


def make_trace_api(client):
    """
    Create an instance of the gapic Trace API.

    Args:
        client (~google.cloud.trace.client.Client): The client that holds
            configuration details.

    Returns:
        A :class:`~google.cloud.trace._gapic._TraceAPI` instance with the
        proper configurations.
    """
    generated = trace_service_client.TraceServiceClient(
        credentials=client._credentials, client_info=_CLIENT_INFO
    )
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
