# Copyright 2024 Google LLC
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
from google.cloud.bigtable.data.execute_query.values import Struct
from google.cloud.bigtable_v2 import Type as PBType, Value as PBValue
from google.cloud.bigtable.data.execute_query._query_result_parsing_utils import (
    _parse_pb_value_to_python_value,
)
from google.cloud.bigtable.data.execute_query.metadata import (
    _pb_type_to_metadata_type,
    SqlType,
)

from google.type import date_pb2
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

import datetime

from tests.unit.data.execute_query.sql_helpers import int64_type

TYPE_BYTES = {"bytes_type": {}}
TYPE_TIMESTAMP = {"timestamp_type": {}}


class TestQueryResultParsingUtils:
    @pytest.mark.parametrize(
        "type_dict,value_dict,expected_metadata_type,expected_value",
        [
            (int64_type(), {"int_value": 1}, SqlType.Int64, 1),
            (
                {"string_type": {}},
                {"string_value": "test"},
                SqlType.String,
                "test",
            ),
            ({"bool_type": {}}, {"bool_value": False}, SqlType.Bool, False),
            (
                {"bytes_type": {}},
                {"bytes_value": b"test"},
                SqlType.Bytes,
                b"test",
            ),
            (
                {"float64_type": {}},
                {"float_value": 17.21},
                SqlType.Float64,
                17.21,
            ),
            (
                {"timestamp_type": {}},
                {"timestamp_value": {"seconds": 1715864647, "nanos": 12}},
                SqlType.Timestamp,
                DatetimeWithNanoseconds(
                    2024, 5, 16, 13, 4, 7, nanosecond=12, tzinfo=datetime.timezone.utc
                ),
            ),
            (
                {"date_type": {}},
                {"date_value": {"year": 1800, "month": 12, "day": 0}},
                SqlType.Date,
                date_pb2.Date(year=1800, month=12, day=0),
            ),
        ],
    )
    def test_basic_types(
        self, type_dict, value_dict, expected_metadata_type, expected_value
    ):
        _type = PBType(type_dict)
        metadata_type = _pb_type_to_metadata_type(_type)
        assert type(metadata_type) is expected_metadata_type
        value = PBValue(value_dict)
        assert (
            _parse_pb_value_to_python_value(value._pb, metadata_type) == expected_value
        )

    # Larger test cases were extracted for readability
    def test__array(self):
        _type = PBType({"array_type": {"element_type": int64_type()}})
        metadata_type = _pb_type_to_metadata_type(_type)
        assert type(metadata_type) is SqlType.Array
        assert type(metadata_type.element_type) is SqlType.Int64
        value = PBValue(
            {
                "array_value": {
                    "values": [
                        {"int_value": 1},
                        {"int_value": 2},
                        {"int_value": 3},
                        {"int_value": 4},
                    ]
                }
            }
        )
        assert _parse_pb_value_to_python_value(value._pb, metadata_type) == [1, 2, 3, 4]

    def test__struct(self):
        _type = PBType(
            {
                "struct_type": {
                    "fields": [
                        {
                            "field_name": "field1",
                            "type_": int64_type(),
                        },
                        {
                            "field_name": None,
                            "type_": {"string_type": {}},
                        },
                        {
                            "field_name": "field3",
                            "type_": {"array_type": {"element_type": int64_type()}},
                        },
                        {
                            "field_name": "field3",
                            "type_": {"string_type": {}},
                        },
                    ]
                }
            }
        )
        value = PBValue(
            {
                "array_value": {
                    "values": [
                        {"int_value": 1},
                        {"string_value": "test2"},
                        {
                            "array_value": {
                                "values": [
                                    {"int_value": 2},
                                    {"int_value": 3},
                                    {"int_value": 4},
                                    {"int_value": 5},
                                ]
                            }
                        },
                        {"string_value": "test4"},
                    ]
                }
            }
        )

        metadata_type = _pb_type_to_metadata_type(_type)
        assert type(metadata_type) is SqlType.Struct
        assert type(metadata_type["field1"]) is SqlType.Int64
        assert type(metadata_type[1]) is SqlType.String
        assert type(metadata_type[2]) is SqlType.Array
        assert type(metadata_type[2].element_type) is SqlType.Int64
        assert type(metadata_type[3]) is SqlType.String

        # duplicate fields not accesible by name
        with pytest.raises(KeyError, match="Ambigious field name"):
            metadata_type["field3"]

        result = _parse_pb_value_to_python_value(value._pb, metadata_type)
        assert isinstance(result, Struct)
        assert result["field1"] == result[0] == 1
        assert result[1] == "test2"

        # duplicate fields not accesible by name
        with pytest.raises(KeyError, match="Ambigious field name"):
            result["field3"]

        # duplicate fields accessible by index
        assert result[2] == [2, 3, 4, 5]
        assert result[3] == "test4"

    def test__array_of_structs(self):
        _type = PBType(
            {
                "array_type": {
                    "element_type": {
                        "struct_type": {
                            "fields": [
                                {
                                    "field_name": "field1",
                                    "type_": int64_type(),
                                },
                                {
                                    "field_name": None,
                                    "type_": {"string_type": {}},
                                },
                                {
                                    "field_name": "field3",
                                    "type_": {"bool_type": {}},
                                },
                            ]
                        }
                    }
                }
            }
        )
        value = PBValue(
            {
                "array_value": {
                    "values": [
                        {
                            "array_value": {
                                "values": [
                                    {"int_value": 1},
                                    {"string_value": "test1"},
                                    {"bool_value": True},
                                ]
                            }
                        },
                        {
                            "array_value": {
                                "values": [
                                    {"int_value": 2},
                                    {"string_value": "test2"},
                                    {"bool_value": False},
                                ]
                            }
                        },
                        {
                            "array_value": {
                                "values": [
                                    {"int_value": 3},
                                    {"string_value": "test3"},
                                    {"bool_value": True},
                                ]
                            }
                        },
                        {
                            "array_value": {
                                "values": [
                                    {"int_value": 4},
                                    {"string_value": "test4"},
                                    {"bool_value": False},
                                ]
                            }
                        },
                    ]
                }
            }
        )

        metadata_type = _pb_type_to_metadata_type(_type)
        assert type(metadata_type) is SqlType.Array
        assert type(metadata_type.element_type) is SqlType.Struct
        assert type(metadata_type.element_type["field1"]) is SqlType.Int64
        assert type(metadata_type.element_type[1]) is SqlType.String
        assert type(metadata_type.element_type["field3"]) is SqlType.Bool

        result = _parse_pb_value_to_python_value(value._pb, metadata_type)
        assert isinstance(result, list)
        assert len(result) == 4

        assert isinstance(result[0], Struct)
        assert result[0]["field1"] == 1
        assert result[0][1] == "test1"
        assert result[0]["field3"]

        assert isinstance(result[1], Struct)
        assert result[1]["field1"] == 2
        assert result[1][1] == "test2"
        assert not result[1]["field3"]

        assert isinstance(result[2], Struct)
        assert result[2]["field1"] == 3
        assert result[2][1] == "test3"
        assert result[2]["field3"]

        assert isinstance(result[3], Struct)
        assert result[3]["field1"] == 4
        assert result[3][1] == "test4"
        assert not result[3]["field3"]

    def test__map(self):
        _type = PBType(
            {
                "map_type": {
                    "key_type": int64_type(),
                    "value_type": {"string_type": {}},
                }
            }
        )
        value = PBValue(
            {
                "array_value": {
                    "values": [
                        {
                            "array_value": {
                                "values": [
                                    {"int_value": 1},
                                    {"string_value": "test1"},
                                ]
                            }
                        },
                        {
                            "array_value": {
                                "values": [
                                    {"int_value": 2},
                                    {"string_value": "test2"},
                                ]
                            }
                        },
                        {
                            "array_value": {
                                "values": [
                                    {"int_value": 3},
                                    {"string_value": "test3"},
                                ]
                            }
                        },
                        {
                            "array_value": {
                                "values": [
                                    {"int_value": 4},
                                    {"string_value": "test4"},
                                ]
                            }
                        },
                    ]
                }
            }
        )

        metadata_type = _pb_type_to_metadata_type(_type)
        assert type(metadata_type) is SqlType.Map
        assert type(metadata_type.key_type) is SqlType.Int64
        assert type(metadata_type.value_type) is SqlType.String

        result = _parse_pb_value_to_python_value(value._pb, metadata_type)
        assert isinstance(result, dict)
        assert len(result) == 4

        assert result == {
            1: "test1",
            2: "test2",
            3: "test3",
            4: "test4",
        }

    def test__map_repeated_values(self):
        _type = PBType(
            {
                "map_type": {
                    "key_type": int64_type(),
                    "value_type": {"string_type": {}},
                }
            },
        )
        value = PBValue(
            {
                "array_value": {
                    "values": [
                        {
                            "array_value": {
                                "values": [
                                    {"int_value": 1},
                                    {"string_value": "test1"},
                                ]
                            }
                        },
                        {
                            "array_value": {
                                "values": [
                                    {"int_value": 1},
                                    {"string_value": "test2"},
                                ]
                            }
                        },
                        {
                            "array_value": {
                                "values": [
                                    {"int_value": 1},
                                    {"string_value": "test3"},
                                ]
                            }
                        },
                    ]
                }
            }
        )

        metadata_type = _pb_type_to_metadata_type(_type)
        result = _parse_pb_value_to_python_value(value._pb, metadata_type)
        assert len(result) == 1

        assert result == {
            1: "test3",
        }

    def test__map_of_maps_of_structs(self):
        _type = PBType(
            {
                "map_type": {
                    "key_type": int64_type(),
                    "value_type": {
                        "map_type": {
                            "key_type": {"string_type": {}},
                            "value_type": {
                                "struct_type": {
                                    "fields": [
                                        {
                                            "field_name": "field1",
                                            "type_": int64_type(),
                                        },
                                        {
                                            "field_name": "field2",
                                            "type_": {"string_type": {}},
                                        },
                                    ]
                                }
                            },
                        }
                    },
                }
            }
        )
        value = PBValue(
            {
                "array_value": {
                    "values": [  # list of (int, map) tuples
                        {
                            "array_value": {
                                "values": [  # (int, map) tuple
                                    {"int_value": 1},
                                    {
                                        "array_value": {
                                            "values": [  # list of (str, struct) tuples
                                                {
                                                    "array_value": {
                                                        "values": [  # (str, struct) tuple
                                                            {"string_value": "1_1"},
                                                            {
                                                                "array_value": {
                                                                    "values": [
                                                                        {
                                                                            "int_value": 1
                                                                        },
                                                                        {
                                                                            "string_value": "test1"
                                                                        },
                                                                    ]
                                                                }
                                                            },
                                                        ]
                                                    }
                                                },
                                                {
                                                    "array_value": {
                                                        "values": [  # (str, struct) tuple
                                                            {"string_value": "1_2"},
                                                            {
                                                                "array_value": {
                                                                    "values": [
                                                                        {
                                                                            "int_value": 2
                                                                        },
                                                                        {
                                                                            "string_value": "test2"
                                                                        },
                                                                    ]
                                                                }
                                                            },
                                                        ]
                                                    }
                                                },
                                            ]
                                        }
                                    },
                                ]
                            }
                        },
                        {
                            "array_value": {
                                "values": [  # (int, map) tuple
                                    {"int_value": 2},
                                    {
                                        "array_value": {
                                            "values": [  # list of (str, struct) tuples
                                                {
                                                    "array_value": {
                                                        "values": [  # (str, struct) tuple
                                                            {"string_value": "2_1"},
                                                            {
                                                                "array_value": {
                                                                    "values": [
                                                                        {
                                                                            "int_value": 3
                                                                        },
                                                                        {
                                                                            "string_value": "test3"
                                                                        },
                                                                    ]
                                                                }
                                                            },
                                                        ]
                                                    }
                                                },
                                                {
                                                    "array_value": {
                                                        "values": [  # (str, struct) tuple
                                                            {"string_value": "2_2"},
                                                            {
                                                                "array_value": {
                                                                    "values": [
                                                                        {
                                                                            "int_value": 4
                                                                        },
                                                                        {
                                                                            "string_value": "test4"
                                                                        },
                                                                    ]
                                                                }
                                                            },
                                                        ]
                                                    }
                                                },
                                            ]
                                        }
                                    },
                                ]
                            }
                        },
                    ]
                }
            }
        )
        metadata_type = _pb_type_to_metadata_type(_type)
        assert type(metadata_type) is SqlType.Map
        assert type(metadata_type.key_type) is SqlType.Int64
        assert type(metadata_type.value_type) is SqlType.Map
        assert type(metadata_type.value_type.key_type) is SqlType.String
        assert type(metadata_type.value_type.value_type) is SqlType.Struct
        assert type(metadata_type.value_type.value_type["field1"]) is SqlType.Int64
        assert type(metadata_type.value_type.value_type["field2"]) is SqlType.String
        result = _parse_pb_value_to_python_value(value._pb, metadata_type)

        assert result[1]["1_1"]["field1"] == 1
        assert result[1]["1_1"]["field2"] == "test1"

        assert result[1]["1_2"]["field1"] == 2
        assert result[1]["1_2"]["field2"] == "test2"

        assert result[2]["2_1"]["field1"] == 3
        assert result[2]["2_1"]["field2"] == "test3"

        assert result[2]["2_2"]["field1"] == 4
        assert result[2]["2_2"]["field2"] == "test4"

    def test__map_of_lists_of_structs(self):
        _type = PBType(
            {
                "map_type": {
                    "key_type": TYPE_BYTES,
                    "value_type": {
                        "array_type": {
                            "element_type": {
                                "struct_type": {
                                    "fields": [
                                        {
                                            "field_name": "timestamp",
                                            "type_": TYPE_TIMESTAMP,
                                        },
                                        {
                                            "field_name": "value",
                                            "type_": TYPE_BYTES,
                                        },
                                    ]
                                }
                            },
                        }
                    },
                }
            }
        )
        value = PBValue(
            {
                "array_value": {
                    "values": [  # list of (byte, list) tuples
                        {
                            "array_value": {
                                "values": [  # (byte, list) tuple
                                    {"bytes_value": b"key1"},
                                    {
                                        "array_value": {
                                            "values": [  # list of structs
                                                {
                                                    "array_value": {
                                                        "values": [  # (timestamp, bytes) tuple
                                                            {
                                                                "timestamp_value": {
                                                                    "seconds": 1111111111
                                                                }
                                                            },
                                                            {
                                                                "bytes_value": b"key1-value1"
                                                            },
                                                        ]
                                                    }
                                                },
                                                {
                                                    "array_value": {
                                                        "values": [  # (timestamp, bytes) tuple
                                                            {
                                                                "timestamp_value": {
                                                                    "seconds": 2222222222
                                                                }
                                                            },
                                                            {
                                                                "bytes_value": b"key1-value2"
                                                            },
                                                        ]
                                                    }
                                                },
                                            ]
                                        }
                                    },
                                ]
                            }
                        },
                        {
                            "array_value": {
                                "values": [  # (byte, list) tuple
                                    {"bytes_value": b"key2"},
                                    {
                                        "array_value": {
                                            "values": [  # list of structs
                                                {
                                                    "array_value": {
                                                        "values": [  # (timestamp, bytes) tuple
                                                            {
                                                                "timestamp_value": {
                                                                    "seconds": 3333333333
                                                                }
                                                            },
                                                            {
                                                                "bytes_value": b"key2-value1"
                                                            },
                                                        ]
                                                    }
                                                },
                                                {
                                                    "array_value": {
                                                        "values": [  # (timestamp, bytes) tuple
                                                            {
                                                                "timestamp_value": {
                                                                    "seconds": 4444444444
                                                                }
                                                            },
                                                            {
                                                                "bytes_value": b"key2-value2"
                                                            },
                                                        ]
                                                    }
                                                },
                                            ]
                                        }
                                    },
                                ]
                            }
                        },
                    ]
                }
            }
        )
        metadata_type = _pb_type_to_metadata_type(_type)
        assert type(metadata_type) is SqlType.Map
        assert type(metadata_type.key_type) is SqlType.Bytes
        assert type(metadata_type.value_type) is SqlType.Array
        assert type(metadata_type.value_type.element_type) is SqlType.Struct
        assert (
            type(metadata_type.value_type.element_type["timestamp"])
            is SqlType.Timestamp
        )
        assert type(metadata_type.value_type.element_type["value"]) is SqlType.Bytes
        result = _parse_pb_value_to_python_value(value._pb, metadata_type)

        timestamp1 = DatetimeWithNanoseconds(
            2005, 3, 18, 1, 58, 31, tzinfo=datetime.timezone.utc
        )
        timestamp2 = DatetimeWithNanoseconds(
            2040, 6, 2, 3, 57, 2, tzinfo=datetime.timezone.utc
        )
        timestamp3 = DatetimeWithNanoseconds(
            2075, 8, 18, 5, 55, 33, tzinfo=datetime.timezone.utc
        )
        timestamp4 = DatetimeWithNanoseconds(
            2110, 11, 3, 7, 54, 4, tzinfo=datetime.timezone.utc
        )

        assert result[b"key1"][0]["timestamp"] == timestamp1
        assert result[b"key1"][0]["value"] == b"key1-value1"
        assert result[b"key1"][1]["timestamp"] == timestamp2
        assert result[b"key1"][1]["value"] == b"key1-value2"
        assert result[b"key2"][0]["timestamp"] == timestamp3
        assert result[b"key2"][0]["value"] == b"key2-value1"
        assert result[b"key2"][1]["timestamp"] == timestamp4
        assert result[b"key2"][1]["value"] == b"key2-value2"

    def test__invalid_type_throws_exception(self):
        _type = PBType({"string_type": {}})
        value = PBValue({"int_value": 1})
        metadata_type = _pb_type_to_metadata_type(_type)

        with pytest.raises(
            ValueError,
            match="string_value field for String type not found in a Value.",
        ):
            _parse_pb_value_to_python_value(value._pb, metadata_type)
