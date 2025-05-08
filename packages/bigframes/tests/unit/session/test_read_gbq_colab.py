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
