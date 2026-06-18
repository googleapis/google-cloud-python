# Copyright 2025 Google LLC
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

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import pyarrow as pa
import pytest

import bigframes._config

# Make sure SettingWithCopyWarning is ignored if it exists.
# It was removed in pandas 3.0.
if hasattr(pd.errors, "SettingWithCopyWarning"):
    warnings.simplefilter("ignore", pd.errors.SettingWithCopyWarning)


@pytest.fixture(scope="session")
def polars_session_or_bpd():
    # Since the doctest imports fixture is autouse=True, don't skip if polars
    # isn't available.
    try:
        from bigframes.testing import polars_session

        return polars_session.TestSession()
    except ImportError:
        import bigframes.pandas as bpd

        return bpd


@pytest.fixture(autouse=True)
def default_doctest_imports(doctest_namespace, polars_session_or_bpd):
    """
    Avoid some boilerplate in pandas-inspired tests.

    See: https://docs.pytest.org/en/stable/how-to/doctest.html#doctest-namespace-fixture
    """
    doctest_namespace["np"] = np
    doctest_namespace["pd"] = pd
    doctest_namespace["pa"] = pa
    doctest_namespace["bpd"] = polars_session_or_bpd
    bigframes._config.options.display.progress_bar = None

    # TODO(tswast): Consider setting the numpy printoptions here for better
    # compatibility across numpy versions.
    # https://numpy.org/doc/stable/release/2.0.0-notes.html#representation-of-numpy-scalars-changed
    # https://numpy.org/doc/stable/reference/generated/numpy.set_printoptions.html#numpy-set-printoptions
