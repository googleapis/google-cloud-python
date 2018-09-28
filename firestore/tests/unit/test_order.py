# Copyright 2017 Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import mock
from google.cloud.firestore_v1beta1._helpers import encode_value
from google.protobuf import timestamp_pb2
from google.type import latlng_pb2
import math


class TestOrder(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1beta1.order import Order

        return Order

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_order(self):
        
        int_max_value = 10 ** 1000
        int_min_value = -10 ** 1000
        float_min_value = -10.0 ** 1000
        float_nan = float('nan')

        groups = [None] * 65

        groups[0] = [nullValue()]

        groups[1] = [_booleanValue(False)]
        groups[2] = [_booleanValue(True)]

        # numbers
        groups[3] = [_doubleValue(float_nan), _doubleValue(float_nan)]
        groups[4] = [_doubleValue(-math.inf)]
        groups[5] = [_intValue(int_min_value - 1)]
        groups[6] = [_intValue(int_min_value)]
        groups[7] = [_doubleValue(-1.1)]
        # Integers and Doubles order the same.
        groups[8] = [_intValue(-1), _doubleValue(-1.0)]
        groups[9] = [_doubleValue(-float_min_value)]
        # zeros all compare the same.
        groups[10] = [_intValue(0), _doubleValue(-0.0),
                      _doubleValue(0.0), _doubleValue(+0.0)]
        groups[11] = [_doubleValue(float_min_value)]
        groups[12] = [_intValue(1), _doubleValue(1.0)]
        groups[13] = [_doubleValue(1.1)]
        groups[14] = [_intValue(int_max_value)]
        groups[15] = [_intValue(int_max_value + 1)]
        groups[16] = [_doubleValue(math.inf)]

        groups[17] = [_timestampValue(123, 0)]
        groups[18] = [_timestampValue(123, 123)]
        groups[19] = [_timestampValue(345, 0)]

        # strings
        groups[20] = [_stringValue("")]
        groups[21] = [_stringValue("\u0000\ud7ff\ue000\uffff")]
        groups[22] = [_stringValue("(╯°□°）╯︵ ┻━┻")]
        groups[23] = [_stringValue("a")]
        groups[24] = [_stringValue("abc def")]
        # latin small letter e + combining acute accent + latin small letter b
        groups[25] = [_stringValue("e\u0301b")]
        groups[26] = [_stringValue("æ")]
        # latin small letter e with acute accent + latin small letter a
        groups[27] = [_stringValue("\u00e9a")]

        # blobs
        groups[28] = [_blobValue(bytes())]
        groups[29] = [_blobValue(bytes([0]))]
        groups[30] = [_blobValue(bytes([0, 1, 2, 3, 4]))]
        groups[31] = [_blobValue(bytes([0, 1, 2, 4, 3]))]
        groups[32] = [_blobValue(bytes([127]))]

        # resource names
        groups[33] = [
            _referenceValue("projects/p1/databases/d1/documents/c1/doc1")]
        groups[34] = [
            _referenceValue("projects/p1/databases/d1/documents/c1/doc2")]
        groups[35] = [
            _referenceValue(
                "projects/p1/databases/d1/documents/c1/doc2/c2/doc1")]
        groups[36] = [
            _referenceValue(
                "projects/p1/databases/d1/documents/c1/doc2/c2/doc2")]
        groups[37] = [
            _referenceValue("projects/p1/databases/d1/documents/c10/doc1")]
        groups[38] = [
            _referenceValue("projects/p1/databases/d1/documents/c2/doc1")]
        groups[39] = [
            _referenceValue("projects/p2/databases/d2/documents/c1/doc1")]
        groups[40] = [
            _referenceValue("projects/p2/databases/d2/documents/c1-/doc1")]
        groups[41] = [
            _referenceValue("projects/p2/databases/d3/documents/c1-/doc1")]

        # geo points
        groups[42] = [_geoPointValue(-90, -180)]
        groups[43] = [_geoPointValue(-90, 0)]
        groups[44] = [_geoPointValue(-90, 180)]
        groups[45] = [_geoPointValue(0, -180)]
        groups[46] = [_geoPointValue(0, 0)]
        groups[47] = [_geoPointValue(0, 180)]
        groups[48] = [_geoPointValue(1, -180)]
        groups[49] = [_geoPointValue(1, 0)]
        groups[50] = [_geoPointValue(1, 180)]
        groups[51] = [_geoPointValue(90, -180)]
        groups[52] = [_geoPointValue(90, 0)]
        groups[53] = [_geoPointValue(90, 180)]

        # arrays
        groups[54] = [_arrayValue()]
        groups[55] = [_arrayValue(_stringValue("bar"))]
        groups[56] = [_arrayValue(_stringValue("foo"))]
        groups[57] = [_arrayValue(_stringValue("foo"), _intValue(0))]
        groups[58] = [_arrayValue(_stringValue("foo"), _intValue(1))]
        groups[59] = [_arrayValue(_stringValue("foo"), _stringValue("0"))]

        # objects
        groups[60] = [_objectValue({"bar": _intValue(0)})]
        groups[61] = [_objectValue({
            "bar": _intValue(0),
            "foo": _intValue(1)
        })]
        groups[62] = [_objectValue({"bar": _intValue(1)})]
        groups[63] = [_objectValue({"bar": _intValue(2)})]
        groups[64] = [_objectValue({"bar": _stringValue("0")})]

        target = self._make_one()
        for left in groups:
            for right in groups:
                for i in groups[left]:
                    for j in groups[right]:
                        self.assertEqual(
                            _compare(left, right),
                            _compare(
                                target.compare(
                                    groups[left][i],
                                    groups[right][j]), 0),
                            "Order does not match for: groups[%d][%d] "
                            "and groups[%d][%d]".format(left, i, right, j)
                        )


def _compare(left, right):
    if left < right:
        return -1
    elif left == right:
        return 0
    return 1


def _booleanValue(b):
    return encode_value(b)


def _doubleValue(d):
    return encode_value(d)


def _intValue(l):
    return encode_value(l)


def _stringValue(s):
    return encode_value(s)


def _referenceValue(r):
    return encode_value(r)


def _blobValue(b):
    return encode_value(b)


def nullValue():
    return encode_value(None)


def _timestampValue(seconds, nanos):
    return timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)


def _geoPointValue(latitude, longitude):
    return latlng_pb2.LatLng(latitude=latitude,
                             longitude=longitude)


def _arrayValue(values):
    return encode_value(values)


def _objectValue(keysAndValues):
    return encode_value(keysAndValues)
