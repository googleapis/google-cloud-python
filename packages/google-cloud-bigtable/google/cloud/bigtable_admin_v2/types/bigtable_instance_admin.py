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

from google.cloud.bigtable_admin_v2.types import instance as gba_instance
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.bigtable.admin.v2",
    manifest={
        "CreateInstanceRequest",
        "GetInstanceRequest",
        "ListInstancesRequest",
        "ListInstancesResponse",
        "PartialUpdateInstanceRequest",
        "DeleteInstanceRequest",
        "CreateClusterRequest",
        "GetClusterRequest",
        "ListClustersRequest",
        "ListClustersResponse",
        "DeleteClusterRequest",
        "CreateInstanceMetadata",
        "UpdateInstanceMetadata",
        "CreateClusterMetadata",
        "UpdateClusterMetadata",
        "PartialUpdateClusterMetadata",
        "PartialUpdateClusterRequest",
        "CreateAppProfileRequest",
        "GetAppProfileRequest",
        "ListAppProfilesRequest",
        "ListAppProfilesResponse",
        "UpdateAppProfileRequest",
        "DeleteAppProfileRequest",
        "UpdateAppProfileMetadata",
        "ListHotTabletsRequest",
        "ListHotTabletsResponse",
    },
)


class CreateInstanceRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.CreateInstance.

    Attributes:
        parent (str):
            Required. The unique name of the project in which to create
            the new instance. Values are of the form
            ``projects/{project}``.
        instance_id (str):
            Required. The ID to be used when referring to the new
            instance within its project, e.g., just ``myinstance``
            rather than ``projects/myproject/instances/myinstance``.
        instance (google.cloud.bigtable_admin_v2.types.Instance):
            Required. The instance to create. Fields marked
            ``OutputOnly`` must be left blank.
        clusters (Sequence[google.cloud.bigtable_admin_v2.types.CreateInstanceRequest.ClustersEntry]):
            Required. The clusters to be created within the instance,
            mapped by desired cluster ID, e.g., just ``mycluster``
            rather than
            ``projects/myproject/instances/myinstance/clusters/mycluster``.
            Fields marked ``OutputOnly`` must be left blank. Currently,
            at most four clusters can be specified.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    instance_id = proto.Field(
        proto.STRING,
        number=2,
    )
    instance = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gba_instance.Instance,
    )
    clusters = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=4,
        message=gba_instance.Cluster,
    )


class GetInstanceRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.GetInstance.

    Attributes:
        name (str):
            Required. The unique name of the requested instance. Values
            are of the form ``projects/{project}/instances/{instance}``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListInstancesRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.ListInstances.

    Attributes:
        parent (str):
            Required. The unique name of the project for which a list of
            instances is requested. Values are of the form
            ``projects/{project}``.
        page_token (str):
            DEPRECATED: This field is unused and ignored.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class ListInstancesResponse(proto.Message):
    r"""Response message for BigtableInstanceAdmin.ListInstances.

    Attributes:
        instances (Sequence[google.cloud.bigtable_admin_v2.types.Instance]):
            The list of requested instances.
        failed_locations (Sequence[str]):
            Locations from which Instance information could not be
            retrieved, due to an outage or some other transient
            condition. Instances whose Clusters are all in one of the
            failed locations may be missing from ``instances``, and
            Instances with at least one Cluster in a failed location may
            only have partial information returned. Values are of the
            form ``projects/<project>/locations/<zone_id>``
        next_page_token (str):
            DEPRECATED: This field is unused and ignored.
    """

    @property
    def raw_page(self):
        return self

    instances = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gba_instance.Instance,
    )
    failed_locations = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class PartialUpdateInstanceRequest(proto.Message):
    r"""Request message for
    BigtableInstanceAdmin.PartialUpdateInstance.

    Attributes:
        instance (google.cloud.bigtable_admin_v2.types.Instance):
            Required. The Instance which will (partially)
            replace the current value.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The subset of Instance fields which
            should be replaced. Must be explicitly set.
    """

    instance = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gba_instance.Instance,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteInstanceRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.DeleteInstance.

    Attributes:
        name (str):
            Required. The unique name of the instance to be deleted.
            Values are of the form
            ``projects/{project}/instances/{instance}``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateClusterRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.CreateCluster.

    Attributes:
        parent (str):
            Required. The unique name of the instance in which to create
            the new cluster. Values are of the form
            ``projects/{project}/instances/{instance}``.
        cluster_id (str):
            Required. The ID to be used when referring to the new
            cluster within its instance, e.g., just ``mycluster`` rather
            than
            ``projects/myproject/instances/myinstance/clusters/mycluster``.
        cluster (google.cloud.bigtable_admin_v2.types.Cluster):
            Required. The cluster to be created. Fields marked
            ``OutputOnly`` must be left blank.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    cluster_id = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gba_instance.Cluster,
    )


class GetClusterRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.GetCluster.

    Attributes:
        name (str):
            Required. The unique name of the requested cluster. Values
            are of the form
            ``projects/{project}/instances/{instance}/clusters/{cluster}``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListClustersRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.ListClusters.

    Attributes:
        parent (str):
            Required. The unique name of the instance for which a list
            of clusters is requested. Values are of the form
            ``projects/{project}/instances/{instance}``. Use
            ``{instance} = '-'`` to list Clusters for all Instances in a
            project, e.g., ``projects/myproject/instances/-``.
        page_token (str):
            DEPRECATED: This field is unused and ignored.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class ListClustersResponse(proto.Message):
    r"""Response message for BigtableInstanceAdmin.ListClusters.

    Attributes:
        clusters (Sequence[google.cloud.bigtable_admin_v2.types.Cluster]):
            The list of requested clusters.
        failed_locations (Sequence[str]):
            Locations from which Cluster information could not be
            retrieved, due to an outage or some other transient
            condition. Clusters from these locations may be missing from
            ``clusters``, or may only have partial information returned.
            Values are of the form
            ``projects/<project>/locations/<zone_id>``
        next_page_token (str):
            DEPRECATED: This field is unused and ignored.
    """

    @property
    def raw_page(self):
        return self

    clusters = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gba_instance.Cluster,
    )
    failed_locations = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteClusterRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.DeleteCluster.

    Attributes:
        name (str):
            Required. The unique name of the cluster to be deleted.
            Values are of the form
            ``projects/{project}/instances/{instance}/clusters/{cluster}``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateInstanceMetadata(proto.Message):
    r"""The metadata for the Operation returned by CreateInstance.

    Attributes:
        original_request (google.cloud.bigtable_admin_v2.types.CreateInstanceRequest):
            The request that prompted the initiation of
            this CreateInstance operation.
        request_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the original request was
            received.
        finish_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the operation failed or was
            completed successfully.
    """

    original_request = proto.Field(
        proto.MESSAGE,
        number=1,
        message="CreateInstanceRequest",
    )
    request_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    finish_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )


class UpdateInstanceMetadata(proto.Message):
    r"""The metadata for the Operation returned by UpdateInstance.

    Attributes:
        original_request (google.cloud.bigtable_admin_v2.types.PartialUpdateInstanceRequest):
            The request that prompted the initiation of
            this UpdateInstance operation.
        request_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the original request was
            received.
        finish_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the operation failed or was
            completed successfully.
    """

    original_request = proto.Field(
        proto.MESSAGE,
        number=1,
        message="PartialUpdateInstanceRequest",
    )
    request_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    finish_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )


class CreateClusterMetadata(proto.Message):
    r"""The metadata for the Operation returned by CreateCluster.

    Attributes:
        original_request (google.cloud.bigtable_admin_v2.types.CreateClusterRequest):
            The request that prompted the initiation of
            this CreateCluster operation.
        request_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the original request was
            received.
        finish_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the operation failed or was
            completed successfully.
    """

    original_request = proto.Field(
        proto.MESSAGE,
        number=1,
        message="CreateClusterRequest",
    )
    request_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    finish_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )


class UpdateClusterMetadata(proto.Message):
    r"""The metadata for the Operation returned by UpdateCluster.

    Attributes:
        original_request (google.cloud.bigtable_admin_v2.types.Cluster):
            The request that prompted the initiation of
            this UpdateCluster operation.
        request_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the original request was
            received.
        finish_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the operation failed or was
            completed successfully.
    """

    original_request = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gba_instance.Cluster,
    )
    request_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    finish_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )


class PartialUpdateClusterMetadata(proto.Message):
    r"""The metadata for the Operation returned by
    PartialUpdateCluster.

    Attributes:
        request_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the original request was
            received.
        finish_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the operation failed or was
            completed successfully.
        original_request (google.cloud.bigtable_admin_v2.types.PartialUpdateClusterRequest):
            The original request for
            PartialUpdateCluster.
    """

    request_time = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    finish_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    original_request = proto.Field(
        proto.MESSAGE,
        number=3,
        message="PartialUpdateClusterRequest",
    )


class PartialUpdateClusterRequest(proto.Message):
    r"""Request message for
    BigtableInstanceAdmin.PartialUpdateCluster.

    Attributes:
        cluster (google.cloud.bigtable_admin_v2.types.Cluster):
            Required. The Cluster which contains the partial updates to
            be applied, subject to the update_mask.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The subset of Cluster fields which
            should be replaced.
    """

    cluster = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gba_instance.Cluster,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class CreateAppProfileRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.CreateAppProfile.

    Attributes:
        parent (str):
            Required. The unique name of the instance in which to create
            the new app profile. Values are of the form
            ``projects/{project}/instances/{instance}``.
        app_profile_id (str):
            Required. The ID to be used when referring to the new app
            profile within its instance, e.g., just ``myprofile`` rather
            than
            ``projects/myproject/instances/myinstance/appProfiles/myprofile``.
        app_profile (google.cloud.bigtable_admin_v2.types.AppProfile):
            Required. The app profile to be created. Fields marked
            ``OutputOnly`` will be ignored.
        ignore_warnings (bool):
            If true, ignore safety checks when creating
            the app profile.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    app_profile_id = proto.Field(
        proto.STRING,
        number=2,
    )
    app_profile = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gba_instance.AppProfile,
    )
    ignore_warnings = proto.Field(
        proto.BOOL,
        number=4,
    )


class GetAppProfileRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.GetAppProfile.

    Attributes:
        name (str):
            Required. The unique name of the requested app profile.
            Values are of the form
            ``projects/{project}/instances/{instance}/appProfiles/{app_profile}``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListAppProfilesRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.ListAppProfiles.

    Attributes:
        parent (str):
            Required. The unique name of the instance for which a list
            of app profiles is requested. Values are of the form
            ``projects/{project}/instances/{instance}``. Use
            ``{instance} = '-'`` to list AppProfiles for all Instances
            in a project, e.g., ``projects/myproject/instances/-``.
        page_size (int):
            Maximum number of results per page.

            A page_size of zero lets the server choose the number of
            items to return. A page_size which is strictly positive will
            return at most that many items. A negative page_size will
            cause an error.

            Following the first request, subsequent paginated calls are
            not required to pass a page_size. If a page_size is set in
            subsequent calls, it must match the page_size given in the
            first request.
        page_token (str):
            The value of ``next_page_token`` returned by a previous
            call.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=3,
    )
    page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class ListAppProfilesResponse(proto.Message):
    r"""Response message for BigtableInstanceAdmin.ListAppProfiles.

    Attributes:
        app_profiles (Sequence[google.cloud.bigtable_admin_v2.types.AppProfile]):
            The list of requested app profiles.
        next_page_token (str):
            Set if not all app profiles could be returned in a single
            response. Pass this value to ``page_token`` in another
            request to get the next page of results.
        failed_locations (Sequence[str]):
            Locations from which AppProfile information could not be
            retrieved, due to an outage or some other transient
            condition. AppProfiles from these locations may be missing
            from ``app_profiles``. Values are of the form
            ``projects/<project>/locations/<zone_id>``
    """

    @property
    def raw_page(self):
        return self

    app_profiles = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gba_instance.AppProfile,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    failed_locations = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class UpdateAppProfileRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.UpdateAppProfile.

    Attributes:
        app_profile (google.cloud.bigtable_admin_v2.types.AppProfile):
            Required. The app profile which will
            (partially) replace the current value.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The subset of app profile fields
            which should be replaced. If unset, all fields
            will be replaced.
        ignore_warnings (bool):
            If true, ignore safety checks when updating
            the app profile.
    """

    app_profile = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gba_instance.AppProfile,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    ignore_warnings = proto.Field(
        proto.BOOL,
        number=3,
    )


class DeleteAppProfileRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.DeleteAppProfile.

    Attributes:
        name (str):
            Required. The unique name of the app profile to be deleted.
            Values are of the form
            ``projects/{project}/instances/{instance}/appProfiles/{app_profile}``.
        ignore_warnings (bool):
            Required. If true, ignore safety checks when
            deleting the app profile.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    ignore_warnings = proto.Field(
        proto.BOOL,
        number=2,
    )


class UpdateAppProfileMetadata(proto.Message):
    r"""The metadata for the Operation returned by UpdateAppProfile."""


class ListHotTabletsRequest(proto.Message):
    r"""Request message for BigtableInstanceAdmin.ListHotTablets.

    Attributes:
        parent (str):
            Required. The cluster name to list hot tablets. Value is in
            the following form:
            ``projects/{project}/instances/{instance}/clusters/{cluster}``.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            The start time to list hot tablets. The hot
            tablets in the response will have start times
            between the requested start time and end time.
            Start time defaults to Now if it is unset, and
            end time defaults to Now - 24 hours if it is
            unset. The start time should be less than the
            end time, and the maximum allowed time range
            between start time and end time is 48 hours.
            Start time and end time should have values
            between Now and Now - 14 days.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The end time to list hot tablets.
        page_size (int):
            Maximum number of results per page.

            A page_size that is empty or zero lets the server choose the
            number of items to return. A page_size which is strictly
            positive will return at most that many items. A negative
            page_size will cause an error.

            Following the first request, subsequent paginated calls do
            not need a page_size field. If a page_size is set in
            subsequent calls, it must match the page_size given in the
            first request.
        page_token (str):
            The value of ``next_page_token`` returned by a previous
            call.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    start_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    page_size = proto.Field(
        proto.INT32,
        number=4,
    )
    page_token = proto.Field(
        proto.STRING,
        number=5,
    )


class ListHotTabletsResponse(proto.Message):
    r"""Response message for BigtableInstanceAdmin.ListHotTablets.

    Attributes:
        hot_tablets (Sequence[google.cloud.bigtable_admin_v2.types.HotTablet]):
            List of hot tablets in the tables of the
            requested cluster that fall within the requested
            time range. Hot tablets are ordered by node cpu
            usage percent. If there are multiple hot tablets
            that correspond to the same tablet within a
            15-minute interval, only the hot tablet with the
            highest node cpu usage will be included in the
            response.
        next_page_token (str):
            Set if not all hot tablets could be returned in a single
            response. Pass this value to ``page_token`` in another
            request to get the next page of results.
    """

    @property
    def raw_page(self):
        return self

    hot_tablets = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gba_instance.HotTablet,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
