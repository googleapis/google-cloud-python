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

from google.cloud.retail_v2.types import common
from google.cloud.retail_v2.types import product as gcr_product
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.retail.v2",
    manifest={"UserEvent", "ProductDetail", "PurchaseTransaction",},
)


class UserEvent(proto.Message):
    r"""UserEvent captures all metadata information Retail API needs
    to know about how end users interact with customers' website.

    Attributes:
        event_type (str):
            Required. User event type. Allowed values are:

            -  ``add-to-cart``: Products being added to cart.
            -  ``category-page-view``: Special pages such as sale or
               promotion pages viewed.
            -  ``detail-page-view``: Products detail page viewed.
            -  ``home-page-view``: Homepage viewed.
            -  ``purchase-complete``: User finishing a purchase.
            -  ``search``: Product search.
            -  ``shopping-cart-page-view``: User viewing a shopping
               cart.
        visitor_id (str):
            Required. A unique identifier for tracking visitors.

            For example, this could be implemented with an HTTP cookie,
            which should be able to uniquely identify a visitor on a
            single device. This unique identifier should not change if
            the visitor log in/out of the website.

            The field must be a UTF-8 encoded string with a length limit
            of 128 characters. Otherwise, an INVALID_ARGUMENT error is
            returned.
        event_time (google.protobuf.timestamp_pb2.Timestamp):
            Only required for
            [UserEventService.ImportUserEvents][google.cloud.retail.v2.UserEventService.ImportUserEvents]
            method. Timestamp of when the user event happened.
        experiment_ids (Sequence[str]):
            A list of identifiers for the independent
            experiment groups this user event belongs to.
            This is used to distinguish between user events
            associated with different experiment setups
            (e.g. using Retail API, using different
            recommendation models).
        attribution_token (str):
            Highly recommended for user events that are the result of
            [PredictionService.Predict][google.cloud.retail.v2.PredictionService.Predict].
            This field enables accurate attribution of recommendation
            model performance.

            The value must be a valid
            [PredictResponse.attribution_token][google.cloud.retail.v2.PredictResponse.attribution_token]
            for user events that are the result of
            [PredictionService.Predict][google.cloud.retail.v2.PredictionService.Predict].

            This token enables us to accurately attribute page view or
            purchase back to the event and the particular predict
            response containing this clicked/purchased product. If user
            clicks on product K in the recommendation results, pass
            [PredictResponse.attribution_token][google.cloud.retail.v2.PredictResponse.attribution_token]
            as a URL parameter to product K's page. When recording
            events on product K's page, log the
            [PredictResponse.attribution_token][google.cloud.retail.v2.PredictResponse.attribution_token]
            to this field.
        product_details (Sequence[google.cloud.retail_v2.types.ProductDetail]):
            The main product details related to the event.

            This field is required for the following event types:

            -  ``add-to-cart``
            -  ``detail-page-view``
            -  ``purchase-complete``

            In a ``search`` event, this field represents the products
            returned to the end user on the current page (the end user
            may have not finished broswing the whole page yet). When a
            new page is returned to the end user, after
            pagination/filtering/ordering even for the same query, a new
            ``search`` event with different
            [product_details][google.cloud.retail.v2.UserEvent.product_details]
            is desired. The end user may have not finished broswing the
            whole page yet.
        attributes (Sequence[google.cloud.retail_v2.types.UserEvent.AttributesEntry]):
            Extra user event features to include in the recommendation
            model.

            The key must be a UTF-8 encoded string with a length limit
            of 5,000 characters. Otherwise, an INVALID_ARGUMENT error is
            returned.

            For product recommendation, an example of extra user
            information is traffic_channel, i.e. how user arrives at the
            site. Users can arrive at the site by coming to the site
            directly, or coming through Google search, and etc.
        cart_id (str):
            The id or name of the associated shopping cart. This id is
            used to associate multiple items added or present in the
            cart before purchase.

            This can only be set for ``add-to-cart``,
            ``purchase-complete``, or ``shopping-cart-page-view``
            events.
        purchase_transaction (google.cloud.retail_v2.types.PurchaseTransaction):
            A transaction represents the entire purchase transaction.

            Required for ``purchase-complete`` events. Other event types
            should not set this field. Otherwise, an INVALID_ARGUMENT
            error is returned.
        search_query (str):
            The user's search query.

            The value must be a UTF-8 encoded string with a length limit
            of 5,000 characters. Otherwise, an INVALID_ARGUMENT error is
            returned.

            Required for ``search`` events. Other event types should not
            set this field. Otherwise, an INVALID_ARGUMENT error is
            returned.
        page_categories (Sequence[str]):
            The categories associated with a category page.

            To represent full path of category, use '>' sign to separate
            different hierarchies. If '>' is part of the category name,
            please replace it with other character(s).

            Category pages include special pages such as sales or
            promotions. For instance, a special sale page may have the
            category hierarchy: "pageCategories" : ["Sales > 2017 Black
            Friday Deals"].

            Required for ``category-page-view`` events. Other event
            types should not set this field. Otherwise, an
            INVALID_ARGUMENT error is returned.
        user_info (google.cloud.retail_v2.types.UserInfo):
            User information.
        uri (str):
            Complete URL (window.location.href) of the
            user's current page.
            When using the client side event reporting with
            JavaScript pixel and Google Tag Manager, this
            value is filled in automatically. Maximum length
            5,000 characters.
        referrer_uri (str):
            The referrer URL of the current page.
            When using the client side event reporting with
            JavaScript pixel and Google Tag Manager, this
            value is filled in automatically.
        page_view_id (str):
            A unique id of a web page view.

            This should be kept the same for all user events triggered
            from the same pageview. For example, an item detail page
            view could trigger multiple events as the user is browsing
            the page. The ``pageViewId`` property should be kept the
            same for all these events so that they can be grouped
            together properly.

            When using the client side event reporting with JavaScript
            pixel and Google Tag Manager, this value is filled in
            automatically.
    """

    event_type = proto.Field(proto.STRING, number=1,)
    visitor_id = proto.Field(proto.STRING, number=2,)
    event_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    experiment_ids = proto.RepeatedField(proto.STRING, number=4,)
    attribution_token = proto.Field(proto.STRING, number=5,)
    product_details = proto.RepeatedField(
        proto.MESSAGE, number=6, message="ProductDetail",
    )
    attributes = proto.MapField(
        proto.STRING, proto.MESSAGE, number=7, message=common.CustomAttribute,
    )
    cart_id = proto.Field(proto.STRING, number=8,)
    purchase_transaction = proto.Field(
        proto.MESSAGE, number=9, message="PurchaseTransaction",
    )
    search_query = proto.Field(proto.STRING, number=10,)
    page_categories = proto.RepeatedField(proto.STRING, number=11,)
    user_info = proto.Field(proto.MESSAGE, number=12, message=common.UserInfo,)
    uri = proto.Field(proto.STRING, number=13,)
    referrer_uri = proto.Field(proto.STRING, number=14,)
    page_view_id = proto.Field(proto.STRING, number=15,)


