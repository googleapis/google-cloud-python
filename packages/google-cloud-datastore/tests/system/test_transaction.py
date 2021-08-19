# Copyright 2011 Google LLC
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

from google.cloud import datastore
from google.cloud.exceptions import Conflict

from . import _helpers


def test_transaction_via_with_statement(datastore_client, entities_to_delete):
    key = datastore_client.key("Company", "Google")
    entity = datastore.Entity(key=key)
    entity["url"] = u"www.google.com"

    with datastore_client.transaction() as xact:
        result = datastore_client.get(entity.key)
        if result is None:
            xact.put(entity)
            entities_to_delete.append(entity)

    # This will always return after the transaction.
    retrieved_entity = datastore_client.get(key)

    entities_to_delete.append(retrieved_entity)
    assert retrieved_entity == entity


def test_transaction_via_explicit_begin_get_commit(
    datastore_client, entities_to_delete,
):
    # See
    # github.com/GoogleCloudPlatform/google-cloud-python/issues/1859
    # Note that this example lacks the threading which provokes the race
    # condition in that issue:  we are basically just exercising the
    # "explict" path for using transactions.
    before_1 = 100
    before_2 = 0
    transfer_amount = 40

    key1 = datastore_client.key("account", "123")
    account1 = datastore.Entity(key=key1)
    account1["balance"] = before_1

    key2 = datastore_client.key("account", "234")
    account2 = datastore.Entity(key=key2)
    account2["balance"] = before_2

    datastore_client.put_multi([account1, account2])
    entities_to_delete.append(account1)
    entities_to_delete.append(account2)

    xact = datastore_client.transaction()
    xact.begin()
    from_account = datastore_client.get(key1, transaction=xact)
    to_account = datastore_client.get(key2, transaction=xact)
    from_account["balance"] -= transfer_amount
    to_account["balance"] += transfer_amount

    xact.put(from_account)
    xact.put(to_account)
    xact.commit()

    after1 = datastore_client.get(key1)
    after2 = datastore_client.get(key2)
    assert after1["balance"] == before_1 - transfer_amount
    assert after2["balance"] == before_2 + transfer_amount


def test_failure_with_contention(datastore_client, entities_to_delete):
    contention_prop_name = "baz"
    local_client = _helpers.clone_client(datastore_client)

    # Insert an entity which will be retrieved in a transaction
    # and updated outside it with a contentious value.
    key = local_client.key("BreakTxn", 1234)
    orig_entity = datastore.Entity(key=key)
    orig_entity["foo"] = u"bar"
    local_client.put(orig_entity)

    entities_to_delete.append(orig_entity)

    with pytest.raises(Conflict):
        with local_client.transaction() as txn:
            entity_in_txn = local_client.get(key)

            # Update the original entity outside the transaction.
            orig_entity[contention_prop_name] = u"outside"
            datastore_client.put(orig_entity)

            # Try to update the entity which we already updated outside the
            # transaction.
            entity_in_txn[contention_prop_name] = u"inside"
            txn.put(entity_in_txn)
