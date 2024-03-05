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

from google.protobuf import field_mask_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.support_v2.types import case as gcs_case
from google.cloud.support_v2.types import escalation as gcs_escalation

__protobuf__ = proto.module(
    package="google.cloud.support.v2",
    manifest={
        "GetCaseRequest",
        "CreateCaseRequest",
        "ListCasesRequest",
        "ListCasesResponse",
        "SearchCasesRequest",
        "SearchCasesResponse",
        "EscalateCaseRequest",
        "UpdateCaseRequest",
        "CloseCaseRequest",
        "SearchCaseClassificationsRequest",
        "SearchCaseClassificationsResponse",
    },
)


class GetCaseRequest(proto.Message):
    r"""The request message for the GetCase endpoint.

    Attributes:
        name (str):
            Required. The fully qualified name of a case
            to be retrieved.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateCaseRequest(proto.Message):
    r"""The request message for the CreateCase endpoint.

    Attributes:
        parent (str):
            Required. The name of the Google Cloud
            Resource under which the case should be created.
        case (google.cloud.support_v2.types.Case):
            Required. The case to be created.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    case: gcs_case.Case = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcs_case.Case,
    )


class ListCasesRequest(proto.Message):
    r"""The request message for the ListCases endpoint.

    Attributes:
        parent (str):
            Required. The fully qualified name of parent
            resource to list cases under.
        filter (str):
            An expression written in filter language. If non-empty, the
            query returns the cases that match the filter. Else, the
            query doesn't filter the cases.

            Filter expressions use the following fields with the
            operators equals (``=``) and ``AND``:

            -  ``state``: The accepted values are ``OPEN`` or
               ``CLOSED``.
            -  ``priority``: The accepted values are ``P0``, ``P1``,
               ``P2``, ``P3``, or ``P4``. You can specify multiple
               values for priority using the ``OR`` operator. For
               example, ``priority=P1 OR priority=P2``.
            -  ``creator.email``: The email address of the case creator.

            Examples:

            -  ``state=CLOSED``
            -  ``state=OPEN AND creator.email="tester@example.com"``
            -  ``state=OPEN AND (priority=P0 OR priority=P1)``
        page_size (int):
            The maximum number of cases fetched with each
            request. Defaults to 10.
        page_token (str):
            A token identifying the page of results to
            return. If unspecified, the first page is
            retrieved.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=2,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=4,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListCasesResponse(proto.Message):
    r"""The response message for the ListCases endpoint.

    Attributes:
        cases (MutableSequence[google.cloud.support_v2.types.Case]):
            The list of cases associated with the Google
            Cloud Resource, after any filters have been
            applied.
        next_page_token (str):
            A token to retrieve the next page of results. This should be
            set in the ``page_token`` field of the subsequent
            ``ListCasesRequest`` message that is issued. If unspecified,
            there are no more results to retrieve.
    """

    @property
    def raw_page(self):
        return self

    cases: MutableSequence[gcs_case.Case] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcs_case.Case,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class SearchCasesRequest(proto.Message):
    r"""The request message for the SearchCases endpoint.

    Attributes:
        parent (str):
            The fully qualified name of parent resource
            to search cases under.
        query (str):
            An expression written in filter language.

            A query uses the following fields with the operators equals
            (``=``) and ``AND``:

            -  ``organization``: An organization name in the form
               ``organizations/<organization_id>``.
            -  ``project``: A project name in the form
               ``projects/<project_id>``.
            -  ``state``: The accepted values are ``OPEN`` or
               ``CLOSED``.
            -  ``priority``: The accepted values are ``P0``, ``P1``,
               ``P2``, ``P3``, or ``P4``. You can specify multiple
               values for priority using the ``OR`` operator. For
               example, ``priority=P1 OR priority=P2``.
            -  ``creator.email``: The email address of the case creator.
            -  ``billingAccount``: A billing account in the form
               ``billingAccounts/<billing_account_id>``

            You must specify either ``organization`` or ``project``.

            To search across ``displayName``, ``description``, and
            comments, use a global restriction with no keyword or
            operator. For example, ``"my search"``.

            To search only cases updated after a certain date, use
            ``update_time`` restricted with that particular date, time,
            and timezone in ISO datetime format. For example,
            ``update_time>"2020-01-01T00:00:00-05:00"``. ``update_time``
            only supports the greater than operator (``>``).

            Examples:

            -  ``organization="organizations/123456789"``
            -  ``project="projects/my-project-id"``
            -  ``project="projects/123456789"``
            -  ``billing_account="billingAccounts/123456-A0B0C0-CUZ789"``
            -  ``organization="organizations/123456789" AND state=CLOSED``
            -  ``project="projects/my-project-id" AND creator.email="tester@example.com"``
            -  ``project="projects/my-project-id" AND (priority=P0 OR priority=P1)``
        page_size (int):
            The maximum number of cases fetched with each
            request. The default page size is 10.
        page_token (str):
            A token identifying the page of results to
            return. If unspecified, the first page is
            retrieved.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=4,
    )
    query: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class SearchCasesResponse(proto.Message):
    r"""The response message for the SearchCases endpoint.

    Attributes:
        cases (MutableSequence[google.cloud.support_v2.types.Case]):
            The list of cases associated with the Google
            Cloud Resource, after any filters have been
            applied.
        next_page_token (str):
            A token to retrieve the next page of results. This should be
            set in the ``page_token`` field of subsequent
            ``SearchCaseRequest`` message that is issued. If
            unspecified, there are no more results to retrieve.
    """

    @property
    def raw_page(self):
        return self

    cases: MutableSequence[gcs_case.Case] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcs_case.Case,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class EscalateCaseRequest(proto.Message):
    r"""The request message for the EscalateCase endpoint.

    Attributes:
        name (str):
            Required. The fully qualified name of the
            Case resource to be escalated.
        escalation (google.cloud.support_v2.types.Escalation):
            The escalation object to be sent with the
            escalation request.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    escalation: gcs_escalation.Escalation = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcs_escalation.Escalation,
    )


class UpdateCaseRequest(proto.Message):
    r"""The request message for the UpdateCase endpoint

    Attributes:
        case (google.cloud.support_v2.types.Case):
            Required. The case object to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            A list of attributes of the case object that should be
            updated as part of this request. Supported values are
            ``priority``, ``display_name``, and
            ``subscriber_email_addresses``. If no fields are specified,
            all supported fields are updated.

            WARNING: If you do not provide a field mask, then you might
            accidentally clear some fields. For example, if you leave
            the field mask empty and do not provide a value for
            ``subscriber_email_addresses``, then
            ``subscriber_email_addresses`` is updated to empty.
    """

    case: gcs_case.Case = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcs_case.Case,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class CloseCaseRequest(proto.Message):
    r"""The request message for the CloseCase endpoint.

    Attributes:
        name (str):
            Required. The fully qualified name of the
            case resource to be closed.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class SearchCaseClassificationsRequest(proto.Message):
    r"""The request message for SearchCaseClassifications endpoint.

    Attributes:
        query (str):
            An expression written in the Google Cloud
            filter language. If non-empty, then only cases
            whose fields match the filter are returned. If
            empty, then no messages are filtered out.
        page_size (int):
            The maximum number of cases fetched with each
            request.
        page_token (str):
            A token identifying the page of results to
            return. If unspecified, the first page is
            retrieved.
    """

    query: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class SearchCaseClassificationsResponse(proto.Message):
    r"""The response message for SearchCaseClassifications endpoint.

    Attributes:
        case_classifications (MutableSequence[google.cloud.support_v2.types.CaseClassification]):
            The classifications retrieved.
        next_page_token (str):
            A token to retrieve the next page of results. This should be
            set in the ``page_token`` field of subsequent
            ``SearchCaseClassificationsRequest`` message that is issued.
            If unspecified, there are no more results to retrieve.
    """

    @property
    def raw_page(self):
        return self

    case_classifications: MutableSequence[
        gcs_case.CaseClassification
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcs_case.CaseClassification,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
