# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.kms.v1",
    manifest={
        "ListEkmConnectionsRequest",
        "ListEkmConnectionsResponse",
        "GetEkmConnectionRequest",
        "CreateEkmConnectionRequest",
        "UpdateEkmConnectionRequest",
        "Certificate",
        "EkmConnection",
    },
)


class ListEkmConnectionsRequest(proto.Message):
    r"""Request message for [KeyManagementService.ListEkmConnections][].

    Attributes:
        parent (str):
            Required. The resource name of the location associated with
            the [EkmConnections][google.cloud.kms.v1.EkmConnection] to
            list, in the format ``projects/*/locations/*``.
        page_size (int):
            Optional. Optional limit on the number of
            [EkmConnections][google.cloud.kms.v1.EkmConnection] to
            include in the response. Further
            [EkmConnections][google.cloud.kms.v1.EkmConnection] can
            subsequently be obtained by including the
            [ListEkmConnectionsResponse.next_page_token][google.cloud.kms.v1.ListEkmConnectionsResponse.next_page_token]
            in a subsequent request. If unspecified, the server will
            pick an appropriate default.
        page_token (str):
            Optional. Optional pagination token, returned earlier via
            [ListEkmConnectionsResponse.next_page_token][google.cloud.kms.v1.ListEkmConnectionsResponse.next_page_token].
        filter (str):
            Optional. Only include resources that match the filter in
            the response. For more information, see `Sorting and
            filtering list
            results <https://cloud.google.com/kms/docs/sorting-and-filtering>`__.
        order_by (str):
            Optional. Specify how the results should be sorted. If not
            specified, the results will be sorted in the default order.
            For more information, see `Sorting and filtering list
            results <https://cloud.google.com/kms/docs/sorting-and-filtering>`__.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListEkmConnectionsResponse(proto.Message):
    r"""Response message for [KeyManagementService.ListEkmConnections][].

    Attributes:
        ekm_connections (Sequence[google.cloud.kms_v1.types.EkmConnection]):
            The list of
            [EkmConnections][google.cloud.kms.v1.EkmConnection].
        next_page_token (str):
            A token to retrieve next page of results. Pass this value in
            [ListEkmConnectionsRequest.page_token][google.cloud.kms.v1.ListEkmConnectionsRequest.page_token]
            to retrieve the next page of results.
        total_size (int):
            The total number of
            [EkmConnections][google.cloud.kms.v1.EkmConnection] that
            matched the query.
    """

    @property
    def raw_page(self):
        return self

    ekm_connections = proto.RepeatedField(
        proto.MESSAGE, number=1, message="EkmConnection",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    total_size = proto.Field(proto.INT32, number=3,)


class GetEkmConnectionRequest(proto.Message):
    r"""Request message for [KeyManagementService.GetEkmConnection][].

    Attributes:
        name (str):
            Required. The [name][google.cloud.kms.v1.EkmConnection.name]
            of the [EkmConnection][google.cloud.kms.v1.EkmConnection] to
            get.
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateEkmConnectionRequest(proto.Message):
    r"""Request message for [KeyManagementService.CreateEkmConnection][].

    Attributes:
        parent (str):
            Required. The resource name of the location associated with
            the [EkmConnection][google.cloud.kms.v1.EkmConnection], in
            the format ``projects/*/locations/*``.
        ekm_connection_id (str):
            Required. It must be unique within a location and match the
            regular expression ``[a-zA-Z0-9_-]{1,63}``.
        ekm_connection (google.cloud.kms_v1.types.EkmConnection):
            Required. An
            [EkmConnection][google.cloud.kms.v1.EkmConnection] with
            initial field values.
    """

    parent = proto.Field(proto.STRING, number=1,)
    ekm_connection_id = proto.Field(proto.STRING, number=2,)
    ekm_connection = proto.Field(proto.MESSAGE, number=3, message="EkmConnection",)


