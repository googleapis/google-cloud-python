# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import test_utils.system

from google.cloud import datastore
from google.cloud import ndb


@pytest.fixture
def ds_entity():
    keys = []
    client = datastore.Client()

    def make_entity(*key_args, **entity_kwargs):
        key = client.key(*key_args)
        assert client.get(key) is None
        entity = datastore.Entity(key=key)
        entity.update(entity_kwargs)
        client.put(entity)

        keys.append(key)
        return entity

    yield make_entity

    for key in keys:
        client.delete(key)


@pytest.fixture
def client_context():
    client = ndb.Client()
    with client.context():
        yield


@pytest.mark.usefixtures("client_context")
def test_retrieve_entity(ds_entity):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity("SomeKind", entity_id, foo=42, bar="none")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    key = ndb.Key("SomeKind", entity_id)
    entity = key.get()
    assert isinstance(entity, SomeKind)
    assert entity.foo == 42
    assert entity.bar == "none"
