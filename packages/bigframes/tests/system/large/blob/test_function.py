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

import os
import traceback
from typing import Generator
import uuid

from google.cloud import storage
import pandas as pd
import pytest

import bigframes
from bigframes import dtypes
import bigframes.pandas as bpd


@pytest.fixture(scope="function")
def images_output_folder() -> Generator[str, None, None]:
    id = uuid.uuid4().hex
    folder = os.path.join("gs://bigframes_blob_test/output/", id)
    yield folder

    # clean up
    try:
        cloud_storage_client = storage.Client()
        bucket = cloud_storage_client.bucket("bigframes_blob_test")
        blobs = bucket.list_blobs(prefix="output/" + id)
        for blob in blobs:
            blob.delete()
    except Exception as exc:
        traceback.print_exception(type(exc), exc, None)


@pytest.fixture(scope="function")
def images_output_uris(images_output_folder: str) -> list[str]:
    return [
        os.path.join(images_output_folder, "img0.jpg"),
        os.path.join(images_output_folder, "img1.jpg"),
    ]


def test_blob_exif(
    bq_connection: str,
    test_session: bigframes.Session,
):
    exif_image_df = test_session.from_glob_path(
        "gs://bigframes_blob_test/images_exif/*",
        name="blob_col",
        connection=bq_connection,
    )

    actual = exif_image_df["blob_col"].blob.exif(connection=bq_connection)
    expected = bpd.Series(
        ['{"ExifOffset": 47, "Make": "MyCamera"}'],
        session=test_session,
        dtype=dtypes.JSON_DTYPE,
    )
    pd.testing.assert_series_equal(
        actual.to_pandas(),
        expected.to_pandas(),
        check_dtype=False,
        check_index_type=False,
    )


def test_blob_image_blur_to_series(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_uris: list[str],
    test_session: bigframes.Session,
):
    series = bpd.Series(images_output_uris, session=test_session).str.to_blob(
        connection=bq_connection
    )

    actual = images_mm_df["blob_col"].blob.image_blur(
        (8, 8), dst=series, connection=bq_connection
    )
    expected_df = pd.DataFrame(
        {
            "uri": images_output_uris,
            "version": [None, None],
            "authorizer": [bq_connection.casefold(), bq_connection.casefold()],
            "details": [None, None],
        }
    )
    pd.testing.assert_frame_equal(
        actual.struct.explode().to_pandas(),
        expected_df,
        check_dtype=False,
        check_index_type=False,
    )

    # verify the files exist
    assert not actual.blob.size().isna().any()


def test_blob_image_blur_to_folder(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_folder: str,
    images_output_uris: list[str],
):
    actual = images_mm_df["blob_col"].blob.image_blur(
        (8, 8), dst=images_output_folder, connection=bq_connection
    )
    expected_df = pd.DataFrame(
        {
            "uri": images_output_uris,
            "version": [None, None],
            "authorizer": [bq_connection.casefold(), bq_connection.casefold()],
            "details": [None, None],
        }
    )
    pd.testing.assert_frame_equal(
        actual.struct.explode().to_pandas(),
        expected_df,
        check_dtype=False,
        check_index_type=False,
    )

    # verify the files exist
    assert not actual.blob.size().isna().any()


def test_blob_image_blur_to_bq(images_mm_df: bpd.DataFrame, bq_connection: str):
    actual = images_mm_df["blob_col"].blob.image_blur((8, 8), connection=bq_connection)

    assert isinstance(actual, bpd.Series)
    assert len(actual) == 2
    assert actual.dtype == dtypes.BYTES_DTYPE


def test_blob_image_resize_to_series(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_uris: list[str],
    test_session: bigframes.Session,
):
    series = bpd.Series(images_output_uris, session=test_session).str.to_blob(
        connection=bq_connection
    )

    actual = images_mm_df["blob_col"].blob.image_resize(
        (200, 300), dst=series, connection=bq_connection
    )
    expected_df = pd.DataFrame(
        {
            "uri": images_output_uris,
            "version": [None, None],
            "authorizer": [bq_connection.casefold(), bq_connection.casefold()],
            "details": [None, None],
        }
    )
    pd.testing.assert_frame_equal(
        actual.struct.explode().to_pandas(),
        expected_df,
        check_dtype=False,
        check_index_type=False,
    )

    # verify the files exist
    assert not actual.blob.size().isna().any()


def test_blob_image_resize_to_folder(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_folder: str,
    images_output_uris: list[str],
):
    actual = images_mm_df["blob_col"].blob.image_resize(
        (200, 300), dst=images_output_folder, connection=bq_connection
    )
    expected_df = pd.DataFrame(
        {
            "uri": images_output_uris,
            "version": [None, None],
            "authorizer": [bq_connection.casefold(), bq_connection.casefold()],
            "details": [None, None],
        }
    )
    pd.testing.assert_frame_equal(
        actual.struct.explode().to_pandas(),
        expected_df,
        check_dtype=False,
        check_index_type=False,
    )

    # verify the files exist
    assert not actual.blob.size().isna().any()


