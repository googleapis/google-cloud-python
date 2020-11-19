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


from google.cloud.orgpolicy.v1 import orgpolicy_pb2 as orgpolicy  # type: ignore
from google.cloud.osconfig_v1 import Inventory  # type: ignore
from google.iam.v1 import policy_pb2 as gi_policy  # type: ignore
from google.identity.accesscontextmanager.v1 import access_level_pb2 as gia_access_level  # type: ignore
from google.identity.accesscontextmanager.v1 import access_policy_pb2 as gia_access_policy  # type: ignore
from google.identity.accesscontextmanager.v1 import service_perimeter_pb2 as gia_service_perimeter  # type: ignore
from google.protobuf import struct_pb2 as struct  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import code_pb2 as gr_code  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.asset.v1",
    manifest={
        "TemporalAsset",
        "TimeWindow",
        "Asset",
        "Resource",
        "ResourceSearchResult",
        "IamPolicySearchResult",
        "IamPolicyAnalysisState",
        "IamPolicyAnalysisResult",
    },
)


class TemporalAsset(proto.Message):
    r"""An asset in Google Cloud and its temporal metadata, including
    the time window when it was observed and its status during that
    window.

    Attributes:
        window (~.assets.TimeWindow):
            The time window when the asset data and state
            was observed.
        deleted (bool):
            Whether the asset has been deleted or not.
        asset (~.assets.Asset):
            An asset in Google Cloud.
        prior_asset_state (~.assets.TemporalAsset.PriorAssetState):
            State of prior_asset.
        prior_asset (~.assets.Asset):
            Prior copy of the asset. Populated if prior_asset_state is
            PRESENT. Currently this is only set for responses in
            Real-Time Feed.
    """

    class PriorAssetState(proto.Enum):
        r"""State of prior asset."""
        PRIOR_ASSET_STATE_UNSPECIFIED = 0
        PRESENT = 1
        INVALID = 2
        DOES_NOT_EXIST = 3
        DELETED = 4

    window = proto.Field(proto.MESSAGE, number=1, message="TimeWindow",)

    deleted = proto.Field(proto.BOOL, number=2)

    asset = proto.Field(proto.MESSAGE, number=3, message="Asset",)

    prior_asset_state = proto.Field(proto.ENUM, number=4, enum=PriorAssetState,)

    prior_asset = proto.Field(proto.MESSAGE, number=5, message="Asset",)


class TimeWindow(proto.Message):
    r"""A time window specified by its ``start_time`` and ``end_time``.

    Attributes:
        start_time (~.timestamp.Timestamp):
            Start time of the time window (exclusive).
        end_time (~.timestamp.Timestamp):
            End time of the time window (inclusive). If
            not specified, the current timestamp is used
            instead.
    """

    start_time = proto.Field(proto.MESSAGE, number=1, message=timestamp.Timestamp,)

    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)


