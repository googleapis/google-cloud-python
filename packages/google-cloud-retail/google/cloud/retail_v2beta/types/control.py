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

from google.cloud.retail_v2beta.types import common, search_service

__protobuf__ = proto.module(
    package="google.cloud.retail.v2beta",
    manifest={
        "Control",
    },
)


class Control(proto.Message):
    r"""Configures dynamic serving time metadata that is used to pre
    and post process search/recommendation model results.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        facet_spec (google.cloud.retail_v2beta.types.SearchRequest.FacetSpec):
            A facet specification to perform faceted
            search.

            This field is a member of `oneof`_ ``control``.
        rule (google.cloud.retail_v2beta.types.Rule):
            A rule control - a condition-action pair.
            Enacts a set action when the condition is
            triggered. For example: Boost "gShoe" when query
            full matches "Running Shoes".

            This field is a member of `oneof`_ ``control``.
        name (str):
            Immutable. Fully qualified name
            ``projects/*/locations/global/catalogs/*/controls/*``
        display_name (str):
            Required. The human readable control display name. Used in
            Retail UI.

            This field must be a UTF-8 encoded string with a length
            limit of 128 characters. Otherwise, an INVALID_ARGUMENT
            error is thrown.
        associated_serving_config_ids (Sequence[str]):
            Output only. List of serving configuration
            ids that that are associated with this control.
            Note the association is managed via the
            ServingConfig, this is an output only
            denormalizeed  view. Assumed to be in the same
            catalog.
        solution_types (Sequence[google.cloud.retail_v2beta.types.SolutionType]):
            Required. Immutable. The solution types that the serving
            config is used for. Currently we support setting only one
            type of solution at creation time.

            Only ``SOLUTION_TYPE_SEARCH`` value is supported at the
            moment. If no solution type is provided at creation time,
            will default to SOLUTION_TYPE_SEARCH.
    """

    facet_spec = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="control",
        message=search_service.SearchRequest.FacetSpec,
    )
    rule = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="control",
        message=common.Rule,
    )
    name = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name = proto.Field(
        proto.STRING,
        number=2,
    )
    associated_serving_config_ids = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    solution_types = proto.RepeatedField(
        proto.ENUM,
        number=6,
        enum=common.SolutionType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
