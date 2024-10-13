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
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.network_management_v1.types import trace

__protobuf__ = proto.module(
    package="google.cloud.networkmanagement.v1",
    manifest={
        "ConnectivityTest",
        "Endpoint",
        "ReachabilityDetails",
        "LatencyPercentile",
        "LatencyDistribution",
        "ProbingDetails",
    },
)


class ConnectivityTest(proto.Message):
    r"""A Connectivity Test for a network reachability analysis.

    Attributes:
        name (str):
            Required. Unique name of the resource using the form:
            ``projects/{project_id}/locations/global/connectivityTests/{test_id}``
        description (str):
            The user-supplied description of the
            Connectivity Test. Maximum of 512 characters.
        source (google.cloud.network_management_v1.types.Endpoint):
            Required. Source specification of the
            Connectivity Test.
            You can use a combination of source IP address,
            virtual machine (VM) instance, or Compute Engine
            network to uniquely identify the source
            location.

            Examples:

            If the source IP address is an internal IP
            address within a Google Cloud Virtual Private
            Cloud (VPC) network, then you must also specify
            the VPC network. Otherwise, specify the VM
            instance, which already contains its internal IP
            address and VPC network information.

            If the source of the test is within an
            on-premises network, then you must provide the
            destination VPC network.

            If the source endpoint is a Compute Engine VM
            instance with multiple network interfaces, the
            instance itself is not sufficient to identify
            the endpoint. So, you must also specify the
            source IP address or VPC network.

            A reachability analysis proceeds even if the
            source location is ambiguous. However, the test
            result may include endpoints that you don't
            intend to test.
        destination (google.cloud.network_management_v1.types.Endpoint):
            Required. Destination specification of the
            Connectivity Test.
            You can use a combination of destination IP
            address, Compute Engine VM instance, or VPC
            network to uniquely identify the destination
            location.

            Even if the destination IP address is not
            unique, the source IP location is unique.
            Usually, the analysis can infer the destination
            endpoint from route information.

            If the destination you specify is a VM instance
            and the instance has multiple network
            interfaces, then you must also specify either a
            destination IP address  or VPC network to
            identify the destination interface.

            A reachability analysis proceeds even if the
            destination location is ambiguous. However, the
            result can include endpoints that you don't
            intend to test.
        protocol (str):
            IP Protocol of the test. When not provided,
            "TCP" is assumed.
        related_projects (MutableSequence[str]):
            Other projects that may be relevant for
            reachability analysis. This is applicable to
            scenarios where a test can cross project
            boundaries.
        display_name (str):
            Output only. The display name of a
            Connectivity Test.
        labels (MutableMapping[str, str]):
            Resource labels to represent user-provided
            metadata.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the test was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the test's
            configuration was updated.
        reachability_details (google.cloud.network_management_v1.types.ReachabilityDetails):
            Output only. The reachability details of this
            test from the latest run. The details are
            updated when creating a new test, updating an
            existing test, or triggering a one-time rerun of
            an existing test.
        probing_details (google.cloud.network_management_v1.types.ProbingDetails):
            Output only. The probing details of this test
            from the latest run, present for applicable
            tests only. The details are updated when
            creating a new test, updating an existing test,
            or triggering a one-time rerun of an existing
            test.
        bypass_firewall_checks (bool):
            Whether the test should skip firewall
            checking. If not provided, we assume false.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    source: "Endpoint" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Endpoint",
    )
    destination: "Endpoint" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Endpoint",
    )
    protocol: str = proto.Field(
        proto.STRING,
        number=5,
    )
    related_projects: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=7,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=8,
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
    reachability_details: "ReachabilityDetails" = proto.Field(
        proto.MESSAGE,
        number=12,
        message="ReachabilityDetails",
    )
    probing_details: "ProbingDetails" = proto.Field(
        proto.MESSAGE,
        number=14,
        message="ProbingDetails",
    )
    bypass_firewall_checks: bool = proto.Field(
        proto.BOOL,
        number=17,
    )


class Endpoint(proto.Message):
    r"""Source or destination of the Connectivity Test.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        ip_address (str):
            The IP address of the endpoint, which can be
            an external or internal IP.
        port (int):
            The IP protocol port of the endpoint.
            Only applicable when protocol is TCP or UDP.
        instance (str):
            A Compute Engine instance URI.
        forwarding_rule (str):
            A forwarding rule and its corresponding IP
            address represent the frontend configuration of
            a Google Cloud load balancer. Forwarding rules
            are also used for protocol forwarding, Private
            Service Connect and other network services to
            provide forwarding information in the control
            plane. Format:

            projects/{project}/global/forwardingRules/{id}
            or
            projects/{project}/regions/{region}/forwardingRules/{id}
        forwarding_rule_target (google.cloud.network_management_v1.types.Endpoint.ForwardingRuleTarget):
            Output only. Specifies the type of the target
            of the forwarding rule.

            This field is a member of `oneof`_ ``_forwarding_rule_target``.
        load_balancer_id (str):
            Output only. ID of the load balancer the
            forwarding rule points to. Empty for forwarding
            rules not related to load balancers.

            This field is a member of `oneof`_ ``_load_balancer_id``.
        load_balancer_type (google.cloud.network_management_v1.types.LoadBalancerType):
            Output only. Type of the load balancer the
            forwarding rule points to.

            This field is a member of `oneof`_ ``_load_balancer_type``.
        gke_master_cluster (str):
            A cluster URI for `Google Kubernetes Engine
            master <https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-architecture>`__.
        cloud_sql_instance (str):
            A `Cloud SQL <https://cloud.google.com/sql>`__ instance URI.
        cloud_function (google.cloud.network_management_v1.types.Endpoint.CloudFunctionEndpoint):
            A `Cloud Function <https://cloud.google.com/functions>`__.
        app_engine_version (google.cloud.network_management_v1.types.Endpoint.AppEngineVersionEndpoint):
            An `App Engine <https://cloud.google.com/appengine>`__
            `service
            version <https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.services.versions>`__.
        cloud_run_revision (google.cloud.network_management_v1.types.Endpoint.CloudRunRevisionEndpoint):
            A `Cloud Run <https://cloud.google.com/run>`__
            `revision <https://cloud.google.com/run/docs/reference/rest/v1/namespaces.revisions/get>`__
        network (str):
            A Compute Engine network URI.
        network_type (google.cloud.network_management_v1.types.Endpoint.NetworkType):
            Type of the network where the endpoint is
            located. Applicable only to source endpoint, as
            destination network type can be inferred from
            the source.
        project_id (str):
            Project ID where the endpoint is located.
            The Project ID can be derived from the URI if
            you provide a VM instance or network URI.
            The following are two cases where you must
            provide the project ID:

            1. Only the IP address is specified, and the IP
                address is within a Google Cloud project.
            2. When you are using Shared VPC and the IP
                address that you provide is from the service
                project. In this case, the network that the
                IP address resides in is defined in the host
                project.
    """

    class NetworkType(proto.Enum):
        r"""The type definition of an endpoint's network. Use one of the
        following choices:

        Values:
            NETWORK_TYPE_UNSPECIFIED (0):
                Default type if unspecified.
            GCP_NETWORK (1):
                A network hosted within Google Cloud.
                To receive more detailed output, specify the URI
                for the source or destination network.
            NON_GCP_NETWORK (2):
                A network hosted outside of Google Cloud.
                This can be an on-premises network, or a network
                hosted by another cloud provider.
        """
        NETWORK_TYPE_UNSPECIFIED = 0
        GCP_NETWORK = 1
        NON_GCP_NETWORK = 2

    class ForwardingRuleTarget(proto.Enum):
        r"""Type of the target of a forwarding rule.

        Values:
            FORWARDING_RULE_TARGET_UNSPECIFIED (0):
                Forwarding rule target is unknown.
            INSTANCE (1):
                Compute Engine instance for protocol
                forwarding.
            LOAD_BALANCER (2):
                Load Balancer. The specific type can be found from
                [load_balancer_type]
                [google.cloud.networkmanagement.v1.Endpoint.load_balancer_type].
            VPN_GATEWAY (3):
                Classic Cloud VPN Gateway.
            PSC (4):
                Forwarding Rule is a Private Service Connect
                endpoint.
        """
        FORWARDING_RULE_TARGET_UNSPECIFIED = 0
        INSTANCE = 1
        LOAD_BALANCER = 2
        VPN_GATEWAY = 3
        PSC = 4

    class CloudFunctionEndpoint(proto.Message):
        r"""Wrapper for Cloud Function attributes.

        Attributes:
            uri (str):
                A `Cloud Function <https://cloud.google.com/functions>`__
                name.
        """

        uri: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class AppEngineVersionEndpoint(proto.Message):
        r"""Wrapper for the App Engine service version attributes.

        Attributes:
            uri (str):
                An `App Engine <https://cloud.google.com/appengine>`__
                `service
                version <https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.services.versions>`__
                name.
        """

        uri: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class CloudRunRevisionEndpoint(proto.Message):
        r"""Wrapper for Cloud Run revision attributes.

        Attributes:
            uri (str):
                A `Cloud Run <https://cloud.google.com/run>`__
                `revision <https://cloud.google.com/run/docs/reference/rest/v1/namespaces.revisions/get>`__
                URI. The format is:
                projects/{project}/locations/{location}/revisions/{revision}
        """

        uri: str = proto.Field(
            proto.STRING,
            number=1,
        )

    ip_address: str = proto.Field(
        proto.STRING,
        number=1,
    )
    port: int = proto.Field(
        proto.INT32,
        number=2,
    )
    instance: str = proto.Field(
        proto.STRING,
        number=3,
    )
    forwarding_rule: str = proto.Field(
        proto.STRING,
        number=13,
    )
    forwarding_rule_target: ForwardingRuleTarget = proto.Field(
        proto.ENUM,
        number=14,
        optional=True,
        enum=ForwardingRuleTarget,
    )
    load_balancer_id: str = proto.Field(
        proto.STRING,
        number=15,
        optional=True,
    )
    load_balancer_type: trace.LoadBalancerType = proto.Field(
        proto.ENUM,
        number=16,
        optional=True,
        enum=trace.LoadBalancerType,
    )
    gke_master_cluster: str = proto.Field(
        proto.STRING,
        number=7,
    )
    cloud_sql_instance: str = proto.Field(
        proto.STRING,
        number=8,
    )
    cloud_function: CloudFunctionEndpoint = proto.Field(
        proto.MESSAGE,
        number=10,
        message=CloudFunctionEndpoint,
    )
    app_engine_version: AppEngineVersionEndpoint = proto.Field(
        proto.MESSAGE,
        number=11,
        message=AppEngineVersionEndpoint,
    )
    cloud_run_revision: CloudRunRevisionEndpoint = proto.Field(
        proto.MESSAGE,
        number=12,
        message=CloudRunRevisionEndpoint,
    )
    network: str = proto.Field(
        proto.STRING,
        number=4,
    )
    network_type: NetworkType = proto.Field(
        proto.ENUM,
        number=5,
        enum=NetworkType,
    )
    project_id: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ReachabilityDetails(proto.Message):
    r"""Results of the configuration analysis from the last run of
    the test.

    Attributes:
        result (google.cloud.network_management_v1.types.ReachabilityDetails.Result):
            The overall result of the test's
            configuration analysis.
        verify_time (google.protobuf.timestamp_pb2.Timestamp):
            The time of the configuration analysis.
        error (google.rpc.status_pb2.Status):
            The details of a failure or a cancellation of
            reachability analysis.
        traces (MutableSequence[google.cloud.network_management_v1.types.Trace]):
            Result may contain a list of traces if a test
            has multiple possible paths in the network, such
            as when destination endpoint is a load balancer
            with multiple backends.
    """

    class Result(proto.Enum):
        r"""The overall result of the test's configuration analysis.

        Values:
            RESULT_UNSPECIFIED (0):
                No result was specified.
            REACHABLE (1):
                Possible scenarios are:

                -  The configuration analysis determined that a packet
                   originating from the source is expected to reach the
                   destination.
                -  The analysis didn't complete because the user lacks
                   permission for some of the resources in the trace.
                   However, at the time the user's permission became
                   insufficient, the trace had been successful so far.
            UNREACHABLE (2):
                A packet originating from the source is
                expected to be dropped before reaching the
                destination.
            AMBIGUOUS (4):
                The source and destination endpoints do not
                uniquely identify the test location in the
                network, and the reachability result contains
                multiple traces. For some traces, a packet could
                be delivered, and for others, it would not be.
                This result is also assigned to configuration
                analysis of return path if on its own it should
                be REACHABLE, but configuration analysis of
                forward path is AMBIGUOUS.
            UNDETERMINED (5):
                The configuration analysis did not complete. Possible
                reasons are:

                -  A permissions error occurred--for example, the user might
                   not have read permission for all of the resources named
                   in the test.
                -  An internal error occurred.
                -  The analyzer received an invalid or unsupported argument
                   or was unable to identify a known endpoint.
        """
        RESULT_UNSPECIFIED = 0
        REACHABLE = 1
        UNREACHABLE = 2
        AMBIGUOUS = 4
        UNDETERMINED = 5

    result: Result = proto.Field(
        proto.ENUM,
        number=1,
        enum=Result,
    )
    verify_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=3,
        message=status_pb2.Status,
    )
    traces: MutableSequence[trace.Trace] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=trace.Trace,
    )


class LatencyPercentile(proto.Message):
    r"""Latency percentile rank and value.

    Attributes:
        percent (int):
            Percentage of samples this data point applies
            to.
        latency_micros (int):
            percent-th percentile of latency observed, in
            microseconds. Fraction of percent/100 of samples
            have latency lower or equal to the value of this
            field.
    """

    percent: int = proto.Field(
        proto.INT32,
        number=1,
    )
    latency_micros: int = proto.Field(
        proto.INT64,
        number=2,
    )


class LatencyDistribution(proto.Message):
    r"""Describes measured latency distribution.

    Attributes:
        latency_percentiles (MutableSequence[google.cloud.network_management_v1.types.LatencyPercentile]):
            Representative latency percentiles.
    """

    latency_percentiles: MutableSequence["LatencyPercentile"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="LatencyPercentile",
    )


class ProbingDetails(proto.Message):
    r"""Results of active probing from the last run of the test.

    Attributes:
        result (google.cloud.network_management_v1.types.ProbingDetails.ProbingResult):
            The overall result of active probing.
        verify_time (google.protobuf.timestamp_pb2.Timestamp):
            The time that reachability was assessed
            through active probing.
        error (google.rpc.status_pb2.Status):
            Details about an internal failure or the
            cancellation of active probing.
        abort_cause (google.cloud.network_management_v1.types.ProbingDetails.ProbingAbortCause):
            The reason probing was aborted.
        sent_probe_count (int):
            Number of probes sent.
        successful_probe_count (int):
            Number of probes that reached the
            destination.
        endpoint_info (google.cloud.network_management_v1.types.EndpointInfo):
            The source and destination endpoints derived
            from the test input and used for active probing.
        probing_latency (google.cloud.network_management_v1.types.LatencyDistribution):
            Latency as measured by active probing in one
            direction: from the source to the destination
            endpoint.
        destination_egress_location (google.cloud.network_management_v1.types.ProbingDetails.EdgeLocation):
            The EdgeLocation from which a packet destined
            for/originating from the internet will egress/ingress the
            Google network. This will only be populated for a
            connectivity test which has an internet destination/source
            address. The absence of this field *must not* be used as an
            indication that the destination/source is part of the Google
            network.
    """

    class ProbingResult(proto.Enum):
        r"""Overall probing result of the test.

        Values:
            PROBING_RESULT_UNSPECIFIED (0):
                No result was specified.
            REACHABLE (1):
                At least 95% of packets reached the
                destination.
            UNREACHABLE (2):
                No packets reached the destination.
            REACHABILITY_INCONSISTENT (3):
                Less than 95% of packets reached the
                destination.
            UNDETERMINED (4):
                Reachability could not be determined. Possible reasons are:

                -  The user lacks permission to access some of the network
                   resources required to run the test.
                -  No valid source endpoint could be derived from the
                   request.
                -  An internal error occurred.
        """
        PROBING_RESULT_UNSPECIFIED = 0
        REACHABLE = 1
        UNREACHABLE = 2
        REACHABILITY_INCONSISTENT = 3
        UNDETERMINED = 4

    class ProbingAbortCause(proto.Enum):
        r"""Abort cause types.

        Values:
            PROBING_ABORT_CAUSE_UNSPECIFIED (0):
                No reason was specified.
            PERMISSION_DENIED (1):
                The user lacks permission to access some of
                the network resources required to run the test.
            NO_SOURCE_LOCATION (2):
                No valid source endpoint could be derived
                from the request.
        """
        PROBING_ABORT_CAUSE_UNSPECIFIED = 0
        PERMISSION_DENIED = 1
        NO_SOURCE_LOCATION = 2

    class EdgeLocation(proto.Message):
        r"""Representation of a network edge location as per
        https://cloud.google.com/vpc/docs/edge-locations.

        Attributes:
            metropolitan_area (str):
                Name of the metropolitan area.
        """

        metropolitan_area: str = proto.Field(
            proto.STRING,
            number=1,
        )

    result: ProbingResult = proto.Field(
        proto.ENUM,
        number=1,
        enum=ProbingResult,
    )
    verify_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=3,
        message=status_pb2.Status,
    )
    abort_cause: ProbingAbortCause = proto.Field(
        proto.ENUM,
        number=4,
        enum=ProbingAbortCause,
    )
    sent_probe_count: int = proto.Field(
        proto.INT32,
        number=5,
    )
    successful_probe_count: int = proto.Field(
        proto.INT32,
        number=6,
    )
    endpoint_info: trace.EndpointInfo = proto.Field(
        proto.MESSAGE,
        number=7,
        message=trace.EndpointInfo,
    )
    probing_latency: "LatencyDistribution" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="LatencyDistribution",
    )
    destination_egress_location: EdgeLocation = proto.Field(
        proto.MESSAGE,
        number=9,
        message=EdgeLocation,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
