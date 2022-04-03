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

from google.api import launch_stage_pb2  # type: ignore
from google.cloud.run_v2.types import condition
from google.cloud.run_v2.types import k8s_min
from google.cloud.run_v2.types import vendor_settings
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.run.v2",
    manifest={
        "GetRevisionRequest",
        "ListRevisionsRequest",
        "ListRevisionsResponse",
        "DeleteRevisionRequest",
        "Revision",
    },
)


class GetRevisionRequest(proto.Message):
    r"""Request message for obtaining a Revision by its full name.

    Attributes:
        name (str):
            Required. The full name of the Revision.
            Format:
            projects/{project}/locations/{location}/services/{service}/revisions/{revision}
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListRevisionsRequest(proto.Message):
    r"""Request message for retrieving a list of Revisions.

    Attributes:
        parent (str):
            Required. The Service from which the
            Revisions should be listed. To list all
            Revisions across Services, use "-" instead of
            Service name. Format:
            projects/{project}/locations/{location}/services/{service}
        page_size (int):
            Maximum number of revisions to return in this
            call.
        page_token (str):
            A page token received from a previous call to
            ListRevisions. All other parameters must match.
        show_deleted (bool):
            If true, returns deleted (but unexpired)
            resources along with active ones.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    show_deleted = proto.Field(
        proto.BOOL,
        number=4,
    )


