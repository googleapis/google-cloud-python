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
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.cloudsecuritycompliance.v1",
    manifest={
        "EnforcementMode",
        "FrameworkCategory",
        "CloudControlCategory",
        "CloudProvider",
        "Severity",
        "RuleActionType",
        "TargetResourceType",
        "Framework",
        "CloudControlDetails",
        "FrameworkReference",
        "Parameter",
        "CloudControl",
        "ParameterSpec",
        "Validation",
        "AllowedValues",
        "RegexpPattern",
        "IntRange",
        "StringList",
        "ParamValue",
        "ParameterSubstitutionRule",
        "AttributeSubstitutionRule",
        "PlaceholderSubstitutionRule",
        "Rule",
        "CELExpression",
        "OperationMetadata",
    },
)


class EnforcementMode(proto.Enum):
    r"""The enforcement mode of the cloud control.

    Values:
        ENFORCEMENT_MODE_UNSPECIFIED (0):
            Default value. This value is unused.
        PREVENTIVE (1):
            The cloud control is enforced to prevent
            resource non-compliance.
        DETECTIVE (2):
            The cloud control is enforced to detect
            resource non-compliance.
        AUDIT (3):
            The cloud control is enforced to audit
            resource non-compliance.
    """
    ENFORCEMENT_MODE_UNSPECIFIED = 0
    PREVENTIVE = 1
    DETECTIVE = 2
    AUDIT = 3


class FrameworkCategory(proto.Enum):
    r"""The category of the framework.

    Values:
        FRAMEWORK_CATEGORY_UNSPECIFIED (0):
            Default value. This value is unused.
        INDUSTRY_DEFINED_STANDARD (1):
            Standard framework
        ASSURED_WORKLOADS (2):
            Assured Workloads framework
        DATA_SECURITY (3):
            Data Security framework
        GOOGLE_BEST_PRACTICES (4):
            Google Best Practices framework
        CUSTOM_FRAMEWORK (5):
            User created framework.
    """
    FRAMEWORK_CATEGORY_UNSPECIFIED = 0
    INDUSTRY_DEFINED_STANDARD = 1
    ASSURED_WORKLOADS = 2
    DATA_SECURITY = 3
    GOOGLE_BEST_PRACTICES = 4
    CUSTOM_FRAMEWORK = 5


class CloudControlCategory(proto.Enum):
    r"""The category of the cloud control.

    Values:
        CLOUD_CONTROL_CATEGORY_UNSPECIFIED (0):
            Default value. This value is unused.
        CC_CATEGORY_INFRASTRUCTURE (1):
            Infrastructure
        CC_CATEGORY_ARTIFICIAL_INTELLIGENCE (2):
            Artificial Intelligence
        CC_CATEGORY_PHYSICAL_SECURITY (3):
            Physical Security
        CC_CATEGORY_DATA_SECURITY (4):
            Data Security
        CC_CATEGORY_NETWORK_SECURITY (5):
            Network Security
        CC_CATEGORY_INCIDENT_MANAGEMENT (6):
            Incident Management
        CC_CATEGORY_IDENTITY_AND_ACCESS_MANAGEMENT (7):
            Identity & Access Management
        CC_CATEGORY_ENCRYPTION (8):
            Encryption
        CC_CATEGORY_LOGS_MANAGEMENT_AND_INFRASTRUCTURE (9):
            Logs Management & Infrastructure
        CC_CATEGORY_HR_ADMIN_AND_PROCESSES (10):
            HR, Admin & Processes
        CC_CATEGORY_THIRD_PARTY_AND_SUB_PROCESSOR_MANAGEMENT (11):
            Third Party & Sub-Processor Management
        CC_CATEGORY_LEGAL_AND_DISCLOSURES (12):
            Legal & Disclosures
        CC_CATEGORY_VULNERABILITY_MANAGEMENT (13):
            Vulnerability Management
        CC_CATEGORY_PRIVACY (14):
            Privacy
        CC_CATEGORY_BCDR (15):
            BCDR (Business Continuity and Disaster
            Recovery)
    """
    CLOUD_CONTROL_CATEGORY_UNSPECIFIED = 0
    CC_CATEGORY_INFRASTRUCTURE = 1
    CC_CATEGORY_ARTIFICIAL_INTELLIGENCE = 2
    CC_CATEGORY_PHYSICAL_SECURITY = 3
    CC_CATEGORY_DATA_SECURITY = 4
    CC_CATEGORY_NETWORK_SECURITY = 5
    CC_CATEGORY_INCIDENT_MANAGEMENT = 6
    CC_CATEGORY_IDENTITY_AND_ACCESS_MANAGEMENT = 7
    CC_CATEGORY_ENCRYPTION = 8
    CC_CATEGORY_LOGS_MANAGEMENT_AND_INFRASTRUCTURE = 9
    CC_CATEGORY_HR_ADMIN_AND_PROCESSES = 10
    CC_CATEGORY_THIRD_PARTY_AND_SUB_PROCESSOR_MANAGEMENT = 11
    CC_CATEGORY_LEGAL_AND_DISCLOSURES = 12
    CC_CATEGORY_VULNERABILITY_MANAGEMENT = 13
    CC_CATEGORY_PRIVACY = 14
    CC_CATEGORY_BCDR = 15


