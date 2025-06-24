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
from google.iam.v1 import policy_pb2  # type: ignore
from google.rpc import code_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.asset.v1p4beta1",
    manifest={
        "IamPolicyAnalysisResult",
    },
)


class IamPolicyAnalysisResult(proto.Message):
    r"""IAM Policy analysis result, consisting of one IAM policy
    binding and derived access control lists.

    Attributes:
        attached_resource_full_name (str):
            The full name of the resource to which the
            [iam_binding][google.cloud.asset.v1p4beta1.IamPolicyAnalysisResult.iam_binding]
            policy attaches.
        iam_binding (google.iam.v1.policy_pb2.Binding):
            The Cloud IAM policy binding under analysis.
        access_control_lists (Sequence[google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisResult.AccessControlList]):
            The access control lists derived from the
            [iam_binding][google.cloud.asset.v1p4beta1.IamPolicyAnalysisResult.iam_binding]
            that match or potentially match resource and access
            selectors specified in the request.
        identity_list (google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisResult.IdentityList):
            The identity list derived from members of the
            [iam_binding][google.cloud.asset.v1p4beta1.IamPolicyAnalysisResult.iam_binding]
            that match or potentially match identity selector specified
            in the request.
        fully_explored (bool):
            Represents whether all nodes in the transitive closure of
            the
            [iam_binding][google.cloud.asset.v1p4beta1.IamPolicyAnalysisResult.iam_binding]
            node have been explored.
    """

    class AnalysisState(proto.Message):
        r"""Represents analysis state of each node in the result graph or
        non-critical errors in the response.

        Attributes:
            code (google.rpc.code_pb2.Code):
                The Google standard error code that best describes the
                state. For example:

                -  OK means the node has been successfully explored;
                -  PERMISSION_DENIED means an access denied error is
                   encountered;
                -  DEADLINE_EXCEEDED means the node hasn't been explored in
                   time;
            cause (str):
                The human-readable description of the cause
                of failure.
        """

        code = proto.Field(
            proto.ENUM,
            number=1,
            enum=code_pb2.Code,
        )
        cause = proto.Field(
            proto.STRING,
            number=2,
        )

    class Resource(proto.Message):
        r"""A GCP resource that appears in an access control list.

        Attributes:
            full_resource_name (str):
                The `full resource
                name <https://aip.dev/122#full-resource-names>`__.
            analysis_state (google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisResult.AnalysisState):
                The analysis state of this resource node.
        """

        full_resource_name = proto.Field(
            proto.STRING,
            number=1,
        )
        analysis_state = proto.Field(
            proto.MESSAGE,
            number=2,
            message="IamPolicyAnalysisResult.AnalysisState",
        )

    class Access(proto.Message):
        r"""A role or permission that appears in an access control list.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            role (str):
                The role.

                This field is a member of `oneof`_ ``oneof_access``.
            permission (str):
                The permission.

                This field is a member of `oneof`_ ``oneof_access``.
            analysis_state (google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisResult.AnalysisState):
                The analysis state of this access node.
        """

        role = proto.Field(
            proto.STRING,
            number=1,
            oneof="oneof_access",
        )
        permission = proto.Field(
            proto.STRING,
            number=2,
            oneof="oneof_access",
        )
        analysis_state = proto.Field(
            proto.MESSAGE,
            number=3,
            message="IamPolicyAnalysisResult.AnalysisState",
        )

    class Edge(proto.Message):
        r"""A directional edge.

        Attributes:
            source_node (str):
                The source node of the edge.
            target_node (str):
                The target node of the edge.
        """

        source_node = proto.Field(
            proto.STRING,
            number=1,
        )
        target_node = proto.Field(
            proto.STRING,
            number=2,
        )

    class Identity(proto.Message):
        r"""An identity that appears in an access control list.

        Attributes:
            name (str):
                The identity name in any form of members appear in `IAM
                policy
                binding <https://cloud.google.com/iam/reference/rest/v1/Binding>`__,
                such as:

                -  user:foo@google.com
                -  group:group1@google.com
                -  serviceAccount:s1@prj1.iam.gserviceaccount.com
                -  projectOwner:some_project_id
                -  domain:google.com
                -  allUsers
                -  etc.
            analysis_state (google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisResult.AnalysisState):
                The analysis state of this identity node.
        """

        name = proto.Field(
            proto.STRING,
            number=1,
        )
        analysis_state = proto.Field(
            proto.MESSAGE,
            number=2,
            message="IamPolicyAnalysisResult.AnalysisState",
        )

    class AccessControlList(proto.Message):
        r"""An access control list, derived from the above IAM policy binding,
        which contains a set of resources and accesses. May include one item
        from each set to compose an access control entry.

        NOTICE that there could be multiple access control lists for one IAM
        policy binding. The access control lists are created based on
        resource and access combinations.

        For example, assume we have the following cases in one IAM policy
        binding:

        -  Permission P1 and P2 apply to resource R1 and R2;
        -  Permission P3 applies to resource R2 and R3;

        This will result in the following access control lists:

        -  AccessControlList 1: [R1, R2], [P1, P2]
        -  AccessControlList 2: [R2, R3], [P3]

        Attributes:
            resources (Sequence[google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisResult.Resource]):
                The resources that match one of the following conditions:

                -  The resource_selector, if it is specified in request;
                -  Otherwise, resources reachable from the policy attached
                   resource.
            accesses (Sequence[google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisResult.Access]):
                The accesses that match one of the following conditions:

                -  The access_selector, if it is specified in request;
                -  Otherwise, access specifiers reachable from the policy
                   binding's role.
            resource_edges (Sequence[google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisResult.Edge]):
                Resource edges of the graph starting from the policy
                attached resource to any descendant resources. The
                [Edge.source_node][google.cloud.asset.v1p4beta1.IamPolicyAnalysisResult.Edge.source_node]
                contains the full resource name of a parent resource and
                [Edge.target_node][google.cloud.asset.v1p4beta1.IamPolicyAnalysisResult.Edge.target_node]
                contains the full resource name of a child resource. This
                field is present only if the output_resource_edges option is
                enabled in request.
        """

        resources = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="IamPolicyAnalysisResult.Resource",
        )
        accesses = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="IamPolicyAnalysisResult.Access",
        )
        resource_edges = proto.RepeatedField(
            proto.MESSAGE,
            number=3,
            message="IamPolicyAnalysisResult.Edge",
        )

    class IdentityList(proto.Message):
        r"""

        Attributes:
            identities (Sequence[google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisResult.Identity]):
                Only the identities that match one of the following
                conditions will be presented:

                -  The identity_selector, if it is specified in request;
                -  Otherwise, identities reachable from the policy binding's
                   members.
            group_edges (Sequence[google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisResult.Edge]):
                Group identity edges of the graph starting from the
                binding's group members to any node of the
                [identities][google.cloud.asset.v1p4beta1.IamPolicyAnalysisResult.IdentityList.identities].
                The
                [Edge.source_node][google.cloud.asset.v1p4beta1.IamPolicyAnalysisResult.Edge.source_node]
                contains a group, such as "group:parent@google.com". The
                [Edge.target_node][google.cloud.asset.v1p4beta1.IamPolicyAnalysisResult.Edge.target_node]
                contains a member of the group, such as
                "group:child@google.com" or "user:foo@google.com". This
                field is present only if the output_group_edges option is
                enabled in request.
        """

        identities = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="IamPolicyAnalysisResult.Identity",
        )
        group_edges = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="IamPolicyAnalysisResult.Edge",
        )

    attached_resource_full_name = proto.Field(
        proto.STRING,
        number=1,
    )
    iam_binding = proto.Field(
        proto.MESSAGE,
        number=2,
        message=policy_pb2.Binding,
    )
    access_control_lists = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=AccessControlList,
    )
    identity_list = proto.Field(
        proto.MESSAGE,
        number=4,
        message=IdentityList,
    )
    fully_explored = proto.Field(
        proto.BOOL,
        number=5,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
