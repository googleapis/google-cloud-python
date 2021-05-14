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

from google.cloud.appengine_admin_v1.types import app_yaml
from google.cloud.appengine_admin_v1.types import deploy
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.appengine.v1",
    manifest={
        "InboundServiceType",
        "ServingStatus",
        "Version",
        "EndpointsApiService",
        "AutomaticScaling",
        "BasicScaling",
        "ManualScaling",
        "CpuUtilization",
        "RequestUtilization",
        "DiskUtilization",
        "NetworkUtilization",
        "StandardSchedulerSettings",
        "Network",
        "Volume",
        "Resources",
        "VpcAccessConnector",
        "Entrypoint",
    },
)


class InboundServiceType(proto.Enum):
    r"""Available inbound services."""
    INBOUND_SERVICE_UNSPECIFIED = 0
    INBOUND_SERVICE_MAIL = 1
    INBOUND_SERVICE_MAIL_BOUNCE = 2
    INBOUND_SERVICE_XMPP_ERROR = 3
    INBOUND_SERVICE_XMPP_MESSAGE = 4
    INBOUND_SERVICE_XMPP_SUBSCRIBE = 5
    INBOUND_SERVICE_XMPP_PRESENCE = 6
    INBOUND_SERVICE_CHANNEL_PRESENCE = 7
    INBOUND_SERVICE_WARMUP = 9


class ServingStatus(proto.Enum):
    r"""Run states of a version."""
    SERVING_STATUS_UNSPECIFIED = 0
    SERVING = 1
    STOPPED = 2