class CloudProvider(proto.Enum):
    r"""The cloud platform.

    Values:
        CLOUD_PROVIDER_UNSPECIFIED (0):
            Default value. This value is unused.
        AWS (1):
            Amazon Web Services (AWS).
        AZURE (2):
            Microsoft Azure.
        GCP (3):
            Google Cloud.
    """
    CLOUD_PROVIDER_UNSPECIFIED = 0
    AWS = 1
    AZURE = 2
    GCP = 3


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


class RuleActionType(proto.Enum):
    r"""The action type of the rule.

    Values:
        RULE_ACTION_TYPE_UNSPECIFIED (0):
            Default value. This value is unused.
        RULE_ACTION_TYPE_PREVENTIVE (1):
            Preventative action type.
        RULE_ACTION_TYPE_DETECTIVE (2):
            Detective action type.
        RULE_ACTION_TYPE_AUDIT (3):
            Audit action type.
    """
    RULE_ACTION_TYPE_UNSPECIFIED = 0
    RULE_ACTION_TYPE_PREVENTIVE = 1
    RULE_ACTION_TYPE_DETECTIVE = 2
    RULE_ACTION_TYPE_AUDIT = 3


class TargetResourceType(proto.Enum):
    r"""TargetResourceType represents the type of resource that a
    control or framework can be applied to.

    Values:
        TARGET_RESOURCE_TYPE_UNSPECIFIED (0):
            Default value. This value is unused.
        TARGET_RESOURCE_CRM_TYPE_ORG (1):
            Target resource is an Organization.
        TARGET_RESOURCE_CRM_TYPE_FOLDER (2):
            Target resource is a Folder.
        TARGET_RESOURCE_CRM_TYPE_PROJECT (3):
            Target resource is a Project.
        TARGET_RESOURCE_TYPE_APPLICATION (4):
            Target resource is an Application.
    """
    TARGET_RESOURCE_TYPE_UNSPECIFIED = 0
    TARGET_RESOURCE_CRM_TYPE_ORG = 1
    TARGET_RESOURCE_CRM_TYPE_FOLDER = 2
    TARGET_RESOURCE_CRM_TYPE_PROJECT = 3
    TARGET_RESOURCE_TYPE_APPLICATION = 4


