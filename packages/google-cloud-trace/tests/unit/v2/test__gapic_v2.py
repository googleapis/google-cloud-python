# Copyright 2017 Google LLC
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
import unittest

import mock


def _str_to_truncatablestr(str_to_convert):
    result = {"value": str_to_convert, "truncated_byte_count": 0}
    return result


class _Base(object):
    from google.cloud.trace_v2.gapic import enums

    # Set the constants used for tests
    project = "PROJECT"
    trace_id = "c801e4119a064c659fe052d88f1d461b"
    span_id = "1234123412341234"
    parent_span_id = "1111000011110000"
    span_name = "projects/{}/traces/{}/spans/{}".format(project, trace_id, span_id)
    start_time = datetime.datetime.utcnow()
    end_time = datetime.datetime.utcnow()
    type = enums.Span.TimeEvent.MessageEvent.Type.SENT
    display_name = "test display name"

    attributes = {
        "attributeMap": {
            "test_int_key": {"int_value": 123},
            "test_str_key": {"string_value": _str_to_truncatablestr("str_value")},
            "test_bool_key": {"bool_value": True},
        }
    }

    st_function_name = "test function name"
    st_origin_name = "test original name"
    st_file_name = "test file name"
    st_line_number = 12
    st_column_number = 2
    st_test_module = "test module"
    st_build_id = "test build id"
    st_source_version = "test source version"
    stack_trace = {
        "stack_frames": {
            "frame": [
                {
                    "function_name": _str_to_truncatablestr(st_function_name),
                    "original_function_name": _str_to_truncatablestr(st_origin_name),
                    "file_name": _str_to_truncatablestr(st_file_name),
                    "line_number": st_line_number,
                    "column_number": st_column_number,
                    "load_module": {
                        "module": _str_to_truncatablestr(st_test_module),
                        "build_id": _str_to_truncatablestr(st_build_id),
                    },
                    "source_version": _str_to_truncatablestr(st_source_version),
                }
            ],
            "dropped_frames_count": 0,
        },
        "stack_trace_hash_id": 1234,
    }

    te_time = datetime.datetime.utcnow().isoformat() + "Z"
    te_description = "test description"
    time_events = {
        "time_event": [
            {
                "time": te_time,
                "annotation": {
                    "description": _str_to_truncatablestr(te_description),
                    "attributes": attributes,
                },  # TimeEvent can contain either annotation
                # or message_event
            }
        ],
        "dropped_annotations_count": 0,
        "dropped_message_events_count": 0,
    }

    link_span_id = "1111222211112222"
    links = {
        "link": [
            {
                "trace_id": trace_id,
                "span_id": link_span_id,
                "type": type,
                "attributes": attributes,
            }
        ],
        "dropped_links_count": 0,
    }

    status_code = 888
    status_message = "test status message"
    status = {"code": status_code, "message": status_message, "details": []}

    same_process_as_parent_span = True
    child_span_count = 0

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)


