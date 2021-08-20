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

from google.cloud.gkehub_v1 import configmanagement_v1  # type: ignore
from google.cloud.gkehub_v1 import multiclusteringress_v1  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.gkehub.v1",
    manifest={
        "Feature",
        "FeatureResourceState",
        "FeatureState",
        "CommonFeatureSpec",
        "CommonFeatureState",
        "MembershipFeatureSpec",
        "MembershipFeatureState",
    },
)


class Feature(proto.Message):
    r"""Feature represents the settings and status of any Hub
    Feature.

    Attributes:
        name (str):
            Output only. The full, unique name of this Feature resource
            in the format ``projects/*/locations/*/features/*``.
        labels (Sequence[google.cloud.gkehub_v1.types.Feature.LabelsEntry]):
            GCP labels for this Feature.
        resource_state (google.cloud.gkehub_v1.types.FeatureResourceState):
            Output only. State of the Feature resource
            itself.
        spec (google.cloud.gkehub_v1.types.CommonFeatureSpec):
            Optional. Hub-wide Feature configuration. If
            this Feature does not support any Hub-wide
            configuration, this field may be unused.
        membership_specs (Sequence[google.cloud.gkehub_v1.types.Feature.MembershipSpecsEntry]):
            Optional. Membership-specific configuration
            for this Feature. If this Feature does not
            support any per-Membership configuration, this
            field may be unused.
            The keys indicate which Membership the
            configuration is for, in the form:
            `projects/{p}/locations/{l}/memberships/{m}`
            Where {p} is the project, {l} is a valid
            location and {m} is a valid Membership in this
            project at that location. {p} WILL match the
            Feature's project.

            {p} will always be returned as the project
            number, but the project ID is also accepted
            during input. If the same Membership is
            specified in the map twice (using the project ID
            form, and the project number form), exactly ONE
            of the entries will be saved, with no guarantees
            as to which. For this reason, it is recommended
            the same format be used for all entries when
            mutating a Feature.
        state (google.cloud.gkehub_v1.types.CommonFeatureState):
            Output only. The Hub-wide Feature state.
        membership_states (Sequence[google.cloud.gkehub_v1.types.Feature.MembershipStatesEntry]):
            Output only. Membership-specific Feature
            status. If this Feature does report any per-
            Membership status, this field may be unused.
            The keys indicate which Membership the state is
            for, in the form:
            `projects/{p}/locations/{l}/memberships/{m}`
            Where {p} is the project number, {l} is a valid
            location and {m} is a valid Membership in this
            project at that location. {p} MUST match the
            Feature's project number.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. When the Feature resource was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. When the Feature resource was
            last updated.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. When the Feature resource was
            deleted.
    """

    name = proto.Field(proto.STRING, number=1,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=2,)
    resource_state = proto.Field(
        proto.MESSAGE, number=3, message="FeatureResourceState",
    )
    spec = proto.Field(proto.MESSAGE, number=4, message="CommonFeatureSpec",)
    membership_specs = proto.MapField(
        proto.STRING, proto.MESSAGE, number=5, message="MembershipFeatureSpec",
    )
    state = proto.Field(proto.MESSAGE, number=6, message="CommonFeatureState",)
    membership_states = proto.MapField(
        proto.STRING, proto.MESSAGE, number=7, message="MembershipFeatureState",
    )
    create_time = proto.Field(proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=9, message=timestamp_pb2.Timestamp,)
    delete_time = proto.Field(
        proto.MESSAGE, number=10, message=timestamp_pb2.Timestamp,
    )


class FeatureResourceState(proto.Message):
    r"""FeatureResourceState describes the state of a Feature *resource* in
    the GkeHub API. See ``FeatureState`` for the "running state" of the
    Feature in the Hub and across Memberships.

    Attributes:
        state (google.cloud.gkehub_v1.types.FeatureResourceState.State):
            The current state of the Feature resource in
            the Hub API.
    """

    class State(proto.Enum):
        r"""State describes the lifecycle status of a Feature."""
        STATE_UNSPECIFIED = 0
        ENABLING = 1
        ACTIVE = 2
        DISABLING = 3
        UPDATING = 4
        SERVICE_UPDATING = 5

    state = proto.Field(proto.ENUM, number=1, enum=State,)


class FeatureState(proto.Message):
    r"""FeatureState describes the high-level state of a Feature. It
    may be used to describe a Feature's state at the environ-level,
    or per-membershop, depending on the context.

    Attributes:
        code (google.cloud.gkehub_v1.types.FeatureState.Code):
            The high-level, machine-readable status of
            this Feature.
        description (str):
            A human-readable description of the current
            status.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The time this status and any related Feature-
            pecific details were updated.
    """

    class Code(proto.Enum):
        r"""Code represents a machine-readable, high-level status of the
        Feature.
        """
        CODE_UNSPECIFIED = 0
        OK = 1
        WARNING = 2
        ERROR = 3

    code = proto.Field(proto.ENUM, number=1, enum=Code,)
    description = proto.Field(proto.STRING, number=2,)
    update_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)


class CommonFeatureSpec(proto.Message):
    r"""CommonFeatureSpec contains Hub-wide configuration informatio.

    Attributes:
        multiclusteringress (google.cloud.gkehub_v1.multiclusteringress_v1.FeatureSpec):
            Multicluster Ingress-specific spec.
    """

    multiclusteringress = proto.Field(
        proto.MESSAGE,
        number=102,
        oneof="feature_spec",
        message=multiclusteringress_v1.FeatureSpec,
    )


class CommonFeatureState(proto.Message):
    r"""CommonFeatureState contains Hub-wide Feature status
    information.

    Attributes:
        state (google.cloud.gkehub_v1.types.FeatureState):
            Output only. The "running state" of the
            Feature in this Hub.
    """

    state = proto.Field(proto.MESSAGE, number=1, message="FeatureState",)


class MembershipFeatureSpec(proto.Message):
    r"""MembershipFeatureSpec contains configuration information for
    a single Membership.

    Attributes:
        configmanagement (google.cloud.gkehub_v1.configmanagement_v1.MembershipSpec):
            Config Management-specific spec.
    """

    configmanagement = proto.Field(
        proto.MESSAGE,
        number=106,
        oneof="feature_spec",
        message=configmanagement_v1.MembershipSpec,
    )


class MembershipFeatureState(proto.Message):
    r"""MembershipFeatureState contains Feature status information
    for a single Membership.

    Attributes:
        configmanagement (google.cloud.gkehub_v1.configmanagement_v1.MembershipState):
            Config Management-specific state.
        state (google.cloud.gkehub_v1.types.FeatureState):
            The high-level state of this Feature for a
            single membership.
    """

    configmanagement = proto.Field(
        proto.MESSAGE,
        number=106,
        oneof="feature_state",
        message=configmanagement_v1.MembershipState,
    )
    state = proto.Field(proto.MESSAGE, number=1, message="FeatureState",)


__all__ = tuple(sorted(__protobuf__.manifest))
