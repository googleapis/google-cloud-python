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


import inspect
import time
from typing import cast, Generator, List, Optional, Union

import bigframes_vendored.sklearn.model_selection._split as vendored_model_selection_split
import bigframes_vendored.sklearn.model_selection._validation as vendored_model_selection_validation
import pandas as pd

from bigframes.core import log_adapter
from bigframes.ml import utils
import bigframes.pandas as bpd


def train_test_split(
    *arrays: utils.ArrayType,
    test_size: Union[float, None] = None,
    train_size: Union[float, None] = None,
    random_state: Union[int, None] = None,
    stratify: Union[bpd.Series, None] = None,
) -> List[Union[bpd.DataFrame, bpd.Series]]:

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

    dfs = list(utils.batch_convert_to_dataframe(*arrays))

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


train_test_split.__doc__ = inspect.getdoc(
    vendored_model_selection_split.train_test_split
)


@log_adapter.class_logger
class KFold(vendored_model_selection_split.KFold):
    __doc__ = inspect.getdoc(vendored_model_selection_split.KFold)

    def __init__(self, n_splits: int = 5, *, random_state: Union[int, None] = None):
        if n_splits < 2:
            raise ValueError(f"n_splits must be at least 2. Got {n_splits}")
        self._n_splits = n_splits
        self._random_state = random_state

    def get_n_splits(self) -> int:
        return self._n_splits

    def split(
        self,
        X: utils.ArrayType,
        y: Union[utils.ArrayType, None] = None,
    ) -> Generator[tuple[Union[bpd.DataFrame, bpd.Series, None], ...], None, None]:
        X_df = next(utils.batch_convert_to_dataframe(X))
        y_df_or = next(utils.batch_convert_to_dataframe(y)) if y is not None else None
        joined_df = X_df.join(y_df_or, how="outer") if y_df_or is not None else X_df

        fracs = (1 / self._n_splits,) * self._n_splits

        dfs = joined_df._split(fracs=fracs, random_state=self._random_state)

        for i in range(len(dfs)):
            train_df = bpd.concat(dfs[:i] + dfs[i + 1 :])
            test_df = dfs[i]

            X_train = train_df[X_df.columns]
            y_train = train_df[y_df_or.columns] if y_df_or is not None else None

            X_test = test_df[X_df.columns]
            y_test = test_df[y_df_or.columns] if y_df_or is not None else None

            yield (
                KFold._convert_to_bf_type(X_train, X),
                KFold._convert_to_bf_type(X_test, X),
                KFold._convert_to_bf_type(y_train, y),
                KFold._convert_to_bf_type(y_test, y),
            )

    @staticmethod
    def _convert_to_bf_type(
        input,
        type_instance: Union[bpd.DataFrame, bpd.Series, pd.DataFrame, pd.Series, None],
    ) -> Union[bpd.DataFrame, bpd.Series, None]:
        if isinstance(type_instance, pd.Series) or isinstance(
            type_instance, bpd.Series
        ):
            return next(utils.batch_convert_to_series(input))

        if isinstance(type_instance, pd.DataFrame) or isinstance(
            type_instance, bpd.DataFrame
        ):
            return next(utils.batch_convert_to_dataframe(input))

        return None


def cross_validate(
    estimator,
    X: utils.ArrayType,
    y: Union[utils.ArrayType, None] = None,
    *,
    cv: Optional[Union[int, KFold]] = None,
) -> dict[str, list]:
    if cv is None:
        cv = KFold(n_splits=5)
    elif isinstance(cv, int):
        cv = KFold(n_splits=cv)

    result: dict[str, list] = {"test_score": [], "fit_time": [], "score_time": []}
    for X_train, X_test, y_train, y_test in cv.split(X, y):  # type: ignore
        fit_start_time = time.perf_counter()
        estimator.fit(X_train, y_train)
        fit_time = time.perf_counter() - fit_start_time

        score_start_time = time.perf_counter()
        score = estimator.score(X_test, y_test)
        score_time = time.perf_counter() - score_start_time

        result["test_score"].append(score)
        result["fit_time"].append(fit_time)
        result["score_time"].append(score_time)

    return result


cross_validate.__doc__ = inspect.getdoc(
    vendored_model_selection_validation.cross_validate
)
