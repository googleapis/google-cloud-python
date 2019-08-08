# -*- coding: utf-8 -*-
# Copyright 2017 Google LLC All rights reserved.
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

import datetime
import sys
import unittest

import mock


class TestGeoPoint(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1._helpers import GeoPoint

        return GeoPoint

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        lat = 81.25
        lng = 359.984375
        geo_pt = self._make_one(lat, lng)
        self.assertEqual(geo_pt.latitude, lat)
        self.assertEqual(geo_pt.longitude, lng)

    def test_to_protobuf(self):
        from google.type import latlng_pb2

        lat = 0.015625
        lng = 20.03125
        geo_pt = self._make_one(lat, lng)
        result = geo_pt.to_protobuf()
        geo_pt_pb = latlng_pb2.LatLng(latitude=lat, longitude=lng)
        self.assertEqual(result, geo_pt_pb)

    def test___eq__(self):
        lat = 0.015625
        lng = 20.03125
        geo_pt1 = self._make_one(lat, lng)
        geo_pt2 = self._make_one(lat, lng)
        self.assertEqual(geo_pt1, geo_pt2)

    def test___eq__type_differ(self):
        lat = 0.015625
        lng = 20.03125
        geo_pt1 = self._make_one(lat, lng)
        geo_pt2 = object()
        self.assertNotEqual(geo_pt1, geo_pt2)
        self.assertIs(geo_pt1.__eq__(geo_pt2), NotImplemented)

    def test___ne__same_value(self):
        lat = 0.015625
        lng = 20.03125
        geo_pt1 = self._make_one(lat, lng)
        geo_pt2 = self._make_one(lat, lng)
        comparison_val = geo_pt1 != geo_pt2
        self.assertFalse(comparison_val)

    def test___ne__(self):
        geo_pt1 = self._make_one(0.0, 1.0)
        geo_pt2 = self._make_one(2.0, 3.0)
        self.assertNotEqual(geo_pt1, geo_pt2)

    def test___ne__type_differ(self):
        lat = 0.015625
        lng = 20.03125
        geo_pt1 = self._make_one(lat, lng)
        geo_pt2 = object()
        self.assertNotEqual(geo_pt1, geo_pt2)
        self.assertIs(geo_pt1.__ne__(geo_pt2), NotImplemented)


class Test_verify_path(unittest.TestCase):
    @staticmethod
    def _call_fut(path, is_collection):
        from google.cloud.firestore_v1._helpers import verify_path

        return verify_path(path, is_collection)

    def test_empty(self):
        path = ()
        with self.assertRaises(ValueError):
            self._call_fut(path, True)
        with self.assertRaises(ValueError):
            self._call_fut(path, False)

    def test_wrong_length_collection(self):
        path = ("foo", "bar")
        with self.assertRaises(ValueError):
            self._call_fut(path, True)

    def test_wrong_length_document(self):
        path = ("Kind",)
        with self.assertRaises(ValueError):
            self._call_fut(path, False)

    def test_wrong_type_collection(self):
        path = (99, "ninety-nine", "zap")
        with self.assertRaises(ValueError):
            self._call_fut(path, True)

    def test_wrong_type_document(self):
        path = ("Users", "Ada", "Candy", {})
        with self.assertRaises(ValueError):
            self._call_fut(path, False)

    def test_success_collection(self):
        path = ("Computer", "Magic", "Win")
        ret_val = self._call_fut(path, True)
        # NOTE: We are just checking that it didn't fail.
        self.assertIsNone(ret_val)

    def test_success_document(self):
        path = ("Tokenizer", "Seventeen", "Cheese", "Burger")
        ret_val = self._call_fut(path, False)
        # NOTE: We are just checking that it didn't fail.
        self.assertIsNone(ret_val)


class Test_encode_value(unittest.TestCase):
    @staticmethod
    def _call_fut(value):
        from google.cloud.firestore_v1._helpers import encode_value

        return encode_value(value)

    def test_none(self):
        from google.protobuf import struct_pb2

        result = self._call_fut(None)
        expected = _value_pb(null_value=struct_pb2.NULL_VALUE)
        self.assertEqual(result, expected)

    def test_boolean(self):
        result = self._call_fut(True)
        expected = _value_pb(boolean_value=True)
        self.assertEqual(result, expected)

    def test_integer(self):
        value = 425178
        result = self._call_fut(value)
        expected = _value_pb(integer_value=value)
        self.assertEqual(result, expected)

    def test_float(self):
        value = 123.4453125
        result = self._call_fut(value)
        expected = _value_pb(double_value=value)
        self.assertEqual(result, expected)

    def test_datetime_with_nanos(self):
        from google.api_core.datetime_helpers import DatetimeWithNanoseconds
        from google.protobuf import timestamp_pb2

        dt_seconds = 1488768504
        dt_nanos = 458816991
        timestamp_pb = timestamp_pb2.Timestamp(seconds=dt_seconds, nanos=dt_nanos)
        dt_val = DatetimeWithNanoseconds.from_timestamp_pb(timestamp_pb)

        result = self._call_fut(dt_val)
        expected = _value_pb(timestamp_value=timestamp_pb)
        self.assertEqual(result, expected)

    def test_datetime_wo_nanos(self):
        from google.protobuf import timestamp_pb2

        dt_seconds = 1488768504
        dt_nanos = 458816000
        # Make sure precision is valid in microseconds too.
        self.assertEqual(dt_nanos % 1000, 0)
        dt_val = datetime.datetime.utcfromtimestamp(dt_seconds + 1e-9 * dt_nanos)

        result = self._call_fut(dt_val)
        timestamp_pb = timestamp_pb2.Timestamp(seconds=dt_seconds, nanos=dt_nanos)
        expected = _value_pb(timestamp_value=timestamp_pb)
        self.assertEqual(result, expected)

    def test_string(self):
        value = u"\u2018left quote, right quote\u2019"
        result = self._call_fut(value)
        expected = _value_pb(string_value=value)
        self.assertEqual(result, expected)

    def test_bytes(self):
        value = b"\xe3\xf2\xff\x00"
        result = self._call_fut(value)
        expected = _value_pb(bytes_value=value)
        self.assertEqual(result, expected)

    def test_reference_value(self):
        client = _make_client()

        value = client.document("my", "friend")
        result = self._call_fut(value)
        expected = _value_pb(reference_value=value._document_path)
        self.assertEqual(result, expected)

    def test_geo_point(self):
        from google.cloud.firestore_v1._helpers import GeoPoint

        value = GeoPoint(50.5, 88.75)
        result = self._call_fut(value)
        expected = _value_pb(geo_point_value=value.to_protobuf())
        self.assertEqual(result, expected)

    def test_array(self):
        from google.cloud.firestore_v1.proto.document_pb2 import ArrayValue

        result = self._call_fut([99, True, 118.5])

        array_pb = ArrayValue(
            values=[
                _value_pb(integer_value=99),
                _value_pb(boolean_value=True),
                _value_pb(double_value=118.5),
            ]
        )
        expected = _value_pb(array_value=array_pb)
        self.assertEqual(result, expected)

    def test_map(self):
        from google.cloud.firestore_v1.proto.document_pb2 import MapValue

        result = self._call_fut({"abc": 285, "def": b"piglatin"})

        map_pb = MapValue(
            fields={
                "abc": _value_pb(integer_value=285),
                "def": _value_pb(bytes_value=b"piglatin"),
            }
        )
        expected = _value_pb(map_value=map_pb)
        self.assertEqual(result, expected)

    def test_bad_type(self):
        value = object()
        with self.assertRaises(TypeError):
            self._call_fut(value)


class Test_encode_dict(unittest.TestCase):
    @staticmethod
    def _call_fut(values_dict):
        from google.cloud.firestore_v1._helpers import encode_dict

        return encode_dict(values_dict)

    def test_many_types(self):
        from google.protobuf import struct_pb2
        from google.protobuf import timestamp_pb2
        from google.cloud.firestore_v1.proto.document_pb2 import ArrayValue
        from google.cloud.firestore_v1.proto.document_pb2 import MapValue

        dt_seconds = 1497397225
        dt_nanos = 465964000
        # Make sure precision is valid in microseconds too.
        self.assertEqual(dt_nanos % 1000, 0)
        dt_val = datetime.datetime.utcfromtimestamp(dt_seconds + 1e-9 * dt_nanos)

        client = _make_client()
        document = client.document("most", "adjective", "thing", "here")

        values_dict = {
            "foo": None,
            "bar": True,
            "baz": 981,
            "quux": 2.875,
            "quuz": dt_val,
            "corge": u"\N{snowman}",
            "grault": b"\xe2\x98\x83",
            "wibble": document,
            "garply": [u"fork", 4.0],
            "waldo": {"fred": u"zap", "thud": False},
        }
        encoded_dict = self._call_fut(values_dict)
        expected_dict = {
            "foo": _value_pb(null_value=struct_pb2.NULL_VALUE),
            "bar": _value_pb(boolean_value=True),
            "baz": _value_pb(integer_value=981),
            "quux": _value_pb(double_value=2.875),
            "quuz": _value_pb(
                timestamp_value=timestamp_pb2.Timestamp(
                    seconds=dt_seconds, nanos=dt_nanos
                )
            ),
            "corge": _value_pb(string_value=u"\N{snowman}"),
            "grault": _value_pb(bytes_value=b"\xe2\x98\x83"),
            "wibble": _value_pb(reference_value=document._document_path),
            "garply": _value_pb(
                array_value=ArrayValue(
                    values=[
                        _value_pb(string_value=u"fork"),
                        _value_pb(double_value=4.0),
                    ]
                )
            ),
            "waldo": _value_pb(
                map_value=MapValue(
                    fields={
                        "fred": _value_pb(string_value=u"zap"),
                        "thud": _value_pb(boolean_value=False),
                    }
                )
            ),
        }
        self.assertEqual(encoded_dict, expected_dict)


class Test_reference_value_to_document(unittest.TestCase):
    @staticmethod
    def _call_fut(reference_value, client):
        from google.cloud.firestore_v1._helpers import reference_value_to_document

        return reference_value_to_document(reference_value, client)

    def test_bad_format(self):
        from google.cloud.firestore_v1._helpers import BAD_REFERENCE_ERROR

        reference_value = "not/the/right/format"
        with self.assertRaises(ValueError) as exc_info:
            self._call_fut(reference_value, None)

        err_msg = BAD_REFERENCE_ERROR.format(reference_value)
        self.assertEqual(exc_info.exception.args, (err_msg,))

    def test_same_client(self):
        from google.cloud.firestore_v1.document import DocumentReference

        client = _make_client()
        document = client.document("that", "this")
        reference_value = document._document_path

        new_document = self._call_fut(reference_value, client)
        self.assertIsNot(new_document, document)

        self.assertIsInstance(new_document, DocumentReference)
        self.assertIs(new_document._client, client)
        self.assertEqual(new_document._path, document._path)

    def test_different_client(self):
        from google.cloud.firestore_v1._helpers import WRONG_APP_REFERENCE

        client1 = _make_client(project="kirk")
        document = client1.document("tin", "foil")
        reference_value = document._document_path

        client2 = _make_client(project="spock")
        with self.assertRaises(ValueError) as exc_info:
            self._call_fut(reference_value, client2)

        err_msg = WRONG_APP_REFERENCE.format(reference_value, client2._database_string)
        self.assertEqual(exc_info.exception.args, (err_msg,))


class Test_decode_value(unittest.TestCase):
    @staticmethod
    def _call_fut(value, client=mock.sentinel.client):
        from google.cloud.firestore_v1._helpers import decode_value

        return decode_value(value, client)

    def test_none(self):
        from google.protobuf import struct_pb2

        value = _value_pb(null_value=struct_pb2.NULL_VALUE)
        self.assertIsNone(self._call_fut(value))

    def test_bool(self):
        value1 = _value_pb(boolean_value=True)
        self.assertTrue(self._call_fut(value1))
        value2 = _value_pb(boolean_value=False)
        self.assertFalse(self._call_fut(value2))

    def test_int(self):
        int_val = 29871
        value = _value_pb(integer_value=int_val)
        self.assertEqual(self._call_fut(value), int_val)

    def test_float(self):
        float_val = 85.9296875
        value = _value_pb(double_value=float_val)
        self.assertEqual(self._call_fut(value), float_val)

    @unittest.skipIf(
        (3,) <= sys.version_info < (3, 4, 4), "known datetime bug (bpo-23517) in Python"
    )
    def test_datetime(self):
        from google.api_core.datetime_helpers import DatetimeWithNanoseconds
        from google.protobuf import timestamp_pb2

        dt_seconds = 552855006
        dt_nanos = 766961828

        timestamp_pb = timestamp_pb2.Timestamp(seconds=dt_seconds, nanos=dt_nanos)
        value = _value_pb(timestamp_value=timestamp_pb)

        expected_dt_val = DatetimeWithNanoseconds.from_timestamp_pb(timestamp_pb)
        self.assertEqual(self._call_fut(value), expected_dt_val)

    def test_unicode(self):
        unicode_val = u"zorgon"
        value = _value_pb(string_value=unicode_val)
        self.assertEqual(self._call_fut(value), unicode_val)

    def test_bytes(self):
        bytes_val = b"abc\x80"
        value = _value_pb(bytes_value=bytes_val)
        self.assertEqual(self._call_fut(value), bytes_val)

    def test_reference(self):
        from google.cloud.firestore_v1.document import DocumentReference

        client = _make_client()
        path = (u"then", u"there-was-one")
        document = client.document(*path)
        ref_string = document._document_path
        value = _value_pb(reference_value=ref_string)

        result = self._call_fut(value, client)
        self.assertIsInstance(result, DocumentReference)
        self.assertIs(result._client, client)
        self.assertEqual(result._path, path)

    def test_geo_point(self):
        from google.cloud.firestore_v1._helpers import GeoPoint

        geo_pt = GeoPoint(latitude=42.5, longitude=99.0625)
        value = _value_pb(geo_point_value=geo_pt.to_protobuf())
        self.assertEqual(self._call_fut(value), geo_pt)

    def test_array(self):
        from google.cloud.firestore_v1.proto import document_pb2

        sub_value1 = _value_pb(boolean_value=True)
        sub_value2 = _value_pb(double_value=14.1396484375)
        sub_value3 = _value_pb(bytes_value=b"\xde\xad\xbe\xef")
        array_pb = document_pb2.ArrayValue(values=[sub_value1, sub_value2, sub_value3])
        value = _value_pb(array_value=array_pb)

        expected = [
            sub_value1.boolean_value,
            sub_value2.double_value,
            sub_value3.bytes_value,
        ]
        self.assertEqual(self._call_fut(value), expected)

    def test_map(self):
        from google.cloud.firestore_v1.proto import document_pb2

        sub_value1 = _value_pb(integer_value=187680)
        sub_value2 = _value_pb(string_value=u"how low can you go?")
        map_pb = document_pb2.MapValue(
            fields={"first": sub_value1, "second": sub_value2}
        )
        value = _value_pb(map_value=map_pb)

        expected = {
            "first": sub_value1.integer_value,
            "second": sub_value2.string_value,
        }
        self.assertEqual(self._call_fut(value), expected)

    def test_nested_map(self):
        from google.cloud.firestore_v1.proto import document_pb2

        actual_value1 = 1009876
        actual_value2 = u"hey you guys"
        actual_value3 = 90.875
        map_pb1 = document_pb2.MapValue(
            fields={
                "lowest": _value_pb(integer_value=actual_value1),
                "aside": _value_pb(string_value=actual_value2),
            }
        )
        map_pb2 = document_pb2.MapValue(
            fields={
                "middle": _value_pb(map_value=map_pb1),
                "aside": _value_pb(boolean_value=True),
            }
        )
        map_pb3 = document_pb2.MapValue(
            fields={
                "highest": _value_pb(map_value=map_pb2),
                "aside": _value_pb(double_value=actual_value3),
            }
        )
        value = _value_pb(map_value=map_pb3)

        expected = {
            "highest": {
                "middle": {"lowest": actual_value1, "aside": actual_value2},
                "aside": True,
            },
            "aside": actual_value3,
        }
        self.assertEqual(self._call_fut(value), expected)

    def test_unset_value_type(self):
        with self.assertRaises(ValueError):
            self._call_fut(_value_pb())

    def test_unknown_value_type(self):
        value_pb = mock.Mock(spec=["WhichOneof"])
        value_pb.WhichOneof.return_value = "zoob_value"

        with self.assertRaises(ValueError):
            self._call_fut(value_pb)

        value_pb.WhichOneof.assert_called_once_with("value_type")


class Test_decode_dict(unittest.TestCase):
    @staticmethod
    def _call_fut(value_fields, client=mock.sentinel.client):
        from google.cloud.firestore_v1._helpers import decode_dict

        return decode_dict(value_fields, client)

    @unittest.skipIf(
        (3,) <= sys.version_info < (3, 4, 4), "known datetime bug (bpo-23517) in Python"
    )
    def test_many_types(self):
        from google.protobuf import struct_pb2
        from google.protobuf import timestamp_pb2
        from google.cloud.firestore_v1.proto.document_pb2 import ArrayValue
        from google.cloud.firestore_v1.proto.document_pb2 import MapValue
        from google.cloud._helpers import UTC
        from google.cloud.firestore_v1.field_path import FieldPath

        dt_seconds = 1394037350
        dt_nanos = 667285000
        # Make sure precision is valid in microseconds too.
        self.assertEqual(dt_nanos % 1000, 0)
        dt_val = datetime.datetime.utcfromtimestamp(
            dt_seconds + 1e-9 * dt_nanos
        ).replace(tzinfo=UTC)

        value_fields = {
            "foo": _value_pb(null_value=struct_pb2.NULL_VALUE),
            "bar": _value_pb(boolean_value=True),
            "baz": _value_pb(integer_value=981),
            "quux": _value_pb(double_value=2.875),
            "quuz": _value_pb(
                timestamp_value=timestamp_pb2.Timestamp(
                    seconds=dt_seconds, nanos=dt_nanos
                )
            ),
            "corge": _value_pb(string_value=u"\N{snowman}"),
            "grault": _value_pb(bytes_value=b"\xe2\x98\x83"),
            "garply": _value_pb(
                array_value=ArrayValue(
                    values=[
                        _value_pb(string_value=u"fork"),
                        _value_pb(double_value=4.0),
                    ]
                )
            ),
            "waldo": _value_pb(
                map_value=MapValue(
                    fields={
                        "fred": _value_pb(string_value=u"zap"),
                        "thud": _value_pb(boolean_value=False),
                    }
                )
            ),
            FieldPath("a", "b", "c").to_api_repr(): _value_pb(boolean_value=False),
        }
        expected = {
            "foo": None,
            "bar": True,
            "baz": 981,
            "quux": 2.875,
            "quuz": dt_val,
            "corge": u"\N{snowman}",
            "grault": b"\xe2\x98\x83",
            "garply": [u"fork", 4.0],
            "waldo": {"fred": u"zap", "thud": False},
            "a.b.c": False,
        }
        self.assertEqual(self._call_fut(value_fields), expected)


class Test_get_doc_id(unittest.TestCase):
    @staticmethod
    def _call_fut(document_pb, expected_prefix):
        from google.cloud.firestore_v1._helpers import get_doc_id

        return get_doc_id(document_pb, expected_prefix)

    @staticmethod
    def _dummy_ref_string(collection_id):
        from google.cloud.firestore_v1.client import DEFAULT_DATABASE

        project = u"bazzzz"
        return u"projects/{}/databases/{}/documents/{}".format(
            project, DEFAULT_DATABASE, collection_id
        )

    def test_success(self):
        from google.cloud.firestore_v1.proto import document_pb2

        prefix = self._dummy_ref_string("sub-collection")
        actual_id = "this-is-the-one"
        name = "{}/{}".format(prefix, actual_id)

        document_pb = document_pb2.Document(name=name)
        document_id = self._call_fut(document_pb, prefix)
        self.assertEqual(document_id, actual_id)

    def test_failure(self):
        from google.cloud.firestore_v1.proto import document_pb2

        actual_prefix = self._dummy_ref_string("the-right-one")
        wrong_prefix = self._dummy_ref_string("the-wrong-one")
        name = "{}/{}".format(actual_prefix, "sorry-wont-works")

        document_pb = document_pb2.Document(name=name)
        with self.assertRaises(ValueError) as exc_info:
            self._call_fut(document_pb, wrong_prefix)

        exc_args = exc_info.exception.args
        self.assertEqual(len(exc_args), 4)
        self.assertEqual(exc_args[1], name)
        self.assertEqual(exc_args[3], wrong_prefix)


class Test_extract_fields(unittest.TestCase):
    @staticmethod
    def _call_fut(document_data, prefix_path, expand_dots=False):
        from google.cloud.firestore_v1 import _helpers

        return _helpers.extract_fields(
            document_data, prefix_path, expand_dots=expand_dots
        )

    def test_w_empty_document(self):
        from google.cloud.firestore_v1._helpers import _EmptyDict

        document_data = {}
        prefix_path = _make_field_path()
        expected = [(_make_field_path(), _EmptyDict)]

        iterator = self._call_fut(document_data, prefix_path)
        self.assertEqual(list(iterator), expected)

    def test_w_invalid_key_and_expand_dots(self):
        document_data = {"b": 1, "a~d": 2, "c": 3}
        prefix_path = _make_field_path()

        with self.assertRaises(ValueError):
            list(self._call_fut(document_data, prefix_path, expand_dots=True))

    def test_w_shallow_keys(self):
        document_data = {"b": 1, "a": 2, "c": 3}
        prefix_path = _make_field_path()
        expected = [
            (_make_field_path("a"), 2),
            (_make_field_path("b"), 1),
            (_make_field_path("c"), 3),
        ]

        iterator = self._call_fut(document_data, prefix_path)
        self.assertEqual(list(iterator), expected)

    def test_w_nested(self):
        from google.cloud.firestore_v1._helpers import _EmptyDict

        document_data = {"b": {"a": {"d": 4, "c": 3, "g": {}}, "e": 7}, "f": 5}
        prefix_path = _make_field_path()
        expected = [
            (_make_field_path("b", "a", "c"), 3),
            (_make_field_path("b", "a", "d"), 4),
            (_make_field_path("b", "a", "g"), _EmptyDict),
            (_make_field_path("b", "e"), 7),
            (_make_field_path("f"), 5),
        ]

        iterator = self._call_fut(document_data, prefix_path)
        self.assertEqual(list(iterator), expected)

    def test_w_expand_dotted(self):
        from google.cloud.firestore_v1._helpers import _EmptyDict

        document_data = {
            "b": {"a": {"d": 4, "c": 3, "g": {}, "k.l.m": 17}, "e": 7},
            "f": 5,
            "h.i.j": 9,
        }
        prefix_path = _make_field_path()
        expected = [
            (_make_field_path("b", "a", "c"), 3),
            (_make_field_path("b", "a", "d"), 4),
            (_make_field_path("b", "a", "g"), _EmptyDict),
            (_make_field_path("b", "a", "k.l.m"), 17),
            (_make_field_path("b", "e"), 7),
            (_make_field_path("f"), 5),
            (_make_field_path("h", "i", "j"), 9),
        ]

        iterator = self._call_fut(document_data, prefix_path, expand_dots=True)
        self.assertEqual(list(iterator), expected)


class Test_set_field_value(unittest.TestCase):
    @staticmethod
    def _call_fut(document_data, field_path, value):
        from google.cloud.firestore_v1 import _helpers

        return _helpers.set_field_value(document_data, field_path, value)

    def test_normal_value_w_shallow(self):
        document = {}
        field_path = _make_field_path("a")
        value = 3

        self._call_fut(document, field_path, value)

        self.assertEqual(document, {"a": 3})

    def test_normal_value_w_nested(self):
        document = {}
        field_path = _make_field_path("a", "b", "c")
        value = 3

        self._call_fut(document, field_path, value)

        self.assertEqual(document, {"a": {"b": {"c": 3}}})

    def test_empty_dict_w_shallow(self):
        from google.cloud.firestore_v1._helpers import _EmptyDict

        document = {}
        field_path = _make_field_path("a")
        value = _EmptyDict

        self._call_fut(document, field_path, value)

        self.assertEqual(document, {"a": {}})

    def test_empty_dict_w_nested(self):
        from google.cloud.firestore_v1._helpers import _EmptyDict

        document = {}
        field_path = _make_field_path("a", "b", "c")
        value = _EmptyDict

        self._call_fut(document, field_path, value)

        self.assertEqual(document, {"a": {"b": {"c": {}}}})


class Test_get_field_value(unittest.TestCase):
    @staticmethod
    def _call_fut(document_data, field_path):
        from google.cloud.firestore_v1 import _helpers

        return _helpers.get_field_value(document_data, field_path)

    def test_w_empty_path(self):
        document = {}

        with self.assertRaises(ValueError):
            self._call_fut(document, _make_field_path())

    def test_miss_shallow(self):
        document = {}

        with self.assertRaises(KeyError):
            self._call_fut(document, _make_field_path("nonesuch"))

    def test_miss_nested(self):
        document = {"a": {"b": {}}}

        with self.assertRaises(KeyError):
            self._call_fut(document, _make_field_path("a", "b", "c"))

    def test_hit_shallow(self):
        document = {"a": 1}

        self.assertEqual(self._call_fut(document, _make_field_path("a")), 1)

    def test_hit_nested(self):
        document = {"a": {"b": {"c": 1}}}

        self.assertEqual(self._call_fut(document, _make_field_path("a", "b", "c")), 1)


class TestDocumentExtractor(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1 import _helpers

        return _helpers.DocumentExtractor

    def _make_one(self, document_data):
        return self._get_target_class()(document_data)

    def test_ctor_w_empty_document(self):
        document_data = {}

        inst = self._make_one(document_data)

        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, {})
        self.assertTrue(inst.empty_document)
        self.assertFalse(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [])

    def test_ctor_w_delete_field_shallow(self):
        from google.cloud.firestore_v1.transforms import DELETE_FIELD

        document_data = {"a": DELETE_FIELD}

        inst = self._make_one(document_data)

        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [_make_field_path("a")])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertFalse(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [])

    def test_ctor_w_delete_field_nested(self):
        from google.cloud.firestore_v1.transforms import DELETE_FIELD

        document_data = {"a": {"b": {"c": DELETE_FIELD}}}

        inst = self._make_one(document_data)

        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [_make_field_path("a", "b", "c")])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertFalse(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [])

    def test_ctor_w_server_timestamp_shallow(self):
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP

        document_data = {"a": SERVER_TIMESTAMP}

        inst = self._make_one(document_data)

        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [_make_field_path("a")])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertTrue(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [_make_field_path("a")])

    def test_ctor_w_server_timestamp_nested(self):
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP

        document_data = {"a": {"b": {"c": SERVER_TIMESTAMP}}}

        inst = self._make_one(document_data)

        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [_make_field_path("a", "b", "c")])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertTrue(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [_make_field_path("a", "b", "c")])

    def test_ctor_w_array_remove_shallow(self):
        from google.cloud.firestore_v1.transforms import ArrayRemove

        values = [1, 3, 5]
        document_data = {"a": ArrayRemove(values)}

        inst = self._make_one(document_data)

        expected_array_removes = {_make_field_path("a"): values}
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, expected_array_removes)
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertTrue(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [_make_field_path("a")])

    def test_ctor_w_array_remove_nested(self):
        from google.cloud.firestore_v1.transforms import ArrayRemove

        values = [2, 4, 8]
        document_data = {"a": {"b": {"c": ArrayRemove(values)}}}

        inst = self._make_one(document_data)

        expected_array_removes = {_make_field_path("a", "b", "c"): values}
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, expected_array_removes)
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertTrue(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [_make_field_path("a", "b", "c")])

    def test_ctor_w_array_union_shallow(self):
        from google.cloud.firestore_v1.transforms import ArrayUnion

        values = [1, 3, 5]
        document_data = {"a": ArrayUnion(values)}

        inst = self._make_one(document_data)

        expected_array_unions = {_make_field_path("a"): values}
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, expected_array_unions)
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertTrue(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [_make_field_path("a")])

    def test_ctor_w_array_union_nested(self):
        from google.cloud.firestore_v1.transforms import ArrayUnion

        values = [2, 4, 8]
        document_data = {"a": {"b": {"c": ArrayUnion(values)}}}

        inst = self._make_one(document_data)

        expected_array_unions = {_make_field_path("a", "b", "c"): values}
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, expected_array_unions)
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertTrue(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [_make_field_path("a", "b", "c")])

    def test_ctor_w_increment_shallow(self):
        from google.cloud.firestore_v1.transforms import Increment

        value = 1
        document_data = {"a": Increment(value)}

        inst = self._make_one(document_data)

        expected_increments = {_make_field_path("a"): value}
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, expected_increments)
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertTrue(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [_make_field_path("a")])

    def test_ctor_w_increment_nested(self):
        from google.cloud.firestore_v1.transforms import Increment

        value = 2
        document_data = {"a": {"b": {"c": Increment(value)}}}

        inst = self._make_one(document_data)

        expected_increments = {_make_field_path("a", "b", "c"): value}
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, expected_increments)
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertTrue(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [_make_field_path("a", "b", "c")])

    def test_ctor_w_maximum_shallow(self):
        from google.cloud.firestore_v1.transforms import Maximum

        value = 1
        document_data = {"a": Maximum(value)}

        inst = self._make_one(document_data)

        expected_maximums = {_make_field_path("a"): value}
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, expected_maximums)
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertTrue(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [_make_field_path("a")])

    def test_ctor_w_maximum_nested(self):
        from google.cloud.firestore_v1.transforms import Maximum

        value = 2
        document_data = {"a": {"b": {"c": Maximum(value)}}}

        inst = self._make_one(document_data)

        expected_maximums = {_make_field_path("a", "b", "c"): value}
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, expected_maximums)
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertTrue(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [_make_field_path("a", "b", "c")])

    def test_ctor_w_minimum_shallow(self):
        from google.cloud.firestore_v1.transforms import Minimum

        value = 1
        document_data = {"a": Minimum(value)}

        inst = self._make_one(document_data)

        expected_minimums = {_make_field_path("a"): value}
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, expected_minimums)
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertTrue(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [_make_field_path("a")])

    def test_ctor_w_minimum_nested(self):
        from google.cloud.firestore_v1.transforms import Minimum

        value = 2
        document_data = {"a": {"b": {"c": Minimum(value)}}}

        inst = self._make_one(document_data)

        expected_minimums = {_make_field_path("a", "b", "c"): value}
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, [])
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, expected_minimums)
        self.assertEqual(inst.set_fields, {})
        self.assertFalse(inst.empty_document)
        self.assertTrue(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [_make_field_path("a", "b", "c")])

    def test_ctor_w_empty_dict_shallow(self):
        document_data = {"a": {}}

        inst = self._make_one(document_data)

        expected_field_paths = [_make_field_path("a")]
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, expected_field_paths)
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, document_data)
        self.assertFalse(inst.empty_document)
        self.assertFalse(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [])

    def test_ctor_w_empty_dict_nested(self):
        document_data = {"a": {"b": {"c": {}}}}

        inst = self._make_one(document_data)

        expected_field_paths = [_make_field_path("a", "b", "c")]
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, expected_field_paths)
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, document_data)
        self.assertFalse(inst.empty_document)
        self.assertFalse(inst.has_transforms)
        self.assertEqual(inst.transform_paths, [])

    def test_ctor_w_normal_value_shallow(self):
        document_data = {"b": 1, "a": 2, "c": 3}

        inst = self._make_one(document_data)

        expected_field_paths = [
            _make_field_path("a"),
            _make_field_path("b"),
            _make_field_path("c"),
        ]
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, expected_field_paths)
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.set_fields, document_data)
        self.assertFalse(inst.empty_document)
        self.assertFalse(inst.has_transforms)

    def test_ctor_w_normal_value_nested(self):
        document_data = {"b": {"a": {"d": 4, "c": 3}, "e": 7}, "f": 5}

        inst = self._make_one(document_data)

        expected_field_paths = [
            _make_field_path("b", "a", "c"),
            _make_field_path("b", "a", "d"),
            _make_field_path("b", "e"),
            _make_field_path("f"),
        ]
        self.assertEqual(inst.document_data, document_data)
        self.assertEqual(inst.field_paths, expected_field_paths)
        self.assertEqual(inst.deleted_fields, [])
        self.assertEqual(inst.server_timestamps, [])
        self.assertEqual(inst.array_removes, {})
        self.assertEqual(inst.array_unions, {})
        self.assertEqual(inst.increments, {})
        self.assertEqual(inst.maximums, {})
        self.assertEqual(inst.minimums, {})
        self.assertEqual(inst.set_fields, document_data)
        self.assertFalse(inst.empty_document)
        self.assertFalse(inst.has_transforms)

    def test_get_update_pb_w_exists_precondition(self):
        from google.cloud.firestore_v1.proto import write_pb2

        document_data = {}
        inst = self._make_one(document_data)
        document_path = (
            "projects/project-id/databases/(default)/" "documents/document-id"
        )

        update_pb = inst.get_update_pb(document_path, exists=False)

        self.assertIsInstance(update_pb, write_pb2.Write)
        self.assertEqual(update_pb.update.name, document_path)
        self.assertEqual(update_pb.update.fields, document_data)
        self.assertTrue(update_pb.HasField("current_document"))
        self.assertFalse(update_pb.current_document.exists)

    def test_get_update_pb_wo_exists_precondition(self):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1._helpers import encode_dict

        document_data = {"a": 1}
        inst = self._make_one(document_data)
        document_path = (
            "projects/project-id/databases/(default)/" "documents/document-id"
        )

        update_pb = inst.get_update_pb(document_path)

        self.assertIsInstance(update_pb, write_pb2.Write)
        self.assertEqual(update_pb.update.name, document_path)
        self.assertEqual(update_pb.update.fields, encode_dict(document_data))
        self.assertFalse(update_pb.HasField("current_document"))

    def test_get_transform_pb_w_server_timestamp_w_exists_precondition(self):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP
        from google.cloud.firestore_v1._helpers import REQUEST_TIME_ENUM

        document_data = {"a": SERVER_TIMESTAMP}
        inst = self._make_one(document_data)
        document_path = (
            "projects/project-id/databases/(default)/" "documents/document-id"
        )

        transform_pb = inst.get_transform_pb(document_path, exists=False)

        self.assertIsInstance(transform_pb, write_pb2.Write)
        self.assertEqual(transform_pb.transform.document, document_path)
        transforms = transform_pb.transform.field_transforms
        self.assertEqual(len(transforms), 1)
        transform = transforms[0]
        self.assertEqual(transform.field_path, "a")
        self.assertEqual(transform.set_to_server_value, REQUEST_TIME_ENUM)
        self.assertTrue(transform_pb.HasField("current_document"))
        self.assertFalse(transform_pb.current_document.exists)

    def test_get_transform_pb_w_server_timestamp_wo_exists_precondition(self):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP
        from google.cloud.firestore_v1._helpers import REQUEST_TIME_ENUM

        document_data = {"a": {"b": {"c": SERVER_TIMESTAMP}}}
        inst = self._make_one(document_data)
        document_path = (
            "projects/project-id/databases/(default)/" "documents/document-id"
        )

        transform_pb = inst.get_transform_pb(document_path)

        self.assertIsInstance(transform_pb, write_pb2.Write)
        self.assertEqual(transform_pb.transform.document, document_path)
        transforms = transform_pb.transform.field_transforms
        self.assertEqual(len(transforms), 1)
        transform = transforms[0]
        self.assertEqual(transform.field_path, "a.b.c")
        self.assertEqual(transform.set_to_server_value, REQUEST_TIME_ENUM)
        self.assertFalse(transform_pb.HasField("current_document"))

    @staticmethod
    def _array_value_to_list(array_value):
        from google.cloud.firestore_v1._helpers import decode_value

        return [decode_value(element, client=None) for element in array_value.values]

    def test_get_transform_pb_w_array_remove(self):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1.transforms import ArrayRemove

        values = [2, 4, 8]
        document_data = {"a": {"b": {"c": ArrayRemove(values)}}}
        inst = self._make_one(document_data)
        document_path = (
            "projects/project-id/databases/(default)/" "documents/document-id"
        )

        transform_pb = inst.get_transform_pb(document_path)

        self.assertIsInstance(transform_pb, write_pb2.Write)
        self.assertEqual(transform_pb.transform.document, document_path)
        transforms = transform_pb.transform.field_transforms
        self.assertEqual(len(transforms), 1)
        transform = transforms[0]
        self.assertEqual(transform.field_path, "a.b.c")
        removed = self._array_value_to_list(transform.remove_all_from_array)
        self.assertEqual(removed, values)
        self.assertFalse(transform_pb.HasField("current_document"))

    def test_get_transform_pb_w_array_union(self):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1.transforms import ArrayUnion

        values = [1, 3, 5]
        document_data = {"a": {"b": {"c": ArrayUnion(values)}}}
        inst = self._make_one(document_data)
        document_path = (
            "projects/project-id/databases/(default)/" "documents/document-id"
        )

        transform_pb = inst.get_transform_pb(document_path)

        self.assertIsInstance(transform_pb, write_pb2.Write)
        self.assertEqual(transform_pb.transform.document, document_path)
        transforms = transform_pb.transform.field_transforms
        self.assertEqual(len(transforms), 1)
        transform = transforms[0]
        self.assertEqual(transform.field_path, "a.b.c")
        added = self._array_value_to_list(transform.append_missing_elements)
        self.assertEqual(added, values)
        self.assertFalse(transform_pb.HasField("current_document"))

    def test_get_transform_pb_w_increment_int(self):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1.transforms import Increment

        value = 1
        document_data = {"a": {"b": {"c": Increment(value)}}}
        inst = self._make_one(document_data)
        document_path = (
            "projects/project-id/databases/(default)/" "documents/document-id"
        )

        transform_pb = inst.get_transform_pb(document_path)

        self.assertIsInstance(transform_pb, write_pb2.Write)
        self.assertEqual(transform_pb.transform.document, document_path)
        transforms = transform_pb.transform.field_transforms
        self.assertEqual(len(transforms), 1)
        transform = transforms[0]
        self.assertEqual(transform.field_path, "a.b.c")
        added = transform.increment.integer_value
        self.assertEqual(added, value)
        self.assertFalse(transform_pb.HasField("current_document"))

    def test_get_transform_pb_w_increment_float(self):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1.transforms import Increment

        value = 3.1415926
        document_data = {"a": {"b": {"c": Increment(value)}}}
        inst = self._make_one(document_data)
        document_path = (
            "projects/project-id/databases/(default)/" "documents/document-id"
        )

        transform_pb = inst.get_transform_pb(document_path)

        self.assertIsInstance(transform_pb, write_pb2.Write)
        self.assertEqual(transform_pb.transform.document, document_path)
        transforms = transform_pb.transform.field_transforms
        self.assertEqual(len(transforms), 1)
        transform = transforms[0]
        self.assertEqual(transform.field_path, "a.b.c")
        added = transform.increment.double_value
        self.assertEqual(added, value)
        self.assertFalse(transform_pb.HasField("current_document"))

    def test_get_transform_pb_w_maximum_int(self):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1.transforms import Maximum

        value = 1
        document_data = {"a": {"b": {"c": Maximum(value)}}}
        inst = self._make_one(document_data)
        document_path = (
            "projects/project-id/databases/(default)/" "documents/document-id"
        )

        transform_pb = inst.get_transform_pb(document_path)

        self.assertIsInstance(transform_pb, write_pb2.Write)
        self.assertEqual(transform_pb.transform.document, document_path)
        transforms = transform_pb.transform.field_transforms
        self.assertEqual(len(transforms), 1)
        transform = transforms[0]
        self.assertEqual(transform.field_path, "a.b.c")
        added = transform.maximum.integer_value
        self.assertEqual(added, value)
        self.assertFalse(transform_pb.HasField("current_document"))

    def test_get_transform_pb_w_maximum_float(self):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1.transforms import Maximum

        value = 3.1415926
        document_data = {"a": {"b": {"c": Maximum(value)}}}
        inst = self._make_one(document_data)
        document_path = (
            "projects/project-id/databases/(default)/" "documents/document-id"
        )

        transform_pb = inst.get_transform_pb(document_path)

        self.assertIsInstance(transform_pb, write_pb2.Write)
        self.assertEqual(transform_pb.transform.document, document_path)
        transforms = transform_pb.transform.field_transforms
        self.assertEqual(len(transforms), 1)
        transform = transforms[0]
        self.assertEqual(transform.field_path, "a.b.c")
        added = transform.maximum.double_value
        self.assertEqual(added, value)
        self.assertFalse(transform_pb.HasField("current_document"))

    def test_get_transform_pb_w_minimum_int(self):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1.transforms import Minimum

        value = 1
        document_data = {"a": {"b": {"c": Minimum(value)}}}
        inst = self._make_one(document_data)
        document_path = (
            "projects/project-id/databases/(default)/" "documents/document-id"
        )

        transform_pb = inst.get_transform_pb(document_path)

        self.assertIsInstance(transform_pb, write_pb2.Write)
        self.assertEqual(transform_pb.transform.document, document_path)
        transforms = transform_pb.transform.field_transforms
        self.assertEqual(len(transforms), 1)
        transform = transforms[0]
        self.assertEqual(transform.field_path, "a.b.c")
        added = transform.minimum.integer_value
        self.assertEqual(added, value)
        self.assertFalse(transform_pb.HasField("current_document"))

    def test_get_transform_pb_w_minimum_float(self):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1.transforms import Minimum

        value = 3.1415926
        document_data = {"a": {"b": {"c": Minimum(value)}}}
        inst = self._make_one(document_data)
        document_path = (
            "projects/project-id/databases/(default)/" "documents/document-id"
        )

        transform_pb = inst.get_transform_pb(document_path)

        self.assertIsInstance(transform_pb, write_pb2.Write)
        self.assertEqual(transform_pb.transform.document, document_path)
        transforms = transform_pb.transform.field_transforms
        self.assertEqual(len(transforms), 1)
        transform = transforms[0]
        self.assertEqual(transform.field_path, "a.b.c")
        added = transform.minimum.double_value
        self.assertEqual(added, value)
        self.assertFalse(transform_pb.HasField("current_document"))