class Version(proto.Message):
    r"""A Version resource is a specific set of source code and
    configuration files that are deployed into a service.

    Attributes:
        name (str):
            Full path to the Version resource in the API. Example:
            ``apps/myapp/services/default/versions/v1``.

            @OutputOnly
        id (str):
            Relative name of the version within the service. Example:
            ``v1``. Version names can contain only lowercase letters,
            numbers, or hyphens. Reserved names: "default", "latest",
            and any name with the prefix "ah-".
        automatic_scaling (google.cloud.appengine_admin_v1.types.AutomaticScaling):
            Automatic scaling is based on request rate,
            response latencies, and other application
            metrics. Instances are dynamically created and
            destroyed as needed in order to handle traffic.
        basic_scaling (google.cloud.appengine_admin_v1.types.BasicScaling):
            A service with basic scaling will create an
            instance when the application receives a
            request. The instance will be turned down when
            the app becomes idle. Basic scaling is ideal for
            work that is intermittent or driven by user
            activity.
        manual_scaling (google.cloud.appengine_admin_v1.types.ManualScaling):
            A service with manual scaling runs
            continuously, allowing you to perform complex
            initialization and rely on the state of its
            memory over time. Manually scaled versions are
            sometimes referred to as "backends".
        inbound_services (Sequence[google.cloud.appengine_admin_v1.types.InboundServiceType]):
            Before an application can receive email or
            XMPP messages, the application must be
            configured to enable the service.
        instance_class (str):
            Instance class that is used to run this version. Valid
            values are:

            -  AutomaticScaling: ``F1``, ``F2``, ``F4``, ``F4_1G``
            -  ManualScaling or BasicScaling: ``B1``, ``B2``, ``B4``,
               ``B8``, ``B4_1G``

            Defaults to ``F1`` for AutomaticScaling and ``B1`` for
            ManualScaling or BasicScaling.
        network (google.cloud.appengine_admin_v1.types.Network):
            Extra network settings.
            Only applicable in the App Engine flexible
            environment.
        zones (Sequence[str]):
            The Google Compute Engine zones that are
            supported by this version in the App Engine
            flexible environment. Deprecated.
        resources (google.cloud.appengine_admin_v1.types.Resources):
            Machine resources for this version.
            Only applicable in the App Engine flexible
            environment.
        runtime (str):
            Desired runtime. Example: ``python27``.
        runtime_channel (str):
            The channel of the runtime to use. Only available for some
            runtimes. Defaults to the ``default`` channel.
        threadsafe (bool):
            Whether multiple requests can be dispatched
            to this version at once.
        vm (bool):
            Whether to deploy this version in a container
            on a virtual machine.
        beta_settings (Sequence[google.cloud.appengine_admin_v1.types.Version.BetaSettingsEntry]):
            Metadata settings that are supplied to this
            version to enable beta runtime features.
        env (str):
            App Engine execution environment for this version.

            Defaults to ``standard``.
        serving_status (google.cloud.appengine_admin_v1.types.ServingStatus):
            Current serving status of this version. Only the versions
            with a ``SERVING`` status create instances and can be
            billed.

            ``SERVING_STATUS_UNSPECIFIED`` is an invalid value. Defaults
            to ``SERVING``.
        created_by (str):
            Email address of the user who created this
            version.
            @OutputOnly
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Time that this version was created.
            @OutputOnly
        disk_usage_bytes (int):
            Total size in bytes of all the files that are
            included in this version and currently hosted on
            the App Engine disk.
            @OutputOnly
        runtime_api_version (str):
            The version of the API in the given runtime
            environment. Please see the app.yaml reference
            for valid values at
            https://cloud.google.com/appengine/docs/standard/<language>/config/appref
        runtime_main_executable_path (str):
            The path or name of the app's main
            executable.
        service_account (str):
            The identity that the deployed version will
            run as. Admin API will use the App Engine
            Appspot service account as default if this field
            is neither provided in app.yaml file nor through
            CLI flag.
        handlers (Sequence[google.cloud.appengine_admin_v1.types.UrlMap]):
            An ordered list of URL-matching patterns that should be
            applied to incoming requests. The first matching URL handles
            the request and other request handlers are not attempted.

            Only returned in ``GET`` requests if ``view=FULL`` is set.
        error_handlers (Sequence[google.cloud.appengine_admin_v1.types.ErrorHandler]):
            Custom static error pages. Limited to 10KB per page.

            Only returned in ``GET`` requests if ``view=FULL`` is set.
        libraries (Sequence[google.cloud.appengine_admin_v1.types.Library]):
            Configuration for third-party Python runtime libraries that
            are required by the application.

            Only returned in ``GET`` requests if ``view=FULL`` is set.
        api_config (google.cloud.appengine_admin_v1.types.ApiConfigHandler):
            Serving configuration for `Google Cloud
            Endpoints <https://cloud.google.com/appengine/docs/python/endpoints/>`__.

            Only returned in ``GET`` requests if ``view=FULL`` is set.
        env_variables (Sequence[google.cloud.appengine_admin_v1.types.Version.EnvVariablesEntry]):
            Environment variables available to the application.

            Only returned in ``GET`` requests if ``view=FULL`` is set.
        build_env_variables (Sequence[google.cloud.appengine_admin_v1.types.Version.BuildEnvVariablesEntry]):
            Environment variables available to the build environment.

            Only returned in ``GET`` requests if ``view=FULL`` is set.
        default_expiration (google.protobuf.duration_pb2.Duration):
            Duration that static files should be cached by web proxies
            and browsers. Only applicable if the corresponding
            `StaticFilesHandler <https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.services.versions#StaticFilesHandler>`__
            does not specify its own expiration time.

            Only returned in ``GET`` requests if ``view=FULL`` is set.
        health_check (google.cloud.appengine_admin_v1.types.HealthCheck):
            Configures health checking for instances. Unhealthy
            instances are stopped and replaced with new instances. Only
            applicable in the App Engine flexible environment.

            Only returned in ``GET`` requests if ``view=FULL`` is set.
        readiness_check (google.cloud.appengine_admin_v1.types.ReadinessCheck):
            Configures readiness health checking for instances.
            Unhealthy instances are not put into the backend traffic
            rotation.

            Only returned in ``GET`` requests if ``view=FULL`` is set.
        liveness_check (google.cloud.appengine_admin_v1.types.LivenessCheck):
            Configures liveness health checking for instances. Unhealthy
            instances are stopped and replaced with new instances

            Only returned in ``GET`` requests if ``view=FULL`` is set.
        nobuild_files_regex (str):
            Files that match this pattern will not be built into this
            version. Only applicable for Go runtimes.

            Only returned in ``GET`` requests if ``view=FULL`` is set.
        deployment (google.cloud.appengine_admin_v1.types.Deployment):
            Code and application artifacts that make up this version.

            Only returned in ``GET`` requests if ``view=FULL`` is set.
        version_url (str):
            Serving URL for this version. Example:
            "https://myversion-dot-myservice-dot-
            myapp.appspot.com"
            @OutputOnly
        endpoints_api_service (google.cloud.appengine_admin_v1.types.EndpointsApiService):
            Cloud Endpoints configuration.

            If endpoints_api_service is set, the Cloud Endpoints
            Extensible Service Proxy will be provided to serve the API
            implemented by the app.
        entrypoint (google.cloud.appengine_admin_v1.types.Entrypoint):
            The entrypoint for the application.
        vpc_access_connector (google.cloud.appengine_admin_v1.types.VpcAccessConnector):
            Enables VPC connectivity for standard apps.
    """

    name = proto.Field(proto.STRING, number=1,)
    id = proto.Field(proto.STRING, number=2,)
    automatic_scaling = proto.Field(
        proto.MESSAGE, number=3, oneof="scaling", message="AutomaticScaling",
    )
    basic_scaling = proto.Field(
        proto.MESSAGE, number=4, oneof="scaling", message="BasicScaling",
    )
    manual_scaling = proto.Field(
        proto.MESSAGE, number=5, oneof="scaling", message="ManualScaling",
    )
    inbound_services = proto.RepeatedField(
        proto.ENUM, number=6, enum="InboundServiceType",
    )
    instance_class = proto.Field(proto.STRING, number=7,)
    network = proto.Field(proto.MESSAGE, number=8, message="Network",)
    zones = proto.RepeatedField(proto.STRING, number=118,)
    resources = proto.Field(proto.MESSAGE, number=9, message="Resources",)
    runtime = proto.Field(proto.STRING, number=10,)
    runtime_channel = proto.Field(proto.STRING, number=117,)
    threadsafe = proto.Field(proto.BOOL, number=11,)
    vm = proto.Field(proto.BOOL, number=12,)
    beta_settings = proto.MapField(proto.STRING, proto.STRING, number=13,)
    env = proto.Field(proto.STRING, number=14,)
    serving_status = proto.Field(proto.ENUM, number=15, enum="ServingStatus",)
    created_by = proto.Field(proto.STRING, number=16,)
    create_time = proto.Field(
        proto.MESSAGE, number=17, message=timestamp_pb2.Timestamp,
    )
    disk_usage_bytes = proto.Field(proto.INT64, number=18,)
    runtime_api_version = proto.Field(proto.STRING, number=21,)
    runtime_main_executable_path = proto.Field(proto.STRING, number=22,)
    service_account = proto.Field(proto.STRING, number=127,)
    handlers = proto.RepeatedField(proto.MESSAGE, number=100, message=app_yaml.UrlMap,)
    error_handlers = proto.RepeatedField(
        proto.MESSAGE, number=101, message=app_yaml.ErrorHandler,
    )
    libraries = proto.RepeatedField(
        proto.MESSAGE, number=102, message=app_yaml.Library,
    )
    api_config = proto.Field(
        proto.MESSAGE, number=103, message=app_yaml.ApiConfigHandler,
    )
    env_variables = proto.MapField(proto.STRING, proto.STRING, number=104,)
    build_env_variables = proto.MapField(proto.STRING, proto.STRING, number=125,)
    default_expiration = proto.Field(
        proto.MESSAGE, number=105, message=duration_pb2.Duration,
    )
    health_check = proto.Field(proto.MESSAGE, number=106, message=app_yaml.HealthCheck,)
    readiness_check = proto.Field(
        proto.MESSAGE, number=112, message=app_yaml.ReadinessCheck,
    )
    liveness_check = proto.Field(
        proto.MESSAGE, number=113, message=app_yaml.LivenessCheck,
    )
    nobuild_files_regex = proto.Field(proto.STRING, number=107,)
    deployment = proto.Field(proto.MESSAGE, number=108, message=deploy.Deployment,)
    version_url = proto.Field(proto.STRING, number=109,)
    endpoints_api_service = proto.Field(
        proto.MESSAGE, number=110, message="EndpointsApiService",
    )
    entrypoint = proto.Field(proto.MESSAGE, number=122, message="Entrypoint",)
    vpc_access_connector = proto.Field(
        proto.MESSAGE, number=121, message="VpcAccessConnector",
    )


