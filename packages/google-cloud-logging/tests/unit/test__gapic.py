# Copyright 2016 Google LLC
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

import unittest

from google.api_core import grpc_helpers
import google.auth.credentials
from google.protobuf import empty_pb2
import mock

import google.cloud.logging
from google.cloud.logging import _gapic
from google.cloud.logging_v2.gapic import config_service_v2_client
from google.cloud.logging_v2.gapic import logging_service_v2_client
from google.cloud.logging_v2.gapic import metrics_service_v2_client
from google.cloud.logging_v2.proto import log_entry_pb2
from google.cloud.logging_v2.proto import logging_pb2
from google.cloud.logging_v2.proto import logging_config_pb2
from google.cloud.logging_v2.proto import logging_metrics_pb2


PROJECT = "PROJECT"
PROJECT_PATH = "projects/%s" % (PROJECT,)
FILTER = "logName:syslog AND severity>=ERROR"


class Test_LoggingAPI(object):
    LOG_NAME = "log_name"
    LOG_PATH = "projects/%s/logs/%s" % (PROJECT, LOG_NAME)

    @staticmethod
    def make_logging_api():
        channel = grpc_helpers.ChannelStub()
        gapic_client = logging_service_v2_client.LoggingServiceV2Client(channel=channel)
        handwritten_client = mock.Mock()
        api = _gapic._LoggingAPI(gapic_client, handwritten_client)
        return channel, api

    def test_ctor(self):
        channel = grpc_helpers.ChannelStub()
        gapic_client = logging_service_v2_client.LoggingServiceV2Client(channel=channel)
        api = _gapic._LoggingAPI(gapic_client, mock.sentinel.client)
        assert api._gapic_api is gapic_client
        assert api._client is mock.sentinel.client

    def test_list_entries(self):
        channel, api = self.make_logging_api()

        log_entry_msg = log_entry_pb2.LogEntry(
            log_name=self.LOG_PATH, text_payload="text"
        )
        channel.ListLogEntries.response = logging_pb2.ListLogEntriesResponse(
            entries=[log_entry_msg]
        )
        result = api.list_entries([PROJECT], FILTER, google.cloud.logging.DESCENDING)

        entries = list(result)

        # Check the response
        assert len(entries) == 1
        entry = entries[0]
        assert isinstance(entry, google.cloud.logging.entries.TextEntry)
        assert entry.payload == "text"

        # Check the request
        assert len(channel.ListLogEntries.requests) == 1
        request = channel.ListLogEntries.requests[0]
        assert request.project_ids == [PROJECT]
        assert request.filter == FILTER
        assert request.order_by == google.cloud.logging.DESCENDING

    def test_list_entries_with_options(self):
        channel, api = self.make_logging_api()

        channel.ListLogEntries.response = logging_pb2.ListLogEntriesResponse(entries=[])

        result = api.list_entries(
            [PROJECT],
            FILTER,
            google.cloud.logging.ASCENDING,
            page_size=42,
            page_token="token",
        )

        list(result)

        # Check the request
        assert len(channel.ListLogEntries.requests) == 1
        request = channel.ListLogEntries.requests[0]
        assert request.project_ids == [PROJECT]
        assert request.filter == FILTER
        assert request.order_by == google.cloud.logging.ASCENDING
        assert request.page_size == 42
        assert request.page_token == "token"

    def test_write_entries_single(self):
        channel, api = self.make_logging_api()

        channel.WriteLogEntries.response = empty_pb2.Empty()

        entry = {
            "logName": self.LOG_PATH,
            "resource": {"type": "global"},
            "textPayload": "text",
        }

        api.write_entries([entry])

        # Check the request
        assert len(channel.WriteLogEntries.requests) == 1
        request = channel.WriteLogEntries.requests[0]
        assert request.partial_success is False
        assert len(request.entries) == 1
        assert request.entries[0].log_name == entry["logName"]
        assert request.entries[0].resource.type == entry["resource"]["type"]
        assert request.entries[0].text_payload == "text"

    def test_logger_delete(self):
        channel, api = self.make_logging_api()

        channel.DeleteLog.response = empty_pb2.Empty()

        api.logger_delete(PROJECT, self.LOG_NAME)

        assert len(channel.DeleteLog.requests) == 1
        request = channel.DeleteLog.requests[0]
        assert request.log_name == self.LOG_PATH