class Asset(proto.Message):
    r"""An asset in Google Cloud. An asset can be any resource in the Google
    Cloud `resource
    hierarchy <https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy>`__,
    a resource outside the Google Cloud resource hierarchy (such as
    Google Kubernetes Engine clusters and objects), or a policy (e.g.
    Cloud IAM policy). See `Supported asset
    types <https://cloud.google.com/asset-inventory/docs/supported-asset-types>`__
    for more information.

    Attributes:
        update_time (~.timestamp.Timestamp):
            The last update timestamp of an asset. update_time is
            updated when create/update/delete operation is performed.
        name (str):
            The full name of the asset. Example:
            ``//compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1``

            See `Resource
            names <https://cloud.google.com/apis/design/resource_names#full_resource_name>`__
            for more information.
        asset_type (str):
            The type of the asset. Example:
            ``compute.googleapis.com/Disk``

            See `Supported asset
            types <https://cloud.google.com/asset-inventory/docs/supported-asset-types>`__
            for more information.
        resource (~.assets.Resource):
            A representation of the resource.
        iam_policy (~.gi_policy.Policy):
            A representation of the Cloud IAM policy set on a Google
            Cloud resource. There can be a maximum of one Cloud IAM
            policy set on any given resource. In addition, Cloud IAM
            policies inherit their granted access scope from any
            policies set on parent resources in the resource hierarchy.
            Therefore, the effectively policy is the union of both the
            policy set on this resource and each policy set on all of
            the resource's ancestry resource levels in the hierarchy.
            See `this
            topic <https://cloud.google.com/iam/docs/policies#inheritance>`__
            for more information.
        org_policy (Sequence[~.orgpolicy.Policy]):
            A representation of an `organization
            policy <https://cloud.google.com/resource-manager/docs/organization-policy/overview#organization_policy>`__.
            There can be more than one organization policy with
            different constraints set on a given resource.
        access_policy (~.gia_access_policy.AccessPolicy):
            Please also refer to the `access policy user
            guide <https://cloud.google.com/access-context-manager/docs/overview#access-policies>`__.
        access_level (~.gia_access_level.AccessLevel):
            Please also refer to the `access level user
            guide <https://cloud.google.com/access-context-manager/docs/overview#access-levels>`__.
        service_perimeter (~.gia_service_perimeter.ServicePerimeter):
            Please also refer to the `service perimeter user
            guide <https://cloud.google.com/vpc-service-controls/docs/overview>`__.
        os_inventory (~.inventory.Inventory):
            A representation of runtime OS Inventory information. See
            `this
            topic <https://cloud.google.com/compute/docs/instances/os-inventory-management>`__
            for more information.
        ancestors (Sequence[str]):
            The ancestry path of an asset in Google Cloud `resource
            hierarchy <https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy>`__,
            represented as a list of relative resource names. An
            ancestry path starts with the closest ancestor in the
            hierarchy and ends at root. If the asset is a project,
            folder, or organization, the ancestry path starts from the
            asset itself.

            Example:
            ``["projects/123456789", "folders/5432", "organizations/1234"]``
    """

    update_time = proto.Field(proto.MESSAGE, number=11, message=timestamp.Timestamp,)

    name = proto.Field(proto.STRING, number=1)

    asset_type = proto.Field(proto.STRING, number=2)

    resource = proto.Field(proto.MESSAGE, number=3, message="Resource",)

    iam_policy = proto.Field(proto.MESSAGE, number=4, message=gi_policy.Policy,)

    org_policy = proto.RepeatedField(proto.MESSAGE, number=6, message=orgpolicy.Policy,)

    access_policy = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="access_context_policy",
        message=gia_access_policy.AccessPolicy,
    )

    access_level = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="access_context_policy",
        message=gia_access_level.AccessLevel,
    )

    service_perimeter = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="access_context_policy",
        message=gia_service_perimeter.ServicePerimeter,
    )

    os_inventory = proto.Field(proto.MESSAGE, number=12, message=Inventory,)

    ancestors = proto.RepeatedField(proto.STRING, number=10)


