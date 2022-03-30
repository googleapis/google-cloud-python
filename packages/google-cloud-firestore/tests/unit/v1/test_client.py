# Copyright 2020 Google LLC All rights reserved.
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
import types

import mock
import pytest


PROJECT = "my-prahjekt"


def _make_client(*args, **kwargs):
    from google.cloud.firestore_v1.client import Client

    return Client(*args, **kwargs)


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_default_client(*args, **kwargs):
    credentials = _make_credentials()
    return _make_client(project=PROJECT, credentials=credentials)


def test_client_constructor_defaults():
    from google.cloud.firestore_v1.client import _CLIENT_INFO
    from google.cloud.firestore_v1.client import DEFAULT_DATABASE

    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials)
    assert client.project == PROJECT
    assert client._credentials == credentials
    assert client._database == DEFAULT_DATABASE
    assert client._client_info is _CLIENT_INFO


def test_client_constructor_explicit():
    from google.api_core.client_options import ClientOptions

    credentials = _make_credentials()
    database = "now-db"
    client_info = mock.Mock()
    client_options = ClientOptions("endpoint")
    client = _make_client(
        project=PROJECT,
        credentials=credentials,
        database=database,
        client_info=client_info,
        client_options=client_options,
    )
    assert client.project == PROJECT
    assert client._credentials == credentials
    assert client._database == database
    assert client._client_info is client_info
    assert client._client_options is client_options


def test_client__firestore_api_property():
    credentials = _make_credentials()
    client = _make_client(project=PROJECT, credentials=credentials)
    helper = client._firestore_api_helper = mock.Mock()

    g_patch = mock.patch("google.cloud.firestore_v1.client.firestore_grpc_transport")
    f_patch = mock.patch("google.cloud.firestore_v1.client.firestore_client")

    with g_patch as grpc_transport:
        with f_patch as firestore_client:
            api = client._firestore_api

    assert api is helper.return_value

    helper.assert_called_once_with(
        grpc_transport.FirestoreGrpcTransport,
        firestore_client.FirestoreClient,
        firestore_client,
    )


def test_client_constructor_w_client_options():
    credentials = _make_credentials()
    client = _make_client(
        project=PROJECT,
        credentials=credentials,
        client_options={"api_endpoint": "foo-firestore.googleapis.com"},
    )
    assert client._target == "foo-firestore.googleapis.com"


def test_client_collection_factory():
    from google.cloud.firestore_v1.collection import CollectionReference

    collection_id = "users"
    client = _make_default_client()
    collection = client.collection(collection_id)

    assert collection._path == (collection_id,)
    assert collection._client is client
    assert isinstance(collection, CollectionReference)


def test_client_collection_factory_nested():
    from google.cloud.firestore_v1.collection import CollectionReference

    client = _make_default_client()
    parts = ("users", "alovelace", "beep")
    collection_path = "/".join(parts)
    collection1 = client.collection(collection_path)

    assert collection1._path == parts
    assert collection1._client is client
    assert isinstance(collection1, CollectionReference)

    # Make sure using segments gives the same result.
    collection2 = client.collection(*parts)
    assert collection2._path == parts
    assert collection2._client is client
    assert isinstance(collection2, CollectionReference)


def test_client__get_collection_reference():
    from google.cloud.firestore_v1.collection import CollectionReference

    client = _make_default_client()
    collection = client._get_collection_reference("collectionId")

    assert collection._client is client
    assert isinstance(collection, CollectionReference)


def test_client_collection_group():
    client = _make_default_client()
    query = client.collection_group("collectionId").where("foo", "==", "bar")

    assert query._all_descendants
    assert query._field_filters[0].field.field_path == "foo"
    assert query._field_filters[0].value.string_value == "bar"
    assert query._field_filters[0].op == query._field_filters[0].Operator.EQUAL
    assert query._parent.id == "collectionId"


def test_client_collection_group_no_slashes():
    client = _make_default_client()
    with pytest.raises(ValueError):
        client.collection_group("foo/bar")