class Test_SinksAPI(object):
    SINK_NAME = "sink_name"
    SINK_PATH = "projects/%s/sinks/%s" % (PROJECT, SINK_NAME)
    DESTINATION_URI = "faux.googleapis.com/destination"
    SINK_WRITER_IDENTITY = "serviceAccount:project-123@example.com"

    @staticmethod
    def make_sinks_api():
        channel = grpc_helpers.ChannelStub()
        gapic_client = config_service_v2_client.ConfigServiceV2Client(channel=channel)
        handwritten_client = mock.Mock()
        api = _gapic._SinksAPI(gapic_client, handwritten_client)
        return channel, api

    def test_ctor(self):
        channel = grpc_helpers.ChannelStub()
        gapic_client = config_service_v2_client.ConfigServiceV2Client(channel=channel)
        api = _gapic._SinksAPI(gapic_client, mock.sentinel.client)
        assert api._gapic_api is gapic_client
        assert api._client is mock.sentinel.client

    def test_list_sinks(self):
        channel, api = self.make_sinks_api()

        sink_msg = logging_config_pb2.LogSink(
            name=self.SINK_PATH, destination=self.DESTINATION_URI, filter=FILTER
        )
        channel.ListSinks.response = logging_config_pb2.ListSinksResponse(
            sinks=[sink_msg]
        )

        result = api.list_sinks(PROJECT)
        sinks = list(result)

        # Check the response
        assert len(sinks) == 1
        sink = sinks[0]
        assert isinstance(sink, google.cloud.logging.sink.Sink)
        assert sink.name == self.SINK_PATH
        assert sink.destination == self.DESTINATION_URI
        assert sink.filter_ == FILTER

        # Check the request
        assert len(channel.ListSinks.requests) == 1
        request = channel.ListSinks.requests[0]
        assert request.parent == PROJECT_PATH

    def test_list_sinks_with_options(self):
        channel, api = self.make_sinks_api()

        channel.ListSinks.response = logging_config_pb2.ListSinksResponse(sinks=[])

        result = api.list_sinks(PROJECT, page_size=42, page_token="token")
        list(result)

        # Check the request
        assert len(channel.ListSinks.requests) == 1
        request = channel.ListSinks.requests[0]
        assert request.parent == "projects/%s" % PROJECT
        assert request.page_size == 42
        assert request.page_token == "token"

    def test_sink_create(self):
        channel, api = self.make_sinks_api()

        channel.CreateSink.response = logging_config_pb2.LogSink(
            name=self.SINK_NAME,
            destination=self.DESTINATION_URI,
            filter=FILTER,
            writer_identity=self.SINK_WRITER_IDENTITY,
        )

        result = api.sink_create(
            PROJECT,
            self.SINK_NAME,
            FILTER,
            self.DESTINATION_URI,
            unique_writer_identity=True,
        )

        # Check response
        assert result == {
            "name": self.SINK_NAME,
            "filter": FILTER,
            "destination": self.DESTINATION_URI,
            "writerIdentity": self.SINK_WRITER_IDENTITY,
        }

        # Check request
        assert len(channel.CreateSink.requests) == 1
        request = channel.CreateSink.requests[0]
        assert request.parent == PROJECT_PATH
        assert request.unique_writer_identity is True
        assert request.sink.name == self.SINK_NAME
        assert request.sink.filter == FILTER
        assert request.sink.destination == self.DESTINATION_URI

    def test_sink_get(self):
        channel, api = self.make_sinks_api()

        channel.GetSink.response = logging_config_pb2.LogSink(
            name=self.SINK_PATH, destination=self.DESTINATION_URI, filter=FILTER
        )

        response = api.sink_get(PROJECT, self.SINK_NAME)

        # Check response
        assert response == {
            "name": self.SINK_PATH,
            "filter": FILTER,
            "destination": self.DESTINATION_URI,
        }

        # Check request
        assert len(channel.GetSink.requests) == 1
        request = channel.GetSink.requests[0]
        assert request.sink_name == self.SINK_PATH

    def test_sink_update(self):
        channel, api = self.make_sinks_api()

        channel.UpdateSink.response = logging_config_pb2.LogSink(
            name=self.SINK_NAME,
            destination=self.DESTINATION_URI,
            filter=FILTER,
            writer_identity=self.SINK_WRITER_IDENTITY,
        )

        result = api.sink_update(
            PROJECT,
            self.SINK_NAME,
            FILTER,
            self.DESTINATION_URI,
            unique_writer_identity=True,
        )

        # Check response
        assert result == {
            "name": self.SINK_NAME,
            "filter": FILTER,
            "destination": self.DESTINATION_URI,
            "writerIdentity": self.SINK_WRITER_IDENTITY,
        }

        # Check request
        assert len(channel.UpdateSink.requests) == 1
        request = channel.UpdateSink.requests[0]
        assert request.sink_name == self.SINK_PATH
        assert request.unique_writer_identity is True
        assert request.sink.name == self.SINK_PATH
        assert request.sink.filter == FILTER
        assert request.sink.destination == self.DESTINATION_URI

    def test_sink_delete(self):
        channel, api = self.make_sinks_api()

        channel.DeleteSink.response = empty_pb2.Empty()

        api.sink_delete(PROJECT, self.SINK_NAME)

        assert len(channel.DeleteSink.requests) == 1
        request = channel.DeleteSink.requests[0]
        assert request.sink_name == self.SINK_PATH


