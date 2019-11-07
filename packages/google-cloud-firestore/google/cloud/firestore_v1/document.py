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

import copy

import six

from google.api_core import exceptions
from google.cloud.firestore_v1 import _helpers
from google.cloud.firestore_v1 import field_path as field_path_module
from google.cloud.firestore_v1.proto import common_pb2
from google.cloud.firestore_v1.watch import Watch


class DocumentReference(object):
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

    _document_path_internal = None

    def __init__(self, *path, **kwargs):
        _helpers.verify_path(path, is_collection=False)
        self._path = path
        self._client = kwargs.pop("client", None)
        if kwargs:
            raise TypeError(
                "Received unexpected arguments", kwargs, "Only `client` is supported"
            )

    def __copy__(self):
        """Shallow copy the instance.

        We leave the client "as-is" but tuple-unpack the path.

        Returns:
            .DocumentReference: A copy of the current document.
        """
        result = self.__class__(*self._path, client=self._client)
        result._document_path_internal = self._document_path_internal
        return result

    def __deepcopy__(self, unused_memo):
        """Deep copy the instance.

        This isn't a true deep copy, wee leave the client "as-is" but
        tuple-unpack the path.

        Returns:
            .DocumentReference: A copy of the current document.
        """
        return self.__copy__()

    def __eq__(self, other):
        """Equality check against another instance.

        Args:
            other (Any): A value to compare against.

        Returns:
            Union[bool, NotImplementedType]: Indicating if the values are
            equal.
        """
        if isinstance(other, DocumentReference):
            return self._client == other._client and self._path == other._path
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self._path) + hash(self._client)

    def __ne__(self, other):
        """Inequality check against another instance.

        Args:
            other (Any): A value to compare against.

        Returns:
            Union[bool, NotImplementedType]: Indicating if the values are
            not equal.
        """
        if isinstance(other, DocumentReference):
            return self._client != other._client or self._path != other._path
        else:
            return NotImplemented

    @property
    def path(self):
        """Database-relative for this document.

        Returns:
            str: The document's relative path.
        """
        return "/".join(self._path)

    @property
    def _document_path(self):
        """Create and cache the full path for this document.

        Of the form:

            ``projects/{project_id}/databases/{database_id}/...
                  documents/{document_path}``

        Returns:
            str: The full document path.

        Raises:
            ValueError: If the current document reference has no ``client``.
        """
        if self._document_path_internal is None:
            if self._client is None:
                raise ValueError("A document reference requires a `client`.")
            self._document_path_internal = _get_document_path(self._client, self._path)

        return self._document_path_internal

    @property
    def id(self):
        """The document identifier (within its collection).

        Returns:
            str: The last component of the path.
        """
        return self._path[-1]

    @property
    def parent(self):
        """Collection that owns the current document.

        Returns:
            :class:`~google.cloud.firestore_v1.collection.CollectionReference`:
            The parent collection.
        """
        parent_path = self._path[:-1]
        return self._client.collection(*parent_path)

    def collection(self, collection_id):
        """Create a sub-collection underneath the current document.

        Args:
            collection_id (str): The sub-collection identifier (sometimes
                referred to as the "kind").

        Returns:
            :class:`~google.cloud.firestore_v1.collection.CollectionReference`:
            The child collection.
        """
        child_path = self._path + (collection_id,)
        return self._client.collection(*child_path)

    def create(self, document_data):
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

    def set(self, document_data, merge=False):
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

    def update(self, field_updates, option=None):
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

    def delete(self, option=None):
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
            self._client._database_string,
            [write_pb],
            transaction=None,
            metadata=self._client._rpc_metadata,
        )

        return commit_response.commit_time

    def get(self, field_paths=None, transaction=None):
        """Retrieve a snapshot of the current document.

        See :meth:`~google.cloud.firestore_v1.client.Client.field_path` for
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
            :class:`~google.cloud.firestore_v1.document.DocumentSnapshot`:
                A snapshot of the current document. If the document does not
                exist at the time of the snapshot is taken, the snapshot's
                :attr:`reference`, :attr:`data`, :attr:`update_time`, and
                :attr:`create_time` attributes will all be ``None`` and
                its :attr:`exists` attribute will be ``False``.
        """
        if isinstance(field_paths, six.string_types):
            raise ValueError("'field_paths' must be a sequence of paths, not a string.")

        if field_paths is not None:
            mask = common_pb2.DocumentMask(field_paths=sorted(field_paths))
        else:
            mask = None

        firestore_api = self._client._firestore_api
        try:
            document_pb = firestore_api.get_document(
                self._document_path,
                mask=mask,
                transaction=_helpers.get_transaction_id(transaction),
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

    def collections(self, page_size=None):
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
            self._document_path,
            page_size=page_size,
            metadata=self._client._rpc_metadata,
        )
        iterator.document = self
        iterator.item_to_value = _item_to_collection_ref
        return iterator

    def on_snapshot(self, callback):
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


