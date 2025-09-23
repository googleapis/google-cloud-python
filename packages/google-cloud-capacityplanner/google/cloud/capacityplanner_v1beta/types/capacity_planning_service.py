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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.capacityplanner_v1beta.types import location as gcc_location
from google.cloud.capacityplanner_v1beta.types import resource

__protobuf__ = proto.module(
    package="google.cloud.capacityplanner.v1beta",
    manifest={
        "State",
        "CapacityType",
        "GetCapacityPlanRequest",
        "QueryCapacityPlansRequest",
        "QueryCapacityPlansResponse",
        "QueryCapacityPlanInsightsRequest",
        "QueryCapacityPlanInsightsResponse",
        "CapacityPlanFilters",
        "CapacityPlanKey",
        "CapacityPlanView",
        "TimeSeriesView",
        "CapacityPlan",
        "DemandMetadata",
        "DemandPreference",
        "ServiceDemand",
        "ResourceDemand",
        "User",
        "DemandValues",
        "DemandValue",
        "TimeValue",
        "ChildResourceDemand",
    },
)


class State(proto.Enum):
    r"""The state of a capacity demand.

    Values:
        STATE_UNSPECIFIED (0):
            The state is unspecified.
        PENDING_REVIEW (1):
            The demand is pending review.
        IN_REVIEW (3):
            The demand is in review.
        APPROVED_PROVISIONAL (8):
            The demand is provisionally approved.
        OBSOLETE (5):
            The demand is obsolete.
        CANNOT_BE_FULFILLED (7):
            The demand cannot be fulfilled.
        ON_HOLD_CONTACT_SALES (9):
            The demand is on hold, contact sales.
        IN_FULFILLMENT (10):
            The demand is in fulfillment.
    """
    STATE_UNSPECIFIED = 0
    PENDING_REVIEW = 1
    IN_REVIEW = 3
    APPROVED_PROVISIONAL = 8
    OBSOLETE = 5
    CANNOT_BE_FULFILLED = 7
    ON_HOLD_CONTACT_SALES = 9
    IN_FULFILLMENT = 10


class CapacityType(proto.Enum):
    r"""CapacityType is the type of the capacity plan.

    Values:
        CAPACITY_TYPE_UNKNOWN (0):
            Default value.
        CAPACITY_TYPE_INORGANIC_DRAFT (1):
            Latest inorganic data stored in horizon DB
            that is in draft state.
        CAPACITY_TYPE_INORGANIC_PENDING (2):
            Latest inorganic data stored in horizon DB
            that are pending i.e. submitted or assessment.
        CAPACITY_TYPE_INORGANIC_APPROVED (3):
            Latest inorganic data stored in horizon DB
            that has been approved.
    """
    CAPACITY_TYPE_UNKNOWN = 0
    CAPACITY_TYPE_INORGANIC_DRAFT = 1
    CAPACITY_TYPE_INORGANIC_PENDING = 2
    CAPACITY_TYPE_INORGANIC_APPROVED = 3


class GetCapacityPlanRequest(proto.Message):
    r"""Request for getting a capacity plan.

    Attributes:
        name (str):
            Required. The name of the capacity plan to retrieve. Format:
            projects/{project}/capacityPlans/{capacity_plan}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class QueryCapacityPlansRequest(proto.Message):
    r"""Request for querying capacity plans.

    Attributes:
        parent (str):
            Required. The parent resource container.
            Format:

                    projects/{project} or
                    folders/{folder} or
                    organizations/{organization}
        page_size (int):
            Optional. The maximum number of plans to
            return per page. The service may return fewer
            than this value. If unspecified, the server will
            use a sensible default. The maximum value is
            1000; values above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``QueryCapacityPlans`` call. Provide this to retrieve the
            subsequent page.
        location (str):
            Optional. The Google Cloud Platform location
            of capacity plans. If unspecified, all locations
            will be included.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    location: str = proto.Field(
        proto.STRING,
        number=4,
    )


