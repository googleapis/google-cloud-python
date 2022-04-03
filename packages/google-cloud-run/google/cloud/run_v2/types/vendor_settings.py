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


__protobuf__ = proto.module(
    package="google.cloud.run.v2",
    manifest={
        "IngressTraffic",
        "ExecutionEnvironment",
        "VpcAccess",
        "BinaryAuthorization",
        "RevisionScaling",
    },
)


class IngressTraffic(proto.Enum):
    r"""Allowed ingress traffic for the Container."""
    INGRESS_TRAFFIC_UNSPECIFIED = 0
    INGRESS_TRAFFIC_ALL = 1
    INGRESS_TRAFFIC_INTERNAL_ONLY = 2
    INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER = 3


class ExecutionEnvironment(proto.Enum):
    r"""Alternatives for execution environments."""
    EXECUTION_ENVIRONMENT_UNSPECIFIED = 0
    EXECUTION_ENVIRONMENT_DEFAULT = 1
    EXECUTION_ENVIRONMENT_GEN2 = 2


class VpcAccess(proto.Message):
    r"""VPC Access settings. For more information on creating a VPC
    Connector, visit
    https://cloud.google.com/vpc/docs/configure-serverless-vpc-access
    For information on how to configure Cloud Run with an existing
    VPC Connector, visit
    https://cloud.google.com/run/docs/configuring/connecting-vpc

    Attributes:
        connector (str):
            VPC Access connector name.
            Format:
            projects/{project}/locations/{location}/connectors/{connector}
        egress (google.cloud.run_v2.types.VpcAccess.VpcEgress):
            Traffic VPC egress settings.
    """

    class VpcEgress(proto.Enum):
        r"""Egress options for VPC access."""
        VPC_EGRESS_UNSPECIFIED = 0
        ALL_TRAFFIC = 1
        PRIVATE_RANGES_ONLY = 2

    connector = proto.Field(
        proto.STRING,
        number=1,
    )
    egress = proto.Field(
        proto.ENUM,
        number=2,
        enum=VpcEgress,
    )


class BinaryAuthorization(proto.Message):
    r"""Settings for Binary Authorization feature.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        use_default (bool):
            If True, indicates to use the default
            project's binary authorization policy. If False,
            binary authorization will be disabled.

            This field is a member of `oneof`_ ``binauthz_method``.
        breakglass_justification (str):
            If present, indicates to use Breakglass using this
            justification. If use_default is False, then it must be
            empty. For more information on breakglass, see
            https://cloud.google.com/binary-authorization/docs/using-breakglass
    """

    use_default = proto.Field(
        proto.BOOL,
        number=1,
        oneof="binauthz_method",
    )
    breakglass_justification = proto.Field(
        proto.STRING,
        number=2,
    )


class RevisionScaling(proto.Message):
    r"""Settings for revision-level scaling settings.

    Attributes:
        min_instance_count (int):
            Minimum number of serving instances that this
            resource should have.
        max_instance_count (int):
            Maximum number of serving instances that this
            resource should have.
    """

    min_instance_count = proto.Field(
        proto.INT32,
        number=1,
    )
    max_instance_count = proto.Field(
        proto.INT32,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
