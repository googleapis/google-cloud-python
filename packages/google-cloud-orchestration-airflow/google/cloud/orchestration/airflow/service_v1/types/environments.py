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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.orchestration.airflow.service.v1",
    manifest={
        "CreateEnvironmentRequest",
        "GetEnvironmentRequest",
        "ListEnvironmentsRequest",
        "ListEnvironmentsResponse",
        "DeleteEnvironmentRequest",
        "UpdateEnvironmentRequest",
        "EnvironmentConfig",
        "WebServerNetworkAccessControl",
        "DatabaseConfig",
        "WebServerConfig",
        "EncryptionConfig",
        "SoftwareConfig",
        "IPAllocationPolicy",
        "NodeConfig",
        "PrivateClusterConfig",
        "PrivateEnvironmentConfig",
        "Environment",
        "CheckUpgradeResponse",
    },
)


class CreateEnvironmentRequest(proto.Message):
    r"""Create a new environment.

    Attributes:
        parent (str):
            The parent must be of the form
            "projects/{projectId}/locations/{locationId}".
        environment (google.cloud.orchestration.airflow.service_v1.types.Environment):
            The environment to create.
    """

    parent = proto.Field(proto.STRING, number=1,)
    environment = proto.Field(proto.MESSAGE, number=2, message="Environment",)


class GetEnvironmentRequest(proto.Message):
    r"""Get an environment.

    Attributes:
        name (str):
            The resource name of the environment to get,
            in the form:
            "projects/{projectId}/locations/{locationId}/environments/{environmentId}".
    """

    name = proto.Field(proto.STRING, number=1,)