class Test_pbs_for_create(unittest.TestCase):
    @staticmethod
    def _call_fut(document_path, document_data):
        from google.cloud.firestore_v1._helpers import pbs_for_create

        return pbs_for_create(document_path, document_data)

    @staticmethod
    def _make_write_w_document(document_path, **data):
        from google.cloud.firestore_v1.proto import document_pb2
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1._helpers import encode_dict
        from google.cloud.firestore_v1.proto import common_pb2

        return write_pb2.Write(
            update=document_pb2.Document(name=document_path, fields=encode_dict(data)),
            current_document=common_pb2.Precondition(exists=False),
        )

    @staticmethod
    def _make_write_w_transform(document_path, fields):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1.gapic import enums

        server_val = enums.DocumentTransform.FieldTransform.ServerValue
        transforms = [
            write_pb2.DocumentTransform.FieldTransform(
                field_path=field, set_to_server_value=server_val.REQUEST_TIME
            )
            for field in fields
        ]

        return write_pb2.Write(
            transform=write_pb2.DocumentTransform(
                document=document_path, field_transforms=transforms
            )
        )

    def _helper(self, do_transform=False, empty_val=False):
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP

        document_path = _make_ref_string(u"little", u"town", u"of", u"ham")
        document_data = {"cheese": 1.5, "crackers": True}

        if do_transform:
            document_data["butter"] = SERVER_TIMESTAMP

        if empty_val:
            document_data["mustard"] = {}

        write_pbs = self._call_fut(document_path, document_data)

        if empty_val:
            update_pb = self._make_write_w_document(
                document_path, cheese=1.5, crackers=True, mustard={}
            )
        else:
            update_pb = self._make_write_w_document(
                document_path, cheese=1.5, crackers=True
            )
        expected_pbs = [update_pb]

        if do_transform:
            expected_pbs.append(
                self._make_write_w_transform(document_path, fields=["butter"])
            )

        self.assertEqual(write_pbs, expected_pbs)

    def test_without_transform(self):
        self._helper()

    def test_w_transform(self):
        self._helper(do_transform=True)

    def test_w_transform_and_empty_value(self):
        self._helper(do_transform=True, empty_val=True)


