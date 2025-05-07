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

import pandas as pd

import bigframes.dtypes as dtypes
import bigframes.pandas as bpd


def test_blob_uri(images_uris: list[str], images_mm_df: bpd.DataFrame):
    actual = images_mm_df["blob_col"].blob.uri().to_pandas()
    expected = pd.Series(images_uris, name="uri")

    pd.testing.assert_series_equal(
        actual, expected, check_dtype=False, check_index_type=False
    )


def test_blob_authorizer(images_mm_df: bpd.DataFrame, bq_connection: str):
    actual = images_mm_df["blob_col"].blob.authorizer().to_pandas()
    expected = pd.Series(
        [bq_connection.casefold(), bq_connection.casefold()], name="authorizer"
    )

    pd.testing.assert_series_equal(
        actual, expected, check_dtype=False, check_index_type=False
    )


def test_blob_version(images_mm_df: bpd.DataFrame):
    actual = images_mm_df["blob_col"].blob.version().to_pandas()
    expected = pd.Series(["1739574332294150", "1739574332271343"], name="version")

    pd.testing.assert_series_equal(
        actual, expected, check_dtype=False, check_index_type=False
    )


def test_blob_metadata(images_mm_df: bpd.DataFrame):
    actual = images_mm_df["blob_col"].blob.metadata().to_pandas()
    expected = pd.Series(
        [
            (
                '{"content_type":"image/jpeg",'
                '"md5_hash":"e130ad042261a1883cd2cc06831cf748",'
                '"size":338390,'
                '"updated":1739574332000000}'
            ),
            (
                '{"content_type":"image/jpeg",'
                '"md5_hash":"e2ae3191ff2b809fd0935f01a537c650",'
                '"size":43333,'
                '"updated":1739574332000000}'
            ),
        ],
        name="metadata",
        dtype=dtypes.JSON_DTYPE,
    )
    expected.index = expected.index.astype(dtypes.INT_DTYPE)
    pd.testing.assert_series_equal(actual, expected)


def test_blob_content_type(images_mm_df: bpd.DataFrame):
    actual = images_mm_df["blob_col"].blob.content_type().to_pandas()
    expected = pd.Series(["image/jpeg", "image/jpeg"], name="content_type")

    pd.testing.assert_series_equal(
        actual, expected, check_dtype=False, check_index_type=False
    )


def test_blob_md5_hash(images_mm_df: bpd.DataFrame):
    actual = images_mm_df["blob_col"].blob.md5_hash().to_pandas()
    expected = pd.Series(
        ["e130ad042261a1883cd2cc06831cf748", "e2ae3191ff2b809fd0935f01a537c650"],
        name="md5_hash",
    )

    pd.testing.assert_series_equal(
        actual, expected, check_dtype=False, check_index_type=False
    )


def test_blob_size(images_mm_df: bpd.DataFrame):
    actual = images_mm_df["blob_col"].blob.size().to_pandas()
    expected = pd.Series([338390, 43333], name="size")

    pd.testing.assert_series_equal(
        actual, expected, check_dtype=False, check_index_type=False
    )


def test_blob_updated(images_mm_df: bpd.DataFrame):
    actual = images_mm_df["blob_col"].blob.updated().to_pandas()
    expected = pd.Series(
        [
            pd.Timestamp("2025-02-14 23:05:32", tz="UTC"),
            pd.Timestamp("2025-02-14 23:05:32", tz="UTC"),
        ],
        name="updated",
    )

    pd.testing.assert_series_equal(
        actual, expected, check_dtype=False, check_index_type=False
    )