class Test_MetricsAPI(object):
    METRIC_NAME = "metric_name"
    METRIC_PATH = "projects/%s/metrics/%s" % (PROJECT, METRIC_NAME)
    DESCRIPTION = "Description"

    @staticmethod
    def make_metrics_api():
        channel = grpc_helpers.ChannelStub()
        gapic_client = metrics_service_v2_client.MetricsServiceV2Client(channel=channel)
        handwritten_client = mock.Mock()
        api = _gapic._MetricsAPI(gapic_client, handwritten_client)
        return channel, api

    def test_ctor(self):
        channel = grpc_helpers.ChannelStub()
        gapic_client = metrics_service_v2_client.MetricsServiceV2Client(channel=channel)
        api = _gapic._MetricsAPI(gapic_client, mock.sentinel.client)
        assert api._gapic_api is gapic_client
        assert api._client is mock.sentinel.client

    def test_list_metrics(self):
        channel, api = self.make_metrics_api()

        sink_msg = logging_metrics_pb2.LogMetric(
            name=self.METRIC_PATH, description=self.DESCRIPTION, filter=FILTER
        )
        channel.ListLogMetrics.response = logging_metrics_pb2.ListLogMetricsResponse(
            metrics=[sink_msg]
        )

        result = api.list_metrics(PROJECT)
        metrics = list(result)

        # Check the response
        assert len(metrics) == 1
        metric = metrics[0]
        assert isinstance(metric, google.cloud.logging.metric.Metric)
        assert metric.name == self.METRIC_PATH
        assert metric.description == self.DESCRIPTION
        assert metric.filter_ == FILTER

        # Check the request
        assert len(channel.ListLogMetrics.requests) == 1
        request = channel.ListLogMetrics.requests[0]
        assert request.parent == PROJECT_PATH

    def test_list_metrics_options(self):
        channel, api = self.make_metrics_api()

        channel.ListLogMetrics.response = logging_metrics_pb2.ListLogMetricsResponse(
            metrics=[]
        )

        result = api.list_metrics(PROJECT, page_size=42, page_token="token")
        list(result)

        # Check the request
        assert len(channel.ListLogMetrics.requests) == 1
        request = channel.ListLogMetrics.requests[0]
        assert request.parent == PROJECT_PATH
        assert request.page_size == 42
        assert request.page_token == "token"

    def test_metric_create(self):
        channel, api = self.make_metrics_api()

        channel.CreateLogMetric.response = empty_pb2.Empty()

        api.metric_create(PROJECT, self.METRIC_NAME, FILTER, self.DESCRIPTION)

        # Check the request
        assert len(channel.CreateLogMetric.requests) == 1
        request = channel.CreateLogMetric.requests[0]
        assert request.parent == PROJECT_PATH
        assert request.metric.name == self.METRIC_NAME
        assert request.metric.filter == FILTER
        assert request.metric.description == self.DESCRIPTION

    def test_metric_get(self):
        channel, api = self.make_metrics_api()

        channel.GetLogMetric.response = logging_metrics_pb2.LogMetric(
            name=self.METRIC_PATH, description=self.DESCRIPTION, filter=FILTER
        )

        response = api.metric_get(PROJECT, self.METRIC_NAME)

        # Check the response
        assert response == {
            "name": self.METRIC_PATH,
            "filter": FILTER,
            "description": self.DESCRIPTION,
        }

        # Check the request
        assert len(channel.GetLogMetric.requests) == 1
        request = channel.GetLogMetric.requests[0]
        assert request.metric_name == self.METRIC_PATH

    def test_metric_update(self):
        channel, api = self.make_metrics_api()

        channel.UpdateLogMetric.response = logging_metrics_pb2.LogMetric(
            name=self.METRIC_PATH, description=self.DESCRIPTION, filter=FILTER
        )

        response = api.metric_update(
            PROJECT, self.METRIC_NAME, FILTER, self.DESCRIPTION
        )

        # Check the response
        assert response == {
            "name": self.METRIC_PATH,
            "filter": FILTER,
            "description": self.DESCRIPTION,
        }

        # Check the request
        assert len(channel.UpdateLogMetric.requests) == 1
        request = channel.UpdateLogMetric.requests[0]
        assert request.metric_name == self.METRIC_PATH
        assert request.metric.name == self.METRIC_PATH
        assert request.metric.filter == FILTER
        assert request.metric.description == self.DESCRIPTION

    def test_metric_delete(self):
        channel, api = self.make_metrics_api()

        channel.DeleteLogMetric.response = empty_pb2.Empty()

        api.metric_delete(PROJECT, self.METRIC_NAME)

        assert len(channel.DeleteLogMetric.requests) == 1
        request = channel.DeleteLogMetric.requests[0]
        assert request.metric_name == self.METRIC_PATH