class QueryCapacityPlansResponse(proto.Message):
    r"""Response of querying capacity plans.

    Attributes:
        capacity_plans (MutableSequence[google.cloud.capacityplanner_v1beta.types.CapacityPlan]):
            List of capacity plans.
        next_page_token (str):
            Token to retrieve the next page of results.
            This will be empty if there are no more pages.
    """

    @property
    def raw_page(self):
        return self

    capacity_plans: MutableSequence["CapacityPlan"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="CapacityPlan",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class QueryCapacityPlanInsightsRequest(proto.Message):
    r"""Request for capacity plan insights.

    Attributes:
        parent (str):
            Required. The parent resource container.
            Format: projects/{project}
        capacity_plan_filters (google.cloud.capacityplanner_v1beta.types.CapacityPlanFilters):
            Required. The filters to apply to the
            capacity plan.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    capacity_plan_filters: "CapacityPlanFilters" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="CapacityPlanFilters",
    )


class QueryCapacityPlanInsightsResponse(proto.Message):
    r"""Response for capacity plan insights.

    Attributes:
        aggregated_capacity_plan_view (google.cloud.capacityplanner_v1beta.types.CapacityPlanView):
            Optional. The aggregated capacity plan view.
            This is the aggregated view of all the capacity
            plans that match the filters.
    """

    aggregated_capacity_plan_view: "CapacityPlanView" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="CapacityPlanView",
    )


class CapacityPlanFilters(proto.Message):
    r"""CapacityPlanFilters is a set of filters to apply to the
    capacity plan.

    Attributes:
        keys (MutableSequence[google.cloud.capacityplanner_v1beta.types.CapacityPlanKey]):
            Required. The capacity plan keys to include
            in the response.
        capacity_types (MutableSequence[google.cloud.capacityplanner_v1beta.types.CapacityType]):
            Required. The capacity types to include in
            the response.
        capacity_plan_id (str):
            Optional. Optional capacity plan id. Should
            be populated for request page to lock based on
            the same capacity plan.
    """

    keys: MutableSequence["CapacityPlanKey"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="CapacityPlanKey",
    )
    capacity_types: MutableSequence["CapacityType"] = proto.RepeatedField(
        proto.ENUM,
        number=2,
        enum="CapacityType",
    )
    capacity_plan_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class CapacityPlanKey(proto.Message):
    r"""CapacityPlanKey is a the unique identifier for each Capacity
    Plan.

    Attributes:
        resource_container (google.cloud.capacityplanner_v1beta.types.ResourceContainer):
            Required. The resource container associated
            with the capacity plan.
        resource_id_key (google.cloud.capacityplanner_v1beta.types.ResourceIdKey):
            Required. The resource id key associated with
            the capacity plan.
        location_id (google.cloud.capacityplanner_v1beta.types.LocationIdentifier):
            Required. Identifier of location.
    """

    resource_container: resource.ResourceContainer = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resource.ResourceContainer,
    )
    resource_id_key: resource.ResourceIdKey = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resource.ResourceIdKey,
    )
    location_id: gcc_location.LocationIdentifier = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gcc_location.LocationIdentifier,
    )


class CapacityPlanView(proto.Message):
    r"""CapacityPlanView contains the capacity plan key and the time
    series views.

    Attributes:
        key (google.cloud.capacityplanner_v1beta.types.CapacityPlanKey):
            Required. The capacity plan key associated
            with the capacity plan view.
        time_series_views (MutableSequence[google.cloud.capacityplanner_v1beta.types.TimeSeriesView]):
            Required. The time series views associated
            with the capacity plan view.
    """

    key: "CapacityPlanKey" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="CapacityPlanKey",
    )
    time_series_views: MutableSequence["TimeSeriesView"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="TimeSeriesView",
    )


class TimeSeriesView(proto.Message):
    r"""TimeSeriesView contains capacity_value which has the timeseries for
    a given type. Each type as a single timeseries associated with it.

    Attributes:
        type_ (google.cloud.capacityplanner_v1beta.types.CapacityType):
            Required. The capacity type associated with
            the time series view.
        capacity_value (google.cloud.capacityplanner_v1beta.types.DemandValue):
            Required. The capacity value associated with
            the time series view.
    """

    type_: "CapacityType" = proto.Field(
        proto.ENUM,
        number=1,
        enum="CapacityType",
    )
    capacity_value: "DemandValue" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="DemandValue",
    )


class CapacityPlan(proto.Message):
    r"""A plan for additional capacity needed by a Google Cloud
    Platform project. This is synonymous with CapacityDemand,
    CapacityRequest, and CapacityDemandRequest.

    Attributes:
        name (str):
            Identifier. The name of the capacity plan.

            Format: projects/{project}/capacityPlans/{capacity_plan_id}
        capacity_demand_metadata (google.cloud.capacityplanner_v1beta.types.DemandMetadata):
            Optional. The metadata associated with a
            capacity demand.
        service_demands (MutableSequence[google.cloud.capacityplanner_v1beta.types.ServiceDemand]):
            Required. The capacity demand associated with
            a service.
        reporter (google.cloud.capacityplanner_v1beta.types.User):
            Output only. User who created the capacity
            plan.
        state (google.cloud.capacityplanner_v1beta.types.State):
            Output only. State of the plan.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when the plan was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when the plan was last
            updated.
        description (str):
            Optional. Description of the plan.
        title (str):
            Optional. Title of the plan.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    capacity_demand_metadata: "DemandMetadata" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="DemandMetadata",
    )
    service_demands: MutableSequence["ServiceDemand"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="ServiceDemand",
    )
    reporter: "User" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="User",
    )
    state: "State" = proto.Field(
        proto.ENUM,
        number=5,
        enum="State",
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    description: str = proto.Field(
        proto.STRING,
        number=8,
    )
    title: str = proto.Field(
        proto.STRING,
        number=9,
    )


class DemandMetadata(proto.Message):
    r"""The metadata associated with a capacity demand.

    Attributes:
        demand_preferences (MutableSequence[google.cloud.capacityplanner_v1beta.types.DemandPreference]):
            Optional. The preferences associated with a
            capacity demand.
    """

    demand_preferences: MutableSequence["DemandPreference"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DemandPreference",
    )


class DemandPreference(proto.Message):
    r"""Preference associated with a request, such as flexibility
    with alternate resource type.

    Attributes:
        preference_id (str):
            Output only. The preference id.
        value (google.cloud.capacityplanner_v1beta.types.Value):
            Required. The value of demand preference.
    """

    preference_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    value: resource.Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resource.Value,
    )


