# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrappers for protocol buffer enum types."""

import enum


class Span(object):
    class SpanKind(enum.IntEnum):
        """
        Type of span. Can be used to specify additional relationships between spans
        in addition to a parent/child relationship.

        Attributes:
          SPAN_KIND_UNSPECIFIED (int): Unspecified. Do NOT use as default.
          Implementations MAY assume SpanKind.INTERNAL to be default.
          INTERNAL (int): Indicates that the span is used internally. Default value.
          SERVER (int): Indicates that the span covers server-side handling of an RPC or other
          remote network request.
          CLIENT (int): Indicates that the span covers the client-side wrapper around an RPC or
          other remote request.
          PRODUCER (int): Indicates that the span describes producer sending a message to a broker.
          Unlike client and  server, there is no direct critical path latency
          relationship between producer and consumer spans (e.g. publishing a
          message to a pubsub service).
          CONSUMER (int): Indicates that the span describes consumer receiving a message from a
          broker. Unlike client and  server, there is no direct critical path
          latency relationship between producer and consumer spans (e.g. receiving
          a message from a pubsub service subscription).
        """

        SPAN_KIND_UNSPECIFIED = 0
        INTERNAL = 1
        SERVER = 2
        CLIENT = 3
        PRODUCER = 4
        CONSUMER = 5

    class TimeEvent(object):
        class MessageEvent(object):
            class Type(enum.IntEnum):
                """
                Indicates whether the message was sent or received.

                Attributes:
                  TYPE_UNSPECIFIED (int): Unknown event type.
                  SENT (int): Indicates a sent message.
                  RECEIVED (int): Indicates a received message.
                """

                TYPE_UNSPECIFIED = 0
                SENT = 1
                RECEIVED = 2

    class Link(object):
        class Type(enum.IntEnum):
            """
            The relationship of the current span relative to the linked span: child,
            parent, or unspecified.

            Attributes:
              TYPE_UNSPECIFIED (int): The relationship of the two spans is unknown.
              CHILD_LINKED_SPAN (int): The linked span is a child of the current span.
              PARENT_LINKED_SPAN (int): The linked span is a parent of the current span.
            """

            TYPE_UNSPECIFIED = 0
            CHILD_LINKED_SPAN = 1
            PARENT_LINKED_SPAN = 2
