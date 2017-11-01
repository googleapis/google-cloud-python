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
import math
import operator
import os
import re

from google.auth._default import _load_credentials_from_file
from google.gax.errors import GaxError
from google.gax.grpc import exc_to_code
from google.protobuf import timestamp_pb2
from grpc import StatusCode
import pytest
import six

from google.cloud._helpers import _pb_timestamp_to_datetime
from google.cloud._helpers import UTC
from google.cloud.exceptions import Conflict
from google.cloud.exceptions import NotFound
from google.cloud import firestore
from test_utils.system import unique_resource_id


FIRESTORE_CREDS = os.environ.get('FIRESTORE_APPLICATION_CREDENTIALS')
RANDOM_ID_REGEX = re.compile('^[a-zA-Z0-9]{20}$')
MISSING_ENTITY = 'no entity to update: '
ALREADY_EXISTS = 'entity already exists: '


@pytest.fixture(scope=u'module')
def client():
    credentials, project = _load_credentials_from_file(FIRESTORE_CREDS)
    yield firestore.Client(project=project, credentials=credentials)


@pytest.fixture
def cleanup():
    to_delete = []
    yield to_delete.append

    for document in to_delete:
        document.delete()


def test_create_document(client, cleanup):
    now = datetime.datetime.utcnow().replace(tzinfo=UTC)
    document_id = 'shun' + unique_resource_id('-')
    document = client.document('collek', document_id)
    # Add to clean-up before API request (in case ``create()`` fails).
    cleanup(document)

    data = {
        'now': firestore.SERVER_TIMESTAMP,
        'eenta-ger': 11,
        'bites': b'\xe2\x98\x83 \xe2\x9b\xb5',
        'also': {
            'nestednow': firestore.SERVER_TIMESTAMP,
            'quarter': 0.25,
        },
    }
    write_result = document.create(data)
    updated = _pb_timestamp_to_datetime(write_result.update_time)
    delta = updated - now
    # Allow a bit of clock skew, but make sure timestamps are close.
    assert -300.0 < delta.total_seconds() < 300.0

    with pytest.raises(Conflict) as exc_info:
        document.create({})

    assert exc_info.value.message.startswith(ALREADY_EXISTS)
    assert document_id in exc_info.value.message

    # Verify the server times.
    snapshot = document.get()
    stored_data = snapshot.to_dict()
    server_now = stored_data['now']

    delta = updated - server_now
    # NOTE: We could check the ``transform_results`` from the write result
    #       for the document transform, but this value gets dropped. Instead
    #       we make sure the timestamps are close.
    assert 0.0 <= delta.total_seconds() < 5.0
    expected_data = {
        'now': server_now,
        'eenta-ger': data['eenta-ger'],
        'bites': data['bites'],
        'also': {
            'nestednow': server_now,
            'quarter': data['also']['quarter'],
        },
    }
    assert stored_data == expected_data


def test_cannot_use_foreign_key(client, cleanup):
    document_id = 'cannot' + unique_resource_id('-')
    document = client.document('foreign-key', document_id)
    # Add to clean-up before API request (in case ``create()`` fails).
    cleanup(document)

    other_client = firestore.Client(
        project='other-prahj',
        credentials=client._credentials,
        database='dee-bee')
    assert other_client._database_string != client._database_string
    fake_doc = other_client.document('foo', 'bar')
    # NOTE: google-gax **does not** raise a GaxError for INVALID_ARGUMENT.
    with pytest.raises(ValueError) as exc_info:
        document.create({'ref': fake_doc})

    assert len(exc_info.value.args) == 1
    err_msg = exc_info.value.args[0]
    assert err_msg == 'RPC failed'


def assert_timestamp_less(timestamp_pb1, timestamp_pb2):
    dt_val1 = _pb_timestamp_to_datetime(timestamp_pb1)
    dt_val2 = _pb_timestamp_to_datetime(timestamp_pb2)
    assert dt_val1 < dt_val2