class Test__TraceAPI(_Base, unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.trace._gapic import _TraceAPI

        return _TraceAPI

    def test_constructor(self):
        gapic_api = object()
        client = object()
        api = self._make_one(gapic_api, client)
        self.assertIs(api._gapic_api, gapic_api)
        self.assertIs(api.client, client)

    def test_batch_write_spans(self):
        from google.cloud.trace_v2.gapic import trace_service_client
        from google.cloud.trace._gapic import _dict_mapping_to_pb

        spans = {
            "spans": [
                {
                    "name": self.span_name,
                    "span_id": self.span_id,
                    "parent_span_id": self.parent_span_id,
                    "display_name": _str_to_truncatablestr(self.display_name),
                    "start_time": self.start_time.isoformat() + "Z",
                    "end_time": self.end_time.isoformat() + "Z",
                    "attributes": self.attributes,
                    "stack_trace": self.stack_trace,
                    "time_events": self.time_events,
                    "links": self.links,
                    "status": self.status,
                    "same_process_as_parent_span": self.same_process_as_parent_span,
                    "child_span_count": self.child_span_count,
                }
            ]
        }

        spans_pb_list = [_dict_mapping_to_pb(spans["spans"][0], "Span")]
        project_name = "projects/{}".format(self.project)

        gapic_api = mock.Mock(spec=trace_service_client.TraceServiceClient)
        api = self._make_one(gapic_api, None)
        retry = mock.Mock()
        timeout = mock.Mock()
        api.batch_write_spans(project_name, spans, retry, timeout)

        gapic_api.batch_write_spans.assert_called_with(
            name=project_name, spans=spans_pb_list, retry=retry, timeout=timeout
        )

    def test_create_span_default(self):
        from google.cloud.trace_v2.gapic import trace_service_client
        from google.cloud.trace._gapic import _dict_mapping_to_pb
        from google.cloud._helpers import _datetime_to_pb_timestamp

        gapic_api = mock.Mock(spec=trace_service_client.TraceServiceClient)
        api = self._make_one(gapic_api, None)
        api.create_span(
            name=self.span_name,
            span_id=self.span_id,
            display_name=_str_to_truncatablestr(self.display_name),
            start_time=self.start_time,
            end_time=self.end_time,
        )

        display_name_pb = _dict_mapping_to_pb(
            _str_to_truncatablestr(self.display_name), "TruncatableString"
        )
        start_time_pb = _datetime_to_pb_timestamp(self.start_time)
        end_time_pb = _datetime_to_pb_timestamp(self.end_time)

        gapic_api.create_span.assert_called_with(
            name=self.span_name,
            span_id=self.span_id,
            display_name=display_name_pb,
            start_time=start_time_pb,
            end_time=end_time_pb,
            parent_span_id=None,
            attributes=None,
            stack_trace=None,
            time_events=None,
            links=None,
            status=None,
            same_process_as_parent_span=None,
            child_span_count=None,
        )

    def test_create_span_explicit(self):
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.trace._gapic import (
            _dict_mapping_to_pb,
            _span_attrs_to_pb,
            _status_mapping_to_pb,
            _value_to_pb,
        )
        from google.cloud.trace_v2.gapic import trace_service_client

        gapic_api = mock.Mock(spec=trace_service_client.TraceServiceClient)
        api = self._make_one(gapic_api, None)
        api.create_span(
            name=self.span_name,
            span_id=self.span_id,
            display_name=_str_to_truncatablestr(self.display_name),
            start_time=self.start_time,
            end_time=self.end_time,
            parent_span_id=self.parent_span_id,
            attributes=self.attributes,
            stack_trace=self.stack_trace,
            time_events=self.time_events,
            links=self.links,
            status=self.status,
            same_process_as_parent_span=self.same_process_as_parent_span,
            child_span_count=self.child_span_count,
        )

        display_name_pb = _dict_mapping_to_pb(
            _str_to_truncatablestr(self.display_name), "TruncatableString"
        )
        start_time_pb = _datetime_to_pb_timestamp(self.start_time)
        end_time_pb = _datetime_to_pb_timestamp(self.end_time)
        attributes_pb = _span_attrs_to_pb(self.attributes, "Attributes")
        stack_trace_pb = _dict_mapping_to_pb(self.stack_trace, "StackTrace")
        time_events_pb = _span_attrs_to_pb(self.time_events, "TimeEvents")
        links_pb = _span_attrs_to_pb(self.links, "Links")
        status_pb = _status_mapping_to_pb(self.status)
        same_process_as_parent_span_pb = _value_to_pb(
            self.same_process_as_parent_span, "BoolValue"
        )
        child_span_count_pb = _value_to_pb(self.child_span_count, "Int32Value")

        gapic_api.create_span.assert_called_with(
            name=self.span_name,
            span_id=self.span_id,
            display_name=display_name_pb,
            start_time=start_time_pb,
            end_time=end_time_pb,
            parent_span_id=self.parent_span_id,
            attributes=attributes_pb,
            stack_trace=stack_trace_pb,
            time_events=time_events_pb,
            links=links_pb,
            status=status_pb,
            same_process_as_parent_span=same_process_as_parent_span_pb,
            child_span_count=child_span_count_pb,
        )


class Test_make_trace_api(unittest.TestCase):
    def _call_fut(self, client):
        from google.cloud.trace._gapic import make_trace_api

        return make_trace_api(client)

    def test_it(self):
        from google.cloud.trace._gapic import _TraceAPI

        credentials = object()
        client = mock.Mock(_credentials=credentials, spec=["_credentials"])
        generated_api_kwargs = []
        generated = object()

        def generated_api(**kwargs):
            generated_api_kwargs.append(kwargs)
            return generated

        host = "foo.apis.invalid"
        generated_api.SERVICE_ADDRESS = host

        patch_api = mock.patch(
            "google.cloud.trace._gapic.trace_service_client." "TraceServiceClient",
            new=generated_api,
        )

        with patch_api:
            trace_api = self._call_fut(client)

        self.assertEqual(len(generated_api_kwargs), 1)

        self.assertIsInstance(trace_api, _TraceAPI)
        self.assertIs(trace_api._gapic_api, generated)
        self.assertIs(trace_api.client, client)
