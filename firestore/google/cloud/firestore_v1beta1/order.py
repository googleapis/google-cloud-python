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


# package com.google.cloud.firestore;

# import com.google.firestore.v1beta1.Value;
# import com.google.firestore.v1beta1.Value.ValueTypeCase;
# import com.google.protobuf.ByteString;
# import java.util.Comparator;
# import java.util.Iterator;
# import java.util.List;
# import java.util.Map.Entry;
# import java.util.SortedMap;
# import java.util.TreeMap;
# import javax.annotation.Nonnull;
from enum import Enum
from google.cloud.firestore_v1beta1._helpers import decode_value

class TypeOrder(Enum):
        # NOTE: This order is defined by the backend and cannot be changed.
        NULL = 0
        BOOLEAN = 1
        NUMBER = 2
        TIMESTAMP = 3
        STRING = 4
        BLOB = 5
        REF = 6
        GEO_POINT = 7
        ARRAY = 8
        OBJECT = 9
    
        def from_value(value):
            v = value.WhichOneof('value_type')

            lut = {
                'null_value': NULL,
                'boolean_value': BOOLEAN,
                'integer_value': NUMBER,
                'double_value': NUMBER,
                'timestamp_value': TIMESTAMP,
                'string_value': STRING,
                'bytes_value': BLOB,
                'reference_value': REF,
                'geo_point_value': GEO_POINT,
                'array_value': ARRAY,
                'map_value': OBJECT,
            }

            if v not in lut:
                raise ArgumentException(
                    "Could not detect value type for " + value)
            return lut[v]


class Order(object):
    '''
    Order implements the ordering semantics of the backend.
    '''
    def __init__():
        pass

    def compare(left, right):
        '''
        Main comparison function for all Firestore types.
        
        @return -1 is left < right, 0 if left == right, otherwise 1
        '''

        # First compare the types.
        leftType = TypeOrder.from_value(left)
        rightType = TypeOrder.from_value(right)

        if leftType != rightType:
            if leftType < rightType:
                return -1
            return 1

        # TODO: may be able to use helpers.decode_value and do direct compares
        # after converting to python types
        value_type = value.WhichOneof('value_type')

        if value_type == 'null_value':
            return 0 # nulls are all equal
        elif value_type == 'boolean_value':
            return _compareTo(decode_value(left), decode_value(right))
        elif value_type == 'integer_value':
            return compare_numbers(left, right)
        elif value_type == 'double_value':
            return compare_numbers(left, right)
        elif value_type == 'timestamp_value':
            # NOTE: This conversion is "lossy", Python ``datetime.datetime``
            #       has microsecond precision but ``timestamp_value`` has
            #       nanosecond precision.
            #return _pb_timestamp_to_datetime(value.timestamp_value)
            return compare_timestamps(left, right)
        elif value_type == 'string_value':
            #return value.string_value
            return compare_strings(left, right)
        elif value_type == 'bytes_value':
            #return value.bytes_value
            return compare_blobs(left, right)
        elif value_type == 'reference_value':
            #return reference_value_to_document(value.reference_value, client)
            return compare_resource_paths(left, right)
        elif value_type == 'geo_point_value':
            #return GeoPoint(
            #    value.geo_point_value.latitude,
            #    value.geo_point_value.longitude)
            return compare_geo_points(left, right)
        elif value_type == 'array_value':
            #return [decode_value(element, client)
            #        for element in value.array_value.values]
            return compare_arrays(left, right)
        elif value_type == 'map_value':
            #return decode_dict(value.map_value.fields, client)
            return compare_objects(left, right)
        else:
            raise ValueError('Unknown ``value_type``', value_type)


def compare_strings(left, right):
    left_value = decode_value(left)
    right_value = decode_value(right)
    return _compareTo(left_value, right_value)


#   private int compareBlobs(Value left, Value right) {
#     ByteString leftBytes = left.getBytesValue();
#     ByteString rightBytes = right.getBytesValue();