def test_document_set(client, cleanup):
    document_id = 'for-set' + unique_resource_id('-')
    document = client.document('i-did-it', document_id)
    # Add to clean-up before API request (in case ``set()`` fails).
    cleanup(document)

    # 0. Make sure the document doesn't exist yet using an option.
    option0 = client.write_option(create_if_missing=False)
    with pytest.raises(NotFound) as exc_info:
        document.set({'no': 'way'}, option=option0)

    assert exc_info.value.message.startswith(MISSING_ENTITY)
    assert document_id in exc_info.value.message

    # 1. Use ``set()`` to create the document (using an option).
    data1 = {'foo': 88}
    option1 = client.write_option(create_if_missing=True)
    write_result1 = document.set(data1, option=option1)
    snapshot1 = document.get()
    assert snapshot1.to_dict() == data1
    # Make sure the update is what created the document.
    assert snapshot1.create_time == snapshot1.update_time
    assert snapshot1.update_time == write_result1.update_time

    # 2. Call ``set()`` again to overwrite (no option).
    data2 = {'bar': None}
    write_result2 = document.set(data2)
    snapshot2 = document.get()
    assert snapshot2.to_dict() == data2
    # Make sure the create time hasn't changed.
    assert snapshot2.create_time == snapshot1.create_time
    assert snapshot2.update_time == write_result2.update_time

    # 3. Call ``set()`` with a valid "last timestamp" option.
    data3 = {'skates': 88}
    option3 = client.write_option(last_update_time=snapshot2.update_time)
    write_result3 = document.set(data3, option=option3)
    snapshot3 = document.get()
    assert snapshot3.to_dict() == data3
    # Make sure the create time hasn't changed.
    assert snapshot3.create_time == snapshot1.create_time
    assert snapshot3.update_time == write_result3.update_time

    # 4. Call ``set()`` with invalid (in the past) "last timestamp" option.
    assert_timestamp_less(option3._last_update_time, snapshot3.update_time)
    with pytest.raises(GaxError) as exc_info:
        document.set({'bad': 'time-past'}, option=option3)

    assert exc_to_code(exc_info.value.cause) == StatusCode.FAILED_PRECONDITION

    # 5. Call ``set()`` with invalid (in the future) "last timestamp" option.
    timestamp_pb = timestamp_pb2.Timestamp(
        seconds=snapshot3.update_time.nanos + 120,
        nanos=snapshot3.update_time.nanos,
    )
    option5 = client.write_option(last_update_time=timestamp_pb)
    with pytest.raises(GaxError) as exc_info:
        document.set({'bad': 'time-future'}, option=option5)

    assert exc_to_code(exc_info.value.cause) == StatusCode.FAILED_PRECONDITION


