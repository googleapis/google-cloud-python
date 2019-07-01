# Copyright 2017, Google LLC All rights reserved.
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
import time

import mock
import pytz
from six.moves import queue
from google.protobuf import timestamp_pb2

from google.api_core import datetime_helpers
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber import message
from google.cloud.pubsub_v1.subscriber._protocol import requests


RECEIVED = datetime.datetime(2012, 4, 21, 15, 0, tzinfo=pytz.utc)
RECEIVED_SECONDS = datetime_helpers.to_milliseconds(RECEIVED) // 1000
PUBLISHED_MICROS = 123456
PUBLISHED = RECEIVED + datetime.timedelta(days=1, microseconds=PUBLISHED_MICROS)
PUBLISHED_SECONDS = datetime_helpers.to_milliseconds(PUBLISHED) // 1000


def create_message(data, ack_id="ACKID", autolease=True, **attrs):
    with mock.patch.object(message.Message, "lease") as lease:
        with mock.patch.object(time, "time") as time_:
            time_.return_value = RECEIVED_SECONDS
            msg = message.Message(
                types.PubsubMessage(
                    attributes=attrs,
                    data=data,
                    message_id="message_id",
                    publish_time=timestamp_pb2.Timestamp(
                        seconds=PUBLISHED_SECONDS, nanos=PUBLISHED_MICROS * 1000
                    ),
                ),
                ack_id,
                queue.Queue(),
                autolease=autolease,
            )
            if autolease:
                lease.assert_called_once_with()
            else:
                lease.assert_not_called()
            return msg


def test_attributes():
    msg = create_message(b"foo", baz="bacon", spam="eggs")
    assert msg.attributes == {"baz": "bacon", "spam": "eggs"}


def test_data():
    msg = create_message(b"foo")
    assert msg.data == b"foo"


def test_size():
    msg = create_message(b"foo")
    assert msg.size == 30  # payload + protobuf overhead


def test_ack_id():
    ack_id = "MY-ACK-ID"
    msg = create_message(b"foo", ack_id=ack_id)
    assert msg.ack_id == ack_id


def test_publish_time():
    msg = create_message(b"foo")
    assert msg.publish_time == PUBLISHED


def test_disable_autolease_on_creation():
    # the create_message() helper does the actual assertion
    create_message(b"foo", autolease=False)


def check_call_types(mock, *args, **kwargs):
    """Checks a mock's call types.

    Args:
        mock: The mock to check.
        args: The types of the positional arguments.
        kwargs: The names of the keyword args to check and their respective
            types.

    Raises:
        AssertionError: if any of the types don't match, or if the number of
            arguments does not match.
    """
    for call in mock.mock_calls:
        _, call_args, call_kwargs = call
        assert len(call_args) == len(args)
        for n, argtype in enumerate(args):
            assert isinstance(call_args[n], argtype)
        for argname, argtype in kwargs:
            assert argname in call_kwargs
            assert isinstance(call_kwargs[argname], argtype)


def test_ack():
    msg = create_message(b"foo", ack_id="bogus_ack_id")
    with mock.patch.object(msg._request_queue, "put") as put:
        msg.ack()
        put.assert_called_once_with(
            requests.AckRequest(
                ack_id="bogus_ack_id", byte_size=30, time_to_ack=mock.ANY
            )
        )
        check_call_types(put, requests.AckRequest)


def test_drop():
    msg = create_message(b"foo", ack_id="bogus_ack_id")
    with mock.patch.object(msg._request_queue, "put") as put:
        msg.drop()
        put.assert_called_once_with(
            requests.DropRequest(ack_id="bogus_ack_id", byte_size=30)
        )
        check_call_types(put, requests.DropRequest)


def test_lease():
    msg = create_message(b"foo", ack_id="bogus_ack_id")
    with mock.patch.object(msg._request_queue, "put") as put:
        msg.lease()
        put.assert_called_once_with(
            requests.LeaseRequest(ack_id="bogus_ack_id", byte_size=30)
        )
        check_call_types(put, requests.LeaseRequest)


def test_modify_ack_deadline():
    msg = create_message(b"foo", ack_id="bogus_ack_id")
    with mock.patch.object(msg._request_queue, "put") as put:
        msg.modify_ack_deadline(60)
        put.assert_called_once_with(
            requests.ModAckRequest(ack_id="bogus_ack_id", seconds=60)
        )
        check_call_types(put, requests.ModAckRequest)


def test_nack():
    msg = create_message(b"foo", ack_id="bogus_ack_id")
    with mock.patch.object(msg._request_queue, "put") as put:
        msg.nack()
        put.assert_called_once_with(
            requests.NackRequest(ack_id="bogus_ack_id", byte_size=30)
        )
        check_call_types(put, requests.NackRequest)


def test_repr():
    data = b"foo"
    msg = create_message(data, snow="cones", orange="juice")
    data_line = "  data: {!r}".format(data)
    expected_repr = "\n".join(
        (
            "Message {",
            data_line,
            "  attributes: {",
            '    "orange": "juice",',
            '    "snow": "cones"',
            "  }",
            "}",
        )
    )
    assert repr(msg) == expected_repr
