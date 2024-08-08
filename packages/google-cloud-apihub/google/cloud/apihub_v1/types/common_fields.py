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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.apihub.v1",
    manifest={
        "LintState",
        "Linter",
        "Severity",
        "Api",
        "Version",
        "Spec",
        "Deployment",
        "ApiOperation",
        "Definition",
        "Attribute",
        "SpecContents",
        "SpecDetails",
        "OpenApiSpecDetails",
        "OperationDetails",
        "HttpOperation",
        "Path",
        "Schema",
        "Owner",
        "Documentation",
        "AttributeValues",
        "Dependency",
        "DependencyEntityReference",
        "DependencyErrorDetail",
        "LintResponse",
        "Issue",
        "Range",
        "Point",
        "OperationMetadata",
        "ApiHubInstance",
        "ExternalApi",
    },
)


class LintState(proto.Enum):
    r"""Lint state represents success or failure for linting.

    Values:
        LINT_STATE_UNSPECIFIED (0):
            Lint state unspecified.
        LINT_STATE_SUCCESS (1):
            Linting was completed successfully.
        LINT_STATE_ERROR (2):
            Linting encountered errors.
    """
    LINT_STATE_UNSPECIFIED = 0
    LINT_STATE_SUCCESS = 1
    LINT_STATE_ERROR = 2


class Linter(proto.Enum):
    r"""Enumeration of linter types.

    Values:
        LINTER_UNSPECIFIED (0):
            Linter type unspecified.
        SPECTRAL (1):
            Linter type spectral.
        OTHER (2):
            Linter type other.
    """
    LINTER_UNSPECIFIED = 0
    SPECTRAL = 1
    OTHER = 2


class Severity(proto.Enum):
    r"""Severity of the issue.

    Values:
        SEVERITY_UNSPECIFIED (0):
            Severity unspecified.
        SEVERITY_ERROR (1):
            Severity error.
        SEVERITY_WARNING (2):
            Severity warning.
        SEVERITY_INFO (3):
            Severity info.
        SEVERITY_HINT (4):
            Severity hint.
    """
    SEVERITY_UNSPECIFIED = 0
    SEVERITY_ERROR = 1
    SEVERITY_WARNING = 2
    SEVERITY_INFO = 3
    SEVERITY_HINT = 4


class Api(proto.Message):
    r"""An API resource in the API Hub.

    Attributes:
        name (str):
            Identifier. The name of the API resource in the API Hub.

            Format:
            ``projects/{project}/locations/{location}/apis/{api}``
        display_name (str):
            Required. The display name of the API
            resource.
        description (str):
            Optional. The description of the API
            resource.
        documentation (google.cloud.apihub_v1.types.Documentation):
            Optional. The documentation for the API
            resource.
        owner (google.cloud.apihub_v1.types.Owner):
            Optional. Owner details for the API resource.
        versions (MutableSequence[str]):
            Output only. The list of versions present in an API
            resource. Note: An API resource can be associated with more
            than 1 version. Format is
            ``projects/{project}/locations/{location}/apis/{api}/versions/{version}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the API
            resource was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the API
            resource was last updated.
        target_user (google.cloud.apihub_v1.types.AttributeValues):
            Optional. The target users for the API. This maps to the
            following system defined attribute:
            ``projects/{project}/locations/{location}/attributes/system-target-user``
            attribute. The number of values for this attribute will be
            based on the cardinality of the attribute. The same can be
            retrieved via GetAttribute API. All values should be from
            the list of allowed values defined for the attribute.
        team (google.cloud.apihub_v1.types.AttributeValues):
            Optional. The team owning the API. This maps to the
            following system defined attribute:
            ``projects/{project}/locations/{location}/attributes/system-team``
            attribute. The number of values for this attribute will be
            based on the cardinality of the attribute. The same can be
            retrieved via GetAttribute API. All values should be from
            the list of allowed values defined for the attribute.
        business_unit (google.cloud.apihub_v1.types.AttributeValues):
            Optional. The business unit owning the API. This maps to the
            following system defined attribute:
            ``projects/{project}/locations/{location}/attributes/system-business-unit``
            attribute. The number of values for this attribute will be
            based on the cardinality of the attribute. The same can be
            retrieved via GetAttribute API. All values should be from
            the list of allowed values defined for the attribute.
        maturity_level (google.cloud.apihub_v1.types.AttributeValues):
            Optional. The maturity level of the API. This maps to the
            following system defined attribute:
            ``projects/{project}/locations/{location}/attributes/system-maturity-level``
            attribute. The number of values for this attribute will be
            based on the cardinality of the attribute. The same can be
            retrieved via GetAttribute API. All values should be from
            the list of allowed values defined for the attribute.
        attributes (MutableMapping[str, google.cloud.apihub_v1.types.AttributeValues]):
            Optional. The list of user defined attributes associated
            with the API resource. The key is the attribute name. It
            will be of the format:
            ``projects/{project}/locations/{location}/attributes/{attribute}``.
            The value is the attribute values associated with the
            resource.
        api_style (google.cloud.apihub_v1.types.AttributeValues):
            Optional. The style of the API. This maps to the following
            system defined attribute:
            ``projects/{project}/locations/{location}/attributes/system-api-style``
            attribute. The number of values for this attribute will be
            based on the cardinality of the attribute. The same can be
            retrieved via GetAttribute API. All values should be from
            the list of allowed values defined for the attribute.
        selected_version (str):
            Optional. The selected version for an API resource. This can
            be used when special handling is needed on client side for
            particular version of the API. Format is
            ``projects/{project}/locations/{location}/apis/{api}/versions/{version}``
    """

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
    documentation: "Documentation" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Documentation",
    )
    owner: "Owner" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="Owner",
    )
    versions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    target_user: "AttributeValues" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="AttributeValues",
    )
    team: "AttributeValues" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="AttributeValues",
    )
    business_unit: "AttributeValues" = proto.Field(
        proto.MESSAGE,
        number=11,
        message="AttributeValues",
    )
    maturity_level: "AttributeValues" = proto.Field(
        proto.MESSAGE,
        number=12,
        message="AttributeValues",
    )
    attributes: MutableMapping[str, "AttributeValues"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=13,
        message="AttributeValues",
    )
    api_style: "AttributeValues" = proto.Field(
        proto.MESSAGE,
        number=14,
        message="AttributeValues",
    )
    selected_version: str = proto.Field(
        proto.STRING,
        number=15,
    )


