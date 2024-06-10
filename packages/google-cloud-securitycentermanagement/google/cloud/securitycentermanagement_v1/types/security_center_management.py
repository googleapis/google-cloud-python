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

from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from google.type import expr_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.securitycentermanagement.v1",
    manifest={
        "SecurityCenterService",
        "EffectiveSecurityHealthAnalyticsCustomModule",
        "ListEffectiveSecurityHealthAnalyticsCustomModulesRequest",
        "ListEffectiveSecurityHealthAnalyticsCustomModulesResponse",
        "GetEffectiveSecurityHealthAnalyticsCustomModuleRequest",
        "SecurityHealthAnalyticsCustomModule",
        "CustomConfig",
        "ListSecurityHealthAnalyticsCustomModulesRequest",
        "ListSecurityHealthAnalyticsCustomModulesResponse",
        "ListDescendantSecurityHealthAnalyticsCustomModulesRequest",
        "ListDescendantSecurityHealthAnalyticsCustomModulesResponse",
        "GetSecurityHealthAnalyticsCustomModuleRequest",
        "CreateSecurityHealthAnalyticsCustomModuleRequest",
        "UpdateSecurityHealthAnalyticsCustomModuleRequest",
        "DeleteSecurityHealthAnalyticsCustomModuleRequest",
        "SimulateSecurityHealthAnalyticsCustomModuleRequest",
        "SimulatedFinding",
        "SimulateSecurityHealthAnalyticsCustomModuleResponse",
        "EffectiveEventThreatDetectionCustomModule",
        "ListEffectiveEventThreatDetectionCustomModulesRequest",
        "ListEffectiveEventThreatDetectionCustomModulesResponse",
        "GetEffectiveEventThreatDetectionCustomModuleRequest",
        "EventThreatDetectionCustomModule",
        "ListEventThreatDetectionCustomModulesRequest",
        "ListEventThreatDetectionCustomModulesResponse",
        "ListDescendantEventThreatDetectionCustomModulesRequest",
        "ListDescendantEventThreatDetectionCustomModulesResponse",
        "GetEventThreatDetectionCustomModuleRequest",
        "CreateEventThreatDetectionCustomModuleRequest",
        "UpdateEventThreatDetectionCustomModuleRequest",
        "DeleteEventThreatDetectionCustomModuleRequest",
        "ValidateEventThreatDetectionCustomModuleRequest",
        "ValidateEventThreatDetectionCustomModuleResponse",
        "GetSecurityCenterServiceRequest",
        "ListSecurityCenterServicesRequest",
        "ListSecurityCenterServicesResponse",
        "UpdateSecurityCenterServiceRequest",
    },
)


class SecurityCenterService(proto.Message):
    r"""Represents a particular Security Command Center service. This
    includes settings information such as top-level enablement in
    addition to individual module settings. Service settings can be
    configured at the organization, folder, or project level.
    Service settings at the organization or folder level are
    inherited by those in child folders and projects.

    Attributes:
        name (str):
            Identifier. The name of the service.

            Its format is:

            -  organizations/{organization}/locations/{location}/securityCenterServices/{service}
            -  folders/{folder}/locations/{location}/securityCenterServices/{service}
            -  projects/{project}/locations/{location}/securityCenterServices/{service}

            The possible values for id {service} are:

            -  container-threat-detection
            -  event-threat-detection
            -  security-health-analytics
            -  vm-threat-detection
            -  web-security-scanner
        intended_enablement_state (google.cloud.securitycentermanagement_v1.types.SecurityCenterService.EnablementState):
            Optional. The intended state of enablement for the service
            at its level of the resource hierarchy. A DISABLED state
            will override all module enablement_states to DISABLED.
        effective_enablement_state (google.cloud.securitycentermanagement_v1.types.SecurityCenterService.EnablementState):
            Output only. The effective enablement state
            for the service at its level of the resource
            hierarchy. If the intended state is set to
            INHERITED, the effective state will be inherited
            from the enablement state of an ancestor. This
            state may differ from the intended enablement
            state due to billing eligibility or onboarding
            status.
        modules (MutableMapping[str, google.cloud.securitycentermanagement_v1.types.SecurityCenterService.ModuleSettings]):
            Optional. The configurations including the
            state of enablement for the service's different
            modules. The absence of a module in the map
            implies its configuration is inherited from its
            parents.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the service was last
            updated. This could be due to an explicit user
            update or due to a side effect of another system
            change such as billing subscription expiry.
        service_config (google.protobuf.struct_pb2.Struct):
            Optional. Additional service specific
            configuration. Not all services will utilize
            this field.
    """

    class EnablementState(proto.Enum):
        r"""Represents the possible intended states of enablement for a
        service or module.

        Values:
            ENABLEMENT_STATE_UNSPECIFIED (0):
                Default value. This value is unused.
            INHERITED (1):
                State is inherited from the parent resource.
                Not a valid effective enablement state.
            ENABLED (2):
                State is enabled.
            DISABLED (3):
                State is disabled.
            INGEST_ONLY (4):
                SCC is configured to ingest findings from this service but
                not enable this service. Not a valid
                intended_enablement_state (that is, this is a readonly
                state).
        """
        ENABLEMENT_STATE_UNSPECIFIED = 0
        INHERITED = 1
        ENABLED = 2
        DISABLED = 3
        INGEST_ONLY = 4

    class ModuleSettings(proto.Message):
        r"""The settings for individual modules.

        Attributes:
            intended_enablement_state (google.cloud.securitycentermanagement_v1.types.SecurityCenterService.EnablementState):
                Optional. The intended state of enablement
                for the module at its level of the resource
                hierarchy.
            effective_enablement_state (google.cloud.securitycentermanagement_v1.types.SecurityCenterService.EnablementState):
                Output only. The effective enablement state
                for the module at its level of the resource
                hierarchy. If the intended state is set to
                INHERITED, the effective state will be inherited
                from the enablement state of an ancestor. This
                state may
                differ from the intended enablement state due to
                billing eligibility or onboarding status.
        """

        intended_enablement_state: "SecurityCenterService.EnablementState" = (
            proto.Field(
                proto.ENUM,
                number=1,
                enum="SecurityCenterService.EnablementState",
            )
        )
        effective_enablement_state: "SecurityCenterService.EnablementState" = (
            proto.Field(
                proto.ENUM,
                number=2,
                enum="SecurityCenterService.EnablementState",
            )
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    intended_enablement_state: EnablementState = proto.Field(
        proto.ENUM,
        number=2,
        enum=EnablementState,
    )
    effective_enablement_state: EnablementState = proto.Field(
        proto.ENUM,
        number=3,
        enum=EnablementState,
    )
    modules: MutableMapping[str, ModuleSettings] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=4,
        message=ModuleSettings,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    service_config: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=6,
        message=struct_pb2.Struct,
    )


