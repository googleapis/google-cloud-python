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
from google.protobuf import duration_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.asset_v1p4beta1.types import assets

__protobuf__ = proto.module(
    package="google.cloud.asset.v1p4beta1",
    manifest={
        "IamPolicyAnalysisQuery",
        "AnalyzeIamPolicyRequest",
        "AnalyzeIamPolicyResponse",
        "IamPolicyAnalysisOutputConfig",
        "ExportIamPolicyAnalysisRequest",
        "ExportIamPolicyAnalysisResponse",
    },
)


class IamPolicyAnalysisQuery(proto.Message):
    r"""IAM policy analysis query message.

    Attributes:
        parent (str):
            Required. The relative name of the root
            asset. Only resources and IAM policies within
            the parent will be analyzed. This can only be an
            organization number (such as
            "organizations/123") or a folder number (such as
            "folders/123").
        resource_selector (google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisQuery.ResourceSelector):
            Optional. Specifies a resource for analysis.
            Leaving it empty means ANY.
        identity_selector (google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisQuery.IdentitySelector):
            Optional. Specifies an identity for analysis.
            Leaving it empty means ANY.
        access_selector (google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisQuery.AccessSelector):
            Optional. Specifies roles or permissions for
            analysis. Leaving it empty means ANY.
    """

    class ResourceSelector(proto.Message):
        r"""Specifies the resource to analyze for access policies, which may be
        set directly on the resource, or on ancestors such as organizations,
        folders or projects. At least one of
        [ResourceSelector][google.cloud.asset.v1p4beta1.IamPolicyAnalysisQuery.ResourceSelector],
        [IdentitySelector][google.cloud.asset.v1p4beta1.IamPolicyAnalysisQuery.IdentitySelector]
        or
        [AccessSelector][google.cloud.asset.v1p4beta1.IamPolicyAnalysisQuery.AccessSelector]
        must be specified in a request.

        Attributes:
            full_resource_name (str):
                Required. The `full resource
                name <https://cloud.google.com/apis/design/resource_names#full_resource_name>`__
                .
        """

        full_resource_name = proto.Field(
            proto.STRING,
            number=1,
        )

    class IdentitySelector(proto.Message):
        r"""Specifies an identity for which to determine resource access,
        based on roles assigned either directly to them or to the groups
        they belong to, directly or indirectly.

        Attributes:
            identity (str):
                Required. The identity appear in the form of members in `IAM
                policy
                binding <https://cloud.google.com/iam/reference/rest/v1/Binding>`__.
        """

        identity = proto.Field(
            proto.STRING,
            number=1,
        )

    class AccessSelector(proto.Message):
        r"""Specifies roles and/or permissions to analyze, to determine
        both the identities possessing them and the resources they
        control. If multiple values are specified, results will include
        identities and resources matching any of them.

        Attributes:
            roles (Sequence[str]):
                Optional. The roles to appear in result.
            permissions (Sequence[str]):
                Optional. The permissions to appear in
                result.
        """

        roles = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        permissions = proto.RepeatedField(
            proto.STRING,
            number=2,
        )

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    resource_selector = proto.Field(
        proto.MESSAGE,
        number=2,
        message=ResourceSelector,
    )
    identity_selector = proto.Field(
        proto.MESSAGE,
        number=3,
        message=IdentitySelector,
    )
    access_selector = proto.Field(
        proto.MESSAGE,
        number=4,
        message=AccessSelector,
    )