class Test_pbs_for_set_no_merge(unittest.TestCase):
    @staticmethod
    def _call_fut(document_path, document_data):
        from google.cloud.firestore_v1 import _helpers

        return _helpers.pbs_for_set_no_merge(document_path, document_data)

    @staticmethod
    def _make_write_w_document(document_path, **data):
        from google.cloud.firestore_v1.proto import document_pb2
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1._helpers import encode_dict

        return write_pb2.Write(
            update=document_pb2.Document(name=document_path, fields=encode_dict(data))
        )

    @staticmethod
    def _make_write_w_transform(document_path, fields):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1.gapic import enums

        server_val = enums.DocumentTransform.FieldTransform.ServerValue
        transforms = [
            write_pb2.DocumentTransform.FieldTransform(
                field_path=field, set_to_server_value=server_val.REQUEST_TIME
            )
            for field in fields
        ]

        return write_pb2.Write(
            transform=write_pb2.DocumentTransform(
                document=document_path, field_transforms=transforms
            )
        )

    def test_w_empty_document(self):
        document_path = _make_ref_string(u"little", u"town", u"of", u"ham")
        document_data = {}

        write_pbs = self._call_fut(document_path, document_data)

        update_pb = self._make_write_w_document(document_path)
        expected_pbs = [update_pb]
        self.assertEqual(write_pbs, expected_pbs)

    def test_w_only_server_timestamp(self):
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP

        document_path = _make_ref_string(u"little", u"town", u"of", u"ham")
        document_data = {"butter": SERVER_TIMESTAMP}

        write_pbs = self._call_fut(document_path, document_data)

        update_pb = self._make_write_w_document(document_path)
        transform_pb = self._make_write_w_transform(document_path, ["butter"])
        expected_pbs = [update_pb, transform_pb]
        self.assertEqual(write_pbs, expected_pbs)

    def _helper(self, do_transform=False, empty_val=False):
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP

        document_path = _make_ref_string(u"little", u"town", u"of", u"ham")
        document_data = {"cheese": 1.5, "crackers": True}

        if do_transform:
            document_data["butter"] = SERVER_TIMESTAMP

        if empty_val:
            document_data["mustard"] = {}

        write_pbs = self._call_fut(document_path, document_data)

        if empty_val:
            update_pb = self._make_write_w_document(
                document_path, cheese=1.5, crackers=True, mustard={}
            )
        else:
            update_pb = self._make_write_w_document(
                document_path, cheese=1.5, crackers=True
            )
        expected_pbs = [update_pb]

        if do_transform:
            expected_pbs.append(
                self._make_write_w_transform(document_path, fields=["butter"])
            )

        self.assertEqual(write_pbs, expected_pbs)

    def test_defaults(self):
        self._helper()

    def test_w_transform(self):
        self._helper(do_transform=True)

    def test_w_transform_and_empty_value(self):
        # Exercise #5944
        self._helper(do_transform=True, empty_val=True)


