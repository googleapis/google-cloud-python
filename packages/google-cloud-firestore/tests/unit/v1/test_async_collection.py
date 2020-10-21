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

import pytest
import types
import aiounittest

import mock
from tests.unit.v1.test__helpers import AsyncMock, AsyncIter


class TestAsyncCollectionReference(aiounittest.AsyncTestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.async_collection import AsyncCollectionReference

        return AsyncCollectionReference

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    @staticmethod
    def _get_public_methods(klass):
        return set().union(
            *(
                (
                    name
                    for name, value in class_.__dict__.items()
                    if (
                        not name.startswith("_")
                        and isinstance(value, types.FunctionType)
                    )
                )
                for class_ in (klass,) + klass.__bases__
            )
        )

    def test_query_method_matching(self):
        from google.cloud.firestore_v1.async_query import AsyncQuery

        query_methods = self._get_public_methods(AsyncQuery)
        klass = self._get_target_class()
        collection_methods = self._get_public_methods(klass)
        # Make sure every query method is present on
        # ``AsyncCollectionReference``.
        self.assertLessEqual(query_methods, collection_methods)

    def test_constructor(self):
        collection_id1 = "rooms"
        document_id = "roomA"
        collection_id2 = "messages"
        client = mock.sentinel.client

        collection = self._make_one(
            collection_id1, document_id, collection_id2, client=client
        )
        self.assertIs(collection._client, client)
        expected_path = (collection_id1, document_id, collection_id2)
        self.assertEqual(collection._path, expected_path)

    @pytest.mark.asyncio
    async def test_add_auto_assigned(self):
        from google.cloud.firestore_v1.types import document
        from google.cloud.firestore_v1.async_document import AsyncDocumentReference
        from google.cloud.firestore_v1 import SERVER_TIMESTAMP
        from google.cloud.firestore_v1._helpers import pbs_for_create

        # Create a minimal fake GAPIC add attach it to a real client.
        firestore_api = AsyncMock(spec=["create_document", "commit"])
        write_result = mock.Mock(
            update_time=mock.sentinel.update_time, spec=["update_time"]
        )
        commit_response = mock.Mock(
            write_results=[write_result],
            spec=["write_results", "commit_time"],
            commit_time=mock.sentinel.commit_time,
        )
        firestore_api.commit.return_value = commit_response
        create_doc_response = document.Document()
        firestore_api.create_document.return_value = create_doc_response
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Actually make a collection.
        collection = self._make_one("grand-parent", "parent", "child", client=client)

        # Actually call add() on our collection; include a transform to make
        # sure transforms during adds work.
        document_data = {"been": "here", "now": SERVER_TIMESTAMP}

        patch = mock.patch("google.cloud.firestore_v1.base_collection._auto_id")
        random_doc_id = "DEADBEEF"
        with patch as patched:
            patched.return_value = random_doc_id
            update_time, document_ref = await collection.add(document_data)

        # Verify the response and the mocks.
        self.assertIs(update_time, mock.sentinel.update_time)
        self.assertIsInstance(document_ref, AsyncDocumentReference)
        self.assertIs(document_ref._client, client)
        expected_path = collection._path + (random_doc_id,)
        self.assertEqual(document_ref._path, expected_path)

        write_pbs = pbs_for_create(document_ref._document_path, document_data)
        firestore_api.commit.assert_called_once_with(
            request={
                "database": client._database_string,
                "writes": write_pbs,
                "transaction": None,
            },
            metadata=client._rpc_metadata,
        )
        # Since we generate the ID locally, we don't call 'create_document'.
        firestore_api.create_document.assert_not_called()

    @staticmethod
    def _write_pb_for_create(document_path, document_data):
        from google.cloud.firestore_v1.types import common
        from google.cloud.firestore_v1.types import document
        from google.cloud.firestore_v1.types import write
        from google.cloud.firestore_v1 import _helpers

        return write.Write(
            update=document.Document(
                name=document_path, fields=_helpers.encode_dict(document_data)
            ),
            current_document=common.Precondition(exists=False),
        )

    async def _add_helper(self, retry=None, timeout=None):
        from google.cloud.firestore_v1.async_document import AsyncDocumentReference
        from google.cloud.firestore_v1 import _helpers

        # Create a minimal fake GAPIC with a dummy response.
        firestore_api = AsyncMock(spec=["commit"])
        write_result = mock.Mock(
            update_time=mock.sentinel.update_time, spec=["update_time"]
        )
        commit_response = mock.Mock(
            write_results=[write_result],
            spec=["write_results", "commit_time"],
            commit_time=mock.sentinel.commit_time,
        )
        firestore_api.commit.return_value = commit_response

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Actually make a collection and call add().
        collection = self._make_one("parent", client=client)
        document_data = {"zorp": 208.75, "i-did-not": b"know that"}
        doc_id = "child"
        kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

        update_time, document_ref = await collection.add(
            document_data, document_id=doc_id, **kwargs,
        )

        # Verify the response and the mocks.
        self.assertIs(update_time, mock.sentinel.update_time)
        self.assertIsInstance(document_ref, AsyncDocumentReference)
        self.assertIs(document_ref._client, client)
        self.assertEqual(document_ref._path, (collection.id, doc_id))

        write_pb = self._write_pb_for_create(document_ref._document_path, document_data)
        firestore_api.commit.assert_called_once_with(
            request={
                "database": client._database_string,
                "writes": [write_pb],
                "transaction": None,
            },
            metadata=client._rpc_metadata,
            **kwargs,
        )

    @pytest.mark.asyncio
    async def test_add_explicit_id(self):
        await self._add_helper()

    @pytest.mark.asyncio
    async def test_add_w_retry_timeout(self):
        from google.api_core.retry import Retry

        retry = Retry(predicate=object())
        timeout = 123.0
        await self._add_helper(retry=retry, timeout=timeout)

    @pytest.mark.asyncio
    async def _list_documents_helper(self, page_size=None, retry=None, timeout=None):
        from google.cloud.firestore_v1 import _helpers
        from google.api_core.page_iterator_async import AsyncIterator
        from google.api_core.page_iterator import Page
        from google.cloud.firestore_v1.async_document import AsyncDocumentReference
        from google.cloud.firestore_v1.types.document import Document

        class _AsyncIterator(AsyncIterator):
            def __init__(self, pages):
                super(_AsyncIterator, self).__init__(client=None)
                self._pages = pages

            async def _next_page(self):
                if self._pages:
                    page, self._pages = self._pages[0], self._pages[1:]
                    return Page(self, page, self.item_to_value)

        client = _make_client()
        template = client._database_string + "/documents/{}"
        document_ids = ["doc-1", "doc-2"]
        documents = [
            Document(name=template.format(document_id)) for document_id in document_ids
        ]
        iterator = _AsyncIterator(pages=[documents])
        firestore_api = AsyncMock()
        firestore_api.mock_add_spec(spec=["list_documents"])
        firestore_api.list_documents.return_value = iterator
        client._firestore_api_internal = firestore_api
        collection = self._make_one("collection", client=client)
        kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

        if page_size is not None:
            documents = [
                i
                async for i in collection.list_documents(page_size=page_size, **kwargs,)
            ]
        else:
            documents = [i async for i in collection.list_documents(**kwargs)]

        # Verify the response and the mocks.
        self.assertEqual(len(documents), len(document_ids))
        for document, document_id in zip(documents, document_ids):
            self.assertIsInstance(document, AsyncDocumentReference)
            self.assertEqual(document.parent, collection)
            self.assertEqual(document.id, document_id)

        parent, _ = collection._parent_info()
        firestore_api.list_documents.assert_called_once_with(
            request={
                "parent": parent,
                "collection_id": collection.id,
                "page_size": page_size,
                "show_missing": True,
            },
            metadata=client._rpc_metadata,
            **kwargs,
        )

    @pytest.mark.asyncio
    async def test_list_documents_wo_page_size(self):
        await self._list_documents_helper()

    @pytest.mark.asyncio
    async def test_list_documents_w_retry_timeout(self):
        from google.api_core.retry import Retry

        retry = Retry(predicate=object())
        timeout = 123.0
        await self._list_documents_helper(retry=retry, timeout=timeout)

    @pytest.mark.asyncio
    async def test_list_documents_w_page_size(self):
        await self._list_documents_helper(page_size=25)

    @mock.patch("google.cloud.firestore_v1.async_query.AsyncQuery", autospec=True)
    @pytest.mark.asyncio
    async def test_get(self, query_class):
        collection = self._make_one("collection")
        get_response = await collection.get()

        query_class.assert_called_once_with(collection)
        query_instance = query_class.return_value

        self.assertIs(get_response, query_instance.get.return_value)
        query_instance.get.assert_called_once_with(transaction=None)

    @mock.patch("google.cloud.firestore_v1.async_query.AsyncQuery", autospec=True)
    @pytest.mark.asyncio
    async def test_get_w_retry_timeout(self, query_class):
        from google.api_core.retry import Retry

        retry = Retry(predicate=object())
        timeout = 123.0
        collection = self._make_one("collection")
        get_response = await collection.get(retry=retry, timeout=timeout)

        query_class.assert_called_once_with(collection)
        query_instance = query_class.return_value

        self.assertIs(get_response, query_instance.get.return_value)
        query_instance.get.assert_called_once_with(
            transaction=None, retry=retry, timeout=timeout,
        )

    @mock.patch("google.cloud.firestore_v1.async_query.AsyncQuery", autospec=True)
    @pytest.mark.asyncio
    async def test_get_with_transaction(self, query_class):
        collection = self._make_one("collection")
        transaction = mock.sentinel.txn
        get_response = await collection.get(transaction=transaction)

        query_class.assert_called_once_with(collection)
        query_instance = query_class.return_value

        self.assertIs(get_response, query_instance.get.return_value)
        query_instance.get.assert_called_once_with(transaction=transaction)

    @mock.patch("google.cloud.firestore_v1.async_query.AsyncQuery", autospec=True)
    @pytest.mark.asyncio
    async def test_stream(self, query_class):
        query_class.return_value.stream.return_value = AsyncIter(range(3))

        collection = self._make_one("collection")
        stream_response = collection.stream()

        async for _ in stream_response:
            pass

        query_class.assert_called_once_with(collection)
        query_instance = query_class.return_value
        query_instance.stream.assert_called_once_with(transaction=None)

    @mock.patch("google.cloud.firestore_v1.async_query.AsyncQuery", autospec=True)
    @pytest.mark.asyncio
    async def test_stream_w_retry_timeout(self, query_class):
        from google.api_core.retry import Retry

        retry = Retry(predicate=object())
        timeout = 123.0
        query_class.return_value.stream.return_value = AsyncIter(range(3))

        collection = self._make_one("collection")
        stream_response = collection.stream(retry=retry, timeout=timeout)

        async for _ in stream_response:
            pass

        query_class.assert_called_once_with(collection)
        query_instance = query_class.return_value
        query_instance.stream.assert_called_once_with(
            transaction=None, retry=retry, timeout=timeout,
        )

    @mock.patch("google.cloud.firestore_v1.async_query.AsyncQuery", autospec=True)
    @pytest.mark.asyncio
    async def test_stream_with_transaction(self, query_class):
        query_class.return_value.stream.return_value = AsyncIter(range(3))

        collection = self._make_one("collection")
        transaction = mock.sentinel.txn
        stream_response = collection.stream(transaction=transaction)

        async for _ in stream_response:
            pass

        query_class.assert_called_once_with(collection)
        query_instance = query_class.return_value
        query_instance.stream.assert_called_once_with(transaction=transaction)


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_client():
    from google.cloud.firestore_v1.async_client import AsyncClient

    credentials = _make_credentials()
    return AsyncClient(project="project-project", credentials=credentials)
