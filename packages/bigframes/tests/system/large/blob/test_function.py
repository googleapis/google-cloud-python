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

import logging
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

pytest.skip("Skipping blob tests due to b/481790217", allow_module_level=True)


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
    session: bigframes.Session,
):
    exif_image_df = session.from_glob_path(
        "gs://bigframes_blob_test/images_exif/*",
        name="blob_col",
        connection=bq_connection,
    )

    actual = exif_image_df["blob_col"].blob.exif(
        engine="pillow", connection=bq_connection, verbose=False
    )
    expected = bpd.Series(
        ['{"ExifOffset": 47, "Make": "MyCamera"}'],
        session=session,
        dtype=dtypes.JSON_DTYPE,
    )
    pd.testing.assert_series_equal(
        actual.to_pandas(),
        expected.to_pandas(),
        check_dtype=False,
        check_index_type=False,
    )


def test_blob_exif_verbose(
    bq_connection: str,
    session: bigframes.Session,
):
    exif_image_df = session.from_glob_path(
        "gs://bigframes_blob_test/images_exif/*",
        name="blob_col",
        connection=bq_connection,
    )

    actual = exif_image_df["blob_col"].blob.exif(
        engine="pillow", connection=bq_connection, verbose=True
    )
    assert hasattr(actual, "struct")
    actual_exploded = actual.struct.explode()
    assert "status" in actual_exploded.columns
    assert "content" in actual_exploded.columns

    status_series = actual_exploded["status"]
    assert status_series.dtype == dtypes.STRING_DTYPE

    content_series = actual_exploded["content"]
    assert content_series.dtype == dtypes.JSON_DTYPE


