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
from google.cloud import datastore
from google.cloud import ndb


def test_retrieve_entity():
    ds_client = datastore.Client()
    ds_key = ds_client.key("SomeKind", 1234)
    ds_entity = datastore.Entity(key=ds_key)
    ds_entity.update({"foo": 42, "bar": "none"})
    ds_client.put(ds_entity)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    client = ndb.Client()

    with client.context():
        key = ndb.Key("SomeKind", 1234)
        entity = key.get()
        assert isinstance(entity, SomeKind)
        assert entity.foo == 42
        assert entity.bar == "none"
