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

from google.api import monitored_resource_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.monitoring.v3",
    manifest={
        "UptimeCheckRegion",
        "GroupResourceType",
        "InternalChecker",
        "UptimeCheckConfig",
        "UptimeCheckIp",
    },
)


class UptimeCheckRegion(proto.Enum):
    r"""The regions from which an Uptime check can be run."""
    REGION_UNSPECIFIED = 0
    USA = 1
    EUROPE = 2
    SOUTH_AMERICA = 3
    ASIA_PACIFIC = 4


class GroupResourceType(proto.Enum):
    r"""The supported resource types that can be used as values of
    ``group_resource.resource_type``. ``INSTANCE`` includes
    ``gce_instance`` and ``aws_ec2_instance`` resource types. The
    resource types ``gae_app`` and ``uptime_url`` are not valid here
    because group checks on App Engine modules and URLs are not allowed.
    """
    RESOURCE_TYPE_UNSPECIFIED = 0
    INSTANCE = 1
    AWS_ELB_LOAD_BALANCER = 2


class InternalChecker(proto.Message):
    r"""An internal checker allows Uptime checks to run on
    private/internal GCP resources.

    Attributes:
        name (str):
            A unique resource name for this InternalChecker. The format
            is:

            ::

                projects/[PROJECT_ID_OR_NUMBER]/internalCheckers/[INTERNAL_CHECKER_ID]

            ``[PROJECT_ID_OR_NUMBER]`` is the Stackdriver Workspace
            project for the Uptime check config associated with the
            internal checker.
        display_name (str):
            The checker's human-readable name. The
            display name should be unique within a
            Stackdriver Workspace in order to make it easier
            to identify; however, uniqueness is not
            enforced.
        network (str):
            The `GCP VPC
            network <https://cloud.google.com/vpc/docs/vpc>`__ where the
            internal resource lives (ex: "default").
        gcp_zone (str):
            The GCP zone the Uptime check should egress from. Only
            respected for internal Uptime checks, where internal_network
            is specified.
        peer_project_id (str):
            The GCP project ID where the internal checker
            lives. Not necessary the same as the Workspace
            project.
        state (google.cloud.monitoring_v3.types.InternalChecker.State):
            The current operational state of the internal
            checker.
    """

    class State(proto.Enum):
        r"""Operational states for an internal checker."""
        UNSPECIFIED = 0
        CREATING = 1
        RUNNING = 2

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    network = proto.Field(proto.STRING, number=3,)
    gcp_zone = proto.Field(proto.STRING, number=4,)
    peer_project_id = proto.Field(proto.STRING, number=6,)
    state = proto.Field(proto.ENUM, number=7, enum=State,)