class ListEnvironmentsRequest(proto.Message):
    r"""List environments in a project and location.

    Attributes:
        parent (str):
            List environments in the given project and
            location, in the form:
            "projects/{projectId}/locations/{locationId}".
        page_size (int):
            The maximum number of environments to return.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListEnvironmentsResponse(proto.Message):
    r"""The environments in a project and location.

    Attributes:
        environments (Sequence[google.cloud.orchestration.airflow.service_v1.types.Environment]):
            The list of environments returned by a
            ListEnvironmentsRequest.
        next_page_token (str):
            The page token used to query for the next
            page if one exists.
    """

    @property
    def raw_page(self):
        return self

    environments = proto.RepeatedField(proto.MESSAGE, number=1, message="Environment",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class DeleteEnvironmentRequest(proto.Message):
    r"""Delete an environment.

    Attributes:
        name (str):
            The environment to delete, in the form:
            "projects/{projectId}/locations/{locationId}/environments/{environmentId}".
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateEnvironmentRequest(proto.Message):
    r"""Update an environment.

    Attributes:
        name (str):
            The relative resource name of the environment
            to update, in the form:
            "projects/{projectId}/locations/{locationId}/environments/{environmentId}".
        environment (google.cloud.orchestration.airflow.service_v1.types.Environment):
            A patch environment. Fields specified by the ``updateMask``
            will be copied from the patch environment into the
            environment under update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. A comma-separated list of paths, relative to
            ``Environment``, of fields to update. For example, to set
            the version of scikit-learn to install in the environment to
            0.19.0 and to remove an existing installation of numpy, the
            ``updateMask`` parameter would include the following two
            ``paths`` values:
            "config.softwareConfig.pypiPackages.scikit-learn" and
            "config.softwareConfig.pypiPackages.numpy". The included
            patch environment would specify the scikit-learn version as
            follows:

            ::

                {
                  "config":{
                    "softwareConfig":{
                      "pypiPackages":{
                        "scikit-learn":"==0.19.0"
                      }
                    }
                  }
                }

            Note that in the above example, any existing PyPI packages
            other than scikit-learn and numpy will be unaffected.

            Only one update type may be included in a single request's
            ``updateMask``. For example, one cannot update both the PyPI
            packages and labels in the same request. However, it is
            possible to update multiple members of a map field
            simultaneously in the same request. For example, to set the
            labels "label1" and "label2" while clearing "label3"
            (assuming it already exists), one can provide the paths
            "labels.label1", "labels.label2", and "labels.label3" and
            populate the patch environment as follows:

            ::

                {
                  "labels":{
                    "label1":"new-label1-value"
                    "label2":"new-label2-value"
                  }
                }

            Note that in the above example, any existing labels that are
            not included in the ``updateMask`` will be unaffected.

            It is also possible to replace an entire map field by
            providing the map field's path in the ``updateMask``. The
            new value of the field will be that which is provided in the
            patch environment. For example, to delete all pre-existing
            user-specified PyPI packages and install botocore at version
            1.7.14, the ``updateMask`` would contain the path
            "config.softwareConfig.pypiPackages", and the patch
            environment would be the following:

            ::

                {
                  "config":{
                    "softwareConfig":{
                      "pypiPackages":{
                        "botocore":"==1.7.14"
                      }
                    }
                  }
                }

            **Note:** Only the following fields can be updated:

            -  ``config.softwareConfig.pypiPackages``

               -  Replace all custom custom PyPI packages. If a
                  replacement package map is not included in
                  ``environment``, all custom PyPI packages are cleared.
                  It is an error to provide both this mask and a mask
                  specifying an individual package.

            -  ``config.softwareConfig.pypiPackages.``\ packagename

               -  Update the custom PyPI package *packagename*,
                  preserving other packages. To delete the package,
                  include it in ``updateMask``, and omit the mapping for
                  it in
                  ``environment.config.softwareConfig.pypiPackages``. It
                  is an error to provide both a mask of this form and
                  the ``config.softwareConfig.pypiPackages`` mask.

            -  ``labels``

               -  Replace all environment labels. If a replacement
                  labels map is not included in ``environment``, all
                  labels are cleared. It is an error to provide both
                  this mask and a mask specifying one or more individual
                  labels.

            -  ``labels.``\ labelName

               -  Set the label named *labelName*, while preserving
                  other labels. To delete the label, include it in
                  ``updateMask`` and omit its mapping in
                  ``environment.labels``. It is an error to provide both
                  a mask of this form and the ``labels`` mask.

            -  ``config.nodeCount``

               -  Horizontally scale the number of nodes in the
                  environment. An integer greater than or equal to 3
                  must be provided in the ``config.nodeCount`` field.

            -  ``config.webServerNetworkAccessControl``

               -  Replace the environment's current
                  ``WebServerNetworkAccessControl``.

            -  ``config.databaseConfig``

               -  Replace the environment's current ``DatabaseConfig``.

            -  ``config.webServerConfig``

               -  Replace the environment's current ``WebServerConfig``.

            -  ``config.softwareConfig.airflowConfigOverrides``

               -  Replace all Apache Airflow config overrides. If a
                  replacement config overrides map is not included in
                  ``environment``, all config overrides are cleared. It
                  is an error to provide both this mask and a mask
                  specifying one or more individual config overrides.

            -  ``config.softwareConfig.airflowConfigOverrides.``\ section-name

               -  Override the Apache Airflow config property *name* in
                  the section named *section*, preserving other
                  properties. To delete the property override, include
                  it in ``updateMask`` and omit its mapping in
                  ``environment.config.softwareConfig.airflowConfigOverrides``.
                  It is an error to provide both a mask of this form and
                  the ``config.softwareConfig.airflowConfigOverrides``
                  mask.

            -  ``config.softwareConfig.envVariables``

               -  Replace all environment variables. If a replacement
                  environment variable map is not included in
                  ``environment``, all custom environment variables are
                  cleared. It is an error to provide both this mask and
                  a mask specifying one or more individual environment
                  variables.
    """

    name = proto.Field(proto.STRING, number=2,)
    environment = proto.Field(proto.MESSAGE, number=1, message="Environment",)
    update_mask = proto.Field(
        proto.MESSAGE, number=3, message=field_mask_pb2.FieldMask,
    )


