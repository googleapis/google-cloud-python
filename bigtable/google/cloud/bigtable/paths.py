# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utilities for constructing paths used in the Bigtable API"""

from google.api_core import path_template


def project_path(project):
    """Return a fully-qualified project string."""
    return path_template.expand(
        'projects/{project}',
        project=project,
    )


def location_path(project, location):
    """Return a fully-qualified location string."""
    return path_template.expand(
        'projects/{project}/locations/{location}',
        project=project,
        location=location,
    )


def instance_path(project, instance):
    """Return a fully-qualified instance string."""
    return path_template.expand(
        'projects/{project}/instances/{instance}',
        project=project,
        instance=instance,
    )


def app_profile_path(project, instance, app_profile):
    """Return a fully-qualified app_profile string."""
    return path_template.expand(
        'projects/{project}/instances/{instance}/appProfiles/{app_profile}',
        project=project,
        instance=instance,
        app_profile=app_profile,
    )


def cluster_path(project, instance, cluster):
    """Return a fully-qualified cluster string."""
    return path_template.expand(
        'projects/{project}/instances/{instance}/clusters/{cluster}',
        project=project,
        instance=instance,
        cluster=cluster,
    )


def snapshot_path(project, instance, cluster, snapshot):
    """Return a fully-qualified snapshot string."""
    return path_template.expand(
        'projects/{project}/instances/{instance}/clusters/{cluster}/'
        'snapshots/{snapshot}',
        project=project,
        instance=instance,
        cluster=cluster,
        snapshot=snapshot,
    )


def table_path(project, instance, table):
    """Return a fully-qualified table string."""
    return path_template.expand(
        'projects/{project}/instances/{instance}/tables/{table}',
        project=project,
        instance=instance,
        table=table,
    )
