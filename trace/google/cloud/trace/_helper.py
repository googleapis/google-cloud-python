# Copyright 2017 Google Inc.
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

from google.cloud.proto.devtools.cloudtrace.v1.trace_pb2 import (
    TraceSpan, Trace, Traces)
from google.protobuf.json_format import ParseDict


def _trace_mapping_to_pb(trace_mapping):
    """Helper for converting trace mapping to pb,
    Performs "impedance matching" between the protobuf attrs and
    the keys expected in the JSON API.

    :type trace_mapping: dict
    :param trace_mapping: The trace dict.

    :rtype: :class: `~google.cloud.proto.devtools.cloudtrace.v1.
                      trace_pb2.Trace`
    :returns: The Trace protobuf instance.
    """
    trace_pb = Trace()
    ParseDict(trace_mapping, trace_pb)
    return trace_pb


def _span_mapping_to_pb(span_mapping):
    """Helper for converting span mapping to pb,
    Performs "impedance matching" between the protobuf attrs and
    the keys expected in the JSON API.

    :type span_mapping: dict
    :param span_mapping: The span dict.

    :rtype: :class: `~google.cloud.proto.devtools.cloudtrace.v1.
                      trace_pb2.TraceSpan`
    :returns: The TraceSpan protobuf instance.
    """
    span_pb = TraceSpan()
    ParseDict(span_mapping, span_pb)
    return span_pb


def _traces_mapping_to_pb(traces_mapping):
    """Convert a trace dict to protobuf.

    :type traces_mapping: dict
    :param traces_mapping: A trace mapping.

    :rtype: class:`google.cloud.proto.devtools.cloudtrace.v1.trace_pb2.Traces`
    :return: The converted protobuf type traces.
    """
    traces_pb = Traces()
    ParseDict(traces_mapping, traces_pb)
    return traces_pb
