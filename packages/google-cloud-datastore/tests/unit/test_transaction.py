# Copyright 2014 Google LLC
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

import mock
import pytest


def test_transaction_ctor_defaults():
    from google.cloud.datastore.transaction import Transaction

    project = "PROJECT"
    client = _Client(project)

    xact = _make_transaction(client)

    assert xact.project == project
    assert xact._client is client
    assert xact.id is None
    assert xact._status == Transaction._INITIAL
    assert xact._mutations == []
    assert len(xact._partial_key_entities) == 0


def test_transaction_constructor_read_only():
    project = "PROJECT"
    id_ = 850302
    ds_api = _make_datastore_api(xact=id_)
    client = _Client(project, datastore_api=ds_api)
    options = _make_options(read_only=True)

    xact = _make_transaction(client, read_only=True)

    assert xact._options == options


def test_transaction_current():
    from google.cloud.datastore_v1.types import datastore as datastore_pb2

    project = "PROJECT"
    id_ = 678
    ds_api = _make_datastore_api(xact_id=id_)
    client = _Client(project, datastore_api=ds_api)
    xact1 = _make_transaction(client)
    xact2 = _make_transaction(client)
    assert xact1.current() is None
    assert xact2.current() is None

    with xact1:
        assert xact1.current() is xact1
        assert xact2.current() is xact1

        with _NoCommitBatch(client):
            assert xact1.current() is None
            assert xact2.current() is None

        with xact2:
            assert xact1.current() is xact2
            assert xact2.current() is xact2

            with _NoCommitBatch(client):
                assert xact1.current() is None
                assert xact2.current() is None

        assert xact1.current() is xact1
        assert xact2.current() is xact1

    assert xact1.current() is None
    assert xact2.current() is None

    begin_txn = ds_api.begin_transaction
    assert begin_txn.call_count == 2
    expected_request = _make_begin_request(project)
    begin_txn.assert_called_with(request=expected_request)

    commit_method = ds_api.commit
    assert commit_method.call_count == 2
    mode = datastore_pb2.CommitRequest.Mode.TRANSACTIONAL
    commit_method.assert_called_with(
        request={
            "project_id": project,
            "mode": mode,
            "mutations": [],
            "transaction": id_,
        }
    )

    ds_api.rollback.assert_not_called()


def test_transaction_begin():
    project = "PROJECT"
    id_ = 889
    ds_api = _make_datastore_api(xact_id=id_)
    client = _Client(project, datastore_api=ds_api)
    xact = _make_transaction(client)

    xact.begin()

    assert xact.id == id_

    expected_request = _make_begin_request(project)
    ds_api.begin_transaction.assert_called_once_with(request=expected_request)


def test_transaction_begin_w_readonly():
    project = "PROJECT"
    id_ = 889
    ds_api = _make_datastore_api(xact_id=id_)
    client = _Client(project, datastore_api=ds_api)
    xact = _make_transaction(client, read_only=True)

    xact.begin()

    assert xact.id == id_

    expected_request = _make_begin_request(project, read_only=True)
    ds_api.begin_transaction.assert_called_once_with(request=expected_request)


def test_transaction_begin_w_retry_w_timeout():
    project = "PROJECT"
    id_ = 889
    retry = mock.Mock()
    timeout = 100000

    ds_api = _make_datastore_api(xact_id=id_)
    client = _Client(project, datastore_api=ds_api)
    xact = _make_transaction(client)

    xact.begin(retry=retry, timeout=timeout)

    assert xact.id == id_

    expected_request = _make_begin_request(project)
    ds_api.begin_transaction.assert_called_once_with(
        request=expected_request, retry=retry, timeout=timeout,
    )


