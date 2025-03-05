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

import pytest

import bigframes
import bigframes.pandas as bpd


@pytest.fixture(scope="session")
def images_gcs_path() -> str:
    return "gs://bigframes_blob_test/images/*"


@pytest.fixture(scope="session")
def images_uris() -> list[str]:
    return [
        "gs://bigframes_blob_test/images/img0.jpg",
        "gs://bigframes_blob_test/images/img1.jpg",
    ]


@pytest.fixture(scope="session")
def images_mm_df(
    images_gcs_path, session: bigframes.Session, bq_connection: str
) -> bpd.DataFrame:
    bigframes.options.experiments.blob = True

    return session.from_glob_path(
        images_gcs_path, name="blob_col", connection=bq_connection
    )
