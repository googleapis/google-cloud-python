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

from google.cloud.ndb import context
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(context)


class TestAutoBatcher:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            context.AutoBatcher()


class TestContext:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            context.Context()


class TestContextOptions:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            context.ContextOptions()


def test_EVENTUAL_CONSISTENCY():
    assert context.EVENTUAL_CONSISTENCY == 1


class TestTransactionOptions:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            context.TransactionOptions()
