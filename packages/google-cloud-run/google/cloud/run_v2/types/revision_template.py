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

from google.cloud.run_v2.types import k8s_min
from google.cloud.run_v2.types import vendor_settings
from google.protobuf import duration_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.run.v2",
    manifest={
        "RevisionTemplate",
    },
)


class RevisionTemplate(proto.Message):
    r"""RevisionTemplate describes the data a revision should have
    when created from a template.

    Attributes:
        revision (str):
            The unique name for the revision. If this
            field is omitted, it will be automatically
            generated based on the Service name.
        labels (Sequence[google.cloud.run_v2.types.RevisionTemplate.LabelsEntry]):
            KRM-style labels for the resource.
        annotations (Sequence[google.cloud.run_v2.types.RevisionTemplate.AnnotationsEntry]):
            KRM-style annotations for the resource.
        scaling (google.cloud.run_v2.types.RevisionScaling):
            Scaling settings for this Revision.
        vpc_access (google.cloud.run_v2.types.VpcAccess):
            VPC Access configuration to use for this
            Revision. For more information, visit
            https://cloud.google.com/run/docs/configuring/connecting-vpc.
        container_concurrency (int):
            Sets the maximum number of requests that each
            serving instance can receive.
        timeout (google.protobuf.duration_pb2.Duration):
            Max allowed time for an instance to respond
            to a request.
        service_account (str):
            Email address of the IAM service account
            associated with the revision of the service. The
            service account represents the identity of the
            running revision, and determines what
            permissions the revision has. If not provided,
            the revision will use the project's default
            service account.
        containers (Sequence[google.cloud.run_v2.types.Container]):
            Holds the single container that defines the
            unit of execution for this Revision.
        volumes (Sequence[google.cloud.run_v2.types.Volume]):
            A list of Volumes to make available to
            containers.
        confidential (bool):
            Enables Confidential Cloud Run in Revisions
            created using this template.
        execution_environment (google.cloud.run_v2.types.ExecutionEnvironment):
            The sandbox environment to host this
            Revision.
        encryption_key (str):
            A reference to a customer managed encryption
            key (CMEK) to use to encrypt this container
            image. For more information, go to
            https://cloud.google.com/run/docs/securing/using-cmek
    """

    revision = proto.Field(
        proto.STRING,
        number=1,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=2,
    )
    annotations = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )
    scaling = proto.Field(
        proto.MESSAGE,
        number=4,
        message=vendor_settings.RevisionScaling,
    )
    vpc_access = proto.Field(
        proto.MESSAGE,
        number=6,
        message=vendor_settings.VpcAccess,
    )
    container_concurrency = proto.Field(
        proto.INT32,
        number=7,
    )
    timeout = proto.Field(
        proto.MESSAGE,
        number=8,
        message=duration_pb2.Duration,
    )
    service_account = proto.Field(
        proto.STRING,
        number=9,
    )
    containers = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message=k8s_min.Container,
    )
    volumes = proto.RepeatedField(
        proto.MESSAGE,
        number=11,
        message=k8s_min.Volume,
    )
    confidential = proto.Field(
        proto.BOOL,
        number=12,
    )
    execution_environment = proto.Field(
        proto.ENUM,
        number=13,
        enum=vendor_settings.ExecutionEnvironment,
    )
    encryption_key = proto.Field(
        proto.STRING,
        number=14,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
