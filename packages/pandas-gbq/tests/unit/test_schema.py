import datetime

import pandas
import pytest

import pandas_gbq.schema


@pytest.mark.parametrize(
    "dataframe,expected_schema",
    [
        (
            pandas.DataFrame(data={"col1": [1, 2, 3]}),
            {"fields": [{"name": "col1", "type": "INTEGER"}]},
        ),
        (
            pandas.DataFrame(data={"col1": [True, False]}),
            {"fields": [{"name": "col1", "type": "BOOLEAN"}]},
        ),
        (
            pandas.DataFrame(data={"col1": [1.0, 3.14]}),
            {"fields": [{"name": "col1", "type": "FLOAT"}]},
        ),
        (
            pandas.DataFrame(data={"col1": [u"hello", u"world"]}),
            {"fields": [{"name": "col1", "type": "STRING"}]},
        ),
        (
            pandas.DataFrame(data={"col1": [datetime.datetime.now()]}),
            {"fields": [{"name": "col1", "type": "TIMESTAMP"}]},
        ),
        (
            pandas.DataFrame(
                data={
                    "col1": [datetime.datetime.now()],
                    "col2": [u"hello"],
                    "col3": [3.14],
                    "col4": [True],
                    "col5": [4],
                }
            ),
            {
                "fields": [
                    {"name": "col1", "type": "TIMESTAMP"},
                    {"name": "col2", "type": "STRING"},
                    {"name": "col3", "type": "FLOAT"},
                    {"name": "col4", "type": "BOOLEAN"},
                    {"name": "col5", "type": "INTEGER"},
                ]
            },
        ),
    ],
)
def test_generate_bq_schema(dataframe, expected_schema):
    schema = pandas_gbq.schema.generate_bq_schema(dataframe)
    assert schema == expected_schema