class Test__parse_log_entry(unittest.TestCase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.logging._gapic import _parse_log_entry

        return _parse_log_entry(*args, **kwargs)

    def test_simple(self):
        from google.cloud.logging_v2.proto.log_entry_pb2 import LogEntry

        entry_pb = LogEntry(log_name=u"lol-jk", text_payload=u"bah humbug")
        result = self._call_fut(entry_pb)
        expected = {"logName": entry_pb.log_name, "textPayload": entry_pb.text_payload}
        self.assertEqual(result, expected)

    @mock.patch("google.cloud.logging._gapic.MessageToDict", side_effect=TypeError)
    def test_non_registry_failure(self, msg_to_dict_mock):
        entry_pb = mock.Mock(spec=["HasField"])
        entry_pb.HasField.return_value = False
        with self.assertRaises(TypeError):
            self._call_fut(entry_pb)

        entry_pb.HasField.assert_called_once_with("proto_payload")
        msg_to_dict_mock.assert_called_once_with(entry_pb)

    def test_unregistered_type(self):
        from google.cloud.logging_v2.proto.log_entry_pb2 import LogEntry
        from google.protobuf import any_pb2
        from google.protobuf import descriptor_pool
        from google.protobuf.timestamp_pb2 import Timestamp

        pool = descriptor_pool.Default()
        type_name = "google.bigtable.admin.v2.UpdateClusterMetadata"
        # Make sure the descriptor is not known in the registry.
        with self.assertRaises(KeyError):
            pool.FindMessageTypeByName(type_name)

        type_url = "type.googleapis.com/" + type_name
        metadata_bytes = b"\n\n\n\x03foo\x12\x03bar\x12\x06\x08\xbd\xb6\xfb\xc6\x05"
        any_pb = any_pb2.Any(type_url=type_url, value=metadata_bytes)
        timestamp = Timestamp(seconds=61, nanos=1234000)

        entry_pb = LogEntry(proto_payload=any_pb, timestamp=timestamp)
        result = self._call_fut(entry_pb)
        self.assertEqual(len(result), 2)
        self.assertEqual(result["timestamp"], "1970-01-01T00:01:01.001234Z")
        # NOTE: This "hack" is needed on Windows, where the equality check
        #       for an ``Any`` instance fails on unregistered types.
        self.assertEqual(result["protoPayload"].type_url, type_url)
        self.assertEqual(result["protoPayload"].value, metadata_bytes)

    def test_registered_type(self):
        from google.cloud.logging_v2.proto.log_entry_pb2 import LogEntry
        from google.protobuf import any_pb2
        from google.protobuf import descriptor_pool
        from google.protobuf.struct_pb2 import Struct
        from google.protobuf.struct_pb2 import Value

        pool = descriptor_pool.Default()
        type_name = "google.protobuf.Struct"
        # Make sure the descriptor is known in the registry.
        descriptor = pool.FindMessageTypeByName(type_name)
        self.assertEqual(descriptor.name, "Struct")

        type_url = "type.googleapis.com/" + type_name
        field_name = "foo"
        field_value = u"Bar"
        struct_pb = Struct(fields={field_name: Value(string_value=field_value)})
        any_pb = any_pb2.Any(type_url=type_url, value=struct_pb.SerializeToString())

        entry_pb = LogEntry(proto_payload=any_pb, log_name=u"all-good")
        result = self._call_fut(entry_pb)
        expected_proto = {
            "logName": entry_pb.log_name,
            "protoPayload": {"@type": type_url, "value": {field_name: field_value}},
        }
        self.assertEqual(result, expected_proto)


class Test__log_entry_mapping_to_pb(unittest.TestCase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.logging._gapic import _log_entry_mapping_to_pb

        return _log_entry_mapping_to_pb(*args, **kwargs)

    def test_simple(self):
        from google.cloud.logging_v2.proto.log_entry_pb2 import LogEntry

        result = self._call_fut({})
        self.assertEqual(result, LogEntry())

    def test_unregistered_type(self):
        from google.protobuf import descriptor_pool
        from google.protobuf.json_format import ParseError

        pool = descriptor_pool.Default()
        type_name = "google.bigtable.admin.v2.UpdateClusterMetadata"
        # Make sure the descriptor is not known in the registry.
        with self.assertRaises(KeyError):
            pool.FindMessageTypeByName(type_name)

        type_url = "type.googleapis.com/" + type_name
        json_mapping = {
            "protoPayload": {
                "@type": type_url,
                "originalRequest": {"name": "foo", "location": "bar"},
                "requestTime": {"seconds": 1491000125},
            }
        }
        with self.assertRaises(ParseError):
            self._call_fut(json_mapping)

    def test_registered_type(self):
        from google.cloud.logging_v2.proto.log_entry_pb2 import LogEntry
        from google.protobuf import any_pb2
        from google.protobuf import descriptor_pool

        pool = descriptor_pool.Default()
        type_name = "google.protobuf.Struct"
        # Make sure the descriptor is known in the registry.
        descriptor = pool.FindMessageTypeByName(type_name)
        self.assertEqual(descriptor.name, "Struct")

        type_url = "type.googleapis.com/" + type_name
        field_name = "foo"
        field_value = u"Bar"
        json_mapping = {
            "logName": u"hi-everybody",
            "protoPayload": {"@type": type_url, "value": {field_name: field_value}},
        }
        # Convert to a valid LogEntry.
        result = self._call_fut(json_mapping)
        entry_pb = LogEntry(
            log_name=json_mapping["logName"],
            proto_payload=any_pb2.Any(
                type_url=type_url, value=b"\n\014\n\003foo\022\005\032\003Bar"
            ),
        )
        self.assertEqual(result, entry_pb)


@mock.patch("google.cloud.logging._gapic.LoggingServiceV2Client", autospec=True)
def test_make_logging_api(gapic_client):
    client = mock.Mock(spec=["_credentials", "_client_info"])
    api = _gapic.make_logging_api(client)
    assert api._client == client
    assert api._gapic_api == gapic_client.return_value
    gapic_client.assert_called_once_with(
        credentials=client._credentials, client_info=client._client_info
    )


@mock.patch("google.cloud.logging._gapic.MetricsServiceV2Client", autospec=True)
def test_make_metrics_api(gapic_client):
    client = mock.Mock(spec=["_credentials", "_client_info"])
    api = _gapic.make_metrics_api(client)
    assert api._client == client
    assert api._gapic_api == gapic_client.return_value
    gapic_client.assert_called_once_with(
        credentials=client._credentials, client_info=client._client_info
    )


@mock.patch("google.cloud.logging._gapic.ConfigServiceV2Client", autospec=True)
def test_make_sinks_api(gapic_client):
    client = mock.Mock(spec=["_credentials", "_client_info"])
    api = _gapic.make_sinks_api(client)
    assert api._client == client
    assert api._gapic_api == gapic_client.return_value
    gapic_client.assert_called_once_with(
        credentials=client._credentials, client_info=client._client_info
    )
