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
from google.type import datetime_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.oracledatabase.v1",
    manifest={
        "CloudVmCluster",
        "CloudVmClusterProperties",
        "DataCollectionOptions",
    },
)


class CloudVmCluster(proto.Message):
    r"""Details of the Cloud VM Cluster resource.
    https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/CloudVmCluster/

    Attributes:
        name (str):
            Identifier. The name of the VM Cluster resource with the
            format:
            projects/{project}/locations/{region}/cloudVmClusters/{cloud_vm_cluster}
        exadata_infrastructure (str):
            Required. The name of the Exadata Infrastructure resource on
            which VM cluster resource is created, in the following
            format:
            projects/{project}/locations/{region}/cloudExadataInfrastuctures/{cloud_extradata_infrastructure}
        display_name (str):
            Optional. User friendly name for this
            resource.
        gcp_oracle_zone (str):
            Output only. Google Cloud Platform location
            where Oracle Exadata is hosted. It is same as
            Google Cloud Platform Oracle zone of Exadata
            infrastructure.
        properties (google.cloud.oracledatabase_v1.types.CloudVmClusterProperties):
            Optional. Various properties of the VM
            Cluster.
        labels (MutableMapping[str, str]):
            Optional. Labels or tags associated with the
            VM Cluster.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The date and time that the VM
            cluster was created.
        cidr (str):
            Required. Network settings. CIDR to use for
            cluster IP allocation.
        backup_subnet_cidr (str):
            Required. CIDR range of the backup subnet.
        network (str):
            Required. The name of the VPC network.
            Format:
            projects/{project}/global/networks/{network}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    exadata_infrastructure: str = proto.Field(
        proto.STRING,
        number=2,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    gcp_oracle_zone: str = proto.Field(
        proto.STRING,
        number=12,
    )
    properties: "CloudVmClusterProperties" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="CloudVmClusterProperties",
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    cidr: str = proto.Field(
        proto.STRING,
        number=9,
    )
    backup_subnet_cidr: str = proto.Field(
        proto.STRING,
        number=10,
    )
    network: str = proto.Field(
        proto.STRING,
        number=11,
    )


class CloudVmClusterProperties(proto.Message):
    r"""Various properties and settings associated with Exadata VM
    cluster.

    Attributes:
        ocid (str):
            Output only. Oracle Cloud Infrastructure ID
            of VM Cluster.
        license_type (google.cloud.oracledatabase_v1.types.CloudVmClusterProperties.LicenseType):
            Required. License type of VM Cluster.
        gi_version (str):
            Optional. Grid Infrastructure Version.
        time_zone (google.type.datetime_pb2.TimeZone):
            Optional. Time zone of VM Cluster to set.
            Defaults to UTC if not specified.
        ssh_public_keys (MutableSequence[str]):
            Optional. SSH public keys to be stored with
            cluster.
        node_count (int):
            Optional. Number of database servers.
        shape (str):
            Output only. Shape of VM Cluster.
        ocpu_count (float):
            Optional. OCPU count per VM. Minimum is 0.1.
        memory_size_gb (int):
            Optional. Memory allocated in GBs.
        db_node_storage_size_gb (int):
            Optional. Local storage per VM.
        storage_size_gb (int):
            Output only. The storage allocation for the
            disk group, in gigabytes (GB).
        data_storage_size_tb (float):
            Optional. The data disk group size to be
            allocated in TBs.
        disk_redundancy (google.cloud.oracledatabase_v1.types.CloudVmClusterProperties.DiskRedundancy):
            Optional. The type of redundancy.
        sparse_diskgroup_enabled (bool):
            Optional. Use exadata sparse snapshots.
        local_backup_enabled (bool):
            Optional. Use local backup.
        hostname_prefix (str):
            Optional. Prefix for VM cluster host names.
        diagnostics_data_collection_options (google.cloud.oracledatabase_v1.types.DataCollectionOptions):
            Optional. Data collection options for
            diagnostics.
        state (google.cloud.oracledatabase_v1.types.CloudVmClusterProperties.State):
            Output only. State of the cluster.
        scan_listener_port_tcp (int):
            Output only. SCAN listener port - TCP
        scan_listener_port_tcp_ssl (int):
            Output only. SCAN listener port - TLS
        domain (str):
            Output only. Parent DNS domain where SCAN DNS
            and hosts names are qualified. ex:
            ocispdelegated.ocisp10jvnet.oraclevcn.com
        scan_dns (str):
            Output only. SCAN DNS name.
            ex:
            sp2-yi0xq-scan.ocispdelegated.ocisp10jvnet.oraclevcn.com
        hostname (str):
            Output only. host name without domain. format:
            "<hostname_prefix>-" with some suffix. ex: sp2-yi0xq where
            "sp2" is the hostname_prefix.
        cpu_core_count (int):
            Required. Number of enabled CPU cores.
        system_version (str):
            Output only. Operating system version of the
            image.
        scan_ip_ids (MutableSequence[str]):
            Output only. OCIDs of scan IPs.
        scan_dns_record_id (str):
            Output only. OCID of scan DNS record.
        oci_url (str):
            Output only. Deep link to the OCI console to
            view this resource.
        db_server_ocids (MutableSequence[str]):
            Optional. OCID of database servers.
        compartment_id (str):
            Output only. Compartment ID of cluster.
        dns_listener_ip (str):
            Output only. DNS listener IP.
        cluster_name (str):
            Optional. OCI Cluster name.
    """

    class LicenseType(proto.Enum):
        r"""Different licenses supported.

        Values:
            LICENSE_TYPE_UNSPECIFIED (0):
                Unspecified
            LICENSE_INCLUDED (1):
                License included part of offer
            BRING_YOUR_OWN_LICENSE (2):
                Bring your own license
        """
        LICENSE_TYPE_UNSPECIFIED = 0
        LICENSE_INCLUDED = 1
        BRING_YOUR_OWN_LICENSE = 2

    class DiskRedundancy(proto.Enum):
        r"""Types of disk redundancy provided by Oracle.

        Values:
            DISK_REDUNDANCY_UNSPECIFIED (0):
                Unspecified.
            HIGH (1):
                High -  3 way mirror.
            NORMAL (2):
                Normal - 2 way mirror.
        """
        DISK_REDUNDANCY_UNSPECIFIED = 0
        HIGH = 1
        NORMAL = 2

    class State(proto.Enum):
        r"""The various lifecycle states of the VM cluster.

        Values:
            STATE_UNSPECIFIED (0):
                Default unspecified value.
            PROVISIONING (1):
                Indicates that the resource is in
                provisioning state.
            AVAILABLE (2):
                Indicates that the resource is in available
                state.
            UPDATING (3):
                Indicates that the resource is in updating
                state.
            TERMINATING (4):
                Indicates that the resource is in terminating
                state.
            TERMINATED (5):
                Indicates that the resource is in terminated
                state.
            FAILED (6):
                Indicates that the resource is in failed
                state.
            MAINTENANCE_IN_PROGRESS (7):
                Indicates that the resource is in maintenance
                in progress state.
        """
        STATE_UNSPECIFIED = 0
        PROVISIONING = 1
        AVAILABLE = 2
        UPDATING = 3
        TERMINATING = 4
        TERMINATED = 5
        FAILED = 6
        MAINTENANCE_IN_PROGRESS = 7

    ocid: str = proto.Field(
        proto.STRING,
        number=1,
    )
    license_type: LicenseType = proto.Field(
        proto.ENUM,
        number=2,
        enum=LicenseType,
    )
    gi_version: str = proto.Field(
        proto.STRING,
        number=3,
    )
    time_zone: datetime_pb2.TimeZone = proto.Field(
        proto.MESSAGE,
        number=4,
        message=datetime_pb2.TimeZone,
    )
    ssh_public_keys: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    node_count: int = proto.Field(
        proto.INT32,
        number=6,
    )
    shape: str = proto.Field(
        proto.STRING,
        number=7,
    )
    ocpu_count: float = proto.Field(
        proto.FLOAT,
        number=8,
    )
    memory_size_gb: int = proto.Field(
        proto.INT32,
        number=9,
    )
    db_node_storage_size_gb: int = proto.Field(
        proto.INT32,
        number=10,
    )
    storage_size_gb: int = proto.Field(
        proto.INT32,
        number=11,
    )
    data_storage_size_tb: float = proto.Field(
        proto.DOUBLE,
        number=12,
    )
    disk_redundancy: DiskRedundancy = proto.Field(
        proto.ENUM,
        number=13,
        enum=DiskRedundancy,
    )
    sparse_diskgroup_enabled: bool = proto.Field(
        proto.BOOL,
        number=14,
    )
    local_backup_enabled: bool = proto.Field(
        proto.BOOL,
        number=15,
    )
    hostname_prefix: str = proto.Field(
        proto.STRING,
        number=16,
    )
    diagnostics_data_collection_options: "DataCollectionOptions" = proto.Field(
        proto.MESSAGE,
        number=19,
        message="DataCollectionOptions",
    )
    state: State = proto.Field(
        proto.ENUM,
        number=20,
        enum=State,
    )
    scan_listener_port_tcp: int = proto.Field(
        proto.INT32,
        number=21,
    )
    scan_listener_port_tcp_ssl: int = proto.Field(
        proto.INT32,
        number=22,
    )
    domain: str = proto.Field(
        proto.STRING,
        number=23,
    )
    scan_dns: str = proto.Field(
        proto.STRING,
        number=24,
    )
    hostname: str = proto.Field(
        proto.STRING,
        number=25,
    )
    cpu_core_count: int = proto.Field(
        proto.INT32,
        number=26,
    )
    system_version: str = proto.Field(
        proto.STRING,
        number=27,
    )
    scan_ip_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=28,
    )
    scan_dns_record_id: str = proto.Field(
        proto.STRING,
        number=29,
    )
    oci_url: str = proto.Field(
        proto.STRING,
        number=30,
    )
    db_server_ocids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=31,
    )
    compartment_id: str = proto.Field(
        proto.STRING,
        number=32,
    )
    dns_listener_ip: str = proto.Field(
        proto.STRING,
        number=35,
    )
    cluster_name: str = proto.Field(
        proto.STRING,
        number=36,
    )


class DataCollectionOptions(proto.Message):
    r"""Data collection options for diagnostics.

    Attributes:
        diagnostics_events_enabled (bool):
            Optional. Indicates whether diagnostic
            collection is enabled for the VM cluster
        health_monitoring_enabled (bool):
            Optional. Indicates whether health monitoring
            is enabled for the VM cluster
        incident_logs_enabled (bool):
            Optional. Indicates whether incident logs and
            trace collection are enabled for the VM cluster
    """

    diagnostics_events_enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    health_monitoring_enabled: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    incident_logs_enabled: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
