# Copyright 2016 Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Wrappers for protocol buffer enum types."""


class TraceSpan(object):
    class SpanKind(object):
        """
        Type of span. Can be used to specify additional relationships between spans
        in addition to a parent/child relationship.

        Attributes:
          SPAN_KIND_UNSPECIFIED (int): Unspecified.
          RPC_SERVER (int): Indicates that the span covers server-side handling of an RPC or other
            remote network request.
          RPC_CLIENT (int): Indicates that the span covers the client-side wrapper around an RPC or
            other remote request.
        """
        SPAN_KIND_UNSPECIFIED = 0
        RPC_SERVER = 1
        RPC_CLIENT = 2


class ListTracesRequest(object):
    class ViewType(object):
        """
        Type of data returned for traces in the list.

        Attributes:
          VIEW_TYPE_UNSPECIFIED (int): Default is ``MINIMAL`` if unspecified.
          MINIMAL (int): Minimal view of the trace record that contains only the project
            and trace IDs.
          ROOTSPAN (int): Root span view of the trace record that returns the root spans along
            with the minimal trace data.
          COMPLETE (int): Complete view of the trace record that contains the actual trace data.
            This is equivalent to calling the REST ``get`` or RPC ``GetTrace`` method
            using the ID of each listed trace.
        """
        VIEW_TYPE_UNSPECIFIED = 0
        MINIMAL = 1
        ROOTSPAN = 2
        COMPLETE = 3
