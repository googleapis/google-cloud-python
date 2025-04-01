# Copyright 2023 Google LLC
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


import pytest

from bigframes.ml import decomposition


def test_decomposition_mf_model():
    model = decomposition.MatrixFactorization(
        num_factors=16,
        feedback_type="implicit",
        user_col="user_id",
        item_col="item_col",
        rating_col="rating_col",
        l2_reg=9,
    )
    assert model.num_factors == 16
    assert model.feedback_type == "implicit"
    assert model.user_col == "user_id"
    assert model.item_col == "item_col"
    assert model.rating_col == "rating_col"


def test_decomposition_mf_feedback_type_explicit():
    model = decomposition.MatrixFactorization(
        num_factors=16,
        feedback_type="explicit",
        user_col="user_id",
        item_col="item_col",
        rating_col="rating_col",
        l2_reg=9.83,
    )
    assert model.feedback_type == "explicit"


def test_decomposition_mf_invalid_feedback_type_raises():
    feedback_type = "explimp"
    with pytest.raises(
        ValueError,
        match="Expected feedback_type to be `explicit` or `implicit`.",
    ):
        decomposition.MatrixFactorization(
            # Intentionally pass in the wrong type. This will fail if the user is using
            # a type checker, but we can't assume that everyone is doing so, especially
            # not in notebook environments.
            num_factors=16,
            feedback_type=feedback_type,  # type: ignore
            user_col="user_id",
            item_col="item_col",
            rating_col="rating_col",
            l2_reg=9.83,
        )


def test_decomposition_mf_num_factors_low():
    model = decomposition.MatrixFactorization(
        num_factors=0,
        feedback_type="explicit",
        user_col="user_id",
        item_col="item_col",
        rating_col="rating_col",
        l2_reg=9.83,
    )
    assert model.num_factors == 0


def test_decomposition_mf_negative_num_factors_raises():
    num_factors = -2
    with pytest.raises(
        ValueError,
        match=f"Expected num_factors to be a positive integer, but got {num_factors}.",
    ):
        decomposition.MatrixFactorization(
            num_factors=num_factors,  # type: ignore
            feedback_type="explicit",
            user_col="user_id",
            item_col="item_col",
            rating_col="rating_col",
            l2_reg=9.83,
        )


def test_decomposition_mf_invalid_num_factors_raises():
    num_factors = 0.5
    with pytest.raises(
        TypeError,
        match=f"Expected num_factors to be an int, but got {type(num_factors)}.",
    ):
        decomposition.MatrixFactorization(
            num_factors=num_factors,  # type: ignore
            feedback_type="explicit",
            user_col="user_id",
            item_col="item_col",
            rating_col="rating_col",
            l2_reg=9.83,
        )


def test_decomposition_mf_invalid_user_col_raises():
    user_col = 123
    with pytest.raises(
        TypeError, match=f"Expected user_col to be a str, but got {type(user_col)}."
    ):
        decomposition.MatrixFactorization(
            num_factors=16,
            feedback_type="explicit",
            user_col=user_col,  # type: ignore
            item_col="item_col",
            rating_col="rating_col",
            l2_reg=9.83,
        )


def test_decomposition_mf_invalid_item_col_raises():
    item_col = 123
    with pytest.raises(
        TypeError, match=f"Expected item_col to be STR, but got {type(item_col)}."
    ):
        decomposition.MatrixFactorization(
            num_factors=16,
            feedback_type="explicit",
            user_col="user_id",
            item_col=item_col,  # type: ignore
            rating_col="rating_col",
            l2_reg=9.83,
        )


def test_decomposition_mf_invalid_rating_col_raises():
    rating_col = 4
    with pytest.raises(
        TypeError, match=f"Expected rating_col to be a str, but got {type(rating_col)}."
    ):
        decomposition.MatrixFactorization(
            num_factors=16,
            feedback_type="explicit",
            user_col="user_id",
            item_col="item_col",
            rating_col=rating_col,  # type: ignore
            l2_reg=9.83,
        )


def test_decomposition_mf_l2_reg():
    model = decomposition.MatrixFactorization(
        num_factors=16,
        feedback_type="explicit",
        user_col="user_id",
        item_col="item_col",
        rating_col="rating_col",
        l2_reg=6.02,  # type: ignore
    )
    assert model.l2_reg == 6.02


def test_decomposition_mf_invalid_l2_reg_raises():
    l2_reg = "6.02"
    with pytest.raises(
        TypeError,
        match=f"Expected l2_reg to be a float or int, but got {type(l2_reg)}.",
    ):
        decomposition.MatrixFactorization(
            num_factors=16,
            feedback_type="explicit",
            user_col="user_id",
            item_col="item_col",
            rating_col="rating_col",
            l2_reg=l2_reg,  # type: ignore
        )