class EnvironmentConfig(proto.Message):
    r"""Configuration information for an environment.

    Attributes:
        gke_cluster (str):
            Output only. The Kubernetes Engine cluster
            used to run this environment.
        dag_gcs_prefix (str):
            Output only. The Cloud Storage prefix of the
            DAGs for this environment. Although Cloud
            Storage objects reside in a flat namespace, a
            hierarchical file tree can be simulated using
            "/"-delimited object name prefixes. DAG objects
            for this environment reside in a simulated
            directory with the given prefix.
        node_count (int):
            The number of nodes in the Kubernetes Engine
            cluster that will be used to run this
            environment.
        software_config (google.cloud.orchestration.airflow.service_v1.types.SoftwareConfig):
            The configuration settings for software
            inside the environment.
        node_config (google.cloud.orchestration.airflow.service_v1.types.NodeConfig):
            The configuration used for the Kubernetes
            Engine cluster.
        private_environment_config (google.cloud.orchestration.airflow.service_v1.types.PrivateEnvironmentConfig):
            The configuration used for the Private IP
            Cloud Composer environment.
        web_server_network_access_control (google.cloud.orchestration.airflow.service_v1.types.WebServerNetworkAccessControl):
            Optional. The network-level access control
            policy for the Airflow web server. If
            unspecified, no network-level access
            restrictions will be applied.
        database_config (google.cloud.orchestration.airflow.service_v1.types.DatabaseConfig):
            Optional. The configuration settings for
            Cloud SQL instance used internally by Apache
            Airflow software.
        web_server_config (google.cloud.orchestration.airflow.service_v1.types.WebServerConfig):
            Optional. The configuration settings for the
            Airflow web server App Engine instance.
        encryption_config (google.cloud.orchestration.airflow.service_v1.types.EncryptionConfig):
            Optional. The encryption options for the
            Cloud Composer environment and its dependencies.
            Cannot be updated.
        airflow_uri (str):
            Output only. The URI of the Apache Airflow Web UI hosted
            within this environment (see `Airflow web
            interface </composer/docs/how-to/accessing/airflow-web-interface>`__).
    """

    gke_cluster = proto.Field(proto.STRING, number=1,)
    dag_gcs_prefix = proto.Field(proto.STRING, number=2,)
    node_count = proto.Field(proto.INT32, number=3,)
    software_config = proto.Field(proto.MESSAGE, number=4, message="SoftwareConfig",)
    node_config = proto.Field(proto.MESSAGE, number=5, message="NodeConfig",)
    private_environment_config = proto.Field(
        proto.MESSAGE, number=7, message="PrivateEnvironmentConfig",
    )
    web_server_network_access_control = proto.Field(
        proto.MESSAGE, number=8, message="WebServerNetworkAccessControl",
    )
    database_config = proto.Field(proto.MESSAGE, number=9, message="DatabaseConfig",)
    web_server_config = proto.Field(
        proto.MESSAGE, number=10, message="WebServerConfig",
    )
    encryption_config = proto.Field(
        proto.MESSAGE, number=11, message="EncryptionConfig",
    )
    airflow_uri = proto.Field(proto.STRING, number=6,)


class WebServerNetworkAccessControl(proto.Message):
    r"""Network-level access control policy for the Airflow web
    server.

    Attributes:
        allowed_ip_ranges (Sequence[google.cloud.orchestration.airflow.service_v1.types.WebServerNetworkAccessControl.AllowedIpRange]):
            A collection of allowed IP ranges with
            descriptions.
    """

    class AllowedIpRange(proto.Message):
        r"""Allowed IP range with user-provided description.

        Attributes:
            value (str):
                IP address or range, defined using CIDR notation, of
                requests that this rule applies to. Examples:
                ``192.168.1.1`` or ``192.168.0.0/16`` or ``2001:db8::/32``
                or ``2001:0db8:0000:0042:0000:8a2e:0370:7334``.

                IP range prefixes should be properly truncated. For example,
                ``1.2.3.4/24`` should be truncated to ``1.2.3.0/24``.
                Similarly, for IPv6, ``2001:db8::1/32`` should be truncated
                to ``2001:db8::/32``.
            description (str):
                Optional. User-provided description. It must
                contain at most 300 characters.
        """

        value = proto.Field(proto.STRING, number=1,)
        description = proto.Field(proto.STRING, number=2,)

    allowed_ip_ranges = proto.RepeatedField(
        proto.MESSAGE, number=1, message=AllowedIpRange,
    )


