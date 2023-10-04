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

"""Functions for test/train split and model tuning. This module is styled after
Scikit-Learn's model_selection module:
https://scikit-learn.org/stable/modules/classes.html#module-sklearn.model_selection."""


import typing
from typing import List, Union

from bigframes.ml import utils
import bigframes.pandas as bpd


def train_test_split(
    *arrays: Union[bpd.DataFrame, bpd.Series],
    test_size: Union[float, None] = None,
    train_size: Union[float, None] = None,
    random_state: Union[int, None] = None,
) -> List[Union[bpd.DataFrame, bpd.Series]]:
    """Splits dataframes or series into random train and test subsets.

    Args:
        *arrays (bigframes.dataframe.DataFrame or bigframes.series.Series):
            A sequence of BigQuery DataFrames or Series that can be joined on
            their indexes
        test_size (default None):
            The proportion of the dataset to include in the test split. If
            None, this will default to the complement of train_size. If both
            are none, it will be set to 0.25.
        train_size (default None):
            The proportion of the dataset to include in the train split. If
            None, this will default to the complement of test_size.
        random_state (default None):
            A seed to use for randomly choosing the rows of the split. If not
            set, a random split will be generated each time.

    Returns:
        List[Union[bigframes.dataframe.DataFrame, bigframes.series.Series]]: A list of BigQuery DataFrames or Series.
    """

    # TODO(garrettwu): Scikit-Learn throws an error when the dataframes don't have the same
    # number of rows. We probably want to do something similar. Now the implementation is based
    # on index. We'll move to based on ordering first.

    if test_size is None:
        if train_size is None:
            test_size = 0.25
        else:
            test_size = 1.0 - train_size
    if train_size is None:
        train_size = 1.0 - test_size

    if train_size <= 0.0 or train_size >= 1.0:
        raise ValueError(f"train_size must be within (0.0, 1.0). But is {train_size}.")

    if test_size <= 0.0 or test_size >= 1.0:
        raise ValueError(f"test_size must be within (0.0, 1.0). But is {test_size}.")

    if train_size + test_size > 1.0:
        raise ValueError(
            f"The sum of train_size and test_size exceeds 1.0. train_size: {train_size}. test_size: {test_size}"
        )

    dfs = list(utils.convert_to_dataframe(*arrays))

    split_dfs = dfs[0]._split(fracs=(train_size, test_size), random_state=random_state)
    train_index = split_dfs[0].index
    test_index = split_dfs[1].index

    split_dfs += typing.cast(
        List[bpd.DataFrame],
        [df.loc[index] for df in dfs[1:] for index in (train_index, test_index)],
    )

    # convert back to Series.
    results: List[Union[bpd.DataFrame, bpd.Series]] = []
    for i, array in enumerate(arrays):
        if isinstance(array, bpd.Series):
            results += utils.convert_to_series(split_dfs[2 * i], split_dfs[2 * i + 1])
        else:
            results += (split_dfs[2 * i], split_dfs[2 * i + 1])

    return results
