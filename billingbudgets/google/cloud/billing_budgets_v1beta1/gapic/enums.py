# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrappers for protocol buffer enum types."""

import enum


class Filter(object):
    class CreditTypesTreatment(enum.IntEnum):
        """
        Specifies how credits should be treated when determining spend for
        threshold calculations.

        Attributes:
          CREDIT_TYPES_TREATMENT_UNSPECIFIED (int)
          INCLUDE_ALL_CREDITS (int): All types of credit are subtracted from the gross cost to determine the
          spend for threshold calculations.
          EXCLUDE_ALL_CREDITS (int): All types of credit are added to the net cost to determine the spend for
          threshold calculations.
        """

        CREDIT_TYPES_TREATMENT_UNSPECIFIED = 0
        INCLUDE_ALL_CREDITS = 1
        EXCLUDE_ALL_CREDITS = 2


class ThresholdRule(object):
    class Basis(enum.IntEnum):
        """
        The type of basis used to determine if spend has passed the threshold.

        Attributes:
          BASIS_UNSPECIFIED (int): Unspecified threshold basis.
          CURRENT_SPEND (int): Use current spend as the basis for comparison against the threshold.
          FORECASTED_SPEND (int): Use forecasted spend for the period as the basis for comparison against
          the threshold.
        """

        BASIS_UNSPECIFIED = 0
        CURRENT_SPEND = 1
        FORECASTED_SPEND = 2