class DatabaseConfig(proto.Message):
    r"""The configuration of Cloud SQL instance that is used by the
    Apache Airflow software.

    Attributes:
        machine_type (str):
            Optional. Cloud SQL machine type used by
            Airflow database. It has to be one of:
            db-n1-standard-2, db-n1-standard-4,
            db-n1-standard-8 or db-n1-standard-16. If not
            specified, db-n1-standard-2 will be used.
    """

    machine_type = proto.Field(proto.STRING, number=1,)


class WebServerConfig(proto.Message):
    r"""The configuration settings for the Airflow web server App
    Engine instance.

    Attributes:
        machine_type (str):
            Optional. Machine type on which Airflow web
            server is running. It has to be one of:
            composer-n1-webserver-2, composer-n1-webserver-4
            or composer-n1-webserver-8.
            If not specified, composer-n1-webserver-2 will
            be used. Value custom is returned only in
            response, if Airflow web server parameters were
            manually changed to a non-standard values.
    """

    machine_type = proto.Field(proto.STRING, number=1,)


class EncryptionConfig(proto.Message):
    r"""The encryption options for the Cloud Composer environment
    and its dependencies.

    Attributes:
        kms_key_name (str):
            Optional. Customer-managed Encryption Key
            available through Google's Key Management
            Service. Cannot be updated. If not specified,
            Google-managed key will be used.
    """

    kms_key_name = proto.Field(proto.STRING, number=1,)