class Framework(proto.Message):
    r"""A Framework is a collection of CloudControls to address
    security and compliance requirements. Frameworks can be used for
    prevention, detection, and auditing. They can be either
    built-in, industry-standard frameworks provided by GCP/AZURE/AWS
    (e.g., NIST, FedRAMP) or custom frameworks created by users.

    Attributes:
        name (str):
            Required. Identifier. The name of the framework. Format:
            organizations/{organization}/locations/{location}/frameworks/{framework_id}
        major_revision_id (int):
            Output only. Major revision of the framework
            incremented in ascending order.
        display_name (str):
            Optional. Display name of the framework. The
            maximum length is 200 characters.
        description (str):
            Optional. The description of the framework.
            The maximum length is 2000 characters.
        type_ (google.cloud.cloudsecuritycompliance_v1.types.Framework.FrameworkType):
            Output only. The type of the framework. The default is
            TYPE_CUSTOM.
        cloud_control_details (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.CloudControlDetails]):
            Optional. The details of the cloud controls
            directly added without any grouping in the
            framework.
        category (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.FrameworkCategory]):
            Optional. The category of the framework.
        supported_cloud_providers (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.CloudProvider]):
            Output only. cloud providers supported
        supported_target_resource_types (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.TargetResourceType]):
            Output only. target resource types supported
            by the Framework.
        supported_enforcement_modes (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.EnforcementMode]):
            Output only. The supported enforcement modes
            of the framework.
    """

    class FrameworkType(proto.Enum):
        r"""The type of the framework.

        Values:
            FRAMEWORK_TYPE_UNSPECIFIED (0):
                Default value. This value is unused.
            BUILT_IN (1):
                The framework is a built-in framework if it
                is created and managed by GCP.
            CUSTOM (2):
                The framework is a custom framework if it is
                created and managed by the user.
        """
        FRAMEWORK_TYPE_UNSPECIFIED = 0
        BUILT_IN = 1
        CUSTOM = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    major_revision_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=4,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    type_: FrameworkType = proto.Field(
        proto.ENUM,
        number=6,
        enum=FrameworkType,
    )
    cloud_control_details: MutableSequence["CloudControlDetails"] = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message="CloudControlDetails",
    )
    category: MutableSequence["FrameworkCategory"] = proto.RepeatedField(
        proto.ENUM,
        number=9,
        enum="FrameworkCategory",
    )
    supported_cloud_providers: MutableSequence["CloudProvider"] = proto.RepeatedField(
        proto.ENUM,
        number=10,
        enum="CloudProvider",
    )
    supported_target_resource_types: MutableSequence[
        "TargetResourceType"
    ] = proto.RepeatedField(
        proto.ENUM,
        number=11,
        enum="TargetResourceType",
    )
    supported_enforcement_modes: MutableSequence[
        "EnforcementMode"
    ] = proto.RepeatedField(
        proto.ENUM,
        number=13,
        enum="EnforcementMode",
    )


class CloudControlDetails(proto.Message):
    r"""CloudControlDetails contains the details of a CloudControl.

    Attributes:
        name (str):
            Required. The name of the CloudControl in the
            format:
            “organizations/{organization}/locations/{location}/
            cloudControls/{cloud-control}”
        major_revision_id (int):
            Required. Major revision of cloudcontrol
        parameters (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.Parameter]):
            Optional. Parameters is a key-value pair that
            is required by the CloudControl. The
            specification of these parameters will be
            present in cloudcontrol.Eg: { "name":
            "location","value": "us-west-1"}.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    major_revision_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    parameters: MutableSequence["Parameter"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="Parameter",
    )


class FrameworkReference(proto.Message):
    r"""FrameworkReference contains the reference of a framework.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        framework (str):
            Required. In the format:

            organizations/{org}/locations/{location}/frameworks/{framework}
        major_revision_id (int):
            Optional. Major revision id of the framework.
            If not specified, corresponds to the latest
            revision of the framework.

            This field is a member of `oneof`_ ``_major_revision_id``.
    """

    framework: str = proto.Field(
        proto.STRING,
        number=1,
    )
    major_revision_id: int = proto.Field(
        proto.INT64,
        number=2,
        optional=True,
    )


class Parameter(proto.Message):
    r"""Parameters is a key-value pair.

    Attributes:
        name (str):
            Required. The name of the parameter.
        parameter_value (google.cloud.cloudsecuritycompliance_v1.types.ParamValue):
            Required. The value of the parameter
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    parameter_value: "ParamValue" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ParamValue",
    )