def test_client_document_factory():
    from google.cloud.firestore_v1.document import DocumentReference

    parts = ("rooms", "roomA")
    client = _make_default_client()
    doc_path = "/".join(parts)
    document1 = client.document(doc_path)

    assert document1._path == parts
    assert document1._client is client
    assert isinstance(document1, DocumentReference)

    # Make sure using segments gives the same result.
    document2 = client.document(*parts)
    assert document2._path == parts
    assert document2._client is client
    assert isinstance(document2, DocumentReference)


def test_client_document_factory_w_absolute_path():
    from google.cloud.firestore_v1.document import DocumentReference

    parts = ("rooms", "roomA")
    client = _make_default_client()
    doc_path = "/".join(parts)
    to_match = client.document(doc_path)
    document1 = client.document(to_match._document_path)

    assert document1._path == parts
    assert document1._client is client
    assert isinstance(document1, DocumentReference)


def test_client_document_factory_w_nested_path():
    from google.cloud.firestore_v1.document import DocumentReference

    client = _make_default_client()
    parts = ("rooms", "roomA", "shoes", "dressy")
    doc_path = "/".join(parts)
    document1 = client.document(doc_path)

    assert document1._path == parts
    assert document1._client is client
    assert isinstance(document1, DocumentReference)

    # Make sure using segments gives the same result.
    document2 = client.document(*parts)
    assert document2._path == parts
    assert document2._client is client
    assert isinstance(document2, DocumentReference)


def _collections_helper(retry=None, timeout=None):
    from google.cloud.firestore_v1 import _helpers
    from google.cloud.firestore_v1.collection import CollectionReference

    collection_ids = ["users", "projects"]

    class Pager(object):
        def __iter__(self):
            yield from collection_ids

    firestore_api = mock.Mock(spec=["list_collection_ids"])
    firestore_api.list_collection_ids.return_value = Pager()

    client = _make_default_client()
    client._firestore_api_internal = firestore_api
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    collections = list(client.collections(**kwargs))

    assert len(collections) == len(collection_ids)
    for collection, collection_id in zip(collections, collection_ids):
        assert isinstance(collection, CollectionReference)
        assert collection.parent is None
        assert collection.id == collection_id

    base_path = client._database_string + "/documents"
    firestore_api.list_collection_ids.assert_called_once_with(
        request={"parent": base_path},
        metadata=client._rpc_metadata,
        **kwargs,
    )


def test_client_collections():
    _collections_helper()


def test_client_collections_w_retry_timeout():
    from google.api_core.retry import Retry

    retry = Retry(predicate=object())
    timeout = 123.0
    _collections_helper(retry=retry, timeout=timeout)


def _invoke_get_all(client, references, document_pbs, **kwargs):
    # Create a minimal fake GAPIC with a dummy response.
    firestore_api = mock.Mock(spec=["batch_get_documents"])
    response_iterator = iter(document_pbs)
    firestore_api.batch_get_documents.return_value = response_iterator

    # Attach the fake GAPIC to a real client.
    client._firestore_api_internal = firestore_api

    # Actually call get_all().
    snapshots = client.get_all(references, **kwargs)
    assert isinstance(snapshots, types.GeneratorType)

    return list(snapshots)