def test_update_document(client, cleanup):
    document_id = 'for-update' + unique_resource_id('-')
    document = client.document('made', document_id)
    # Add to clean-up before API request (in case ``create()`` fails).
    cleanup(document)

    # 0. Try to update before the document exists.
    with pytest.raises(NotFound) as exc_info:
        document.update({'not': 'there'})
    assert exc_info.value.message.startswith(MISSING_ENTITY)
    assert document_id in exc_info.value.message

    # 1. Try to update before the document exists (now with an option).
    option1 = client.write_option(create_if_missing=False)
    with pytest.raises(NotFound) as exc_info:
        document.update({'still': 'not-there'}, option=option1)
    assert exc_info.value.message.startswith(MISSING_ENTITY)
    assert document_id in exc_info.value.message

    # 2. Update and create the document (with an option).
    data = {
        'foo': {
            'bar': 'baz',
        },
        'scoop': {
            'barn': 981,
        },
        'other': True,
    }
    option2 = client.write_option(create_if_missing=True)
    write_result2 = document.update(data, option=option2)

    # 3. Send an update without a field path (no option).
    field_updates3 = {'foo': {'quux': 800}}
    write_result3 = document.update(field_updates3)
    assert_timestamp_less(write_result2.update_time, write_result3.update_time)
    snapshot3 = document.get()
    expected3 = {
        'foo': field_updates3['foo'],
        'scoop': data['scoop'],
        'other': data['other'],
    }
    assert snapshot3.to_dict() == expected3

    # 4. Send an update **with** a field path and a delete and a valid
    #    "last timestamp" option.
    field_updates4 = {
        'scoop.silo': None,
        'other': firestore.DELETE_FIELD,
    }
    option4 = client.write_option(last_update_time=snapshot3.update_time)
    write_result4 = document.update(field_updates4, option=option4)
    assert_timestamp_less(write_result3.update_time, write_result4.update_time)
    snapshot4 = document.get()
    expected4 = {
        'foo': field_updates3['foo'],
        'scoop': {
            'barn': data['scoop']['barn'],
            'silo': field_updates4['scoop.silo'],
        },
    }
    assert snapshot4.to_dict() == expected4

    # 5. Call ``update()`` with invalid (in the past) "last timestamp" option.
    assert_timestamp_less(option4._last_update_time, snapshot4.update_time)
    with pytest.raises(GaxError) as exc_info:
        document.update({'bad': 'time-past'}, option=option4)

    assert exc_to_code(exc_info.value.cause) == StatusCode.FAILED_PRECONDITION

    # 6. Call ``update()`` with invalid (in future) "last timestamp" option.
    timestamp_pb = timestamp_pb2.Timestamp(
        seconds=snapshot4.update_time.nanos + 3600,
        nanos=snapshot4.update_time.nanos,
    )
    option6 = client.write_option(last_update_time=timestamp_pb)
    with pytest.raises(GaxError) as exc_info:
        document.set({'bad': 'time-future'}, option=option6)

    assert exc_to_code(exc_info.value.cause) == StatusCode.FAILED_PRECONDITION


def check_snapshot(snapshot, document, data, write_result):
    assert snapshot.reference is document
    assert snapshot.to_dict() == data
    assert snapshot.exists
    assert snapshot.create_time == write_result.update_time
    assert snapshot.update_time == write_result.update_time


def test_document_get(client, cleanup):
    now = datetime.datetime.utcnow().replace(tzinfo=UTC)
    document_id = 'for-get' + unique_resource_id('-')
    document = client.document('created', document_id)
    # Add to clean-up before API request (in case ``create()`` fails).
    cleanup(document)

    # First make sure it doesn't exist.
    with pytest.raises(NotFound) as exc_info:
        document.get()

    assert exc_info.value.message == document._document_path

    ref_doc = client.document('top', 'middle1', 'middle2', 'bottom')
    data = {
        'turtle': 'power',
        'cheese': 19.5,
        'fire': 199099299,
        'referee': ref_doc,
        'gio': firestore.GeoPoint(45.5, 90.0),
        'deep': [
            u'some',
            b'\xde\xad\xbe\xef',
        ],
        'map': {
            'ice': True,
            'water': None,
            'vapor': {
                'deeper': now,
            },
        },
    }
    write_result = document.create(data)
    snapshot = document.get()
    check_snapshot(snapshot, document, data, write_result)
    assert_timestamp_less(snapshot.create_time, snapshot.read_time)


