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
from google.cloud.hypercomputecluster_v1beta import gapic_version as package_version

__version__ = package_version.__version__


import google.api_core as api_core

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.hypercomputecluster_v1beta")  # type: ignore
    api_core.check_dependency_versions("google.cloud.hypercomputecluster_v1beta")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.hypercomputecluster_v1beta"
        if sys.version_info < (3, 9):
            warnings.warn(
                "You are using a non-supported Python version "
                + f"({_py_version_str}).  Google will not post any further "
                + f"updates to {_package_label} supporting this Python version. "
                + "Please upgrade to the latest Python version, or at "
                + f"least to Python 3.9, and then update {_package_label}.",
                FutureWarning,
            )
        if sys.version_info[:2] == (3, 9):
            warnings.warn(
                f"You are using a Python version ({_py_version_str}) "
                + f"which Google will stop supporting in {_package_label} in "
                + "January 2026. Please "
                + "upgrade to the latest Python version, or at "
                + "least to Python 3.10, before then, and "
                + f"then update {_package_label}.",
                FutureWarning,
            )

        from packaging.version import parse as parse_version

        if sys.version_info < (3, 8):
            import pkg_resources

            def _get_version(dependency_name):
                try:
                    version_string = pkg_resources.get_distribution(
                        dependency_name
                    ).version
                    return (parse_version(version_string), version_string)
                except pkg_resources.DistributionNotFound:
                    return (None, "--")

        else:
            from importlib import metadata

            def _get_version(dependency_name):
                try:
                    version_string = metadata.version("requests")
                    parsed_version = parse_version(version_string)
                    return (parsed_version.release, version_string)
                except metadata.PackageNotFoundError:
                    return (None, "--")

        _dependency_package = "google.protobuf"
        _next_supported_version = "4.25.8"
        _next_supported_version_tuple = (4, 25, 8)
        _recommendation = " (we recommend 6.x)"
        (_version_used, _version_used_string) = _get_version(_dependency_package)
        if _version_used and _version_used < _next_supported_version_tuple:
            warnings.warn(
                f"Package {_package_label} depends on "
                + f"{_dependency_package}, currently installed at version "
                + f"{_version_used_string}. Future updates to "
                + f"{_package_label} will require {_dependency_package} at "
                + f"version {_next_supported_version} or higher{_recommendation}."
                + " Please ensure "
                + "that either (a) your Python environment doesn't pin the "
                + f"version of {_dependency_package}, so that updates to "
                + f"{_package_label} can require the higher version, or "
                + "(b) you manually update your Python environment to use at "
                + f"least version {_next_supported_version} of "
                + f"{_dependency_package}.",
                FutureWarning,
            )
    except Exception:
        warnings.warn(
            "Could not determine the version of Python "
            + "currently being used. To continue receiving "
            + "updates for {_package_label}, ensure you are "
            + "using a supported version of Python; see "
            + "https://devguide.python.org/versions/"
        )


from .services.hypercompute_cluster import (
    HypercomputeClusterAsyncClient,
    HypercomputeClusterClient,
)
from .types.hypercompute_cluster import (
    BootDisk,
    BucketReference,
    Cluster,
    ComputeInstance,
    ComputeInstanceSlurmNodeSet,
    ComputeResource,
    ComputeResourceConfig,
    CreateClusterRequest,
    DeleteClusterRequest,
    ExistingBucketConfig,
    ExistingFilestoreConfig,
    ExistingLustreConfig,
    ExistingNetworkConfig,
    FileShareConfig,
    FilestoreReference,
    GcsAutoclassConfig,
    GcsHierarchicalNamespaceConfig,
    GetClusterRequest,
    ListClustersRequest,
    ListClustersResponse,
    LustreReference,
    NetworkReference,
    NetworkResource,
    NetworkResourceConfig,
    NewBucketConfig,
    NewFilestoreConfig,
    NewFlexStartInstancesConfig,
    NewLustreConfig,
    NewNetworkConfig,
    NewOnDemandInstancesConfig,
    NewReservedInstancesConfig,
    NewSpotInstancesConfig,
    Orchestrator,
    SlurmLoginNodes,
    SlurmNodeSet,
    SlurmOrchestrator,
    SlurmPartition,
    StorageConfig,
    StorageResource,
    StorageResourceConfig,
    UpdateClusterRequest,
)
from .types.operation_metadata import OperationMetadata

__all__ = (
    "HypercomputeClusterAsyncClient",
    "BootDisk",
    "BucketReference",
    "Cluster",
    "ComputeInstance",
    "ComputeInstanceSlurmNodeSet",
    "ComputeResource",
    "ComputeResourceConfig",
    "CreateClusterRequest",
    "DeleteClusterRequest",
    "ExistingBucketConfig",
    "ExistingFilestoreConfig",
    "ExistingLustreConfig",
    "ExistingNetworkConfig",
    "FileShareConfig",
    "FilestoreReference",
    "GcsAutoclassConfig",
    "GcsHierarchicalNamespaceConfig",
    "GetClusterRequest",
    "HypercomputeClusterClient",
    "ListClustersRequest",
    "ListClustersResponse",
    "LustreReference",
    "NetworkReference",
    "NetworkResource",
    "NetworkResourceConfig",
    "NewBucketConfig",
    "NewFilestoreConfig",
    "NewFlexStartInstancesConfig",
    "NewLustreConfig",
    "NewNetworkConfig",
    "NewOnDemandInstancesConfig",
    "NewReservedInstancesConfig",
    "NewSpotInstancesConfig",
    "OperationMetadata",
    "Orchestrator",
    "SlurmLoginNodes",
    "SlurmNodeSet",
    "SlurmOrchestrator",
    "SlurmPartition",
    "StorageConfig",
    "StorageResource",
    "StorageResourceConfig",
    "UpdateClusterRequest",
)
