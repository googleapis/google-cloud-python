# Copyright 2026 Google LLC
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
"""Root pytest configuration for the package.

The only job here is to keep ``pytest.ini`` portable across the range of
``pytest-asyncio`` versions this package is tested with. ``pytest.ini`` sets
``asyncio_default_fixture_loop_scope``/``asyncio_default_test_loop_scope`` so the
session-scoped async fixtures in the system suites share one event loop on
modern ``pytest-asyncio`` (>=0.23). Older ``pytest-asyncio`` (e.g. the 0.21.2 the
nox ``system`` session pins) does not register those ini options, so it would
emit a ``PytestConfigWarning: Unknown config option`` -- harmless on its own, but
fatal in any environment that runs pytest with ``-W error``.

Registering the options defensively here makes them "known" on older
``pytest-asyncio`` (silencing that warning) while staying a no-op on newer
versions, which already register them (the duplicate ``addini`` raises
``ValueError``, which we swallow). Both the value and pytest-asyncio's own
handling are otherwise untouched.
"""


def pytest_addoption(parser):
    for name, help_text in (
        (
            "asyncio_default_fixture_loop_scope",
            "default event-loop scope for asyncio fixtures (pytest-asyncio)",
        ),
        (
            "asyncio_default_test_loop_scope",
            "default event-loop scope for asyncio tests (pytest-asyncio)",
        ),
    ):
        try:
            parser.addini(name, help_text, default=None)
        except ValueError:
            # Already registered by a pytest-asyncio new enough to own it.
            pass
