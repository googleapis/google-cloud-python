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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.managedidentities.v1", manifest={"Domain", "Trust",},
)


class Domain(proto.Message):
    r"""Represents a managed Microsoft Active Directory domain.
    Attributes:
        name (str):
            Required. The unique name of the domain using the form:
            ``projects/{project_id}/locations/global/domains/{domain_name}``.
        labels (Sequence[google.cloud.managedidentities_v1.types.Domain.LabelsEntry]):
            Optional. Resource labels that can contain
            user-provided metadata.
        authorized_networks (Sequence[str]):
            Optional. The full names of the Google Compute Engine
            `networks </compute/docs/networks-and-firewalls#networks>`__
            the domain instance is connected to. Networks can be added
            using UpdateDomain. The domain is only available on networks
            listed in ``authorized_networks``. If CIDR subnets overlap
            between networks, domain creation will fail.
        reserved_ip_range (str):
            Required. The CIDR range of internal addresses that are
            reserved for this domain. Reserved networks must be /24 or
            larger. Ranges must be unique and non-overlapping with
            existing subnets in [Domain].[authorized_networks].
        locations (Sequence[str]):
            Required. Locations where domain needs to be provisioned.
            [regions][compute/docs/regions-zones/] e.g. us-west1 or
            us-east4 Service supports up to 4 locations at once. Each
            location will use a /26 block.
        admin (str):
            Optional. The name of delegated administrator account used
            to perform Active Directory operations. If not specified,
            ``setupadmin`` will be used.
        fqdn (str):
            Output only. The fully-qualified domain name
            of the exposed domain used by clients to connect
            to the service. Similar to what would be chosen
            for an Active Directory set up on an internal
            network.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the instance was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last update time.
        state (google.cloud.managedidentities_v1.types.Domain.State):
            Output only. The current state of this
            domain.
        status_message (str):
            Output only. Additional information about the
            current status of this domain, if available.
        trusts (Sequence[google.cloud.managedidentities_v1.types.Trust]):
            Output only. The current trusts associated
            with the domain.
    """

    class State(proto.Enum):
        r"""Represents the different states of a managed domain."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
        UPDATING = 3
        DELETING = 4
        REPAIRING = 5
        PERFORMING_MAINTENANCE = 6
        UNAVAILABLE = 7

    name = proto.Field(proto.STRING, number=1,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=2,)
    authorized_networks = proto.RepeatedField(proto.STRING, number=3,)
    reserved_ip_range = proto.Field(proto.STRING, number=4,)
    locations = proto.RepeatedField(proto.STRING, number=5,)
    admin = proto.Field(proto.STRING, number=6,)
    fqdn = proto.Field(proto.STRING, number=10,)
    create_time = proto.Field(
        proto.MESSAGE, number=11, message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE, number=12, message=timestamp_pb2.Timestamp,
    )
    state = proto.Field(proto.ENUM, number=13, enum=State,)
    status_message = proto.Field(proto.STRING, number=14,)
    trusts = proto.RepeatedField(proto.MESSAGE, number=15, message="Trust",)


class Trust(proto.Message):
    r"""Represents a relationship between two domains. This allows a
    controller in one domain to authenticate a user in another
    domain.

    Attributes:
        target_domain_name (str):
            Required. The fully qualified target domain
            name which will be in trust with the current
            domain.
        trust_type (google.cloud.managedidentities_v1.types.Trust.TrustType):
            Required. The type of trust represented by
            the trust resource.
        trust_direction (google.cloud.managedidentities_v1.types.Trust.TrustDirection):
            Required. The trust direction, which decides
            if the current domain is trusted, trusting, or
            both.
        selective_authentication (bool):
            Optional. The trust authentication type,
            which decides whether the trusted side has
            forest/domain wide access or selective access to
            an approved set of resources.
        target_dns_ip_addresses (Sequence[str]):
            Required. The target DNS server IP addresses
            which can resolve the remote domain involved in
            the trust.
        trust_handshake_secret (str):
            Required. The trust secret used for the
            handshake with the target domain. This will not
            be stored.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the instance was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last update time.
        state (google.cloud.managedidentities_v1.types.Trust.State):
            Output only. The current state of the trust.
        state_description (str):
            Output only. Additional information about the
            current state of the trust, if available.
        last_trust_heartbeat_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last heartbeat time when the
            trust was known to be connected.
    """

    class State(proto.Enum):
        r"""Represents the different states of a domain trust."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        UPDATING = 2
        DELETING = 3
        CONNECTED = 4
        DISCONNECTED = 5

    class TrustType(proto.Enum):
        r"""Represents the different inter-forest trust types."""
        TRUST_TYPE_UNSPECIFIED = 0
        FOREST = 1
        EXTERNAL = 2

    class TrustDirection(proto.Enum):
        r"""Represents the direction of trust. See
        `System.DirectoryServices.ActiveDirectory.TrustDirection <https://docs.microsoft.com/en-us/dotnet/api/system.directoryservices.activedirectory.trustdirection?view=netframework-4.7.2>`__
        for more information.
        """
        TRUST_DIRECTION_UNSPECIFIED = 0
        INBOUND = 1
        OUTBOUND = 2
        BIDIRECTIONAL = 3

    target_domain_name = proto.Field(proto.STRING, number=1,)
    trust_type = proto.Field(proto.ENUM, number=2, enum=TrustType,)
    trust_direction = proto.Field(proto.ENUM, number=3, enum=TrustDirection,)
    selective_authentication = proto.Field(proto.BOOL, number=4,)
    target_dns_ip_addresses = proto.RepeatedField(proto.STRING, number=5,)
    trust_handshake_secret = proto.Field(proto.STRING, number=6,)
    create_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,)
    state = proto.Field(proto.ENUM, number=9, enum=State,)
    state_description = proto.Field(proto.STRING, number=11,)
    last_trust_heartbeat_time = proto.Field(
        proto.MESSAGE, number=12, message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
