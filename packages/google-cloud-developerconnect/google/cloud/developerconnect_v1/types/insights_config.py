# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.developerconnect.v1",
    manifest={
        "InsightsConfig",
        "RuntimeConfig",
        "GKEWorkload",
        "AppHubWorkload",
        "ArtifactConfig",
        "GoogleArtifactAnalysis",
        "GoogleArtifactRegistry",
        "CreateInsightsConfigRequest",
        "GetInsightsConfigRequest",
        "ListInsightsConfigsRequest",
        "ListInsightsConfigsResponse",
        "DeleteInsightsConfigRequest",
        "UpdateInsightsConfigRequest",
    },
)


class InsightsConfig(proto.Message):
    r"""The InsightsConfig resource is the core configuration object
    to capture events from your Software Development Lifecycle. It
    acts as the central hub for managing how Developer connect
    understands your application, its runtime environments, and the
    artifacts deployed within them.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        app_hub_application (str):
            Optional. The name of the App Hub
            Application. Format:

            projects/{project}/locations/{location}/applications/{application}

            This field is a member of `oneof`_ ``insights_config_context``.
        name (str):
            Identifier. The name of the InsightsConfig.
            Format:

            projects/{project}/locations/{location}/insightsConfigs/{insightsConfig}
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Create timestamp
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Update timestamp
        runtime_configs (MutableSequence[google.cloud.developerconnect_v1.types.RuntimeConfig]):
            Output only. The runtime configurations where
            the application is deployed.
        artifact_configs (MutableSequence[google.cloud.developerconnect_v1.types.ArtifactConfig]):
            Optional. The artifact configurations of the
            artifacts that are deployed.
        state (google.cloud.developerconnect_v1.types.InsightsConfig.State):
            Optional. Output only. The state of the
            InsightsConfig.
        annotations (MutableMapping[str, str]):
            Optional. User specified annotations. See
            https://google.aip.dev/148#annotations for more
            details such as format and size limitations.
        labels (MutableMapping[str, str]):
            Optional. Set of labels associated with an
            InsightsConfig.
        reconciling (bool):
            Output only. Reconciling
            (https://google.aip.dev/128#reconciliation). Set
            to true if the current state of InsightsConfig
            does not match the user's intended state, and
            the service is actively updating the resource to
            reconcile them. This can happen due to
            user-triggered updates or system actions like
            failover or maintenance.
        errors (MutableSequence[google.rpc.status_pb2.Status]):
            Output only. Any errors that occurred while setting up the
            InsightsConfig. Each error will be in the format:
            ``field_name: error_message``, e.g. GetAppHubApplication:
            Permission denied while getting App Hub application. Please
            grant permissions to the P4SA.
    """

    class State(proto.Enum):
        r"""The state of the InsightsConfig.

        Values:
            STATE_UNSPECIFIED (0):
                No state specified.
            PENDING (5):
                The InsightsConfig is pending application
                discovery/runtime discovery.
            COMPLETE (3):
                The initial discovery process is complete.
            ERROR (4):
                The InsightsConfig is in an error state.
        """
        STATE_UNSPECIFIED = 0
        PENDING = 5
        COMPLETE = 3
        ERROR = 4

    app_hub_application: str = proto.Field(
        proto.STRING,
        number=4,
        oneof="insights_config_context",
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    runtime_configs: MutableSequence["RuntimeConfig"] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="RuntimeConfig",
    )
    artifact_configs: MutableSequence["ArtifactConfig"] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message="ArtifactConfig",
    )
    state: State = proto.Field(
        proto.ENUM,
        number=7,
        enum=State,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=8,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )
    reconciling: bool = proto.Field(
        proto.BOOL,
        number=10,
    )
    errors: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=11,
        message=status_pb2.Status,
    )


class RuntimeConfig(proto.Message):
    r"""RuntimeConfig represents the runtimes where the application
    is deployed.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gke_workload (google.cloud.developerconnect_v1.types.GKEWorkload):
            Output only. Google Kubernetes Engine
            runtime.

            This field is a member of `oneof`_ ``runtime``.
        app_hub_workload (google.cloud.developerconnect_v1.types.AppHubWorkload):
            Output only. App Hub Workload.

            This field is a member of `oneof`_ ``derived_from``.
        uri (str):
            Required. Immutable. The URI of the runtime
            configuration. For GKE, this is the cluster
            name. For Cloud Run, this is the service name.
        state (google.cloud.developerconnect_v1.types.RuntimeConfig.State):
            Output only. The state of the Runtime.
    """

    class State(proto.Enum):
        r"""The state of the runtime in the InsightsConfig.
        Whether the runtime is linked to the InsightsConfig.

        Values:
            STATE_UNSPECIFIED (0):
                No state specified.
            LINKED (1):
                The runtime configuration has been linked to
                the InsightsConfig.
            UNLINKED (2):
                The runtime configuration has been unlinked
                to the InsightsConfig.
        """
        STATE_UNSPECIFIED = 0
        LINKED = 1
        UNLINKED = 2

    gke_workload: "GKEWorkload" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="runtime",
        message="GKEWorkload",
    )
    app_hub_workload: "AppHubWorkload" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="derived_from",
        message="AppHubWorkload",
    )
    uri: str = proto.Field(
        proto.STRING,
        number=1,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=2,
        enum=State,
    )