def _get_all_helper(num_snapshots=2, txn_id=None, retry=None, timeout=None):
    from google.cloud.firestore_v1 import _helpers
    from google.cloud.firestore_v1.types import common
    from google.cloud.firestore_v1.async_document import DocumentSnapshot

    client = _make_default_client()

    data1 = {"a": "cheese"}
    document1 = client.document("pineapple", "lamp1")
    document_pb1, read_time = _doc_get_info(document1._document_path, data1)
    response1 = _make_batch_response(found=document_pb1, read_time=read_time)

    data2 = {"b": True, "c": 18}
    document2 = client.document("pineapple", "lamp2")
    document, read_time = _doc_get_info(document2._document_path, data2)
    response2 = _make_batch_response(found=document, read_time=read_time)

    document3 = client.document("pineapple", "lamp3")
    response3 = _make_batch_response(missing=document3._document_path)

    expected_data = [data1, data2, None][:num_snapshots]
    documents = [document1, document2, document3][:num_snapshots]
    responses = [response1, response2, response3][:num_snapshots]
    field_paths = [
        field_path for field_path in ["a", "b", None][:num_snapshots] if field_path
    ]
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    if txn_id is not None:
        transaction = client.transaction()
        transaction._id = txn_id
        kwargs["transaction"] = transaction

    snapshots = _invoke_get_all(
        client,
        documents,
        responses,
        field_paths=field_paths,
        **kwargs,
    )

    assert len(snapshots) == num_snapshots

    for data, document, snapshot in zip(expected_data, documents, snapshots):
        assert isinstance(snapshot, DocumentSnapshot)
        assert snapshot._reference is document
        if data is None:
            assert not snapshot.exists
        else:
            assert snapshot._data == data

    # Verify the call to the mock.
    doc_paths = [document._document_path for document in documents]
    mask = common.DocumentMask(field_paths=field_paths)

    kwargs.pop("transaction", None)

    client._firestore_api.batch_get_documents.assert_called_once_with(
        request={
            "database": client._database_string,
            "documents": doc_paths,
            "mask": mask,
            "transaction": txn_id,
        },
        metadata=client._rpc_metadata,
        **kwargs,
    )


def test_client_get_all():
    _get_all_helper()


def test_client_get_all_with_transaction():
    txn_id = b"the-man-is-non-stop"
    _get_all_helper(num_snapshots=1, txn_id=txn_id)


def test_client_get_all_w_retry_timeout():
    from google.api_core.retry import Retry

    retry = Retry(predicate=object())
    timeout = 123.0
    _get_all_helper(retry=retry, timeout=timeout)


def test_client_get_all_wrong_order():
    _get_all_helper(num_snapshots=3)


def test_client_get_all_unknown_result():
    from google.cloud.firestore_v1.base_client import _BAD_DOC_TEMPLATE

    client = _make_default_client()

    expected_document = client.document("pineapple", "lamp1")

    data = {"z": 28.5}
    wrong_document = client.document("pineapple", "lamp2")
    document_pb, read_time = _doc_get_info(wrong_document._document_path, data)
    response = _make_batch_response(found=document_pb, read_time=read_time)

    # Exercise the mocked ``batch_get_documents``.
    with pytest.raises(ValueError) as exc_info:
        _invoke_get_all(client, [expected_document], [response])

    err_msg = _BAD_DOC_TEMPLATE.format(response.found.name)
    assert exc_info.value.args == (err_msg,)

    # Verify the call to the mock.
    doc_paths = [expected_document._document_path]
    client._firestore_api.batch_get_documents.assert_called_once_with(
        request={
            "database": client._database_string,
            "documents": doc_paths,
            "mask": None,
            "transaction": None,
        },
        metadata=client._rpc_metadata,
    )


def test_client_recursive_delete():
    from google.cloud.firestore_v1.types import document
    from google.cloud.firestore_v1.types import firestore

    client = _make_default_client()
    client._firestore_api_internal = mock.Mock(spec=["run_query"])
    collection_ref = client.collection("my_collection")

    results = []
    for index in range(10):
        results.append(
            firestore.RunQueryResponse(
                document=document.Document(name=f"{collection_ref.id}/{index}")
            )
        )

    chunks = [
        results[:3],
        results[3:6],
        results[6:9],
        results[9:],
    ]

    def _get_chunk(*args, **kwargs):
        return iter(chunks.pop(0))

    client._firestore_api_internal.run_query.side_effect = _get_chunk

    bulk_writer = mock.MagicMock()
    bulk_writer.mock_add_spec(spec=["delete", "close"])

    num_deleted = client.recursive_delete(
        collection_ref, bulk_writer=bulk_writer, chunk_size=3
    )
    assert num_deleted == len(results)