class Version(proto.Message):
    r"""Represents a version of the API resource in API hub. This is
    also referred to as the API version.

    Attributes:
        name (str):
            Identifier. The name of the version.

            Format:
            ``projects/{project}/locations/{location}/apis/{api}/versions/{version}``
        display_name (str):
            Required. The display name of the version.
        description (str):
            Optional. The description of the version.
        documentation (google.cloud.apihub_v1.types.Documentation):
            Optional. The documentation of the version.
        specs (MutableSequence[str]):
            Output only. The specs associated with this version. Note
            that an API version can be associated with multiple specs.
            Format is
            ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}``
        api_operations (MutableSequence[str]):
            Output only. The operations contained in the API version.
            These operations will be added to the version when a new
            spec is added or when an existing spec is updated. Format is
            ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/operations/{operation}``
        definitions (MutableSequence[str]):
            Output only. The definitions contained in the API version.
            These definitions will be added to the version when a new
            spec is added or when an existing spec is updated. Format is
            ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/definitions/{definition}``
        deployments (MutableSequence[str]):
            Optional. The deployments linked to this API version. Note:
            A particular API version could be deployed to multiple
            deployments (for dev deployment, UAT deployment, etc) Format
            is
            ``projects/{project}/locations/{location}/deployments/{deployment}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the version
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the version
            was last updated.
        lifecycle (google.cloud.apihub_v1.types.AttributeValues):
            Optional. The lifecycle of the API version. This maps to the
            following system defined attribute:
            ``projects/{project}/locations/{location}/attributes/system-lifecycle``
            attribute. The number of values for this attribute will be
            based on the cardinality of the attribute. The same can be
            retrieved via GetAttribute API. All values should be from
            the list of allowed values defined for the attribute.
        compliance (google.cloud.apihub_v1.types.AttributeValues):
            Optional. The compliance associated with the API version.
            This maps to the following system defined attribute:
            ``projects/{project}/locations/{location}/attributes/system-compliance``
            attribute. The number of values for this attribute will be
            based on the cardinality of the attribute. The same can be
            retrieved via GetAttribute API. All values should be from
            the list of allowed values defined for the attribute.
        accreditation (google.cloud.apihub_v1.types.AttributeValues):
            Optional. The accreditations associated with the API
            version. This maps to the following system defined
            attribute:
            ``projects/{project}/locations/{location}/attributes/system-accreditation``
            attribute. The number of values for this attribute will be
            based on the cardinality of the attribute. The same can be
            retrieved via GetAttribute API. All values should be from
            the list of allowed values defined for the attribute.
        attributes (MutableMapping[str, google.cloud.apihub_v1.types.AttributeValues]):
            Optional. The list of user defined attributes associated
            with the Version resource. The key is the attribute name. It
            will be of the format:
            ``projects/{project}/locations/{location}/attributes/{attribute}``.
            The value is the attribute values associated with the
            resource.
        selected_deployment (str):
            Optional. The selected deployment for a Version resource.
            This can be used when special handling is needed on client
            side for a particular deployment linked to the version.
            Format is
            ``projects/{project}/locations/{location}/deployments/{deployment}``
    """

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
    documentation: "Documentation" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Documentation",
    )
    specs: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    api_operations: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    definitions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    deployments: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=8,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    lifecycle: "AttributeValues" = proto.Field(
        proto.MESSAGE,
        number=11,
        message="AttributeValues",
    )
    compliance: "AttributeValues" = proto.Field(
        proto.MESSAGE,
        number=12,
        message="AttributeValues",
    )
    accreditation: "AttributeValues" = proto.Field(
        proto.MESSAGE,
        number=13,
        message="AttributeValues",
    )
    attributes: MutableMapping[str, "AttributeValues"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=14,
        message="AttributeValues",
    )
    selected_deployment: str = proto.Field(
        proto.STRING,
        number=16,
    )


