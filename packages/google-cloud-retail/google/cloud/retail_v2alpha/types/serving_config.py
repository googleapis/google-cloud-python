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

from google.cloud.retail_v2alpha.types import common, search_service

__protobuf__ = proto.module(
    package="google.cloud.retail.v2alpha",
    manifest={
        "ServingConfig",
    },
)


class ServingConfig(proto.Message):
    r"""Configures metadata that is used to generate serving time results
    (e.g. search results or recommendation predictions). The
    ServingConfig is passed in the search and predict request and
    together with the Catalog.default_branch, generates results.

    Attributes:
        name (str):
            Immutable. Fully qualified name
            ``projects/*/locations/global/catalogs/*/servingConfig/*``
        display_name (str):
            Required. The human readable serving config display name.
            Used in Retail UI.

            This field must be a UTF-8 encoded string with a length
            limit of 128 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.
        model_id (str):
            The id of the model to use at serving time. Currently only
            RecommendationModels are supported:
            https://cloud.google.com/retail/recommendations-ai/docs/create-models
            Can be changed but only to a compatible model (e.g.
            others-you-may-like CTR to others-you-may-like CVR).

            Required when
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_RECOMMENDATION][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_RECOMMENDATION].
        price_reranking_level (str):
            How much price ranking we want in serving results. Price
            reranking causes product items with a similar recommendation
            probability to be ordered by price, with the highest-priced
            items first. This setting could result in a decrease in
            click-through and conversion rates. Allowed values are:

            -  'no-price-reranking'
            -  'low-price-raranking'
            -  'medium-price-reranking'
            -  'high-price-reranking'

            If not specified, we choose default based on model type.
            Default value: 'no-price-reranking'.

            Can only be set if
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_RECOMMENDATION][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_RECOMMENDATION].
        facet_control_ids (Sequence[str]):
            Facet specifications for faceted search. If empty, no facets
            are returned. The ids refer to the ids of
            [Control][google.cloud.retail.v2alpha.Control] resources
            with only the Facet control set. These controls are assumed
            to be in the same
            [Catalog][google.cloud.retail.v2alpha.Catalog] as the
            [ServingConfig][google.cloud.retail.v2alpha.ServingConfig].
            A maximum of 100 values are allowed. Otherwise, an
            INVALID_ARGUMENT error is returned.

            Can only be set if
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_SEARCH][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_SEARCH].
        dynamic_facet_spec (google.cloud.retail_v2alpha.types.SearchRequest.DynamicFacetSpec):
            The specification for dynamically generated facets. Notice
            that only textual facets can be dynamically generated.

            Can only be set if
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_SEARCH][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_SEARCH].
        boost_control_ids (Sequence[str]):
            Condition boost specifications. If a product matches
            multiple conditions in the specifications, boost scores from
            these specifications are all applied and combined in a
            non-linear way. Maximum number of specifications is 100.

            Notice that if both
            [ServingConfig.boost_control_ids][google.cloud.retail.v2alpha.ServingConfig.boost_control_ids]
            and
            [SearchRequest.boost_spec][google.cloud.retail.v2alpha.SearchRequest.boost_spec]
            are set, the boost conditions from both places are
            evaluated. If a search request matches multiple boost
            conditions, the final boost score is equal to the sum of the
            boost scores from all matched boost conditions.

            Can only be set if
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_SEARCH][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_SEARCH].
        filter_control_ids (Sequence[str]):
            Condition filter specifications. If a product matches
            multiple conditions in the specifications, filters from
            these specifications are all applied and combined via the
            AND operator. Maximum number of specifications is 100.

            Can only be set if
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_SEARCH][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_SEARCH].
        redirect_control_ids (Sequence[str]):
            Condition redirect specifications. Only the first triggered
            redirect action is applied, even if multiple apply. Maximum
            number of specifications is 1000.

            Can only be set if
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_SEARCH][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_SEARCH].
        twoway_synonyms_control_ids (Sequence[str]):
            Condition synonyms specifications. If multiple syonyms
            conditions match, all matching synonyms control in the list
            will execute. Order of controls in the list will not matter.
            Maximum number of specifications is 100.

            Can only be set if
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_SEARCH][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_SEARCH].
        oneway_synonyms_control_ids (Sequence[str]):
            Condition oneway synonyms specifications. If multiple oneway
            synonyms conditions match, all matching oneway synonyms
            controls in the list will execute. Order of controls in the
            list will not matter. Maximum number of specifications is
            100.

            Can only be set if
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_SEARCH][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_SEARCH].
        do_not_associate_control_ids (Sequence[str]):
            Condition do not associate specifications. If multiple do
            not associate conditions match, all matching do not
            associate controls in the list will execute.

            -  Order does not matter.
            -  Maximum number of specifications is 100.

            Can only be set if
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_SEARCH][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_SEARCH].
        replacement_control_ids (Sequence[str]):
            Condition replacement specifications.

            -  Applied according to the order in the list.
            -  A previously replaced term can not be re-replaced.
            -  Maximum number of specifications is 100.

            Can only be set if
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_SEARCH][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_SEARCH].
        ignore_control_ids (Sequence[str]):
            Condition ignore specifications. If multiple ignore
            conditions match, all matching ignore controls in the list
            will execute.

            -  Order does not matter.
            -  Maximum number of specifications is 100.

            Can only be set if
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_SEARCH][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_SEARCH].
        diversity_level (str):
            How much diversity to use in recommendation model results
            e.g. 'medium-diversity' or 'high-diversity'. Currently
            supported values:

            -  'no-diversity'
            -  'low-diversity'
            -  'medium-diversity'
            -  'high-diversity'
            -  'auto-diversity'

            If not specified, we choose default based on recommendation
            model type. Default value: 'no-diversity'.

            Can only be set if
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_RECOMMENDATION][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_RECOMMENDATION].
        enable_category_filter_level (str):
            Whether to add additional category filters on the
            'similar-items' model. If not specified, we enable it by
            default. Allowed values are:

            -  'no-category-match': No additional filtering of original
               results from the model and the customer's filters.
            -  'relaxed-category-match': Only keep results with
               categories that match at least one item categories in the
               PredictRequests's context item.

               -  If customer also sends filters in the PredictRequest,
                  then the results will satisfy both conditions (user
                  given and category match).

            Can only be set if
            [solution_types][google.cloud.retail.v2alpha.ServingConfig.solution_types]
            is
            [SOLUTION_TYPE_RECOMMENDATION][google.cloud.retail.v2main.SolutionType.SOLUTION_TYPE_RECOMMENDATION].
        solution_types (Sequence[google.cloud.retail_v2alpha.types.SolutionType]):
            Required. Immutable. Specifies the solution
            types that a serving config can be associated
            with. Currently we support setting only one type
            of solution.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name = proto.Field(
        proto.STRING,
        number=2,
    )
    model_id = proto.Field(
        proto.STRING,
        number=3,
    )
    price_reranking_level = proto.Field(
        proto.STRING,
        number=4,
    )
    facet_control_ids = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    dynamic_facet_spec = proto.Field(
        proto.MESSAGE,
        number=6,
        message=search_service.SearchRequest.DynamicFacetSpec,
    )
    boost_control_ids = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    filter_control_ids = proto.RepeatedField(
        proto.STRING,
        number=9,
    )
    redirect_control_ids = proto.RepeatedField(
        proto.STRING,
        number=10,
    )
    twoway_synonyms_control_ids = proto.RepeatedField(
        proto.STRING,
        number=18,
    )
    oneway_synonyms_control_ids = proto.RepeatedField(
        proto.STRING,
        number=12,
    )
    do_not_associate_control_ids = proto.RepeatedField(
        proto.STRING,
        number=13,
    )
    replacement_control_ids = proto.RepeatedField(
        proto.STRING,
        number=14,
    )
    ignore_control_ids = proto.RepeatedField(
        proto.STRING,
        number=15,
    )
    diversity_level = proto.Field(
        proto.STRING,
        number=8,
    )
    enable_category_filter_level = proto.Field(
        proto.STRING,
        number=16,
    )
    solution_types = proto.RepeatedField(
        proto.ENUM,
        number=19,
        enum=common.SolutionType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