class AnalyzeIamPolicyRequest(proto.Message):
    r"""A request message for
    [AssetService.AnalyzeIamPolicy][google.cloud.asset.v1p4beta1.AssetService.AnalyzeIamPolicy].

    Attributes:
        analysis_query (google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisQuery):
            Required. The request query.
        options (google.cloud.asset_v1p4beta1.types.AnalyzeIamPolicyRequest.Options):
            Optional. The request options.
    """

    class Options(proto.Message):
        r"""Contains request options.

        Attributes:
            expand_groups (bool):
                Optional. If true, the identities section of the result will
                expand any Google groups appearing in an IAM policy binding.

                If [identity_selector][] is specified, the identity in the
                result will be determined by the selector, and this flag
                will have no effect.

                Default is false.
            expand_roles (bool):
                Optional. If true, the access section of result will expand
                any roles appearing in IAM policy bindings to include their
                permissions.

                If [access_selector][] is specified, the access section of
                the result will be determined by the selector, and this flag
                will have no effect.

                Default is false.
            expand_resources (bool):
                Optional. If true, the resource section of the result will
                expand any resource attached to an IAM policy to include
                resources lower in the resource hierarchy.

                For example, if the request analyzes for which resources
                user A has permission P, and the results include an IAM
                policy with P on a GCP folder, the results will also include
                resources in that folder with permission P.

                If [resource_selector][] is specified, the resource section
                of the result will be determined by the selector, and this
                flag will have no effect. Default is false.
            output_resource_edges (bool):
                Optional. If true, the result will output
                resource edges, starting from the policy
                attached resource, to any expanded resources.
                Default is false.
            output_group_edges (bool):
                Optional. If true, the result will output
                group identity edges, starting from the
                binding's group members, to any expanded
                identities. Default is false.
            analyze_service_account_impersonation (bool):
                Optional. If true, the response will include access analysis
                from identities to resources via service account
                impersonation. This is a very expensive operation, because
                many derived queries will be executed. We highly recommend
                you use ExportIamPolicyAnalysis rpc instead.

                For example, if the request analyzes for which resources
                user A has permission P, and there's an IAM policy states
                user A has iam.serviceAccounts.getAccessToken permission to
                a service account SA, and there's another IAM policy states
                service account SA has permission P to a GCP folder F, then
                user A potentially has access to the GCP folder F. And those
                advanced analysis results will be included in
                [AnalyzeIamPolicyResponse.service_account_impersonation_analysis][google.cloud.asset.v1p4beta1.AnalyzeIamPolicyResponse.service_account_impersonation_analysis].

                Another example, if the request analyzes for who has
                permission P to a GCP folder F, and there's an IAM policy
                states user A has iam.serviceAccounts.actAs permission to a
                service account SA, and there's another IAM policy states
                service account SA has permission P to the GCP folder F,
                then user A potentially has access to the GCP folder F. And
                those advanced analysis results will be included in
                [AnalyzeIamPolicyResponse.service_account_impersonation_analysis][google.cloud.asset.v1p4beta1.AnalyzeIamPolicyResponse.service_account_impersonation_analysis].

                Default is false.
            execution_timeout (google.protobuf.duration_pb2.Duration):
                Optional. Amount of time executable has to complete. See
                JSON representation of
                `Duration <https://developers.google.com/protocol-buffers/docs/proto3#json>`__.

                If this field is set with a value less than the RPC
                deadline, and the execution of your query hasn't finished in
                the specified execution timeout, you will get a response
                with partial result. Otherwise, your query's execution will
                continue until the RPC deadline. If it's not finished until
                then, you will get a DEADLINE_EXCEEDED error.

                Default is empty.
        """

        expand_groups = proto.Field(
            proto.BOOL,
            number=1,
        )
        expand_roles = proto.Field(
            proto.BOOL,
            number=2,
        )
        expand_resources = proto.Field(
            proto.BOOL,
            number=3,
        )
        output_resource_edges = proto.Field(
            proto.BOOL,
            number=4,
        )
        output_group_edges = proto.Field(
            proto.BOOL,
            number=5,
        )
        analyze_service_account_impersonation = proto.Field(
            proto.BOOL,
            number=6,
        )
        execution_timeout = proto.Field(
            proto.MESSAGE,
            number=7,
            message=duration_pb2.Duration,
        )

    analysis_query = proto.Field(
        proto.MESSAGE,
        number=1,
        message="IamPolicyAnalysisQuery",
    )
    options = proto.Field(
        proto.MESSAGE,
        number=2,
        message=Options,
    )