class Spec(proto.Message):
    r"""Represents a spec associated with an API version in the API
    Hub. Note that specs of various types can be uploaded, however
    parsing of details is supported for OpenAPI spec currently.

    Attributes:
        name (str):
            Identifier. The name of the spec.

            Format:
            ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}``
        display_name (str):
            Required. The display name of the spec.
            This can contain the file name of the spec.
        spec_type (google.cloud.apihub_v1.types.AttributeValues):
            Required. The type of spec. The value should be one of the
            allowed values defined for
            ``projects/{project}/locations/{location}/attributes/system-spec-type``
            attribute. The number of values for this attribute will be
            based on the cardinality of the attribute. The same can be
            retrieved via GetAttribute API.

            Note, this field is mandatory if content is provided.
        contents (google.cloud.apihub_v1.types.SpecContents):
            Optional. Input only. The contents of the
            uploaded spec.
        details (google.cloud.apihub_v1.types.SpecDetails):
            Output only. Details parsed from the spec.
        source_uri (str):
            Optional. The URI of the spec source in case
            file is uploaded from an external version
            control system.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the spec was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the spec was
            last updated.
        lint_response (google.cloud.apihub_v1.types.LintResponse):
            Optional. The lint response for the spec.
        attributes (MutableMapping[str, google.cloud.apihub_v1.types.AttributeValues]):
            Optional. The list of user defined attributes associated
            with the spec. The key is the attribute name. It will be of
            the format:
            ``projects/{project}/locations/{location}/attributes/{attribute}``.
            The value is the attribute values associated with the
            resource.
        documentation (google.cloud.apihub_v1.types.Documentation):
            Optional. The documentation of the spec. For OpenAPI spec,
            this will be populated from ``externalDocs`` in OpenAPI
            spec.
        parsing_mode (google.cloud.apihub_v1.types.Spec.ParsingMode):
            Optional. Input only. Enum specifying the
            parsing mode for OpenAPI Specification (OAS)
            parsing.
    """

    class ParsingMode(proto.Enum):
        r"""Specifies the parsing mode for API specifications during creation
        and update.

        -  ``RELAXED``: Parsing errors in the specification content do not
           fail the API call.
        -  ``STRICT``: Parsing errors in the specification content result in
           failure of the API call. If not specified, defaults to
           ``RELAXED``.

        Values:
            PARSING_MODE_UNSPECIFIED (0):
                Defaults to ``RELAXED``.
            RELAXED (1):
                Parsing of the Spec on create and update is
                relaxed, meaning that parsing errors the spec
                contents will not fail the API call.
            STRICT (2):
                Parsing of the Spec on create and update is
                strict, meaning that parsing errors in the spec
                contents will fail the API call.
        """
        PARSING_MODE_UNSPECIFIED = 0
        RELAXED = 1
        STRICT = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    spec_type: "AttributeValues" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="AttributeValues",
    )
    contents: "SpecContents" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="SpecContents",
    )
    details: "SpecDetails" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="SpecDetails",
    )
    source_uri: str = proto.Field(
        proto.STRING,
        number=6,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    lint_response: "LintResponse" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="LintResponse",
    )
    attributes: MutableMapping[str, "AttributeValues"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=10,
        message="AttributeValues",
    )
    documentation: "Documentation" = proto.Field(
        proto.MESSAGE,
        number=11,
        message="Documentation",
    )
    parsing_mode: ParsingMode = proto.Field(
        proto.ENUM,
        number=12,
        enum=ParsingMode,
    )


class Deployment(proto.Message):
    r"""Details of the deployment where APIs are hosted.
    A deployment could represent an Apigee proxy, API gateway, other
    Google Cloud services or non-Google Cloud services as well. A
    deployment entity is a root level entity in the API hub and
    exists independent of any API.

    Attributes:
        name (str):
            Identifier. The name of the deployment.

            Format:
            ``projects/{project}/locations/{location}/deployments/{deployment}``
        display_name (str):
            Required. The display name of the deployment.
        description (str):
            Optional. The description of the deployment.
        documentation (google.cloud.apihub_v1.types.Documentation):
            Optional. The documentation of the
            deployment.
        deployment_type (google.cloud.apihub_v1.types.AttributeValues):
            Required. The type of deployment. This maps to the following
            system defined attribute:
            ``projects/{project}/locations/{location}/attributes/system-deployment-type``
            attribute. The number of values for this attribute will be
            based on the cardinality of the attribute. The same can be
            retrieved via GetAttribute API. All values should be from
            the list of allowed values defined for the attribute.
        resource_uri (str):
            Required. A URI to the runtime resource. This URI can be
            used to manage the resource. For example, if the runtime
            resource is of type APIGEE_PROXY, then this field will
            contain the URI to the management UI of the proxy.
        endpoints (MutableSequence[str]):
            Required. The endpoints at which this
            deployment resource is listening for API
            requests. This could be a list of complete URIs,
            hostnames or an IP addresses.
        api_versions (MutableSequence[str]):
            Output only. The API versions linked to this
            deployment. Note: A particular deployment could
            be linked to multiple different API versions (of
            same or different APIs).
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the deployment
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the deployment
            was last updated.
        slo (google.cloud.apihub_v1.types.AttributeValues):
            Optional. The SLO for this deployment. This maps to the
            following system defined attribute:
            ``projects/{project}/locations/{location}/attributes/system-slo``
            attribute. The number of values for this attribute will be
            based on the cardinality of the attribute. The same can be
            retrieved via GetAttribute API. All values should be from
            the list of allowed values defined for the attribute.
        environment (google.cloud.apihub_v1.types.AttributeValues):
            Optional. The environment mapping to this deployment. This
            maps to the following system defined attribute:
            ``projects/{project}/locations/{location}/attributes/system-environment``
            attribute. The number of values for this attribute will be
            based on the cardinality of the attribute. The same can be
            retrieved via GetAttribute API. All values should be from
            the list of allowed values defined for the attribute.
        attributes (MutableMapping[str, google.cloud.apihub_v1.types.AttributeValues]):
            Optional. The list of user defined attributes associated
            with the deployment resource. The key is the attribute name.
            It will be of the format:
            ``projects/{project}/locations/{location}/attributes/{attribute}``.
            The value is the attribute values associated with the
            resource.
    """

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
    documentation: "Documentation" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Documentation",
    )
    deployment_type: "AttributeValues" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="AttributeValues",
    )
    resource_uri: str = proto.Field(
        proto.STRING,
        number=6,
    )
    endpoints: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    api_versions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=8,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    slo: "AttributeValues" = proto.Field(
        proto.MESSAGE,
        number=11,
        message="AttributeValues",
    )
    environment: "AttributeValues" = proto.Field(
        proto.MESSAGE,
        number=12,
        message="AttributeValues",
    )
    attributes: MutableMapping[str, "AttributeValues"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=13,
        message="AttributeValues",
    )


