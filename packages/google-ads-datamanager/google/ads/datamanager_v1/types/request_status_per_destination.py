# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

from google.ads.datamanager_v1.types import destination as gad_destination
from google.ads.datamanager_v1.types import match_rate, processing_errors

__protobuf__ = proto.module(
    package="google.ads.datamanager.v1",
    manifest={
        "RequestStatusPerDestination",
    },
)


class RequestStatusPerDestination(proto.Message):
    r"""A request status per destination.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        destination (google.ads.datamanager_v1.types.Destination):
            A destination within a DM API request.
        request_status (google.ads.datamanager_v1.types.RequestStatusPerDestination.RequestStatus):
            The request status of the destination.
        error_info (google.ads.datamanager_v1.types.ErrorInfo):
            An error info error containing the error
            reason and error counts related to the upload.
        warning_info (google.ads.datamanager_v1.types.WarningInfo):
            A warning info containing the warning reason
            and warning counts related to the upload.
        audience_members_ingestion_status (google.ads.datamanager_v1.types.RequestStatusPerDestination.IngestAudienceMembersStatus):
            The status of the ingest audience members
            request.

            This field is a member of `oneof`_ ``status``.
        events_ingestion_status (google.ads.datamanager_v1.types.RequestStatusPerDestination.IngestEventsStatus):
            The status of the ingest events request.

            This field is a member of `oneof`_ ``status``.
        audience_members_removal_status (google.ads.datamanager_v1.types.RequestStatusPerDestination.RemoveAudienceMembersStatus):
            The status of the remove audience members
            request.

            This field is a member of `oneof`_ ``status``.
    """

    class RequestStatus(proto.Enum):
        r"""The request status.

        Values:
            REQUEST_STATUS_UNKNOWN (0):
                The request status is unknown.
            SUCCESS (1):
                The request succeeded.
            PROCESSING (2):
                The request is processing.
            FAILED (3):
                The request failed.
            PARTIAL_SUCCESS (4):
                The request partially succeeded.
        """

        REQUEST_STATUS_UNKNOWN = 0
        SUCCESS = 1
        PROCESSING = 2
        FAILED = 3
        PARTIAL_SUCCESS = 4

    class IngestAudienceMembersStatus(proto.Message):
        r"""The status of the ingest audience members request.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            user_data_ingestion_status (google.ads.datamanager_v1.types.RequestStatusPerDestination.IngestUserDataStatus):
                The status of the user data ingestion to the
                destination.

                This field is a member of `oneof`_ ``status``.
            mobile_data_ingestion_status (google.ads.datamanager_v1.types.RequestStatusPerDestination.IngestMobileDataStatus):
                The status of the mobile data ingestion to
                the destination.

                This field is a member of `oneof`_ ``status``.
            pair_data_ingestion_status (google.ads.datamanager_v1.types.RequestStatusPerDestination.IngestPairDataStatus):
                The status of the pair data ingestion to the
                destination.

                This field is a member of `oneof`_ ``status``.
        """

        user_data_ingestion_status: "RequestStatusPerDestination.IngestUserDataStatus" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="status",
            message="RequestStatusPerDestination.IngestUserDataStatus",
        )
        mobile_data_ingestion_status: "RequestStatusPerDestination.IngestMobileDataStatus" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="status",
            message="RequestStatusPerDestination.IngestMobileDataStatus",
        )
        pair_data_ingestion_status: "RequestStatusPerDestination.IngestPairDataStatus" = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="status",
            message="RequestStatusPerDestination.IngestPairDataStatus",
        )

    class RemoveAudienceMembersStatus(proto.Message):
        r"""The status of the remove audience members request.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            user_data_removal_status (google.ads.datamanager_v1.types.RequestStatusPerDestination.RemoveUserDataStatus):
                The status of the user data removal from the
                destination.

                This field is a member of `oneof`_ ``status``.
            mobile_data_removal_status (google.ads.datamanager_v1.types.RequestStatusPerDestination.RemoveMobileDataStatus):
                The status of the mobile data removal from
                the destination.

                This field is a member of `oneof`_ ``status``.
            pair_data_removal_status (google.ads.datamanager_v1.types.RequestStatusPerDestination.RemovePairDataStatus):
                The status of the pair data removal from the
                destination.

                This field is a member of `oneof`_ ``status``.
        """

        user_data_removal_status: "RequestStatusPerDestination.RemoveUserDataStatus" = (
            proto.Field(
                proto.MESSAGE,
                number=1,
                oneof="status",
                message="RequestStatusPerDestination.RemoveUserDataStatus",
            )
        )
        mobile_data_removal_status: "RequestStatusPerDestination.RemoveMobileDataStatus" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="status",
            message="RequestStatusPerDestination.RemoveMobileDataStatus",
        )
        pair_data_removal_status: "RequestStatusPerDestination.RemovePairDataStatus" = (
            proto.Field(
                proto.MESSAGE,
                number=3,
                oneof="status",
                message="RequestStatusPerDestination.RemovePairDataStatus",
            )
        )

    class IngestEventsStatus(proto.Message):
        r"""The status of the events ingestion to the destination.

        Attributes:
            record_count (int):
                The total count of events sent in the upload
                request. Includes all events in the request,
                regardless of whether they were successfully
                ingested or not.
        """

        record_count: int = proto.Field(
            proto.INT64,
            number=1,
        )

    class IngestUserDataStatus(proto.Message):
        r"""The status of the user data ingestion to the destination
        containing stats related to the ingestion.

        Attributes:
            record_count (int):
                The total count of audience members sent in
                the upload request for the destination. Includes
                all audience members in the request, regardless
                of whether they were successfully ingested or
                not.
            user_identifier_count (int):
                The total count of user identifiers sent in
                the upload request for the destination. Includes
                all user identifiers in the request, regardless
                of whether they were successfully ingested or
                not.
            upload_match_rate_range (google.ads.datamanager_v1.types.MatchRateRange):
                The match rate range of the upload.
        """

        record_count: int = proto.Field(
            proto.INT64,
            number=1,
        )
        user_identifier_count: int = proto.Field(
            proto.INT64,
            number=2,
        )
        upload_match_rate_range: match_rate.MatchRateRange = proto.Field(
            proto.ENUM,
            number=3,
            enum=match_rate.MatchRateRange,
        )

    class RemoveUserDataStatus(proto.Message):
        r"""The status of the user data removal from the destination.

        Attributes:
            record_count (int):
                The total count of audience members sent in
                the removal request. Includes all audience
                members in the request, regardless of whether
                they were successfully removed or not.
            user_identifier_count (int):
                The total count of user identifiers sent in
                the removal request. Includes all user
                identifiers in the request, regardless of
                whether they were successfully removed or not.
        """

        record_count: int = proto.Field(
            proto.INT64,
            number=1,
        )
        user_identifier_count: int = proto.Field(
            proto.INT64,
            number=2,
        )

    class IngestMobileDataStatus(proto.Message):
        r"""The status of the mobile data ingestion to the destination
        containing stats related to the ingestion.

        Attributes:
            record_count (int):
                The total count of audience members sent in
                the upload request for the destination. Includes
                all audience members in the request, regardless
                of whether they were successfully ingested or
                not.
            mobile_id_count (int):
                The total count of mobile ids sent in the
                upload request for the destination. Includes all
                mobile ids in the request, regardless of whether
                they were successfully ingested or not.
        """

        record_count: int = proto.Field(
            proto.INT64,
            number=1,
        )
        mobile_id_count: int = proto.Field(
            proto.INT64,
            number=2,
        )

    class RemoveMobileDataStatus(proto.Message):
        r"""The status of the mobile data removal from the destination.

        Attributes:
            record_count (int):
                The total count of audience members sent in
                the removal request. Includes all audience
                members in the request, regardless of whether
                they were successfully removed or not.
            mobile_id_count (int):
                The total count of mobile Ids sent in the
                removal request. Includes all mobile ids in the
                request, regardless of whether they were
                successfully removed or not.
        """

        record_count: int = proto.Field(
            proto.INT64,
            number=1,
        )
        mobile_id_count: int = proto.Field(
            proto.INT64,
            number=2,
        )

    class IngestPairDataStatus(proto.Message):
        r"""The status of the pair data ingestion to the destination
        containing stats related to the ingestion.

        Attributes:
            record_count (int):
                The total count of audience members sent in
                the upload request for the destination. Includes
                all audience members in the request, regardless
                of whether they were successfully ingested or
                not.
            pair_id_count (int):
                The total count of pair ids sent in the
                upload request for the destination. Includes all
                pair ids in the request, regardless of whether
                they were successfully ingested or not.
        """

        record_count: int = proto.Field(
            proto.INT64,
            number=1,
        )
        pair_id_count: int = proto.Field(
            proto.INT64,
            number=2,
        )

    class RemovePairDataStatus(proto.Message):
        r"""The status of the pair data removal from the destination.

        Attributes:
            record_count (int):
                The total count of audience members sent in
                the removal request. Includes all audience
                members in the request, regardless of whether
                they were successfully removed or not.
            pair_id_count (int):
                The total count of pair ids sent in the
                removal request. Includes all pair ids in the
                request, regardless of whether they were
                successfully removed or not.
        """

        record_count: int = proto.Field(
            proto.INT64,
            number=1,
        )
        pair_id_count: int = proto.Field(
            proto.INT64,
            number=2,
        )

    destination: gad_destination.Destination = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gad_destination.Destination,
    )
    request_status: RequestStatus = proto.Field(
        proto.ENUM,
        number=2,
        enum=RequestStatus,
    )
    error_info: processing_errors.ErrorInfo = proto.Field(
        proto.MESSAGE,
        number=3,
        message=processing_errors.ErrorInfo,
    )
    warning_info: processing_errors.WarningInfo = proto.Field(
        proto.MESSAGE,
        number=7,
        message=processing_errors.WarningInfo,
    )
    audience_members_ingestion_status: IngestAudienceMembersStatus = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="status",
        message=IngestAudienceMembersStatus,
    )
    events_ingestion_status: IngestEventsStatus = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="status",
        message=IngestEventsStatus,
    )
    audience_members_removal_status: RemoveAudienceMembersStatus = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="status",
        message=RemoveAudienceMembersStatus,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