class ServiceDemand(proto.Message):
    r"""Capacity demand for a service.

    Attributes:
        service (str):
            Required. Name of the service.
        demand_metadata (google.cloud.capacityplanner_v1beta.types.DemandMetadata):
            Optional. The metadata associated with a
            service demand.
        resource_demands (MutableSequence[google.cloud.capacityplanner_v1beta.types.ResourceDemand]):
            Required. The demand associated with the
            resources.
    """

    service: str = proto.Field(
        proto.STRING,
        number=1,
    )
    demand_metadata: "DemandMetadata" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="DemandMetadata",
    )
    resource_demands: MutableSequence["ResourceDemand"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="ResourceDemand",
    )


class ResourceDemand(proto.Message):
    r"""Capacity demand for a resource.

    Attributes:
        id (str):
            Output only. Identifier of resource demand.
        resource_container (google.cloud.capacityplanner_v1beta.types.ResourceContainer):
            Required. The resource container associated
            with the demand.
        resource_id (google.cloud.capacityplanner_v1beta.types.ResourceIdentifier):
            Required. Identifier of resource.
        location_id (google.cloud.capacityplanner_v1beta.types.LocationIdentifier):
            Required. Identifier of location.
        state (google.cloud.capacityplanner_v1beta.types.State):
            Output only. State of the resource demand.
        reporter (google.cloud.capacityplanner_v1beta.types.User):
            Output only. User who reported the demand.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when the demand was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when the demand was
            last updated.
        demand_values (google.cloud.capacityplanner_v1beta.types.DemandValues):
            Required. The demand values associated with
            the resource.
        demand_metadata (google.cloud.capacityplanner_v1beta.types.DemandMetadata):
            Optional. The metadata associated with the
            demand.
        child_resource_demands (MutableSequence[google.cloud.capacityplanner_v1beta.types.ChildResourceDemand]):
            Optional. The child resource demands
            associated with the resource.
    """

    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    resource_container: resource.ResourceContainer = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resource.ResourceContainer,
    )
    resource_id: resource.ResourceIdentifier = proto.Field(
        proto.MESSAGE,
        number=3,
        message=resource.ResourceIdentifier,
    )
    location_id: gcc_location.LocationIdentifier = proto.Field(
        proto.MESSAGE,
        number=4,
        message=gcc_location.LocationIdentifier,
    )
    state: "State" = proto.Field(
        proto.ENUM,
        number=5,
        enum="State",
    )
    reporter: "User" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="User",
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
    demand_values: "DemandValues" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="DemandValues",
    )
    demand_metadata: "DemandMetadata" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="DemandMetadata",
    )
    child_resource_demands: MutableSequence[
        "ChildResourceDemand"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=11,
        message="ChildResourceDemand",
    )


