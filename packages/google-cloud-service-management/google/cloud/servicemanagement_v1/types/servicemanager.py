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

from google.api import service_pb2  # type: ignore
from google.cloud.servicemanagement_v1.types import resources
from google.protobuf import any_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.api.servicemanagement.v1",
    manifest={
        "ListServicesRequest",
        "ListServicesResponse",
        "GetServiceRequest",
        "CreateServiceRequest",
        "DeleteServiceRequest",
        "UndeleteServiceRequest",
        "UndeleteServiceResponse",
        "GetServiceConfigRequest",
        "ListServiceConfigsRequest",
        "ListServiceConfigsResponse",
        "CreateServiceConfigRequest",
        "SubmitConfigSourceRequest",
        "SubmitConfigSourceResponse",
        "CreateServiceRolloutRequest",
        "ListServiceRolloutsRequest",
        "ListServiceRolloutsResponse",
        "GetServiceRolloutRequest",
        "EnableServiceRequest",
        "EnableServiceResponse",
        "DisableServiceRequest",
        "DisableServiceResponse",
        "GenerateConfigReportRequest",
        "GenerateConfigReportResponse",
    },
)


class ListServicesRequest(proto.Message):
    r"""Request message for ``ListServices`` method.
    Attributes:
        producer_project_id (str):
            Include services produced by the specified
            project.
        page_size (int):
            The max number of items to include in the
            response list. Page size is 50 if not specified.
            Maximum value is 100.
        page_token (str):
            Token identifying which result to start with;
            returned by a previous list call.
        consumer_id (str):
            Include services consumed by the specified consumer.

            The Google Service Management implementation accepts the
            following forms:

            -  project:<project_id>
    """

    producer_project_id = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=5,)
    page_token = proto.Field(proto.STRING, number=6,)
    consumer_id = proto.Field(proto.STRING, number=7,)


class ListServicesResponse(proto.Message):
    r"""Response message for ``ListServices`` method.
    Attributes:
        services (Sequence[google.cloud.servicemanagement_v1.types.ManagedService]):
            The returned services will only have the name
            field set.
        next_page_token (str):
            Token that can be passed to ``ListServices`` to resume a
            paginated query.
    """

    @property
    def raw_page(self):
        return self

    services = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.ManagedService,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetServiceRequest(proto.Message):
    r"""Request message for ``GetService`` method.
    Attributes:
        service_name (str):
            Required. The name of the service. See the
            ``ServiceManager`` overview for naming requirements. For
            example: ``example.googleapis.com``.
    """

    service_name = proto.Field(proto.STRING, number=1,)


class CreateServiceRequest(proto.Message):
    r"""Request message for CreateService method.
    Attributes:
        service (google.cloud.servicemanagement_v1.types.ManagedService):
            Required. Initial values for the service
            resource.
    """

    service = proto.Field(proto.MESSAGE, number=1, message=resources.ManagedService,)


class DeleteServiceRequest(proto.Message):
    r"""Request message for DeleteService method.
    Attributes:
        service_name (str):
            Required. The name of the service. See the
            `overview <https://cloud.google.com/service-management/overview>`__
            for naming requirements. For example:
            ``example.googleapis.com``.
    """

    service_name = proto.Field(proto.STRING, number=1,)


class UndeleteServiceRequest(proto.Message):
    r"""Request message for UndeleteService method.
    Attributes:
        service_name (str):
            Required. The name of the service. See the
            `overview <https://cloud.google.com/service-management/overview>`__
            for naming requirements. For example:
            ``example.googleapis.com``.
    """

    service_name = proto.Field(proto.STRING, number=1,)


class UndeleteServiceResponse(proto.Message):
    r"""Response message for UndeleteService method.
    Attributes:
        service (google.cloud.servicemanagement_v1.types.ManagedService):
            Revived service resource.
    """

    service = proto.Field(proto.MESSAGE, number=1, message=resources.ManagedService,)


class GetServiceConfigRequest(proto.Message):
    r"""Request message for GetServiceConfig method.
    Attributes:
        service_name (str):
            Required. The name of the service. See the
            `overview <https://cloud.google.com/service-management/overview>`__
            for naming requirements. For example:
            ``example.googleapis.com``.
        config_id (str):
            Required. The id of the service configuration resource.

            This field must be specified for the server to return all
            fields, including ``SourceInfo``.
        view (google.cloud.servicemanagement_v1.types.GetServiceConfigRequest.ConfigView):
            Specifies which parts of the Service Config
            should be returned in the response.
    """

    class ConfigView(proto.Enum):
        r""""""
        BASIC = 0
        FULL = 1

    service_name = proto.Field(proto.STRING, number=1,)
    config_id = proto.Field(proto.STRING, number=2,)
    view = proto.Field(proto.ENUM, number=3, enum=ConfigView,)


