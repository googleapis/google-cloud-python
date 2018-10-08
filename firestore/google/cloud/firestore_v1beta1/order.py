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
import math

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
                'null_value': TypeOrder.NULL,
                'boolean_value': TypeOrder.BOOLEAN,
                'integer_value': TypeOrder.NUMBER,
                'double_value': TypeOrder.NUMBER,
                'timestamp_value': TypeOrder.TIMESTAMP,
                'string_value': TypeOrder.STRING,
                'bytes_value': TypeOrder.BLOB,
                'reference_value': TypeOrder.REF,
                'geo_point_value': TypeOrder.GEO_POINT,
                'array_value': TypeOrder.ARRAY,
                'map_value': TypeOrder.OBJECT,
            }

            if v not in lut:
                raise ArgumentException(
                    "Could not detect value type for " + value)
            return lut[v]


class Order(object):
    '''
    Order implements the ordering semantics of the backend.
    '''
    def __init__(self):
        pass
    
    def compare(self, left, right):
        '''
        Main comparison function for all Firestore types.
        
        @return -1 is left < right, 0 if left == right, otherwise 1
        '''

        # First compare the types.
        leftType = TypeOrder.from_value(left).value
        rightType = TypeOrder.from_value(right).value

        if leftType != rightType:
            if leftType < rightType:
                return -1
            return 1

        # TODO: may be able to use helpers.decode_value and do direct compares
        # after converting to python types
        value_type = left.WhichOneof('value_type')

        if value_type == 'null_value':
            return 0  # nulls are all equal
        elif value_type == 'boolean_value':
            return self._compareTo(left.boolean_value, right.boolean_value)
        elif value_type == 'integer_value':
            return self.compare_numbers(left, right)
        elif value_type == 'double_value':
            return self.compare_numbers(left, right)
        elif value_type == 'timestamp_value':
            return self.compare_timestamps(left, right)
        elif value_type == 'string_value':
            return self._compareTo(left.string_value, right.string_value)
        elif value_type == 'bytes_value':
            return self.compare_blobs(left, right)
        elif value_type == 'reference_value':
            return self.compare_resource_paths(left, right)
        elif value_type == 'geo_point_value':
            return self.compare_geo_points(left, right)
        elif value_type == 'array_value':
            return self.compare_arrays(left, right)
        elif value_type == 'map_value':
            return self.compare_objects(left, right)
        else:
            raise ValueError('Unknown ``value_type``', value_type)


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
    @staticmethod
    def compare_blobs(left, right):
        left_bytes = left.bytes_value
        right_bytes = right.bytes_value
        
        # TODO: verify this is okay. python can compare bytes so *shrugs*
        return Order._compareTo(left_bytes, right_bytes)

    @staticmethod
    def compare_timestamps(left, right):
        left = left.timestamp_value
        right = right.timestamp_value

        seconds = Order._compareTo(left.seconds or 0, right.seconds or 0)
        if seconds != 0:
            return seconds
        
        return Order._compareTo(left.nanos or 0, right.nanos or 0)

        # cmp = 0
        # if left_value.seconds < right_value.seconds:
        #     cmp = -1
        # elif left_value.seconds == right_value.seconds:
        #     cmp = 0
        # else:
        #     cmp = 0

        # if cmp != 0:
        #     return cmp
        # else:
        #     if left_value.nanos < right_value.nanos:
        #         cmp = -1
        #     elif left_value.nanos == right_value.nanos:
        #         cmp = 0
        #     else:
        #         cmp = 1
        #     return cmp

    @staticmethod
    def compare_geo_points(left, right):
        left_value = decode_value(left, None)
        right_value = decode_value(right, None)
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
            if left_value.longitude < right_value.longitude:
                cmp = -1
            elif left_value.longitude == right_value.longitude:
                cmp = 0
            else:
                cmp = 1
            return cmp

    #   private int compareResourcePaths(Value left, Value right) {
    #     ResourcePath leftPath = ResourcePath.create(left.getReferenceValue());
    #     ResourcePath rightPath = ResourcePath.create(right.getReferenceValue());
    #     return leftPath.compareTo(rightPath);
    #   }
    @staticmethod
    def compare_resource_paths(left, right):
        """
        compareTo(other: Path<T>): number {
        const len = Math.min(left.segments.length, right.segments.length);
        for (let i = 0; i < len; i++) {
        if (left.segments[i] < right.segments[i]) {
            return -1;
        }
        if (left.segments[i] > right.segments[i]) {
            return 1;
        }
        }
        if (left.segments.length < right.segments.length) {
        return -1;
        }
        if (left.segments.length > right.segments.length) {
        return 1;
        }
        return 0;
    }
    """ 
        left = left.reference_value
        right = right.reference_value


        left_segments = left.split('/')
        right_segments = right.split('/')
        shorter = min(len(left_segments), len(right_segments))
        # compare segments
        for i in range(shorter):
            if (left_segments[i] < right_segments[i]):
                return -1
            
            if (left_segments[i] > right_segments[i]):
                return 1
            


        left_length = len(left)
        right_length = len(right)
        if left_length < right_length:
            return -1
        if left_length > right_length:
            return 1

        return 0


    @staticmethod
    def compare_arrays(left, right):
        l_values = left.array_value.values#.keys()
        r_values = right.array_value.values#.keys()

        length = min(len(l_values), len(r_values))
        for i in range(length):
            cmp = Order().compare(l_values[i], r_values[i])
            if cmp != 0:
                return cmp
            
        return Order._compareTo(len(l_values), len(r_values))


    @staticmethod
    def compare_objects(left, right):
        left_fields = left.map_value.fields
        right_fields = right.map_value.fields

        l_iter = left_fields.__iter__()
        r_iter = right_fields.__iter__()
        try:
            while True:
                left_key = l_iter.__next__()
                right_key = r_iter.__next__()
                
                keyCompare = Order._compareTo(left_key, right_key)
                if keyCompare != 0:
                    return keyCompare

                value_compare = Order().compare(
                    left_fields[left_key], right_fields[right_key])
                if value_compare != 0:
                    return value_compare
        except StopIteration:
            pass
            
        return Order._compareTo(len(left_fields), len(right_fields))

    @staticmethod
    def compare_numbers(left, right):
        left_value = decode_value(left, None)
        right_value = decode_value(right, None)
        return Order.compare_doubles(left_value, right_value)

    @staticmethod
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

        return Order._compareTo(left, right)

    @staticmethod
    def _compareTo(left, right):
        if left < right:
            return -1
        elif left == right:
            return 0
        # left > right
        return 1
