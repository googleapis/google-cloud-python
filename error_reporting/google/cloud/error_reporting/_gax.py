# Copyright 2016 Google LLC All Rights Reserved.
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

"""GAX wrapper for Error Reporting API requests."""

from google.cloud._helpers import make_secure_channel
from google.cloud._http import DEFAULT_USER_AGENT

from google.cloud.gapic.errorreporting.v1beta1 import (
    report_errors_service_client)
from google.cloud.proto.devtools.clouderrorreporting.v1beta1 import (
    report_errors_service_pb2)
from google.protobuf.json_format import ParseDict

from google.cloud.error_reporting import __version__


def make_report_error_api(client):
    """Create an instance of the GAX Logging API.

    :type client::class:`google.cloud.error_reporting.Client`
    :param client: Error Reporting client.

    :rtype: :class:_ErrorReportingGaxApi
    :returns: An Error Reporting API instance.
    """
    channel = make_secure_channel(
        client._credentials,
        DEFAULT_USER_AGENT,
        report_errors_service_client.ReportErrorsServiceClient.SERVICE_ADDRESS)
    gax_client = report_errors_service_client.ReportErrorsServiceClient(
        channel=channel, lib_name='gccl', lib_version=__version__)
    return _ErrorReportingGaxApi(gax_client, client.project)


class _ErrorReportingGaxApi(object):
    """Helper mapping Error Reporting-related APIs

    :type gax_api:
        :class:`v1beta1.report_errors_service_client.ReportErrorsServiceClient`
    :param gax_api: API object used to make GAX requests.

    :type project: str
    :param project: Google Cloud Project ID
    """

    def __init__(self, gax_api, project):
        self._gax_api = gax_api
        self._project = project

    def report_error_event(self, error_report):
        """Uses the GAX client to report the error.

        :type error_report: dict
        :param error_report:
            payload of the error report formatted according to
            https://cloud.google.com/error-reporting/docs/formatting-error-messages
            This object should be built using
            Use
            :meth:~`google.cloud.error_reporting.client._build_error_report`
        """
        project_name = self._gax_api.project_path(self._project)
        error_report_payload = report_errors_service_pb2.ReportedErrorEvent()
        ParseDict(error_report, error_report_payload)
        self._gax_api.report_error_event(project_name, error_report_payload)
