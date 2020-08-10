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


from google.protobuf import duration_pb2 as duration  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dataproc.v1",
    manifest={
        "AutoscalingPolicy",
        "BasicAutoscalingAlgorithm",
        "BasicYarnAutoscalingConfig",
        "InstanceGroupAutoscalingPolicyConfig",
        "CreateAutoscalingPolicyRequest",
        "GetAutoscalingPolicyRequest",
        "UpdateAutoscalingPolicyRequest",
        "DeleteAutoscalingPolicyRequest",
        "ListAutoscalingPoliciesRequest",
        "ListAutoscalingPoliciesResponse",
    },
)


class AutoscalingPolicy(proto.Message):
    r"""Describes an autoscaling policy for Dataproc cluster
    autoscaler.

    Attributes:
        id (str):
            Required. The policy id.

            The id must contain only letters (a-z, A-Z), numbers (0-9),
            underscores (_), and hyphens (-). Cannot begin or end with
            underscore or hyphen. Must consist of between 3 and 50
            characters.
        name (str):
            Output only. The "resource name" of the autoscaling policy,
            as described in
            https://cloud.google.com/apis/design/resource_names.

            -  For ``projects.regions.autoscalingPolicies``, the
               resource name of the policy has the following format:
               ``projects/{project_id}/regions/{region}/autoscalingPolicies/{policy_id}``

            -  For ``projects.locations.autoscalingPolicies``, the
               resource name of the policy has the following format:
               ``projects/{project_id}/locations/{location}/autoscalingPolicies/{policy_id}``
        basic_algorithm (~.autoscaling_policies.BasicAutoscalingAlgorithm):

        worker_config (~.autoscaling_policies.InstanceGroupAutoscalingPolicyConfig):
            Required. Describes how the autoscaler will
            operate for primary workers.
        secondary_worker_config (~.autoscaling_policies.InstanceGroupAutoscalingPolicyConfig):
            Optional. Describes how the autoscaler will
            operate for secondary workers.
    """

    id = proto.Field(proto.STRING, number=1)

    name = proto.Field(proto.STRING, number=2)

    basic_algorithm = proto.Field(
        proto.MESSAGE, number=3, oneof="algorithm", message="BasicAutoscalingAlgorithm",
    )

    worker_config = proto.Field(
        proto.MESSAGE, number=4, message="InstanceGroupAutoscalingPolicyConfig",
    )

    secondary_worker_config = proto.Field(
        proto.MESSAGE, number=5, message="InstanceGroupAutoscalingPolicyConfig",
    )


class BasicAutoscalingAlgorithm(proto.Message):
    r"""Basic algorithm for autoscaling.

    Attributes:
        yarn_config (~.autoscaling_policies.BasicYarnAutoscalingConfig):
            Required. YARN autoscaling configuration.
        cooldown_period (~.duration.Duration):
            Optional. Duration between scaling events. A scaling period
            starts after the update operation from the previous event
            has completed.

            Bounds: [2m, 1d]. Default: 2m.
    """

    yarn_config = proto.Field(
        proto.MESSAGE, number=1, message="BasicYarnAutoscalingConfig",
    )

    cooldown_period = proto.Field(proto.MESSAGE, number=2, message=duration.Duration,)


