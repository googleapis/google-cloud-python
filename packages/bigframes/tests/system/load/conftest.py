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


from typing import Generator

import pytest

import bigframes


# Override the session to target at bigframes-load-testing at all load tests. That allows to run load tests locally with authentic env.
@pytest.fixture(scope="session")
def session() -> Generator[bigframes.Session, None, None]:
    context = bigframes.BigQueryOptions(location="US", project="bigframes-load-testing")
    session = bigframes.Session(context=context)
    yield session
    session.close()  # close generated session at cleanup time


@pytest.fixture(scope="session")
def session_us_east5() -> Generator[bigframes.Session, None, None]:
    context = bigframes.BigQueryOptions(
        location="us-east5", project="bigframes-load-testing"
    )
    session = bigframes.Session(context=context)
    yield session
    session.close()  # close generated session at cleanup time