class EndpointsApiService(proto.Message):
    r"""`Cloud Endpoints <https://cloud.google.com/endpoints>`__
    configuration. The Endpoints API Service provides tooling for
    serving Open API and gRPC endpoints via an NGINX proxy. Only valid
    for App Engine Flexible environment deployments.

    The fields here refer to the name and configuration ID of a
    "service" resource in the `Service Management
    API <https://cloud.google.com/service-management/overview>`__.

    Attributes:
        name (str):
            Endpoints service name which is the name of
            the "service" resource in the Service Management
            API. For example
            "myapi.endpoints.myproject.cloud.goog".
        config_id (str):
            Endpoints service configuration ID as specified by the
            Service Management API. For example "2016-09-19r1".

            By default, the rollout strategy for Endpoints is
            ``RolloutStrategy.FIXED``. This means that Endpoints starts
            up with a particular configuration ID. When a new
            configuration is rolled out, Endpoints must be given the new
            configuration ID. The ``config_id`` field is used to give
            the configuration ID and is required in this case.

            Endpoints also has a rollout strategy called
            ``RolloutStrategy.MANAGED``. When using this, Endpoints
            fetches the latest configuration and does not need the
            configuration ID. In this case, ``config_id`` must be
            omitted.
        rollout_strategy (google.cloud.appengine_admin_v1.types.EndpointsApiService.RolloutStrategy):
            Endpoints rollout strategy. If ``FIXED``, ``config_id`` must
            be specified. If ``MANAGED``, ``config_id`` must be omitted.
        disable_trace_sampling (bool):
            Enable or disable trace sampling. By default,
            this is set to false for enabled.
    """

    class RolloutStrategy(proto.Enum):
        r"""Available rollout strategies."""
        UNSPECIFIED_ROLLOUT_STRATEGY = 0
        FIXED = 1
        MANAGED = 2

    name = proto.Field(proto.STRING, number=1,)
    config_id = proto.Field(proto.STRING, number=2,)
    rollout_strategy = proto.Field(proto.ENUM, number=3, enum=RolloutStrategy,)
    disable_trace_sampling = proto.Field(proto.BOOL, number=4,)