class ListServiceConfigsRequest(proto.Message):
    r"""Request message for ListServiceConfigs method.
    Attributes:
        service_name (str):
            Required. The name of the service. See the
            `overview <https://cloud.google.com/service-management/overview>`__
            for naming requirements. For example:
            ``example.googleapis.com``.
        page_token (str):
            The token of the page to retrieve.
        page_size (int):
            The max number of items to include in the
            response list. Page size is 50 if not specified.
            Maximum value is 100.
    """

    service_name = proto.Field(proto.STRING, number=1,)
    page_token = proto.Field(proto.STRING, number=2,)
    page_size = proto.Field(proto.INT32, number=3,)


class ListServiceConfigsResponse(proto.Message):
    r"""Response message for ListServiceConfigs method.
    Attributes:
        service_configs (Sequence[google.api.service_pb2.Service]):
            The list of service configuration resources.
        next_page_token (str):
            The token of the next page of results.
    """

    @property
    def raw_page(self):
        return self

    service_configs = proto.RepeatedField(
        proto.MESSAGE, number=1, message=service_pb2.Service,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class CreateServiceConfigRequest(proto.Message):
    r"""Request message for CreateServiceConfig method.
    Attributes:
        service_name (str):
            Required. The name of the service. See the
            `overview <https://cloud.google.com/service-management/overview>`__
            for naming requirements. For example:
            ``example.googleapis.com``.
        service_config (google.api.service_pb2.Service):
            Required. The service configuration resource.
    """

    service_name = proto.Field(proto.STRING, number=1,)
    service_config = proto.Field(proto.MESSAGE, number=2, message=service_pb2.Service,)


class SubmitConfigSourceRequest(proto.Message):
    r"""Request message for SubmitConfigSource method.
    Attributes:
        service_name (str):
            Required. The name of the service. See the
            `overview <https://cloud.google.com/service-management/overview>`__
            for naming requirements. For example:
            ``example.googleapis.com``.
        config_source (google.cloud.servicemanagement_v1.types.ConfigSource):
            Required. The source configuration for the
            service.
        validate_only (bool):
            Optional. If set, this will result in the generation of a
            ``google.api.Service`` configuration based on the
            ``ConfigSource`` provided, but the generated config and the
            sources will NOT be persisted.
    """

    service_name = proto.Field(proto.STRING, number=1,)
    config_source = proto.Field(
        proto.MESSAGE, number=2, message=resources.ConfigSource,
    )
    validate_only = proto.Field(proto.BOOL, number=3,)


class SubmitConfigSourceResponse(proto.Message):
    r"""Response message for SubmitConfigSource method.
    Attributes:
        service_config (google.api.service_pb2.Service):
            The generated service configuration.
    """

    service_config = proto.Field(proto.MESSAGE, number=1, message=service_pb2.Service,)


class CreateServiceRolloutRequest(proto.Message):
    r"""Request message for 'CreateServiceRollout'
    Attributes:
        service_name (str):
            Required. The name of the service. See the
            `overview <https://cloud.google.com/service-management/overview>`__
            for naming requirements. For example:
            ``example.googleapis.com``.
        rollout (google.cloud.servicemanagement_v1.types.Rollout):
            Required. The rollout resource. The ``service_name`` field
            is output only.
    """

    service_name = proto.Field(proto.STRING, number=1,)
    rollout = proto.Field(proto.MESSAGE, number=2, message=resources.Rollout,)


class ListServiceRolloutsRequest(proto.Message):
    r"""Request message for 'ListServiceRollouts'
    Attributes:
        service_name (str):
            Required. The name of the service. See the
            `overview <https://cloud.google.com/service-management/overview>`__
            for naming requirements. For example:
            ``example.googleapis.com``.
        page_token (str):
            The token of the page to retrieve.
        page_size (int):
            The max number of items to include in the
            response list. Page size is 50 if not specified.
            Maximum value is 100.
        filter (str):
            Required. Use ``filter`` to return subset of rollouts. The
            following filters are supported: -- To limit the results to
            only those in status
            (google.api.servicemanagement.v1.RolloutStatus) 'SUCCESS',
            use filter='status=SUCCESS' -- To limit the results to those
            in status (google.api.servicemanagement.v1.RolloutStatus)
            'CANCELLED' or 'FAILED', use filter='status=CANCELLED OR
            status=FAILED'
    """

    service_name = proto.Field(proto.STRING, number=1,)
    page_token = proto.Field(proto.STRING, number=2,)
    page_size = proto.Field(proto.INT32, number=3,)
    filter = proto.Field(proto.STRING, number=4,)


class ListServiceRolloutsResponse(proto.Message):
    r"""Response message for ListServiceRollouts method.
    Attributes:
        rollouts (Sequence[google.cloud.servicemanagement_v1.types.Rollout]):
            The list of rollout resources.
        next_page_token (str):
            The token of the next page of results.
    """

    @property
    def raw_page(self):
        return self

    rollouts = proto.RepeatedField(proto.MESSAGE, number=1, message=resources.Rollout,)
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetServiceRolloutRequest(proto.Message):
    r"""Request message for GetServiceRollout method.
    Attributes:
        service_name (str):
            Required. The name of the service. See the
            `overview <https://cloud.google.com/service-management/overview>`__
            for naming requirements. For example:
            ``example.googleapis.com``.
        rollout_id (str):
            Required. The id of the rollout resource.
    """

    service_name = proto.Field(proto.STRING, number=1,)
    rollout_id = proto.Field(proto.STRING, number=2,)


class EnableServiceRequest(proto.Message):
    r"""Request message for EnableService method.
    Attributes:
        service_name (str):
            Required. Name of the service to enable.
            Specifying an unknown service name will cause
            the request to fail.
        consumer_id (str):
            Required. The identity of consumer resource which service
            enablement will be applied to.

            The Google Service Management implementation accepts the
            following forms:

            -  "project:<project_id>"

            Note: this is made compatible with
            google.api.servicecontrol.v1.Operation.consumer_id.
    """

    service_name = proto.Field(proto.STRING, number=1,)
    consumer_id = proto.Field(proto.STRING, number=2,)


class EnableServiceResponse(proto.Message):
    r"""Operation payload for EnableService method.    """


class DisableServiceRequest(proto.Message):
    r"""Request message for DisableService method.
    Attributes:
        service_name (str):
            Required. Name of the service to disable.
            Specifying an unknown service name will cause
            the request to fail.
        consumer_id (str):
            Required. The identity of consumer resource which service
            disablement will be applied to.

            The Google Service Management implementation accepts the
            following forms:

            -  "project:<project_id>"

            Note: this is made compatible with
            google.api.servicecontrol.v1.Operation.consumer_id.
    """

    service_name = proto.Field(proto.STRING, number=1,)
    consumer_id = proto.Field(proto.STRING, number=2,)


class DisableServiceResponse(proto.Message):
    r"""Operation payload for DisableService method.    """


class GenerateConfigReportRequest(proto.Message):
    r"""Request message for GenerateConfigReport method.
    Attributes:
        new_config (google.protobuf.any_pb2.Any):
            Required. Service configuration for which we want to
            generate the report. For this version of API, the supported
            types are
            [google.api.servicemanagement.v1.ConfigRef][google.api.servicemanagement.v1.ConfigRef],
            [google.api.servicemanagement.v1.ConfigSource][google.api.servicemanagement.v1.ConfigSource],
            and [google.api.Service][google.api.Service]
        old_config (google.protobuf.any_pb2.Any):
            Optional. Service configuration against which the comparison
            will be done. For this version of API, the supported types
            are
            [google.api.servicemanagement.v1.ConfigRef][google.api.servicemanagement.v1.ConfigRef],
            [google.api.servicemanagement.v1.ConfigSource][google.api.servicemanagement.v1.ConfigSource],
            and [google.api.Service][google.api.Service]
    """

    new_config = proto.Field(proto.MESSAGE, number=1, message=any_pb2.Any,)
    old_config = proto.Field(proto.MESSAGE, number=2, message=any_pb2.Any,)


class GenerateConfigReportResponse(proto.Message):
    r"""Response message for GenerateConfigReport method.
    Attributes:
        service_name (str):
            Name of the service this report belongs to.
        id (str):
            ID of the service configuration this report
            belongs to.
        change_reports (Sequence[google.cloud.servicemanagement_v1.types.ChangeReport]):
            list of ChangeReport, each corresponding to
            comparison between two service configurations.
        diagnostics (Sequence[google.cloud.servicemanagement_v1.types.Diagnostic]):
            Errors / Linter warnings associated with the
            service definition this report
            belongs to.
    """

    service_name = proto.Field(proto.STRING, number=1,)
    id = proto.Field(proto.STRING, number=2,)
    change_reports = proto.RepeatedField(
        proto.MESSAGE, number=3, message=resources.ChangeReport,
    )
    diagnostics = proto.RepeatedField(
        proto.MESSAGE, number=4, message=resources.Diagnostic,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