def test_client_recursive_delete_from_document():
    from google.cloud.firestore_v1.types import document
    from google.cloud.firestore_v1.types import firestore

    client = _make_default_client()
    client._firestore_api_internal = mock.Mock(
        spec=["run_query", "list_collection_ids"]
    )
    collection_ref = client.collection("my_collection")

    collection_1_id: str = "collection_1_id"
    collection_2_id: str = "collection_2_id"

    parent_doc = collection_ref.document("parent")

    collection_1_results = []
    collection_2_results = []

    for index in range(10):
        collection_1_results.append(
            firestore.RunQueryResponse(
                document=document.Document(name=f"{collection_1_id}/{index}"),
            ),
        )

        collection_2_results.append(
            firestore.RunQueryResponse(
                document=document.Document(name=f"{collection_2_id}/{index}"),
            ),
        )

    col_1_chunks = [
        collection_1_results[:3],
        collection_1_results[3:6],
        collection_1_results[6:9],
        collection_1_results[9:],
    ]

    col_2_chunks = [
        collection_2_results[:3],
        collection_2_results[3:6],
        collection_2_results[6:9],
        collection_2_results[9:],
    ]

    def _get_chunk(*args, **kwargs):
        start_at = (
            kwargs["request"]["structured_query"].start_at.values[0].reference_value
        )

        if collection_1_id in start_at:
            return iter(col_1_chunks.pop(0))
        return iter(col_2_chunks.pop(0))

    client._firestore_api_internal.run_query.side_effect = _get_chunk
    client._firestore_api_internal.list_collection_ids.return_value = [
        collection_1_id,
        collection_2_id,
    ]

    bulk_writer = mock.MagicMock()
    bulk_writer.mock_add_spec(spec=["delete", "close"])

    num_deleted = client.recursive_delete(
        parent_doc, bulk_writer=bulk_writer, chunk_size=3
    )

    expected_len = len(collection_1_results) + len(collection_2_results) + 1
    assert num_deleted == expected_len


def test_client_recursive_delete_raises():
    client = _make_default_client()
    with pytest.raises(TypeError):
        client.recursive_delete(object())


def test_client_batch():
    from google.cloud.firestore_v1.batch import WriteBatch

    client = _make_default_client()
    batch = client.batch()
    assert isinstance(batch, WriteBatch)
    assert batch._client is client
    assert batch._write_pbs == []


def test_client_bulk_writer():
    from google.cloud.firestore_v1.bulk_writer import BulkWriter

    client = _make_default_client()
    bulk_writer = client.bulk_writer()
    assert isinstance(bulk_writer, BulkWriter)
    assert bulk_writer._client is client


def test_client_transaction():
    from google.cloud.firestore_v1.transaction import Transaction

    client = _make_default_client()
    transaction = client.transaction(max_attempts=3, read_only=True)
    assert isinstance(transaction, Transaction)
    assert transaction._write_pbs == []
    assert transaction._max_attempts == 3
    assert transaction._read_only
    assert transaction._id is None


def _make_batch_response(**kwargs):
    from google.cloud.firestore_v1.types import firestore

    return firestore.BatchGetDocumentsResponse(**kwargs)


def _doc_get_info(ref_string, values):
    from google.cloud.firestore_v1.types import document
    from google.cloud._helpers import _datetime_to_pb_timestamp
    from google.cloud.firestore_v1 import _helpers

    now = datetime.datetime.utcnow()
    read_time = _datetime_to_pb_timestamp(now)
    delta = datetime.timedelta(seconds=100)
    update_time = _datetime_to_pb_timestamp(now - delta)
    create_time = _datetime_to_pb_timestamp(now - 2 * delta)

    document_pb = document.Document(
        name=ref_string,
        fields=_helpers.encode_dict(values),
        create_time=create_time,
        update_time=update_time,
    )

    return document_pb, read_time
