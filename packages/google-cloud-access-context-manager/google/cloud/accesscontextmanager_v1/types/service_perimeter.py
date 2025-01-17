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
    package="google.identity.accesscontextmanager.v1",
    manifest={
        "ServicePerimeter",
        "ServicePerimeterConfig",
    },
)


class ServicePerimeter(proto.Message):
    r"""``ServicePerimeter`` describes a set of Google Cloud resources which
    can freely import and export data amongst themselves, but not export
    outside of the ``ServicePerimeter``. If a request with a source
    within this ``ServicePerimeter`` has a target outside of the
    ``ServicePerimeter``, the request will be blocked. Otherwise the
    request is allowed. There are two types of Service Perimeter -
    Regular and Bridge. Regular Service Perimeters cannot overlap, a
    single Google Cloud project can only belong to a single regular
    Service Perimeter. Service Perimeter Bridges can contain only Google
    Cloud projects as members, a single Google Cloud project may belong
    to multiple Service Perimeter Bridges.

    Attributes:
        name (str):
            Required. Resource name for the ServicePerimeter. The
            ``short_name`` component must begin with a letter and only
            include alphanumeric and '_'. Format:
            ``accessPolicies/{access_policy}/servicePerimeters/{service_perimeter}``
        title (str):
            Human readable title. Must be unique within
            the Policy.
        description (str):
            Description of the ``ServicePerimeter`` and its use. Does
            not affect behavior.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time the ``ServicePerimeter`` was created in
            UTC.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time the ``ServicePerimeter`` was updated in
            UTC.
        perimeter_type (google.cloud.accesscontextmanager_v1.types.ServicePerimeter.PerimeterType):
            Perimeter type indicator. A single project is
            allowed to be a member of single regular
            perimeter, but multiple service perimeter
            bridges. A project cannot be a included in a
            perimeter bridge without being included in
            regular perimeter. For perimeter bridges, the
            restricted service list as well as access level
            lists must be empty.
        status (google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig):
            Current ServicePerimeter configuration.
            Specifies sets of resources, restricted services
            and access levels that determine perimeter
            content and boundaries.
        spec (google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig):
            Proposed (or dry run) ServicePerimeter configuration. This
            configuration allows to specify and test ServicePerimeter
            configuration without enforcing actual access restrictions.
            Only allowed to be set when the "use_explicit_dry_run_spec"
            flag is set.
        use_explicit_dry_run_spec (bool):
            Use explicit dry run spec flag. Ordinarily, a dry-run spec
            implicitly exists for all Service Perimeters, and that spec
            is identical to the status for those Service Perimeters.
            When this flag is set, it inhibits the generation of the
            implicit spec, thereby allowing the user to explicitly
            provide a configuration ("spec") to use in a dry-run version
            of the Service Perimeter. This allows the user to test
            changes to the enforced config ("status") without actually
            enforcing them. This testing is done through analyzing the
            differences between currently enforced and suggested
            restrictions. use_explicit_dry_run_spec must bet set to True
            if any of the fields in the spec are set to non-default
            values.
    """

    class PerimeterType(proto.Enum):
        r"""Specifies the type of the Perimeter. There are two types:
        regular and bridge. Regular Service Perimeter contains
        resources, access levels, and restricted services. Every
        resource can be in at most ONE regular Service Perimeter.

        In addition to being in a regular service perimeter, a resource
        can also be in zero or more perimeter bridges.  A perimeter
        bridge only contains resources.  Cross project operations are
        permitted if all effected resources share some perimeter
        (whether bridge or regular). Perimeter Bridge does not contain
        access levels or services: those are governed entirely by the
        regular perimeter that resource is in.

        Perimeter Bridges are typically useful when building more
        complex toplogies with many independent perimeters that need to
        share some data with a common perimeter, but should not be able
        to share data among themselves.

        Values:
            PERIMETER_TYPE_REGULAR (0):
                Regular Perimeter.
            PERIMETER_TYPE_BRIDGE (1):
                Perimeter Bridge.
        """
        PERIMETER_TYPE_REGULAR = 0
        PERIMETER_TYPE_BRIDGE = 1

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    title: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
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
    perimeter_type: PerimeterType = proto.Field(
        proto.ENUM,
        number=6,
        enum=PerimeterType,
    )
    status: "ServicePerimeterConfig" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="ServicePerimeterConfig",
    )
    spec: "ServicePerimeterConfig" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="ServicePerimeterConfig",
    )
    use_explicit_dry_run_spec: bool = proto.Field(
        proto.BOOL,
        number=9,
    )