class SoftwareConfig(proto.Message):
    r"""Specifies the selection and configuration of software inside
    the environment.

    Attributes:
        image_version (str):
            The version of the software running in the environment. This
            encapsulates both the version of Cloud Composer
            functionality and the version of Apache Airflow. It must
            match the regular expression
            ``composer-([0-9]+\.[0-9]+\.[0-9]+|latest)-airflow-[0-9]+\.[0-9]+(\.[0-9]+.*)?``.
            When used as input, the server also checks if the provided
            version is supported and denies the request for an
            unsupported version.

            The Cloud Composer portion of the version is a `semantic
            version <https://semver.org>`__ or ``latest``. When the
            patch version is omitted, the current Cloud Composer patch
            version is selected. When ``latest`` is provided instead of
            an explicit version number, the server replaces ``latest``
            with the current Cloud Composer version and stores that
            version number in the same field.

            The portion of the image version that follows *airflow-* is
            an official Apache Airflow repository `release
            name <https://github.com/apache/incubator-airflow/releases>`__.

            See also `Version
            List </composer/docs/concepts/versioning/composer-versions>`__.
        airflow_config_overrides (Sequence[google.cloud.orchestration.airflow.service_v1.types.SoftwareConfig.AirflowConfigOverridesEntry]):
            Optional. Apache Airflow configuration properties to
            override.

            Property keys contain the section and property names,
            separated by a hyphen, for example
            "core-dags_are_paused_at_creation". Section names must not
            contain hyphens ("-"), opening square brackets ("["), or
            closing square brackets ("]"). The property name must not be
            empty and must not contain an equals sign ("=") or semicolon
            (";"). Section and property names must not contain a period
            ("."). Apache Airflow configuration property names must be
            written in
            `snake_case <https://en.wikipedia.org/wiki/Snake_case>`__.
            Property values can contain any character, and can be
            written in any lower/upper case format.

            Certain Apache Airflow configuration property values are
            `blocked </composer/docs/concepts/airflow-configurations>`__,
            and cannot be overridden.
        pypi_packages (Sequence[google.cloud.orchestration.airflow.service_v1.types.SoftwareConfig.PypiPackagesEntry]):
            Optional. Custom Python Package Index (PyPI) packages to be
            installed in the environment.

            Keys refer to the lowercase package name such as "numpy" and
            values are the lowercase extras and version specifier such
            as "==1.12.0", "[devel,gcp_api]", or "[devel]>=1.8.2,
            <1.9.2". To specify a package without pinning it to a
            version specifier, use the empty string as the value.
        env_variables (Sequence[google.cloud.orchestration.airflow.service_v1.types.SoftwareConfig.EnvVariablesEntry]):
            Optional. Additional environment variables to provide to the
            Apache Airflow scheduler, worker, and webserver processes.

            Environment variable names must match the regular expression
            ``[a-zA-Z_][a-zA-Z0-9_]*``. They cannot specify Apache
            Airflow software configuration overrides (they cannot match
            the regular expression ``AIRFLOW__[A-Z0-9_]+__[A-Z0-9_]+``),
            and they cannot match any of the following reserved names:

            -  ``AIRFLOW_HOME``
            -  ``C_FORCE_ROOT``
            -  ``CONTAINER_NAME``
            -  ``DAGS_FOLDER``
            -  ``GCP_PROJECT``
            -  ``GCS_BUCKET``
            -  ``GKE_CLUSTER_NAME``
            -  ``SQL_DATABASE``
            -  ``SQL_INSTANCE``
            -  ``SQL_PASSWORD``
            -  ``SQL_PROJECT``
            -  ``SQL_REGION``
            -  ``SQL_USER``
        python_version (str):
            Optional. The major version of Python used to
            run the Apache Airflow scheduler, worker, and
            webserver processes.
            Can be set to '2' or '3'. If not specified, the
            default is '3'. Cannot be updated.
    """

    image_version = proto.Field(proto.STRING, number=1,)
    airflow_config_overrides = proto.MapField(proto.STRING, proto.STRING, number=2,)
    pypi_packages = proto.MapField(proto.STRING, proto.STRING, number=3,)
    env_variables = proto.MapField(proto.STRING, proto.STRING, number=4,)
    python_version = proto.Field(proto.STRING, number=6,)


class IPAllocationPolicy(proto.Message):
    r"""Configuration for controlling how IPs are allocated in the
    GKE cluster running the Apache Airflow software.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        use_ip_aliases (bool):
            Optional. Whether or not to enable Alias IPs in the GKE
            cluster. If ``true``, a VPC-native cluster is created.
        cluster_secondary_range_name (str):
            Optional. The name of the GKE cluster's secondary range used
            to allocate IP addresses to pods.

            This field is applicable only when ``use_ip_aliases`` is
            true.

            This field is a member of `oneof`_ ``cluster_ip_allocation``.
        cluster_ipv4_cidr_block (str):
            Optional. The IP address range used to allocate IP addresses
            to pods in the GKE cluster.

            This field is applicable only when ``use_ip_aliases`` is
            true.

            Set to blank to have GKE choose a range with the default
            size.

            Set to /netmask (e.g. ``/14``) to have GKE choose a range
            with a specific netmask.

            Set to a
            `CIDR <http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`__
            notation (e.g. ``10.96.0.0/14``) from the RFC-1918 private
            networks (e.g. ``10.0.0.0/8``, ``172.16.0.0/12``,
            ``192.168.0.0/16``) to pick a specific range to use.

            This field is a member of `oneof`_ ``cluster_ip_allocation``.
        services_secondary_range_name (str):
            Optional. The name of the services' secondary range used to
            allocate IP addresses to the GKE cluster.

            This field is applicable only when ``use_ip_aliases`` is
            true.

            This field is a member of `oneof`_ ``services_ip_allocation``.
        services_ipv4_cidr_block (str):
            Optional. The IP address range of the services IP addresses
            in this GKE cluster.

            This field is applicable only when ``use_ip_aliases`` is
            true.

            Set to blank to have GKE choose a range with the default
            size.

            Set to /netmask (e.g. ``/14``) to have GKE choose a range
            with a specific netmask.

            Set to a
            `CIDR <http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`__
            notation (e.g. ``10.96.0.0/14``) from the RFC-1918 private
            networks (e.g. ``10.0.0.0/8``, ``172.16.0.0/12``,
            ``192.168.0.0/16``) to pick a specific range to use.

            This field is a member of `oneof`_ ``services_ip_allocation``.
    """

    use_ip_aliases = proto.Field(proto.BOOL, number=1,)
    cluster_secondary_range_name = proto.Field(
        proto.STRING, number=2, oneof="cluster_ip_allocation",
    )
    cluster_ipv4_cidr_block = proto.Field(
        proto.STRING, number=4, oneof="cluster_ip_allocation",
    )
    services_secondary_range_name = proto.Field(
        proto.STRING, number=3, oneof="services_ip_allocation",
    )
    services_ipv4_cidr_block = proto.Field(
        proto.STRING, number=5, oneof="services_ip_allocation",
    )


