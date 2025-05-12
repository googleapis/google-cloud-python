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

"""Unit tests for read_gbq_colab helper functions."""

from bigframes.testing import mocks


def test_read_gbq_colab_includes_label():
    """Make sure we can tell direct colab usage apart from regular read_gbq usage."""
    session = mocks.create_bigquery_session()
    _ = session._read_gbq_colab("SELECT 'read-gbq-colab-test'")
    configs = session._job_configs  # type: ignore

    label_values = []
    for config in configs:
        if config is None:
            continue
        label_values.extend(config.labels.values())

    assert "read_gbq_colab" in label_values


def test_read_gbq_colab_includes_formatted_values_in_dry_run():
    session = mocks.create_bigquery_session()

    pyformat_args = {
        "some_integer": 123,
        "some_string": "This could be dangerous, but we escape it",
        # This is not a supported type, but ignored if not referenced.
        "some_object": object(),
    }
    _ = session._read_gbq_colab(
        """
        SELECT {some_integer} as some_integer,
        {some_string} as some_string,
        '{{escaped}}' as escaped
        """,
        pyformat_args=pyformat_args,
        dry_run=True,
    )
    expected = """
        SELECT 123 as some_integer,
        'This could be dangerous, but we escape it' as some_string,
        '{escaped}' as escaped
        """
    queries = session._queries  # type: ignore
    configs = session._job_configs  # type: ignore

    for query, config in zip(queries, configs):
        if config is None:
            continue
        if config.dry_run:
            break

    assert config.dry_run
    assert query.strip() == expected.strip()
