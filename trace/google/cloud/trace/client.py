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

"""Client for interacting with the Stackdriver Trace API."""

from google.cloud.trace._gax import make_gax_trace_api
from google.cloud.trace.trace import Trace
from google.cloud.client import ClientWithProject
from google.protobuf.timestamp_pb2 import Timestamp

from datetime import datetime
import math

_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


class Client(ClientWithProject):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: The project which the client acts on behalf of.
                    If not passed, falls back to the default inferred from
                    the environment.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed, falls back to the default
                        inferred from the environment.
    """
    _trace_api = None

    def __init__(self, project=None, credentials=None):
        super(Client, self).__init__(
            project=project, credentials=credentials)

    @property
    def trace_api(self):
        """Helper for trace-related API calls.

        See
        https://cloud.google.com/trace/docs/reference/v1/rpc/google.devtools.
        cloudtrace.v1
        """
        self._trace_api = make_gax_trace_api(self)
        return self._trace_api

    def trace(self, project_id=None, trace_id=None):
        """Initialize a new trace instance.

        :type project_id: str
        :param project_id: ID of the Cloud project where the trace data
                           is stored.

        :type trace_id: str
        :param trace_id: ID of the trace. 32 digits uuid.

        :rtype: :class:`~google.cloud.trace.trace.Trace`
        :return: A Trace instance.
        """
        if project_id is None:
            project_id = self.project
        return Trace(client=self, project_id=project_id, trace_id=trace_id)

    def patch_traces(self, traces, project_id=None, options=None):
        """Sends new traces to Stackdriver Trace or updates existing traces.

        :type traces: dict
        :param traces: The traces to be patched in the API call.

        :type project_id: str
        :param project_id: (Optional) ID of the Cloud project where the trace
                           data is stored.

        :type options: :class:`~google.gax.CallOptions`
        :param options: (Optional) Overrides the default settings for this
                        call, e.g, timeout, retries etc.
        """
        if project_id is None:
            project_id = self.project

        return self.trace_api.patch_traces(
            project_id=project_id,
            traces=traces,
            options=options)

    def get_trace(self, trace_id, project_id=None, options=None):
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
        if project_id is None:
            project_id = self.project

        return self.trace_api.get_trace(
            project_id=project_id,
            trace_id=trace_id,
            options=options)

    def list_traces(
            self,
            project_id=None,
            view=None,
            page_size=None,
            start_time=None,
            end_time=None,
            filter_=None,
            order_by=None,
            options=None):
        """Returns of a list of traces that match the filter conditions.

        :type project_id: str
        :param project_id: (Optional) ID of the Cloud project where the trace
                           data is stored.

        :type view: :class:`google.cloud.gapic.trace.v1.enums.
                            ListTracesRequest.ViewType`
        :param view: (Optional) Type of data returned for traces in the list.
                     Default is ``MINIMAL``.

        :type page_size: int
        :param page_size: (Optional) Maximum number of traces to return.
                          If not specified or <= 0, the implementation selects
                          a reasonable value. The implementation may return
                          fewer traces than the requested page size.

        :type start_time: :class:`~datetime.datetime`
        :param start_time: (Optional) Start of the time interval (inclusive)
                           during which the trace data was collected from the
                           application.

        :type end_time: :class:`~datetime.datetime`
        :param end_time: (Optional) End of the time interval (inclusive) during
                         which the trace data was collected from the
                         application.

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
        if project_id is None:
            project_id = self.project

        if start_time is not None:
            start_time = _datetime_to_timestamp_protobuf(start_time)

        if end_time is not None:
            end_time = _datetime_to_timestamp_protobuf(end_time)

        return self.trace_api.list_traces(
            project_id=project_id,
            view=view,
            page_size=page_size,
            start_time=start_time,
            end_time=end_time,
            filter_=filter_,
            order_by=order_by,
            options=options)


def _datetime_to_timestamp_protobuf(datetime_str):
    """Helper to convert datetime to Timestamp protobuf.

    :type datetime_str: str
    :param datetime: Datetime string to be converted.
                     Format required: %Y-%m-%dT%H:%M:%S.%f
                     Use datetime.isoformat() to convert to this format.
                     e.g. datetime.now().isoformat()

    :rtype: :class:`~google.protobuf.timestamp_pb2.Timestamp`
    :returns: A Timestamp protobuf instance.
    """
    try:
        datetime_parsed = datetime.strptime(datetime_str, _DATETIME_FORMAT)
    except ValueError:
        return 'Time data {} does not match the format {}.'\
            .format(datetime_str, _DATETIME_FORMAT)

    timestamp = datetime_parsed.timestamp()
    parts = divmod(timestamp, 1)
    seconds = int(parts[0])
    nanos = round(parts[1] * math.pow(10, 9))

    timestamp_pb = Timestamp()
    timestamp_pb.seconds = seconds
    timestamp_pb.nanos = nanos

    return timestamp_pb