class ListRevisionsResponse(proto.Message):
    r"""Response message containing a list of Revisions.

    Attributes:
        revisions (Sequence[google.cloud.run_v2.types.Revision]):
            The resulting list of Revisions.
        next_page_token (str):
            A token indicating there are more items than page_size. Use
            it in the next ListRevisions request to continue.
    """

    @property
    def raw_page(self):
        return self

    revisions = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Revision",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteRevisionRequest(proto.Message):
    r"""Request message for deleting a retired Revision.
    Revision lifecycle is usually managed by making changes to the
    parent Service. Only retired revisions can be deleted with this
    API.

    Attributes:
        name (str):
            Required. The name of the Revision to delete.
            Format:
            projects/{project}/locations/{location}/services/{service}/revisions/{revision}
        validate_only (bool):
            Indicates that the request should be
            validated without actually deleting any
            resources.
        etag (str):
            A system-generated fingerprint for this
            version of the resource. This may be used to
            detect modification conflict during updates.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=2,
    )
    etag = proto.Field(
        proto.STRING,
        number=3,
    )


class Revision(proto.Message):
    r"""A Revision is an immutable snapshot of code and
    configuration.  A Revision references a container image.
    Revisions are only created by updates to its parent Service.

    Attributes:
        name (str):
            Output only. The unique name of this
            Revision.
        uid (str):
            Output only. Server assigned unique
            identifier for the Revision. The value is a
            UUID4 string and guaranteed to remain unchanged
            until the resource is deleted.
        generation (int):
            Output only. A number that monotonically
            increases every time the user modifies the
            desired state.
        labels (Sequence[google.cloud.run_v2.types.Revision.LabelsEntry]):
            KRM-style labels for the resource.
            User-provided labels are shared with Google's
            billing system, so they can be used to filter,
            or break down billing charges by team,
            component, environment, state, etc. For more
            information, visit
            https://cloud.google.com/resource-manager/docs/creating-managing-labels
            or
            https://cloud.google.com/run/docs/configuring/labels
            Cloud Run will populate some labels with
            'run.googleapis.com' or 'serving.knative.dev'
            namespaces. Those labels are read-only, and user
            changes will not be preserved.
        annotations (Sequence[google.cloud.run_v2.types.Revision.AnnotationsEntry]):
            KRM-style annotations for the resource.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last-modified time.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. For a deleted resource, the
            deletion time. It is only populated as a
            response to a Delete request.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. For a deleted resource, the time
            after which it will be permamently deleted. It
            is only populated as a response to a Delete
            request.
        launch_stage (google.api.launch_stage_pb2.LaunchStage):
            Set the launch stage to a preview stage on write to allow
            use of preview features in that stage. On read, describes
            whether the resource uses preview features. Launch Stages
            are defined at `Google Cloud Platform Launch
            Stages <https://cloud.google.com/terms/launch-stages>`__.
        service (str):
            Output only. The name of the parent service.
        scaling (google.cloud.run_v2.types.RevisionScaling):
            Scaling settings for this revision.
        vpc_access (google.cloud.run_v2.types.VpcAccess):
            VPC Access configuration for this Revision.
            For more information, visit
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
            permissions the revision has.
        containers (Sequence[google.cloud.run_v2.types.Container]):
            Holds the single container that defines the
            unit of execution for this Revision.
        volumes (Sequence[google.cloud.run_v2.types.Volume]):
            A list of Volumes to make available to
            containers.
        confidential (bool):
            Indicates whether Confidential Cloud Run is
            enabled in this Revision.
        execution_environment (google.cloud.run_v2.types.ExecutionEnvironment):
            The execution environment being used to host
            this Revision.
        encryption_key (str):
            A reference to a customer managed encryption
            key (CMEK) to use to encrypt this container
            image. For more information, go to
            https://cloud.google.com/run/docs/securing/using-cmek
        reconciling (bool):
            Output only. Indicates whether the resource's reconciliation
            is still in progress. See comments in
            ``Service.reconciling`` for additional information on
            reconciliation process in Cloud Run.
        conditions (Sequence[google.cloud.run_v2.types.Condition]):
            Output only. The Condition of this Revision,
            containing its readiness status, and detailed
            error information in case it did not reach a
            serving state.
        observed_generation (int):
            Output only. The generation of this Revision currently
            serving traffic. See comments in ``reconciling`` for
            additional information on reconciliation process in Cloud
            Run.
        log_uri (str):
            Output only. The Google Console URI to obtain
            logs for the Revision.
        etag (str):
            Output only. A system-generated fingerprint
            for this version of the resource. May be used to
            detect modification conflict during updates.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    uid = proto.Field(
        proto.STRING,
        number=2,
    )
    generation = proto.Field(
        proto.INT64,
        number=3,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    annotations = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    delete_time = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    expire_time = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    launch_stage = proto.Field(
        proto.ENUM,
        number=10,
        enum=launch_stage_pb2.LaunchStage,
    )
    service = proto.Field(
        proto.STRING,
        number=11,
    )
    scaling = proto.Field(
        proto.MESSAGE,
        number=12,
        message=vendor_settings.RevisionScaling,
    )
    vpc_access = proto.Field(
        proto.MESSAGE,
        number=13,
        message=vendor_settings.VpcAccess,
    )
    container_concurrency = proto.Field(
        proto.INT32,
        number=14,
    )
    timeout = proto.Field(
        proto.MESSAGE,
        number=15,
        message=duration_pb2.Duration,
    )
    service_account = proto.Field(
        proto.STRING,
        number=16,
    )
    containers = proto.RepeatedField(
        proto.MESSAGE,
        number=17,
        message=k8s_min.Container,
    )
    volumes = proto.RepeatedField(
        proto.MESSAGE,
        number=18,
        message=k8s_min.Volume,
    )
    confidential = proto.Field(
        proto.BOOL,
        number=19,
    )
    execution_environment = proto.Field(
        proto.ENUM,
        number=20,
        enum=vendor_settings.ExecutionEnvironment,
    )
    encryption_key = proto.Field(
        proto.STRING,
        number=21,
    )
    reconciling = proto.Field(
        proto.BOOL,
        number=30,
    )
    conditions = proto.RepeatedField(
        proto.MESSAGE,
        number=31,
        message=condition.Condition,
    )
    observed_generation = proto.Field(
        proto.INT64,
        number=32,
    )
    log_uri = proto.Field(
        proto.STRING,
        number=33,
    )
    etag = proto.Field(
        proto.STRING,
        number=99,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
