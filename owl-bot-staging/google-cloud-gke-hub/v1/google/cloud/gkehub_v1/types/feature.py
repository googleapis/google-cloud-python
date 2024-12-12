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

from google.cloud.gkehub.configmanagement.v1 import configmanagement_pb2  # type: ignore
from google.cloud.gkehub.multiclusteringress.v1 import multiclusteringress_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.cloud.gkehub.v1',
    manifest={
        'Feature',
        'FeatureResourceState',
        'FeatureState',
        'CommonFeatureSpec',
        'CommonFeatureState',
        'MembershipFeatureSpec',
        'MembershipFeatureState',
    },
)


class Feature(proto.Message):
    r"""Feature represents the settings and status of any Hub
    Feature.

    Attributes:
        name (str):
            Output only. The full, unique name of this Feature resource
            in the format ``projects/*/locations/*/features/*``.
        labels (MutableMapping[str, str]):
            GCP labels for this Feature.
        resource_state (google.cloud.gkehub_v1.types.FeatureResourceState):
            Output only. State of the Feature resource
            itself.
        spec (google.cloud.gkehub_v1.types.CommonFeatureSpec):
            Optional. Hub-wide Feature configuration. If
            this Feature does not support any Hub-wide
            configuration, this field may be unused.
        membership_specs (MutableMapping[str, google.cloud.gkehub_v1.types.MembershipFeatureSpec]):
            Optional. Membership-specific configuration
            for this Feature. If this Feature does not
            support any per-Membership configuration, this
            field may be unused.

            The keys indicate which Membership the
            configuration is for, in the form:

                projects/{p}/locations/{l}/memberships/{m}

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
        membership_states (MutableMapping[str, google.cloud.gkehub_v1.types.MembershipFeatureState]):
            Output only. Membership-specific Feature
            status. If this Feature does report any
            per-Membership status, this field may be unused.

            The keys indicate which Membership the state is
            for, in the form:

                projects/{p}/locations/{l}/memberships/{m}

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

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=2,
    )
    resource_state: 'FeatureResourceState' = proto.Field(
        proto.MESSAGE,
        number=3,
        message='FeatureResourceState',
    )
    spec: 'CommonFeatureSpec' = proto.Field(
        proto.MESSAGE,
        number=4,
        message='CommonFeatureSpec',
    )
    membership_specs: MutableMapping[str, 'MembershipFeatureSpec'] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=5,
        message='MembershipFeatureSpec',
    )
    state: 'CommonFeatureState' = proto.Field(
        proto.MESSAGE,
        number=6,
        message='CommonFeatureState',
    )
    membership_states: MutableMapping[str, 'MembershipFeatureState'] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=7,
        message='MembershipFeatureState',
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
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
        r"""State describes the lifecycle status of a Feature.

        Values:
            STATE_UNSPECIFIED (0):
                State is unknown or not set.
            ENABLING (1):
                The Feature is being enabled, and the Feature
                resource is being created. Once complete, the
                corresponding Feature will be enabled in this
                Hub.
            ACTIVE (2):
                The Feature is enabled in this Hub, and the
                Feature resource is fully available.
            DISABLING (3):
                The Feature is being disabled in this Hub,
                and the Feature resource is being deleted.
            UPDATING (4):
                The Feature resource is being updated.
            SERVICE_UPDATING (5):
                The Feature resource is being updated by the
                Hub Service.
        """
        STATE_UNSPECIFIED = 0
        ENABLING = 1
        ACTIVE = 2
        DISABLING = 3
        UPDATING = 4
        SERVICE_UPDATING = 5

    state: State = proto.Field(
        proto.ENUM,
        number=1,
        enum=State,
    )


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
            The time this status and any related
            Feature-specific details were updated.
    """
    class Code(proto.Enum):
        r"""Code represents a machine-readable, high-level status of the
        Feature.

        Values:
            CODE_UNSPECIFIED (0):
                Unknown or not set.
            OK (1):
                The Feature is operating normally.
            WARNING (2):
                The Feature has encountered an issue, and is
                operating in a degraded state. The Feature may
                need intervention to return to normal operation.
                See the description and any associated
                Feature-specific details for more information.
            ERROR (3):
                The Feature is not operating or is in a
                severely degraded state. The Feature may need
                intervention to return to normal operation. See
                the description and any associated
                Feature-specific details for more information.
        """
        CODE_UNSPECIFIED = 0
        OK = 1
        WARNING = 2
        ERROR = 3

    code: Code = proto.Field(
        proto.ENUM,
        number=1,
        enum=Code,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )


class CommonFeatureSpec(proto.Message):
    r"""CommonFeatureSpec contains Hub-wide configuration information

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        multiclusteringress (google.cloud.gkehub.multiclusteringress.v1.multiclusteringress_pb2.FeatureSpec):
            Multicluster Ingress-specific spec.

            This field is a member of `oneof`_ ``feature_spec``.
    """

    multiclusteringress: multiclusteringress_pb2.FeatureSpec = proto.Field(
        proto.MESSAGE,
        number=102,
        oneof='feature_spec',
        message=multiclusteringress_pb2.FeatureSpec,
    )


class CommonFeatureState(proto.Message):
    r"""CommonFeatureState contains Hub-wide Feature status
    information.

    Attributes:
        state (google.cloud.gkehub_v1.types.FeatureState):
            Output only. The "running state" of the
            Feature in this Hub.
    """

    state: 'FeatureState' = proto.Field(
        proto.MESSAGE,
        number=1,
        message='FeatureState',
    )


class MembershipFeatureSpec(proto.Message):
    r"""MembershipFeatureSpec contains configuration information for
    a single Membership.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        configmanagement (google.cloud.gkehub.configmanagement.v1.configmanagement_pb2.MembershipSpec):
            Config Management-specific spec.

            This field is a member of `oneof`_ ``feature_spec``.
    """

    configmanagement: configmanagement_pb2.MembershipSpec = proto.Field(
        proto.MESSAGE,
        number=106,
        oneof='feature_spec',
        message=configmanagement_pb2.MembershipSpec,
    )


class MembershipFeatureState(proto.Message):
    r"""MembershipFeatureState contains Feature status information
    for a single Membership.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        configmanagement (google.cloud.gkehub.configmanagement.v1.configmanagement_pb2.MembershipState):
            Config Management-specific state.

            This field is a member of `oneof`_ ``feature_state``.
        state (google.cloud.gkehub_v1.types.FeatureState):
            The high-level state of this Feature for a
            single membership.
    """

    configmanagement: configmanagement_pb2.MembershipState = proto.Field(
        proto.MESSAGE,
        number=106,
        oneof='feature_state',
        message=configmanagement_pb2.MembershipState,
    )
    state: 'FeatureState' = proto.Field(
        proto.MESSAGE,
        number=1,
        message='FeatureState',
    )


__all__ = tuple(sorted(__protobuf__.manifest))
