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

"""
Difficult to classify regression tests.
"""
import pickle

import pytest

from google.cloud import ndb


# Pickle can only pickle/unpickle global classes
class PickleOtherKind(ndb.Model):
    foo = ndb.IntegerProperty()

    @classmethod
    def _get_kind(cls):
        return "OtherKind"


class PickleSomeKind(ndb.Model):
    other = ndb.StructuredProperty(PickleOtherKind)

    @classmethod
    def _get_kind(cls):
        return "SomeKind"


@pytest.mark.usefixtures("client_context")
def test_pickle_roundtrip_structured_property(dispose_of):
    """Regression test for Issue #281.

    https://github.com/googleapis/python-ndb/issues/281
    """
    ndb.Model._kind_map["SomeKind"] = PickleSomeKind
    ndb.Model._kind_map["OtherKind"] = PickleOtherKind

    entity = PickleSomeKind(other=PickleOtherKind(foo=1))
    key = entity.put()
    dispose_of(key._key)

    entity = key.get(use_cache=False)
    assert entity.other.key is None or entity.other.key.id() is None
    entity = pickle.loads(pickle.dumps(entity))
    assert entity.other.foo == 1


@pytest.mark.usefixtures("client_context")
def test_tasklet_yield_emtpy_list():
    """
    Regression test for Issue #353.

    https://github.com/googleapis/python-ndb/issues/353
    """

    @ndb.tasklet
    def test_it():
        nothing = yield []
        raise ndb.Return(nothing)

    assert test_it().result() == ()