class GKEWorkload(proto.Message):
    r"""GKEWorkload represents the Google Kubernetes Engine runtime.

    Attributes:
        cluster (str):
            Required. Immutable. The name of the GKE cluster. Format:
            ``projects/{project}/locations/{location}/clusters/{cluster}``.
        deployment (str):
            Output only. The name of the GKE deployment. Format:
            ``projects/{project}/locations/{location}/clusters/{cluster}/namespaces/{namespace}/deployments/{deployment}``.
    """

    cluster: str = proto.Field(
        proto.STRING,
        number=1,
    )
    deployment: str = proto.Field(
        proto.STRING,
        number=2,
    )


class AppHubWorkload(proto.Message):
    r"""AppHubWorkload represents the App Hub Workload.

    Attributes:
        workload (str):
            Required. Output only. Immutable. The name of the App Hub
            Workload. Format:
            ``projects/{project}/locations/{location}/applications/{application}/workloads/{workload}``.
        criticality (str):
            Output only. The criticality of the App Hub
            Workload.
        environment (str):
            Output only. The environment of the App Hub
            Workload.
    """

    workload: str = proto.Field(
        proto.STRING,
        number=1,
    )
    criticality: str = proto.Field(
        proto.STRING,
        number=2,
    )
    environment: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ArtifactConfig(proto.Message):
    r"""The artifact config of the artifact that is deployed.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        google_artifact_registry (google.cloud.developerconnect_v1.types.GoogleArtifactRegistry):
            Optional. Set if the artifact is stored in
            Artifact regsitry.

            This field is a member of `oneof`_ ``artifact_storage``.
        google_artifact_analysis (google.cloud.developerconnect_v1.types.GoogleArtifactAnalysis):
            Optional. Set if the artifact metadata is
            stored in Artifact analysis.

            This field is a member of `oneof`_ ``artifact_metadata_storage``.
        uri (str):
            Required. Immutable. The URI of the artifact that is
            deployed. e.g.
            ``us-docker.pkg.dev/my-project/my-repo/image``. The URI does
            not include the tag / digest because it captures a lineage
            of artifacts.
    """

    google_artifact_registry: "GoogleArtifactRegistry" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="artifact_storage",
        message="GoogleArtifactRegistry",
    )
    google_artifact_analysis: "GoogleArtifactAnalysis" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="artifact_metadata_storage",
        message="GoogleArtifactAnalysis",
    )
    uri: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GoogleArtifactAnalysis(proto.Message):
    r"""Google Artifact Analysis configurations.

    Attributes:
        project_id (str):
            Required. The project id of the project where
            the provenance is stored.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GoogleArtifactRegistry(proto.Message):
    r"""Google Artifact Registry configurations.

    Attributes:
        project_id (str):
            Required. The host project of Artifact
            Registry.
        artifact_registry_package (str):
            Required. Immutable. The name of the artifact
            registry package.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    artifact_registry_package: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateInsightsConfigRequest(proto.Message):
    r"""Request for creating an InsightsConfig.

    Attributes:
        parent (str):
            Required. Value for parent.
        insights_config_id (str):
            Required. ID of the requesting
            InsightsConfig.
        insights_config (google.cloud.developerconnect_v1.types.InsightsConfig):
            Required. The resource being created.
        validate_only (bool):
            Optional. If set, validate the request, but
            do not actually post it.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    insights_config_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    insights_config: "InsightsConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="InsightsConfig",
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class GetInsightsConfigRequest(proto.Message):
    r"""Request for getting an InsightsConfig.

    Attributes:
        name (str):
            Required. Name of the resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListInsightsConfigsRequest(proto.Message):
    r"""Request for requesting list of InsightsConfigs.

    Attributes:
        parent (str):
            Required. Parent value for
            ListInsightsConfigsRequest.
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
        filter (str):
            Optional. Filtering results. See
            https://google.aip.dev/160 for more details.
            Filter string, adhering to the rules in
            https://google.aip.dev/160. List only
            InsightsConfigs matching the filter. If filter
            is empty, all InsightsConfigs are listed.
        order_by (str):
            Optional. Hint for how to order the results.
    """

    parent: str = proto.Field(
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListInsightsConfigsResponse(proto.Message):
    r"""Request for response to listing InsightsConfigs.

    Attributes:
        insights_configs (MutableSequence[google.cloud.developerconnect_v1.types.InsightsConfig]):
            The list of InsightsConfigs.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    insights_configs: MutableSequence["InsightsConfig"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="InsightsConfig",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class DeleteInsightsConfigRequest(proto.Message):
    r"""Request for deleting an InsightsConfig.

    Attributes:
        name (str):
            Required. Value for parent.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. If set, validate the request, but
            do not actually post it.
        etag (str):
            Optional. This checksum is computed by the
            server based on the value of other fields, and
            may be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateInsightsConfigRequest(proto.Message):
    r"""Request for updating an InsightsConfig.

    Attributes:
        insights_config (google.cloud.developerconnect_v1.types.InsightsConfig):
            Required. The resource being updated.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        allow_missing (bool):
            Optional. If set to true, and the insightsConfig is not
            found a new insightsConfig will be created. In this
            situation ``update_mask`` is ignored. The creation will
            succeed only if the input insightsConfig has all the
            necessary information (e.g a github_config with both
            user_oauth_token and installation_id properties).
        validate_only (bool):
            Optional. If set, validate the request, but
            do not actually post it.
    """

    insights_config: "InsightsConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="InsightsConfig",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