class DocumentSnapshot(object):
    """A snapshot of document data in a Firestore database.

    This represents data retrieved at a specific time and may not contain
    all fields stored for the document (i.e. a hand-picked selection of
    fields may have been retrieved).

    Instances of this class are not intended to be constructed by hand,
    rather they'll be returned as responses to various methods, such as
    :meth:`~google.cloud.DocumentReference.get`.

    Args:
        reference (:class:`~google.cloud.firestore_v1.document.DocumentReference`):
            A document reference corresponding to the document that contains
            the data in this snapshot.
        data (Dict[str, Any]):
            The data retrieved in the snapshot.
        exists (bool):
            Indicates if the document existed at the time the snapshot was
            retrieved.
        read_time (:class:`google.protobuf.timestamp_pb2.Timestamp`):
            The time that this snapshot was read from the server.
        create_time (:class:`google.protobuf.timestamp_pb2.Timestamp`):
            The time that this document was created.
        update_time (:class:`google.protobuf.timestamp_pb2.Timestamp`):
            The time that this document was last updated.
    """

    def __init__(self, reference, data, exists, read_time, create_time, update_time):
        self._reference = reference
        # We want immutable data, so callers can't modify this value
        # out from under us.
        self._data = copy.deepcopy(data)
        self._exists = exists
        self.read_time = read_time
        self.create_time = create_time
        self.update_time = update_time

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._reference == other._reference and self._data == other._data

    def __hash__(self):
        seconds = self.update_time.seconds
        nanos = self.update_time.nanos
        return hash(self._reference) + hash(seconds) + hash(nanos)

    @property
    def _client(self):
        """The client that owns the document reference for this snapshot.

        Returns:
            :class:`~google.cloud.firestore_v1.client.Client`:
            The client that owns this document.
        """
        return self._reference._client

    @property
    def exists(self):
        """Existence flag.

        Indicates if the document existed at the time this snapshot
        was retrieved.

        Returns:
            bool: The existence flag.
        """
        return self._exists

    @property
    def id(self):
        """The document identifier (within its collection).

        Returns:
            str: The last component of the path of the document.
        """
        return self._reference.id

    @property
    def reference(self):
        """Document reference corresponding to document that owns this data.

        Returns:
            :class:`~google.cloud.firestore_v1.document.DocumentReference`:
            A document reference corresponding to this document.
        """
        return self._reference

    def get(self, field_path):
        """Get a value from the snapshot data.

        If the data is nested, for example:

        .. code-block:: python

           >>> snapshot.to_dict()
           {
               'top1': {
                   'middle2': {
                       'bottom3': 20,
                       'bottom4': 22,
                   },
                   'middle5': True,
               },
               'top6': b'\x00\x01 foo',
           }

        a **field path** can be used to access the nested data. For
        example:

        .. code-block:: python

           >>> snapshot.get('top1')
           {
               'middle2': {
                   'bottom3': 20,
                   'bottom4': 22,
               },
               'middle5': True,
           }
           >>> snapshot.get('top1.middle2')
           {
               'bottom3': 20,
               'bottom4': 22,
           }
           >>> snapshot.get('top1.middle2.bottom3')
           20

        See :meth:`~google.cloud.firestore_v1.client.Client.field_path` for
        more information on **field paths**.

        A copy is returned since the data may contain mutable values,
        but the data stored in the snapshot must remain immutable.

        Args:
            field_path (str): A field path (``.``-delimited list of
                field names).

        Returns:
            Any or None:
                (A copy of) the value stored for the ``field_path`` or
                None if snapshot document does not exist.

        Raises:
            KeyError: If the ``field_path`` does not match nested data
                in the snapshot.
        """
        if not self._exists:
            return None
        nested_data = field_path_module.get_nested_value(field_path, self._data)
        return copy.deepcopy(nested_data)

    def to_dict(self):
        """Retrieve the data contained in this snapshot.

        A copy is returned since the data may contain mutable values,
        but the data stored in the snapshot must remain immutable.

        Returns:
            Dict[str, Any] or None:
                The data in the snapshot.  Returns None if reference
                does not exist.
        """
        if not self._exists:
            return None
        return copy.deepcopy(self._data)


def _get_document_path(client, path):
    """Convert a path tuple into a full path string.

    Of the form:

        ``projects/{project_id}/databases/{database_id}/...
              documents/{document_path}``

    Args:
        client (:class:`~google.cloud.firestore_v1.client.Client`):
            The client that holds configuration details and a GAPIC client
            object.
        path (Tuple[str, ...]): The components in a document path.

    Returns:
        str: The fully-qualified document path.
    """
    parts = (client._database_string, "documents") + path
    return _helpers.DOCUMENT_PATH_DELIMITER.join(parts)


def _consume_single_get(response_iterator):
    """Consume a gRPC stream that should contain a single response.

    The stream will correspond to a ``BatchGetDocuments`` request made
    for a single document.

    Args:
        response_iterator (~google.cloud.exceptions.GrpcRendezvous): A
            streaming iterator returned from a ``BatchGetDocuments``
            request.

    Returns:
        ~google.cloud.proto.firestore.v1.\
            firestore_pb2.BatchGetDocumentsResponse: The single "get"
        response in the batch.

    Raises:
        ValueError: If anything other than exactly one response is returned.
    """
    # Calling ``list()`` consumes the entire iterator.
    all_responses = list(response_iterator)
    if len(all_responses) != 1:
        raise ValueError(
            "Unexpected response from `BatchGetDocumentsResponse`",
            all_responses,
            "Expected only one result",
        )

    return all_responses[0]


def _first_write_result(write_results):
    """Get first write result from list.

    For cases where ``len(write_results) > 1``, this assumes the writes
    occurred at the same time (e.g. if an update and transform are sent
    at the same time).

    Args:
        write_results (List[google.cloud.proto.firestore.v1.\
            write_pb2.WriteResult, ...]: The write results from a
            ``CommitResponse``.

    Returns:
        google.cloud.firestore_v1.types.WriteResult: The
        lone write result from ``write_results``.

    Raises:
        ValueError: If there are zero write results. This is likely to
            **never** occur, since the backend should be stable.
    """
    if not write_results:
        raise ValueError("Expected at least one write result")

    return write_results[0]


def _item_to_collection_ref(iterator, item):
    """Convert collection ID to collection ref.

    Args:
        iterator (google.api_core.page_iterator.GRPCIterator):
            iterator response
        item (str): ID of the collection
    """
    return iterator.document.collection(item)