class User(proto.Message):
    r"""A user who created or updated a capacity demand.

    Attributes:
        email (str):
            Required. Email of the user.
    """

    email: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DemandValues(proto.Message):
    r"""The capacity demand values for a resource.

    Attributes:
        values (MutableSequence[google.cloud.capacityplanner_v1beta.types.DemandValue]):
            Required. The demand values.
    """

    values: MutableSequence["DemandValue"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DemandValue",
    )


class DemandValue(proto.Message):
    r"""Capacity demand value for a single resource attribute such as
    CPU count, vertex AI peak QPM, etc.

    Attributes:
        name (str):
            Required. The name of the demand value such
            as CPU count.
        time_values (MutableSequence[google.cloud.capacityplanner_v1beta.types.TimeValue]):
            Required. The demand values at different time
            points.
        unit (google.cloud.capacityplanner_v1beta.types.Unit):
            Required. Unit of measurement.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    time_values: MutableSequence["TimeValue"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="TimeValue",
    )
    unit: resource.Unit = proto.Field(
        proto.ENUM,
        number=3,
        enum=resource.Unit,
    )


class TimeValue(proto.Message):
    r"""Capacity demand value for a single time point.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        time (google.protobuf.timestamp_pb2.Timestamp):
            Required. The time point. If this demand
            value is non-temporal, set time to -1.
        value (float):
            Required. The demand value at the time point.

            This field is a member of `oneof`_ ``_value``.
    """

    time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    value: float = proto.Field(
        proto.DOUBLE,
        number=2,
        optional=True,
    )


class ChildResourceDemand(proto.Message):
    r"""Capacity demand for a child resource such as shapes.

    Attributes:
        resource_id (google.cloud.capacityplanner_v1beta.types.ResourceIdentifier):
            Required. Identifier of resource.
        demand_values (google.cloud.capacityplanner_v1beta.types.DemandValues):
            Required. The demand values associated with
            the child resource.
        demand_metadata (google.cloud.capacityplanner_v1beta.types.DemandMetadata):
            Optional. The metadata associated with the
            child resource demand.
    """

    resource_id: resource.ResourceIdentifier = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resource.ResourceIdentifier,
    )
    demand_values: "DemandValues" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="DemandValues",
    )
    demand_metadata: "DemandMetadata" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="DemandMetadata",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
