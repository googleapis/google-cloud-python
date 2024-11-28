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

"""Build composite transformers on heterogeneous data. This module is styled
after scikit-Learn's compose module:
https://scikit-learn.org/stable/modules/classes.html#module-sklearn.compose."""

from __future__ import annotations

import re
import types
import typing
from typing import cast, Iterable, List, Optional, Set, Tuple, Union

from bigframes_vendored import constants
import bigframes_vendored.sklearn.compose._column_transformer
from google.cloud import bigquery

from bigframes.core import log_adapter
import bigframes.core.compile.googlesql as sql_utils
from bigframes.ml import base, core, globals, impute, preprocessing, utils
import bigframes.pandas as bpd

_BQML_TRANSFROM_TYPE_MAPPING = types.MappingProxyType(
    {
        "ML.STANDARD_SCALER": preprocessing.StandardScaler,
        "ML.ONE_HOT_ENCODER": preprocessing.OneHotEncoder,
        "ML.MAX_ABS_SCALER": preprocessing.MaxAbsScaler,
        "ML.MIN_MAX_SCALER": preprocessing.MinMaxScaler,
        "ML.BUCKETIZE": preprocessing.KBinsDiscretizer,
        "ML.QUANTILE_BUCKETIZE": preprocessing.KBinsDiscretizer,
        "ML.LABEL_ENCODER": preprocessing.LabelEncoder,
        "ML.POLYNOMIAL_EXPAND": preprocessing.PolynomialFeatures,
        "ML.IMPUTER": impute.SimpleImputer,
    }
)


class SQLScalarColumnTransformer:
    r"""
    Wrapper for plain SQL code contained in a ColumnTransformer.

    Create a single column transformer in plain sql.
    This transformer can only be used inside ColumnTransformer.

    When creating an instance '{0}' can be used as placeholder
    for the column to transform:

        SQLScalarColumnTransformer("{0}+1")

    The default target column gets the prefix 'transformed\_'
    but can also be changed when creating an instance:

        SQLScalarColumnTransformer("{0}+1", "inc_{0}")

    **Examples:**

        >>> from bigframes.ml.compose import ColumnTransformer, SQLScalarColumnTransformer
        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.progress_bar = None

        >>> df = bpd.DataFrame({'name': ["James", None, "Mary"], 'city': ["New York", "Boston", None]})
        >>> col_trans = ColumnTransformer([
        ...     ("strlen",
        ...      SQLScalarColumnTransformer("CASE WHEN {0} IS NULL THEN 15 ELSE LENGTH({0}) END"),
        ...      ['name', 'city']),
        ... ])
        >>> col_trans = col_trans.fit(df)
        >>> df_transformed = col_trans.transform(df)
        >>> df_transformed
           transformed_name  transformed_city
        0                 5                 8
        1                15                 6
        2                 4                15
        <BLANKLINE>
        [3 rows x 2 columns]

    SQLScalarColumnTransformer can be combined with other transformers, like StandardScaler:

        >>> col_trans = ColumnTransformer([
        ...     ("identity", SQLScalarColumnTransformer("{0}", target_column="{0}"), ["col1", "col5"]),
        ...     ("increment", SQLScalarColumnTransformer("{0}+1", target_column="inc_{0}"), "col2"),
        ...     ("stdscale", preprocessing.StandardScaler(), "col3"),
        ...     # ...
        ... ])

    """

    def __init__(self, sql: str, target_column: str = "transformed_{0}"):
        super().__init__()
        self._sql = sql
        # TODO: More robust unescaping
        self._target_column = target_column.replace("`", "")

    PLAIN_COLNAME_RX = re.compile("^[a-z][a-z0-9_]*$", re.IGNORECASE)

    def _compile_to_sql(
        self, X: bpd.DataFrame, columns: Optional[Iterable[str]] = None
    ) -> List[str]:
        if columns is None:
            columns = X.columns
        result = []
        for column in columns:
            current_sql = self._sql.format(sql_utils.identifier(column))
            current_target_column = sql_utils.identifier(
                self._target_column.format(column)
            )
            result.append(f"{current_sql} AS {current_target_column}")
        return result

    def __repr__(self):
        return f"SQLScalarColumnTransformer(sql='{self._sql}', target_column='{self._target_column}')"

    def __eq__(self, other) -> bool:
        return type(self) is type(other) and self._keys() == other._keys()

    def __hash__(self) -> int:
        return hash(self._keys())

    def _keys(self):
        return (self._sql, self._target_column)


# Type hints for transformers contained in ColumnTransformer
SingleColTransformer = Union[
    preprocessing.PreprocessingType,
    impute.SimpleImputer,
    SQLScalarColumnTransformer,
]