class ServicePerimeterConfig(proto.Message):
    r"""``ServicePerimeterConfig`` specifies a set of Google Cloud resources
    that describe specific Service Perimeter configuration.

    Attributes:
        resources (MutableSequence[str]):
            A list of Google Cloud resources that are inside of the
            service perimeter. Currently only projects are allowed.
            Format: ``projects/{project_number}``
        access_levels (MutableSequence[str]):
            A list of ``AccessLevel`` resource names that allow
            resources within the ``ServicePerimeter`` to be accessed
            from the internet. ``AccessLevels`` listed must be in the
            same policy as this ``ServicePerimeter``. Referencing a
            nonexistent ``AccessLevel`` is a syntax error. If no
            ``AccessLevel`` names are listed, resources within the
            perimeter can only be accessed via Google Cloud calls with
            request origins within the perimeter. Example:
            ``"accessPolicies/MY_POLICY/accessLevels/MY_LEVEL"``. For
            Service Perimeter Bridge, must be empty.
        restricted_services (MutableSequence[str]):
            Google Cloud services that are subject to the Service
            Perimeter restrictions. For example, if
            ``storage.googleapis.com`` is specified, access to the
            storage buckets inside the perimeter must meet the
            perimeter's access restrictions.
        vpc_accessible_services (google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig.VpcAccessibleServices):
            Configuration for APIs allowed within
            Perimeter.
        ingress_policies (MutableSequence[google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig.IngressPolicy]):
            List of [IngressPolicies]
            [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy]
            to apply to the perimeter. A perimeter may have multiple
            [IngressPolicies]
            [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy],
            each of which is evaluated separately. Access is granted if
            any [Ingress Policy]
            [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy]
            grants it. Must be empty for a perimeter bridge.
        egress_policies (MutableSequence[google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig.EgressPolicy]):
            List of [EgressPolicies]
            [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressPolicy]
            to apply to the perimeter. A perimeter may have multiple
            [EgressPolicies]
            [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressPolicy],
            each of which is evaluated separately. Access is granted if
            any [EgressPolicy]
            [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressPolicy]
            grants it. Must be empty for a perimeter bridge.
    """

    class IdentityType(proto.Enum):
        r"""Specifies the types of identities that are allowed access in either
        [IngressFrom]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressFrom]
        or [EgressFrom]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressFrom]
        rules.

        Values:
            IDENTITY_TYPE_UNSPECIFIED (0):
                No blanket identity group specified.
            ANY_IDENTITY (1):
                Authorize access from all identities outside
                the perimeter.
            ANY_USER_ACCOUNT (2):
                Authorize access from all human users outside
                the perimeter.
            ANY_SERVICE_ACCOUNT (3):
                Authorize access from all service accounts
                outside the perimeter.
        """
        IDENTITY_TYPE_UNSPECIFIED = 0
        ANY_IDENTITY = 1
        ANY_USER_ACCOUNT = 2
        ANY_SERVICE_ACCOUNT = 3

    class VpcAccessibleServices(proto.Message):
        r"""Specifies how APIs are allowed to communicate within the
        Service Perimeter.

        Attributes:
            enable_restriction (bool):
                Whether to restrict API calls within the Service Perimeter
                to the list of APIs specified in 'allowed_services'.
            allowed_services (MutableSequence[str]):
                The list of APIs usable within the Service Perimeter. Must
                be empty unless 'enable_restriction' is True. You can
                specify a list of individual services, as well as include
                the 'RESTRICTED-SERVICES' value, which automatically
                includes all of the services protected by the perimeter.
        """

        enable_restriction: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        allowed_services: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )

    class MethodSelector(proto.Message):
        r"""An allowed method or permission of a service specified in
        [ApiOperation]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.ApiOperation].

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            method (str):
                Value for ``method`` should be a valid method name for the
                corresponding ``service_name`` in [ApiOperation]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.ApiOperation].
                If ``*`` used as value for ``method``, then ALL methods and
                permissions are allowed.

                This field is a member of `oneof`_ ``kind``.
            permission (str):
                Value for ``permission`` should be a valid Cloud IAM
                permission for the corresponding ``service_name`` in
                [ApiOperation]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.ApiOperation].

                This field is a member of `oneof`_ ``kind``.
        """

        method: str = proto.Field(
            proto.STRING,
            number=1,
            oneof="kind",
        )
        permission: str = proto.Field(
            proto.STRING,
            number=2,
            oneof="kind",
        )

    class ApiOperation(proto.Message):
        r"""Identification for an API Operation.

        Attributes:
            service_name (str):
                The name of the API whose methods or permissions the
                [IngressPolicy]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy]
                or [EgressPolicy]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressPolicy]
                want to allow. A single [ApiOperation]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.ApiOperation]
                with ``service_name`` field set to ``*`` will allow all
                methods AND permissions for all services.
            method_selectors (MutableSequence[google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig.MethodSelector]):
                API methods or permissions to allow. Method or permission
                must belong to the service specified by ``service_name``
                field. A single [MethodSelector]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.MethodSelector]
                entry with ``*`` specified for the ``method`` field will
                allow all methods AND permissions for the service specified
                in ``service_name``.
        """

        service_name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        method_selectors: MutableSequence[
            "ServicePerimeterConfig.MethodSelector"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="ServicePerimeterConfig.MethodSelector",
        )

    class IngressSource(proto.Message):
        r"""The source that [IngressPolicy]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy]
        authorizes access from.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            access_level (str):
                An [AccessLevel]
                [google.identity.accesscontextmanager.v1.AccessLevel]
                resource name that allow resources within the
                [ServicePerimeters]
                [google.identity.accesscontextmanager.v1.ServicePerimeter]
                to be accessed from the internet. [AccessLevels]
                [google.identity.accesscontextmanager.v1.AccessLevel] listed
                must be in the same policy as this [ServicePerimeter]
                [google.identity.accesscontextmanager.v1.ServicePerimeter].
                Referencing a nonexistent [AccessLevel]
                [google.identity.accesscontextmanager.v1.AccessLevel] will
                cause an error. If no [AccessLevel]
                [google.identity.accesscontextmanager.v1.AccessLevel] names
                are listed, resources within the perimeter can only be
                accessed via Google Cloud calls with request origins within
                the perimeter. Example:
                ``accessPolicies/MY_POLICY/accessLevels/MY_LEVEL``. If a
                single ``*`` is specified for ``access_level``, then all
                [IngressSources]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressSource]
                will be allowed.

                This field is a member of `oneof`_ ``source``.
            resource (str):
                A Google Cloud resource that is allowed to ingress the
                perimeter. Requests from these resources will be allowed to
                access perimeter data. Currently only projects are allowed.
                Format: ``projects/{project_number}`` The project may be in
                any Google Cloud organization, not just the organization
                that the perimeter is defined in. ``*`` is not allowed, the
                case of allowing all Google Cloud resources only is not
                supported.

                This field is a member of `oneof`_ ``source``.
        """

        access_level: str = proto.Field(
            proto.STRING,
            number=1,
            oneof="source",
        )
        resource: str = proto.Field(
            proto.STRING,
            number=2,
            oneof="source",
        )

    class IngressFrom(proto.Message):
        r"""Defines the conditions under which an [IngressPolicy]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy]
        matches a request. Conditions are based on information about the
        source of the request. The request must satisfy what is defined in
        ``sources`` AND identity related fields in order to match.

        Attributes:
            sources (MutableSequence[google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig.IngressSource]):
                Sources that this [IngressPolicy]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy]
                authorizes access from.
            identities (MutableSequence[str]):
                A list of identities that are allowed access
                through this ingress policy. Should be in the
                format of email address. The email address
                should represent individual user or service
                account only.
            identity_type (google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig.IdentityType):
                Specifies the type of identities that are allowed access
                from outside the perimeter. If left unspecified, then
                members of ``identities`` field will be allowed access.
        """

        sources: MutableSequence[
            "ServicePerimeterConfig.IngressSource"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="ServicePerimeterConfig.IngressSource",
        )
        identities: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )
        identity_type: "ServicePerimeterConfig.IdentityType" = proto.Field(
            proto.ENUM,
            number=3,
            enum="ServicePerimeterConfig.IdentityType",
        )

    class IngressTo(proto.Message):
        r"""Defines the conditions under which an [IngressPolicy]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy]
        matches a request. Conditions are based on information about the
        [ApiOperation]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.ApiOperation]
        intended to be performed on the target resource of the request. The
        request must satisfy what is defined in ``operations`` AND
        ``resources`` in order to match.

        Attributes:
            operations (MutableSequence[google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig.ApiOperation]):
                A list of [ApiOperations]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.ApiOperation]
                allowed to be performed by the sources specified in
                corresponding [IngressFrom]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressFrom]
                in this [ServicePerimeter]
                [google.identity.accesscontextmanager.v1.ServicePerimeter].
            resources (MutableSequence[str]):
                A list of resources, currently only projects in the form
                ``projects/<projectnumber>``, protected by this
                [ServicePerimeter]
                [google.identity.accesscontextmanager.v1.ServicePerimeter]
                that are allowed to be accessed by sources defined in the
                corresponding [IngressFrom]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressFrom].
                If a single ``*`` is specified, then access to all resources
                inside the perimeter are allowed.
        """

        operations: MutableSequence[
            "ServicePerimeterConfig.ApiOperation"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="ServicePerimeterConfig.ApiOperation",
        )
        resources: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )

    class IngressPolicy(proto.Message):
        r"""Policy for ingress into [ServicePerimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter].

        [IngressPolicies]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy]
        match requests based on ``ingress_from`` and ``ingress_to`` stanzas.
        For an ingress policy to match, both the ``ingress_from`` and
        ``ingress_to`` stanzas must be matched. If an [IngressPolicy]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy]
        matches a request, the request is allowed through the perimeter
        boundary from outside the perimeter.

        For example, access from the internet can be allowed either based on
        an [AccessLevel]
        [google.identity.accesscontextmanager.v1.AccessLevel] or, for
        traffic hosted on Google Cloud, the project of the source network.
        For access from private networks, using the project of the hosting
        network is required.

        Individual ingress policies can be limited by restricting which
        services and/or actions they match using the ``ingress_to`` field.

        Attributes:
            ingress_from (google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig.IngressFrom):
                Defines the conditions on the source of a request causing
                this [IngressPolicy]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy]
                to apply.
            ingress_to (google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig.IngressTo):
                Defines the conditions on the [ApiOperation]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.ApiOperation]
                and request destination that cause this [IngressPolicy]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy]
                to apply.
        """

        ingress_from: "ServicePerimeterConfig.IngressFrom" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="ServicePerimeterConfig.IngressFrom",
        )
        ingress_to: "ServicePerimeterConfig.IngressTo" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="ServicePerimeterConfig.IngressTo",
        )

    class EgressFrom(proto.Message):
        r"""Defines the conditions under which an [EgressPolicy]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressPolicy]
        matches a request. Conditions based on information about the source
        of the request. Note that if the destination of the request is also
        protected by a [ServicePerimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter], then
        that [ServicePerimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] must have
        an [IngressPolicy]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy]
        which allows access in order for this request to succeed.

        Attributes:
            identities (MutableSequence[str]):
                A list of identities that are allowed access through this
                [EgressPolicy]. Should be in the format of email address.
                The email address should represent individual user or
                service account only.
            identity_type (google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig.IdentityType):
                Specifies the type of identities that are allowed access to
                outside the perimeter. If left unspecified, then members of
                ``identities`` field will be allowed access.
        """

        identities: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        identity_type: "ServicePerimeterConfig.IdentityType" = proto.Field(
            proto.ENUM,
            number=2,
            enum="ServicePerimeterConfig.IdentityType",
        )

    class EgressTo(proto.Message):
        r"""Defines the conditions under which an [EgressPolicy]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressPolicy]
        matches a request. Conditions are based on information about the
        [ApiOperation]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.ApiOperation]
        intended to be performed on the ``resources`` specified. Note that
        if the destination of the request is also protected by a
        [ServicePerimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter], then
        that [ServicePerimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] must have
        an [IngressPolicy]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.IngressPolicy]
        which allows access in order for this request to succeed. The
        request must match ``operations`` AND ``resources`` fields in order
        to be allowed egress out of the perimeter.

        Attributes:
            resources (MutableSequence[str]):
                A list of resources, currently only projects in the form
                ``projects/<projectnumber>``, that are allowed to be
                accessed by sources defined in the corresponding
                [EgressFrom]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressFrom].
                A request matches if it contains a resource in this list. If
                ``*`` is specified for ``resources``, then this [EgressTo]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressTo]
                rule will authorize access to all resources outside the
                perimeter.
            operations (MutableSequence[google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig.ApiOperation]):
                A list of [ApiOperations]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.ApiOperation]
                allowed to be performed by the sources specified in the
                corresponding [EgressFrom]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressFrom].
                A request matches if it uses an operation/service in this
                list.
            external_resources (MutableSequence[str]):
                A list of external resources that are allowed to be
                accessed. Only AWS and Azure resources are supported. For
                Amazon S3, the supported format is s3://BUCKET_NAME. For
                Azure Storage, the supported format is
                azure://myaccount.blob.core.windows.net/CONTAINER_NAME. A
                request matches if it contains an external resource in this
                list (Example: s3://bucket/path). Currently '*' is not
                allowed.
        """

        resources: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        operations: MutableSequence[
            "ServicePerimeterConfig.ApiOperation"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="ServicePerimeterConfig.ApiOperation",
        )
        external_resources: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=3,
        )

    class EgressPolicy(proto.Message):
        r"""Policy for egress from perimeter.

        [EgressPolicies]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressPolicy]
        match requests based on ``egress_from`` and ``egress_to`` stanzas.
        For an [EgressPolicy]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressPolicy]
        to match, both ``egress_from`` and ``egress_to`` stanzas must be
        matched. If an [EgressPolicy]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressPolicy]
        matches a request, the request is allowed to span the
        [ServicePerimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] boundary.
        For example, an [EgressPolicy]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressPolicy]
        can be used to allow VMs on networks within the [ServicePerimeter]
        [google.identity.accesscontextmanager.v1.ServicePerimeter] to access
        a defined set of projects outside the perimeter in certain contexts
        (e.g. to read data from a Cloud Storage bucket or query against a
        BigQuery dataset).

        [EgressPolicies]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressPolicy]
        are concerned with the *resources* that a request relates as well as
        the API services and API actions being used. They do not related to
        the direction of data movement. More detailed documentation for this
        concept can be found in the descriptions of [EgressFrom]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressFrom]
        and [EgressTo]
        [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressTo].

        Attributes:
            egress_from (google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig.EgressFrom):
                Defines conditions on the source of a request causing this
                [EgressPolicy]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressPolicy]
                to apply.
            egress_to (google.cloud.accesscontextmanager_v1.types.ServicePerimeterConfig.EgressTo):
                Defines the conditions on the [ApiOperation]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.ApiOperation]
                and destination resources that cause this [EgressPolicy]
                [google.identity.accesscontextmanager.v1.ServicePerimeterConfig.EgressPolicy]
                to apply.
        """

        egress_from: "ServicePerimeterConfig.EgressFrom" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="ServicePerimeterConfig.EgressFrom",
        )
        egress_to: "ServicePerimeterConfig.EgressTo" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="ServicePerimeterConfig.EgressTo",
        )

    resources: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    access_levels: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    restricted_services: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    vpc_accessible_services: VpcAccessibleServices = proto.Field(
        proto.MESSAGE,
        number=10,
        message=VpcAccessibleServices,
    )
    ingress_policies: MutableSequence[IngressPolicy] = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message=IngressPolicy,
    )
    egress_policies: MutableSequence[EgressPolicy] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message=EgressPolicy,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
