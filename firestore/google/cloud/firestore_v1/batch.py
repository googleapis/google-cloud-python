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

"""Helpers for batch requests to the Google Cloud Firestore API."""


from google.cloud.firestore_v1 import _helpers


class WriteBatch(object):
    """Accumulate write operations to be sent in a batch.

    This has the same set of methods for write operations that
    :class:`~google.cloud.firestore_v1.document.DocumentReference` does,
    e.g. :meth:`~google.cloud.firestore_v1.document.DocumentReference.create`.

    Args:
        client (:class:`~google.cloud.firestore_v1.client.Client`):
            The client that created this batch.
    """

    def __init__(self, client):
        self._client = client
        self._write_pbs = []
        self.write_results = None
        self.commit_time = None

    def _add_write_pbs(self, write_pbs):
        """Add `Write`` protobufs to this transaction.

        This method intended to be over-ridden by subclasses.

        Args:
            write_pbs (List[google.cloud.proto.firestore.v1.\
                write_pb2.Write]): A list of write protobufs to be added.
        """
        self._write_pbs.extend(write_pbs)

    def create(self, reference, document_data):
        """Add a "change" to this batch to create a document.

        If the document given by ``reference`` already exists, then this
        batch will fail when :meth:`commit`-ed.

        Args:
            reference (:class:`~google.cloud.firestore_v1.document.DocumentReference`):
                A document reference to be created in this batch.
            document_data (dict): Property names and values to use for
                creating a document.
        """
        write_pbs = _helpers.pbs_for_create(reference._document_path, document_data)
        self._add_write_pbs(write_pbs)

    def set(self, reference, document_data, merge=False):
        """Add a "change" to replace a document.

        See
        :meth:`google.cloud.firestore_v1.document.DocumentReference.set` for
        more information on how ``option`` determines how the change is
        applied.

        Args:
            reference (:class:`~google.cloud.firestore_v1.document.DocumentReference`):
                A document reference that will have values set in this batch.
            document_data (dict):
                Property names and values to use for replacing a document.
            merge (Optional[bool] or Optional[List<apispec>]):
                If True, apply merging instead of overwriting the state
                of the document.
        """
        if merge is not False:
            write_pbs = _helpers.pbs_for_set_with_merge(
                reference._document_path, document_data, merge
            )
        else:
            write_pbs = _helpers.pbs_for_set_no_merge(
                reference._document_path, document_data
            )

        self._add_write_pbs(write_pbs)

    def update(self, reference, field_updates, option=None):
        """Add a "change" to update a document.

        See
        :meth:`google.cloud.firestore_v1.document.DocumentReference.update`
        for more information on ``field_updates`` and ``option``.

        Args:
            reference (:class:`~google.cloud.firestore_v1.document.DocumentReference`):
                A document reference that will be updated in this batch.
            field_updates (dict):
                Field names or paths to update and values to update with.
            option (Optional[:class:`~google.cloud.firestore_v1.client.WriteOption`]):
                A write option to make assertions / preconditions on the server
                state of the document before applying changes.
        """
        if option.__class__.__name__ == "ExistsOption":
            raise ValueError("you must not pass an explicit write option to " "update.")
        write_pbs = _helpers.pbs_for_update(
            reference._document_path, field_updates, option
        )
        self._add_write_pbs(write_pbs)

    def delete(self, reference, option=None):
        """Add a "change" to delete a document.

        See
        :meth:`google.cloud.firestore_v1.document.DocumentReference.delete`
        for more information on how ``option`` determines how the change is
        applied.

        Args:
            reference (:class:`~google.cloud.firestore_v1.document.DocumentReference`):
                A document reference that will be deleted in this batch.
            option (Optional[:class:`~google.cloud.firestore_v1.client.WriteOption`]):
                A write option to make assertions / preconditions on the server
                state of the document before applying changes.
        """
        write_pb = _helpers.pb_for_delete(reference._document_path, option)
        self._add_write_pbs([write_pb])

    def commit(self):
        """Commit the changes accumulated in this batch.

        Returns:
            List[:class:`google.cloud.proto.firestore.v1.write_pb2.WriteResult`, ...]:
            The write results corresponding to the changes committed, returned
            in the same order as the changes were applied to this batch. A
            write result contains an ``update_time`` field.
        """
        commit_response = self._client._firestore_api.commit(
            self._client._database_string,
            self._write_pbs,
            transaction=None,
            metadata=self._client._rpc_metadata,
        )

        self._write_pbs = []
        self.write_results = results = list(commit_response.write_results)
        self.commit_time = commit_response.commit_time
        return results

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
