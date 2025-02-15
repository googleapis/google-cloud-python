# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script create the bigtable resources required for
# bigframes.streaming testing if they don't already exist

import os
from pathlib import Path
import sys

import google.cloud.exceptions as exceptions
from google.cloud.storage import transfer_manager
import google.cloud.storage as gcs

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

if not PROJECT_ID:
    print(
        "Please set GOOGLE_CLOUD_PROJECT environment variable before running.",
        file=sys.stderr,
    )
    sys.exit(1)


def create_bucket(client: gcs.Client) -> gcs.Bucket:
    bucket_name = "bigframes_blob_test"

    print(f"Creating bucket: {bucket_name}")
    try:
        bucket = client.create_bucket(bucket_name)
        print(f"Bucket {bucket_name} created. ")

    except exceptions.Conflict:
        print(f"Bucket {bucket_name} already exists.")
        bucket = client.bucket(bucket_name)

    return bucket


def upload_data(bucket: gcs.Bucket):
    # from https://cloud.google.com/storage/docs/samples/storage-transfer-manager-upload-directory
    source_directory = "scripts/data/"
    workers = 8

    # First, recursively get all files in `directory` as Path objects.
    directory_as_path_obj = Path(source_directory)
    paths = directory_as_path_obj.rglob("*")

    # Filter so the list only includes files, not directories themselves.
    file_paths = [path for path in paths if path.is_file()]

    # These paths are relative to the current working directory. Next, make them
    # relative to `directory`
    relative_paths = [path.relative_to(source_directory) for path in file_paths]

    # Finally, convert them all to strings.
    string_paths = [str(path) for path in relative_paths]

    print("Found {} files.".format(len(string_paths)))

    # Start the upload.
    results = transfer_manager.upload_many_from_filenames(
        bucket, string_paths, source_directory=source_directory, max_workers=workers
    )

    for name, result in zip(string_paths, results):
        # The results list is either `None` or an exception for each filename in
        # the input list, in order.

        if isinstance(result, Exception):
            print("Failed to upload {} due to exception: {}".format(name, result))
        else:
            print("Uploaded {} to {}.".format(name, bucket.name))


def main():
    client = gcs.Client(project=PROJECT_ID)

    bucket = create_bucket(client)

    upload_data(bucket)


if __name__ == "__main__":
    main()
