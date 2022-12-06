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

import pytest

with pytest.warns(UserWarning):
    from google.cloud.storage import transfer_manager

from google.api_core import exceptions

import os
import tempfile
import unittest
import mock


class Test_Transfer_Manager(unittest.TestCase):
    def test_upload_many_with_filenames(self):
        FILE_BLOB_PAIRS = [("file_a.txt", mock.Mock()), ("file_b.txt", mock.Mock())]
        FAKE_CONTENT_TYPE = "text/fake"
        UPLOAD_KWARGS = {"content-type": FAKE_CONTENT_TYPE}
        EXPECTED_UPLOAD_KWARGS = {"if_generation_match": 0, **UPLOAD_KWARGS}
        FAKE_RESULT = "nothing to see here"

        for _, blob_mock in FILE_BLOB_PAIRS:
            blob_mock.upload_from_filename.return_value = FAKE_RESULT

        results = transfer_manager.upload_many(
            FILE_BLOB_PAIRS, skip_if_exists=True, upload_kwargs=UPLOAD_KWARGS
        )
        for (filename, mock_blob) in FILE_BLOB_PAIRS:
            mock_blob.upload_from_filename.assert_any_call(
                filename, **EXPECTED_UPLOAD_KWARGS
            )
        for result in results:
            self.assertEqual(result, FAKE_RESULT)

    def test_upload_many_with_file_objs(self):
        FILE_BLOB_PAIRS = [
            (tempfile.TemporaryFile(), mock.Mock()),
            (tempfile.TemporaryFile(), mock.Mock()),
        ]
        FAKE_CONTENT_TYPE = "text/fake"
        UPLOAD_KWARGS = {"content-type": FAKE_CONTENT_TYPE}
        EXPECTED_UPLOAD_KWARGS = {"if_generation_match": 0, **UPLOAD_KWARGS}
        FAKE_RESULT = "nothing to see here"

        for _, blob_mock in FILE_BLOB_PAIRS:
            blob_mock.upload_from_file.return_value = FAKE_RESULT

        results = transfer_manager.upload_many(
            FILE_BLOB_PAIRS, skip_if_exists=True, upload_kwargs=UPLOAD_KWARGS
        )
        for (file, mock_blob) in FILE_BLOB_PAIRS:
            mock_blob.upload_from_file.assert_any_call(file, **EXPECTED_UPLOAD_KWARGS)
        for result in results:
            self.assertEqual(result, FAKE_RESULT)

    def test_upload_many_passes_concurrency_options(self):
        FILE_BLOB_PAIRS = [
            (tempfile.TemporaryFile(), mock.Mock()),
            (tempfile.TemporaryFile(), mock.Mock()),
        ]
        MAX_WORKERS = 7
        DEADLINE = 10
        with mock.patch(
            "concurrent.futures.ThreadPoolExecutor"
        ) as pool_patch, mock.patch("concurrent.futures.wait") as wait_patch:
            transfer_manager.upload_many(
                FILE_BLOB_PAIRS, threads=MAX_WORKERS, deadline=DEADLINE
            )
            pool_patch.assert_called_with(max_workers=MAX_WORKERS)
            wait_patch.assert_called_with(
                mock.ANY, timeout=DEADLINE, return_when=mock.ANY
            )

    def test_upload_many_suppresses_exceptions(self):
        FILE_BLOB_PAIRS = [("file_a.txt", mock.Mock()), ("file_b.txt", mock.Mock())]
        for _, mock_blob in FILE_BLOB_PAIRS:
            mock_blob.upload_from_filename.side_effect = ConnectionError()

        results = transfer_manager.upload_many(FILE_BLOB_PAIRS)
        for result in results:
            self.assertEqual(type(result), ConnectionError)

    def test_upload_many_raises_exceptions(self):
        FILE_BLOB_PAIRS = [("file_a.txt", mock.Mock()), ("file_b.txt", mock.Mock())]
        for _, mock_blob in FILE_BLOB_PAIRS:
            mock_blob.upload_from_filename.side_effect = ConnectionError()

        with self.assertRaises(ConnectionError):
            transfer_manager.upload_many(FILE_BLOB_PAIRS, raise_exception=True)

    def test_upload_many_suppresses_412_with_skip_if_exists(self):
        FILE_BLOB_PAIRS = [("file_a.txt", mock.Mock()), ("file_b.txt", mock.Mock())]
        for _, mock_blob in FILE_BLOB_PAIRS:
            mock_blob.upload_from_filename.side_effect = exceptions.PreconditionFailed(
                "412"
            )

        results = transfer_manager.upload_many(
            FILE_BLOB_PAIRS, skip_if_exists=True, raise_exception=True
        )
        for result in results:
            self.assertEqual(type(result), exceptions.PreconditionFailed)

    def test_download_many_with_filenames(self):
        BLOB_FILE_PAIRS = [(mock.Mock(), "file_a.txt"), (mock.Mock(), "file_b.txt")]
        FAKE_ENCODING = "fake_gzip"
        DOWNLOAD_KWARGS = {"accept-encoding": FAKE_ENCODING}
        FAKE_RESULT = "nothing to see here"

        for blob_mock, _ in BLOB_FILE_PAIRS:
            blob_mock.download_to_filename.return_value = FAKE_RESULT

        results = transfer_manager.download_many(
            BLOB_FILE_PAIRS, download_kwargs=DOWNLOAD_KWARGS
        )
        for (mock_blob, file) in BLOB_FILE_PAIRS:
            mock_blob.download_to_filename.assert_any_call(file, **DOWNLOAD_KWARGS)
        for result in results:
            self.assertEqual(result, FAKE_RESULT)

    def test_download_many_with_file_objs(self):
        BLOB_FILE_PAIRS = [
            (mock.Mock(), tempfile.TemporaryFile()),
            (mock.Mock(), tempfile.TemporaryFile()),
        ]
        FAKE_ENCODING = "fake_gzip"
        DOWNLOAD_KWARGS = {"accept-encoding": FAKE_ENCODING}
        FAKE_RESULT = "nothing to see here"

        for blob_mock, _ in BLOB_FILE_PAIRS:
            blob_mock.download_to_file.return_value = FAKE_RESULT

        results = transfer_manager.download_many(
            BLOB_FILE_PAIRS, download_kwargs=DOWNLOAD_KWARGS
        )
        for (mock_blob, file) in BLOB_FILE_PAIRS:
            mock_blob.download_to_file.assert_any_call(file, **DOWNLOAD_KWARGS)
        for result in results:
            self.assertEqual(result, FAKE_RESULT)

    def test_download_many_passes_concurrency_options(self):
        BLOB_FILE_PAIRS = [
            (mock.Mock(), tempfile.TemporaryFile()),
            (mock.Mock(), tempfile.TemporaryFile()),
        ]
        MAX_WORKERS = 7
        DEADLINE = 10
        with mock.patch(
            "concurrent.futures.ThreadPoolExecutor"
        ) as pool_patch, mock.patch("concurrent.futures.wait") as wait_patch:
            transfer_manager.download_many(
                BLOB_FILE_PAIRS, threads=MAX_WORKERS, deadline=DEADLINE
            )
            pool_patch.assert_called_with(max_workers=MAX_WORKERS)
            wait_patch.assert_called_with(
                mock.ANY, timeout=DEADLINE, return_when=mock.ANY
            )

    def test_download_many_suppresses_exceptions(self):
        BLOB_FILE_PAIRS = [(mock.Mock(), "file_a.txt"), (mock.Mock(), "file_b.txt")]
        for mock_blob, _ in BLOB_FILE_PAIRS:
            mock_blob.download_to_filename.side_effect = ConnectionError()

        results = transfer_manager.download_many(BLOB_FILE_PAIRS)
        for result in results:
            self.assertEqual(type(result), ConnectionError)

    def test_download_many_raises_exceptions(self):
        BLOB_FILE_PAIRS = [(mock.Mock(), "file_a.txt"), (mock.Mock(), "file_b.txt")]
        for mock_blob, _ in BLOB_FILE_PAIRS:
            mock_blob.download_to_filename.side_effect = ConnectionError()

        transfer_manager.download_many(BLOB_FILE_PAIRS)
        with self.assertRaises(ConnectionError):
            transfer_manager.download_many(BLOB_FILE_PAIRS, raise_exception=True)

    def test_upload_many_from_filenames(self):
        bucket = mock.Mock()

        FILENAMES = ["file_a.txt", "file_b.txt"]
        ROOT = "mypath/"
        PREFIX = "myprefix/"
        KEY_NAME = "keyname"
        BLOB_CONSTRUCTOR_KWARGS = {"kms_key_name": KEY_NAME}
        UPLOAD_KWARGS = {"content-type": "text/fake"}
        MAX_WORKERS = 7
        DEADLINE = 10

        EXPECTED_FILE_BLOB_PAIRS = [
            (os.path.join(ROOT, filename), mock.ANY) for filename in FILENAMES
        ]

        with mock.patch(
            "google.cloud.storage.transfer_manager.upload_many"
        ) as mock_upload_many:
            transfer_manager.upload_many_from_filenames(
                bucket,
                FILENAMES,
                source_directory=ROOT,
                blob_name_prefix=PREFIX,
                skip_if_exists=True,
                blob_constructor_kwargs=BLOB_CONSTRUCTOR_KWARGS,
                upload_kwargs=UPLOAD_KWARGS,
                threads=MAX_WORKERS,
                deadline=DEADLINE,
                raise_exception=True,
            )

        mock_upload_many.assert_called_once_with(
            EXPECTED_FILE_BLOB_PAIRS,
            skip_if_exists=True,
            upload_kwargs=UPLOAD_KWARGS,
            threads=MAX_WORKERS,
            deadline=DEADLINE,
            raise_exception=True,
        )
        bucket.blob.assert_any_call(PREFIX + FILENAMES[0], **BLOB_CONSTRUCTOR_KWARGS)
        bucket.blob.assert_any_call(PREFIX + FILENAMES[1], **BLOB_CONSTRUCTOR_KWARGS)

    def test_upload_many_from_filenames_minimal_args(self):
        bucket = mock.Mock()

        FILENAMES = ["file_a.txt", "file_b.txt"]

        EXPECTED_FILE_BLOB_PAIRS = [(filename, mock.ANY) for filename in FILENAMES]

        with mock.patch(
            "google.cloud.storage.transfer_manager.upload_many"
        ) as mock_upload_many:
            transfer_manager.upload_many_from_filenames(
                bucket,
                FILENAMES,
            )

        mock_upload_many.assert_called_once_with(
            EXPECTED_FILE_BLOB_PAIRS,
            skip_if_exists=False,
            upload_kwargs=None,
            threads=4,
            deadline=None,
            raise_exception=False,
        )
        bucket.blob.assert_any_call(FILENAMES[0])
        bucket.blob.assert_any_call(FILENAMES[1])

    def test_download_many_to_path(self):
        bucket = mock.Mock()

        BLOBNAMES = ["file_a.txt", "file_b.txt", "dir_a/file_c.txt"]
        PATH_ROOT = "mypath/"
        BLOB_NAME_PREFIX = "myprefix/"
        DOWNLOAD_KWARGS = {"accept-encoding": "fake-gzip"}
        MAX_WORKERS = 7
        DEADLINE = 10

        EXPECTED_BLOB_FILE_PAIRS = [
            (mock.ANY, os.path.join(PATH_ROOT, blobname)) for blobname in BLOBNAMES
        ]

        with mock.patch(
            "google.cloud.storage.transfer_manager.download_many"
        ) as mock_download_many:
            transfer_manager.download_many_to_path(
                bucket,
                BLOBNAMES,
                destination_directory=PATH_ROOT,
                blob_name_prefix=BLOB_NAME_PREFIX,
                download_kwargs=DOWNLOAD_KWARGS,
                threads=MAX_WORKERS,
                deadline=DEADLINE,
                create_directories=False,
                raise_exception=True,
            )

        mock_download_many.assert_called_once_with(
            EXPECTED_BLOB_FILE_PAIRS,
            download_kwargs=DOWNLOAD_KWARGS,
            threads=MAX_WORKERS,
            deadline=DEADLINE,
            raise_exception=True,
        )
        for blobname in BLOBNAMES:
            bucket.blob.assert_any_call(BLOB_NAME_PREFIX + blobname)

    def test_download_many_to_path_creates_directories(self):
        bucket = mock.Mock()

        with tempfile.TemporaryDirectory() as tempdir:
            DIR_NAME = "dir_a/dir_b"
            BLOBNAMES = [
                "file_a.txt",
                "file_b.txt",
                os.path.join(DIR_NAME, "file_c.txt"),
            ]

            EXPECTED_BLOB_FILE_PAIRS = [
                (mock.ANY, os.path.join(tempdir, blobname)) for blobname in BLOBNAMES
            ]

            with mock.patch(
                "google.cloud.storage.transfer_manager.download_many"
            ) as mock_download_many:
                transfer_manager.download_many_to_path(
                    bucket,
                    BLOBNAMES,
                    destination_directory=tempdir,
                    create_directories=True,
                    raise_exception=True,
                )

            mock_download_many.assert_called_once_with(
                EXPECTED_BLOB_FILE_PAIRS,
                download_kwargs=None,
                threads=4,
                deadline=None,
                raise_exception=True,
            )
            for blobname in BLOBNAMES:
                bucket.blob.assert_any_call(blobname)

            assert os.path.isdir(os.path.join(tempdir, DIR_NAME))
