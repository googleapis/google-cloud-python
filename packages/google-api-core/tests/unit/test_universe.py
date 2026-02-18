# Copyright 2024 Google LLC
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
from google.api_core import universe


class _Fake_Credentials:
    def __init__(self, universe_domain=None):
        if universe_domain:
            self.universe_domain = universe_domain


def test_determine_domain():
    domain_client = "foo.com"
    domain_env = "bar.com"

    assert universe.determine_domain(domain_client, domain_env) == domain_client
    assert universe.determine_domain(None, domain_env) == domain_env
    assert universe.determine_domain(domain_client, None) == domain_client
    assert universe.determine_domain(None, None) == universe.DEFAULT_UNIVERSE

    with pytest.raises(universe.EmptyUniverseError):
        universe.determine_domain("", None)

    with pytest.raises(universe.EmptyUniverseError):
        universe.determine_domain(None, "")


def test_compare_domains():
    fake_domain = "foo.com"
    another_fake_domain = "bar.com"

    assert universe.compare_domains(universe.DEFAULT_UNIVERSE, _Fake_Credentials())
    assert universe.compare_domains(fake_domain, _Fake_Credentials(fake_domain))

    with pytest.raises(universe.UniverseMismatchError) as excinfo:
        universe.compare_domains(
            universe.DEFAULT_UNIVERSE, _Fake_Credentials(fake_domain)
        )
    assert str(excinfo.value).find(universe.DEFAULT_UNIVERSE) >= 0
    assert str(excinfo.value).find(fake_domain) >= 0

    with pytest.raises(universe.UniverseMismatchError) as excinfo:
        universe.compare_domains(fake_domain, _Fake_Credentials())
    assert str(excinfo.value).find(fake_domain) >= 0
    assert str(excinfo.value).find(universe.DEFAULT_UNIVERSE) >= 0

    with pytest.raises(universe.UniverseMismatchError) as excinfo:
        universe.compare_domains(fake_domain, _Fake_Credentials(another_fake_domain))
    assert str(excinfo.value).find(fake_domain) >= 0
    assert str(excinfo.value).find(another_fake_domain) >= 0
