# Copyright 2018 Google LLC
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

from unittest import mock

import pytest

from google.cloud.datastore_v1.proto import query_pb2

from google.cloud.ndb import _datastore_query
from google.cloud.ndb import key as key_module
from google.cloud.ndb import query as query_module
from google.cloud.ndb import tasklets


@pytest.mark.usefixtures("in_context")
class Test_fetch:
    @staticmethod
    def test_unsupported_option():
        query = mock.Mock(ancestor="foo")
        tasklet = _datastore_query.fetch(query)
        with pytest.raises(NotImplementedError):
            tasklet.result()

    @staticmethod
    @mock.patch(
        "google.cloud.ndb._datastore_query._process_result",
        lambda *args: "".join(filter(None, args)),
    )
    @mock.patch("google.cloud.ndb._datastore_query._run_query")
    @mock.patch("google.cloud.ndb._datastore_query._query_to_protobuf")
    def test_project_from_query(_query_to_protobuf, _run_query):
        query = mock.Mock(
            app="myapp", projection=None, spec=("app", "projection")
        )
        query_pb = _query_to_protobuf.return_value

        _run_query_future = tasklets.Future()
        _run_query.return_value = _run_query_future

        tasklet = _datastore_query.fetch(query)
        _run_query_future.set_result([("a", "b"), ("c", "d"), ("e", "f")])
        assert tasklet.result() == ["ab", "cd", "ef"]

        assert _query_to_protobuf.called_once_with(query)
        _run_query.assert_called_once_with("myapp", query_pb)

    @staticmethod
    @mock.patch(
        "google.cloud.ndb._datastore_query._process_result",
        lambda *args: "".join(filter(None, args)),
    )
    @mock.patch("google.cloud.ndb._datastore_query._run_query")
    @mock.patch("google.cloud.ndb._datastore_query._query_to_protobuf")
    def test_project_from_context(_query_to_protobuf, _run_query, in_context):
        query = mock.Mock(
            app=None, projection=None, spec=("app", "projection")
        )
        query_pb = _query_to_protobuf.return_value

        _run_query_future = tasklets.Future()
        _run_query.return_value = _run_query_future

        tasklet = _datastore_query.fetch(query)
        _run_query_future.set_result([("a", "b"), ("c", "d"), ("e", "f")])
        assert tasklet.result() == ["ab", "cd", "ef"]

        assert _query_to_protobuf.called_once_with(query)
        _run_query.assert_called_once_with("testing", query_pb)


class Test__process_result:
    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_query.model")
    def test_unsupported_result_type(model):
        model._entity_from_protobuf.return_value = "bar"
        result = mock.Mock(entity="foo", spec=("entity",))
        with pytest.raises(NotImplementedError):
            _datastore_query._process_result("foo", result, None)

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_query.model")
    def test_full_entity(model):
        model._entity_from_protobuf.return_value = "bar"
        result = mock.Mock(entity="foo", spec=("entity",))
        assert (
            _datastore_query._process_result(
                _datastore_query.RESULT_TYPE_FULL, result, None
            )
            == "bar"
        )

        model._entity_from_protobuf.assert_called_once_with("foo")

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_query.model")
    def test_projection(model):
        entity = mock.Mock(spec=("_set_projection",))
        model._entity_from_protobuf.return_value = entity
        result = mock.Mock(entity="foo", spec=("entity",))
        assert (
            _datastore_query._process_result(
                _datastore_query.RESULT_TYPE_PROJECTION, result, ("a", "b")
            )
            is entity
        )

        model._entity_from_protobuf.assert_called_once_with("foo")
        entity._set_projection.assert_called_once_with(("a", "b"))