class EffectiveSecurityHealthAnalyticsCustomModule(proto.Message):
    r"""An EffectiveSecurityHealthAnalyticsCustomModule is the
    representation of a Security Health Analytics custom module at a
    specified level of the resource hierarchy: organization, folder, or
    project. If a custom module is inherited from a parent organization
    or folder, the value of the ``enablementState`` property in
    EffectiveSecurityHealthAnalyticsCustomModule is set to the value
    that is effective in the parent, instead of ``INHERITED``. For
    example, if the module is enabled in a parent organization or
    folder, the effective enablement_state for the module in all child
    folders or projects is also ``enabled``.
    EffectiveSecurityHealthAnalyticsCustomModule is read-only.

    Attributes:
        name (str):
            Identifier. The full resource name of the custom module,
            specified in one of the following formats:

            -  ``organizations/organization/{location}/effectiveSecurityHealthAnalyticsCustomModules/{effective_security_health_analytics_custom_module}``
            -  ``folders/folder/{location}/effectiveSecurityHealthAnalyticsCustomModules/{effective_security_health_analytics_custom_module}``
            -  ``projects/project/{location}/effectiveSecurityHealthAnalyticsCustomModules/{effective_security_health_analytics_custom_module}``
        custom_config (google.cloud.securitycentermanagement_v1.types.CustomConfig):
            Output only. The user-specified configuration
            for the module.
        enablement_state (google.cloud.securitycentermanagement_v1.types.EffectiveSecurityHealthAnalyticsCustomModule.EnablementState):
            Output only. The effective state of
            enablement for the module at the given level of
            the hierarchy.
        display_name (str):
            Output only. The display name for the custom
            module. The name must be between 1 and 128
            characters, start with a lowercase letter, and
            contain alphanumeric characters or underscores
            only.
    """

    class EnablementState(proto.Enum):
        r"""The enablement state of the module.

        Values:
            ENABLEMENT_STATE_UNSPECIFIED (0):
                Unspecified enablement state.
            ENABLED (1):
                The module is enabled at the given level.
            DISABLED (2):
                The module is disabled at the given level.
        """
        ENABLEMENT_STATE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    custom_config: "CustomConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="CustomConfig",
    )
    enablement_state: EnablementState = proto.Field(
        proto.ENUM,
        number=3,
        enum=EnablementState,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListEffectiveSecurityHealthAnalyticsCustomModulesRequest(proto.Message):
    r"""Request message for listing effective Security Health
    Analytics custom modules.

    Attributes:
        parent (str):
            Required. Name of parent to list effective custom modules.
            specified in one of the following formats:

            -  ``organizations/{organization}/locations/{location}``
            -  ``folders/{folder}/locations/{location}`` or
               ``projects/{project}/locations/{location}``
        page_size (int):
            Optional. The maximum number of results to
            return in a single response. Default is 10,
            minimum is 1, maximum is 1000.
        page_token (str):
            Optional. The value returned by the last call
            indicating a continuation.
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


class ListEffectiveSecurityHealthAnalyticsCustomModulesResponse(proto.Message):
    r"""Response message for listing effective Security Health
    Analytics custom modules.

    Attributes:
        effective_security_health_analytics_custom_modules (MutableSequence[google.cloud.securitycentermanagement_v1.types.EffectiveSecurityHealthAnalyticsCustomModule]):
            The list of
            EffectiveSecurityHealthAnalyticsCustomModule
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    effective_security_health_analytics_custom_modules: MutableSequence[
        "EffectiveSecurityHealthAnalyticsCustomModule"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="EffectiveSecurityHealthAnalyticsCustomModule",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetEffectiveSecurityHealthAnalyticsCustomModuleRequest(proto.Message):
    r"""Message for getting a
    EffectiveSecurityHealthAnalyticsCustomModule

    Attributes:
        name (str):
            Required. The full resource name of the custom module,
            specified in one of the following formats:

            -  ``organizations/organization/{location}/effectiveSecurityHealthAnalyticsCustomModules/{effective_security_health_analytics_custom_module}``
            -  ``folders/folder/{location}/effectiveSecurityHealthAnalyticsCustomModules/{effective_security_health_analytics_custom_module}``
            -  ``projects/project/{location}/effectiveSecurityHealthAnalyticsCustomModules/{effective_security_health_analytics_custom_module}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class SecurityHealthAnalyticsCustomModule(proto.Message):
    r"""Represents an instance of a Security Health Analytics custom
    module, including its full module name, display name, enablement
    state, and last updated time. You can create a custom module at
    the organization, folder, or project level. Custom modules that
    you create at the organization or folder level are inherited by
    the child folders and projects.

    Attributes:
        name (str):
            Identifier. The full resource name of the custom module,
            specified in one of the following formats:

            -  ``organizations/{organization}/locations/{location}/securityHealthAnalyticsCustomModules/{security_health_analytics_custom_module}``
            -  ``folders/{folder}/locations/{location}/securityHealthAnalyticsCustomModules/{security_health_analytics_custom_module}``
            -  ``projects/{project}/locations/{location}/securityHealthAnalyticsCustomModules/{security_health_analytics_custom_module}``
        display_name (str):
            Optional. The display name of the Security
            Health Analytics custom module. This display
            name becomes the finding category for all
            findings that are returned by this custom
            module. The display name must be between 1 and
            128 characters, start with a lowercase letter,
            and contain alphanumeric characters or
            underscores only.
        enablement_state (google.cloud.securitycentermanagement_v1.types.SecurityHealthAnalyticsCustomModule.EnablementState):
            Optional. The enablement state of the custom
            module.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the custom
            module was last updated.
        last_editor (str):
            Output only. The editor that last updated the
            custom module.
        ancestor_module (str):
            Output only. Specifies the organization or
            folder from which the custom module is
            inherited. If empty, indicates that the custom
            module was created in the organization, folder,
            or project in which you are viewing the custom
            module.
        custom_config (google.cloud.securitycentermanagement_v1.types.CustomConfig):
            Optional. The user specified custom
            configuration for the module.
    """

    class EnablementState(proto.Enum):
        r"""Possible enablement states of a custom module.

        Values:
            ENABLEMENT_STATE_UNSPECIFIED (0):
                Unspecified enablement state.
            ENABLED (1):
                The module is enabled at the given CRM
                resource.
            DISABLED (2):
                The module is disabled at the given CRM
                resource.
            INHERITED (3):
                State is inherited from an ancestor module. The module will
                either be effectively ENABLED or DISABLED based on its
                closest non-inherited ancestor module in the CRM hierarchy.
                Attempting to set a top level module (module with no parent)
                to the INHERITED state will result in an INVALID_ARGUMENT
                error.
        """
        ENABLEMENT_STATE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2
        INHERITED = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    enablement_state: EnablementState = proto.Field(
        proto.ENUM,
        number=3,
        enum=EnablementState,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    last_editor: str = proto.Field(
        proto.STRING,
        number=5,
    )
    ancestor_module: str = proto.Field(
        proto.STRING,
        number=6,
    )
    custom_config: "CustomConfig" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="CustomConfig",
    )


class CustomConfig(proto.Message):
    r"""Defines the properties in a custom module configuration for
    Security Health Analytics. Use the custom module configuration
    to create custom detectors that generate custom findings for
    resources that you specify.

    Attributes:
        predicate (google.type.expr_pb2.Expr):
            Optional. The CEL expression to evaluate to
            produce findings. When the expression evaluates
            to true against a resource, a finding is
            generated.
        custom_output (google.cloud.securitycentermanagement_v1.types.CustomConfig.CustomOutputSpec):
            Optional. Custom output properties.
        resource_selector (google.cloud.securitycentermanagement_v1.types.CustomConfig.ResourceSelector):
            Optional. The Cloud Asset Inventory resource types that the
            custom module operates on. For information about resource
            types, see `Supported asset
            types <https://cloud.google.com/asset-inventory/docs/supported-asset-types>`__.
            Each custom module can specify up to 5 resource types.
        severity (google.cloud.securitycentermanagement_v1.types.CustomConfig.Severity):
            Optional. The severity to assign to findings
            generated by the module.
        description (str):
            Optional. Text that describes the
            vulnerability or misconfiguration that the
            custom module detects. This explanation is
            returned with each finding instance to help
            investigators understand the detected issue. The
            text must be enclosed in quotation marks.
        recommendation (str):
            Optional. An explanation of the recommended steps that
            security teams can take to resolve the detected issue. This
            explanation is returned with each finding generated by this
            module in the ``nextSteps`` property of the finding JSON.
    """

    class Severity(proto.Enum):
        r"""Defines the valid value options for the severity of a
        finding.

        Values:
            SEVERITY_UNSPECIFIED (0):
                Unspecified severity.
            CRITICAL (1):
                Critical severity.
            HIGH (2):
                High severity.
            MEDIUM (3):
                Medium severity.
            LOW (4):
                Low severity.
        """
        SEVERITY_UNSPECIFIED = 0
        CRITICAL = 1
        HIGH = 2
        MEDIUM = 3
        LOW = 4

    class CustomOutputSpec(proto.Message):
        r"""A set of optional name-value pairs that define custom source
        properties to return with each finding that is generated by the
        custom module. The custom source properties that are defined here
        are included in the finding JSON under ``sourceProperties``.

        Attributes:
            properties (MutableSequence[google.cloud.securitycentermanagement_v1.types.CustomConfig.CustomOutputSpec.Property]):
                Optional. A list of custom output properties
                to add to the finding.
        """

        class Property(proto.Message):
            r"""An individual name-value pair that defines a custom source
            property.

            Attributes:
                name (str):
                    Optional. Name of the property for the custom
                    output.
                value_expression (google.type.expr_pb2.Expr):
                    Optional. The CEL expression for the custom
                    output. A resource property can be specified to
                    return the value of the property or a text
                    string enclosed in quotation marks.
            """

            name: str = proto.Field(
                proto.STRING,
                number=1,
            )
            value_expression: expr_pb2.Expr = proto.Field(
                proto.MESSAGE,
                number=2,
                message=expr_pb2.Expr,
            )

        properties: MutableSequence[
            "CustomConfig.CustomOutputSpec.Property"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="CustomConfig.CustomOutputSpec.Property",
        )

    class ResourceSelector(proto.Message):
        r"""Resource for selecting resource type.

        Attributes:
            resource_types (MutableSequence[str]):
                Optional. The resource types to run the
                detector on.
        """

        resource_types: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )

    predicate: expr_pb2.Expr = proto.Field(
        proto.MESSAGE,
        number=1,
        message=expr_pb2.Expr,
    )
    custom_output: CustomOutputSpec = proto.Field(
        proto.MESSAGE,
        number=2,
        message=CustomOutputSpec,
    )
    resource_selector: ResourceSelector = proto.Field(
        proto.MESSAGE,
        number=3,
        message=ResourceSelector,
    )
    severity: Severity = proto.Field(
        proto.ENUM,
        number=4,
        enum=Severity,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    recommendation: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ListSecurityHealthAnalyticsCustomModulesRequest(proto.Message):
    r"""Request message for listing Security Health Analytics custom
    modules.

    Attributes:
        parent (str):
            Required. Name of parent organization, folder, or project in
            which to list custom modules, specified in one of the
            following formats:

            -  ``organizations/{organization}/locations/{location}``
            -  ``folders/{folder}/locations/{location}``
            -  ``projects/{project}/locations/{location}``
        page_size (int):
            Optional. The maximum number of results to
            return in a single response. Default is 10,
            minimum is 1, maximum is 1000.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
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


class ListSecurityHealthAnalyticsCustomModulesResponse(proto.Message):
    r"""Response message for listing Security Health Analytics custom
    modules.

    Attributes:
        security_health_analytics_custom_modules (MutableSequence[google.cloud.securitycentermanagement_v1.types.SecurityHealthAnalyticsCustomModule]):
            The list of
            SecurityHealthAnalyticsCustomModules
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    security_health_analytics_custom_modules: MutableSequence[
        "SecurityHealthAnalyticsCustomModule"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="SecurityHealthAnalyticsCustomModule",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListDescendantSecurityHealthAnalyticsCustomModulesRequest(proto.Message):
    r"""Request message for listing descendant Security Health
    Analytics custom modules.

    Attributes:
        parent (str):
            Required. Name of the parent organization, folder, or
            project in which to list custom modules, specified in one of
            the following formats:

            -  ``organizations/{organization}/locations/{location}``
            -  ``folders/{folder}/locations/{location}``
            -  ``projects/{project}/locations/{location}``
        page_size (int):
            Optional. The maximum number of results to
            return in a single response. Default is 10,
            minimum is 1, maximum is 1000.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
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


class ListDescendantSecurityHealthAnalyticsCustomModulesResponse(proto.Message):
    r"""Response message for listing descendant Security Health
    Analytics custom modules.

    Attributes:
        security_health_analytics_custom_modules (MutableSequence[google.cloud.securitycentermanagement_v1.types.SecurityHealthAnalyticsCustomModule]):
            The list of
            SecurityHealthAnalyticsCustomModules
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    security_health_analytics_custom_modules: MutableSequence[
        "SecurityHealthAnalyticsCustomModule"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="SecurityHealthAnalyticsCustomModule",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetSecurityHealthAnalyticsCustomModuleRequest(proto.Message):
    r"""Message for getting a SecurityHealthAnalyticsCustomModule

    Attributes:
        name (str):
            Required. Name of the resource
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateSecurityHealthAnalyticsCustomModuleRequest(proto.Message):
    r"""Message for creating a SecurityHealthAnalyticsCustomModule

    Attributes:
        parent (str):
            Required. Name of the parent organization, folder, or
            project of the module, specified in one of the following
            formats:

            -  ``organizations/{organization}/locations/{location}``
            -  ``folders/{folder}/locations/{location}``
            -  ``projects/{project}/locations/{location}``
        security_health_analytics_custom_module (google.cloud.securitycentermanagement_v1.types.SecurityHealthAnalyticsCustomModule):
            Required. The resource being created
        validate_only (bool):
            Optional. When set to true, only validations
            (including IAM checks) will done for the request
            (no module will be created). An OK response
            indicates the request is valid while an error
            response indicates the request is invalid. Note
            that a subsequent request to actually create the
            module could still fail because:

            - The state could have changed (e.g. IAM permission lost) or
            - A failure occurred during creation of the module. Defaults to false.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    security_health_analytics_custom_module: "SecurityHealthAnalyticsCustomModule" = (
        proto.Field(
            proto.MESSAGE,
            number=2,
            message="SecurityHealthAnalyticsCustomModule",
        )
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class UpdateSecurityHealthAnalyticsCustomModuleRequest(proto.Message):
    r"""Message for updating a SecurityHealthAnalyticsCustomModule

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. The only fields
            that can be updated are ``enablement_state`` and
            ``custom_config``. If empty or set to the wildcard value
            ``*``, both ``enablement_state`` and ``custom_config`` are
            updated.
        security_health_analytics_custom_module (google.cloud.securitycentermanagement_v1.types.SecurityHealthAnalyticsCustomModule):
            Required. The resource being updated
        validate_only (bool):
            Optional. When set to true, only validations
            (including IAM checks) will done for the request
            (module will not be updated). An OK response
            indicates the request is valid while an error
            response indicates the request is invalid. Note
            that a subsequent request to actually update the
            module could still fail because:

            - The state could have changed (e.g. IAM permission lost) or
            - A failure occurred while trying to update the module.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    security_health_analytics_custom_module: "SecurityHealthAnalyticsCustomModule" = (
        proto.Field(
            proto.MESSAGE,
            number=2,
            message="SecurityHealthAnalyticsCustomModule",
        )
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class DeleteSecurityHealthAnalyticsCustomModuleRequest(proto.Message):
    r"""Message for deleting a SecurityHealthAnalyticsCustomModule

    Attributes:
        name (str):
            Required. The resource name of the SHA custom module.

            Its format is:

            -  ``organizations/{organization}/locations/{location}/securityHealthAnalyticsCustomModules/{security_health_analytics_custom_module}``.
            -  ``folders/{folder}/locations/{location}/securityHealthAnalyticsCustomModules/{security_health_analytics_custom_module}``.
            -  ``projects/{project}/locations/{location}/securityHealthAnalyticsCustomModules/{security_health_analytics_custom_module}``.
        validate_only (bool):
            Optional. When set to true, only validations
            (including IAM checks) will done for the request
            (module will not be deleted). An OK response
            indicates the request is valid while an error
            response indicates the request is invalid. Note
            that a subsequent request to actually delete the
            module could still fail because:

            - The state could have changed (e.g. IAM permission lost) or
            - A failure occurred while trying to delete the module.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class SimulateSecurityHealthAnalyticsCustomModuleRequest(proto.Message):
    r"""Request message to simulate a CustomConfig against a given
    test resource. Maximum size of the request is 4 MB by default.

    Attributes:
        parent (str):
            Required. The relative resource name of the organization,
            project, or folder. For more information about relative
            resource names, see `Relative Resource
            Name <https://cloud.google.com/apis/design/resource_names#relative_resource_name>`__
            Example: ``organizations/{organization_id}``.
        custom_config (google.cloud.securitycentermanagement_v1.types.CustomConfig):
            Required. The custom configuration that you
            need to test.
        resource (google.cloud.securitycentermanagement_v1.types.SimulateSecurityHealthAnalyticsCustomModuleRequest.SimulatedResource):
            Required. Resource data to simulate custom
            module against.
    """

    class SimulatedResource(proto.Message):
        r"""Manually constructed resource name. If the custom module evaluates
        against only the resource data, you can omit the ``iam_policy_data``
        field. If it evaluates only the ``iam_policy_data`` field, you can
        omit the resource data.

        Attributes:
            resource_type (str):
                Required. The type of the resource, for example,
                ``compute.googleapis.com/Disk``.
            resource_data (google.protobuf.struct_pb2.Struct):
                Optional. A representation of the Google
                Cloud resource. Should match the Google Cloud
                resource JSON format.
            iam_policy_data (google.iam.v1.policy_pb2.Policy):
                Optional. A representation of the IAM policy.
        """

        resource_type: str = proto.Field(
            proto.STRING,
            number=1,
        )
        resource_data: struct_pb2.Struct = proto.Field(
            proto.MESSAGE,
            number=2,
            message=struct_pb2.Struct,
        )
        iam_policy_data: policy_pb2.Policy = proto.Field(
            proto.MESSAGE,
            number=3,
            message=policy_pb2.Policy,
        )

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    custom_config: "CustomConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="CustomConfig",
    )
    resource: SimulatedResource = proto.Field(
        proto.MESSAGE,
        number=3,
        message=SimulatedResource,
    )


class SimulatedFinding(proto.Message):
    r"""A subset of the fields of the Security Center Finding proto.
    The minimum set of fields needed to represent a simulated
    finding from a SHA custom module.

    Attributes:
        name (str):
            Identifier. The `relative resource
            name <https://cloud.google.com/apis/design/resource_names#relative_resource_name>`__
            of the finding. Example:
            ``organizations/{organization_id}/sources/{source_id}/findings/{finding_id}``,
            ``folders/{folder_id}/sources/{source_id}/findings/{finding_id}``,
            ``projects/{project_id}/sources/{source_id}/findings/{finding_id}``.
        parent (str):
            The relative resource name of the source the finding belongs
            to. See:
            https://cloud.google.com/apis/design/resource_names#relative_resource_name
            This field is immutable after creation time. For example:
            ``organizations/{organization_id}/sources/{source_id}``
        resource_name (str):
            For findings on Google Cloud resources, the full resource
            name of the Google Cloud resource this finding is for. See:
            https://cloud.google.com/apis/design/resource_names#full_resource_name
            When the finding is for a non-Google Cloud resource, the
            resourceName can be a customer or partner defined string.
            This field is immutable after creation time.
        category (str):
            The additional taxonomy group within findings from a given
            source. This field is immutable after creation time.
            Example: "XSS_FLASH_INJECTION".
        state (google.cloud.securitycentermanagement_v1.types.SimulatedFinding.State):
            Output only. The state of the finding.
        source_properties (MutableMapping[str, google.protobuf.struct_pb2.Value]):
            Source specific properties. These properties are managed by
            the source that writes the finding. The key names in the
            source_properties map must be between 1 and 255 characters,
            and must start with a letter and contain alphanumeric
            characters or underscores only.
        event_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the finding was first detected. If
            an existing finding is updated, then this is the
            time the update occurred. For example, if the
            finding represents an open firewall, this
            property captures the time the detector believes
            the firewall became open. The accuracy is
            determined by the detector. If the finding is
            later resolved, then this time reflects when the
            finding was resolved. This must not be set to a
            value greater than the current timestamp.
        severity (google.cloud.securitycentermanagement_v1.types.SimulatedFinding.Severity):
            The severity of the finding. This field is
            managed by the source that writes the finding.
        finding_class (google.cloud.securitycentermanagement_v1.types.SimulatedFinding.FindingClass):
            The class of the finding.
    """

    class State(proto.Enum):
        r"""The state of the finding.

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified state.
            ACTIVE (1):
                The finding requires attention and has not
                been addressed yet.
            INACTIVE (2):
                The finding has been fixed, triaged as a
                non-issue or otherwise addressed and is no
                longer active.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        INACTIVE = 2

    class Severity(proto.Enum):
        r"""The severity of the finding.

        Values:
            SEVERITY_UNSPECIFIED (0):
                This value is used for findings when a source
                doesn't write a severity value.
            CRITICAL (1):
                Vulnerability:

                A critical vulnerability is easily discoverable
                by an external actor, exploitable, and results
                in the direct ability to execute arbitrary code,
                exfiltrate data, and otherwise gain additional
                access and privileges to cloud resources and
                workloads. Examples include publicly accessible
                unprotected user data and public SSH access with
                weak or no passwords.

                Threat:

                Indicates a threat that is able to access,
                modify, or delete data or execute unauthorized
                code within existing resources.
            HIGH (2):
                Vulnerability:

                A high risk vulnerability can be easily
                discovered and exploited in combination with
                other vulnerabilities in order to gain direct
                access and the ability to execute arbitrary
                code, exfiltrate data, and otherwise gain
                additional access and privileges to cloud
                resources and workloads. An example is a
                database with weak or no passwords that is only
                accessible internally. This database could
                easily be compromised by an actor that had
                access to the internal network.

                Threat:

                Indicates a threat that is able to create new
                computational resources in an environment but
                not able to access data or execute code in
                existing resources.
            MEDIUM (3):
                Vulnerability:

                A medium risk vulnerability could be used by an
                actor to gain access to resources or privileges
                that enable them to eventually (through multiple
                steps or a complex exploit) gain access and the
                ability to execute arbitrary code or exfiltrate
                data. An example is a service account with
                access to more projects than it should have. If
                an actor gains access to the service account,
                they could potentially use that access to
                manipulate a project the service account was not
                intended to.

                Threat:

                Indicates a threat that is able to cause
                operational impact but may not access data or
                execute unauthorized code.
            LOW (4):
                Vulnerability:

                A low risk vulnerability hampers a security
                organization's ability to detect vulnerabilities
                or active threats in their deployment, or
                prevents the root cause investigation of
                security issues. An example is monitoring and
                logs being disabled for resource configurations
                and access.

                Threat:

                Indicates a threat that has obtained minimal
                access to an environment but is not able to
                access data, execute code, or create resources.
        """
        SEVERITY_UNSPECIFIED = 0
        CRITICAL = 1
        HIGH = 2
        MEDIUM = 3
        LOW = 4

    class FindingClass(proto.Enum):
        r"""Represents what kind of Finding it is.

        Values:
            FINDING_CLASS_UNSPECIFIED (0):
                Unspecified finding class.
            THREAT (1):
                Describes unwanted or malicious activity.
            VULNERABILITY (2):
                Describes a potential weakness in software
                that increases risk to Confidentiality &
                Integrity & Availability.
            MISCONFIGURATION (3):
                Describes a potential weakness in cloud
                resource/asset configuration that increases
                risk.
            OBSERVATION (4):
                Describes a security observation that is for
                informational purposes.
            SCC_ERROR (5):
                Describes an error that prevents some SCC
                functionality.
            POSTURE_VIOLATION (6):
                Describes a potential security risk due to a
                change in the security posture.
            TOXIC_COMBINATION (7):
                Describes a combination of security issues
                that represent a more severe security problem
                when taken together.
        """
        FINDING_CLASS_UNSPECIFIED = 0
        THREAT = 1
        VULNERABILITY = 2
        MISCONFIGURATION = 3
        OBSERVATION = 4
        SCC_ERROR = 5
        POSTURE_VIOLATION = 6
        TOXIC_COMBINATION = 7

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    parent: str = proto.Field(
        proto.STRING,
        number=2,
    )
    resource_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    category: str = proto.Field(
        proto.STRING,
        number=4,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    source_properties: MutableMapping[str, struct_pb2.Value] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=6,
        message=struct_pb2.Value,
    )
    event_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    severity: Severity = proto.Field(
        proto.ENUM,
        number=8,
        enum=Severity,
    )
    finding_class: FindingClass = proto.Field(
        proto.ENUM,
        number=9,
        enum=FindingClass,
    )


class SimulateSecurityHealthAnalyticsCustomModuleResponse(proto.Message):
    r"""Response message for simulating a
    ``SecurityHealthAnalyticsCustomModule`` against a given resource.

    Attributes:
        result (google.cloud.securitycentermanagement_v1.types.SimulateSecurityHealthAnalyticsCustomModuleResponse.SimulatedResult):
            Result for test case in the corresponding
            request.
    """

    class SimulatedResult(proto.Message):
        r"""Possible test result.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            finding (google.cloud.securitycentermanagement_v1.types.SimulatedFinding):
                Finding that would be published for the test
                case, if a violation is detected.

                This field is a member of `oneof`_ ``result``.
            no_violation (google.protobuf.empty_pb2.Empty):
                Indicates that the test case does not trigger
                any violation.

                This field is a member of `oneof`_ ``result``.
            error (google.rpc.status_pb2.Status):
                Error encountered during the test.

                This field is a member of `oneof`_ ``result``.
        """

        finding: "SimulatedFinding" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="result",
            message="SimulatedFinding",
        )
        no_violation: empty_pb2.Empty = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="result",
            message=empty_pb2.Empty,
        )
        error: status_pb2.Status = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="result",
            message=status_pb2.Status,
        )

    result: SimulatedResult = proto.Field(
        proto.MESSAGE,
        number=1,
        message=SimulatedResult,
    )