def test_blob_image_blur_to_series(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_uris: list[str],
    session: bigframes.Session,
):
    series = bpd.Series(images_output_uris, session=session).str.to_blob(
        connection=bq_connection
    )

    actual = images_mm_df["blob_col"].blob.image_blur(
        (8, 8), dst=series, connection=bq_connection, engine="opencv", verbose=False
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


def test_blob_image_blur_to_series_verbose(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_uris: list[str],
    session: bigframes.Session,
):
    series = bpd.Series(images_output_uris, session=session).str.to_blob(
        connection=bq_connection
    )

    actual = images_mm_df["blob_col"].blob.image_blur(
        (8, 8), dst=series, connection=bq_connection, engine="opencv", verbose=True
    )

    assert hasattr(actual, "struct")
    actual_exploded = actual.struct.explode()
    assert "status" in actual_exploded.columns
    assert "content" in actual_exploded.columns

    status_series = actual_exploded["status"]
    assert status_series.dtype == dtypes.STRING_DTYPE

    # Content should be blob objects for GCS destination
    # verify the files exist
    assert not actual.blob.size().isna().any()


def test_blob_image_blur_to_folder(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_folder: str,
    images_output_uris: list[str],
):
    actual = images_mm_df["blob_col"].blob.image_blur(
        (8, 8),
        dst=images_output_folder,
        connection=bq_connection,
        engine="opencv",
        verbose=False,
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


def test_blob_image_blur_to_folder_verbose(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_folder: str,
    images_output_uris: list[str],
):
    actual = images_mm_df["blob_col"].blob.image_blur(
        (8, 8),
        dst=images_output_folder,
        connection=bq_connection,
        engine="opencv",
        verbose=True,
    )
    assert hasattr(actual, "struct")
    actual_exploded = actual.struct.explode()
    assert "status" in actual_exploded.columns
    assert "content" in actual_exploded.columns

    status_series = actual_exploded["status"]
    assert status_series.dtype == dtypes.STRING_DTYPE

    content_series = actual_exploded["content"]
    # Content should be blob objects for GCS destination
    assert hasattr(content_series, "blob")

    # verify the files exist
    assert not actual.blob.size().isna().any()


def test_blob_image_blur_to_bq(images_mm_df: bpd.DataFrame, bq_connection: str):
    actual = images_mm_df["blob_col"].blob.image_blur(
        (8, 8), connection=bq_connection, engine="opencv", verbose=False
    )

    assert isinstance(actual, bpd.Series)
    assert len(actual) == 2
    assert actual.dtype == dtypes.BYTES_DTYPE


def test_blob_image_blur_to_bq_verbose(images_mm_df: bpd.DataFrame, bq_connection: str):
    actual = images_mm_df["blob_col"].blob.image_blur(
        (8, 8), connection=bq_connection, engine="opencv", verbose=True
    )

    assert isinstance(actual, bpd.Series)
    assert len(actual) == 2

    assert hasattr(actual, "struct")
    actual_exploded = actual.struct.explode()
    assert "status" in actual_exploded.columns
    assert "content" in actual_exploded.columns

    status_series = actual_exploded["status"]
    assert status_series.dtype == dtypes.STRING_DTYPE

    content_series = actual_exploded["content"]
    assert content_series.dtype == dtypes.BYTES_DTYPE


def test_blob_image_resize_to_series(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_uris: list[str],
    session: bigframes.Session,
):
    series = bpd.Series(images_output_uris, session=session).str.to_blob(
        connection=bq_connection
    )

    actual = images_mm_df["blob_col"].blob.image_resize(
        (200, 300),
        dst=series,
        connection=bq_connection,
        engine="opencv",
        verbose=False,
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


def test_blob_image_resize_to_series_verbose(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_uris: list[str],
    session: bigframes.Session,
):
    series = bpd.Series(images_output_uris, session=session).str.to_blob(
        connection=bq_connection
    )

    actual = images_mm_df["blob_col"].blob.image_resize(
        (200, 300),
        dst=series,
        connection=bq_connection,
        engine="opencv",
        verbose=True,
    )

    assert hasattr(actual, "struct")
    actual_exploded = actual.struct.explode()
    assert "status" in actual_exploded.columns
    assert "content" in actual_exploded.columns

    status_series = actual_exploded["status"]
    assert status_series.dtype == dtypes.STRING_DTYPE

    content_series = actual_exploded["content"]
    # Content should be blob objects for GCS destination
    assert hasattr(content_series, "blob")

    # verify the files exist
    assert not actual.blob.size().isna().any()


def test_blob_image_resize_to_folder(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_folder: str,
    images_output_uris: list[str],
):
    actual = images_mm_df["blob_col"].blob.image_resize(
        (200, 300),
        dst=images_output_folder,
        connection=bq_connection,
        engine="opencv",
        verbose=False,
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


def test_blob_image_resize_to_folder_verbose(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_folder: str,
    images_output_uris: list[str],
):
    actual = images_mm_df["blob_col"].blob.image_resize(
        (200, 300),
        dst=images_output_folder,
        connection=bq_connection,
        engine="opencv",
        verbose=True,
    )

    assert hasattr(actual, "struct")
    actual_exploded = actual.struct.explode()
    assert "status" in actual_exploded.columns
    assert "content" in actual_exploded.columns

    status_series = actual_exploded["status"]
    assert status_series.dtype == dtypes.STRING_DTYPE

    content_series = actual_exploded["content"]
    # Content should be blob objects for GCS destination
    assert hasattr(content_series, "blob")

    # verify the files exist
    assert not content_series.blob.size().isna().any()


def test_blob_image_resize_to_bq(images_mm_df: bpd.DataFrame, bq_connection: str):
    actual = images_mm_df["blob_col"].blob.image_resize(
        (200, 300), connection=bq_connection, engine="opencv", verbose=False
    )

    assert isinstance(actual, bpd.Series)
    assert len(actual) == 2
    assert actual.dtype == dtypes.BYTES_DTYPE


def test_blob_image_resize_to_bq_verbose(
    images_mm_df: bpd.DataFrame, bq_connection: str
):
    actual = images_mm_df["blob_col"].blob.image_resize(
        (200, 300), connection=bq_connection, engine="opencv", verbose=True
    )

    assert isinstance(actual, bpd.Series)
    assert len(actual) == 2

    assert hasattr(actual, "struct")
    actual_exploded = actual.struct.explode()
    assert "status" in actual_exploded.columns
    assert "content" in actual_exploded.columns

    status_series = actual_exploded["status"]
    assert status_series.dtype == dtypes.STRING_DTYPE

    content_series = actual_exploded["content"]
    assert content_series.dtype == dtypes.BYTES_DTYPE


def test_blob_image_normalize_to_series(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_uris: list[str],
    session: bigframes.Session,
):
    series = bpd.Series(images_output_uris, session=session).str.to_blob(
        connection=bq_connection
    )

    actual = images_mm_df["blob_col"].blob.image_normalize(
        alpha=50.0,
        beta=150.0,
        norm_type="minmax",
        dst=series,
        connection=bq_connection,
        engine="opencv",
        verbose=False,
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


def test_blob_image_normalize_to_series_verbose(
    images_mm_df: bpd.DataFrame,
    bq_connection: str,
    images_output_uris: list[str],
    session: bigframes.Session,
):
    series = bpd.Series(images_output_uris, session=session).str.to_blob(
        connection=bq_connection
    )

    actual = images_mm_df["blob_col"].blob.image_normalize(
        alpha=50.0,
        beta=150.0,
        norm_type="minmax",
        dst=series,
        connection=bq_connection,
        engine="opencv",
        verbose=True,
    )

    assert hasattr(actual, "struct")
    actual_exploded = actual.struct.explode()
    assert "status" in actual_exploded.columns
    assert "content" in actual_exploded.columns

    status_series = actual_exploded["status"]
    assert status_series.dtype == dtypes.STRING_DTYPE

    content_series = actual_exploded["content"]
    # Content should be blob objects for GCS destination
    assert hasattr(content_series, "blob")


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
        engine="opencv",
        verbose=False,
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


def test_blob_image_normalize_to_folder_verbose(
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
        engine="opencv",
        verbose=True,
    )

    assert hasattr(actual, "struct")
    actual_exploded = actual.struct.explode()
    assert "status" in actual_exploded.columns
    assert "content" in actual_exploded.columns

    status_series = actual_exploded["status"]
    assert status_series.dtype == dtypes.STRING_DTYPE

    content_series = actual_exploded["content"]
    # Content should be blob objects for GCS destination
    assert hasattr(content_series, "blob")


def test_blob_image_normalize_to_bq(images_mm_df: bpd.DataFrame, bq_connection: str):
    actual = images_mm_df["blob_col"].blob.image_normalize(
        alpha=50.0,
        beta=150.0,
        norm_type="minmax",
        connection=bq_connection,
        engine="opencv",
        verbose=False,
    )

    assert isinstance(actual, bpd.Series)
    assert len(actual) == 2
    assert actual.dtype == dtypes.BYTES_DTYPE


def test_blob_image_normalize_to_bq_verbose(
    images_mm_df: bpd.DataFrame, bq_connection: str
):
    actual = images_mm_df["blob_col"].blob.image_normalize(
        alpha=50.0,
        beta=150.0,
        norm_type="minmax",
        connection=bq_connection,
        engine="opencv",
        verbose=True,
    )

    assert isinstance(actual, bpd.Series)
    assert len(actual) == 2

    assert hasattr(actual, "struct")
    actual_exploded = actual.struct.explode()
    assert "status" in actual_exploded.columns
    assert "content" in actual_exploded.columns

    status_series = actual_exploded["status"]
    assert status_series.dtype == dtypes.STRING_DTYPE

    content_series = actual_exploded["content"]
    assert content_series.dtype == dtypes.BYTES_DTYPE


def test_blob_pdf_extract(
    pdf_mm_df: bpd.DataFrame,
    bq_connection: str,
):
    actual = (
        pdf_mm_df["pdf"]
        .blob.pdf_extract(connection=bq_connection, verbose=False, engine="pypdf")
        .explode()
        .to_pandas()
    )

    # check relative length
    expected_text = "Sample PDF This is a testing file. Some dummy messages are used for testing purposes."
    expected_len = len(expected_text)

    actual_text = actual[actual != ""].iloc[0]
    actual_len = len(actual_text)

    relative_length_tolerance = 0.25
    min_acceptable_len = expected_len * (1 - relative_length_tolerance)
    max_acceptable_len = expected_len * (1 + relative_length_tolerance)
    assert min_acceptable_len <= actual_len <= max_acceptable_len, (
        f"Item (verbose=False): Extracted text length {actual_len} is outside the acceptable range "
        f"[{min_acceptable_len:.0f}, {max_acceptable_len:.0f}]. "
        f"Expected reference length was {expected_len}. "
    )

    # check for major keywords
    major_keywords = ["Sample", "PDF", "testing", "dummy", "messages"]
    for keyword in major_keywords:
        assert (
            keyword.lower() in actual_text.lower()
        ), f"Item (verbose=False): Expected keyword '{keyword}' not found in extracted text. "


def test_blob_pdf_extract_verbose(
    pdf_mm_df: bpd.DataFrame,
    bq_connection: str,
):
    actual = (
        pdf_mm_df["pdf"]
        .blob.pdf_extract(connection=bq_connection, verbose=True, engine="pypdf")
        .explode()
        .to_pandas()
    )

    # check relative length
    expected_text = "Sample PDF This is a testing file. Some dummy messages are used for testing purposes."
    expected_len = len(expected_text)

    # The first entry is for a file that doesn't exist, so we check the second one
    successful_results = actual[actual.apply(lambda x: x["status"] == "")]
    actual_text = successful_results.apply(lambda x: x["content"]).iloc[0]
    actual_len = len(actual_text)

    relative_length_tolerance = 0.25
    min_acceptable_len = expected_len * (1 - relative_length_tolerance)
    max_acceptable_len = expected_len * (1 + relative_length_tolerance)
    assert min_acceptable_len <= actual_len <= max_acceptable_len, (
        f"Item (verbose=True): Extracted text length {actual_len} is outside the acceptable range "
        f"[{min_acceptable_len:.0f}, {max_acceptable_len:.0f}]. "
        f"Expected reference length was {expected_len}. "
    )

    # check for major keywords
    major_keywords = ["Sample", "PDF", "testing", "dummy", "messages"]
    for keyword in major_keywords:
        assert (
            keyword.lower() in actual_text.lower()
        ), f"Item (verbose=True): Expected keyword '{keyword}' not found in extracted text. "


def test_blob_pdf_chunk(pdf_mm_df: bpd.DataFrame, bq_connection: str):
    actual = (
        pdf_mm_df["pdf"]
        .blob.pdf_chunk(
            connection=bq_connection,
            chunk_size=50,
            overlap_size=10,
            verbose=False,
            engine="pypdf",
        )
        .explode()
        .to_pandas()
    )

    # check relative length
    expected_text = "Sample PDF This is a testing file. Some dummy messages are used for testing purposes."
    expected_len = len(expected_text)

    # First entry is NA
    actual_text = "".join(actual.dropna())
    actual_len = len(actual_text)

    relative_length_tolerance = 0.25
    min_acceptable_len = expected_len * (1 - relative_length_tolerance)
    max_acceptable_len = expected_len * (1 + relative_length_tolerance)
    assert min_acceptable_len <= actual_len <= max_acceptable_len, (
        f"Item (verbose=False): Extracted text length {actual_len} is outside the acceptable range "
        f"[{min_acceptable_len:.0f}, {max_acceptable_len:.0f}]. "
        f"Expected reference length was {expected_len}. "
    )

    # check for major keywords
    major_keywords = ["Sample", "PDF", "testing", "dummy", "messages"]
    for keyword in major_keywords:
        assert (
            keyword.lower() in actual_text.lower()
        ), f"Item (verbose=False): Expected keyword '{keyword}' not found in extracted text. "


def test_blob_pdf_chunk_verbose(pdf_mm_df: bpd.DataFrame, bq_connection: str):
    actual = (
        pdf_mm_df["pdf"]
        .blob.pdf_chunk(
            connection=bq_connection,
            chunk_size=50,
            overlap_size=10,
            verbose=True,
            engine="pypdf",
        )
        .explode()
        .to_pandas()
    )

    # check relative length
    expected_text = "Sample PDF This is a testing file. Some dummy messages are used for testing purposes."
    expected_len = len(expected_text)

    # The first entry is for a file that doesn't exist, so we check the second one
    successful_results = actual[actual.apply(lambda x: x["status"] == "")]
    actual_text = "".join(successful_results.apply(lambda x: x["content"]).iloc[0])
    actual_len = len(actual_text)

    relative_length_tolerance = 0.25
    min_acceptable_len = expected_len * (1 - relative_length_tolerance)
    max_acceptable_len = expected_len * (1 + relative_length_tolerance)
    assert min_acceptable_len <= actual_len <= max_acceptable_len, (
        f"Item (verbose=True): Extracted text length {actual_len} is outside the acceptable range "
        f"[{min_acceptable_len:.0f}, {max_acceptable_len:.0f}]. "
        f"Expected reference length was {expected_len}. "
    )

    # check for major keywords
    major_keywords = ["Sample", "PDF", "testing", "dummy", "messages"]
    for keyword in major_keywords:
        assert (
            keyword.lower() in actual_text.lower()
        ), f"Item (verbose=True): Expected keyword '{keyword}' not found in extracted text. "


@pytest.mark.parametrize(
    "model_name",
    [
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-lite-001",
    ],
)
def test_blob_transcribe(
    audio_mm_df: bpd.DataFrame,
    model_name: str,
):
    actual = (
        audio_mm_df["audio"]
        .blob.audio_transcribe(
            model_name=model_name,  # type: ignore
            verbose=False,
        )
        .to_pandas()
    )

    # check relative length
    expected_text = "Now, as all books not primarily intended as picture-books consist principally of types composed to form letterpress"
    expected_len = len(expected_text)

    actual_text = actual[0]

    if pd.isna(actual_text) or actual_text == "":
        # Ensure the tests are robust to flakes in the model, which isn't
        # particularly useful information for the bigframes team.
        logging.warning(f"blob_transcribe() model {model_name} verbose=False failure")
        return

    actual_len = len(actual_text)

    relative_length_tolerance = 0.2
    min_acceptable_len = expected_len * (1 - relative_length_tolerance)
    max_acceptable_len = expected_len * (1 + relative_length_tolerance)
    assert min_acceptable_len <= actual_len <= max_acceptable_len, (
        f"Item (verbose=False): Transcribed text length {actual_len} is outside the acceptable range "
        f"[{min_acceptable_len:.0f}, {max_acceptable_len:.0f}]. "
        f"Expected reference length was {expected_len}. "
    )

    # check for major keywords
    major_keywords = ["book", "picture"]
    for keyword in major_keywords:
        assert (
            keyword.lower() in actual_text.lower()
        ), f"Item (verbose=False): Expected keyword '{keyword}' not found in transcribed text. "


@pytest.mark.parametrize(
    "model_name",
    [
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-lite-001",
    ],
)
def test_blob_transcribe_verbose(
    audio_mm_df: bpd.DataFrame,
    model_name: str,
):
    actual = (
        audio_mm_df["audio"]
        .blob.audio_transcribe(
            model_name=model_name,  # type: ignore
            verbose=True,
        )
        .to_pandas()
    )

    # check relative length
    expected_text = "Now, as all books not primarily intended as picture-books consist principally of types composed to form letterpress"
    expected_len = len(expected_text)

    actual_text = actual[0]["content"]

    if pd.isna(actual_text) or actual_text == "":
        # Ensure the tests are robust to flakes in the model, which isn't
        # particularly useful information for the bigframes team.
        logging.warning(f"blob_transcribe() model {model_name} verbose=True failure")
        return

    actual_len = len(actual_text)

    relative_length_tolerance = 0.2
    min_acceptable_len = expected_len * (1 - relative_length_tolerance)
    max_acceptable_len = expected_len * (1 + relative_length_tolerance)
    assert min_acceptable_len <= actual_len <= max_acceptable_len, (
        f"Item (verbose=True): Transcribed text length {actual_len} is outside the acceptable range "
        f"[{min_acceptable_len:.0f}, {max_acceptable_len:.0f}]. "
        f"Expected reference length was {expected_len}. "
    )

    # check for major keywords
    major_keywords = ["book", "picture"]
    for keyword in major_keywords:
        assert (
            keyword.lower() in actual_text.lower()
        ), f"Item (verbose=True): Expected keyword '{keyword}' not found in transcribed text. "
