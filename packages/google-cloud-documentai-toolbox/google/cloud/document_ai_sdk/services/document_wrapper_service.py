"""This module has all of the helper functions needed to merge shards."""
import re
from typing import List

from google.cloud import documentai_v1
from google.cloud import storage


def _read_output(gcs_prefix: str) -> List[documentai_v1.Document]:
  """Returns a list of Document shards."""

  shards = []

  output_bucket, output_prefix = re.match(r"gs://(.*?)/(.*)",
                                          gcs_prefix).groups()

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
