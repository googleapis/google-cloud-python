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
from google.cloud.run_v2.types import revision_template
from google.cloud.run_v2.types import traffic_target
from google.cloud.run_v2.types import vendor_settings
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.run.v2",
    manifest={
        "CreateServiceRequest",
        "UpdateServiceRequest",
        "ListServicesRequest",
        "ListServicesResponse",
        "GetServiceRequest",
        "DeleteServiceRequest",
        "Service",
    },
)


class CreateServiceRequest(proto.Message):
    r"""Request message for creating a Service.

    Attributes:
        parent (str):
            Required. The location and project in which
            this service should be created. Format:
            projects/{projectnumber}/locations/{location}
        service (google.cloud.run_v2.types.Service):
            Required. The Service instance to create.
        service_id (str):
            Required. The unique identifier for the Service. The name of
            the service becomes {parent}/services/{service_id}.
        validate_only (bool):
            Indicates that the request should be
            validated and default values populated, without
            persisting the request or creating any
            resources.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    service = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Service",
    )
    service_id = proto.Field(
        proto.STRING,
        number=3,
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateServiceRequest(proto.Message):
    r"""Request message for updating a service.

    Attributes:
        service (google.cloud.run_v2.types.Service):
            Required. The Service to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to be updated.
        validate_only (bool):
            Indicates that the request should be
            validated and default values populated, without
            persisting the request or updating any
            resources.
        allow_missing (bool):
            If set to true, and if the Service does not
            exist, it will create a new one. Caller must
            have both create and update permissions for this
            call if this is set to true.
    """

    service = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Service",
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=3,
    )
    allow_missing = proto.Field(
        proto.BOOL,
        number=4,
    )


class ListServicesRequest(proto.Message):
    r"""Request message for retrieving a list of Services.

    Attributes:
        parent (str):
            Required. The location and project to list
            resources on. Location must be a valid GCP
            region, and may not be the "-" wildcard. Format:
            projects/{projectnumber}/locations/{location}
        page_size (int):
            Maximum number of Services to return in this
            call.
        page_token (str):
            A page token received from a previous call to
            ListServices. All other parameters must match.
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


class ListServicesResponse(proto.Message):
    r"""Response message containing a list of Services.

    Attributes:
        services (Sequence[google.cloud.run_v2.types.Service]):
            The resulting list of Services.
        next_page_token (str):
            A token indicating there are more items than page_size. Use
            it in the next ListServices request to continue.
    """

    @property
    def raw_page(self):
        return self

    services = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Service",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetServiceRequest(proto.Message):
    r"""Request message for obtaining a Service by its full name.

    Attributes:
        name (str):
            Required. The full name of the Service.
            Format:
            projects/{projectnumber}/locations/{location}/services/{service}
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteServiceRequest(proto.Message):
    r"""Request message to delete a Service by its full name.

    Attributes:
        name (str):
            Required. The full name of the Service.
            Format:
            projects/{projectnumber}/locations/{location}/services/{service}
        validate_only (bool):
            Indicates that the request should be
            validated without actually deleting any
            resources.
        etag (str):
            A system-generated fingerprint for this
            version of the resource. May be used to detect
            modification conflict during updates.
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