class ProductDetail(proto.Message):
    r"""Detailed product information associated with a user event.
    Attributes:
        product (google.cloud.retail_v2.types.Product):
            Required. [Product][google.cloud.retail.v2.Product]
            information.

            Only [Product.id][google.cloud.retail.v2.Product.id] field
            is used when ingesting an event, all other product fields
            are ignored as we will look them up from the catalog.
        quantity (google.protobuf.wrappers_pb2.Int32Value):
            Quantity of the product associated with the user event.

            For example, this field will be 2 if two products are added
            to the shopping cart for ``purchase-complete`` event.
            Required for ``add-to-cart`` and ``purchase-complete`` event
            types.
    """

    product = proto.Field(proto.MESSAGE, number=1, message=gcr_product.Product,)
    quantity = proto.Field(proto.MESSAGE, number=2, message=wrappers_pb2.Int32Value,)


class PurchaseTransaction(proto.Message):
    r"""A transaction represents the entire purchase transaction.
    Attributes:
        id (str):
            The transaction ID with a length limit of 128
            characters.
        revenue (float):
            Required. Total non-zero revenue or grand
            total associated with the transaction. This
            value include shipping, tax, or other
            adjustments to total revenue that you want to
            include as part of your revenue calculations.
        tax (float):
            All the taxes associated with the
            transaction.
        cost (float):
            All the costs associated with the products. These can be
            manufacturing costs, shipping expenses not borne by the end
            user, or any other costs, such that:

            -  Profit =
               [revenue][google.cloud.retail.v2.PurchaseTransaction.revenue]
               - [tax][google.cloud.retail.v2.PurchaseTransaction.tax] -
               [cost][google.cloud.retail.v2.PurchaseTransaction.cost]
        currency_code (str):
            Required. Currency code. Use three-character
            ISO-4217 code.
    """

    id = proto.Field(proto.STRING, number=1,)
    revenue = proto.Field(proto.FLOAT, number=2,)
    tax = proto.Field(proto.FLOAT, number=3,)
    cost = proto.Field(proto.FLOAT, number=4,)
    currency_code = proto.Field(proto.STRING, number=5,)


__all__ = tuple(sorted(__protobuf__.manifest))