class NodeConfig(proto.Message):
    r"""The configuration information for the Kubernetes Engine nodes
    running the Apache Airflow software.

    Attributes:
        location (str):
            Optional. The Compute Engine
            `zone </compute/docs/regions-zones>`__ in which to deploy
            the VMs used to run the Apache Airflow software, specified
            as a `relative resource
            name </apis/design/resource_names#relative_resource_name>`__.
            For example: "projects/{projectId}/zones/{zoneId}".

            This ``location`` must belong to the enclosing environment's
            project and location. If both this field and
            ``nodeConfig.machineType`` are specified,
            ``nodeConfig.machineType`` must belong to this ``location``;
            if both are unspecified, the service will pick a zone in the
            Compute Engine region corresponding to the Cloud Composer
            location, and propagate that choice to both fields. If only
            one field (``location`` or ``nodeConfig.machineType``) is
            specified, the location information from the specified field
            will be propagated to the unspecified field.
        machine_type (str):
            Optional. The Compute Engine `machine
            type </compute/docs/machine-types>`__ used for cluster
            instances, specified as a `relative resource
            name </apis/design/resource_names#relative_resource_name>`__.
            For example:
            "projects/{projectId}/zones/{zoneId}/machineTypes/{machineTypeId}".

            The ``machineType`` must belong to the enclosing
            environment's project and location. If both this field and
            ``nodeConfig.location`` are specified, this ``machineType``
            must belong to the ``nodeConfig.location``; if both are
            unspecified, the service will pick a zone in the Compute
            Engine region corresponding to the Cloud Composer location,
            and propagate that choice to both fields. If exactly one of
            this field and ``nodeConfig.location`` is specified, the
            location information from the specified field will be
            propagated to the unspecified field.

            The ``machineTypeId`` must not be a `shared-core machine
            type </compute/docs/machine-types#sharedcore>`__.

            If this field is unspecified, the ``machineTypeId`` defaults
            to "n1-standard-1".
        network (str):
            Optional. The Compute Engine network to be used for machine
            communications, specified as a `relative resource
            name </apis/design/resource_names#relative_resource_name>`__.
            For example:
            "projects/{projectId}/global/networks/{networkId}".

            If unspecified, the "default" network ID in the
            environment's project is used. If a `Custom Subnet
            Network </vpc/docs/vpc#vpc_networks_and_subnets>`__ is
            provided, ``nodeConfig.subnetwork`` must also be provided.
            For `Shared VPC </vpc/docs/shared-vpc>`__ subnetwork
            requirements, see ``nodeConfig.subnetwork``.
        subnetwork (str):
            Optional. The Compute Engine subnetwork to be used for
            machine communications, specified as a `relative resource
            name </apis/design/resource_names#relative_resource_name>`__.
            For example:
            "projects/{projectId}/regions/{regionId}/subnetworks/{subnetworkId}"

            If a subnetwork is provided, ``nodeConfig.network`` must
            also be provided, and the subnetwork must belong to the
            enclosing environment's project and location.
        disk_size_gb (int):
            Optional. The disk size in GB used for node
            VMs. Minimum size is 20GB. If unspecified,
            defaults to 100GB. Cannot be updated.
        oauth_scopes (Sequence[str]):
            Optional. The set of Google API scopes to be made available
            on all node VMs. If ``oauth_scopes`` is empty, defaults to
            ["https://www.googleapis.com/auth/cloud-platform"]. Cannot
            be updated.
        service_account (str):
            Optional. The Google Cloud Platform Service
            Account to be used by the node VMs. If a service
            account is not specified, the "default" Compute
            Engine service account is used. Cannot be
            updated.
        tags (Sequence[str]):
            Optional. The list of instance tags applied to all node VMs.
            Tags are used to identify valid sources or targets for
            network firewalls. Each tag within the list must comply with
            `RFC1035 <https://www.ietf.org/rfc/rfc1035.txt>`__. Cannot
            be updated.
        ip_allocation_policy (google.cloud.orchestration.airflow.service_v1.types.IPAllocationPolicy):
            Optional. The configuration for controlling
            how IPs are allocated in the GKE cluster.
    """

    location = proto.Field(proto.STRING, number=1,)
    machine_type = proto.Field(proto.STRING, number=2,)
    network = proto.Field(proto.STRING, number=3,)
    subnetwork = proto.Field(proto.STRING, number=4,)
    disk_size_gb = proto.Field(proto.INT32, number=5,)
    oauth_scopes = proto.RepeatedField(proto.STRING, number=6,)
    service_account = proto.Field(proto.STRING, number=7,)
    tags = proto.RepeatedField(proto.STRING, number=8,)
    ip_allocation_policy = proto.Field(
        proto.MESSAGE, number=9, message="IPAllocationPolicy",
    )


