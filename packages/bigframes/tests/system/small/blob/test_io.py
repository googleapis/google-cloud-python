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

import bigframes
import bigframes.pandas as bpd


def test_blob_create_from_uri_str():
    bigframes.options.experiments.blob = True

    uri_series = bpd.Series(
        [
            "gs://bigframes_blob_test/images/img0.jpg",
            "gs://bigframes_blob_test/images/img1.jpg",
        ]
    )
    # TODO: use bq_connection fixture when MMD location capitalization fix is in prod
    blob_series = uri_series.str.to_blob(connection="us.bigframes-default-connection")

    pd_blob_series = blob_series.to_pandas()

    assert len(pd_blob_series) == 2