class AutomaticScaling(proto.Message):
    r"""Automatic scaling is based on request rate, response
    latencies, and other application metrics.

    Attributes:
        cool_down_period (google.protobuf.duration_pb2.Duration):
            The time period that the
            `Autoscaler <https://cloud.google.com/compute/docs/autoscaler/>`__
            should wait before it starts collecting information from a
            new instance. This prevents the autoscaler from collecting
            information when the instance is initializing, during which
            the collected usage would not be reliable. Only applicable
            in the App Engine flexible environment.
        cpu_utilization (google.cloud.appengine_admin_v1.types.CpuUtilization):
            Target scaling by CPU usage.
        max_concurrent_requests (int):
            Number of concurrent requests an automatic
            scaling instance can accept before the scheduler
            spawns a new instance.
            Defaults to a runtime-specific value.
        max_idle_instances (int):
            Maximum number of idle instances that should
            be maintained for this version.
        max_total_instances (int):
            Maximum number of instances that should be
            started to handle requests for this version.
        max_pending_latency (google.protobuf.duration_pb2.Duration):
            Maximum amount of time that a request should
            wait in the pending queue before starting a new
            instance to handle it.
        min_idle_instances (int):
            Minimum number of idle instances that should
            be maintained for this version. Only applicable
            for the default version of a service.
        min_total_instances (int):
            Minimum number of running instances that
            should be maintained for this version.
        min_pending_latency (google.protobuf.duration_pb2.Duration):
            Minimum amount of time a request should wait
            in the pending queue before starting a new
            instance to handle it.
        request_utilization (google.cloud.appengine_admin_v1.types.RequestUtilization):
            Target scaling by request utilization.
        disk_utilization (google.cloud.appengine_admin_v1.types.DiskUtilization):
            Target scaling by disk usage.
        network_utilization (google.cloud.appengine_admin_v1.types.NetworkUtilization):
            Target scaling by network usage.
        standard_scheduler_settings (google.cloud.appengine_admin_v1.types.StandardSchedulerSettings):
            Scheduler settings for standard environment.
    """

    cool_down_period = proto.Field(
        proto.MESSAGE, number=1, message=duration_pb2.Duration,
    )
    cpu_utilization = proto.Field(proto.MESSAGE, number=2, message="CpuUtilization",)
    max_concurrent_requests = proto.Field(proto.INT32, number=3,)
    max_idle_instances = proto.Field(proto.INT32, number=4,)
    max_total_instances = proto.Field(proto.INT32, number=5,)
    max_pending_latency = proto.Field(
        proto.MESSAGE, number=6, message=duration_pb2.Duration,
    )
    min_idle_instances = proto.Field(proto.INT32, number=7,)
    min_total_instances = proto.Field(proto.INT32, number=8,)
    min_pending_latency = proto.Field(
        proto.MESSAGE, number=9, message=duration_pb2.Duration,
    )
    request_utilization = proto.Field(
        proto.MESSAGE, number=10, message="RequestUtilization",
    )
    disk_utilization = proto.Field(proto.MESSAGE, number=11, message="DiskUtilization",)
    network_utilization = proto.Field(
        proto.MESSAGE, number=12, message="NetworkUtilization",
    )
    standard_scheduler_settings = proto.Field(
        proto.MESSAGE, number=20, message="StandardSchedulerSettings",
    )


