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

"""Client for interacting with the Google Cloud Firestore API.

This is the base from which all interactions with the API occur.

In the hierarchy of API concepts

* a :class:`~.firestore_v1beta1.client.Client` owns a
  :class:`~.firestore_v1beta1.collection.CollectionReference`
* a :class:`~.firestore_v1beta1.client.Client` owns a
  :class:`~.firestore_v1beta1.document.DocumentReference`
"""
from google.cloud.client import ClientWithProject

from google.cloud.firestore_v1beta1 import _helpers
from google.cloud.firestore_v1beta1 import types
from google.cloud.firestore_v1beta1.batch import WriteBatch
from google.cloud.firestore_v1beta1.collection import CollectionReference
from google.cloud.firestore_v1beta1.document import DocumentReference
from google.cloud.firestore_v1beta1.document import DocumentSnapshot
from google.cloud.firestore_v1beta1.field_path import render_field_path
from google.cloud.firestore_v1beta1.gapic import firestore_client
from google.cloud.firestore_v1beta1.transaction import Transaction


DEFAULT_DATABASE = "(default)"
"""str: The default database used in a :class:`~.firestore.client.Client`."""
_BAD_OPTION_ERR = (
    "Exactly one of ``last_update_time`` or ``exists`` " "must be provided."
)
_BAD_DOC_TEMPLATE = (
    "Document {!r} appeared in response but was not present among references"
)
_ACTIVE_TXN = "There is already an active transaction."
_INACTIVE_TXN = "There is no active transaction."