class BasicYarnAutoscalingConfig(proto.Message):
    r"""Basic autoscaling configurations for YARN.

    Attributes:
        graceful_decommission_timeout (~.duration.Duration):
            Required. Timeout for YARN graceful decommissioning of Node
            Managers. Specifies the duration to wait for jobs to
            complete before forcefully removing workers (and potentially
            interrupting jobs). Only applicable to downscaling
            operations.

            Bounds: [0s, 1d].
        scale_up_factor (float):
            Required. Fraction of average YARN pending memory in the
            last cooldown period for which to add workers. A scale-up
            factor of 1.0 will result in scaling up so that there is no
            pending memory remaining after the update (more aggressive
            scaling). A scale-up factor closer to 0 will result in a
            smaller magnitude of scaling up (less aggressive scaling).
            See `How autoscaling
            works <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/autoscaling#how_autoscaling_works>`__
            for more information.

            Bounds: [0.0, 1.0].
        scale_down_factor (float):
            Required. Fraction of average YARN pending memory in the
            last cooldown period for which to remove workers. A
            scale-down factor of 1 will result in scaling down so that
            there is no available memory remaining after the update
            (more aggressive scaling). A scale-down factor of 0 disables
            removing workers, which can be beneficial for autoscaling a
            single job. See `How autoscaling
            works <https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/autoscaling#how_autoscaling_works>`__
            for more information.

            Bounds: [0.0, 1.0].
        scale_up_min_worker_fraction (float):
            Optional. Minimum scale-up threshold as a fraction of total
            cluster size before scaling occurs. For example, in a
            20-worker cluster, a threshold of 0.1 means the autoscaler
            must recommend at least a 2-worker scale-up for the cluster
            to scale. A threshold of 0 means the autoscaler will scale
            up on any recommended change.

            Bounds: [0.0, 1.0]. Default: 0.0.
        scale_down_min_worker_fraction (float):
            Optional. Minimum scale-down threshold as a fraction of
            total cluster size before scaling occurs. For example, in a
            20-worker cluster, a threshold of 0.1 means the autoscaler
            must recommend at least a 2 worker scale-down for the
            cluster to scale. A threshold of 0 means the autoscaler will
            scale down on any recommended change.

            Bounds: [0.0, 1.0]. Default: 0.0.
    """

    graceful_decommission_timeout = proto.Field(
        proto.MESSAGE, number=5, message=duration.Duration,
    )

    scale_up_factor = proto.Field(proto.DOUBLE, number=1)

    scale_down_factor = proto.Field(proto.DOUBLE, number=2)

    scale_up_min_worker_fraction = proto.Field(proto.DOUBLE, number=3)

    scale_down_min_worker_fraction = proto.Field(proto.DOUBLE, number=4)


class InstanceGroupAutoscalingPolicyConfig(proto.Message):
    r"""Configuration for the size bounds of an instance group,
    including its proportional size to other groups.

    Attributes:
        min_instances (int):
            Optional. Minimum number of instances for this group.

            Primary workers - Bounds: [2, max_instances]. Default: 2.
            Secondary workers - Bounds: [0, max_instances]. Default: 0.
        max_instances (int):
            Required. Maximum number of instances for this group.
            Required for primary workers. Note that by default, clusters
            will not use secondary workers. Required for secondary
            workers if the minimum secondary instances is set.

            Primary workers - Bounds: [min_instances, ). Secondary
            workers - Bounds: [min_instances, ). Default: 0.
        weight (int):
            Optional. Weight for the instance group, which is used to
            determine the fraction of total workers in the cluster from
            this instance group. For example, if primary workers have
            weight 2, and secondary workers have weight 1, the cluster
            will have approximately 2 primary workers for each secondary
            worker.

            The cluster may not reach the specified balance if
            constrained by min/max bounds or other autoscaling settings.
            For example, if ``max_instances`` for secondary workers is
            0, then only primary workers will be added. The cluster can
            also be out of balance when created.

            If weight is not set on any instance group, the cluster will
            default to equal weight for all groups: the cluster will
            attempt to maintain an equal number of workers in each group
            within the configured size bounds for each group. If weight
            is set for one group only, the cluster will default to zero
            weight on the unset group. For example if weight is set only
            on primary workers, the cluster will use primary workers
            only and no secondary workers.
    """

    min_instances = proto.Field(proto.INT32, number=1)

    max_instances = proto.Field(proto.INT32, number=2)

    weight = proto.Field(proto.INT32, number=3)