class AnalyzeIamPolicyResponse(proto.Message):
    r"""A response message for
    [AssetService.AnalyzeIamPolicy][google.cloud.asset.v1p4beta1.AssetService.AnalyzeIamPolicy].

    Attributes:
        main_analysis (google.cloud.asset_v1p4beta1.types.AnalyzeIamPolicyResponse.IamPolicyAnalysis):
            The main analysis that matches the original
            request.
        service_account_impersonation_analysis (Sequence[google.cloud.asset_v1p4beta1.types.AnalyzeIamPolicyResponse.IamPolicyAnalysis]):
            The service account impersonation analysis if
            [AnalyzeIamPolicyRequest.analyze_service_account_impersonation][]
            is enabled.
        fully_explored (bool):
            Represents whether all entries in the
            [main_analysis][google.cloud.asset.v1p4beta1.AnalyzeIamPolicyResponse.main_analysis]
            and
            [service_account_impersonation_analysis][google.cloud.asset.v1p4beta1.AnalyzeIamPolicyResponse.service_account_impersonation_analysis]
            have been fully explored to answer the query in the request.
        non_critical_errors (Sequence[google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisResult.AnalysisState]):
            A list of non-critical errors happened during the request
            handling to explain why ``fully_explored`` is false, or
            empty if no error happened.
    """

    class IamPolicyAnalysis(proto.Message):
        r"""An analysis message to group the query and results.

        Attributes:
            analysis_query (google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisQuery):
                The analysis query.
            analysis_results (Sequence[google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisResult]):
                A list of
                [IamPolicyAnalysisResult][google.cloud.asset.v1p4beta1.IamPolicyAnalysisResult]
                that matches the analysis query, or empty if no result is
                found.
            fully_explored (bool):
                Represents whether all entries in the
                [analysis_results][google.cloud.asset.v1p4beta1.AnalyzeIamPolicyResponse.IamPolicyAnalysis.analysis_results]
                have been fully explored to answer the query.
        """

        analysis_query = proto.Field(
            proto.MESSAGE,
            number=1,
            message="IamPolicyAnalysisQuery",
        )
        analysis_results = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message=assets.IamPolicyAnalysisResult,
        )
        fully_explored = proto.Field(
            proto.BOOL,
            number=3,
        )

    main_analysis = proto.Field(
        proto.MESSAGE,
        number=1,
        message=IamPolicyAnalysis,
    )
    service_account_impersonation_analysis = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=IamPolicyAnalysis,
    )
    fully_explored = proto.Field(
        proto.BOOL,
        number=3,
    )
    non_critical_errors = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=assets.IamPolicyAnalysisResult.AnalysisState,
    )


class IamPolicyAnalysisOutputConfig(proto.Message):
    r"""Output configuration for export IAM policy analysis
    destination.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_destination (google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisOutputConfig.GcsDestination):
            Destination on Cloud Storage.

            This field is a member of `oneof`_ ``destination``.
    """

    class GcsDestination(proto.Message):
        r"""A Cloud Storage location.

        Attributes:
            uri (str):
                Required. The uri of the Cloud Storage object. It's the same
                uri that is used by gsutil. For example:
                "gs://bucket_name/object_name". See `Viewing and Editing
                Object
                Metadata <https://cloud.google.com/storage/docs/viewing-editing-metadata>`__
                for more information.
        """

        uri = proto.Field(
            proto.STRING,
            number=1,
        )

    gcs_destination = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="destination",
        message=GcsDestination,
    )


