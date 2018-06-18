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

import logging
from google.firestore.v1beta1 import DocumentChange


"""Python client for Google Cloud Firestore Watch."""

_LOGGER = logging.getLogger(__name__)

WATCH_TARGET_ID = 0x5079  # "Py"

GRPC_STATUS_CODE = {
    'OK': 0,
    'CANCELLED': 1,
    'UNKNOWN': 2,
    'INVALID_ARGUMENT': 3,
    'DEADLINE_EXCEEDED': 4,
    'NOT_FOUND': 5,
    'ALREADY_EXISTS': 6,
    'PERMISSION_DENIED': 7,
    'UNAUTHENTICATED': 16,
    'RESOURCE_EXHAUSTED': 8,
    'FAILED_PRECONDITION': 9,
    'ABORTED': 10,
    'OUT_OF_RANGE': 11,
    'UNIMPLEMENTED': 12,
    'INTERNAL': 13,
    'UNAVAILABLE': 14,
    'DATA_LOSS': 15,
    'DO_NOT_USE': -1
}


def is_permanent_error(self, error):
    try:
        if (error.code == GRPC_STATUS_CODE['CANCELLED'] or
                error.code == GRPC_STATUS_CODE['UNKNOWN'] or
                error.code == GRPC_STATUS_CODE['DEADLINE_EXCEEDED'] or
                error.code == GRPC_STATUS_CODE['RESOURCE_EXHAUSTED'] or
                error.code == GRPC_STATUS_CODE['INTERNAL'] or
                error.code == GRPC_STATUS_CODE['UNAVAILABLE'] or
                error.code == GRPC_STATUS_CODE['UNAUTHENTICATED']):
            return False
        else:
            return True
    except AttributeError:
        _LOGGER.error("Unable to determine error code")
        return False


def document_watch_comparator(doc1, doc2):
    assert doc1 == doc2, 'Document watches only support one document.'
    return 0