class BasicScaling(proto.Message):
    r"""A service with basic scaling will create an instance when the
    application receives a request. The instance will be turned down
    when the app becomes idle. Basic scaling is ideal for work that
    is intermittent or driven by user activity.

    Attributes:
        idle_timeout (google.protobuf.duration_pb2.Duration):
            Duration of time after the last request that
            an instance must wait before the instance is
            shut down.
        max_instances (int):
            Maximum number of instances to create for
            this version.
    """

    idle_timeout = proto.Field(proto.MESSAGE, number=1, message=duration_pb2.Duration,)
    max_instances = proto.Field(proto.INT32, number=2,)


class ManualScaling(proto.Message):
    r"""A service with manual scaling runs continuously, allowing you
    to perform complex initialization and rely on the state of its
    memory over time.

    Attributes:
        instances (int):
            Number of instances to assign to the service at the start.
            This number can later be altered by using the `Modules
            API <https://cloud.google.com/appengine/docs/python/modules/functions>`__
            ``set_num_instances()`` function.
    """

    instances = proto.Field(proto.INT32, number=1,)


class CpuUtilization(proto.Message):
    r"""Target scaling by CPU usage.
    Attributes:
        aggregation_window_length (google.protobuf.duration_pb2.Duration):
            Period of time over which CPU utilization is
            calculated.
        target_utilization (float):
            Target CPU utilization ratio to maintain when
            scaling. Must be between 0 and 1.
    """

    aggregation_window_length = proto.Field(
        proto.MESSAGE, number=1, message=duration_pb2.Duration,
    )
    target_utilization = proto.Field(proto.DOUBLE, number=2,)


class RequestUtilization(proto.Message):
    r"""Target scaling by request utilization.
    Only applicable in the App Engine flexible environment.

    Attributes:
        target_request_count_per_second (int):
            Target requests per second.
        target_concurrent_requests (int):
            Target number of concurrent requests.
    """

    target_request_count_per_second = proto.Field(proto.INT32, number=1,)
    target_concurrent_requests = proto.Field(proto.INT32, number=2,)


class DiskUtilization(proto.Message):
    r"""Target scaling by disk usage.
    Only applicable in the App Engine flexible environment.

    Attributes:
        target_write_bytes_per_second (int):
            Target bytes written per second.
        target_write_ops_per_second (int):
            Target ops written per second.
        target_read_bytes_per_second (int):
            Target bytes read per second.
        target_read_ops_per_second (int):
            Target ops read per seconds.
    """

    target_write_bytes_per_second = proto.Field(proto.INT32, number=14,)
    target_write_ops_per_second = proto.Field(proto.INT32, number=15,)
    target_read_bytes_per_second = proto.Field(proto.INT32, number=16,)
    target_read_ops_per_second = proto.Field(proto.INT32, number=17,)


class NetworkUtilization(proto.Message):
    r"""Target scaling by network usage.
    Only applicable in the App Engine flexible environment.

    Attributes:
        target_sent_bytes_per_second (int):
            Target bytes sent per second.
        target_sent_packets_per_second (int):
            Target packets sent per second.
        target_received_bytes_per_second (int):
            Target bytes received per second.
        target_received_packets_per_second (int):
            Target packets received per second.
    """

    target_sent_bytes_per_second = proto.Field(proto.INT32, number=1,)
    target_sent_packets_per_second = proto.Field(proto.INT32, number=11,)
    target_received_bytes_per_second = proto.Field(proto.INT32, number=12,)
    target_received_packets_per_second = proto.Field(proto.INT32, number=13,)