class CreateAutoscalingPolicyRequest(proto.Message):
    r"""A request to create an autoscaling policy.

    Attributes:
        parent (str):
            Required. The "resource name" of the region or location, as
            described in
            https://cloud.google.com/apis/design/resource_names.

            -  For ``projects.regions.autoscalingPolicies.create``, the
               resource name of the region has the following format:
               ``projects/{project_id}/regions/{region}``

            -  For ``projects.locations.autoscalingPolicies.create``,
               the resource name of the location has the following
               format: ``projects/{project_id}/locations/{location}``
        policy (~.autoscaling_policies.AutoscalingPolicy):
            Required. The autoscaling policy to create.
    """

    parent = proto.Field(proto.STRING, number=1)

    policy = proto.Field(proto.MESSAGE, number=2, message=AutoscalingPolicy,)


class GetAutoscalingPolicyRequest(proto.Message):
    r"""A request to fetch an autoscaling policy.

    Attributes:
        name (str):
            Required. The "resource name" of the autoscaling policy, as
            described in
            https://cloud.google.com/apis/design/resource_names.

            -  For ``projects.regions.autoscalingPolicies.get``, the
               resource name of the policy has the following format:
               ``projects/{project_id}/regions/{region}/autoscalingPolicies/{policy_id}``

            -  For ``projects.locations.autoscalingPolicies.get``, the
               resource name of the policy has the following format:
               ``projects/{project_id}/locations/{location}/autoscalingPolicies/{policy_id}``
    """

    name = proto.Field(proto.STRING, number=1)


class UpdateAutoscalingPolicyRequest(proto.Message):
    r"""A request to update an autoscaling policy.

    Attributes:
        policy (~.autoscaling_policies.AutoscalingPolicy):
            Required. The updated autoscaling policy.
    """

    policy = proto.Field(proto.MESSAGE, number=1, message=AutoscalingPolicy,)


class DeleteAutoscalingPolicyRequest(proto.Message):
    r"""A request to delete an autoscaling policy.
    Autoscaling policies in use by one or more clusters will not be
    deleted.

    Attributes:
        name (str):
            Required. The "resource name" of the autoscaling policy, as
            described in
            https://cloud.google.com/apis/design/resource_names.

            -  For ``projects.regions.autoscalingPolicies.delete``, the
               resource name of the policy has the following format:
               ``projects/{project_id}/regions/{region}/autoscalingPolicies/{policy_id}``

            -  For ``projects.locations.autoscalingPolicies.delete``,
               the resource name of the policy has the following format:
               ``projects/{project_id}/locations/{location}/autoscalingPolicies/{policy_id}``
    """

    name = proto.Field(proto.STRING, number=1)


class ListAutoscalingPoliciesRequest(proto.Message):
    r"""A request to list autoscaling policies in a project.

    Attributes:
        parent (str):
            Required. The "resource name" of the region or location, as
            described in
            https://cloud.google.com/apis/design/resource_names.

            -  For ``projects.regions.autoscalingPolicies.list``, the
               resource name of the region has the following format:
               ``projects/{project_id}/regions/{region}``

            -  For ``projects.locations.autoscalingPolicies.list``, the
               resource name of the location has the following format:
               ``projects/{project_id}/locations/{location}``
        page_size (int):
            Optional. The maximum number of results to
            return in each response. Must be less than or
            equal to 1000. Defaults to 100.
        page_token (str):
            Optional. The page token, returned by a
            previous call, to request the next page of
            results.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListAutoscalingPoliciesResponse(proto.Message):
    r"""A response to a request to list autoscaling policies in a
    project.

    Attributes:
        policies (Sequence[~.autoscaling_policies.AutoscalingPolicy]):
            Output only. Autoscaling policies list.
        next_page_token (str):
            Output only. This token is included in the
            response if there are more results to fetch.
    """

    @property
    def raw_page(self):
        return self

    policies = proto.RepeatedField(proto.MESSAGE, number=1, message=AutoscalingPolicy,)

    next_page_token = proto.Field(proto.STRING, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))
