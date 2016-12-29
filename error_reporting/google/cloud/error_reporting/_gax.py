# Copyright 2016 Google Inc. All Rights Reserved.
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

from google.cloud.gapic.errorreporting.v1beta1 import report_errors_service_api
from google.devtools.clouderrorreporting.v1beta1 import report_errors_service_pb2
from google.protobuf.json_format import ParseDict


def make_report_error_api(project):
    """Create an instance of the GAX Logging API."""
    api = report_errors_service_api.ReportErrorsServiceApi()
    return _ErrorReportingGaxApi(api, project)


class _ErrorReportingGaxApi(object):
    """Helper mapping Error Reporting-related APIs

    :type gax_api:
        :class:`google.cloud.gapic.errorreporting.v1beta1
        .report_errors_service_api.report_errors_service_api`
    :param gax_api: API object used to make GAX requests.
    """
    def __init__(self, gax_api, project):
        self._gax_api = gax_api
        self._project = project

    def report_error_event(self, error_report):
        """Uses the GAX client to report the error.

        :type project: str
        :param: project: Project ID to report the error to

        :type error: dict:
        :param: error: dict payload of the error report formatted
                       according to
                       https://cloud.google.com/error-reporting/docs/formatting-error-messages
                       This object should be built using
                       Use :meth:~`google.cloud.error_reporting.client._build_error_report`
        """
        project_name = self._gax_api.project_path(self._project)
        error_report_payload = report_errors_service_pb2.ReportedErrorEvent()
        ParseDict(error_report, error_report_payload)
        self._gax_api.report_error_event(project_name, error_report_payload)
