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

"""Client for interacting with the Stackdriver Trace API."""

from google.cloud.trace.v1._gapic import make_trace_api
from google.cloud.client import ClientWithProject
from google.cloud._helpers import _datetime_to_pb_timestamp


class Client(ClientWithProject):
    """
    Client to bundle configuration needed for API requests.

    Args:
        project (str): Required. The project which the client acts on behalf
            of. If not passed, falls back to the default inferred
            from the environment.

        credentials (Optional[~google.auth.credentials.Credentials]):
            The OAuth2 Credentials to use for this client. If not
            passed, falls back to the default inferred from the
            environment.
    """

    SCOPE = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/trace.append",
    )
    """The scopes required for authenticating as a Trace consumer."""

    _trace_api = None

    def __init__(self, project=None, credentials=None):
        super(Client, self).__init__(project=project, credentials=credentials)

    @property
    def trace_api(self):
        """Helper for trace-related API calls.

        See
        https://cloud.google.com/trace/docs/reference/v1/rpc/google.devtools.
        cloudtrace.v1
        """
        self._trace_api = make_trace_api(self)
        return self._trace_api

    def patch_traces(self, traces, project_id=None):
        """Sends new traces to Stackdriver Trace or updates existing traces.

        Args:
            traces (dict): Required. The traces to be patched in the API call.

            project_id (Optional[str]): ID of the Cloud project where the trace
                data is stored.
        """
        if project_id is None:
            project_id = self.project

        self.trace_api.patch_traces(project_id=project_id, traces=traces)

    def get_trace(self, trace_id, project_id=None):
        """
        Gets a single trace by its ID.

        Args:
            trace_id (str): ID of the trace to return.

            project_id (str): Required. ID of the Cloud project where the trace
                data is stored.

        Returns:
            A Trace dict.
        """
        if project_id is None:
            project_id = self.project

        return self.trace_api.get_trace(project_id=project_id, trace_id=trace_id)

    def list_traces(
        self,
        project_id=None,
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
        if project_id is None:
            project_id = self.project

        if start_time is not None:
            start_time = _datetime_to_pb_timestamp(start_time)

        if end_time is not None:
            end_time = _datetime_to_pb_timestamp(end_time)

        return self.trace_api.list_traces(
            project_id=project_id,
            view=view,
            page_size=page_size,
            start_time=start_time,
            end_time=end_time,
            filter_=filter_,
            order_by=order_by,
            page_token=page_token,
        )