def test_transaction_begin_tombstoned():
    project = "PROJECT"
    id_ = 1094
    ds_api = _make_datastore_api(xact_id=id_)
    client = _Client(project, datastore_api=ds_api)
    xact = _make_transaction(client)

    xact.begin()

    assert xact.id == id_

    expected_request = _make_begin_request(project)
    ds_api.begin_transaction.assert_called_once_with(request=expected_request)

    xact.rollback()

    client._datastore_api.rollback.assert_called_once_with(
        request={"project_id": project, "transaction": id_}
    )
    assert xact.id is None

    with pytest.raises(ValueError):
        xact.begin()


def test_transaction_begin_w_begin_transaction_failure():
    project = "PROJECT"
    id_ = 712
    ds_api = _make_datastore_api(xact_id=id_)
    ds_api.begin_transaction = mock.Mock(side_effect=RuntimeError, spec=[])
    client = _Client(project, datastore_api=ds_api)
    xact = _make_transaction(client)

    with pytest.raises(RuntimeError):
        xact.begin()

    assert xact.id is None

    expected_request = _make_begin_request(project)
    ds_api.begin_transaction.assert_called_once_with(request=expected_request)


def test_transaction_rollback():
    project = "PROJECT"
    id_ = 239
    ds_api = _make_datastore_api(xact_id=id_)
    client = _Client(project, datastore_api=ds_api)
    xact = _make_transaction(client)
    xact.begin()

    xact.rollback()

    assert xact.id is None
    ds_api.rollback.assert_called_once_with(
        request={"project_id": project, "transaction": id_}
    )


def test_transaction_rollback_w_retry_w_timeout():
    project = "PROJECT"
    id_ = 239
    retry = mock.Mock()
    timeout = 100000

    ds_api = _make_datastore_api(xact_id=id_)
    client = _Client(project, datastore_api=ds_api)
    xact = _make_transaction(client)
    xact.begin()

    xact.rollback(retry=retry, timeout=timeout)

    assert xact.id is None
    ds_api.rollback.assert_called_once_with(
        request={"project_id": project, "transaction": id_},
        retry=retry,
        timeout=timeout,
    )


def test_transaction_commit_no_partial_keys():
    from google.cloud.datastore_v1.types import datastore as datastore_pb2

    project = "PROJECT"
    id_ = 1002930
    mode = datastore_pb2.CommitRequest.Mode.TRANSACTIONAL

    ds_api = _make_datastore_api(xact_id=id_)
    client = _Client(project, datastore_api=ds_api)
    xact = _make_transaction(client)
    xact.begin()
    xact.commit()

    ds_api.commit.assert_called_once_with(
        request={
            "project_id": project,
            "mode": mode,
            "mutations": [],
            "transaction": id_,
        }
    )
    assert xact.id is None


def test_transaction_commit_w_partial_keys_w_retry_w_timeout():
    from google.cloud.datastore_v1.types import datastore as datastore_pb2

    project = "PROJECT"
    kind = "KIND"
    id1 = 123
    mode = datastore_pb2.CommitRequest.Mode.TRANSACTIONAL
    key = _make_key(kind, id1, project)
    id2 = 234
    retry = mock.Mock()
    timeout = 100000

    ds_api = _make_datastore_api(key, xact_id=id2)
    client = _Client(project, datastore_api=ds_api)
    xact = _make_transaction(client)
    xact.begin()
    entity = _Entity()

    xact.put(entity)
    xact.commit(retry=retry, timeout=timeout)

    ds_api.commit.assert_called_once_with(
        request={
            "project_id": project,
            "mode": mode,
            "mutations": xact.mutations,
            "transaction": id2,
        },
        retry=retry,
        timeout=timeout,
    )
    assert xact.id is None
    assert entity.key.path == [{"kind": kind, "id": id1}]


def test_transaction_context_manager_no_raise():
    from google.cloud.datastore_v1.types import datastore as datastore_pb2

    project = "PROJECT"
    id_ = 912830
    ds_api = _make_datastore_api(xact_id=id_)
    client = _Client(project, datastore_api=ds_api)
    xact = _make_transaction(client)

    with xact:
        # only set between begin / commit
        assert xact.id == id_

    assert xact.id is None

    expected_request = _make_begin_request(project)
    ds_api.begin_transaction.assert_called_once_with(request=expected_request)

    mode = datastore_pb2.CommitRequest.Mode.TRANSACTIONAL
    client._datastore_api.commit.assert_called_once_with(
        request={
            "project_id": project,
            "mode": mode,
            "mutations": [],
            "transaction": id_,
        },
    )