@pytest.mark.usefixtures("in_context")
class Test__query_to_protobuf:
    @staticmethod
    def test_no_args():
        query = query_module.Query()
        assert _datastore_query._query_to_protobuf(query) == query_pb2.Query()

    @staticmethod
    def test_kind():
        query = query_module.Query(kind="Foo")
        assert _datastore_query._query_to_protobuf(query) == query_pb2.Query(
            kind=[query_pb2.KindExpression(name="Foo")]
        )

    @staticmethod
    def test_ancestor():
        key = key_module.Key("Foo", 123)
        query = query_module.Query(ancestor=key)
        expected_pb = query_pb2.Query(
            filter=query_pb2.Filter(
                property_filter=query_pb2.PropertyFilter(
                    property=query_pb2.PropertyReference(name="__key__"),
                    op=query_pb2.PropertyFilter.HAS_ANCESTOR,
                )
            )
        )
        expected_pb.filter.property_filter.value.key_value.CopyFrom(
            key._key.to_protobuf()
        )
        assert _datastore_query._query_to_protobuf(query) == expected_pb

    @staticmethod
    def test_projection():
        query = query_module.Query(projection=("a", "b"))
        expected_pb = query_pb2.Query(
            projection=[
                query_pb2.Projection(
                    property=query_pb2.PropertyReference(name="a")
                ),
                query_pb2.Projection(
                    property=query_pb2.PropertyReference(name="b")
                ),
            ]
        )
        assert _datastore_query._query_to_protobuf(query) == expected_pb


@pytest.mark.usefixtures("in_context")
class Test__run_query:
    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_query.datastore_pb2")
    @mock.patch("google.cloud.ndb._datastore_query._datastore_api")
    def test_single_batch(_datastore_api, datastore_pb2):
        request = datastore_pb2.RunQueryRequest.return_value
        query_pb = object()

        make_call_future = tasklets.Future("RunQuery")
        _datastore_api.make_call.return_value = make_call_future

        batch = mock.Mock(
            more_results="nope",
            entity_result_type="this type",
            entity_results=["foo", "bar", "baz"],
            spec=("more_results", "entity_result_type", "entity_results"),
        )

        tasklet = _datastore_query._run_query("testing", query_pb)
        make_call_future.set_result(mock.Mock(batch=batch, spec=("batch",)))

        assert tasklet.result() == [
            ("this type", "foo"),
            ("this type", "bar"),
            ("this type", "baz"),
        ]

        datastore_pb2.RunQueryRequest.assert_called_once_with(
            project_id="testing", query=query_pb
        )
        _datastore_api.make_call.assert_called_once_with("RunQuery", request)

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_query.datastore_pb2")
    @mock.patch("google.cloud.ndb._datastore_query._datastore_api")
    def test_double_batch(_datastore_api, datastore_pb2):
        query_pb = mock.Mock(spec=("start_cursor",))

        make_call_future1 = tasklets.Future("RunQuery")
        make_call_future2 = tasklets.Future("RunQuery")
        _datastore_api.make_call.side_effect = (
            make_call_future1,
            make_call_future2,
        )

        batch1 = mock.Mock(
            more_results=_datastore_query.MORE_RESULTS_TYPE_NOT_FINISHED,
            entity_result_type="this type",
            entity_results=["foo"],
            end_cursor=b"end",
            spec=(
                "more_results",
                "entity_result_type",
                "entity_results",
                "end_cursor",
            ),
        )
        batch2 = mock.Mock(
            more_results="nope",
            entity_result_type="that type",
            entity_results=["bar", "baz"],
            spec=("more_results", "entity_result_type", "entity_results"),
        )

        tasklet = _datastore_query._run_query("testing", query_pb)
        make_call_future1.set_result(mock.Mock(batch=batch1, spec=("batch",)))
        make_call_future2.set_result(mock.Mock(batch=batch2, spec=("batch",)))

        assert tasklet.result() == [
            ("this type", "foo"),
            ("that type", "bar"),
            ("that type", "baz"),
        ]

        assert datastore_pb2.RunQueryRequest.call_count == 2
        assert _datastore_api.make_call.call_count == 2
        assert query_pb.start_cursor == b"end"