class Resource(proto.Message):
    r"""A representation of a Google Cloud resource.

    Attributes:
        version (str):
            The API version. Example: ``v1``
        discovery_document_uri (str):
            The URL of the discovery document containing the resource's
            JSON schema. Example:
            ``https://www.googleapis.com/discovery/v1/apis/compute/v1/rest``

            This value is unspecified for resources that do not have an
            API based on a discovery document, such as Cloud Bigtable.
        discovery_name (str):
            The JSON schema name listed in the discovery document.
            Example: ``Project``

            This value is unspecified for resources that do not have an
            API based on a discovery document, such as Cloud Bigtable.
        resource_url (str):
            The REST URL for accessing the resource. An HTTP ``GET``
            request using this URL returns the resource itself. Example:
            ``https://cloudresourcemanager.googleapis.com/v1/projects/my-project-123``

            This value is unspecified for resources without a REST API.
        parent (str):
            The full name of the immediate parent of this resource. See
            `Resource
            Names <https://cloud.google.com/apis/design/resource_names#full_resource_name>`__
            for more information.

            For Google Cloud assets, this value is the parent resource
            defined in the `Cloud IAM policy
            hierarchy <https://cloud.google.com/iam/docs/overview#policy_hierarchy>`__.
            Example:
            ``//cloudresourcemanager.googleapis.com/projects/my_project_123``

            For third-party assets, this field may be set differently.
        data (~.struct.Struct):
            The content of the resource, in which some
            sensitive fields are removed and may not be
            present.
        location (str):
            The location of the resource in Google Cloud,
            such as its zone and region. For more
            information, see
            https://cloud.google.com/about/locations/.
    """

    version = proto.Field(proto.STRING, number=1)

    discovery_document_uri = proto.Field(proto.STRING, number=2)

    discovery_name = proto.Field(proto.STRING, number=3)

    resource_url = proto.Field(proto.STRING, number=4)

    parent = proto.Field(proto.STRING, number=5)

    data = proto.Field(proto.MESSAGE, number=6, message=struct.Struct,)

    location = proto.Field(proto.STRING, number=8)


class ResourceSearchResult(proto.Message):
    r"""A result of Resource Search, containing information of a
    cloud resource.

    Attributes:
        name (str):
            The full resource name of this resource. Example:
            ``//compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1``.
            See `Cloud Asset Inventory Resource Name
            Format <https://cloud.google.com/asset-inventory/docs/resource-name-format>`__
            for more information.

            To search against the ``name``:

            -  use a field query. Example: ``name:instance1``
            -  use a free text query. Example: ``instance1``
        asset_type (str):
            The type of this resource. Example:
            ``compute.googleapis.com/Disk``.

            To search against the ``asset_type``:

            -  specify the ``asset_type`` field in your search request.
        project (str):
            The project that this resource belongs to, in the form of
            projects/{PROJECT_NUMBER}.

            To search against the ``project``:

            -  specify the ``scope`` field as this project in your
               search request.
        display_name (str):
            The display name of this resource.

            To search against the ``display_name``:

            -  use a field query. Example: ``displayName:"My Instance"``
            -  use a free text query. Example: ``"My Instance"``
        description (str):
            One or more paragraphs of text description of this resource.
            Maximum length could be up to 1M bytes.

            To search against the ``description``:

            -  use a field query. Example:
               ``description:"*important instance*"``
            -  use a free text query. Example:
               ``"*important instance*"``
        location (str):
            Location can be ``global``, regional like ``us-east1``, or
            zonal like ``us-west1-b``.

            To search against the ``location``:

            -  use a field query. Example: ``location:us-west*``
            -  use a free text query. Example: ``us-west*``
        labels (Sequence[~.assets.ResourceSearchResult.LabelsEntry]):
            Labels associated with this resource. See `Labelling and
            grouping GCP
            resources <https://cloud.google.com/blog/products/gcp/labelling-and-grouping-your-google-cloud-platform-resources>`__
            for more information.

            To search against the ``labels``:

            -  use a field query:

               -  query on any label's key or value. Example:
                  ``labels:prod``
               -  query by a given label. Example: ``labels.env:prod``
               -  query by a given label's existence. Example:
                  ``labels.env:*``

            -  use a free text query. Example: ``prod``
        network_tags (Sequence[str]):
            Network tags associated with this resource. Like labels,
            network tags are a type of annotations used to group GCP
            resources. See `Labelling GCP
            resources <https://cloud.google.com/blog/products/gcp/labelling-and-grouping-your-google-cloud-platform-resources>`__
            for more information.

            To search against the ``network_tags``:

            -  use a field query. Example: ``networkTags:internal``
            -  use a free text query. Example: ``internal``
        additional_attributes (~.struct.Struct):
            The additional searchable attributes of this resource. The
            attributes may vary from one resource type to another.
            Examples: ``projectId`` for Project, ``dnsName`` for DNS
            ManagedZone. This field contains a subset of the resource
            metadata fields that are returned by the List or Get APIs
            provided by the corresponding GCP service (e.g., Compute
            Engine). see `API references and supported searchable
            attributes <https://cloud.google.com/asset-inventory/docs/supported-asset-types#searchable_asset_types>`__
            for more information.

            You can search values of these fields through free text
            search. However, you should not consume the field
            programically as the field names and values may change as
            the GCP service updates to a new incompatible API version.

            To search against the ``additional_attributes``:

            -  use a free text query to match the attributes values.
               Example: to search
               ``additional_attributes = { dnsName: "foobar" }``, you
               can issue a query ``foobar``.
    """

    name = proto.Field(proto.STRING, number=1)

    asset_type = proto.Field(proto.STRING, number=2)

    project = proto.Field(proto.STRING, number=3)

    display_name = proto.Field(proto.STRING, number=4)

    description = proto.Field(proto.STRING, number=5)

    location = proto.Field(proto.STRING, number=6)

    labels = proto.MapField(proto.STRING, proto.STRING, number=7)

    network_tags = proto.RepeatedField(proto.STRING, number=8)

    additional_attributes = proto.Field(proto.MESSAGE, number=9, message=struct.Struct,)


