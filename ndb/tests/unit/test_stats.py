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

from google.cloud.ndb import stats
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(stats)


class TestBaseKindStatistic:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.BaseKindStatistic()


class TestBaseStatistic:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.BaseStatistic()


class TestGlobalStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.GlobalStat()


class TestKindCompositeIndexStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.KindCompositeIndexStat()


class TestKindNonRootEntityStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.KindNonRootEntityStat()


class TestKindPropertyNamePropertyTypeStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.KindPropertyNamePropertyTypeStat()


class TestKindPropertyNameStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.KindPropertyNameStat()


class TestKindPropertyTypeStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.KindPropertyTypeStat()


class TestKindRootEntityStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.KindRootEntityStat()


class TestKindStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.KindStat()


class TestNamespaceGlobalStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.NamespaceGlobalStat()


class TestNamespaceKindCompositeIndexStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.NamespaceKindCompositeIndexStat()


class TestNamespaceKindNonRootEntityStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.NamespaceKindNonRootEntityStat()


class TestNamespaceKindPropertyNamePropertyTypeStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.NamespaceKindPropertyNamePropertyTypeStat()


class TestNamespaceKindPropertyNameStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.NamespaceKindPropertyNameStat()


class TestNamespaceKindPropertyTypeStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.NamespaceKindPropertyTypeStat()


class TestNamespaceKindRootEntityStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.NamespaceKindRootEntityStat()


class TestNamespaceKindStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.NamespaceKindStat()


class TestNamespacePropertyTypeStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.NamespacePropertyTypeStat()


class TestNamespaceStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.NamespaceStat()


class TestPropertyTypeStat:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            stats.PropertyTypeStat()
