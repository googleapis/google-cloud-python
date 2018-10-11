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

from google.cloud.ndb import key
from google.cloud.ndb import model
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(model)


def test_Key():
    assert model.Key is key.Key


def test_BlobKey():
    assert model.BlobKey is NotImplemented


def test_GeoPt():
    assert model.GeoPt is NotImplemented


class TestBlobKeyProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.BlobKeyProperty()


class TestBlobProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.BlobProperty()


class TestBooleanProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.BooleanProperty()


class TestComputedProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.ComputedProperty()


class TestDateProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.DateProperty()


class TestDateTimeProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.DateTimeProperty()


def test_delete_multi():
    with pytest.raises(NotImplementedError):
        model.delete_multi()


def test_delete_multi_async():
    with pytest.raises(NotImplementedError):
        model.delete_multi_async()


class TestExpando:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.Expando()


class TestFloatProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.FloatProperty()


class TestGenericProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.GenericProperty()


class TestGeoPtProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.GeoPtProperty()


def test_get_indexes():
    with pytest.raises(NotImplementedError):
        model.get_indexes()


def test_get_indexes_async():
    with pytest.raises(NotImplementedError):
        model.get_indexes_async()


def test_get_multi():
    with pytest.raises(NotImplementedError):
        model.get_multi()


def test_get_multi_async():
    with pytest.raises(NotImplementedError):
        model.get_multi_async()


def test_in_transaction():
    with pytest.raises(NotImplementedError):
        model.in_transaction()


class TestIndex:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.Index()


class TestIndexProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.IndexProperty()


class TestIndexState:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.IndexState()


class TestIntegerProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.IntegerProperty()


class TestJsonProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.JsonProperty()


class TestKeyProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.KeyProperty()


class TestLocalStructuredProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.LocalStructuredProperty()


def test_make_connection():
    with pytest.raises(NotImplementedError):
        model.make_connection()


class TestMetaModel:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.MetaModel()


class TestModel:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.Model()

    @staticmethod
    def test__get_kind():
        assert model.Model._get_kind() == "Model"

        class Simple(model.Model):
            pass

        assert Simple._get_kind() == "Simple"


class TestModelAdapter:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.ModelAdapter()


class TestModelAttribute:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.ModelAttribute()


class TestModelKey:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.ModelKey()


def test_non_transactional():
    with pytest.raises(NotImplementedError):
        model.non_transactional()


class TestPickleProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.PickleProperty()


class TestProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.Property()


def test_put_multi():
    with pytest.raises(NotImplementedError):
        model.put_multi()


def test_put_multi_async():
    with pytest.raises(NotImplementedError):
        model.put_multi_async()


class TestStringProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.StringProperty()


class TestStructuredProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.StructuredProperty()


class TestTextProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.TextProperty()


class TestTimeProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.TimeProperty()


def test_transaction():
    with pytest.raises(NotImplementedError):
        model.transaction()


def test_transaction_async():
    with pytest.raises(NotImplementedError):
        model.transaction_async()


def test_transactional():
    with pytest.raises(NotImplementedError):
        model.transactional()


def test_transactional_async():
    with pytest.raises(NotImplementedError):
        model.transactional_async()


def test_transactional_tasklet():
    with pytest.raises(NotImplementedError):
        model.transactional_tasklet()


class TestUserProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.UserProperty()