def test_transaction_context_manager_w_raise():
    class Foo(Exception):
        pass

    project = "PROJECT"
    id_ = 614416
    ds_api = _make_datastore_api(xact_id=id_)
    client = _Client(project, datastore_api=ds_api)
    xact = _make_transaction(client)
    xact._mutation = object()
    try:
        with xact:
            assert xact.id == id_
            raise Foo()
    except Foo:
        pass

    assert xact.id is None

    expected_request = _make_begin_request(project)
    ds_api.begin_transaction.assert_called_once_with(request=expected_request)

    client._datastore_api.commit.assert_not_called()

    client._datastore_api.rollback.assert_called_once_with(
        request={"project_id": project, "transaction": id_}
    )


def test_transaction_put_read_only():
    project = "PROJECT"
    id_ = 943243
    ds_api = _make_datastore_api(xact_id=id_)
    client = _Client(project, datastore_api=ds_api)
    entity = _Entity()
    xact = _make_transaction(client, read_only=True)
    xact.begin()

    with pytest.raises(RuntimeError):
        xact.put(entity)


def _make_key(kind, id_, project):
    from google.cloud.datastore_v1.types import entity as entity_pb2

    key = entity_pb2.Key()
    key.partition_id.project_id = project
    elem = key._pb.path.add()
    elem.kind = kind
    elem.id = id_
    return key


class _Entity(dict):
    def __init__(self):
        super(_Entity, self).__init__()
        from google.cloud.datastore.key import Key

        self.key = Key("KIND", project="PROJECT")


class _Client(object):
    def __init__(self, project, datastore_api=None, namespace=None):
        self.project = project
        if datastore_api is None:
            datastore_api = _make_datastore_api()
        self._datastore_api = datastore_api
        self.namespace = namespace
        self._batches = []

    def _push_batch(self, batch):
        self._batches.insert(0, batch)

    def _pop_batch(self):
        return self._batches.pop(0)

    @property
    def current_batch(self):
        return self._batches and self._batches[0] or None


class _NoCommitBatch(object):
    def __init__(self, client):
        from google.cloud.datastore.batch import Batch

        self._client = client
        self._batch = Batch(client)

    def __enter__(self):
        self._client._push_batch(self._batch)
        return self._batch

    def __exit__(self, *args):
        self._client._pop_batch()


def _make_options(read_only=False, previous_transaction=None):
    from google.cloud.datastore_v1.types import TransactionOptions

    kw = {}

    if read_only:
        kw["read_only"] = TransactionOptions.ReadOnly()

    return TransactionOptions(**kw)


def _make_transaction(client, **kw):
    from google.cloud.datastore.transaction import Transaction

    return Transaction(client, **kw)


def _make_begin_request(project, read_only=False):
    expected_options = _make_options(read_only=read_only)
    return {
        "project_id": project,
        "transaction_options": expected_options,
    }


def _make_commit_response(*keys):
    from google.cloud.datastore_v1.types import datastore as datastore_pb2

    mutation_results = [datastore_pb2.MutationResult(key=key)._pb for key in keys]
    return datastore_pb2.CommitResponse(mutation_results=mutation_results)


def _make_datastore_api(*keys, **kwargs):
    commit_method = mock.Mock(return_value=_make_commit_response(*keys), spec=[])

    xact_id = kwargs.pop("xact_id", 123)
    txn_pb = mock.Mock(transaction=xact_id, spec=["transaction"])
    begin_txn = mock.Mock(return_value=txn_pb, spec=[])

    return mock.Mock(
        commit=commit_method,
        begin_transaction=begin_txn,
        spec=["begin_transaction", "commit", "rollback"],
    )