class Client(ClientWithProject):
    """Client for interacting with Google Cloud Firestore API.

    .. note::

        Since the Cloud Firestore API requires the gRPC transport, no
        ``_http`` argument is accepted by this class.

    Args:
        project (Optional[str]): The project which the client acts on behalf
            of. If not passed, falls back to the default inferred
            from the environment.
        credentials (Optional[~google.auth.credentials.Credentials]): The
            OAuth2 Credentials to use for this client. If not passed, falls
            back to the default inferred from the environment.
        database (Optional[str]): The database name that the client targets.
            For now, :attr:`DEFAULT_DATABASE` (the default value) is the
            only valid database.
    """

    SCOPE = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/datastore",
    )
    """The scopes required for authenticating with the Firestore service."""

    _firestore_api_internal = None
    _database_string_internal = None
    _rpc_metadata_internal = None

    def __init__(self, project=None, credentials=None, database=DEFAULT_DATABASE):
        # NOTE: This API has no use for the _http argument, but sending it
        #       will have no impact since the _http() @property only lazily
        #       creates a working HTTP object.
        super(Client, self).__init__(
            project=project, credentials=credentials, _http=None
        )
        self._database = database

    @property
    def _firestore_api(self):
        """Lazy-loading getter GAPIC Firestore API.

        Returns:
            ~.gapic.firestore.v1beta1.firestore_client.FirestoreClient: The
            GAPIC client with the credentials of the current client.
        """
        if self._firestore_api_internal is None:
            self._firestore_api_internal = firestore_client.FirestoreClient(
                credentials=self._credentials
            )

        return self._firestore_api_internal

    @property
    def _database_string(self):
        """The database string corresponding to this client's project.

        This value is lazy-loaded and cached.

        Will be of the form

            ``projects/{project_id}/databases/{database_id}``

        but ``database_id == '(default)'`` for the time being.

        Returns:
            str: The fully-qualified database string for the current
            project. (The default database is also in this string.)
        """
        if self._database_string_internal is None:
            # NOTE: database_root_path() is a classmethod, so we don't use
            #       self._firestore_api (it isn't necessary).
            db_str = firestore_client.FirestoreClient.database_root_path(
                self.project, self._database
            )
            self._database_string_internal = db_str

        return self._database_string_internal

    @property
    def _rpc_metadata(self):
        """The RPC metadata for this client's associated database.

        Returns:
            Sequence[Tuple(str, str)]: RPC metadata with resource prefix
            for the database associated with this client.
        """
        if self._rpc_metadata_internal is None:
            self._rpc_metadata_internal = _helpers.metadata_with_prefix(
                self._database_string
            )

        return self._rpc_metadata_internal

    def collection(self, *collection_path):
        """Get a reference to a collection.

        For a top-level collection:

        .. code-block:: python

            >>> client.collection('top')

        For a sub-collection:

        .. code-block:: python

            >>> client.collection('mydocs/doc/subcol')
            >>> # is the same as
            >>> client.collection('mydocs', 'doc', 'subcol')

        Sub-collections can be nested deeper in a similar fashion.

        Args:
            collection_path (Tuple[str, ...]): Can either be

                * A single ``/``-delimited path to a collection
                * A tuple of collection path segments

        Returns:
            ~.firestore_v1beta1.collection.CollectionReference: A reference
            to a collection in the Firestore database.
        """
        if len(collection_path) == 1:
            path = collection_path[0].split(_helpers.DOCUMENT_PATH_DELIMITER)
        else:
            path = collection_path

        return CollectionReference(*path, client=self)

    def document(self, *document_path):
        """Get a reference to a document in a collection.

        For a top-level document:

        .. code-block:: python

            >>> client.document('collek/shun')
            >>> # is the same as
            >>> client.document('collek', 'shun')

        For a document in a sub-collection:

        .. code-block:: python

            >>> client.document('mydocs/doc/subcol/child')
            >>> # is the same as
            >>> client.document('mydocs', 'doc', 'subcol', 'child')

        Documents in sub-collections can be nested deeper in a similar fashion.

        Args:
            document_path (Tuple[str, ...]): Can either be

                * A single ``/``-delimited path to a document
                * A tuple of document path segments

        Returns:
            ~.firestore_v1beta1.document.DocumentReference: A reference
            to a document in a collection.
        """
        if len(document_path) == 1:
            path = document_path[0].split(_helpers.DOCUMENT_PATH_DELIMITER)
        else:
            path = document_path

        return DocumentReference(*path, client=self)

    @staticmethod
    def field_path(*field_names):
        """Create a **field path** from a list of nested field names.

        A **field path** is a ``.``-delimited concatenation of the field
        names. It is used to represent a nested field. For example,
        in the data

        .. code-block:: python

           data = {
              'aa': {
                  'bb': {
                      'cc': 10,
                  },
              },
           }

        the field path ``'aa.bb.cc'`` represents the data stored in
        ``data['aa']['bb']['cc']``.

        Args:
            field_names (Tuple[str, ...]): The list of field names.

        Returns:
            str: The ``.``-delimited field path.
        """
        return render_field_path(field_names)

    @staticmethod
    def write_option(**kwargs):
        """Create a write option for write operations.

        Write operations include :meth:`~.DocumentReference.set`,
        :meth:`~.DocumentReference.update` and
        :meth:`~.DocumentReference.delete`.

        One of the following keyword arguments must be provided:

        * ``last_update_time`` (:class:`google.protobuf.timestamp_pb2.\
               Timestamp`): A timestamp. When set, the target document must
               exist and have been last updated at that time. Protobuf
               ``update_time`` timestamps are typically returned from methods
               that perform write operations as part of a "write result"
               protobuf or directly.
        * ``exists`` (:class:`bool`): Indicates if the document being modified
              should already exist.

        Providing no argument would make the option have no effect (so
        it is not allowed). Providing multiple would be an apparent
        contradiction, since ``last_update_time`` assumes that the
        document **was** updated (it can't have been updated if it
        doesn't exist) and ``exists`` indicate that it is unknown if the
        document exists or not.

        Args:
            kwargs (Dict[str, Any]): The keyword arguments described above.

        Raises:
            TypeError: If anything other than exactly one argument is
                provided by the caller.
        """
        if len(kwargs) != 1:
            raise TypeError(_BAD_OPTION_ERR)

        name, value = kwargs.popitem()
        if name == "last_update_time":
            return _helpers.LastUpdateOption(value)
        elif name == "exists":
            return _helpers.ExistsOption(value)
        else:
            extra = "{!r} was provided".format(name)
            raise TypeError(_BAD_OPTION_ERR, extra)

    def get_all(self, references, field_paths=None, transaction=None):
        """Retrieve a batch of documents.

        .. note::

           Documents returned by this method are not guaranteed to be
           returned in the same order that they are given in ``references``.

        .. note::

           If multiple ``references`` refer to the same document, the server
           will only return one result.

        See :meth:`~.firestore_v1beta1.client.Client.field_path` for
        more information on **field paths**.

        If a ``transaction`` is used and it already has write operations
        added, this method cannot be used (i.e. read-after-write is not
        allowed).

        Args:
            references (List[.DocumentReference, ...]): Iterable of document
                references to be retrieved.
            field_paths (Optional[Iterable[str, ...]]): An iterable of field
                paths (``.``-delimited list of field names) to use as a
                projection of document fields in the returned results. If
                no value is provided, all fields will be returned.
            transaction (Optional[~.firestore_v1beta1.transaction.\
                Transaction]): An existing transaction that these
                ``references`` will be retrieved in.

        Yields:
            .DocumentSnapshot: The next document snapshot that fulfills the
            query, or :data:`None` if the document does not exist.
        """
        document_paths, reference_map = _reference_info(references)
        mask = _get_doc_mask(field_paths)
        response_iterator = self._firestore_api.batch_get_documents(
            self._database_string,
            document_paths,
            mask,
            transaction=_helpers.get_transaction_id(transaction),
            metadata=self._rpc_metadata,
        )

        for get_doc_response in response_iterator:
            yield _parse_batch_get(get_doc_response, reference_map, self)

    def collections(self):
        """List top-level collections of the client's database.

        Returns:
            Sequence[~.firestore_v1beta1.collection.CollectionReference]:
                iterator of subcollections of the current document.
        """
        iterator = self._firestore_api.list_collection_ids(
            self._database_string, metadata=self._rpc_metadata
        )
        iterator.client = self
        iterator.item_to_value = _item_to_collection_ref
        return iterator

    def batch(self):
        """Get a batch instance from this client.

        Returns:
            ~.firestore_v1beta1.batch.WriteBatch: A "write" batch to be
            used for accumulating document changes and sending the changes
            all at once.
        """
        return WriteBatch(self)

    def transaction(self, **kwargs):
        """Get a transaction that uses this client.

        See :class:`~.firestore_v1beta1.transaction.Transaction` for
        more information on transactions and the constructor arguments.

        Args:
            kwargs (Dict[str, Any]): The keyword arguments (other than
                ``client``) to pass along to the
                :class:`~.firestore_v1beta1.transaction.Transaction`
                constructor.

        Returns:
            ~.firestore_v1beta1.transaction.Transaction: A transaction
            attached to this client.
        """
        return Transaction(self, **kwargs)