class UpdateEkmConnectionRequest(proto.Message):
    r"""Request message for [KeyManagementService.UpdateEkmConnection][].

    Attributes:
        ekm_connection (google.cloud.kms_v1.types.EkmConnection):
            Required. [EkmConnection][google.cloud.kms.v1.EkmConnection]
            with updated values.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. List of fields to be updated in
            this request.
    """

    ekm_connection = proto.Field(proto.MESSAGE, number=1, message="EkmConnection",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class Certificate(proto.Message):
    r"""A [Certificate][google.cloud.kms.v1.Certificate] represents an X.509
    certificate used to authenticate HTTPS connections to EKM replicas.

    Attributes:
        raw_der (bytes):
            Required. The raw certificate bytes in DER
            format.
        parsed (bool):
            Output only. True if the certificate was
            parsed successfully.
        issuer (str):
            Output only. The issuer distinguished name in RFC 2253
            format. Only present if
            [parsed][google.cloud.kms.v1.Certificate.parsed] is true.
        subject (str):
            Output only. The subject distinguished name in RFC 2253
            format. Only present if
            [parsed][google.cloud.kms.v1.Certificate.parsed] is true.
        subject_alternative_dns_names (Sequence[str]):
            Output only. The subject Alternative DNS names. Only present
            if [parsed][google.cloud.kms.v1.Certificate.parsed] is true.
        not_before_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The certificate is not valid before this time.
            Only present if
            [parsed][google.cloud.kms.v1.Certificate.parsed] is true.
        not_after_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The certificate is not valid after this time.
            Only present if
            [parsed][google.cloud.kms.v1.Certificate.parsed] is true.
        serial_number (str):
            Output only. The certificate serial number as a hex string.
            Only present if
            [parsed][google.cloud.kms.v1.Certificate.parsed] is true.
        sha256_fingerprint (str):
            Output only. The SHA-256 certificate fingerprint as a hex
            string. Only present if
            [parsed][google.cloud.kms.v1.Certificate.parsed] is true.
    """

    raw_der = proto.Field(proto.BYTES, number=1,)
    parsed = proto.Field(proto.BOOL, number=2,)
    issuer = proto.Field(proto.STRING, number=3,)
    subject = proto.Field(proto.STRING, number=4,)
    subject_alternative_dns_names = proto.RepeatedField(proto.STRING, number=5,)
    not_before_time = proto.Field(
        proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,
    )
    not_after_time = proto.Field(
        proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,
    )
    serial_number = proto.Field(proto.STRING, number=8,)
    sha256_fingerprint = proto.Field(proto.STRING, number=9,)


class EkmConnection(proto.Message):
    r"""An [EkmConnection][google.cloud.kms.v1.EkmConnection] represents an
    individual EKM connection. It can be used for creating
    [CryptoKeys][google.cloud.kms.v1.CryptoKey] and
    [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion] with a
    [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel] of
    [EXTERNAL_VPC][CryptoKeyVersion.ProtectionLevel.EXTERNAL_VPC], as
    well as performing cryptographic operations using keys created
    within the [EkmConnection][google.cloud.kms.v1.EkmConnection].

    Attributes:
        name (str):
            Output only. The resource name for the
            [EkmConnection][google.cloud.kms.v1.EkmConnection] in the
            format ``projects/*/locations/*/ekmConnections/*``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the
            [EkmConnection][google.cloud.kms.v1.EkmConnection] was
            created.
        service_resolvers (Sequence[google.cloud.kms_v1.types.EkmConnection.ServiceResolver]):
            A list of
            [ServiceResolvers][google.cloud.kms.v1.EkmConnection.ServiceResolver]
            where the EKM can be reached. There should be one
            ServiceResolver per EKM replica. Currently, only a single
            [ServiceResolver][google.cloud.kms.v1.EkmConnection.ServiceResolver]
            is supported.
        etag (str):
            This checksum is computed by the server based
            on the value of other fields, and may be sent on
            update requests to ensure the client has an
            up-to-date value before proceeding.
    """

    class ServiceResolver(proto.Message):
        r"""A
        [ServiceResolver][google.cloud.kms.v1.EkmConnection.ServiceResolver]
        represents an EKM replica that can be reached within an
        [EkmConnection][google.cloud.kms.v1.EkmConnection].

        Attributes:
            service_directory_service (str):
                Required. The resource name of the Service Directory service
                pointing to an EKM replica, in the format
                ``projects/*/locations/*/namespaces/*/services/*``.
            endpoint_filter (str):
                Optional. The filter applied to the endpoints
                of the resolved service. If no filter is
                specified, all endpoints will be considered. An
                endpoint will be chosen arbitrarily from the
                filtered list for each request.
                For endpoint filter syntax and examples, see
                https://cloud.google.com/service-directory/docs/reference/rpc/google.cloud.servicedirectory.v1#resolveservicerequest.
            hostname (str):
                Required. The hostname of the EKM replica
                used at TLS and HTTP layers.
            server_certificates (Sequence[google.cloud.kms_v1.types.Certificate]):
                Required. A list of leaf server certificates
                used to authenticate HTTPS connections to the
                EKM replica.
        """

        service_directory_service = proto.Field(proto.STRING, number=1,)
        endpoint_filter = proto.Field(proto.STRING, number=2,)
        hostname = proto.Field(proto.STRING, number=3,)
        server_certificates = proto.RepeatedField(
            proto.MESSAGE, number=4, message="Certificate",
        )

    name = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    service_resolvers = proto.RepeatedField(
        proto.MESSAGE, number=3, message=ServiceResolver,
    )
    etag = proto.Field(proto.STRING, number=5,)


__all__ = tuple(sorted(__protobuf__.manifest))