def test_document_delete(client, cleanup):
    document_id = 'deleted' + unique_resource_id('-')
    document = client.document('here-to-be', document_id)
    # Add to clean-up before API request (in case ``create()`` fails).
    cleanup(document)
    document.create({'not': 'much'})

    # 1. Call ``delete()`` with invalid (in the past) "last timestamp" option.
    snapshot1 = document.get()
    timestamp_pb = timestamp_pb2.Timestamp(
        seconds=snapshot1.update_time.nanos - 3600,
        nanos=snapshot1.update_time.nanos,
    )
    option1 = client.write_option(last_update_time=timestamp_pb)
    with pytest.raises(GaxError) as exc_info:
        document.delete(option=option1)

    assert exc_to_code(exc_info.value.cause) == StatusCode.FAILED_PRECONDITION

    # 2. Call ``delete()`` with invalid (in future) "last timestamp" option.
    timestamp_pb = timestamp_pb2.Timestamp(
        seconds=snapshot1.update_time.nanos + 3600,
        nanos=snapshot1.update_time.nanos,
    )
    option2 = client.write_option(last_update_time=timestamp_pb)
    with pytest.raises(GaxError) as exc_info:
        document.delete(option=option2)

    assert exc_to_code(exc_info.value.cause) == StatusCode.FAILED_PRECONDITION

    # 3. Actually ``delete()`` the document.
    delete_time3 = document.delete()

    # 4. ``delete()`` again, even though we know the document is gone.
    delete_time4 = document.delete()
    assert_timestamp_less(delete_time3, delete_time4)


def test_collection_add(client, cleanup):
    collection1 = client.collection('collek')
    collection2 = client.collection('collek', 'shun', 'child')
    explicit_doc_id = 'hula' + unique_resource_id('-')

    # Auto-ID at top-level.
    data1 = {'foo': 'bar'}
    update_time1, document_ref1 = collection1.add(data1)
    cleanup(document_ref1)
    snapshot1 = document_ref1.get()
    assert snapshot1.to_dict() == data1
    assert snapshot1.create_time == update_time1
    assert snapshot1.update_time == update_time1
    assert RANDOM_ID_REGEX.match(document_ref1.id)

    # Explicit ID at top-level.
    data2 = {'baz': 999}
    update_time2, document_ref2 = collection1.add(
        data2, document_id=explicit_doc_id)
    cleanup(document_ref2)
    snapshot2 = document_ref2.get()
    assert snapshot2.to_dict() == data2
    assert snapshot2.create_time == update_time2
    assert snapshot2.update_time == update_time2
    assert document_ref2.id == explicit_doc_id

    # Auto-ID for nested collection.
    data3 = {'quux': b'\x00\x01\x02\x03'}
    update_time3, document_ref3 = collection2.add(data3)
    cleanup(document_ref3)
    snapshot3 = document_ref3.get()
    assert snapshot3.to_dict() == data3
    assert snapshot3.create_time == update_time3
    assert snapshot3.update_time == update_time3
    assert RANDOM_ID_REGEX.match(document_ref3.id)

    # Explicit for nested collection.
    data4 = {'kazaam': None, 'bad': False}
    update_time4, document_ref4 = collection2.add(
        data4, document_id=explicit_doc_id)
    cleanup(document_ref4)
    snapshot4 = document_ref4.get()
    assert snapshot4.to_dict() == data4
    assert snapshot4.create_time == update_time4
    assert snapshot4.update_time == update_time4
    assert document_ref4.id == explicit_doc_id