def _reference_info(references):
    """Get information about document references.

    Helper for :meth:`~.firestore_v1beta1.client.Client.get_all`.

    Args:
        references (List[.DocumentReference, ...]): Iterable of document
            references.

    Returns:
        Tuple[List[str, ...], Dict[str, .DocumentReference]]: A two-tuple of

        * fully-qualified documents paths for each reference in ``references``
        * a mapping from the paths to the original reference. (If multiple
          ``references`` contains multiple references to the same document,
          that key will be overwritten in the result.)
    """
    document_paths = []
    reference_map = {}
    for reference in references:
        doc_path = reference._document_path
        document_paths.append(doc_path)
        reference_map[doc_path] = reference

    return document_paths, reference_map


def _get_reference(document_path, reference_map):
    """Get a document reference from a dictionary.

    This just wraps a simple dictionary look-up with a helpful error that is
    specific to :meth:`~.firestore.client.Client.get_all`, the
    **public** caller of this function.

    Args:
        document_path (str): A fully-qualified document path.
        reference_map (Dict[str, .DocumentReference]): A mapping (produced
            by :func:`_reference_info`) of fully-qualified document paths to
            document references.

    Returns:
        .DocumentReference: The matching reference.

    Raises:
        ValueError: If ``document_path`` has not been encountered.
    """
    try:
        return reference_map[document_path]
    except KeyError:
        msg = _BAD_DOC_TEMPLATE.format(document_path)
        raise ValueError(msg)


def _parse_batch_get(get_doc_response, reference_map, client):
    """Parse a `BatchGetDocumentsResponse` protobuf.

    Args:
        get_doc_response (~google.cloud.proto.firestore.v1beta1.\
            firestore_pb2.BatchGetDocumentsResponse): A single response (from
            a stream) containing the "get" response for a document.
        reference_map (Dict[str, .DocumentReference]): A mapping (produced
            by :func:`_reference_info`) of fully-qualified document paths to
            document references.
        client (~.firestore_v1beta1.client.Client): A client that has
            a document factory.

    Returns:
       [.DocumentSnapshot]: The retrieved snapshot.

    Raises:
        ValueError: If the response has a ``result`` field (a oneof) other
            than ``found`` or ``missing``.
    """
    result_type = get_doc_response.WhichOneof("result")
    if result_type == "found":
        reference = _get_reference(get_doc_response.found.name, reference_map)
        data = _helpers.decode_dict(get_doc_response.found.fields, client)
        snapshot = DocumentSnapshot(
            reference,
            data,
            exists=True,
            read_time=get_doc_response.read_time,
            create_time=get_doc_response.found.create_time,
            update_time=get_doc_response.found.update_time,
        )
    elif result_type == "missing":
        snapshot = DocumentSnapshot(
            None,
            None,
            exists=False,
            read_time=get_doc_response.read_time,
            create_time=None,
            update_time=None,
        )
    else:
        raise ValueError(
            "`BatchGetDocumentsResponse.result` (a oneof) had a field other "
            "than `found` or `missing` set, or was unset"
        )
    return snapshot


def _get_doc_mask(field_paths):
    """Get a document mask if field paths are provided.

    Args:
        field_paths (Optional[Iterable[str, ...]]): An iterable of field
            paths (``.``-delimited list of field names) to use as a
            projection of document fields in the returned results.

    Returns:
        Optional[google.cloud.firestore_v1beta1.types.DocumentMask]: A mask
            to project documents to a restricted set of field paths.
    """
    if field_paths is None:
        return None
    else:
        return types.DocumentMask(field_paths=field_paths)


def _item_to_collection_ref(iterator, item):
    """Convert collection ID to collection ref.

    Args:
        iterator (google.api_core.page_iterator.GRPCIterator):
            iterator response
        item (str): ID of the collection
    """
    return iterator.client.collection(item)
