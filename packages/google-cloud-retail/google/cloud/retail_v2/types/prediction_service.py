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

from google.cloud.retail_v2.types import user_event as gcr_user_event
from google.protobuf import struct_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.retail.v2", manifest={"PredictRequest", "PredictResponse",},
)


class PredictRequest(proto.Message):
    r"""Request message for Predict method.
    Attributes:
        placement (str):
            Required. Full resource name of the format:
            {name=projects/*/locations/global/catalogs/default_catalog/placements/*}
            The id of the recommendation engine placement. This id is
            used to identify the set of models that will be used to make
            the prediction.

            We currently support three placements with the following IDs
            by default:

            -  ``shopping_cart``: Predicts products frequently bought
               together with one or more products in the same shopping
               session. Commonly displayed after ``add-to-cart`` events,
               on product detail pages, or on the shopping cart page.

            -  ``home_page``: Predicts the next product that a user will
               most likely engage with or purchase based on the shopping
               or viewing history of the specified ``userId`` or
               ``visitorId``. For example - Recommendations for you.

            -  ``product_detail``: Predicts the next product that a user
               will most likely engage with or purchase. The prediction
               is based on the shopping or viewing history of the
               specified ``userId`` or ``visitorId`` and its relevance
               to a specified ``CatalogItem``. Typically used on product
               detail pages. For example - More products like this.

            -  ``recently_viewed_default``: Returns up to 75 products
               recently viewed by the specified ``userId`` or
               ``visitorId``, most recent ones first. Returns nothing if
               neither of them has viewed any products yet. For example
               - Recently viewed.

            The full list of available placements can be seen at
            https://console.cloud.google.com/recommendation/catalogs/default_catalog/placements
        user_event (google.cloud.retail_v2.types.UserEvent):
            Required. Context about the user, what they
            are looking at and what action they took to
            trigger the predict request. Note that this user
            event detail won't be ingested to userEvent
            logs. Thus, a separate userEvent write request
            is required for event logging.
        page_size (int):
            Maximum number of results to return per page.
            Set this property to the number of prediction
            results needed. If zero, the service will choose
            a reasonable default. The maximum allowed value
            is 100. Values above 100 will be coerced to 100.
        page_token (str):
            The previous PredictResponse.next_page_token.
        filter (str):
            Filter for restricting prediction results with a length
            limit of 5,000 characters. Accepts values for tags and the
            ``filterOutOfStockItems`` flag.

            -  Tag expressions. Restricts predictions to products that
               match all of the specified tags. Boolean operators ``OR``
               and ``NOT`` are supported if the expression is enclosed
               in parentheses, and must be separated from the tag values
               by a space. ``-"tagA"`` is also supported and is
               equivalent to ``NOT "tagA"``. Tag values must be double
               quoted UTF-8 encoded strings with a size limit of 1,000
               characters.

            -  filterOutOfStockItems. Restricts predictions to products
               that do not have a stockState value of OUT_OF_STOCK.

            Examples:

            -  tag=("Red" OR "Blue") tag="New-Arrival" tag=(NOT
               "promotional")
            -  filterOutOfStockItems tag=(-"promotional")
            -  filterOutOfStockItems

            If your filter blocks all prediction results, nothing will
            be returned. If you want generic (unfiltered) popular
            products to be returned instead, set ``strictFiltering`` to
            false in ``PredictRequest.params``.
        validate_only (bool):
            Use validate only mode for this prediction
            query. If set to true, a dummy model will be
            used that returns arbitrary products. Note that
            the validate only mode should only be used for
            testing the API, or if the model is not ready.
        params (Sequence[google.cloud.retail_v2.types.PredictRequest.ParamsEntry]):
            Additional domain specific parameters for the predictions.

            Allowed values:

            -  ``returnProduct``: Boolean. If set to true, the
               associated product object will be returned in the
               ``results.metadata`` field in the prediction response.
            -  ``returnScore``: Boolean. If set to true, the prediction
               'score' corresponding to each returned product will be
               set in the ``results.metadata`` field in the prediction
               response. The given 'score' indicates the probability of
               an product being clicked/purchased given the user's
               context and history.
            -  ``strictFiltering``: Boolean. True by default. If set to
               false, the service will return generic (unfiltered)
               popular products instead of empty if your filter blocks
               all prediction results.
        labels (Sequence[google.cloud.retail_v2.types.PredictRequest.LabelsEntry]):
            The labels for the predict request.

            -  Label keys can contain lowercase letters, digits and
               hyphens, must start with a letter, and must end with a
               letter or digit.
            -  Non-zero label values can contain lowercase letters,
               digits and hyphens, must start with a letter, and must
               end with a letter or digit.
            -  No more than 64 labels can be associated with a given
               request.

            See https://goo.gl/xmQnxf for more information on and
            examples of labels.
    """

    placement = proto.Field(proto.STRING, number=1,)
    user_event = proto.Field(proto.MESSAGE, number=2, message=gcr_user_event.UserEvent,)
    page_size = proto.Field(proto.INT32, number=3,)
    page_token = proto.Field(proto.STRING, number=4,)
    filter = proto.Field(proto.STRING, number=5,)
    validate_only = proto.Field(proto.BOOL, number=6,)
    params = proto.MapField(
        proto.STRING, proto.MESSAGE, number=7, message=struct_pb2.Value,
    )
    labels = proto.MapField(proto.STRING, proto.STRING, number=8,)


class PredictResponse(proto.Message):
    r"""Response message for predict method.
    Attributes:
        results (Sequence[google.cloud.retail_v2.types.PredictResponse.PredictionResult]):
            A list of recommended products. The order
            represents the ranking (from the most relevant
            product to the least).
        attribution_token (str):
            A unique attribution token. This should be included in the
            [UserEvent][google.cloud.retail.v2.UserEvent] logs resulting
            from this recommendation, which enables accurate attribution
            of recommendation model performance.
        missing_ids (Sequence[str]):
            IDs of products in the request that were
            missing from the inventory.
        validate_only (bool):
            True if the validateOnly property was set in
            the request.
    """

    class PredictionResult(proto.Message):
        r"""PredictionResult represents the recommendation prediction
        results.

        Attributes:
            id (str):
                ID of the recommended product
            metadata (Sequence[google.cloud.retail_v2.types.PredictResponse.PredictionResult.MetadataEntry]):
                Additional product metadata / annotations.

                Possible values:

                -  ``product``: JSON representation of the product. Will be
                   set if ``returnProduct`` is set to true in
                   ``PredictRequest.params``.
                -  ``score``: Prediction score in double value. Will be set
                   if ``returnScore`` is set to true in
                   ``PredictRequest.params``.
        """

        id = proto.Field(proto.STRING, number=1,)
        metadata = proto.MapField(
            proto.STRING, proto.MESSAGE, number=2, message=struct_pb2.Value,
        )

    results = proto.RepeatedField(proto.MESSAGE, number=1, message=PredictionResult,)
    attribution_token = proto.Field(proto.STRING, number=2,)
    missing_ids = proto.RepeatedField(proto.STRING, number=3,)
    validate_only = proto.Field(proto.BOOL, number=4,)


__all__ = tuple(sorted(__protobuf__.manifest))
