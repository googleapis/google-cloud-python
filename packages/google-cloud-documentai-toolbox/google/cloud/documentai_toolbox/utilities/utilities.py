# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
"""Document AI utilities."""
import os
import re
from typing import Dict, List, Optional

from google.cloud import documentai

from google.cloud.documentai_toolbox import constants
from google.cloud.documentai_toolbox.wrappers.document import _get_storage_client


def list_gcs_document_tree(
    gcs_bucket_name: str, gcs_prefix: str
) -> Dict[str, List[str]]:
    r"""Returns a list path to files in Cloud Storage folder and prints the tree to terminal.

    Args:
        gcs_bucket_name (str):
            Required. The name of the gcs bucket.

            Format: `gs://{bucket_name}/{optional_folder}/{target_folder}/` where gcs_bucket_name=`bucket`.
        gcs_prefix (str):
            Required. The prefix of the json files in the target_folder.

            Format: `gs://{bucket_name}/{optional_folder}/{target_folder}/` where gcs_prefix=`{optional_folder}/{target_folder}`.
    Returns:
        Dict[str, List[str]]:
            The paths to documents in `gs://{gcs_bucket_name}/{gcs_prefix}`.

    """
    file_check = re.match(constants.FILE_CHECK_REGEX, gcs_prefix)

    if file_check is not None:
        raise ValueError("gcs_prefix cannot contain file types")

    storage_client = _get_storage_client()
    blob_list = storage_client.list_blobs(gcs_bucket_name, prefix=gcs_prefix)

    path_list: Dict[str, List[str]] = {}

    for blob in blob_list:
        directory, file_name = os.path.split(blob.name)

        if directory in path_list:
            path_list[directory].append(file_name)
        else:
            path_list[directory] = [file_name]

    return path_list


def print_gcs_document_tree(gcs_bucket_name: str, gcs_prefix: str) -> None:
    r"""Prints a tree of filenames in Cloud Storage folder..

    Args:
        gcs_bucket_name (str):
            Required. The name of the gcs bucket.

            Format: `gs://{bucket_name}/{optional_folder}/{target_folder}/` where gcs_bucket_name=`bucket`.
        gcs_prefix (str):
            Required. The prefix of the json files in the target_folder.

            Format: `gs://{bucket_name}/{optional_folder}/{target_folder}/` where gcs_prefix=`{optional_folder}/{target_folder}`.
    Returns:
        None.

    """
    FILENAME_TREE_MIDDLE = "├──"
    FILENAME_TREE_LAST = "└──"
    FILES_TO_DISPLAY = 4

    path_list = list_gcs_document_tree(
        gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_prefix
    )

    for directory, files in path_list.items():
        print(f"{directory}")
        dir_size = len(files)
        for idx, file_name in enumerate(files):
            if idx == dir_size - 1:
                if dir_size > FILES_TO_DISPLAY:
                    print("│  ....")
                print(f"{FILENAME_TREE_LAST}{file_name}\n")
                break
            if idx <= FILES_TO_DISPLAY:
                print(f"{FILENAME_TREE_MIDDLE}{file_name}")


def create_batches(
    gcs_bucket_name: str,
    gcs_prefix: str,
    batch_size: Optional[int] = constants.BATCH_MAX_FILES,
) -> List[documentai.BatchDocumentsInputConfig]:
    """Create batches of documents in Cloud Storage to process with `batch_process_documents()`.

    Args:
        gcs_bucket_name (str):
            Required. The name of the gcs bucket.

            Format: `gs://bucket/optional_folder/target_folder/` where gcs_bucket_name=`bucket`.
        gcs_prefix (str):
            Required. The prefix of the json files in the `target_folder`

            Format: `gs://bucket/optional_folder/target_folder/` where gcs_prefix=`optional_folder/target_folder`.
        batch_size (Optional[int]):
            Optional. Size of each batch of documents. Default is `50`.

    Returns:
        List[documentai.BatchDocumentsInputConfig]:
            A list of `BatchDocumentsInputConfig`, each corresponding to one batch.
    """
    if batch_size > constants.BATCH_MAX_FILES:
        raise ValueError(
            f"Batch size must be less than {constants.BATCH_MAX_FILES}. You provided {batch_size}."
        )

    storage_client = _get_storage_client()
    blob_list = storage_client.list_blobs(gcs_bucket_name, prefix=gcs_prefix)
    batches: List[documentai.BatchDocumentsInputConfig] = []
    batch: List[documentai.GcsDocument] = []

    for blob in blob_list:
        # Skip Directories
        if blob.name.endswith("/"):
            continue

        if blob.content_type not in constants.VALID_MIME_TYPES:
            print(f"Skipping file {blob.name}. Invalid Mime Type {blob.content_type}.")
            continue

        if blob.size > constants.BATCH_MAX_FILE_SIZE:
            print(
                f"Skipping file {blob.name}. File size must be less than {constants.BATCH_MAX_FILE_SIZE} bytes. File size is {blob.size} bytes."
            )
            continue

        if len(batch) == batch_size:
            batches.append(
                documentai.BatchDocumentsInputConfig(
                    gcs_documents=documentai.GcsDocuments(documents=batch)
                )
            )
            batch = []

        batch.append(
            documentai.GcsDocument(
                gcs_uri=f"gs://{gcs_bucket_name}/{blob.name}",
                mime_type=blob.content_type,
            )
        )

    if batch:
        # Append the last batch, which could be less than `batch_size`
        batches.append(
            documentai.BatchDocumentsInputConfig(
                gcs_documents=documentai.GcsDocuments(documents=batch)
            )
        )

    return batches