class EffectiveEventThreatDetectionCustomModule(proto.Message):
    r"""An EffectiveEventThreatDetectionCustomModule is the representation
    of EventThreatDetectionCustomModule at a given level taking
    hierarchy into account and resolving various fields accordingly.
    e.g. if the module is enabled at the ancestor level, effective
    modules at all descendant levels will have enablement_state set to
    ENABLED. Similarly, if module.inherited is set, then effective
    module's config will contain the ancestor's config details.
    EffectiveEventThreatDetectionCustomModule is read-only.

    Attributes:
        name (str):
            Identifier. The resource name of the ETD custom module.

            Its format is:

            -  ``organizations/{organization}/locations/{location}/effectiveEventThreatDetectionCustomModules/{effective_event_threat_detection_custom_module}``.
            -  ``folders/{folder}/locations/{location}/effectiveEventThreatDetectionCustomModules/{effective_event_threat_detection_custom_module}``.
            -  ``projects/{project}/locations/{location}/effectiveEventThreatDetectionCustomModules/{effective_event_threat_detection_custom_module}``.
        config (google.protobuf.struct_pb2.Struct):
            Output only. Config for the effective module.
        enablement_state (google.cloud.securitycentermanagement_v1.types.EffectiveEventThreatDetectionCustomModule.EnablementState):
            Output only. The effective state of
            enablement for the module at the given level of
            the hierarchy.
        type_ (str):
            Output only. Type for the module. e.g. CONFIGURABLE_BAD_IP.
        display_name (str):
            Output only. The human readable name to be
            displayed for the module.
        description (str):
            Output only. The description for the module.
    """

    class EnablementState(proto.Enum):
        r"""The enablement state of the module.

        Values:
            ENABLEMENT_STATE_UNSPECIFIED (0):
                Unspecified enablement state.
            ENABLED (1):
                The module is enabled at the given level.
            DISABLED (2):
                The module is disabled at the given level.
        """
        ENABLEMENT_STATE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    config: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=2,
        message=struct_pb2.Struct,
    )
    enablement_state: EnablementState = proto.Field(
        proto.ENUM,
        number=3,
        enum=EnablementState,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=4,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    description: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ListEffectiveEventThreatDetectionCustomModulesRequest(proto.Message):
    r"""Request message for listing effective Event Threat Detection
    custom modules.

    Attributes:
        parent (str):
            Required. Name of parent to list effective custom modules.
            Its format is
            ``organizations/{organization}/locations/{location}``,
            ``folders/{folder}/locations/{location}``, or
            ``projects/{project}/locations/{location}``
        page_size (int):
            Optional. The maximum number of results to
            return in a single response. Default is 10,
            minimum is 1, maximum is 1000.
        page_token (str):
            Optional. The value returned by the last call
            indicating a continuation
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


class ListEffectiveEventThreatDetectionCustomModulesResponse(proto.Message):
    r"""Response message for listing effective Event Threat Detection
    custom modules.

    Attributes:
        effective_event_threat_detection_custom_modules (MutableSequence[google.cloud.securitycentermanagement_v1.types.EffectiveEventThreatDetectionCustomModule]):
            The list of
            EffectiveEventThreatDetectionCustomModules
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    effective_event_threat_detection_custom_modules: MutableSequence[
        "EffectiveEventThreatDetectionCustomModule"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="EffectiveEventThreatDetectionCustomModule",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetEffectiveEventThreatDetectionCustomModuleRequest(proto.Message):
    r"""Message for getting a
    EffectiveEventThreatDetectionCustomModule

    Attributes:
        name (str):
            Required. The resource name of the ETD custom module.

            Its format is:

            -  ``organizations/{organization}/locations/{location}/effectiveEventThreatDetectionCustomModules/{effective_event_threat_detection_custom_module}``.
            -  ``folders/{folder}/locations/{location}/effectiveEventThreatDetectionCustomModules/{effective_event_threat_detection_custom_module}``.
            -  ``projects/{project}/locations/{location}/effectiveEventThreatDetectionCustomModules/{effective_event_threat_detection_custom_module}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class EventThreatDetectionCustomModule(proto.Message):
    r"""An event threat detection custom module is a Cloud SCC
    resource that contains the configuration and enablement state of
    a custom module, which enables ETD to write certain findings to
    Cloud SCC.

    Attributes:
        name (str):
            Identifier. The resource name of the ETD custom module.

            Its format is:

            -  ``organizations/{organization}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.
            -  ``folders/{folder}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.
            -  ``projects/{project}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.
        config (google.protobuf.struct_pb2.Struct):
            Optional. Config for the module. For the
            resident module, its config value is defined at
            this level. For the inherited module, its config
            value is inherited from the ancestor module.
        ancestor_module (str):
            Output only. The closest ancestor module that
            this module inherits the enablement state from.
            If empty, indicates that the custom module was
            created in the requesting parent organization,
            folder, or project. The format is the same as
            the EventThreatDetectionCustomModule resource
            name.
        enablement_state (google.cloud.securitycentermanagement_v1.types.EventThreatDetectionCustomModule.EnablementState):
            Optional. The state of enablement for the
            module at the given level of the hierarchy.
        type_ (str):
            Optional. Type for the module. e.g. CONFIGURABLE_BAD_IP.
        display_name (str):
            Optional. The human readable name to be
            displayed for the module.
        description (str):
            Optional. The description for the module.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the module was last
            updated.
        last_editor (str):
            Output only. The editor the module was last
            updated by.
    """

    class EnablementState(proto.Enum):
        r"""The enablement state of the module.

        Values:
            ENABLEMENT_STATE_UNSPECIFIED (0):
                Unspecified enablement state.
            ENABLED (1):
                The module is enabled at the given level.
            DISABLED (2):
                The module is disabled at the given level.
            INHERITED (3):
                State is inherited from an ancestor module.
                The module will either be effectively ENABLED or
                DISABLED based on its closest non-inherited
                ancestor module in the CRM hierarchy. Attempting
                to set a top level module (module with no
                parent) to the INHERITED state will result in an
                error.
        """
        ENABLEMENT_STATE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2
        INHERITED = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    config: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=2,
        message=struct_pb2.Struct,
    )
    ancestor_module: str = proto.Field(
        proto.STRING,
        number=3,
    )
    enablement_state: EnablementState = proto.Field(
        proto.ENUM,
        number=4,
        enum=EnablementState,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=5,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=6,
    )
    description: str = proto.Field(
        proto.STRING,
        number=7,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    last_editor: str = proto.Field(
        proto.STRING,
        number=9,
    )


class ListEventThreatDetectionCustomModulesRequest(proto.Message):
    r"""Request message for listing Event Threat Detection custom
    modules.

    Attributes:
        parent (str):
            Required. Name of parent to list custom modules. Its format
            is ``organizations/{organization}/locations/{location}``,
            ``folders/{folder}/locations/{location}``, or
            ``projects/{project}/locations/{location}``
        page_size (int):
            Optional. The maximum number of modules to
            return. The service may return fewer than this
            value. If unspecified, at most 10 configs will
            be returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListEventThreatDetectionCustomModules`` call. Provide this
            to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListEventThreatDetectionCustomModules`` must match the
            call that provided the page token.
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


class ListEventThreatDetectionCustomModulesResponse(proto.Message):
    r"""Response message for listing Event Threat Detection custom
    modules.

    Attributes:
        event_threat_detection_custom_modules (MutableSequence[google.cloud.securitycentermanagement_v1.types.EventThreatDetectionCustomModule]):
            The list of EventThreatDetectionCustomModules
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    event_threat_detection_custom_modules: MutableSequence[
        "EventThreatDetectionCustomModule"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="EventThreatDetectionCustomModule",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListDescendantEventThreatDetectionCustomModulesRequest(proto.Message):
    r"""Request message for listing descendant Event Threat Detection
    custom modules.

    Attributes:
        parent (str):
            Required. Name of parent to list custom modules. Its format
            is ``organizations/{organization}/locations/{location}``,
            ``folders/{folder}/locations/{location}``, or
            ``projects/{project}/locations/{location}``
        page_size (int):
            Optional. The maximum number of modules to
            return. The service may return fewer than this
            value. If unspecified, at most 10 configs will
            be returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
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


class ListDescendantEventThreatDetectionCustomModulesResponse(proto.Message):
    r"""Response message for listing descendant Event Threat
    Detection custom modules.

    Attributes:
        event_threat_detection_custom_modules (MutableSequence[google.cloud.securitycentermanagement_v1.types.EventThreatDetectionCustomModule]):
            The list of EventThreatDetectionCustomModules
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    event_threat_detection_custom_modules: MutableSequence[
        "EventThreatDetectionCustomModule"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="EventThreatDetectionCustomModule",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetEventThreatDetectionCustomModuleRequest(proto.Message):
    r"""Message for getting a EventThreatDetectionCustomModule

    Attributes:
        name (str):
            Required. The resource name of the ETD custom module.

            Its format is:

            -  ``organizations/{organization}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.
            -  ``folders/{folder}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.
            -  ``projects/{project}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateEventThreatDetectionCustomModuleRequest(proto.Message):
    r"""Message for creating a EventThreatDetectionCustomModule

    Attributes:
        parent (str):
            Required. Name of parent for the module. Its format is
            ``organizations/{organization}/locations/{location}``,
            ``folders/{folder}/locations/{location}``, or
            ``projects/{project}/locations/{location}``
        event_threat_detection_custom_module (google.cloud.securitycentermanagement_v1.types.EventThreatDetectionCustomModule):
            Required. The module to create. The
            event_threat_detection_custom_module.name will be ignored
            and server generated.
        validate_only (bool):
            Optional. When set to true, only validations
            (including IAM checks) will done for the request
            (no module will be created). An OK response
            indicates the request is valid while an error
            response indicates the request is invalid. Note
            that a subsequent request to actually create the
            module could still fail because:

            - The state could have changed (e.g. IAM permission lost) or
            - A failure occurred during creation of the module.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    event_threat_detection_custom_module: "EventThreatDetectionCustomModule" = (
        proto.Field(
            proto.MESSAGE,
            number=3,
            message="EventThreatDetectionCustomModule",
        )
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateEventThreatDetectionCustomModuleRequest(proto.Message):
    r"""Message for updating a EventThreatDetectionCustomModule

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the EventThreatDetectionCustomModule resource
            by the update. The fields specified in the update_mask are
            relative to the resource, not the full request. A field will
            be overwritten if it is in the mask. If the user does not
            provide a mask then all fields will be overwritten.
        event_threat_detection_custom_module (google.cloud.securitycentermanagement_v1.types.EventThreatDetectionCustomModule):
            Required. The module being updated
        validate_only (bool):
            Optional. When set to true, only validations
            (including IAM checks) will done for the request
            (module will not be updated). An OK response
            indicates the request is valid while an error
            response indicates the request is invalid. Note
            that a subsequent request to actually update the
            module could still fail because:

            - The state could have changed (e.g. IAM permission lost) or
            - A failure occurred while trying to update the module.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    event_threat_detection_custom_module: "EventThreatDetectionCustomModule" = (
        proto.Field(
            proto.MESSAGE,
            number=2,
            message="EventThreatDetectionCustomModule",
        )
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class DeleteEventThreatDetectionCustomModuleRequest(proto.Message):
    r"""Message for deleting a EventThreatDetectionCustomModule

    Attributes:
        name (str):
            Required. The resource name of the ETD custom module.

            Its format is:

            -  ``organizations/{organization}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.
            -  ``folders/{folder}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.
            -  ``projects/{project}/locations/{location}/eventThreatDetectionCustomModules/{event_threat_detection_custom_module}``.
        validate_only (bool):
            Optional. When set to true, only validations
            (including IAM checks) will done for the request
            (module will not be deleted). An OK response
            indicates the request is valid while an error
            response indicates the request is invalid. Note
            that a subsequent request to actually delete the
            module could still fail because:

            - The state could have changed (e.g. IAM permission lost) or
            - A failure occurred while trying to delete the module.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class ValidateEventThreatDetectionCustomModuleRequest(proto.Message):
    r"""Request to validate an Event Threat Detection custom module.

    Attributes:
        parent (str):
            Required. Resource name of the parent to validate the Custom
            Module under.

            Its format is:

            -  ``organizations/{organization}/locations/{location}``.
        raw_text (str):
            Required. The raw text of the module's
            contents. Used to generate error messages.
        type_ (str):
            Required. The type of the module (e.g. CONFIGURABLE_BAD_IP).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    raw_text: str = proto.Field(
        proto.STRING,
        number=2,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ValidateEventThreatDetectionCustomModuleResponse(proto.Message):
    r"""Response to validating an Event Threat Detection custom
    module.

    Attributes:
        errors (MutableSequence[google.cloud.securitycentermanagement_v1.types.ValidateEventThreatDetectionCustomModuleResponse.CustomModuleValidationError]):
            A list of errors returned by the validator.
            If the list is empty, there were no errors.
    """

    class CustomModuleValidationError(proto.Message):
        r"""An error encountered while validating the uploaded
        configuration of an Event Threat Detection Custom Module.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            description (str):
                A description of the error, suitable for
                human consumption. Required.
            field_path (str):
                The path, in RFC 8901 JSON Pointer format, to
                the field that failed validation. This may be
                left empty if no specific field is affected.
            start (google.cloud.securitycentermanagement_v1.types.ValidateEventThreatDetectionCustomModuleResponse.Position):
                The initial position of the error in the
                uploaded text version of the module. This field
                may be omitted if no specific position applies,
                or if one could not be computed.

                This field is a member of `oneof`_ ``_start``.
            end (google.cloud.securitycentermanagement_v1.types.ValidateEventThreatDetectionCustomModuleResponse.Position):
                The end position of the error in the uploaded
                text version of the module. This field may be
                omitted if no specific position applies, or if
                one could not be computed..

                This field is a member of `oneof`_ ``_end``.
        """

        description: str = proto.Field(
            proto.STRING,
            number=1,
        )
        field_path: str = proto.Field(
            proto.STRING,
            number=2,
        )
        start: "ValidateEventThreatDetectionCustomModuleResponse.Position" = (
            proto.Field(
                proto.MESSAGE,
                number=3,
                optional=True,
                message="ValidateEventThreatDetectionCustomModuleResponse.Position",
            )
        )
        end: "ValidateEventThreatDetectionCustomModuleResponse.Position" = proto.Field(
            proto.MESSAGE,
            number=4,
            optional=True,
            message="ValidateEventThreatDetectionCustomModuleResponse.Position",
        )

    class Position(proto.Message):
        r"""A position in the uploaded text version of a module.

        Attributes:
            line_number (int):
                The line position in the text
            column_number (int):
                The column position in the line
        """

        line_number: int = proto.Field(
            proto.INT32,
            number=1,
        )
        column_number: int = proto.Field(
            proto.INT32,
            number=2,
        )

    errors: MutableSequence[CustomModuleValidationError] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=CustomModuleValidationError,
    )


class GetSecurityCenterServiceRequest(proto.Message):
    r"""Request message for getting a Security Command Center
    service.

    Attributes:
        name (str):
            Required. The Security Command Center service to retrieve.

            Formats:

            -  organizations/{organization}/locations/{location}/securityCenterServices/{service}
            -  folders/{folder}/locations/{location}/securityCenterServices/{service}
            -  projects/{project}/locations/{location}/securityCenterServices/{service}

            The possible values for id {service} are:

            -  container-threat-detection
            -  event-threat-detection
            -  security-health-analytics
            -  vm-threat-detection
            -  web-security-scanner
        show_eligible_modules_only (bool):
            Flag that, when set, will be used to filter
            the ModuleSettings that are in scope. The
            default setting is that all modules will be
            shown.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    show_eligible_modules_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class ListSecurityCenterServicesRequest(proto.Message):
    r"""Request message for listing Security Command Center services.

    Attributes:
        parent (str):
            Required. The name of the parent to list Security Command
            Center services.

            Formats:

            -  organizations/{organization}/locations/{location}
            -  folders/{folder}/locations/{location}
            -  projects/{project}/locations/{location}
        page_size (int):
            Optional. The maximum number of results to
            return in a single response. Default is 10,
            minimum is 1, maximum is 1000.
        page_token (str):
            Optional. The value returned by the last call
            indicating a continuation.
        show_eligible_modules_only (bool):
            Flag that, when set, will be used to filter
            the ModuleSettings that are in scope. The
            default setting is that all modules will be
            shown.
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
    show_eligible_modules_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class ListSecurityCenterServicesResponse(proto.Message):
    r"""Response message for listing Security Command Center
    services.

    Attributes:
        security_center_services (MutableSequence[google.cloud.securitycentermanagement_v1.types.SecurityCenterService]):
            The list of services.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    security_center_services: MutableSequence[
        "SecurityCenterService"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="SecurityCenterService",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class UpdateSecurityCenterServiceRequest(proto.Message):
    r"""Request message for updating a Security Command Center
    service.

    Attributes:
        security_center_service (google.cloud.securitycentermanagement_v1.types.SecurityCenterService):
            Required. The updated service.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Possible values:

            -  "intended_enablement_state"
            -  "modules".
        validate_only (bool):
            Optional. When set to true, only validations
            (including IAM checks) will be done for the
            request (service will not be updated). An OK
            response indicates that the request is valid,
            while an error response indicates that the
            request is invalid. Note that a subsequent
            request to actually update the service could
            still fail for one of the following reasons:

            - The state could have changed (e.g. IAM
              permission lost).
            - A failure occurred while trying to delete the
              module.
    """

    security_center_service: "SecurityCenterService" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="SecurityCenterService",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