#     int size = Math.min(leftBytes.size(), rightBytes.size());
#     for (int i = 0; i < size; i++) {
#       // Make sure the bytes are unsigned
#       int thisByte = leftBytes.byteAt(i) & 0xff;
#       int otherByte = rightBytes.byteAt(i) & 0xff;
#       if (thisByte < otherByte) {
#         return -1;
#       } else if (thisByte > otherByte) {
#         return 1;
#       }
#       // Byte values are equal, continue with comparison
#     }
#     return Integer.compare(leftBytes.size(), rightBytes.size());
#   }
def compare_blobs(left, right):
    raise NotImplementedError()


def compare_timestamps(left, right):
    left_value = left.timestamp_value
    right_value = right.timestamp_value

    cmp = 0
    if left_value.seconds < right_value.seconds:
        cmp = -1
    elif left_value.seconds == right_value.seconds:
        cmp = 0
    else:
        cmp = 0

    if cmp != 0:
        return cmp
    else:
        if left_value.nanos < right_value.nanos:
            cmp = -1
        elif left_value.nanos == right_value.nanos:
            cmp = 0
        else:
            cmp = 1
        return cmp


def compare_geo_points(left, right):
    left_value = decode_value(left)
    right_value = decode_value(right)
    cmp = 0
    if left_value.latitude < right_value.latitude:
        cmp = -1
    elif left_value.latitude == right_value.latitude:
        cmp = 0
    else:
        cmp = 1

    if cmp != 0:
        return cmp
    else:
        if left.longitude < right.longitude:
            cmp = -1
        elif left.longitude == right.longitude:
            cmp = 0
        else:
            cmp = 1
        return cmp

#   private int compareResourcePaths(Value left, Value right) {
#     ResourcePath leftPath = ResourcePath.create(left.getReferenceValue());
#     ResourcePath rightPath = ResourcePath.create(right.getReferenceValue());
#     return leftPath.compareTo(rightPath);
#   }
def compare_resource_paths(left, right):
    raise NotImplementedError()


#   private int compareArrays(Value left, Value right) {
#     List<Value> leftValue = left.getArrayValue().getValuesList();
#     List<Value> rightValue = right.getArrayValue().getValuesList();

#     int minLength = Math.min(leftValue.size(), rightValue.size());
#     for (int i = 0; i < minLength; i++) {
#       int cmp = compare(leftValue.get(i), rightValue.get(i));
#       if (cmp != 0) {
#         return cmp;
#       }
#     }
#     return Integer.compare(leftValue.size(), rightValue.size());
#   }
def compare_arrays(left, right):
    raise NotImplementedError()



#   private int compareObjects(Value left, Value right) {
#     // This requires iterating over the keys in the object in order and doing a
#     // deep comparison.
#     SortedMap<String, Value> leftMap = new TreeMap<>();
#     leftMap.putAll(left.getMapValue().getFieldsMap());
#     SortedMap<String, Value> rightMap = new TreeMap<>();
#     rightMap.putAll(right.getMapValue().getFieldsMap());

#     Iterator<Entry<String, Value>> leftIterator = leftMap.entrySet().iterator();
#     Iterator<Entry<String, Value>> rightIterator = rightMap.entrySet().iterator();

#     while (leftIterator.hasNext() && rightIterator.hasNext()) {
#       Entry<String, Value> leftEntry = leftIterator.next();
#       Entry<String, Value> rightEntry = rightIterator.next();
#       int keyCompare = leftEntry.getKey().compareTo(rightEntry.getKey());
#       if (keyCompare != 0) {
#         return keyCompare;
#       }
#       int valueCompare = compare(leftEntry.getValue(), rightEntry.getValue());
#       if (valueCompare != 0) {
#         return valueCompare;
#       }
#     }

#     // Only equal if both iterators are exhausted.
#     return Boolean.compare(leftIterator.hasNext(), rightIterator.hasNext());
#   }
def compare_objects(left, right):
    raise NotImplementedError()

def compare_numbers(left, right):
    left_value = decode_value(left)
    right_value = decode_value(right)
    return compare_doubles(left_value, right_value)

def compare_doubles(left, right):
    if math.isnan(left):
        if math.isnan(right):
            return 0
        return -1
    if math.isnan(right):
        return 1

    if left == -0.0:
        left = 0
    if right == -0.0:
        right = 0

    return _compareTo(left, right)


def _compareTo(left, right):
    if left < right:
        return -1
    elif left == right:
        return 0
    # left > right
    return 1