@log_adapter.class_logger
class ColumnTransformer(
    base.Transformer,
    bigframes_vendored.sklearn.compose._column_transformer.ColumnTransformer,
):
    __doc__ = (
        bigframes_vendored.sklearn.compose._column_transformer.ColumnTransformer.__doc__
    )

    def __init__(
        self,
        transformers: Iterable[
            Tuple[
                str,
                SingleColTransformer,
                Union[str, Iterable[str]],
            ]
        ],
    ):
        # TODO: if any(transformers) has fitted raise warning
        self.transformers = list(transformers)
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()
        # call self.transformers_ to check chained transformers
        self.transformers_

    def _keys(self):
        return (self.transformers, self._bqml_model)

    @property
    def transformers_(
        self,
    ) -> List[Tuple[str, SingleColTransformer, str,]]:
        """The collection of transformers as tuples of (name, transformer, column)."""
        result: List[
            Tuple[
                str,
                SingleColTransformer,
                str,
            ]
        ] = []

        for entry in self.transformers:
            name, transformer, column_or_columns = entry
            columns = (
                column_or_columns
                if isinstance(column_or_columns, List)
                else [column_or_columns]
            )

            for column in columns:
                result.append((name, transformer, column))

        return result

    AS_FLEXNAME_SUFFIX_RX = re.compile("^(.*)\\bAS\\s*`[^`]+`\\s*$", re.IGNORECASE)

    @classmethod
    def _extract_from_bq_model(
        cls,
        bq_model: bigquery.Model,
    ) -> ColumnTransformer:
        """Extract transformers as ColumnTransformer obj from a BQ Model. Keep the _bqml_model field as None."""
        assert "transformColumns" in bq_model._properties

        transformers_set: Set[
            Tuple[
                str,
                SingleColTransformer,
                Union[str, List[str]],
            ]
        ] = set()

        def camel_to_snake(name):
            name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
            return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

        output_names = []
        for transform_col in bq_model._properties["transformColumns"]:
            transform_col_dict = cast(dict, transform_col)
            # pass the columns that are not transformed
            if "transformSql" not in transform_col_dict:
                continue
            transform_sql: str = transform_col_dict["transformSql"]

            # workaround for bug in bq_model returning " AS `...`" suffix for flexible names
            flex_name_match = cls.AS_FLEXNAME_SUFFIX_RX.match(transform_sql)
            if flex_name_match:
                transform_sql = flex_name_match.group(1)

            output_names.append(transform_col_dict["name"])
            found_transformer = False
            for prefix in _BQML_TRANSFROM_TYPE_MAPPING:
                if transform_sql.startswith(prefix):
                    transformer_cls = _BQML_TRANSFROM_TYPE_MAPPING[prefix]
                    transformers_set.add(
                        (
                            camel_to_snake(transformer_cls.__name__),
                            # TODO: This is very fragile, use real SQL parser
                            *transformer_cls._parse_from_sql(transform_sql),  # type: ignore
                        )
                    )

                    found_transformer = True
                    break
            if not found_transformer:
                if transform_sql.startswith("ML."):
                    raise NotImplementedError(
                        f"Unsupported transformer type. {constants.FEEDBACK_LINK}"
                    )

                target_column = transform_col_dict["name"]
                sql_transformer = SQLScalarColumnTransformer(
                    transform_sql.strip(), target_column=target_column
                )
                input_column_name = f"?{target_column}"
                transformers_set.add(
                    (
                        camel_to_snake(sql_transformer.__class__.__name__),
                        sql_transformer,
                        input_column_name,
                    )
                )

        transformer = cls(transformers=list(transformers_set))
        transformer._output_names = output_names

        return transformer

    def _merge(
        self, bq_model: bigquery.Model
    ) -> Union[
        ColumnTransformer, Union[preprocessing.PreprocessingType, impute.SimpleImputer]
    ]:
        """Try to merge the column transformer to a simple transformer. Depends on all the columns in bq_model are transformed with the same transformer."""
        transformers = self.transformers

        assert len(transformers) > 0
        _, transformer_0, column_0 = transformers[0]
        if isinstance(transformer_0, SQLScalarColumnTransformer):
            return self  # SQLScalarColumnTransformer only work inside ColumnTransformer
        feature_columns_sorted = sorted(
            [
                cast(str, feature_column.name)
                for feature_column in bq_model.feature_columns
            ]
        )

        if (
            len(transformers) == 1
            and isinstance(transformer_0, preprocessing.PolynomialFeatures)
            and sorted(column_0) == feature_columns_sorted
        ):
            transformer_0._output_names = self._output_names
            return transformer_0

        if not isinstance(column_0, str):
            return self
        columns = [column_0]
        for _, transformer, column in transformers[1:]:
            if not isinstance(column, str):
                return self
            # all transformers are the same
            if transformer != transformer_0:
                return self
            columns.append(column)
        # all feature columns are transformed
        if sorted(columns) == feature_columns_sorted:
            transformer_0._output_names = self._output_names
            return transformer_0

        return self

    def _compile_to_sql(
        self,
        X: bpd.DataFrame,
    ) -> List[str]:
        """Compile this transformer to a list of SQL expressions that can be included in
        a BQML TRANSFORM clause

        Args:
            X: DataFrame to transform.

        Returns: a list of sql_expr."""
        result = []
        for _, transformer, target_columns in self.transformers:
            if isinstance(target_columns, str):
                target_columns = [target_columns]
            result += transformer._compile_to_sql(X, target_columns)
        return result

    def fit(
        self,
        X: utils.ArrayType,
        y=None,  # ignored
    ) -> ColumnTransformer:
        (X,) = utils.batch_convert_to_dataframe(X)

        transform_sqls = self._compile_to_sql(X)
        self._bqml_model = self._bqml_model_factory.create_model(
            X,
            options={"model_type": "transform_only"},
            transforms=transform_sqls,
        )

        self._extract_output_names()
        return self

    def transform(self, X: utils.ArrayType) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("Must be fitted before transform")

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        df = self._bqml_model.transform(X)
        return typing.cast(
            bpd.DataFrame,
            df[self._output_names],
        )