class Service(proto.Message):
    r"""Service acts as a top-level container that manages a set of
    configurations and revision templates which implement a network
    service. Service exists to provide a singular abstraction which
    can be access controlled, reasoned about, and which encapsulates
    software lifecycle decisions such as rollout policy and team
    resource ownership.

    Attributes:
        name (str):
            The fully qualified name of this Service. In
            CreateServiceRequest, this field is ignored, and instead
            composed from CreateServiceRequest.parent and
            CreateServiceRequest.service_id.

            Format:
            projects/{project}/locations/{location}/services/{service_id}
        description (str):
            User-provided description of the Service.
            This field currently has a 512-character limit.
        uid (str):
            Output only. Server assigned unique
            identifier for the trigger. The value is a UUID4
            string and guaranteed to remain unchanged until
            the resource is deleted.
        generation (int):
            Output only. A number that monotonically
            increases every time the user modifies the
            desired state.
        labels (Sequence[google.cloud.run_v2.types.Service.LabelsEntry]):
            Map of string keys and values that can be
            used to organize and categorize objects.
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
        annotations (Sequence[google.cloud.run_v2.types.Service.AnnotationsEntry]):
            Unstructured key value map that may be set by
            external tools to store and arbitrary metadata.
            They are not queryable and should be preserved
            when modifying objects. Cloud Run will populate
            some annotations using 'run.googleapis.com' or
            'serving.knative.dev' namespaces. This field
            follows Kubernetes annotations' namespacing,
            limits, and rules. More info:
            https://kubernetes.io/docs/user-guide/annotations
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last-modified time.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The deletion time.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. For a deleted resource, the time
            after which it will be permamently deleted.
        creator (str):
            Output only. Email address of the
            authenticated creator.
        last_modifier (str):
            Output only. Email address of the last
            authenticated modifier.
        client (str):
            Arbitrary identifier for the API client.
        client_version (str):
            Arbitrary version identifier for the API
            client.
        ingress (google.cloud.run_v2.types.IngressTraffic):
            Provides the ingress settings for this Service. On output,
            returns the currently observed ingress settings, or
            INGRESS_TRAFFIC_UNSPECIFIED if no revision is active.
        launch_stage (google.api.launch_stage_pb2.LaunchStage):
            The launch stage as defined by `Google Cloud Platform Launch
            Stages <https://cloud.google.com/terms/launch-stages>`__.
            Cloud Run supports ``ALPHA``, ``BETA``, and ``GA``. If no
            value is specified, GA is assumed.
        binary_authorization (google.cloud.run_v2.types.BinaryAuthorization):
            Settings for the Binary Authorization
            feature.
        template (google.cloud.run_v2.types.RevisionTemplate):
            Required. The template used to create
            revisions for this Service.
        traffic (Sequence[google.cloud.run_v2.types.TrafficTarget]):
            Specifies how to distribute traffic over a collection of
            Revisions belonging to the Service. If traffic is empty or
            not provided, defaults to 100% traffic to the latest
            ``Ready`` Revision.
        observed_generation (int):
            Output only. The generation of this Service currently
            serving traffic. See comments in ``reconciling`` for
            additional information on reconciliation process in Cloud
            Run.
        terminal_condition (google.cloud.run_v2.types.Condition):
            Output only. The Condition of this Service, containing its
            readiness status, and detailed error information in case it
            did not reach a serving state. See comments in
            ``reconciling`` for additional information on reconciliation
            process in Cloud Run.
        conditions (Sequence[google.cloud.run_v2.types.Condition]):
            Output only. The Conditions of all other associated
            sub-resources. They contain additional diagnostics
            information in case the Service does not reach its Serving
            state. See comments in ``reconciling`` for additional
            information on reconciliation process in Cloud Run.
        latest_ready_revision (str):
            Output only. Name of the latest revision that is serving
            traffic. See comments in ``reconciling`` for additional
            information on reconciliation process in Cloud Run.
        latest_created_revision (str):
            Output only. Name of the last created revision. See comments
            in ``reconciling`` for additional information on
            reconciliation process in Cloud Run.
        traffic_statuses (Sequence[google.cloud.run_v2.types.TrafficTargetStatus]):
            Output only. Detailed status information for corresponding
            traffic targets. See comments in ``reconciling`` for
            additional information on reconciliation process in Cloud
            Run.
        uri (str):
            Output only. The main URI in which this
            Service is serving traffic.
        reconciling (bool):
            Output only. Returns true if the Service is currently being
            acted upon by the system to bring it into the desired state.

            When a new Service is created, or an existing one is
            updated, Cloud Run will asynchronously perform all necessary
            steps to bring the Service to the desired serving state.
            This process is called reconciliation. While reconciliation
            is in process, ``observed_generation``,
            ``latest_ready_revison``, ``traffic_statuses``, and ``uri``
            will have transient values that might mismatch the intended
            state: Once reconciliation is over (and this field is
            false), there are two possible outcomes: reconciliation
            succeeded and the serving state matches the Service, or
            there was an error, and reconciliation failed. This state
            can be found in ``terminal_condition.state``.

            If reconciliation succeeded, the following fields will
            match: ``traffic`` and ``traffic_statuses``,
            ``observed_generation`` and ``generation``,
            ``latest_ready_revision`` and ``latest_created_revision``.

            If reconciliation failed, ``traffic_statuses``,
            ``observed_generation``, and ``latest_ready_revision`` will
            have the state of the last serving revision, or empty for
            newly created Services. Additional information on the
            failure can be found in ``terminal_condition`` and
            ``conditions``.
        etag (str):
            Output only. A system-generated fingerprint
            for this version of the resource. May be used to
            detect modification conflict during updates.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    description = proto.Field(
        proto.STRING,
        number=2,
    )
    uid = proto.Field(
        proto.STRING,
        number=3,
    )
    generation = proto.Field(
        proto.INT64,
        number=4,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    annotations = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    delete_time = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    expire_time = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    creator = proto.Field(
        proto.STRING,
        number=11,
    )
    last_modifier = proto.Field(
        proto.STRING,
        number=12,
    )
    client = proto.Field(
        proto.STRING,
        number=13,
    )
    client_version = proto.Field(
        proto.STRING,
        number=14,
    )
    ingress = proto.Field(
        proto.ENUM,
        number=15,
        enum=vendor_settings.IngressTraffic,
    )
    launch_stage = proto.Field(
        proto.ENUM,
        number=16,
        enum=launch_stage_pb2.LaunchStage,
    )
    binary_authorization = proto.Field(
        proto.MESSAGE,
        number=17,
        message=vendor_settings.BinaryAuthorization,
    )
    template = proto.Field(
        proto.MESSAGE,
        number=18,
        message=revision_template.RevisionTemplate,
    )
    traffic = proto.RepeatedField(
        proto.MESSAGE,
        number=19,
        message=traffic_target.TrafficTarget,
    )
    observed_generation = proto.Field(
        proto.INT64,
        number=30,
    )
    terminal_condition = proto.Field(
        proto.MESSAGE,
        number=31,
        message=condition.Condition,
    )
    conditions = proto.RepeatedField(
        proto.MESSAGE,
        number=32,
        message=condition.Condition,
    )
    latest_ready_revision = proto.Field(
        proto.STRING,
        number=33,
    )
    latest_created_revision = proto.Field(
        proto.STRING,
        number=34,
    )
    traffic_statuses = proto.RepeatedField(
        proto.MESSAGE,
        number=35,
        message=traffic_target.TrafficTargetStatus,
    )
    uri = proto.Field(
        proto.STRING,
        number=36,
    )
    reconciling = proto.Field(
        proto.BOOL,
        number=98,
    )
    etag = proto.Field(
        proto.STRING,
        number=99,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
