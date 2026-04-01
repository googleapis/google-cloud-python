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
from unittest import mock

from google.cloud import bigquery
import pytest

from bigframes.ml import compose, preprocessing
from bigframes.ml.compose import ColumnTransformer, SQLScalarColumnTransformer
from bigframes.ml.core import BqmlModel
import bigframes.pandas as bpd


def test_columntransformer_init_expectedtransforms():
    onehot_transformer = preprocessing.OneHotEncoder()
    standard_scaler_transformer = preprocessing.StandardScaler()
    max_abs_scaler_transformer = preprocessing.MaxAbsScaler()
    min_max_scaler_transformer = preprocessing.MinMaxScaler()
    k_bins_discretizer_transformer = preprocessing.KBinsDiscretizer(strategy="uniform")
    label_transformer = preprocessing.LabelEncoder()
    column_transformer = compose.ColumnTransformer(
        [
            ("onehot", onehot_transformer, "species"),
            (
                "standard_scale",
                standard_scaler_transformer,
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "max_abs_scale",
                max_abs_scaler_transformer,
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "min_max_scale",
                min_max_scaler_transformer,
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "k_bins_discretizer",
                k_bins_discretizer_transformer,
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            ("label", label_transformer, "species"),
        ]
    )

    assert column_transformer.transformers_ == [
        ("onehot", onehot_transformer, "species"),
        ("standard_scale", standard_scaler_transformer, "culmen_length_mm"),
        ("standard_scale", standard_scaler_transformer, "flipper_length_mm"),
        ("max_abs_scale", max_abs_scaler_transformer, "culmen_length_mm"),
        ("max_abs_scale", max_abs_scaler_transformer, "flipper_length_mm"),
        ("min_max_scale", min_max_scaler_transformer, "culmen_length_mm"),
        ("min_max_scale", min_max_scaler_transformer, "flipper_length_mm"),
        ("k_bins_discretizer", k_bins_discretizer_transformer, "culmen_length_mm"),
        ("k_bins_discretizer", k_bins_discretizer_transformer, "flipper_length_mm"),
        ("label", label_transformer, "species"),
    ]


def test_columntransformer_repr():
    column_transformer = compose.ColumnTransformer(
        [
            (
                "onehot",
                preprocessing.OneHotEncoder(),
                "species",
            ),
            (
                "standard_scale",
                preprocessing.StandardScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "max_abs_scale",
                preprocessing.MaxAbsScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "min_max_scale",
                preprocessing.MinMaxScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "k_bins_discretizer",
                preprocessing.KBinsDiscretizer(strategy="uniform"),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
        ]
    )

    assert (
        column_transformer.__repr__()
        == """ColumnTransformer(transformers=[('onehot', OneHotEncoder(), 'species'),
                                ('standard_scale', StandardScaler(),
                                 ['culmen_length_mm', 'flipper_length_mm']),
                                ('max_abs_scale', MaxAbsScaler(),
                                 ['culmen_length_mm', 'flipper_length_mm']),
                                ('min_max_scale', MinMaxScaler(),
                                 ['culmen_length_mm', 'flipper_length_mm']),
                                ('k_bins_discretizer',
                                 KBinsDiscretizer(strategy='uniform'),
                                 ['culmen_length_mm', 'flipper_length_mm'])])"""
    )


def test_columntransformer_repr_matches_sklearn():
    sklearn_compose = pytest.importorskip("sklearn.compose")
    sklearn_preprocessing = pytest.importorskip("sklearn.preprocessing")
    bf_column_transformer = compose.ColumnTransformer(
        [
            (
                "onehot",
                preprocessing.OneHotEncoder(),
                "species",
            ),
            (
                "standard_scale",
                preprocessing.StandardScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "max_abs_scale",
                preprocessing.MaxAbsScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "min_max_scale",
                preprocessing.MinMaxScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "k_bins_discretizer",
                preprocessing.KBinsDiscretizer(strategy="uniform"),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
        ]
    )
    sk_column_transformer = sklearn_compose.ColumnTransformer(
        [
            (
                "onehot",
                sklearn_preprocessing.OneHotEncoder(),
                "species",
            ),
            (
                "standard_scale",
                sklearn_preprocessing.StandardScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "max_abs_scale",
                sklearn_preprocessing.MaxAbsScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "min_max_scale",
                sklearn_preprocessing.MinMaxScaler(),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            (
                "k_bins_discretizer",
                sklearn_preprocessing.KBinsDiscretizer(strategy="uniform"),
                ["culmen_length_mm", "flipper_length_mm"],
            ),
        ]
    )

    assert bf_column_transformer.__repr__() == sk_column_transformer.__repr__()


@pytest.fixture(scope="session")
def mock_X():
    mock_df = mock.create_autospec(spec=bpd.DataFrame)
    return mock_df


def test_columntransformer_init_with_sqltransformers():
    ident_transformer = SQLScalarColumnTransformer("{0}", target_column="ident_{0}")
    len1_transformer = SQLScalarColumnTransformer(
        "CASE WHEN {0} IS NULL THEN -2 ELSE LENGTH({0}) END", target_column="len1_{0}"
    )
    len2_transformer = SQLScalarColumnTransformer(
        "CASE WHEN {0} IS NULL THEN 99 ELSE LENGTH({0}) END", target_column="len2_{0}"
    )
    label_transformer = preprocessing.LabelEncoder()
    column_transformer = compose.ColumnTransformer(
        [
            (
                "ident_trafo",
                ident_transformer,
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            ("len1_trafo", len1_transformer, ["species"]),
            ("len2_trafo", len2_transformer, ["species"]),
            ("label", label_transformer, "species"),
        ]
    )

    assert column_transformer.transformers_ == [
        ("ident_trafo", ident_transformer, "culmen_length_mm"),
        ("ident_trafo", ident_transformer, "flipper_length_mm"),
        ("len1_trafo", len1_transformer, "species"),
        ("len2_trafo", len2_transformer, "species"),
        ("label", label_transformer, "species"),
    ]


def test_columntransformer_repr_sqltransformers():
    ident_transformer = SQLScalarColumnTransformer("{0}", target_column="ident_{0}")
    len1_transformer = SQLScalarColumnTransformer(
        "CASE WHEN {0} IS NULL THEN -2 ELSE LENGTH({0}) END", target_column="len1_{0}"
    )
    len2_transformer = SQLScalarColumnTransformer(
        "CASE WHEN {0} IS NULL THEN 99 ELSE LENGTH({0}) END", target_column="len2_{0}"
    )
    label_transformer = preprocessing.LabelEncoder()
    column_transformer = compose.ColumnTransformer(
        [
            (
                "ident_trafo",
                ident_transformer,
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            ("len1_trafo", len1_transformer, ["species"]),
            ("len2_trafo", len2_transformer, ["species"]),
            ("label", label_transformer, "species"),
        ]
    )

    expected = """ColumnTransformer(transformers=[('ident_trafo',
                                 SQLScalarColumnTransformer(sql='{0}', target_column='ident_{0}'),
                                 ['culmen_length_mm', 'flipper_length_mm']),
                                ('len1_trafo',
                                 SQLScalarColumnTransformer(sql='CASE WHEN {0} IS NULL THEN -2 ELSE LENGTH({0}) END', target_column='len1_{0}'),
                                 ['species']),
                                ('len2_trafo',
                                 SQLScalarColumnTransformer(sql='CASE WHEN {0} IS NULL THEN 99 ELSE LENGTH({0}) END', target_column='len2_{0}'),
                                 ['species']),
                                ('label', LabelEncoder(), 'species')])"""
    actual = column_transformer.__repr__()
    assert expected == actual


def test_customtransformer_compile_sql(mock_X):
    ident_trafo = SQLScalarColumnTransformer("{0}", target_column="ident_{0}")
    sqls = ident_trafo._compile_to_sql(X=mock_X, columns=["col1", "col2"])
    assert sqls == [
        "`col1` AS `ident_col1`",
        "`col2` AS `ident_col2`",
    ]

    len1_trafo = SQLScalarColumnTransformer(
        "CASE WHEN {0} IS NULL THEN -5 ELSE LENGTH({0}) END", target_column="len1_{0}"
    )
    sqls = len1_trafo._compile_to_sql(X=mock_X, columns=["col1", "col2"])
    assert sqls == [
        "CASE WHEN `col1` IS NULL THEN -5 ELSE LENGTH(`col1`) END AS `len1_col1`",
        "CASE WHEN `col2` IS NULL THEN -5 ELSE LENGTH(`col2`) END AS `len1_col2`",
    ]

    len2_trafo = SQLScalarColumnTransformer(
        "CASE WHEN {0} IS NULL THEN 99 ELSE LENGTH({0}) END", target_column="len2_{0}"
    )
    sqls = len2_trafo._compile_to_sql(X=mock_X, columns=["col1", "col2"])
    assert sqls == [
        "CASE WHEN `col1` IS NULL THEN 99 ELSE LENGTH(`col1`) END AS `len2_col1`",
        "CASE WHEN `col2` IS NULL THEN 99 ELSE LENGTH(`col2`) END AS `len2_col2`",
    ]


def create_bq_model_mock(monkeypatch, transform_columns, feature_columns=None):
    properties = {"transformColumns": transform_columns}
    mock_bq_model = bigquery.Model("model_project.model_dataset.model_id")
    type(mock_bq_model)._properties = mock.PropertyMock(return_value=properties)
    if feature_columns:
        result = [
            bigquery.standard_sql.StandardSqlField(col, None) for col in feature_columns
        ]
        monkeypatch.setattr(
            type(mock_bq_model),
            "feature_columns",
            mock.PropertyMock(return_value=result),
        )

    return mock_bq_model


@pytest.fixture
def bq_model_good(monkeypatch):
    return create_bq_model_mock(
        monkeypatch,
        [
            {
                "name": "ident_culmen_length_mm",
                "type": {"typeKind": "INT64"},
                "transformSql": "culmen_length_mm /*CT.IDENT()*/",
            },
            {
                "name": "ident_flipper_length_mm",
                "type": {"typeKind": "INT64"},
                "transformSql": "flipper_length_mm /*CT.IDENT()*/",
            },
            {
                "name": "len1_species",
                "type": {"typeKind": "INT64"},
                "transformSql": "CASE WHEN species IS NULL THEN -5 ELSE LENGTH(species) END /*CT.LEN1()*/",
            },
            {
                "name": "len2_species",
                "type": {"typeKind": "INT64"},
                "transformSql": "CASE WHEN species IS NULL THEN 99 ELSE LENGTH(species) END /*CT.LEN2([99])*/",
            },
            {
                "name": "labelencoded_county",
                "type": {"typeKind": "INT64"},
                "transformSql": "ML.LABEL_ENCODER(county, 1000000, 0) OVER()",
            },
            {
                "name": "labelencoded_species",
                "type": {"typeKind": "INT64"},
                "transformSql": "ML.LABEL_ENCODER(species, 1000000, 0) OVER()",
            },
        ],
    )


@pytest.fixture
def bq_model_merge(monkeypatch):
    return create_bq_model_mock(
        monkeypatch,
        [
            {
                "name": "labelencoded_county",
                "type": {"typeKind": "INT64"},
                "transformSql": "ML.LABEL_ENCODER(county, 1000000, 0) OVER()",
            },
            {
                "name": "labelencoded_species",
                "type": {"typeKind": "INT64"},
                "transformSql": "ML.LABEL_ENCODER(species, 1000000, 0) OVER()",
            },
        ],
        ["county", "species"],
    )


@pytest.fixture
def bq_model_no_merge(monkeypatch):
    return create_bq_model_mock(
        monkeypatch,
        [
            {
                "name": "ident_culmen_length_mm",
                "type": {"typeKind": "INT64"},
                "transformSql": "culmen_length_mm /*CT.IDENT()*/",
            }
        ],
        ["culmen_length_mm"],
    )


@pytest.fixture
def bq_model_unknown_ML(monkeypatch):
    return create_bq_model_mock(
        monkeypatch,
        [
            {
                "name": "unknownml_culmen_length_mm",
                "type": {"typeKind": "INT64"},
                "transformSql": "ML.UNKNOWN(culmen_length_mm)",
            },
            {
                "name": "labelencoded_county",
                "type": {"typeKind": "INT64"},
                "transformSql": "ML.LABEL_ENCODER(county, 1000000, 0) OVER()",
            },
        ],
    )


@pytest.fixture
def bq_model_flexnames(monkeypatch):
    return create_bq_model_mock(
        monkeypatch,
        [
            {
                "name": "Flex Name culmen_length_mm",
                "type": {"typeKind": "INT64"},
                "transformSql": "culmen_length_mm",
            },
            {
                "name": "transformed_Culmen Length MM",
                "type": {"typeKind": "INT64"},
                "transformSql": "`Culmen Length MM`*/",
            },
            # test workaround for bug in get_model
            {
                "name": "Flex Name flipper_length_mm",
                "type": {"typeKind": "INT64"},
                "transformSql": "flipper_length_mm AS `Flex Name flipper_length_mm`",
            },
            {
                "name": "transformed_Flipper Length MM",
                "type": {"typeKind": "INT64"},
                "transformSql": "`Flipper Length MM` AS `transformed_Flipper Length MM`*/",
            },
        ],
    )


def test_columntransformer_extract_from_bq_model_good(bq_model_good):
    col_trans = ColumnTransformer._extract_from_bq_model(bq_model_good)
    assert len(col_trans.transformers) == 6
    # normalize the representation for string comparing
    col_trans.transformers.sort(key=lambda trafo: str(trafo))
    actual = col_trans.__repr__()
    expected = """ColumnTransformer(transformers=[('label_encoder',
                                 LabelEncoder(max_categories=1000001,
                                              min_frequency=0),
                                 'county'),
                                ('label_encoder',
                                 LabelEncoder(max_categories=1000001,
                                              min_frequency=0),
                                 'species'),
                                ('sql_scalar_column_transformer',
                                 SQLScalarColumnTransformer(sql='CASE WHEN species IS NULL THEN -5 ELSE LENGTH(species) END /*CT.LEN1()*/', target_column='len1_species'),
                                 '?len1_species'),
                                ('sql_scalar_column_transformer',
                                 SQLScalarColumnTransformer(sql='CASE WHEN species IS NULL THEN 99 ELSE LENGTH(species) END /*CT.LEN2([99])*/', target_column='len2_species'),
                                 '?len2_species'),
                                ('sql_scalar_column_transformer',
                                 SQLScalarColumnTransformer(sql='culmen_length_mm /*CT.IDENT()*/', target_column='ident_culmen_length_mm'),
                                 '?ident_culmen_length_mm'),
                                ('sql_scalar_column_transformer',
                                 SQLScalarColumnTransformer(sql='flipper_length_mm /*CT.IDENT()*/', target_column='ident_flipper_length_mm'),
                                 '?ident_flipper_length_mm')])"""
    assert expected == actual


def test_columntransformer_extract_from_bq_model_merge(bq_model_merge):
    col_trans = ColumnTransformer._extract_from_bq_model(bq_model_merge)
    assert isinstance(col_trans, ColumnTransformer)
    merged_col_trans = col_trans._merge(bq_model_merge)
    assert isinstance(merged_col_trans, preprocessing.LabelEncoder)
    assert (
        merged_col_trans.__repr__()
        == """LabelEncoder(max_categories=1000001, min_frequency=0)"""
    )
    assert merged_col_trans._output_names == [
        "labelencoded_county",
        "labelencoded_species",
    ]


def test_columntransformer_extract_from_bq_model_no_merge(bq_model_no_merge):
    col_trans = ColumnTransformer._extract_from_bq_model(bq_model_no_merge)
    merged_col_trans = col_trans._merge(bq_model_no_merge)
    assert isinstance(merged_col_trans, ColumnTransformer)
    expected = """ColumnTransformer(transformers=[('sql_scalar_column_transformer',
                                 SQLScalarColumnTransformer(sql='culmen_length_mm /*CT.IDENT()*/', target_column='ident_culmen_length_mm'),
                                 '?ident_culmen_length_mm')])"""
    actual = merged_col_trans.__repr__()
    assert expected == actual


def test_columntransformer_extract_from_bq_model_unknown_ML(bq_model_unknown_ML):
    try:
        _ = ColumnTransformer._extract_from_bq_model(bq_model_unknown_ML)
        assert False
    except NotImplementedError as e:
        assert "Unsupported transformer type" in e.args[0]


def test_columntransformer_extract_output_names(bq_model_good):
    class BQMLModel(BqmlModel):
        def __init__(self, bq_model):
            self._model = bq_model

    col_trans = ColumnTransformer._extract_from_bq_model(bq_model_good)
    col_trans._bqml_model = BQMLModel(bq_model_good)
    col_trans._extract_output_names()
    assert col_trans._output_names == [
        "ident_culmen_length_mm",
        "ident_flipper_length_mm",
        "len1_species",
        "len2_species",
        "labelencoded_county",
        "labelencoded_species",
    ]


def test_columntransformer_compile_to_sql(mock_X):
    ident_transformer = SQLScalarColumnTransformer("{0}", target_column="ident_{0}")
    len1_transformer = SQLScalarColumnTransformer(
        "CASE WHEN {0} IS NULL THEN -2 ELSE LENGTH({0}) END", target_column="len1_{0}"
    )
    len2_transformer = SQLScalarColumnTransformer(
        "CASE WHEN {0} IS NULL THEN 99 ELSE LENGTH({0}) END", target_column="len2_{0}"
    )
    label_transformer = preprocessing.LabelEncoder()
    column_transformer = compose.ColumnTransformer(
        [
            (
                "ident_trafo",
                ident_transformer,
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            ("len1_trafo", len1_transformer, ["species"]),
            ("len2_trafo", len2_transformer, ["species"]),
            ("label", label_transformer, "species"),
        ]
    )
    sqls = column_transformer._compile_to_sql(mock_X)
    assert sqls == [
        "`culmen_length_mm` AS `ident_culmen_length_mm`",
        "`flipper_length_mm` AS `ident_flipper_length_mm`",
        "CASE WHEN `species` IS NULL THEN -2 ELSE LENGTH(`species`) END AS `len1_species`",
        "CASE WHEN `species` IS NULL THEN 99 ELSE LENGTH(`species`) END AS `len2_species`",
        "ML.LABEL_ENCODER(`species`, 1000000, 0) OVER() AS `labelencoded_species`",
    ]


def test_columntransformer_flexible_column_names(mock_X):
    ident_transformer = SQLScalarColumnTransformer("{0}", target_column="ident {0}")
    len1_transformer = SQLScalarColumnTransformer(
        "CASE WHEN {0} IS NULL THEN -2 ELSE LENGTH({0}) END", target_column="len1_{0}"
    )
    len2_transformer = SQLScalarColumnTransformer(
        "CASE WHEN {0} IS NULL THEN 99 ELSE LENGTH({0}) END", target_column="len2_{0}"
    )
    column_transformer = compose.ColumnTransformer(
        [
            (
                "ident_trafo",
                ident_transformer,
                ["culmen_length_mm", "flipper_length_mm"],
            ),
            ("len1_trafo", len1_transformer, ["species shortname"]),
            ("len2_trafo", len2_transformer, ["species longname"]),
        ]
    )
    sqls = column_transformer._compile_to_sql(mock_X)
    assert sqls == [
        "`culmen_length_mm` AS `ident culmen_length_mm`",
        "`flipper_length_mm` AS `ident flipper_length_mm`",
        "CASE WHEN `species shortname` IS NULL THEN -2 ELSE LENGTH(`species shortname`) END AS `len1_species shortname`",
        "CASE WHEN `species longname` IS NULL THEN 99 ELSE LENGTH(`species longname`) END AS `len2_species longname`",
    ]


def test_columntransformer_extract_from_bq_model_flexnames(bq_model_flexnames):
    col_trans = ColumnTransformer._extract_from_bq_model(bq_model_flexnames)
    assert len(col_trans.transformers) == 4
    # normalize the representation for string comparing
    col_trans.transformers.sort(key=lambda trafo: str(trafo))
    actual = col_trans.__repr__()
    expected = """ColumnTransformer(transformers=[('sql_scalar_column_transformer',
                                 SQLScalarColumnTransformer(sql='`Culmen Length MM`*/', target_column='transformed_Culmen Length MM'),
                                 '?transformed_Culmen Length MM'),
                                ('sql_scalar_column_transformer',
                                 SQLScalarColumnTransformer(sql='`Flipper Length MM` AS `transformed_Flipper Length MM`*/', target_column='transformed_Flipper Length MM'),
                                 '?transformed_Flipper Length MM'),
                                ('sql_scalar_column_transformer',
                                 SQLScalarColumnTransformer(sql='culmen_length_mm', target_column='Flex Name culmen_length_mm'),
                                 '?Flex Name culmen_length_mm'),
                                ('sql_scalar_column_transformer',
                                 SQLScalarColumnTransformer(sql='flipper_length_mm', target_column='Flex Name flipper_length_mm'),
                                 '?Flex Name flipper_length_mm')])"""
    assert expected == actual