def test_query_get(client, cleanup):
    sub_collection = 'child' + unique_resource_id('-')
    collection = client.collection('collek', 'shun', sub_collection)

    stored = {}
    num_vals = 5
    allowed_vals = six.moves.xrange(num_vals)
    for a_val in allowed_vals:
        for b_val in allowed_vals:
            document_data = {
                'a': a_val,
                'b': b_val,
                'stats': {
                    'sum': a_val + b_val,
                    'product': a_val * b_val,
                },
            }
            _, doc_ref = collection.add(document_data)
            # Add to clean-up.
            cleanup(doc_ref)
            stored[doc_ref.id] = document_data

    # 0. Limit to snapshots where ``a==1``.
    query0 = collection.where('a', '==', 1)
    values0 = {
        snapshot.id: snapshot.to_dict()
        for snapshot in query0.get()
    }
    assert len(values0) == num_vals
    for key, value in six.iteritems(values0):
        assert stored[key] == value
        assert value['a'] == 1

    # 1. Order by ``b``.
    query1 = collection.order_by('b', direction=query0.DESCENDING)
    values1 = [
        (snapshot.id, snapshot.to_dict())
        for snapshot in query1.get()
    ]
    assert len(values1) == len(stored)
    b_vals1 = []
    for key, value in values1:
        assert stored[key] == value
        b_vals1.append(value['b'])
    # Make sure the ``b``-values are in DESCENDING order.
    assert sorted(b_vals1, reverse=True) == b_vals1

    # 2. Limit to snapshots where ``stats.sum > 1`` (a field path).
    query2 = collection.where('stats.sum', '>', 4)
    values2 = {
        snapshot.id: snapshot.to_dict()
        for snapshot in query2.get()
    }
    assert len(values2) == 10
    ab_pairs2 = set()
    for key, value in six.iteritems(values2):
        assert stored[key] == value
        ab_pairs2.add((value['a'], value['b']))

    expected_ab_pairs = set([
        (a_val, b_val)
        for a_val in allowed_vals
        for b_val in allowed_vals
        if a_val + b_val > 4
    ])
    assert expected_ab_pairs == ab_pairs2

    # 3. Use a start and end cursor.
    query3 = collection.start_at({'a': num_vals - 2})
    query3 = query3.order_by('a')
    query3 = query3.end_before({'a': num_vals - 1})
    values3 = [
        (snapshot.id, snapshot.to_dict())
        for snapshot in query3.get()
    ]
    assert len(values3) == num_vals
    for key, value in values3:
        assert stored[key] == value
        assert value['a'] == num_vals - 2
        b_vals1.append(value['b'])

    # 4. Send a query with no results.
    query4 = collection.where('b', '==', num_vals + 100)
    values4 = list(query4.get())
    assert len(values4) == 0

    # 5. Select a subset of fields.
    query5 = collection.where('b', '<=', 1)
    query5 = query5.select(['a', 'stats.product'])
    values5 = {
        snapshot.id: snapshot.to_dict()
        for snapshot in query5.get()
    }
    assert len(values5) == num_vals * 2  # a ANY, b in (0, 1)
    for key, value in six.iteritems(values5):
        expected = {
            'a': stored[key]['a'],
            'stats': {
                'product': stored[key]['stats']['product'],
            },
        }
        assert expected == value

    # 6. Add multiple filters via ``where()``.
    query6 = collection.where('stats.product', '>', 5)
    query6 = query6.where('stats.product', '<', 10)
    values6 = {
        snapshot.id: snapshot.to_dict()
        for snapshot in query6.get()
    }

    matching_pairs = [
        (a_val, b_val)
        for a_val in allowed_vals
        for b_val in allowed_vals
        if 5 < a_val * b_val < 10
    ]
    assert len(values6) == len(matching_pairs)
    for key, value in six.iteritems(values6):
        assert stored[key] == value
        pair = (value['a'], value['b'])
        assert pair in matching_pairs

    # 7. Skip the first three results, when ``b==2``
    query7 = collection.where('b', '==', 2)
    offset = 3
    query7 = query7.offset(offset)
    values7 = {
        snapshot.id: snapshot.to_dict()
        for snapshot in query7.get()
    }
    # NOTE: We don't check the ``a``-values, since that would require
    #       an ``order_by('a')``, which combined with the ``b == 2``
    #       filter would necessitate an index.
    assert len(values7) == num_vals - offset
    for key, value in six.iteritems(values7):
        assert stored[key] == value
        assert value['b'] == 2


def test_query_unary(client, cleanup):
    collection_name = 'unary' + unique_resource_id('-')
    collection = client.collection(collection_name)
    field_name = 'foo'

    _, document0 = collection.add({field_name: None})
    # Add to clean-up.
    cleanup(document0)

    nan_val = float('nan')
    _, document1 = collection.add({field_name: nan_val})
    # Add to clean-up.
    cleanup(document1)

    # 0. Query for null.
    query0 = collection.where(field_name, '==', None)
    values0 = list(query0.get())
    assert len(values0) == 1
    snapshot0 = values0[0]
    assert snapshot0.reference._path == document0._path
    assert snapshot0.to_dict() == {field_name: None}

    # 1. Query for a NAN.
    query1 = collection.where(field_name, '==', nan_val)
    values1 = list(query1.get())
    assert len(values1) == 1
    snapshot1 = values1[0]
    assert snapshot1.reference._path == document1._path
    data1 = snapshot1.to_dict()
    assert len(data1) == 1
    assert math.isnan(data1[field_name])


