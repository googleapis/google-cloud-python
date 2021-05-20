# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.retail.v2",
    manifest={"PurgeMetadata", "PurgeUserEventsRequest", "PurgeUserEventsResponse",},
)


class PurgeMetadata(proto.Message):
    r"""Metadata related to the progress of the Purge operation.
    This will be returned by the
    google.longrunning.Operation.metadata field.
        """


class PurgeUserEventsRequest(proto.Message):
    r"""Request message for PurgeUserEvents method.
    Attributes:
        parent (str):
            Required. The resource name of the catalog
            under which the events are created. The format
            is
            "projects/${projectId}/locations/global/catalogs/${catalogId}".
        filter (str):
            Required. The filter string to specify the events to be
            deleted with a length limit of 5,000 characters. Empty
            string filter is not allowed. The eligible fields for
            filtering are:

            -  ``eventType``: Double quoted
               [UserEvent.event_type][google.cloud.retail.v2.UserEvent.event_type]
               string.
            -  ``eventTime``: in ISO 8601 "zulu" format.
            -  ``visitorId``: Double quoted string. Specifying this will
               delete all events associated with a visitor.
            -  ``userId``: Double quoted string. Specifying this will
               delete all events associated with a user.

            Examples:

            -  Deleting all events in a time range:
               ``eventTime > "2012-04-23T18:25:43.511Z" eventTime < "2012-04-23T18:30:43.511Z"``
            -  Deleting specific eventType in time range:
               ``eventTime > "2012-04-23T18:25:43.511Z" eventType = "detail-page-view"``
            -  Deleting all events for a specific visitor:
               ``visitorId = "visitor1024"``

            The filtering fields are assumed to have an implicit AND.
        force (bool):
            Actually perform the purge. If ``force`` is set to false,
            the method will return the expected purge count without
            deleting any user events.
    """

    parent = proto.Field(proto.STRING, number=1,)
    filter = proto.Field(proto.STRING, number=2,)
    force = proto.Field(proto.BOOL, number=3,)


class PurgeUserEventsResponse(proto.Message):
    r"""Response of the PurgeUserEventsRequest. If the long running
    operation is successfully done, then this message is returned by
    the google.longrunning.Operations.response field.

    Attributes:
        purged_events_count (int):
            The total count of events purged as a result
            of the operation.
    """

    purged_events_count = proto.Field(proto.INT64, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