class IamPolicySearchResult(proto.Message):
    r"""A result of IAM Policy search, containing information of an
    IAM policy.

    Attributes:
        resource (str):
            The full resource name of the resource associated with this
            IAM policy. Example:
            ``//compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1``.
            See `Cloud Asset Inventory Resource Name
            Format <https://cloud.google.com/asset-inventory/docs/resource-name-format>`__
            for more information.

            To search against the ``resource``:

            -  use a field query. Example:
               ``resource:organizations/123``
        project (str):
            The project that the associated GCP resource belongs to, in
            the form of projects/{PROJECT_NUMBER}. If an IAM policy is
            set on a resource (like VM instance, Cloud Storage bucket),
            the project field will indicate the project that contains
            the resource. If an IAM policy is set on a folder or
            orgnization, the project field will be empty.

            To search against the ``project``:

            -  specify the ``scope`` field as this project in your
               search request.
        policy (~.gi_policy.Policy):
            The IAM policy directly set on the given resource. Note that
            the original IAM policy can contain multiple bindings. This
            only contains the bindings that match the given query. For
            queries that don't contain a constrain on policies (e.g., an
            empty query), this contains all the bindings.

            To search against the ``policy`` bindings:

            -  use a field query:

               -  query by the policy contained members. Example:
                  ``policy:amy@gmail.com``
               -  query by the policy contained roles. Example:
                  ``policy:roles/compute.admin``
               -  query by the policy contained roles' included
                  permissions. Example:
                  ``policy.role.permissions:compute.instances.create``
        explanation (~.assets.IamPolicySearchResult.Explanation):
            Explanation about the IAM policy search
            result. It contains additional information to
            explain why the search result matches the query.
    """

    class Explanation(proto.Message):
        r"""Explanation about the IAM policy search result.

        Attributes:
            matched_permissions (Sequence[~.assets.IamPolicySearchResult.Explanation.MatchedPermissionsEntry]):
                The map from roles to their included permissions that match
                the permission query (i.e., a query containing
                ``policy.role.permissions:``). Example: if query
                ``policy.role.permissions:compute.disk.get`` matches a
                policy binding that contains owner role, the
                matched_permissions will be
                ``{"roles/owner": ["compute.disk.get"]}``. The roles can
                also be found in the returned ``policy`` bindings. Note that
                the map is populated only for requests with permission
                queries.
        """

        class Permissions(proto.Message):
            r"""IAM permissions

            Attributes:
                permissions (Sequence[str]):
                    A list of permissions. A sample permission string:
                    ``compute.disk.get``.
            """

            permissions = proto.RepeatedField(proto.STRING, number=1)

        matched_permissions = proto.MapField(
            proto.STRING,
            proto.MESSAGE,
            number=1,
            message="IamPolicySearchResult.Explanation.Permissions",
        )

    resource = proto.Field(proto.STRING, number=1)

    project = proto.Field(proto.STRING, number=2)

    policy = proto.Field(proto.MESSAGE, number=3, message=gi_policy.Policy,)

    explanation = proto.Field(proto.MESSAGE, number=4, message=Explanation,)