class PrivateClusterConfig(proto.Message):
    r"""Configuration options for the private GKE cluster in a Cloud
    Composer environment.

    Attributes:
        enable_private_endpoint (bool):
            Optional. If ``true``, access to the public endpoint of the
            GKE cluster is denied.
        master_ipv4_cidr_block (str):
            Optional. The CIDR block from which IPv4
            range for GKE master will be reserved. If left
            blank, the default value of '172.16.0.0/23' is
            used.
        master_ipv4_reserved_range (str):
            Output only. The IP range in CIDR notation to
            use for the hosted master network. This range is
            used for assigning internal IP addresses to the
            GKE cluster master or set of masters and to the
            internal load balancer virtual IP. This range
            must not overlap with any other ranges in use
            within the cluster's network.
    """

    enable_private_endpoint = proto.Field(proto.BOOL, number=1,)
    master_ipv4_cidr_block = proto.Field(proto.STRING, number=2,)
    master_ipv4_reserved_range = proto.Field(proto.STRING, number=3,)


class PrivateEnvironmentConfig(proto.Message):
    r"""The configuration information for configuring a Private IP
    Cloud Composer environment.

    Attributes:
        enable_private_environment (bool):
            Optional. If ``true``, a Private IP Cloud Composer
            environment is created. If this field is set to true,
            ``IPAllocationPolicy.use_ip_aliases`` must be set to true.
        private_cluster_config (google.cloud.orchestration.airflow.service_v1.types.PrivateClusterConfig):
            Optional. Configuration for the private GKE
            cluster for a Private IP Cloud Composer
            environment.
        web_server_ipv4_cidr_block (str):
            Optional. The CIDR block from which IP range for web server
            will be reserved. Needs to be disjoint from
            ``private_cluster_config.master_ipv4_cidr_block`` and
            ``cloud_sql_ipv4_cidr_block``.
        cloud_sql_ipv4_cidr_block (str):
            Optional. The CIDR block from which IP range in tenant
            project will be reserved for Cloud SQL. Needs to be disjoint
            from ``web_server_ipv4_cidr_block``.
        web_server_ipv4_reserved_range (str):
            Output only. The IP range reserved for the
            tenant project's App Engine VMs.
    """

    enable_private_environment = proto.Field(proto.BOOL, number=1,)
    private_cluster_config = proto.Field(
        proto.MESSAGE, number=2, message="PrivateClusterConfig",
    )
    web_server_ipv4_cidr_block = proto.Field(proto.STRING, number=3,)
    cloud_sql_ipv4_cidr_block = proto.Field(proto.STRING, number=4,)
    web_server_ipv4_reserved_range = proto.Field(proto.STRING, number=5,)