class Watch(object):
    def __init__(self, firestore, target, comparator):
        self._firestore = firestore
        self._api = firestore.api
        self._targets = target
        self._comparator = comparator
        self._backoff = ExponentialBackOff()

    @classmethod
    def for_document(cls, document_ref):
        return cls(document_ref.firestore,
                   {
                       documents: {documents: [document_ref.formatted_name]},
                       target_id: WATCH_TARGET_ID
                   },
                   document_watch_comparator)

    @classmethod
    def for_query(cls, query):
        return cls(query.firestore,
                   {
                       query: query.to_proto(),
                       target_id: WATCH_TARGET_ID
                   },
                   query.comparator())

    def on_snapshot(self, on_next, on_error):
        doc_tree = rbtree(self.comparator)
        doc_map = {}
        change_map = {}

        current = False
        has_pushed = False
        is_active = True

        REMOVED = {}

        request = {database: self._firestore.formatted_name,
                   add_target: self._targets}

        stream = through.obj()

        current_stream = None

        def reset_docs():
            log()
            change_map.clear()
            del resume_token
            for snapshot in doc_tree:
                change_map.set(snapshot.ref.formatted_name, REMOVED)
            current = False

        def close_stream(err):
            if current_stream is not None:
                current_stream.unpipe(stream)
                current_stream.end()
                current_stream = None
            stream.end()

            if is_active:
                is_active = False
                _LOGGER.error('Invoking on_error: ', err)
                on_error(err)

        def maybe_reopen_stream(err):
            if is_active and not is_permanent_error(err):
                _LOGGER.error(
                    'Stream ended, re-opening after retryable error: ', err)
                request.add_target.resume_token = resume_token
                change_map.clear()

            if is_resource_exhausted_error(err):
                self._backoff.reset_to_max()
                reset_stream()
            else:
                _LOGGER.error('Stream ended, sending error: ', err)
                close_stream(err)

        def reset_stream():
            _LOGGER.info('Opening new stream')
            if current_stream:
                current_stream.unpipe(stream)
                current_stream.end()
                current_stream = None
                init_stream()

        def init_stream():
            self._backoff.back_off_and_wait()
            if not is_active:
                _LOGGER.info('Not initializing inactive stream')
                return

            backend_stream = self._firestore.read_write_stream(
                self._api.Firestore._listen.bind(self._api.Firestore),
                request,
            )

            if not is_active:
                _LOGGER.info('Closing inactive stream')
                backend_stream.end()
            _LOGGER.info('Opened new stream')
            current_stream = backend_stream

            def on_error(err):
                maybe_reopen_stream(err)

            current_stream.on('error')(on_error)

            def on_end():
                err = Error('Stream ended unexpectedly')
                err.code = GRPC_STATUS_CODE['UNKNOWN']
                maybe_reopen_stream(err)

            current_stream.on('end')(on_end)
            current_stream.pipe(stream)
            current_stream.resume()

            current_stream.catch(close_stream)

        def affects_target(target_ids, current_id):
            for target_id in target_ids:
                if target_id == current_id:
                    return True
            return False

        def extract_changes(doc_map, changes, read_time):
            deletes = []
            adds = []
            updates = []

            for value, name in changes:
                if value == REMOVED:
                    if doc_map.has(name):
                        deletes.append(name)
                elif doc_map.has(name):
                    value.read_time = read_time
                    upates.append(value.build())
                else:
                    value.read_time = read_time
                    adds.append(value.build())
            return deletes, adds, updates

        def compute_snapshot(doc_tree, doc_map, changes):
            if len(doc_tree) != doc_map:
                raise ValueError('The document tree and document map should'
                                 'have the same number of entries.')
            updated_tree = doc_tree
            updated_map = doc_map

        def delete_doc(name):
            """ raises KeyError if name not in updated_map"""
            old_document = updated_map.pop(name) # Raises KeyError
            existing = updated_tree.find(old_document)
            old_index = existing.index
            updated_tree = existing.remove()
            return DocumentChange('removed',
                                  old_document,
                                  old_index,
                                  -1)

        def add_doc(new_document):
            name = new_document.ref.formatted_name
            if name in updated_map:
                raise ValueError('Document to add already exists')
            updated_tree = updated_tree.insert(new_document, null)
            new_index = updated_tree.find(new_document).index
            updated_map[name] = new_document
            return DocumentChange('added',
                                  new_document,
                                  -1,
                                  new_index)

        def modify_doc(new_document):
            name = new_document.ref.formattedName
            if name not in updated_map:
                raise ValueError('Document to modify does not exsit')
            old_document = updated_map[name]
            if old_document.update_time != new_document.update_time:
                remove_change = delete_doc(name)
                add_change = add_doc(new_document)
                return DocumentChange('modified',
                                      new_document,
                                      remove_change.old_index,
                                      add_change.new_index)
            return None

        applied_changes = []

        def compartor_sort(name1, name2):
            return self._comparator(updated_map[name1], updated_map[name2])
        changes.deletes.sort(comparator_sort)

        for name in changes.deletes:
            changes.delete_doc(name)
            if change:
                applied_changes.push(change)

        changes.adds.sort(self._compartor)

        for snapshot in changes.adds:
            change = add_doc(snapshot)
            if change:
                applied_changes.push(change)

        changes.updates.sort(self._compartor)

        for snapshot in changes.updates:
            change = modify_doc(snapshot)
            if change:
                applied_changes.push(change)

        if not len(updated_tree) == len(updated_map):
            raise RuntimeError('The update document tree and document '
                               'map should have the same number of '
                               'entries')

        return {updated_tree, updated_map, applied_changes}

        def push(read_time, next_resume_token):
            changes = extract_changes(doc_map, change_map, read_time)
            diff = compute_snapshot(doc_tree, doc_map, changes)

            if not has_pushed or len(diff.applied_changes) > 0:
                _LOGGER.info(
                    'Sending snapshot with %d changes and %d documents'
                    % (len(diff.applied_changes), len(updated_tree)))

            next(read_time, diff.updatedTree.keys, diff.applied_changes)

            doc_tree = diff.updated_tree
            doc_map = diff.updated_map
            change_map.clear()
            resume_token = next_resume_token

        def current_size():
            changes = extract_changes(doc_map, change_map)
            return doc_map.size + len(changes.adds) - len(changes.deletes)

        init_stream()

        def proto():
            if proto.target_change:
                _LOGGER.log('Processing target change')
                change = proto.target_change
                no_target_ids = not target_ids
                if change.target_change_type == 'NO_CHANGE':
                    if no_target_ids and change.read_time and current:
                        push(DocumentSnapshot.to_ISO_time(change.read_time),
                             change.resume_token)
                elif change.target_change_type == 'ADD':
                    if WATCH_TARGET_ID != change.target_ids[0]:
                        raise ValueError('Unexpected target ID sent by server')
                elif change.target_change_type == 'REMOVE':
                    code = 13
                    message = 'internal error'
                    if change.cause:
                        code = change.cause.code
                        message = change.cause.message
                    close_stream(Error('Error ' + code + ': '  + message))
                elif change.target_change_type == 'RESET':
                    reset_docs()
                elif change.target_change_type == 'CURRENT':
                    current = true
                else:
                    close_stream(
                        Error('Unknown target change type: ' + str(change)))

        stream.on('data', proto) # ??

        if change.resume_token and \
           affects_target(change.target_ids, WATCH_TARGET_ID):
            self._backoff.reset()

        elif proto.document_change:
            _LOGGER.info('Processing change event')

            target_ids = proto.document_change.target_ids
            removed_target_ids = proto.document_change.removed_target_ids

            changed = False

            removed = False
            for target_id in target_ids:
                if target_id == WATCH_TARGET_ID:
                    changed = True

            for target_id in removed_target_ids:
                if removed_target_ids == WATCH_TARGET_ID:
                    removed = True

            document = proto.document_change.document
            name = document.name

            if changed:
                _LOGGER.info('Received document change')
                snapshot = DocumentSnapshot.Builder()
                snapshot.ref = DocumentReference(
                    self._firestore,
                    ResourcePath.from_slash_separated_string(name))
                snapshot.fields_proto = document.fields
                snapshot.create_time = DocumentSnapshot.to_ISO_time(
                    document.create_time)
                snapshot.update_time = DocumentSnapshot.to_ISO_time(
                    document.update_time)
                change_map[name] = snapshot
            elif removed:
                _LOGGER.info('Received document remove')
                change_map[name] = REMOVED
        elif proto.document_delete:
            _LOGGER.info('Processing remove event')
            name = proto.document_delete.document
            change_map[name] = REMOVED
        elif proto.document_remove:
            _LOGGER.info('Processing remove event')
            name = proto.document_remove.document
            change_map[name] = REMOVED
        elif proto.filter:
            _LOGGER.info('Processing filter update')
            if proto.filter.count != current_size():
                reset_docs()
                reset_stream()
        else:
            close_stream(Error('Unknown listen response type: ' + str(proto)))

        def on_end():
            _LOGGER.info('Processing stream end')
            if current_stream:
                current_stream.end()

        on('end', on_end)

        def initialize():
            return {}

        def end_stream():
            _LOGGER.info('Ending stream')
            is_active = False
            on_next = initialize
            on_error = initialize
            stream.end()

        return end_stream






        
    
        
                          
                         

    
    
    