def test_get_all(client, cleanup):
    collection_name = 'get-all' + unique_resource_id('-')

    document1 = client.document(collection_name, 'a')
    document2 = client.document(collection_name, 'b')
    document3 = client.document(collection_name, 'c')
    # Add to clean-up before API requests (in case ``create()`` fails).
    cleanup(document1)
    cleanup(document3)

    data1 = {
        'a': {
            'b': 2,
            'c': 3,
        },
        'd': 4,
        'e': 0,
    }
    write_result1 = document1.create(data1)
    data3 = {
        'a': {
            'b': 5,
            'c': 6,
        },
        'd': 7,
        'e': 100,
    }
    write_result3 = document3.create(data3)

    # 0. Get 3 unique documents, one of which is missing.
    snapshots = list(client.get_all(
        [document1, document2, document3]))

    assert snapshots.count(None) == 1
    snapshots.remove(None)
    id_attr = operator.attrgetter('id')
    snapshots.sort(key=id_attr)

    snapshot1, snapshot3 = snapshots
    check_snapshot(snapshot1, document1, data1, write_result1)
    check_snapshot(snapshot3, document3, data3, write_result3)

    # 1. Get 2 colliding documents.
    document1_also = client.document(collection_name, 'a')
    snapshots = list(client.get_all([document1, document1_also]))

    assert len(snapshots) == 1
    assert document1 is not document1_also
    check_snapshot(snapshots[0], document1_also, data1, write_result1)

    # 2. Use ``field_paths`` / projection in ``get_all()``.
    snapshots = list(client.get_all(
        [document1, document3], field_paths=['a.b', 'd']))

    assert len(snapshots) == 2
    snapshots.sort(key=id_attr)

    snapshot1, snapshot3 = snapshots
    restricted1 = {
        'a': {'b': data1['a']['b']},
        'd': data1['d'],
    }
    check_snapshot(snapshot1, document1, restricted1, write_result1)
    restricted3 = {
        'a': {'b': data3['a']['b']},
        'd': data3['d'],
    }
    check_snapshot(snapshot3, document3, restricted3, write_result3)


def test_batch(client, cleanup):
    collection_name = 'batch' + unique_resource_id('-')

    document1 = client.document(collection_name, 'abc')
    document2 = client.document(collection_name, 'mno')
    document3 = client.document(collection_name, 'xyz')
    # Add to clean-up before API request (in case ``create()`` fails).
    cleanup(document1)
    cleanup(document2)
    cleanup(document3)

    data2 = {
        'some': {
            'deep': 'stuff',
            'and': 'here',
        },
        'water': 100.0,
    }
    document2.create(data2)
    document3.create({'other': 19})

    batch = client.batch()
    data1 = {'all': True}
    batch.create(document1, data1)
    new_value = 'there'
    batch.update(document2, {'some.and': new_value})
    batch.delete(document3)
    write_results = batch.commit()

    assert len(write_results) == 3

    write_result1 = write_results[0]
    write_result2 = write_results[1]
    write_result3 = write_results[2]
    assert not write_result3.HasField('update_time')

    snapshot1 = document1.get()
    assert snapshot1.to_dict() == data1
    assert snapshot1.create_time == write_result1.update_time
    assert snapshot1.update_time == write_result1.update_time

    snapshot2 = document2.get()
    assert snapshot2.to_dict() != data2
    data2['some']['and'] = new_value
    assert snapshot2.to_dict() == data2
    assert_timestamp_less(snapshot2.create_time, write_result2.update_time)
    assert snapshot2.update_time == write_result2.update_time

    with pytest.raises(NotFound):
        document3.get()