def test_blob_image_resize_to_bq(images_mm_df: bpd.DataFrame, bq_connection: str):
    actual = images_mm_df["blob_col"].blob.image_resize(
        (200, 300), connection=bq_connection
    )

    assert isinstance(actual, bpd.Series)
    assert len(actual) == 2
    assert actual.dtype == dtypes.BYTES_DTYPE


def test_blob_image_normalize_to_series(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_uris: list[str],
    test_session: bigframes.Session,
):
    series = bpd.Series(images_output_uris, session=test_session).str.to_blob(
        connection=bq_connection
    )

    actual = images_mm_df["blob_col"].blob.image_normalize(
        alpha=50.0, beta=150.0, norm_type="minmax", dst=series, connection=bq_connection
    )
    expected_df = pd.DataFrame(
        {
            "uri": images_output_uris,
            "version": [None, None],
            "authorizer": [bq_connection.casefold(), bq_connection.casefold()],
            "details": [None, None],
        }
    )
    pd.testing.assert_frame_equal(
        actual.struct.explode().to_pandas(),
        expected_df,
        check_dtype=False,
        check_index_type=False,
    )

    # verify the files exist
    assert not actual.blob.size().isna().any()


def test_blob_image_normalize_to_folder(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_folder: str,
    images_output_uris: list[str],
):
    actual = images_mm_df["blob_col"].blob.image_normalize(
        alpha=50.0,
        beta=150.0,
        norm_type="minmax",
        dst=images_output_folder,
        connection=bq_connection,
    )
    expected_df = pd.DataFrame(
        {
            "uri": images_output_uris,
            "version": [None, None],
            "authorizer": [bq_connection.casefold(), bq_connection.casefold()],
            "details": [None, None],
        }
    )
    pd.testing.assert_frame_equal(
        actual.struct.explode().to_pandas(),
        expected_df,
        check_dtype=False,
        check_index_type=False,
    )

    # verify the files exist
    assert not actual.blob.size().isna().any()


def test_blob_image_normalize_to_bq(images_mm_df: bpd.DataFrame, bq_connection: str):
    actual = images_mm_df["blob_col"].blob.image_normalize(
        alpha=50.0, beta=150.0, norm_type="minmax", connection=bq_connection
    )

    assert isinstance(actual, bpd.Series)
    assert len(actual) == 2
    assert actual.dtype == dtypes.BYTES_DTYPE


@pytest.mark.parametrize(
    "verbose, expected",
    [
        (
            True,
            pd.Series(
                [
                    {"status": "File has not been decrypted", "content": ""},
                    {
                        "status": "",
                        "content": "Sample  PDF    This  is  a  testing  file.  Some  dummy  messages  are  used  for  testing  purposes.   ",
                    },
                ]
            ),
        ),
        (
            False,
            pd.Series(
                [
                    "",
                    "Sample  PDF    This  is  a  testing  file.  Some  dummy  messages  are  used  for  testing  purposes.   ",
                ],
                name="pdf",
            ),
        ),
    ],
)
def test_blob_pdf_extract(
    pdf_mm_df: bpd.DataFrame,
    verbose: bool,
    bq_connection: str,
    expected: pd.Series,
):
    actual = (
        pdf_mm_df["pdf"]
        .blob.pdf_extract(connection=bq_connection, verbose=verbose)
        .explode()
        .to_pandas()
    )

    pd.testing.assert_series_equal(
        actual,
        expected,
        check_dtype=False,
        check_index=False,
    )


@pytest.mark.parametrize(
    "verbose, expected",
    [
        (
            True,
            pd.Series(
                [
                    {"status": "File has not been decrypted", "content": []},
                    {
                        "status": "",
                        "content": [
                            "Sample  PDF    This  is  a  testing  file.  Some ",
                            "dummy  messages  are  used  for  testing ",
                            "purposes.   ",
                        ],
                    },
                ]
            ),
        ),
        (
            False,
            pd.Series(
                [
                    pd.NA,
                    "Sample  PDF    This  is  a  testing  file.  Some ",
                    "dummy  messages  are  used  for  testing ",
                    "purposes.   ",
                ],
            ),
        ),
    ],
)
def test_blob_pdf_chunk(
    pdf_mm_df: bpd.DataFrame, verbose: bool, bq_connection: str, expected: pd.Series
):
    actual = (
        pdf_mm_df["pdf"]
        .blob.pdf_chunk(
            connection=bq_connection, chunk_size=50, overlap_size=10, verbose=verbose
        )
        .explode()
        .to_pandas()
    )

    pd.testing.assert_series_equal(
        actual,
        expected,
        check_dtype=False,
        check_index=False,
    )