class ExportIamPolicyAnalysisRequest(proto.Message):
    r"""A request message for
    [AssetService.ExportIamPolicyAnalysis][google.cloud.asset.v1p4beta1.AssetService.ExportIamPolicyAnalysis].

    Attributes:
        analysis_query (google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisQuery):
            Required. The request query.
        options (google.cloud.asset_v1p4beta1.types.ExportIamPolicyAnalysisRequest.Options):
            Optional. The request options.
        output_config (google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisOutputConfig):
            Required. Output configuration indicating
            where the results will be output to.
    """

    class Options(proto.Message):
        r"""Contains request options.

        Attributes:
            expand_groups (bool):
                Optional. If true, the identities section of the result will
                expand any Google groups appearing in an IAM policy binding.

                If [identity_selector][] is specified, the identity in the
                result will be determined by the selector, and this flag
                will have no effect.

                Default is false.
            expand_roles (bool):
                Optional. If true, the access section of result will expand
                any roles appearing in IAM policy bindings to include their
                permissions.

                If [access_selector][] is specified, the access section of
                the result will be determined by the selector, and this flag
                will have no effect.

                Default is false.
            expand_resources (bool):
                Optional. If true, the resource section of the result will
                expand any resource attached to an IAM policy to include
                resources lower in the resource hierarchy.

                For example, if the request analyzes for which resources
                user A has permission P, and the results include an IAM
                policy with P on a GCP folder, the results will also include
                resources in that folder with permission P.

                If [resource_selector][] is specified, the resource section
                of the result will be determined by the selector, and this
                flag will have no effect. Default is false.
            output_resource_edges (bool):
                Optional. If true, the result will output
                resource edges, starting from the policy
                attached resource, to any expanded resources.
                Default is false.
            output_group_edges (bool):
                Optional. If true, the result will output
                group identity edges, starting from the
                binding's group members, to any expanded
                identities. Default is false.
            analyze_service_account_impersonation (bool):
                Optional. If true, the response will include access analysis
                from identities to resources via service account
                impersonation. This is a very expensive operation, because
                many derived queries will be executed.

                For example, if the request analyzes for which resources
                user A has permission P, and there's an IAM policy states
                user A has iam.serviceAccounts.getAccessToken permission to
                a service account SA, and there's another IAM policy states
                service account SA has permission P to a GCP folder F, then
                user A potentially has access to the GCP folder F. And those
                advanced analysis results will be included in
                [AnalyzeIamPolicyResponse.service_account_impersonation_analysis][google.cloud.asset.v1p4beta1.AnalyzeIamPolicyResponse.service_account_impersonation_analysis].

                Another example, if the request analyzes for who has
                permission P to a GCP folder F, and there's an IAM policy
                states user A has iam.serviceAccounts.actAs permission to a
                service account SA, and there's another IAM policy states
                service account SA has permission P to the GCP folder F,
                then user A potentially has access to the GCP folder F. And
                those advanced analysis results will be included in
                [AnalyzeIamPolicyResponse.service_account_impersonation_analysis][google.cloud.asset.v1p4beta1.AnalyzeIamPolicyResponse.service_account_impersonation_analysis].

                Default is false.
        """

        expand_groups = proto.Field(
            proto.BOOL,
            number=1,
        )
        expand_roles = proto.Field(
            proto.BOOL,
            number=2,
        )
        expand_resources = proto.Field(
            proto.BOOL,
            number=3,
        )
        output_resource_edges = proto.Field(
            proto.BOOL,
            number=4,
        )
        output_group_edges = proto.Field(
            proto.BOOL,
            number=5,
        )
        analyze_service_account_impersonation = proto.Field(
            proto.BOOL,
            number=6,
        )

    analysis_query = proto.Field(
        proto.MESSAGE,
        number=1,
        message="IamPolicyAnalysisQuery",
    )
    options = proto.Field(
        proto.MESSAGE,
        number=2,
        message=Options,
    )
    output_config = proto.Field(
        proto.MESSAGE,
        number=3,
        message="IamPolicyAnalysisOutputConfig",
    )


class ExportIamPolicyAnalysisResponse(proto.Message):
    r"""The export IAM policy analysis response. This message is returned by
    the [google.longrunning.Operations.GetOperation][] method in the
    returned [google.longrunning.Operation.response][] field.

    Attributes:
        output_config (google.cloud.asset_v1p4beta1.types.IamPolicyAnalysisOutputConfig):
            Output configuration indicating where the
            results were output to.
    """

    output_config = proto.Field(
        proto.MESSAGE,
        number=1,
        message="IamPolicyAnalysisOutputConfig",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
