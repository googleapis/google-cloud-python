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
scikit-learn's model_selection module:
https://scikit-learn.org/stable/modules/classes.html#module-sklearn.model_selection."""


from typing import cast, List, Union

from bigframes.ml import utils
import bigframes.pandas as bpd


def train_test_split(
    *arrays: Union[bpd.DataFrame, bpd.Series],
    test_size: Union[float, None] = None,
    train_size: Union[float, None] = None,
    random_state: Union[int, None] = None,
    stratify: Union[bpd.Series, None] = None,
) -> List[Union[bpd.DataFrame, bpd.Series]]:
    """Splits dataframes or series into random train and test subsets.

    Args:
        *arrays (bigframes.dataframe.DataFrame or bigframes.series.Series):
            A sequence of BigQuery DataFrames or Series that can be joined on
            their indexes.
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
        stratify: (bigframes.series.Series or None, default None):
            If not None, data is split in a stratified fashion, using this as the class labels. Each split has the same distribution of the class labels with the original dataset.
            Default to None.
            Note: By setting the stratify parameter, the memory consumption and generated SQL will be linear to the unique values in the Series. May return errors if the unique values size is too large.

    Returns:
        List[Union[bigframes.dataframe.DataFrame, bigframes.series.Series]]: A list of BigQuery DataFrames or Series.
    """

    # TODO(garrettwu): scikit-learn throws an error when the dataframes don't have the same
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

    def _stratify_split(df: bpd.DataFrame, stratify: bpd.Series) -> List[bpd.DataFrame]:
        """Split a single DF accoding to the stratify Series."""
        stratify = stratify.rename("bigframes_stratify_col")  # avoid name conflicts
        merged_df = df.join(stratify.to_frame(), how="outer")

        train_dfs, test_dfs = [], []
        uniq = stratify.value_counts().index
        for value in uniq:
            cur = merged_df[merged_df["bigframes_stratify_col"] == value]
            train, test = train_test_split(
                cur,
                test_size=test_size,
                train_size=train_size,
                random_state=random_state,
            )
            train_dfs.append(train)
            test_dfs.append(test)

        train_df = cast(
            bpd.DataFrame, bpd.concat(train_dfs).drop(columns="bigframes_stratify_col")
        )
        test_df = cast(
            bpd.DataFrame, bpd.concat(test_dfs).drop(columns="bigframes_stratify_col")
        )
        return [train_df, test_df]

    joined_df = dfs[0]
    for df in dfs[1:]:
        joined_df = joined_df.join(df, how="outer")
    if stratify is None:
        joined_df_train, joined_df_test = joined_df._split(
            fracs=(train_size, test_size), random_state=random_state
        )
    else:
        joined_df_train, joined_df_test = _stratify_split(joined_df, stratify)

    results = []
    for array in arrays:
        columns = array.name if isinstance(array, bpd.Series) else array.columns
        results.append(joined_df_train[columns])
        results.append(joined_df_test[columns])

    return results
