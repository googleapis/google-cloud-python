# Copyright 2017 Google LLC All rights reserved.
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

"""Classes for representing documents for the Google Cloud Firestore API."""

from google.cloud.firestore_v1.base_document import (
    BaseDocumentReference,
    DocumentSnapshot,
    _first_write_result,
)

from google.api_core import exceptions  # type: ignore
from google.cloud.firestore_v1 import _helpers
from google.cloud.firestore_v1.types import common
from google.cloud.firestore_v1.watch import Watch
from typing import Any, Callable, Generator, Iterable


class DocumentReference(BaseDocumentReference):
    """A reference to a document in a Firestore database.

    The document may already exist or can be created by this class.

    Args:
        path (Tuple[str, ...]): The components in the document path.
            This is a series of strings representing each collection and
            sub-collection ID, as well as the document IDs for any documents
            that contain a sub-collection (as well as the base document).
        kwargs (dict): The keyword arguments for the constructor. The only
            supported keyword is ``client`` and it must be a
            :class:`~google.cloud.firestore_v1.client.Client`. It represents
            the client that created this document reference.

    Raises:
        ValueError: if

            * the ``path`` is empty
            * there are an even number of elements
            * a collection ID in ``path`` is not a string
            * a document ID in ``path`` is not a string
        TypeError: If a keyword other than ``client`` is used.
    """

    def __init__(self, *path, **kwargs) -> None:
        super(DocumentReference, self).__init__(*path, **kwargs)

    def create(self, document_data) -> Any:
        """Create the current document in the Firestore database.

        Args:
            document_data (dict): Property names and values to use for
                creating a document.

        Returns:
            :class:`~google.cloud.firestore_v1.types.WriteResult`:
                The write result corresponding to the committed document.
                A write result contains an ``update_time`` field.

        Raises:
            :class:`~google.cloud.exceptions.Conflict`:
                If the document already exists.
        """
        batch = self._client.batch()
        batch.create(self, document_data)
        write_results = batch.commit()
        return _first_write_result(write_results)

    def set(self, document_data: dict, merge: bool = False) -> Any:
        """Replace the current document in the Firestore database.

        A write ``option`` can be specified to indicate preconditions of
        the "set" operation. If no ``option`` is specified and this document
        doesn't exist yet, this method will create it.

        Overwrites all content for the document with the fields in
        ``document_data``. This method performs almost the same functionality
        as :meth:`create`. The only difference is that this method doesn't
        make any requirements on the existence of the document (unless
        ``option`` is used), whereas as :meth:`create` will fail if the
        document already exists.

        Args:
            document_data (dict): Property names and values to use for
                replacing a document.
            merge (Optional[bool] or Optional[List<apispec>]):
                If True, apply merging instead of overwriting the state
                of the document.

        Returns:
            :class:`~google.cloud.firestore_v1.types.WriteResult`:
            The write result corresponding to the committed document. A write
            result contains an ``update_time`` field.
        """
        batch = self._client.batch()
        batch.set(self, document_data, merge=merge)
        write_results = batch.commit()
        return _first_write_result(write_results)

    def update(self, field_updates: dict, option: _helpers.WriteOption = None) -> Any:
        """Update an existing document in the Firestore database.

        By default, this method verifies that the document exists on the
        server before making updates. A write ``option`` can be specified to
        override these preconditions.

        Each key in ``field_updates`` can either be a field name or a
        **field path** (For more information on **field paths**, see
        :meth:`~google.cloud.firestore_v1.client.Client.field_path`.) To
        illustrate this, consider a document with

        .. code-block:: python

           >>> snapshot = document.get()
           >>> snapshot.to_dict()
           {
               'foo': {
                   'bar': 'baz',
               },
               'other': True,
           }

        stored on the server. If the field name is used in the update:

        .. code-block:: python

           >>> field_updates = {
           ...     'foo': {
           ...         'quux': 800,
           ...     },
           ... }
           >>> document.update(field_updates)

        then all of ``foo`` will be overwritten on the server and the new
        value will be

        .. code-block:: python

           >>> snapshot = document.get()
           >>> snapshot.to_dict()
           {
               'foo': {
                   'quux': 800,
               },
               'other': True,
           }

        On the other hand, if a ``.``-delimited **field path** is used in the
        update:

        .. code-block:: python

           >>> field_updates = {
           ...     'foo.quux': 800,
           ... }
           >>> document.update(field_updates)

        then only ``foo.quux`` will be updated on the server and the
        field ``foo.bar`` will remain intact:

        .. code-block:: python

           >>> snapshot = document.get()
           >>> snapshot.to_dict()
           {
               'foo': {
                   'bar': 'baz',
                   'quux': 800,
               },
               'other': True,
           }

        .. warning::

           A **field path** can only be used as a top-level key in
           ``field_updates``.

        To delete / remove a field from an existing document, use the
        :attr:`~google.cloud.firestore_v1.transforms.DELETE_FIELD` sentinel.
        So with the example above, sending

        .. code-block:: python

           >>> field_updates = {
           ...     'other': firestore.DELETE_FIELD,
           ... }
           >>> document.update(field_updates)

        would update the value on the server to:

        .. code-block:: python

           >>> snapshot = document.get()
           >>> snapshot.to_dict()
           {
               'foo': {
                   'bar': 'baz',
               },
           }

        To set a field to the current time on the server when the
        update is received, use the
        :attr:`~google.cloud.firestore_v1.transforms.SERVER_TIMESTAMP`
        sentinel.
        Sending

        .. code-block:: python

           >>> field_updates = {
           ...     'foo.now': firestore.SERVER_TIMESTAMP,
           ... }
           >>> document.update(field_updates)

        would update the value on the server to:

        .. code-block:: python

           >>> snapshot = document.get()
           >>> snapshot.to_dict()
           {
               'foo': {
                   'bar': 'baz',
                   'now': datetime.datetime(2012, ...),
               },
               'other': True,
           }

        Args:
            field_updates (dict): Field names or paths to update and values
                to update with.
            option (Optional[:class:`~google.cloud.firestore_v1.client.WriteOption`]):
                A write option to make assertions / preconditions on the server
                state of the document before applying changes.

        Returns:
            :class:`~google.cloud.firestore_v1.types.WriteResult`:
            The write result corresponding to the updated document. A write
            result contains an ``update_time`` field.

        Raises:
            ~google.cloud.exceptions.NotFound: If the document does not exist.
        """
        batch = self._client.batch()
        batch.update(self, field_updates, option=option)
        write_results = batch.commit()
        return _first_write_result(write_results)

    def delete(self, option: _helpers.WriteOption = None) -> Any:
        """Delete the current document in the Firestore database.

        Args:
            option (Optional[:class:`~google.cloud.firestore_v1.client.WriteOption`]):
                A write option to make assertions / preconditions on the server
                state of the document before applying changes.

        Returns:
            :class:`google.protobuf.timestamp_pb2.Timestamp`:
            The time that the delete request was received by the server.
            If the document did not exist when the delete was sent (i.e.
            nothing was deleted), this method will still succeed and will
            still return the time that the request was received by the server.
        """
        write_pb = _helpers.pb_for_delete(self._document_path, option)
        commit_response = self._client._firestore_api.commit(
            request={
                "database": self._client._database_string,
                "writes": [write_pb],
                "transaction": None,
            },
            metadata=self._client._rpc_metadata,
        )

        return commit_response.commit_time

    def get(
        self, field_paths: Iterable[str] = None, transaction=None
    ) -> DocumentSnapshot:
        """Retrieve a snapshot of the current document.

        See :meth:`~google.cloud.firestore_v1.base_client.BaseClient.field_path` for
        more information on **field paths**.

        If a ``transaction`` is used and it already has write operations
        added, this method cannot be used (i.e. read-after-write is not
        allowed).

        Args:
            field_paths (Optional[Iterable[str, ...]]): An iterable of field
                paths (``.``-delimited list of field names) to use as a
                projection of document fields in the returned results. If
                no value is provided, all fields will be returned.
            transaction (Optional[:class:`~google.cloud.firestore_v1.transaction.Transaction`]):
                An existing transaction that this reference
                will be retrieved in.

        Returns:
            :class:`~google.cloud.firestore_v1.base_document.DocumentSnapshot`:
                A snapshot of the current document. If the document does not
                exist at the time of the snapshot is taken, the snapshot's
                :attr:`reference`, :attr:`data`, :attr:`update_time`, and
                :attr:`create_time` attributes will all be ``None`` and
                its :attr:`exists` attribute will be ``False``.
        """
        if isinstance(field_paths, str):
            raise ValueError("'field_paths' must be a sequence of paths, not a string.")

        if field_paths is not None:
            mask = common.DocumentMask(field_paths=sorted(field_paths))
        else:
            mask = None

        firestore_api = self._client._firestore_api
        try:
            document_pb = firestore_api.get_document(
                request={
                    "name": self._document_path,
                    "mask": mask,
                    "transaction": _helpers.get_transaction_id(transaction),
                },
                metadata=self._client._rpc_metadata,
            )
        except exceptions.NotFound:
            data = None
            exists = False
            create_time = None
            update_time = None
        else:
            data = _helpers.decode_dict(document_pb.fields, self._client)
            exists = True
            create_time = document_pb.create_time
            update_time = document_pb.update_time

        return DocumentSnapshot(
            reference=self,
            data=data,
            exists=exists,
            read_time=None,  # No server read_time available
            create_time=create_time,
            update_time=update_time,
        )

    def collections(self, page_size: int = None) -> Generator[Any, Any, None]:
        """List subcollections of the current document.

        Args:
            page_size (Optional[int]]): The maximum number of collections
            in each page of results from this request. Non-positive values
            are ignored. Defaults to a sensible value set by the API.

        Returns:
            Sequence[:class:`~google.cloud.firestore_v1.collection.CollectionReference`]:
                iterator of subcollections of the current document. If the
                document does not exist at the time of `snapshot`, the
                iterator will be empty
        """
        iterator = self._client._firestore_api.list_collection_ids(
            request={"parent": self._document_path, "page_size": page_size},
            metadata=self._client._rpc_metadata,
        )

        while True:
            for i in iterator.collection_ids:
                yield self.collection(i)
            if iterator.next_page_token:
                iterator = self._client._firestore_api.list_collection_ids(
                    request={
                        "parent": self._document_path,
                        "page_size": page_size,
                        "page_token": iterator.next_page_token,
                    },
                    metadata=self._client._rpc_metadata,
                )
            else:
                return

        # TODO(microgen): currently this method is rewritten to iterate/page itself.
        # it seems the generator ought to be able to do this itself.
        # iterator.document = self
        # iterator.item_to_value = _item_to_collection_ref
        # return iterator

    def on_snapshot(self, callback: Callable) -> Watch:
        """Watch this document.

        This starts a watch on this document using a background thread. The
        provided callback is run on the snapshot.

        Args:
            callback(Callable[[:class:`~google.cloud.firestore.document.DocumentSnapshot`], NoneType]):
                a callback to run when a change occurs

        Example:

        .. code-block:: python

            from google.cloud import firestore_v1

            db = firestore_v1.Client()
            collection_ref = db.collection(u'users')

            def on_snapshot(document_snapshot, changes, read_time):
                doc = document_snapshot
                print(u'{} => {}'.format(doc.id, doc.to_dict()))

            doc_ref = db.collection(u'users').document(
                u'alovelace' + unique_resource_id())

            # Watch this document
            doc_watch = doc_ref.on_snapshot(on_snapshot)

            # Terminate this watch
            doc_watch.unsubscribe()
        """
        return Watch.for_document(self, callback, DocumentSnapshot, DocumentReference)