class ApiOperation(proto.Message):
    r"""Represents an operation contained in an API version in the
    API Hub. An operation is added/updated/deleted in an API version
    when a new spec is added or an existing spec is updated/deleted
    in a version. Currently, an operation will be created only
    corresponding to OpenAPI spec as parsing is supported for
    OpenAPI spec.

    Attributes:
        name (str):
            Identifier. The name of the operation.

            Format:
            ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/operations/{operation}``
        spec (str):
            Output only. The name of the spec from where the operation
            was parsed. Format is
            ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}``
        details (google.cloud.apihub_v1.types.OperationDetails):
            Output only. Operation details.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the operation
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the operation
            was last updated.
        attributes (MutableMapping[str, google.cloud.apihub_v1.types.AttributeValues]):
            Optional. The list of user defined attributes associated
            with the API operation resource. The key is the attribute
            name. It will be of the format:
            ``projects/{project}/locations/{location}/attributes/{attribute}``.
            The value is the attribute values associated with the
            resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    spec: str = proto.Field(
        proto.STRING,
        number=2,
    )
    details: "OperationDetails" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="OperationDetails",
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    attributes: MutableMapping[str, "AttributeValues"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=6,
        message="AttributeValues",
    )


class Definition(proto.Message):
    r"""Represents a definition for example schema, request, response
    definitions contained in an API version. A definition is
    added/updated/deleted in an API version when a new spec is added or
    an existing spec is updated/deleted in a version. Currently,
    definition will be created only corresponding to OpenAPI spec as
    parsing is supported for OpenAPI spec. Also, within OpenAPI spec,
    only ``schema`` object is supported.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        schema (google.cloud.apihub_v1.types.Schema):
            Output only. The value of a schema
            definition.

            This field is a member of `oneof`_ ``value``.
        name (str):
            Identifier. The name of the definition.

            Format:
            ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/definitions/{definition}``
        spec (str):
            Output only. The name of the spec from where the definition
            was parsed. Format is
            ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/specs/{spec}``
        type_ (google.cloud.apihub_v1.types.Definition.Type):
            Output only. The type of the definition.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the definition
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the definition
            was last updated.
        attributes (MutableMapping[str, google.cloud.apihub_v1.types.AttributeValues]):
            Optional. The list of user defined attributes associated
            with the definition resource. The key is the attribute name.
            It will be of the format:
            ``projects/{project}/locations/{location}/attributes/{attribute}``.
            The value is the attribute values associated with the
            resource.
    """

    class Type(proto.Enum):
        r"""Enumeration of definition types.

        Values:
            TYPE_UNSPECIFIED (0):
                Definition type unspecified.
            SCHEMA (1):
                Definition type schema.
        """
        TYPE_UNSPECIFIED = 0
        SCHEMA = 1

    schema: "Schema" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="value",
        message="Schema",
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    spec: str = proto.Field(
        proto.STRING,
        number=2,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=3,
        enum=Type,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    attributes: MutableMapping[str, "AttributeValues"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=7,
        message="AttributeValues",
    )


class Attribute(proto.Message):
    r"""An attribute in the API Hub.
    An attribute is a name value pair which can be attached to
    different resources in the API hub based on the scope of the
    attribute. Attributes can either be pre-defined by the API Hub
    or created by users.

    Attributes:
        name (str):
            Identifier. The name of the attribute in the API Hub.

            Format:
            ``projects/{project}/locations/{location}/attributes/{attribute}``
        display_name (str):
            Required. The display name of the attribute.
        description (str):
            Optional. The description of the attribute.
        definition_type (google.cloud.apihub_v1.types.Attribute.DefinitionType):
            Output only. The definition type of the
            attribute.
        scope (google.cloud.apihub_v1.types.Attribute.Scope):
            Required. The scope of the attribute. It
            represents the resource in the API Hub to which
            the attribute can be linked.
        data_type (google.cloud.apihub_v1.types.Attribute.DataType):
            Required. The type of the data of the
            attribute.
        allowed_values (MutableSequence[google.cloud.apihub_v1.types.Attribute.AllowedValue]):
            Optional. The list of allowed values when the attribute
            value is of type enum. This is required when the data_type
            of the attribute is ENUM. The maximum number of allowed
            values of an attribute will be 1000.
        cardinality (int):
            Optional. The maximum number of values that
            the attribute can have when associated with an
            API Hub resource. Cardinality 1 would represent
            a single-valued attribute. It must not be less
            than 1 or greater than 20. If not specified, the
            cardinality would be set to 1 by default and
            represent a single-valued attribute.
        mandatory (bool):
            Output only. When mandatory is true, the
            attribute is mandatory for the resource
            specified in the scope. Only System defined
            attributes can be mandatory.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the attribute
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the attribute
            was last updated.
    """

    class DefinitionType(proto.Enum):
        r"""Enumeration of attribute definition types.

        Values:
            DEFINITION_TYPE_UNSPECIFIED (0):
                Attribute definition type unspecified.
            SYSTEM_DEFINED (1):
                The attribute is predefined by the API Hub.
                Note that only the list of allowed values can be
                updated in this case via UpdateAttribute method.
            USER_DEFINED (2):
                The attribute is defined by the user.
        """
        DEFINITION_TYPE_UNSPECIFIED = 0
        SYSTEM_DEFINED = 1
        USER_DEFINED = 2

    class Scope(proto.Enum):
        r"""Enumeration for the scope of the attribute representing the
        resource in the API Hub to which the attribute can be linked.

        Values:
            SCOPE_UNSPECIFIED (0):
                Scope Unspecified.
            API (1):
                Attribute can be linked to an API.
            VERSION (2):
                Attribute can be linked to an API version.
            SPEC (3):
                Attribute can be linked to a Spec.
            API_OPERATION (4):
                Attribute can be linked to an API Operation.
            DEPLOYMENT (5):
                Attribute can be linked to a Deployment.
            DEPENDENCY (6):
                Attribute can be linked to a Dependency.
            DEFINITION (7):
                Attribute can be linked to a definition.
            EXTERNAL_API (8):
                Attribute can be linked to a ExternalAPI.
            PLUGIN (9):
                Attribute can be linked to a Plugin.
        """
        SCOPE_UNSPECIFIED = 0
        API = 1
        VERSION = 2
        SPEC = 3
        API_OPERATION = 4
        DEPLOYMENT = 5
        DEPENDENCY = 6
        DEFINITION = 7
        EXTERNAL_API = 8
        PLUGIN = 9

    class DataType(proto.Enum):
        r"""Enumeration of attribute's data type.

        Values:
            DATA_TYPE_UNSPECIFIED (0):
                Attribute data type unspecified.
            ENUM (1):
                Attribute's value is of type enum.
            JSON (2):
                Attribute's value is of type json.
            STRING (3):
                Attribute's value is of type string.
        """
        DATA_TYPE_UNSPECIFIED = 0
        ENUM = 1
        JSON = 2
        STRING = 3

    class AllowedValue(proto.Message):
        r"""The value that can be assigned to the attribute when the data
        type is enum.

        Attributes:
            id (str):
                Required. The ID of the allowed value.

                -  If provided, the same will be used. The service will
                   throw an error if the specified id is already used by
                   another allowed value in the same attribute resource.
                -  If not provided, a system generated id derived from the
                   display name will be used. In this case, the service will
                   handle conflict resolution by adding a system generated
                   suffix in case of duplicates.

                This value should be 4-63 characters, and valid characters
                are /[a-z][0-9]-/.
            display_name (str):
                Required. The display name of the allowed
                value.
            description (str):
                Optional. The detailed description of the
                allowed value.
            immutable (bool):
                Optional. When set to true, the allowed value
                cannot be updated or deleted by the user. It can
                only be true for System defined attributes.
        """

        id: str = proto.Field(
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
        immutable: bool = proto.Field(
            proto.BOOL,
            number=4,
        )

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
    definition_type: DefinitionType = proto.Field(
        proto.ENUM,
        number=4,
        enum=DefinitionType,
    )
    scope: Scope = proto.Field(
        proto.ENUM,
        number=5,
        enum=Scope,
    )
    data_type: DataType = proto.Field(
        proto.ENUM,
        number=6,
        enum=DataType,
    )
    allowed_values: MutableSequence[AllowedValue] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message=AllowedValue,
    )
    cardinality: int = proto.Field(
        proto.INT32,
        number=8,
    )
    mandatory: bool = proto.Field(
        proto.BOOL,
        number=9,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=11,
        message=timestamp_pb2.Timestamp,
    )


class SpecContents(proto.Message):
    r"""The spec contents.

    Attributes:
        contents (bytes):
            Required. The contents of the spec.
        mime_type (str):
            Required. The mime type of the content for
            example application/json, application/yaml,
            application/wsdl etc.
    """

    contents: bytes = proto.Field(
        proto.BYTES,
        number=1,
    )
    mime_type: str = proto.Field(
        proto.STRING,
        number=2,
    )


class SpecDetails(proto.Message):
    r"""SpecDetails contains the details parsed from supported
    spec types.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        open_api_spec_details (google.cloud.apihub_v1.types.OpenApiSpecDetails):
            Output only. Additional details apart from
            ``OperationDetails`` parsed from an OpenAPI spec. The
            OperationDetails parsed from the spec can be obtained by
            using
            [ListAPIOperations][google.cloud.apihub.v1.ApiHub.ListApiOperations]
            method.

            This field is a member of `oneof`_ ``details``.
        description (str):
            Output only. The description of the spec.
    """

    open_api_spec_details: "OpenApiSpecDetails" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="details",
        message="OpenApiSpecDetails",
    )
    description: str = proto.Field(
        proto.STRING,
        number=1,
    )


class OpenApiSpecDetails(proto.Message):
    r"""OpenApiSpecDetails contains the details parsed from an OpenAPI spec
    in addition to the fields mentioned in
    [SpecDetails][google.cloud.apihub.v1.SpecDetails].

    Attributes:
        format_ (google.cloud.apihub_v1.types.OpenApiSpecDetails.Format):
            Output only. The format of the spec.
        version (str):
            Output only. The version in the spec. This maps to
            ``info.version`` in OpenAPI spec.
        owner (google.cloud.apihub_v1.types.Owner):
            Output only. Owner details for the spec. This maps to
            ``info.contact`` in OpenAPI spec.
    """

    class Format(proto.Enum):
        r"""Enumeration of spec formats.

        Values:
            FORMAT_UNSPECIFIED (0):
                SpecFile type unspecified.
            OPEN_API_SPEC_2_0 (1):
                OpenAPI Spec v2.0.
            OPEN_API_SPEC_3_0 (2):
                OpenAPI Spec v3.0.
            OPEN_API_SPEC_3_1 (3):
                OpenAPI Spec v3.1.
        """
        FORMAT_UNSPECIFIED = 0
        OPEN_API_SPEC_2_0 = 1
        OPEN_API_SPEC_3_0 = 2
        OPEN_API_SPEC_3_1 = 3

    format_: Format = proto.Field(
        proto.ENUM,
        number=1,
        enum=Format,
    )
    version: str = proto.Field(
        proto.STRING,
        number=2,
    )
    owner: "Owner" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Owner",
    )


class OperationDetails(proto.Message):
    r"""The operation details parsed from the spec.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        http_operation (google.cloud.apihub_v1.types.HttpOperation):
            The HTTP Operation.

            This field is a member of `oneof`_ ``operation``.
        description (str):
            Output only. Description of the operation behavior. For
            OpenAPI spec, this will map to ``operation.description`` in
            the spec, in case description is empty,
            ``operation.summary`` will be used.
        documentation (google.cloud.apihub_v1.types.Documentation):
            Output only. Additional external documentation for this
            operation. For OpenAPI spec, this will map to
            ``operation.documentation`` in the spec.
        deprecated (bool):
            Output only. For OpenAPI spec, this will be set if
            ``operation.deprecated``\ is marked as ``true`` in the spec.
    """

    http_operation: "HttpOperation" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="operation",
        message="HttpOperation",
    )
    description: str = proto.Field(
        proto.STRING,
        number=1,
    )
    documentation: "Documentation" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Documentation",
    )
    deprecated: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class HttpOperation(proto.Message):
    r"""The HTTP Operation.

    Attributes:
        path (google.cloud.apihub_v1.types.Path):
            Output only. The path details for the
            Operation.
        method (google.cloud.apihub_v1.types.HttpOperation.Method):
            Output only. Operation method
    """

    class Method(proto.Enum):
        r"""Enumeration of Method types.

        Values:
            METHOD_UNSPECIFIED (0):
                Method unspecified.
            GET (1):
                Get Operation type.
            PUT (2):
                Put Operation type.
            POST (3):
                Post Operation type.
            DELETE (4):
                Delete Operation type.
            OPTIONS (5):
                Options Operation type.
            HEAD (6):
                Head Operation type.
            PATCH (7):
                Patch Operation type.
            TRACE (8):
                Trace Operation type.
        """
        METHOD_UNSPECIFIED = 0
        GET = 1
        PUT = 2
        POST = 3
        DELETE = 4
        OPTIONS = 5
        HEAD = 6
        PATCH = 7
        TRACE = 8

    path: "Path" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Path",
    )
    method: Method = proto.Field(
        proto.ENUM,
        number=2,
        enum=Method,
    )


class Path(proto.Message):
    r"""The path details derived from the spec.

    Attributes:
        path (str):
            Output only. Complete path relative to server
            endpoint.
        description (str):
            Output only. A short description for the path
            applicable to all operations.
    """

    path: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Schema(proto.Message):
    r"""The schema details derived from the spec. Currently, this entity is
    supported for OpenAPI spec only. For OpenAPI spec, this maps to the
    schema defined in the ``definitions`` section for OpenAPI 2.0
    version and in ``components.schemas`` section for OpenAPI 3.0 and
    3.1 version.

    Attributes:
        display_name (str):
            Output only. The display name of the schema.
            This will map to the name of the schema in the
            spec.
        raw_value (bytes):
            Output only. The raw value of the schema
            definition corresponding to the schema name in
            the spec.
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    raw_value: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )


class Owner(proto.Message):
    r"""Owner details.

    Attributes:
        display_name (str):
            Optional. The name of the owner.
        email (str):
            Required. The email of the owner.
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    email: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Documentation(proto.Message):
    r"""Documentation details.

    Attributes:
        external_uri (str):
            Optional. The uri of the externally hosted
            documentation.
    """

    external_uri: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AttributeValues(proto.Message):
    r"""The attribute values associated with resource.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        enum_values (google.cloud.apihub_v1.types.AttributeValues.EnumAttributeValues):
            The attribute values associated with a
            resource in case attribute data type is enum.

            This field is a member of `oneof`_ ``Value``.
        string_values (google.cloud.apihub_v1.types.AttributeValues.StringAttributeValues):
            The attribute values associated with a
            resource in case attribute data type is string.

            This field is a member of `oneof`_ ``Value``.
        json_values (google.cloud.apihub_v1.types.AttributeValues.StringAttributeValues):
            The attribute values associated with a
            resource in case attribute data type is JSON.

            This field is a member of `oneof`_ ``Value``.
        attribute (str):
            Output only. The name of the attribute.
            Format:
            projects/{project}/locations/{location}/attributes/{attribute}
    """

    class EnumAttributeValues(proto.Message):
        r"""The attribute values of data type enum.

        Attributes:
            values (MutableSequence[google.cloud.apihub_v1.types.Attribute.AllowedValue]):
                Required. The attribute values in case
                attribute data type is enum.
        """

        values: MutableSequence["Attribute.AllowedValue"] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="Attribute.AllowedValue",
        )

    class StringAttributeValues(proto.Message):
        r"""The attribute values of data type string or JSON.

        Attributes:
            values (MutableSequence[str]):
                Required. The attribute values in case
                attribute data type is string or JSON.
        """

        values: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )

    enum_values: EnumAttributeValues = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="Value",
        message=EnumAttributeValues,
    )
    string_values: StringAttributeValues = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="Value",
        message=StringAttributeValues,
    )
    json_values: StringAttributeValues = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="Value",
        message=StringAttributeValues,
    )
    attribute: str = proto.Field(
        proto.STRING,
        number=1,
    )


class Dependency(proto.Message):
    r"""A dependency resource defined in the API hub describes a dependency
    directed from a consumer to a supplier entity. A dependency can be
    defined between two [Operations][google.cloud.apihub.v1.Operation]
    or between an [Operation][google.cloud.apihub.v1.Operation] and
    [External API][google.cloud.apihub.v1.ExternalApi].

    Attributes:
        name (str):
            Identifier. The name of the dependency in the API Hub.

            Format:
            ``projects/{project}/locations/{location}/dependencies/{dependency}``
        consumer (google.cloud.apihub_v1.types.DependencyEntityReference):
            Required. Immutable. The entity acting as the
            consumer in the dependency.
        supplier (google.cloud.apihub_v1.types.DependencyEntityReference):
            Required. Immutable. The entity acting as the
            supplier in the dependency.
        state (google.cloud.apihub_v1.types.Dependency.State):
            Output only. State of the dependency.
        description (str):
            Optional. Human readable description
            corresponding of the dependency.
        discovery_mode (google.cloud.apihub_v1.types.Dependency.DiscoveryMode):
            Output only. Discovery mode of the
            dependency.
        error_detail (google.cloud.apihub_v1.types.DependencyErrorDetail):
            Output only. Error details of a dependency if
            the system has detected it internally.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the dependency
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the dependency
            was last updated.
        attributes (MutableMapping[str, google.cloud.apihub_v1.types.AttributeValues]):
            Optional. The list of user defined attributes associated
            with the dependency resource. The key is the attribute name.
            It will be of the format:
            ``projects/{project}/locations/{location}/attributes/{attribute}``.
            The value is the attribute values associated with the
            resource.
    """

    class State(proto.Enum):
        r"""Possible states for a dependency.

        Values:
            STATE_UNSPECIFIED (0):
                Default value. This value is unused.
            PROPOSED (1):
                Dependency will be in a proposed state when
                it is newly identified by the API hub on its
                own.
            VALIDATED (2):
                Dependency will be in a validated state when
                it is validated by the admin or manually created
                in the API hub.
        """
        STATE_UNSPECIFIED = 0
        PROPOSED = 1
        VALIDATED = 2

    class DiscoveryMode(proto.Enum):
        r"""Possible modes of discovering the dependency.

        Values:
            DISCOVERY_MODE_UNSPECIFIED (0):
                Default value. This value is unused.
            MANUAL (1):
                Manual mode of discovery when the dependency
                is defined by the user.
        """
        DISCOVERY_MODE_UNSPECIFIED = 0
        MANUAL = 1

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    consumer: "DependencyEntityReference" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="DependencyEntityReference",
    )
    supplier: "DependencyEntityReference" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="DependencyEntityReference",
    )
    state: State = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    discovery_mode: DiscoveryMode = proto.Field(
        proto.ENUM,
        number=6,
        enum=DiscoveryMode,
    )
    error_detail: "DependencyErrorDetail" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="DependencyErrorDetail",
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
    attributes: MutableMapping[str, "AttributeValues"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=10,
        message="AttributeValues",
    )


class DependencyEntityReference(proto.Message):
    r"""Reference to an entity participating in a dependency.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        operation_resource_name (str):
            The resource name of an operation in the API Hub.

            Format:
            ``projects/{project}/locations/{location}/apis/{api}/versions/{version}/operations/{operation}``

            This field is a member of `oneof`_ ``identifier``.
        external_api_resource_name (str):
            The resource name of an external API in the API Hub.

            Format:
            ``projects/{project}/locations/{location}/externalApis/{external_api}``

            This field is a member of `oneof`_ ``identifier``.
        display_name (str):
            Output only. Display name of the entity.
    """

    operation_resource_name: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="identifier",
    )
    external_api_resource_name: str = proto.Field(
        proto.STRING,
        number=3,
        oneof="identifier",
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DependencyErrorDetail(proto.Message):
    r"""Details describing error condition of a dependency.

    Attributes:
        error (google.cloud.apihub_v1.types.DependencyErrorDetail.Error):
            Optional. Error in the dependency.
        error_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. Timestamp at which the error was
            found.
    """

    class Error(proto.Enum):
        r"""Possible values representing an error in the dependency.

        Values:
            ERROR_UNSPECIFIED (0):
                Default value used for no error in the
                dependency.
            SUPPLIER_NOT_FOUND (1):
                Supplier entity has been deleted.
            SUPPLIER_RECREATED (2):
                Supplier entity has been recreated.
        """
        ERROR_UNSPECIFIED = 0
        SUPPLIER_NOT_FOUND = 1
        SUPPLIER_RECREATED = 2

    error: Error = proto.Field(
        proto.ENUM,
        number=1,
        enum=Error,
    )
    error_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


class LintResponse(proto.Message):
    r"""LintResponse contains the response from the linter.

    Attributes:
        issues (MutableSequence[google.cloud.apihub_v1.types.Issue]):
            Optional. Array of issues found in the
            analyzed document.
        summary (MutableSequence[google.cloud.apihub_v1.types.LintResponse.SummaryEntry]):
            Optional. Summary of all issue types and
            counts for each severity level.
        state (google.cloud.apihub_v1.types.LintState):
            Required. Lint state represents success or
            failure for linting.
        source (str):
            Required. Name of the linting application.
        linter (google.cloud.apihub_v1.types.Linter):
            Required. Name of the linter used.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Required. Timestamp when the linting response
            was generated.
    """

    class SummaryEntry(proto.Message):
        r"""Count of issues with a given severity.

        Attributes:
            severity (google.cloud.apihub_v1.types.Severity):
                Required. Severity of the issue.
            count (int):
                Required. Count of issues with the given
                severity.
        """

        severity: "Severity" = proto.Field(
            proto.ENUM,
            number=1,
            enum="Severity",
        )
        count: int = proto.Field(
            proto.INT32,
            number=2,
        )

    issues: MutableSequence["Issue"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Issue",
    )
    summary: MutableSequence[SummaryEntry] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=SummaryEntry,
    )
    state: "LintState" = proto.Field(
        proto.ENUM,
        number=3,
        enum="LintState",
    )
    source: str = proto.Field(
        proto.STRING,
        number=4,
    )
    linter: "Linter" = proto.Field(
        proto.ENUM,
        number=5,
        enum="Linter",
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )


class Issue(proto.Message):
    r"""Issue contains the details of a single issue found by the
    linter.

    Attributes:
        code (str):
            Required. Rule code unique to each rule
            defined in linter.
        path (MutableSequence[str]):
            Required. An array of strings indicating the
            location in the analyzed document where the rule
            was triggered.
        message (str):
            Required. Human-readable message describing
            the issue found by the linter.
        severity (google.cloud.apihub_v1.types.Severity):
            Required. Severity level of the rule
            violation.
        range_ (google.cloud.apihub_v1.types.Range):
            Required. Object describing where in the file
            the issue was found.
    """

    code: str = proto.Field(
        proto.STRING,
        number=1,
    )
    path: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    message: str = proto.Field(
        proto.STRING,
        number=3,
    )
    severity: "Severity" = proto.Field(
        proto.ENUM,
        number=4,
        enum="Severity",
    )
    range_: "Range" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="Range",
    )


class Range(proto.Message):
    r"""Object describing where in the file the issue was found.

    Attributes:
        start (google.cloud.apihub_v1.types.Point):
            Required. Start of the issue.
        end (google.cloud.apihub_v1.types.Point):
            Required. End of the issue.
    """

    start: "Point" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Point",
    )
    end: "Point" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Point",
    )


class Point(proto.Message):
    r"""Point within the file (line and character).

    Attributes:
        line (int):
            Required. Line number (zero-indexed).
        character (int):
            Required. Character position within the line
            (zero-indexed).
    """

    line: int = proto.Field(
        proto.INT32,
        number=1,
    )
    character: int = proto.Field(
        proto.INT32,
        number=2,
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


class ApiHubInstance(proto.Message):
    r"""An ApiHubInstance represents the instance resources of the
    API Hub. Currently, only one ApiHub instance is allowed for each
    project.

    Attributes:
        name (str):
            Identifier. Format:
            ``projects/{project}/locations/{location}/apiHubInstances/{apiHubInstance}``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation timestamp.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last update timestamp.
        state (google.cloud.apihub_v1.types.ApiHubInstance.State):
            Output only. The current state of the ApiHub
            instance.
        state_message (str):
            Output only. Extra information about ApiHub instance state.
            Currently the message would be populated when state is
            ``FAILED``.
        config (google.cloud.apihub_v1.types.ApiHubInstance.Config):
            Required. Config of the ApiHub instance.
        labels (MutableMapping[str, str]):
            Optional. Instance labels to represent
            user-provided metadata. Refer to cloud
            documentation on labels for more details.
            https://cloud.google.com/compute/docs/labeling-resources
        description (str):
            Optional. Description of the ApiHub instance.
    """

    class State(proto.Enum):
        r"""State of the ApiHub Instance.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                state is omitted.
            INACTIVE (1):
                The ApiHub instance has not been initialized
                or has been deleted.
            CREATING (2):
                The ApiHub instance is being created.
            ACTIVE (3):
                The ApiHub instance has been created and is
                ready for use.
            UPDATING (4):
                The ApiHub instance is being updated.
            DELETING (5):
                The ApiHub instance is being deleted.
            FAILED (6):
                The ApiHub instance encountered an error
                during a state change.
        """
        STATE_UNSPECIFIED = 0
        INACTIVE = 1
        CREATING = 2
        ACTIVE = 3
        UPDATING = 4
        DELETING = 5
        FAILED = 6

    class Config(proto.Message):
        r"""Available configurations to provision an ApiHub Instance.

        Attributes:
            cmek_key_name (str):
                Required. The Customer Managed Encryption Key (CMEK) used
                for data encryption. The CMEK name should follow the format
                of
                ``projects/([^/]+)/locations/([^/]+)/keyRings/([^/]+)/cryptoKeys/([^/]+)``,
                where the location must match the instance location.
        """

        cmek_key_name: str = proto.Field(
            proto.STRING,
            number=1,
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
    state: State = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )
    state_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    config: Config = proto.Field(
        proto.MESSAGE,
        number=6,
        message=Config,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )
    description: str = proto.Field(
        proto.STRING,
        number=8,
    )


class ExternalApi(proto.Message):
    r"""An external API represents an API being provided by external
    sources. This can be used to model third-party APIs and can be
    used to define dependencies.

    Attributes:
        name (str):
            Identifier. Format:
            ``projects/{project}/locations/{location}/externalApi/{externalApi}``.
        display_name (str):
            Required. Display name of the external API.
            Max length is 63 characters (Unicode Code
            Points).
        description (str):
            Optional. Description of the external API.
            Max length is 2000 characters (Unicode Code
            Points).
        endpoints (MutableSequence[str]):
            Optional. List of endpoints on which this API
            is accessible.
        paths (MutableSequence[str]):
            Optional. List of paths served by this API.
        documentation (google.cloud.apihub_v1.types.Documentation):
            Optional. Documentation of the external API.
        attributes (MutableMapping[str, google.cloud.apihub_v1.types.AttributeValues]):
            Optional. The list of user defined attributes associated
            with the Version resource. The key is the attribute name. It
            will be of the format:
            ``projects/{project}/locations/{location}/attributes/{attribute}``.
            The value is the attribute values associated with the
            resource.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation timestamp.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Last update timestamp.
    """

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
    endpoints: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    paths: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    documentation: "Documentation" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="Documentation",
    )
    attributes: MutableMapping[str, "AttributeValues"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=7,
        message="AttributeValues",
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


__all__ = tuple(sorted(__protobuf__.manifest))
