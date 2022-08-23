# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
#
"""This module has all of the helper functions needed to merge shards."""
import re
from typing import List

from google.cloud import documentai_v1
from google.cloud import storage


def _read_output(gcs_prefix: str) -> List[documentai_v1.Document]:
    """Returns a list of Document shards."""

    shards = []

    output_bucket, output_prefix = re.match(r"gs://(.*?)/(.*)", gcs_prefix).groups()

    file_check = re.match(r"(.*[.].*$)", output_prefix)

    if file_check is not None:
        raise TypeError("gcs_prefix cannot contain file types")

    storage_client = storage.Client()

    blob_list = storage_client.list_blobs(output_bucket, prefix=output_prefix)

    for blob in blob_list:
        if blob.name.endswith(".json"):
            blob_as_bytes = blob.download_as_bytes()
            shards.append(documentai_v1.types.Document.from_json(blob_as_bytes))

    return shards