class CloudControl(proto.Message):
    r"""A CloudControl is the fundamental unit encapsulating the rules to
    meet a specific security or compliance intent. It can contain
    various rule types (like Organization Policies, CEL expressions,
    etc.) enabling different enforcement modes (Preventive, Detective,
    Audit). CloudControls are often parameterized for reusability and
    can be either BUILT_IN (provided by Google) or CUSTOM (defined by
    the user).

    Attributes:
        name (str):
            Required. Identifier. The resource name of the cloud
            control. Format:
            organizations/{organization}/locations/{location}/cloudControls/{cloud_control_id}
        major_revision_id (int):
            Output only. Major revision of the cloud
            control incremented in ascending order.
        description (str):
            Optional. A description of the cloud control.
            The maximum length is 2000 characters.
        display_name (str):
            Optional. The display name of the cloud
            control. The maximum length is 200 characters.
        supported_enforcement_modes (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.EnforcementMode]):
            Output only. The supported enforcement mode
            of the cloud control. Default is DETECTIVE.
        parameter_spec (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.ParameterSpec]):
            Optional. The parameter spec of the cloud
            control.
        rules (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.Rule]):
            Optional. The Policy to be enforced to
            prevent/detect resource non-compliance.
        severity (google.cloud.cloudsecuritycompliance_v1.types.Severity):
            Optional. The severity of findings generated
            by the cloud control.
        finding_category (str):
            Optional. The finding_category of the cloud control. The
            maximum length is 255 characters.
        supported_cloud_providers (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.CloudProvider]):
            Optional. cloud providers supported
        related_frameworks (MutableSequence[str]):
            Output only. The Frameworks that include this
            CloudControl
        remediation_steps (str):
            Optional. The remediation steps for the
            findings generated by the cloud control. The
            maximum length is 400 characters.
        categories (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.CloudControlCategory]):
            Optional. The categories of the cloud
            control.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last updated time of the cloud control. The
            create_time is used because a new CC is created whenever we
            update an existing CC.
        supported_target_resource_types (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.TargetResourceType]):
            Optional. target resource types supported by
            the CloudControl.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    major_revision_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=4,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    supported_enforcement_modes: MutableSequence[
        "EnforcementMode"
    ] = proto.RepeatedField(
        proto.ENUM,
        number=7,
        enum="EnforcementMode",
    )
    parameter_spec: MutableSequence["ParameterSpec"] = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message="ParameterSpec",
    )
    rules: MutableSequence["Rule"] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message="Rule",
    )
    severity: "Severity" = proto.Field(
        proto.ENUM,
        number=11,
        enum="Severity",
    )
    finding_category: str = proto.Field(
        proto.STRING,
        number=12,
    )
    supported_cloud_providers: MutableSequence["CloudProvider"] = proto.RepeatedField(
        proto.ENUM,
        number=13,
        enum="CloudProvider",
    )
    related_frameworks: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=14,
    )
    remediation_steps: str = proto.Field(
        proto.STRING,
        number=15,
    )
    categories: MutableSequence["CloudControlCategory"] = proto.RepeatedField(
        proto.ENUM,
        number=16,
        enum="CloudControlCategory",
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=17,
        message=timestamp_pb2.Timestamp,
    )
    supported_target_resource_types: MutableSequence[
        "TargetResourceType"
    ] = proto.RepeatedField(
        proto.ENUM,
        number=18,
        enum="TargetResourceType",
    )


class ParameterSpec(proto.Message):
    r"""A parameter spec of the cloud control.

    Attributes:
        name (str):
            Required. The name of the parameter.
        display_name (str):
            Optional. The display name of the parameter.
            The maximum length is 200 characters.
        description (str):
            Optional. The description of the parameter.
            The maximum length is 2000 characters.
        is_required (bool):
            Required. if the parameter is required
        value_type (google.cloud.cloudsecuritycompliance_v1.types.ParameterSpec.ValueType):
            Required. Parameter value type.
        default_value (google.cloud.cloudsecuritycompliance_v1.types.ParamValue):
            Optional. The default value of the parameter.
        substitution_rules (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.ParameterSubstitutionRule]):
            Optional. List of parameter substitutions.
        sub_parameters (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.ParameterSpec]):
            Optional. ParameterSpec for oneof attributes.
        validation (google.cloud.cloudsecuritycompliance_v1.types.Validation):
            Optional. The allowed set of values for the
            parameter.
    """

    class ValueType(proto.Enum):
        r"""The type of the parameter value.

        Values:
            VALUE_TYPE_UNSPECIFIED (0):
                Default value. This value is unused.
            STRING (3):
                String value.
            BOOLEAN (4):
                Boolean value.
            STRINGLIST (5):
                String list value.
            NUMBER (6):
                Numeric value.
            ONEOF (7):
                OneOf value.
        """
        VALUE_TYPE_UNSPECIFIED = 0
        STRING = 3
        BOOLEAN = 4
        STRINGLIST = 5
        NUMBER = 6
        ONEOF = 7

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    is_required: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    value_type: ValueType = proto.Field(
        proto.ENUM,
        number=5,
        enum=ValueType,
    )
    default_value: "ParamValue" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="ParamValue",
    )
    substitution_rules: MutableSequence[
        "ParameterSubstitutionRule"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message="ParameterSubstitutionRule",
    )
    sub_parameters: MutableSequence["ParameterSpec"] = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message="ParameterSpec",
    )
    validation: "Validation" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="Validation",
    )


class Validation(proto.Message):
    r"""Validation of the parameter.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        allowed_values (google.cloud.cloudsecuritycompliance_v1.types.AllowedValues):
            Allowed set of values for the parameter.

            This field is a member of `oneof`_ ``constraint``.
        int_range (google.cloud.cloudsecuritycompliance_v1.types.IntRange):
            Allowed range for numeric parameters.

            This field is a member of `oneof`_ ``constraint``.
        regexp_pattern (google.cloud.cloudsecuritycompliance_v1.types.RegexpPattern):
            Regular expression for string parameters.

            This field is a member of `oneof`_ ``constraint``.
    """

    allowed_values: "AllowedValues" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="constraint",
        message="AllowedValues",
    )
    int_range: "IntRange" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="constraint",
        message="IntRange",
    )
    regexp_pattern: "RegexpPattern" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="constraint",
        message="RegexpPattern",
    )


class AllowedValues(proto.Message):
    r"""Allowed set of values for the parameter.

    Attributes:
        values (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.ParamValue]):
            Required. List of allowed values for the
            parameter.
    """

    values: MutableSequence["ParamValue"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ParamValue",
    )


class RegexpPattern(proto.Message):
    r"""Regular Expression Validator for parameter values.

    Attributes:
        pattern (str):
            Required. Regex Pattern to match the value(s)
            of parameter.
    """

    pattern: str = proto.Field(
        proto.STRING,
        number=1,
    )


class IntRange(proto.Message):
    r"""Number range for number parameters.

    Attributes:
        min_ (int):
            Required. Minimum allowed value for the
            numeric parameter (inclusive).
        max_ (int):
            Required. Maximum allowed value for the
            numeric parameter (inclusive).
    """

    min_: int = proto.Field(
        proto.INT64,
        number=1,
    )
    max_: int = proto.Field(
        proto.INT64,
        number=2,
    )


class StringList(proto.Message):
    r"""A list of strings.

    Attributes:
        values (MutableSequence[str]):
            Required. The strings in the list.
    """

    values: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


class ParamValue(proto.Message):
    r"""Possible parameter value types.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        string_value (str):
            Represents a string value.

            This field is a member of `oneof`_ ``kind``.
        bool_value (bool):
            Represents a boolean value.

            This field is a member of `oneof`_ ``kind``.
        string_list_value (google.cloud.cloudsecuritycompliance_v1.types.StringList):
            Represents a repeated string.

            This field is a member of `oneof`_ ``kind``.
        number_value (float):
            Represents a double value.

            This field is a member of `oneof`_ ``kind``.
        oneof_value (google.cloud.cloudsecuritycompliance_v1.types.Parameter):
            Represents sub-parameter values.

            This field is a member of `oneof`_ ``kind``.
    """

    string_value: str = proto.Field(
        proto.STRING,
        number=3,
        oneof="kind",
    )
    bool_value: bool = proto.Field(
        proto.BOOL,
        number=4,
        oneof="kind",
    )
    string_list_value: "StringList" = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="kind",
        message="StringList",
    )
    number_value: float = proto.Field(
        proto.DOUBLE,
        number=6,
        oneof="kind",
    )
    oneof_value: "Parameter" = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="kind",
        message="Parameter",
    )


class ParameterSubstitutionRule(proto.Message):
    r"""Parameter substitution rules.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        placeholder_substitution_rule (google.cloud.cloudsecuritycompliance_v1.types.PlaceholderSubstitutionRule):
            Placeholder substitution rule.

            This field is a member of `oneof`_ ``substitution_type``.
        attribute_substitution_rule (google.cloud.cloudsecuritycompliance_v1.types.AttributeSubstitutionRule):
            Attribute substitution rule.

            This field is a member of `oneof`_ ``substitution_type``.
    """

    placeholder_substitution_rule: "PlaceholderSubstitutionRule" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="substitution_type",
        message="PlaceholderSubstitutionRule",
    )
    attribute_substitution_rule: "AttributeSubstitutionRule" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="substitution_type",
        message="AttributeSubstitutionRule",
    )


class AttributeSubstitutionRule(proto.Message):
    r"""Attribute at the given path is substituted entirely.

    Attributes:
        attribute (str):
            Fully qualified proto attribute path (in dot notation).
            Example: rules[0].cel_expression.resource_types_values
    """

    attribute: str = proto.Field(
        proto.STRING,
        number=1,
    )


class PlaceholderSubstitutionRule(proto.Message):
    r"""Placeholder is substituted in the rendered string.

    Attributes:
        attribute (str):
            Fully qualified proto attribute path (e.g.,
            dot notation)
    """

    attribute: str = proto.Field(
        proto.STRING,
        number=1,
    )


class Rule(proto.Message):
    r"""A rule of the cloud control.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        cel_expression (google.cloud.cloudsecuritycompliance_v1.types.CELExpression):
            Logic expression in CEL language.

            This field is a member of `oneof`_ ``implementation``.
        description (str):
            Optional. Description of the Rule. The
            maximum length is 2000 characters.
        rule_action_types (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.RuleActionType]):
            Required. The functionality enabled by the
            Rule.
    """

    cel_expression: "CELExpression" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="implementation",
        message="CELExpression",
    )
    description: str = proto.Field(
        proto.STRING,
        number=10,
    )
    rule_action_types: MutableSequence["RuleActionType"] = proto.RepeatedField(
        proto.ENUM,
        number=16,
        enum="RuleActionType",
    )


class CELExpression(proto.Message):
    r"""A `CEL
    expression <https://cloud.google.com/certificate-authority-service/docs/using-cel>`__.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_types_values (google.cloud.cloudsecuritycompliance_v1.types.StringList):
            The resource instance types on which this expression is
            defined. Format will be of the form :
            ``<canonical service name>/<type>`` Example:
            ``compute.googleapis.com/Instance``.

            This field is a member of `oneof`_ ``criteria``.
        expression (str):
            Required. Logic expression in CEL language.
            The max length of the condition is 1000
            characters.
    """

    resource_types_values: "StringList" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="criteria",
        message="StringList",
    )
    expression: str = proto.Field(
        proto.STRING,
        number=1,
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
        requested_cancellation (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have been
            cancelled successfully have [Operation.error][] value with a
            [google.rpc.Status.code][google.rpc.Status.code] of 1,
            corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