class TestDocumentExtractorForMerge(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1 import _helpers

        return _helpers.DocumentExtractorForMerge

    def _make_one(self, document_data):
        return self._get_target_class()(document_data)

    def test_ctor_w_empty_document(self):
        document_data = {}

        inst = self._make_one(document_data)

        self.assertEqual(inst.data_merge, [])
        self.assertEqual(inst.transform_merge, [])
        self.assertEqual(inst.merge, [])

    def test_apply_merge_all_w_empty_document(self):
        document_data = {}
        inst = self._make_one(document_data)

        inst.apply_merge(True)

        self.assertEqual(inst.data_merge, [])
        self.assertEqual(inst.transform_merge, [])
        self.assertEqual(inst.merge, [])
        self.assertFalse(inst.has_updates)

    def test_apply_merge_all_w_delete(self):
        from google.cloud.firestore_v1.transforms import DELETE_FIELD

        document_data = {"write_me": "value", "delete_me": DELETE_FIELD}
        inst = self._make_one(document_data)

        inst.apply_merge(True)

        expected_data_merge = [
            _make_field_path("delete_me"),
            _make_field_path("write_me"),
        ]
        self.assertEqual(inst.data_merge, expected_data_merge)
        self.assertEqual(inst.transform_merge, [])
        self.assertEqual(inst.merge, expected_data_merge)
        self.assertTrue(inst.has_updates)

    def test_apply_merge_all_w_server_timestamp(self):
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP

        document_data = {"write_me": "value", "timestamp": SERVER_TIMESTAMP}
        inst = self._make_one(document_data)

        inst.apply_merge(True)

        expected_data_merge = [_make_field_path("write_me")]
        expected_transform_merge = [_make_field_path("timestamp")]
        expected_merge = [_make_field_path("timestamp"), _make_field_path("write_me")]
        self.assertEqual(inst.data_merge, expected_data_merge)
        self.assertEqual(inst.transform_merge, expected_transform_merge)
        self.assertEqual(inst.merge, expected_merge)
        self.assertTrue(inst.has_updates)

    def test_apply_merge_list_fields_w_empty_document(self):
        document_data = {}
        inst = self._make_one(document_data)

        with self.assertRaises(ValueError):
            inst.apply_merge(["nonesuch", "or.this"])

    def test_apply_merge_list_fields_w_unmerged_delete(self):
        from google.cloud.firestore_v1.transforms import DELETE_FIELD

        document_data = {
            "write_me": "value",
            "delete_me": DELETE_FIELD,
            "ignore_me": 123,
            "unmerged_delete": DELETE_FIELD,
        }
        inst = self._make_one(document_data)

        with self.assertRaises(ValueError):
            inst.apply_merge(["write_me", "delete_me"])

    def test_apply_merge_list_fields_w_delete(self):
        from google.cloud.firestore_v1.transforms import DELETE_FIELD

        document_data = {
            "write_me": "value",
            "delete_me": DELETE_FIELD,
            "ignore_me": 123,
        }
        inst = self._make_one(document_data)

        inst.apply_merge(["write_me", "delete_me"])

        expected_set_fields = {"write_me": "value"}
        expected_deleted_fields = [_make_field_path("delete_me")]
        self.assertEqual(inst.set_fields, expected_set_fields)
        self.assertEqual(inst.deleted_fields, expected_deleted_fields)
        self.assertTrue(inst.has_updates)

    def test_apply_merge_list_fields_w_prefixes(self):

        document_data = {"a": {"b": {"c": 123}}}
        inst = self._make_one(document_data)

        with self.assertRaises(ValueError):
            inst.apply_merge(["a", "a.b"])

    def test_apply_merge_list_fields_w_missing_data_string_paths(self):

        document_data = {"write_me": "value", "ignore_me": 123}
        inst = self._make_one(document_data)

        with self.assertRaises(ValueError):
            inst.apply_merge(["write_me", "nonesuch"])

    def test_apply_merge_list_fields_w_non_merge_field(self):

        document_data = {"write_me": "value", "ignore_me": 123}
        inst = self._make_one(document_data)

        inst.apply_merge([_make_field_path("write_me")])

        expected_set_fields = {"write_me": "value"}
        self.assertEqual(inst.set_fields, expected_set_fields)
        self.assertTrue(inst.has_updates)

    def test_apply_merge_list_fields_w_server_timestamp(self):
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP

        document_data = {
            "write_me": "value",
            "timestamp": SERVER_TIMESTAMP,
            "ignored_stamp": SERVER_TIMESTAMP,
        }
        inst = self._make_one(document_data)

        inst.apply_merge([_make_field_path("write_me"), _make_field_path("timestamp")])

        expected_data_merge = [_make_field_path("write_me")]
        expected_transform_merge = [_make_field_path("timestamp")]
        expected_merge = [_make_field_path("timestamp"), _make_field_path("write_me")]
        self.assertEqual(inst.data_merge, expected_data_merge)
        self.assertEqual(inst.transform_merge, expected_transform_merge)
        self.assertEqual(inst.merge, expected_merge)
        expected_server_timestamps = [_make_field_path("timestamp")]
        self.assertEqual(inst.server_timestamps, expected_server_timestamps)
        self.assertTrue(inst.has_updates)

    def test_apply_merge_list_fields_w_array_remove(self):
        from google.cloud.firestore_v1.transforms import ArrayRemove

        values = [2, 4, 8]
        document_data = {
            "write_me": "value",
            "remove_me": ArrayRemove(values),
            "ignored_remove_me": ArrayRemove((1, 3, 5)),
        }
        inst = self._make_one(document_data)

        inst.apply_merge([_make_field_path("write_me"), _make_field_path("remove_me")])

        expected_data_merge = [_make_field_path("write_me")]
        expected_transform_merge = [_make_field_path("remove_me")]
        expected_merge = [_make_field_path("remove_me"), _make_field_path("write_me")]
        self.assertEqual(inst.data_merge, expected_data_merge)
        self.assertEqual(inst.transform_merge, expected_transform_merge)
        self.assertEqual(inst.merge, expected_merge)
        expected_array_removes = {_make_field_path("remove_me"): values}
        self.assertEqual(inst.array_removes, expected_array_removes)
        self.assertTrue(inst.has_updates)

    def test_apply_merge_list_fields_w_array_union(self):
        from google.cloud.firestore_v1.transforms import ArrayUnion

        values = [1, 3, 5]
        document_data = {
            "write_me": "value",
            "union_me": ArrayUnion(values),
            "ignored_union_me": ArrayUnion((2, 4, 8)),
        }
        inst = self._make_one(document_data)

        inst.apply_merge([_make_field_path("write_me"), _make_field_path("union_me")])

        expected_data_merge = [_make_field_path("write_me")]
        expected_transform_merge = [_make_field_path("union_me")]
        expected_merge = [_make_field_path("union_me"), _make_field_path("write_me")]
        self.assertEqual(inst.data_merge, expected_data_merge)
        self.assertEqual(inst.transform_merge, expected_transform_merge)
        self.assertEqual(inst.merge, expected_merge)
        expected_array_unions = {_make_field_path("union_me"): values}
        self.assertEqual(inst.array_unions, expected_array_unions)
        self.assertTrue(inst.has_updates)


class Test_pbs_for_set_with_merge(unittest.TestCase):
    @staticmethod
    def _call_fut(document_path, document_data, merge):
        from google.cloud.firestore_v1 import _helpers

        return _helpers.pbs_for_set_with_merge(
            document_path, document_data, merge=merge
        )

    @staticmethod
    def _make_write_w_document(document_path, **data):
        from google.cloud.firestore_v1.proto import document_pb2
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1._helpers import encode_dict

        return write_pb2.Write(
            update=document_pb2.Document(name=document_path, fields=encode_dict(data))
        )

    @staticmethod
    def _make_write_w_transform(document_path, fields):
        from google.cloud.firestore_v1.proto import write_pb2
        from google.cloud.firestore_v1.gapic import enums

        server_val = enums.DocumentTransform.FieldTransform.ServerValue
        transforms = [
            write_pb2.DocumentTransform.FieldTransform(
                field_path=field, set_to_server_value=server_val.REQUEST_TIME
            )
            for field in fields
        ]

        return write_pb2.Write(
            transform=write_pb2.DocumentTransform(
                document=document_path, field_transforms=transforms
            )
        )

    @staticmethod
    def _update_document_mask(update_pb, field_paths):
        from google.cloud.firestore_v1.proto import common_pb2

        update_pb.update_mask.CopyFrom(
            common_pb2.DocumentMask(field_paths=sorted(field_paths))
        )

    def test_with_merge_true_wo_transform(self):
        document_path = _make_ref_string(u"little", u"town", u"of", u"ham")
        document_data = {"cheese": 1.5, "crackers": True}

        write_pbs = self._call_fut(document_path, document_data, merge=True)

        update_pb = self._make_write_w_document(document_path, **document_data)
        self._update_document_mask(update_pb, field_paths=sorted(document_data))
        expected_pbs = [update_pb]
        self.assertEqual(write_pbs, expected_pbs)

    def test_with_merge_field_wo_transform(self):
        document_path = _make_ref_string(u"little", u"town", u"of", u"ham")
        document_data = {"cheese": 1.5, "crackers": True}

        write_pbs = self._call_fut(document_path, document_data, merge=["cheese"])

        update_pb = self._make_write_w_document(
            document_path, cheese=document_data["cheese"]
        )
        self._update_document_mask(update_pb, field_paths=["cheese"])
        expected_pbs = [update_pb]
        self.assertEqual(write_pbs, expected_pbs)

    def test_with_merge_true_w_transform(self):
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP

        document_path = _make_ref_string(u"little", u"town", u"of", u"ham")
        update_data = {"cheese": 1.5, "crackers": True}
        document_data = update_data.copy()
        document_data["butter"] = SERVER_TIMESTAMP

        write_pbs = self._call_fut(document_path, document_data, merge=True)

        update_pb = self._make_write_w_document(document_path, **update_data)
        self._update_document_mask(update_pb, field_paths=sorted(update_data))
        transform_pb = self._make_write_w_transform(document_path, fields=["butter"])
        expected_pbs = [update_pb, transform_pb]
        self.assertEqual(write_pbs, expected_pbs)

    def test_with_merge_field_w_transform(self):
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP

        document_path = _make_ref_string(u"little", u"town", u"of", u"ham")
        update_data = {"cheese": 1.5, "crackers": True}
        document_data = update_data.copy()
        document_data["butter"] = SERVER_TIMESTAMP

        write_pbs = self._call_fut(
            document_path, document_data, merge=["cheese", "butter"]
        )

        update_pb = self._make_write_w_document(
            document_path, cheese=document_data["cheese"]
        )
        self._update_document_mask(update_pb, ["cheese"])
        transform_pb = self._make_write_w_transform(document_path, fields=["butter"])
        expected_pbs = [update_pb, transform_pb]
        self.assertEqual(write_pbs, expected_pbs)

    def test_with_merge_field_w_transform_masking_simple(self):
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP

        document_path = _make_ref_string(u"little", u"town", u"of", u"ham")
        update_data = {"cheese": 1.5, "crackers": True}
        document_data = update_data.copy()
        document_data["butter"] = {"pecan": SERVER_TIMESTAMP}

        write_pbs = self._call_fut(document_path, document_data, merge=["butter.pecan"])

        update_pb = self._make_write_w_document(document_path)
        transform_pb = self._make_write_w_transform(
            document_path, fields=["butter.pecan"]
        )
        expected_pbs = [update_pb, transform_pb]
        self.assertEqual(write_pbs, expected_pbs)

    def test_with_merge_field_w_transform_parent(self):
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP

        document_path = _make_ref_string(u"little", u"town", u"of", u"ham")
        update_data = {"cheese": 1.5, "crackers": True}
        document_data = update_data.copy()
        document_data["butter"] = {"popcorn": "yum", "pecan": SERVER_TIMESTAMP}

        write_pbs = self._call_fut(
            document_path, document_data, merge=["cheese", "butter"]
        )

        update_pb = self._make_write_w_document(
            document_path, cheese=update_data["cheese"], butter={"popcorn": "yum"}
        )
        self._update_document_mask(update_pb, ["cheese", "butter"])
        transform_pb = self._make_write_w_transform(
            document_path, fields=["butter.pecan"]
        )
        expected_pbs = [update_pb, transform_pb]
        self.assertEqual(write_pbs, expected_pbs)


class TestDocumentExtractorForUpdate(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1 import _helpers

        return _helpers.DocumentExtractorForUpdate

    def _make_one(self, document_data):
        return self._get_target_class()(document_data)

    def test_ctor_w_empty_document(self):
        document_data = {}

        inst = self._make_one(document_data)
        self.assertEqual(inst.top_level_paths, [])

    def test_ctor_w_simple_keys(self):
        document_data = {"a": 1, "b": 2, "c": 3}

        expected_paths = [
            _make_field_path("a"),
            _make_field_path("b"),
            _make_field_path("c"),
        ]
        inst = self._make_one(document_data)
        self.assertEqual(inst.top_level_paths, expected_paths)

    def test_ctor_w_nested_keys(self):
        document_data = {"a": {"d": {"e": 1}}, "b": {"f": 7}, "c": 3}

        expected_paths = [
            _make_field_path("a"),
            _make_field_path("b"),
            _make_field_path("c"),
        ]
        inst = self._make_one(document_data)
        self.assertEqual(inst.top_level_paths, expected_paths)

    def test_ctor_w_dotted_keys(self):
        document_data = {"a.d.e": 1, "b.f": 7, "c": 3}

        expected_paths = [
            _make_field_path("a", "d", "e"),
            _make_field_path("b", "f"),
            _make_field_path("c"),
        ]
        inst = self._make_one(document_data)
        self.assertEqual(inst.top_level_paths, expected_paths)

    def test_ctor_w_nested_dotted_keys(self):
        document_data = {"a.d.e": 1, "b.f": {"h.i": 9}, "c": 3}

        expected_paths = [
            _make_field_path("a", "d", "e"),
            _make_field_path("b", "f"),
            _make_field_path("c"),
        ]
        expected_set_fields = {"a": {"d": {"e": 1}}, "b": {"f": {"h.i": 9}}, "c": 3}
        inst = self._make_one(document_data)
        self.assertEqual(inst.top_level_paths, expected_paths)
        self.assertEqual(inst.set_fields, expected_set_fields)


class Test_pbs_for_update(unittest.TestCase):
    @staticmethod
    def _call_fut(document_path, field_updates, option):
        from google.cloud.firestore_v1._helpers import pbs_for_update

        return pbs_for_update(document_path, field_updates, option)

    def _helper(self, option=None, do_transform=False, **write_kwargs):
        from google.cloud.firestore_v1 import _helpers
        from google.cloud.firestore_v1.field_path import FieldPath
        from google.cloud.firestore_v1.transforms import SERVER_TIMESTAMP
        from google.cloud.firestore_v1.gapic import enums
        from google.cloud.firestore_v1.proto import common_pb2
        from google.cloud.firestore_v1.proto import document_pb2
        from google.cloud.firestore_v1.proto import write_pb2

        document_path = _make_ref_string(u"toy", u"car", u"onion", u"garlic")
        field_path1 = "bitez.yum"
        value = b"\x00\x01"
        field_path2 = "blog.internet"

        field_updates = {field_path1: value}
        if do_transform:
            field_updates[field_path2] = SERVER_TIMESTAMP

        write_pbs = self._call_fut(document_path, field_updates, option)

        map_pb = document_pb2.MapValue(fields={"yum": _value_pb(bytes_value=value)})

        field_paths = [field_path1]

        expected_update_pb = write_pb2.Write(
            update=document_pb2.Document(
                name=document_path, fields={"bitez": _value_pb(map_value=map_pb)}
            ),
            update_mask=common_pb2.DocumentMask(field_paths=field_paths),
            **write_kwargs
        )
        if isinstance(option, _helpers.ExistsOption):
            precondition = common_pb2.Precondition(exists=False)
            expected_update_pb.current_document.CopyFrom(precondition)
        expected_pbs = [expected_update_pb]
        if do_transform:
            transform_paths = FieldPath.from_string(field_path2)
            server_val = enums.DocumentTransform.FieldTransform.ServerValue
            expected_transform_pb = write_pb2.Write(
                transform=write_pb2.DocumentTransform(
                    document=document_path,
                    field_transforms=[
                        write_pb2.DocumentTransform.FieldTransform(
                            field_path=transform_paths.to_api_repr(),
                            set_to_server_value=server_val.REQUEST_TIME,
                        )
                    ],
                )
            )
            expected_pbs.append(expected_transform_pb)
        self.assertEqual(write_pbs, expected_pbs)

    def test_without_option(self):
        from google.cloud.firestore_v1.proto import common_pb2

        precondition = common_pb2.Precondition(exists=True)
        self._helper(current_document=precondition)

    def test_with_exists_option(self):
        from google.cloud.firestore_v1.client import _helpers

        option = _helpers.ExistsOption(False)
        self._helper(option=option)

    def test_update_and_transform(self):
        from google.cloud.firestore_v1.proto import common_pb2

        precondition = common_pb2.Precondition(exists=True)
        self._helper(current_document=precondition, do_transform=True)


class Test_pb_for_delete(unittest.TestCase):
    @staticmethod
    def _call_fut(document_path, option):
        from google.cloud.firestore_v1._helpers import pb_for_delete

        return pb_for_delete(document_path, option)

    def _helper(self, option=None, **write_kwargs):
        from google.cloud.firestore_v1.proto import write_pb2

        document_path = _make_ref_string(u"chicken", u"philly", u"one", u"two")
        write_pb = self._call_fut(document_path, option)

        expected_pb = write_pb2.Write(delete=document_path, **write_kwargs)
        self.assertEqual(write_pb, expected_pb)

    def test_without_option(self):
        self._helper()

    def test_with_option(self):
        from google.protobuf import timestamp_pb2
        from google.cloud.firestore_v1.proto import common_pb2
        from google.cloud.firestore_v1 import _helpers

        update_time = timestamp_pb2.Timestamp(seconds=1309700594, nanos=822211297)
        option = _helpers.LastUpdateOption(update_time)
        precondition = common_pb2.Precondition(update_time=update_time)
        self._helper(option=option, current_document=precondition)


class Test_get_transaction_id(unittest.TestCase):
    @staticmethod
    def _call_fut(transaction, **kwargs):
        from google.cloud.firestore_v1._helpers import get_transaction_id

        return get_transaction_id(transaction, **kwargs)

    def test_no_transaction(self):
        ret_val = self._call_fut(None)
        self.assertIsNone(ret_val)

    def test_invalid_transaction(self):
        from google.cloud.firestore_v1.transaction import Transaction

        transaction = Transaction(mock.sentinel.client)
        self.assertFalse(transaction.in_progress)
        with self.assertRaises(ValueError):
            self._call_fut(transaction)

    def test_after_writes_not_allowed(self):
        from google.cloud.firestore_v1._helpers import ReadAfterWriteError
        from google.cloud.firestore_v1.transaction import Transaction

        transaction = Transaction(mock.sentinel.client)
        transaction._id = b"under-hook"
        transaction._write_pbs.append(mock.sentinel.write)

        with self.assertRaises(ReadAfterWriteError):
            self._call_fut(transaction)

    def test_after_writes_allowed(self):
        from google.cloud.firestore_v1.transaction import Transaction

        transaction = Transaction(mock.sentinel.client)
        txn_id = b"we-are-0fine"
        transaction._id = txn_id
        transaction._write_pbs.append(mock.sentinel.write)

        ret_val = self._call_fut(transaction, read_operation=False)
        self.assertEqual(ret_val, txn_id)

    def test_good_transaction(self):
        from google.cloud.firestore_v1.transaction import Transaction

        transaction = Transaction(mock.sentinel.client)
        txn_id = b"doubt-it"
        transaction._id = txn_id
        self.assertTrue(transaction.in_progress)

        self.assertEqual(self._call_fut(transaction), txn_id)


class Test_metadata_with_prefix(unittest.TestCase):
    @staticmethod
    def _call_fut(database_string):
        from google.cloud.firestore_v1._helpers import metadata_with_prefix

        return metadata_with_prefix(database_string)

    def test_it(self):
        database_string = u"projects/prahj/databases/dee-bee"
        metadata = self._call_fut(database_string)

        self.assertEqual(metadata, [("google-cloud-resource-prefix", database_string)])


class TestWriteOption(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1._helpers import WriteOption

        return WriteOption

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_modify_write(self):
        option = self._make_one()
        with self.assertRaises(NotImplementedError):
            option.modify_write(None)


class TestLastUpdateOption(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1._helpers import LastUpdateOption

        return LastUpdateOption

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        option = self._make_one(mock.sentinel.timestamp)
        self.assertIs(option._last_update_time, mock.sentinel.timestamp)

    def test___eq___different_type(self):
        option = self._make_one(mock.sentinel.timestamp)
        other = object()
        self.assertFalse(option == other)

    def test___eq___different_timestamp(self):
        option = self._make_one(mock.sentinel.timestamp)
        other = self._make_one(mock.sentinel.other_timestamp)
        self.assertFalse(option == other)

    def test___eq___same_timestamp(self):
        option = self._make_one(mock.sentinel.timestamp)
        other = self._make_one(mock.sentinel.timestamp)
        self.assertTrue(option == other)

    def test_modify_write_update_time(self):
        from google.protobuf import timestamp_pb2
        from google.cloud.firestore_v1.proto import common_pb2
        from google.cloud.firestore_v1.proto import write_pb2

        timestamp_pb = timestamp_pb2.Timestamp(seconds=683893592, nanos=229362000)
        option = self._make_one(timestamp_pb)
        write_pb = write_pb2.Write()
        ret_val = option.modify_write(write_pb)

        self.assertIsNone(ret_val)
        expected_doc = common_pb2.Precondition(update_time=timestamp_pb)
        self.assertEqual(write_pb.current_document, expected_doc)


class TestExistsOption(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1._helpers import ExistsOption

        return ExistsOption

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        option = self._make_one(mock.sentinel.totes_bool)
        self.assertIs(option._exists, mock.sentinel.totes_bool)

    def test___eq___different_type(self):
        option = self._make_one(mock.sentinel.timestamp)
        other = object()
        self.assertFalse(option == other)

    def test___eq___different_exists(self):
        option = self._make_one(True)
        other = self._make_one(False)
        self.assertFalse(option == other)

    def test___eq___same_exists(self):
        option = self._make_one(True)
        other = self._make_one(True)
        self.assertTrue(option == other)

    def test_modify_write(self):
        from google.cloud.firestore_v1.proto import common_pb2
        from google.cloud.firestore_v1.proto import write_pb2

        for exists in (True, False):
            option = self._make_one(exists)
            write_pb = write_pb2.Write()
            ret_val = option.modify_write(write_pb)

            self.assertIsNone(ret_val)
            expected_doc = common_pb2.Precondition(exists=exists)
            self.assertEqual(write_pb.current_document, expected_doc)


def _value_pb(**kwargs):
    from google.cloud.firestore_v1.proto.document_pb2 import Value

    return Value(**kwargs)


def _make_ref_string(project, database, *path):
    from google.cloud.firestore_v1 import _helpers

    doc_rel_path = _helpers.DOCUMENT_PATH_DELIMITER.join(path)
    return u"projects/{}/databases/{}/documents/{}".format(
        project, database, doc_rel_path
    )


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_client(project="quark"):
    from google.cloud.firestore_v1.client import Client

    credentials = _make_credentials()
    return Client(project=project, credentials=credentials)


def _make_field_path(*fields):
    from google.cloud.firestore_v1 import field_path

    return field_path.FieldPath(*fields)