class IamPolicyAnalysisState(proto.Message):
    r"""Represents the detailed state of an entity under analysis,
    such as a resource, an identity or an access.

    Attributes:
        code (~.gr_code.Code):
            The Google standard error code that best describes the
            state. For example:

            -  OK means the analysis on this entity has been
               successfully finished;
            -  PERMISSION_DENIED means an access denied error is
               encountered;
            -  DEADLINE_EXCEEDED means the analysis on this entity
               hasn't been started in time;
        cause (str):
            The human-readable description of the cause
            of failure.
    """

    code = proto.Field(proto.ENUM, number=1, enum=gr_code.Code,)

    cause = proto.Field(proto.STRING, number=2)


class IamPolicyAnalysisResult(proto.Message):
    r"""IAM Policy analysis result, consisting of one IAM policy
    binding and derived access control lists.

    Attributes:
        attached_resource_full_name (str):
            The `full resource
            name <https://cloud.google.com/asset-inventory/docs/resource-name-format>`__
            of the resource to which the
            [iam_binding][google.cloud.asset.v1.IamPolicyAnalysisResult.iam_binding]
            policy attaches.
        iam_binding (~.gi_policy.Binding):
            The Cloud IAM policy binding under analysis.
        access_control_lists (Sequence[~.assets.IamPolicyAnalysisResult.AccessControlList]):
            The access control lists derived from the
            [iam_binding][google.cloud.asset.v1.IamPolicyAnalysisResult.iam_binding]
            that match or potentially match resource and access
            selectors specified in the request.
        identity_list (~.assets.IamPolicyAnalysisResult.IdentityList):
            The identity list derived from members of the
            [iam_binding][google.cloud.asset.v1.IamPolicyAnalysisResult.iam_binding]
            that match or potentially match identity selector specified
            in the request.
        fully_explored (bool):
            Represents whether all analyses on the
            [iam_binding][google.cloud.asset.v1.IamPolicyAnalysisResult.iam_binding]
            have successfully finished.
    """

    class Resource(proto.Message):
        r"""A Google Cloud resource under analysis.

        Attributes:
            full_resource_name (str):
                The `full resource
                name <https://cloud.google.com/asset-inventory/docs/resource-name-format>`__
            analysis_state (~.assets.IamPolicyAnalysisState):
                The analysis state of this resource.
        """

        full_resource_name = proto.Field(proto.STRING, number=1)

        analysis_state = proto.Field(
            proto.MESSAGE, number=2, message="IamPolicyAnalysisState",
        )

    class Access(proto.Message):
        r"""An IAM role or permission under analysis.

        Attributes:
            role (str):
                The role.
            permission (str):
                The permission.
            analysis_state (~.assets.IamPolicyAnalysisState):
                The analysis state of this access.
        """

        role = proto.Field(proto.STRING, number=1, oneof="oneof_access")

        permission = proto.Field(proto.STRING, number=2, oneof="oneof_access")

        analysis_state = proto.Field(
            proto.MESSAGE, number=3, message="IamPolicyAnalysisState",
        )

    class Identity(proto.Message):
        r"""An identity under analysis.

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
            analysis_state (~.assets.IamPolicyAnalysisState):
                The analysis state of this identity.
        """

        name = proto.Field(proto.STRING, number=1)

        analysis_state = proto.Field(
            proto.MESSAGE, number=2, message="IamPolicyAnalysisState",
        )

    class Edge(proto.Message):
        r"""A directional edge.

        Attributes:
            source_node (str):
                The source node of the edge. For example, it
                could be a full resource name for a resource
                node or an email of an identity.
            target_node (str):
                The target node of the edge. For example, it
                could be a full resource name for a resource
                node or an email of an identity.
        """

        source_node = proto.Field(proto.STRING, number=1)

        target_node = proto.Field(proto.STRING, number=2)

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
            resources (Sequence[~.assets.IamPolicyAnalysisResult.Resource]):
                The resources that match one of the following conditions:

                -  The resource_selector, if it is specified in request;
                -  Otherwise, resources reachable from the policy attached
                   resource.
            accesses (Sequence[~.assets.IamPolicyAnalysisResult.Access]):
                The accesses that match one of the following conditions:

                -  The access_selector, if it is specified in request;
                -  Otherwise, access specifiers reachable from the policy
                   binding's role.
            resource_edges (Sequence[~.assets.IamPolicyAnalysisResult.Edge]):
                Resource edges of the graph starting from the policy
                attached resource to any descendant resources. The
                [Edge.source_node][google.cloud.asset.v1.IamPolicyAnalysisResult.Edge.source_node]
                contains the full resource name of a parent resource and
                [Edge.target_node][google.cloud.asset.v1.IamPolicyAnalysisResult.Edge.target_node]
                contains the full resource name of a child resource. This
                field is present only if the output_resource_edges option is
                enabled in request.
        """

        resources = proto.RepeatedField(
            proto.MESSAGE, number=1, message="IamPolicyAnalysisResult.Resource",
        )

        accesses = proto.RepeatedField(
            proto.MESSAGE, number=2, message="IamPolicyAnalysisResult.Access",
        )

        resource_edges = proto.RepeatedField(
            proto.MESSAGE, number=3, message="IamPolicyAnalysisResult.Edge",
        )

    class IdentityList(proto.Message):
        r"""The identities and group edges.

        Attributes:
            identities (Sequence[~.assets.IamPolicyAnalysisResult.Identity]):
                Only the identities that match one of the following
                conditions will be presented:

                -  The identity_selector, if it is specified in request;
                -  Otherwise, identities reachable from the policy binding's
                   members.
            group_edges (Sequence[~.assets.IamPolicyAnalysisResult.Edge]):
                Group identity edges of the graph starting from the
                binding's group members to any node of the
                [identities][google.cloud.asset.v1.IamPolicyAnalysisResult.IdentityList.identities].
                The
                [Edge.source_node][google.cloud.asset.v1.IamPolicyAnalysisResult.Edge.source_node]
                contains a group, such as ``group:parent@google.com``. The
                [Edge.target_node][google.cloud.asset.v1.IamPolicyAnalysisResult.Edge.target_node]
                contains a member of the group, such as
                ``group:child@google.com`` or ``user:foo@google.com``. This
                field is present only if the output_group_edges option is
                enabled in request.
        """

        identities = proto.RepeatedField(
            proto.MESSAGE, number=1, message="IamPolicyAnalysisResult.Identity",
        )

        group_edges = proto.RepeatedField(
            proto.MESSAGE, number=2, message="IamPolicyAnalysisResult.Edge",
        )

    attached_resource_full_name = proto.Field(proto.STRING, number=1)

    iam_binding = proto.Field(proto.MESSAGE, number=2, message=gi_policy.Binding,)

    access_control_lists = proto.RepeatedField(
        proto.MESSAGE, number=3, message=AccessControlList,
    )

    identity_list = proto.Field(proto.MESSAGE, number=4, message=IdentityList,)

    fully_explored = proto.Field(proto.BOOL, number=5)


__all__ = tuple(sorted(__protobuf__.manifest))