class Environment(proto.Message):
    r"""An environment for running orchestration tasks.

    Attributes:
        name (str):
            The resource name of the environment, in the
            form:
            "projects/{projectId}/locations/{locationId}/environments/{environmentId}"
            EnvironmentId must start with a lowercase letter
            followed by up to 63 lowercase letters, numbers,
            or hyphens, and cannot end with a hyphen.
        config (google.cloud.orchestration.airflow.service_v1.types.EnvironmentConfig):
            Configuration parameters for this
            environment.
        uuid (str):
            Output only. The UUID (Universally Unique
            IDentifier) associated with this environment.
            This value is generated when the environment is
            created.
        state (google.cloud.orchestration.airflow.service_v1.types.Environment.State):
            The current state of the environment.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            environment was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            environment was last modified.
        labels (Sequence[google.cloud.orchestration.airflow.service_v1.types.Environment.LabelsEntry]):
            Optional. User-defined labels for this environment. The
            labels map can contain no more than 64 entries. Entries of
            the labels map are UTF8 strings that comply with the
            following restrictions:

            -  Keys must conform to regexp:
               [\p{Ll}\p{Lo}][\p{Ll}\p{Lo}\p{N}_-]{0,62}
            -  Values must conform to regexp:
               [\p{Ll}\p{Lo}\p{N}_-]{0,63}
            -  Both keys and values are additionally constrained to be
               <= 128 bytes in size.
    """

    class State(proto.Enum):
        r"""State of the environment."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        RUNNING = 2
        UPDATING = 3
        DELETING = 4
        ERROR = 5

    name = proto.Field(proto.STRING, number=1,)
    config = proto.Field(proto.MESSAGE, number=2, message="EnvironmentConfig",)
    uuid = proto.Field(proto.STRING, number=3,)
    state = proto.Field(proto.ENUM, number=4, enum=State,)
    create_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=7,)


class CheckUpgradeResponse(proto.Message):
    r"""Message containing information about the result of an upgrade
    check operation.

    Attributes:
        build_log_uri (str):
            Output only. Url for a docker build log of an
            upgraded image.
        contains_pypi_modules_conflict (google.cloud.orchestration.airflow.service_v1.types.CheckUpgradeResponse.ConflictResult):
            Output only. Whether build has succeeded or
            failed on modules conflicts.
        pypi_conflict_build_log_extract (str):
            Output only. Extract from a docker image
            build log containing information about pypi
            modules conflicts.
        image_version (str):
            Composer image for which the build was
            happening.
        pypi_dependencies (Sequence[google.cloud.orchestration.airflow.service_v1.types.CheckUpgradeResponse.PypiDependenciesEntry]):
            Pypi dependencies specified in the
            environment configuration, at the time when the
            build was triggered.
    """

    class ConflictResult(proto.Enum):
        r"""Whether there were python modules conflict during image
        build.
        """
        CONFLICT_RESULT_UNSPECIFIED = 0
        CONFLICT = 1
        NO_CONFLICT = 2

    build_log_uri = proto.Field(proto.STRING, number=1,)
    contains_pypi_modules_conflict = proto.Field(
        proto.ENUM, number=4, enum=ConflictResult,
    )
    pypi_conflict_build_log_extract = proto.Field(proto.STRING, number=3,)
    image_version = proto.Field(proto.STRING, number=5,)
    pypi_dependencies = proto.MapField(proto.STRING, proto.STRING, number=6,)


__all__ = tuple(sorted(__protobuf__.manifest))
