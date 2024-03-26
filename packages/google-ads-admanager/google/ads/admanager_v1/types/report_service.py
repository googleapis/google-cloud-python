# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "Report",
        "ExportSavedReportRequest",
        "ExportSavedReportMetadata",
        "ExportSavedReportResponse",
    },
)


class Report(proto.Message):
    r"""The Report resource.

    Attributes:
        name (str):
            Identifier. The resource name of the Report. Report resource
            name have the form:
            ``networks/{network_code}/reports/{report_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ExportSavedReportRequest(proto.Message):
    r"""Request proto for the configuration of a report run.

    Attributes:
        report (str):
            The name of a particular saved report resource.

            A report will be run based on the specification of this
            saved report. It must have the format of
            "networks/{network_code}/reports/{report_id}".
        format_ (google.ads.admanager_v1.types.ExportSavedReportRequest.Format):
            Required. The export format requested.
        include_report_properties (bool):
            Whether or not to include the report
            properties (e.g. network, user, date
            generated...) in the generated report.
        include_ids (bool):
            Whether or not to include the IDs if there
            are any (e.g. advertiser ID,  order ID...)
            present in the report.
        include_totals_row (bool):
            Whether or not to include a row containing
            metric totals.
        file_name (str):
            The file name of report download. The file extension is
            determined by export_format and gzip_compressed.

            Defaults to "DFP Report" if not specified.
    """

    class Format(proto.Enum):
        r"""Supported file formats.

        Values:
            FORMAT_UNSPECIFIED (0):
                Default value. This value is unused.
            CSV_DUMP (2):
                Comma separated values meant to be used by
                automated machine processing.

                Unlike other formats, the output is not
                localized and there is no totals row by default.
            XLSX (5):
                The report file is generated as an Office
                Open XML spreadsheet designed for Excel 2007+.
            XML (6):
                The report is generated as XML.
        """
        FORMAT_UNSPECIFIED = 0
        CSV_DUMP = 2
        XLSX = 5
        XML = 6

    report: str = proto.Field(
        proto.STRING,
        number=1,
    )
    format_: Format = proto.Field(
        proto.ENUM,
        number=2,
        enum=Format,
    )
    include_report_properties: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    include_ids: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    include_totals_row: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    file_name: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ExportSavedReportMetadata(proto.Message):
    r"""The message stored in the
    google.longrunning.Operation.metadata field. Contains metadata
    regarding this execution.

    Attributes:
        result_id (int):
            The result generated in this report run.
    """

    result_id: int = proto.Field(
        proto.INT64,
        number=1,
    )


class ExportSavedReportResponse(proto.Message):
    r"""Message included in the longrunning Operation result.response
    field when the report completes successfully.

    Attributes:
        download_url (str):
            The link to the exported file.
    """

    download_url: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