class UptimeCheckConfig(proto.Message):
    r"""This message configures which resources and services to
    monitor for availability.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            A unique resource name for this Uptime check configuration.
            The format is:

            ::

                 projects/[PROJECT_ID_OR_NUMBER]/uptimeCheckConfigs/[UPTIME_CHECK_ID]

            ``[PROJECT_ID_OR_NUMBER]`` is the Workspace host project
            associated with the Uptime check.

            This field should be omitted when creating the Uptime check
            configuration; on create, the resource name is assigned by
            the server and included in the response.
        display_name (str):
            A human-friendly name for the Uptime check
            configuration. The display name should be unique
            within a Stackdriver Workspace in order to make
            it easier to identify; however, uniqueness is
            not enforced. Required.
        monitored_resource (google.api.monitored_resource_pb2.MonitoredResource):
            The `monitored
            resource <https://cloud.google.com/monitoring/api/resources>`__
            associated with the configuration. The following monitored
            resource types are valid for this field: ``uptime_url``,
            ``gce_instance``, ``gae_app``, ``aws_ec2_instance``,
            ``aws_elb_load_balancer`` ``k8s_service``

            This field is a member of `oneof`_ ``resource``.
        resource_group (google.cloud.monitoring_v3.types.UptimeCheckConfig.ResourceGroup):
            The group resource associated with the
            configuration.

            This field is a member of `oneof`_ ``resource``.
        http_check (google.cloud.monitoring_v3.types.UptimeCheckConfig.HttpCheck):
            Contains information needed to make an HTTP
            or HTTPS check.

            This field is a member of `oneof`_ ``check_request_type``.
        tcp_check (google.cloud.monitoring_v3.types.UptimeCheckConfig.TcpCheck):
            Contains information needed to make a TCP
            check.

            This field is a member of `oneof`_ ``check_request_type``.
        period (google.protobuf.duration_pb2.Duration):
            How often, in seconds, the Uptime check is performed.
            Currently, the only supported values are ``60s`` (1 minute),
            ``300s`` (5 minutes), ``600s`` (10 minutes), and ``900s``
            (15 minutes). Optional, defaults to ``60s``.
        timeout (google.protobuf.duration_pb2.Duration):
            The maximum amount of time to wait for the
            request to complete (must be between 1 and 60
            seconds). Required.
        content_matchers (Sequence[google.cloud.monitoring_v3.types.UptimeCheckConfig.ContentMatcher]):
            The content that is expected to appear in the data returned
            by the target server against which the check is run.
            Currently, only the first entry in the ``content_matchers``
            list is supported, and additional entries will be ignored.
            This field is optional and should only be specified if a
            content match is required as part of the/ Uptime check.
        selected_regions (Sequence[google.cloud.monitoring_v3.types.UptimeCheckRegion]):
            The list of regions from which the check will
            be run. Some regions contain one location, and
            others contain more than one. If this field is
            specified, enough regions must be provided to
            include a minimum of 3 locations.  Not
            specifying this field will result in Uptime
            checks running from all available regions.
        is_internal (bool):
            If this is ``true``, then checks are made only from the
            'internal_checkers'. If it is ``false``, then checks are
            made only from the 'selected_regions'. It is an error to
            provide 'selected_regions' when is_internal is ``true``, or
            to provide 'internal_checkers' when is_internal is
            ``false``.
        internal_checkers (Sequence[google.cloud.monitoring_v3.types.InternalChecker]):
            The internal checkers that this check will egress from. If
            ``is_internal`` is ``true`` and this list is empty, the
            check will egress from all the InternalCheckers configured
            for the project that owns this ``UptimeCheckConfig``.
    """

    class ResourceGroup(proto.Message):
        r"""The resource submessage for group checks. It can be used
        instead of a monitored resource, when multiple resources are
        being monitored.

        Attributes:
            group_id (str):
                The group of resources being monitored. Should be only the
                ``[GROUP_ID]``, and not the full-path
                ``projects/[PROJECT_ID_OR_NUMBER]/groups/[GROUP_ID]``.
            resource_type (google.cloud.monitoring_v3.types.GroupResourceType):
                The resource type of the group members.
        """

        group_id = proto.Field(proto.STRING, number=1,)
        resource_type = proto.Field(proto.ENUM, number=2, enum="GroupResourceType",)

    class HttpCheck(proto.Message):
        r"""Information involved in an HTTP/HTTPS Uptime check request.

        Attributes:
            request_method (google.cloud.monitoring_v3.types.UptimeCheckConfig.HttpCheck.RequestMethod):
                The HTTP request method to use for the check. If set to
                ``METHOD_UNSPECIFIED`` then ``request_method`` defaults to
                ``GET``.
            use_ssl (bool):
                If ``true``, use HTTPS instead of HTTP to run the check.
            path (str):
                Optional (defaults to "/"). The path to the page against
                which to run the check. Will be combined with the ``host``
                (specified within the ``monitored_resource``) and ``port``
                to construct the full URL. If the provided path does not
                begin with "/", a "/" will be prepended automatically.
            port (int):
                Optional (defaults to 80 when ``use_ssl`` is ``false``, and
                443 when ``use_ssl`` is ``true``). The TCP port on the HTTP
                server against which to run the check. Will be combined with
                host (specified within the ``monitored_resource``) and
                ``path`` to construct the full URL.
            auth_info (google.cloud.monitoring_v3.types.UptimeCheckConfig.HttpCheck.BasicAuthentication):
                The authentication information. Optional when
                creating an HTTP check; defaults to empty.
            mask_headers (bool):
                Boolean specifying whether to encrypt the header
                information. Encryption should be specified for any headers
                related to authentication that you do not wish to be seen
                when retrieving the configuration. The server will be
                responsible for encrypting the headers. On Get/List calls,
                if ``mask_headers`` is set to ``true`` then the headers will
                be obscured with ``******.``
            headers (Sequence[google.cloud.monitoring_v3.types.UptimeCheckConfig.HttpCheck.HeadersEntry]):
                The list of headers to send as part of the
                Uptime check request. If two headers have the
                same key and different values, they should be
                entered as a single header, with the value being
                a comma-separated list of all the desired values
                as described at
                https://www.w3.org/Protocols/rfc2616/rfc2616.txt
                (page 31). Entering two separate headers with
                the same key in a Create call will cause the
                first to be overwritten by the second. The
                maximum number of headers allowed is 100.
            content_type (google.cloud.monitoring_v3.types.UptimeCheckConfig.HttpCheck.ContentType):
                The content type header to use for the check. The following
                configurations result in errors:

                1. Content type is specified in both the ``headers`` field
                   and the ``content_type`` field.
                2. Request method is ``GET`` and ``content_type`` is not
                   ``TYPE_UNSPECIFIED``
                3. Request method is ``POST`` and ``content_type`` is
                   ``TYPE_UNSPECIFIED``.
                4. Request method is ``POST`` and a "Content-Type" header is
                   provided via ``headers`` field. The ``content_type``
                   field should be used instead.
            validate_ssl (bool):
                Boolean specifying whether to include SSL certificate
                validation as a part of the Uptime check. Only applies to
                checks where ``monitored_resource`` is set to
                ``uptime_url``. If ``use_ssl`` is ``false``, setting
                ``validate_ssl`` to ``true`` has no effect.
            body (bytes):
                The request body associated with the HTTP POST request. If
                ``content_type`` is ``URL_ENCODED``, the body passed in must
                be URL-encoded. Users can provide a ``Content-Length``
                header via the ``headers`` field or the API will do so. If
                the ``request_method`` is ``GET`` and ``body`` is not empty,
                the API will return an error. The maximum byte size is 1
                megabyte. Note: As with all ``bytes`` fields, JSON
                representations are base64 encoded. e.g.: "foo=bar" in
                URL-encoded form is "foo%3Dbar" and in base64 encoding is
                "Zm9vJTI1M0RiYXI=".
        """

        class RequestMethod(proto.Enum):
            r"""The HTTP request method options."""
            METHOD_UNSPECIFIED = 0
            GET = 1
            POST = 2

        class ContentType(proto.Enum):
            r"""Header options corresponding to the content type of a HTTP
            request body.
            """
            TYPE_UNSPECIFIED = 0
            URL_ENCODED = 1

        class BasicAuthentication(proto.Message):
            r"""The authentication parameters to provide to the specified resource
            or URL that requires a username and password. Currently, only `Basic
            HTTP authentication <https://tools.ietf.org/html/rfc7617>`__ is
            supported in Uptime checks.

            Attributes:
                username (str):
                    The username to use when authenticating with
                    the HTTP server.
                password (str):
                    The password to use when authenticating with
                    the HTTP server.
            """

            username = proto.Field(proto.STRING, number=1,)
            password = proto.Field(proto.STRING, number=2,)

        request_method = proto.Field(
            proto.ENUM, number=8, enum="UptimeCheckConfig.HttpCheck.RequestMethod",
        )
        use_ssl = proto.Field(proto.BOOL, number=1,)
        path = proto.Field(proto.STRING, number=2,)
        port = proto.Field(proto.INT32, number=3,)
        auth_info = proto.Field(
            proto.MESSAGE,
            number=4,
            message="UptimeCheckConfig.HttpCheck.BasicAuthentication",
        )
        mask_headers = proto.Field(proto.BOOL, number=5,)
        headers = proto.MapField(proto.STRING, proto.STRING, number=6,)
        content_type = proto.Field(
            proto.ENUM, number=9, enum="UptimeCheckConfig.HttpCheck.ContentType",
        )
        validate_ssl = proto.Field(proto.BOOL, number=7,)
        body = proto.Field(proto.BYTES, number=10,)

    class TcpCheck(proto.Message):
        r"""Information required for a TCP Uptime check request.

        Attributes:
            port (int):
                The TCP port on the server against which to run the check.
                Will be combined with host (specified within the
                ``monitored_resource``) to construct the full URL. Required.
        """

        port = proto.Field(proto.INT32, number=1,)

    class ContentMatcher(proto.Message):
        r"""Optional. Used to perform content matching. This allows
        matching based on substrings and regular expressions, together
        with their negations. Only the first 4&nbsp;MB of an HTTP or
        HTTPS check's response (and the first 1&nbsp;MB of a TCP check's
        response) are examined for purposes of content matching.

        Attributes:
            content (str):
                String or regex content to match. Maximum 1024 bytes. An
                empty ``content`` string indicates no content matching is to
                be performed.
            matcher (google.cloud.monitoring_v3.types.UptimeCheckConfig.ContentMatcher.ContentMatcherOption):
                The type of content matcher that will be applied to the
                server output, compared to the ``content`` string when the
                check is run.
        """

        class ContentMatcherOption(proto.Enum):
            r"""Options to perform content matching."""
            CONTENT_MATCHER_OPTION_UNSPECIFIED = 0
            CONTAINS_STRING = 1
            NOT_CONTAINS_STRING = 2
            MATCHES_REGEX = 3
            NOT_MATCHES_REGEX = 4

        content = proto.Field(proto.STRING, number=1,)
        matcher = proto.Field(
            proto.ENUM,
            number=2,
            enum="UptimeCheckConfig.ContentMatcher.ContentMatcherOption",
        )

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    monitored_resource = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="resource",
        message=monitored_resource_pb2.MonitoredResource,
    )
    resource_group = proto.Field(
        proto.MESSAGE, number=4, oneof="resource", message=ResourceGroup,
    )
    http_check = proto.Field(
        proto.MESSAGE, number=5, oneof="check_request_type", message=HttpCheck,
    )
    tcp_check = proto.Field(
        proto.MESSAGE, number=6, oneof="check_request_type", message=TcpCheck,
    )
    period = proto.Field(proto.MESSAGE, number=7, message=duration_pb2.Duration,)
    timeout = proto.Field(proto.MESSAGE, number=8, message=duration_pb2.Duration,)
    content_matchers = proto.RepeatedField(
        proto.MESSAGE, number=9, message=ContentMatcher,
    )
    selected_regions = proto.RepeatedField(
        proto.ENUM, number=10, enum="UptimeCheckRegion",
    )
    is_internal = proto.Field(proto.BOOL, number=15,)
    internal_checkers = proto.RepeatedField(
        proto.MESSAGE, number=14, message="InternalChecker",
    )


class UptimeCheckIp(proto.Message):
    r"""Contains the region, location, and list of IP
    addresses where checkers in the location run from.

    Attributes:
        region (google.cloud.monitoring_v3.types.UptimeCheckRegion):
            A broad region category in which the IP
            address is located.
        location (str):
            A more specific location within the region
            that typically encodes a particular
            city/town/metro (and its containing
            state/province or country) within the broader
            umbrella region category.
        ip_address (str):
            The IP address from which the Uptime check
            originates. This is a fully specified IP address
            (not an IP address range). Most IP addresses, as
            of this publication, are in IPv4 format;
            however, one should not rely on the IP addresses
            being in IPv4 format indefinitely, and should
            support interpreting this field in either IPv4
            or IPv6 format.
    """

    region = proto.Field(proto.ENUM, number=1, enum="UptimeCheckRegion",)
    location = proto.Field(proto.STRING, number=2,)
    ip_address = proto.Field(proto.STRING, number=3,)


__all__ = tuple(sorted(__protobuf__.manifest))