class StandardSchedulerSettings(proto.Message):
    r"""Scheduler settings for standard environment.
    Attributes:
        target_cpu_utilization (float):
            Target CPU utilization ratio to maintain when
            scaling.
        target_throughput_utilization (float):
            Target throughput utilization ratio to
            maintain when scaling
        min_instances (int):
            Minimum number of instances to run for this version. Set to
            zero to disable ``min_instances`` configuration.
        max_instances (int):
            Maximum number of instances to run for this version. Set to
            zero to disable ``max_instances`` configuration.
    """

    target_cpu_utilization = proto.Field(proto.DOUBLE, number=1,)
    target_throughput_utilization = proto.Field(proto.DOUBLE, number=2,)
    min_instances = proto.Field(proto.INT32, number=3,)
    max_instances = proto.Field(proto.INT32, number=4,)


class Network(proto.Message):
    r"""Extra network settings.
    Only applicable in the App Engine flexible environment.

    Attributes:
        forwarded_ports (Sequence[str]):
            List of ports, or port pairs, to forward from
            the virtual machine to the application
            container. Only applicable in the App Engine
            flexible environment.
        instance_tag (str):
            Tag to apply to the instance during creation.
            Only applicable in the App Engine flexible
            environment.
        name (str):
            Google Compute Engine network where the virtual machines are
            created. Specify the short name, not the resource path.

            Defaults to ``default``.
        subnetwork_name (str):
            Google Cloud Platform sub-network where the virtual machines
            are created. Specify the short name, not the resource path.

            If a subnetwork name is specified, a network name will also
            be required unless it is for the default network.

            -  If the network that the instance is being created in is a
               Legacy network, then the IP address is allocated from the
               IPv4Range.
            -  If the network that the instance is being created in is
               an auto Subnet Mode Network, then only network name
               should be specified (not the subnetwork_name) and the IP
               address is created from the IPCidrRange of the subnetwork
               that exists in that zone for that network.
            -  If the network that the instance is being created in is a
               custom Subnet Mode Network, then the subnetwork_name must
               be specified and the IP address is created from the
               IPCidrRange of the subnetwork.

            If specified, the subnetwork must exist in the same region
            as the App Engine flexible environment application.
        session_affinity (bool):
            Enable session affinity.
            Only applicable in the App Engine flexible
            environment.
    """

    forwarded_ports = proto.RepeatedField(proto.STRING, number=1,)
    instance_tag = proto.Field(proto.STRING, number=2,)
    name = proto.Field(proto.STRING, number=3,)
    subnetwork_name = proto.Field(proto.STRING, number=4,)
    session_affinity = proto.Field(proto.BOOL, number=5,)


class Volume(proto.Message):
    r"""Volumes mounted within the app container.
    Only applicable in the App Engine flexible environment.

    Attributes:
        name (str):
            Unique name for the volume.
        volume_type (str):
            Underlying volume type, e.g. 'tmpfs'.
        size_gb (float):
            Volume size in gigabytes.
    """

    name = proto.Field(proto.STRING, number=1,)
    volume_type = proto.Field(proto.STRING, number=2,)
    size_gb = proto.Field(proto.DOUBLE, number=3,)


class Resources(proto.Message):
    r"""Machine resources for a version.
    Attributes:
        cpu (float):
            Number of CPU cores needed.
        disk_gb (float):
            Disk size (GB) needed.
        memory_gb (float):
            Memory (GB) needed.
        volumes (Sequence[google.cloud.appengine_admin_v1.types.Volume]):
            User specified volumes.
        kms_key_reference (str):
            The name of the encryption key that is stored
            in Google Cloud KMS. Only should be used by
            Cloud Composer to encrypt the vm disk
    """

    cpu = proto.Field(proto.DOUBLE, number=1,)
    disk_gb = proto.Field(proto.DOUBLE, number=2,)
    memory_gb = proto.Field(proto.DOUBLE, number=3,)
    volumes = proto.RepeatedField(proto.MESSAGE, number=4, message="Volume",)
    kms_key_reference = proto.Field(proto.STRING, number=5,)


class VpcAccessConnector(proto.Message):
    r"""VPC access connector specification.
    Attributes:
        name (str):
            Full Serverless VPC Access Connector name
            e.g. /projects/my-project/locations/us-
            central1/connectors/c1.
    """

    name = proto.Field(proto.STRING, number=1,)


class Entrypoint(proto.Message):
    r"""The entrypoint for the application.
    Attributes:
        shell (str):
            The format should be a shell command that can be fed to
            ``bash -c``.
    """

    shell = proto.Field(proto.STRING, number=1, oneof="command",)


__all__ = tuple(sorted(__protobuf__.manifest))
