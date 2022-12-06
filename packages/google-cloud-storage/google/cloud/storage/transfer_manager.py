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

"""Concurrent media operations. This is a PREVIEW FEATURE: API may change."""

import concurrent.futures

import os
import warnings

from google.api_core import exceptions

warnings.warn(
    "The module `transfer_manager` is a preview feature. Functionality and API "
    "may change. This warning will be removed in a future release."
)


DEFAULT_CHUNK_SIZE = 200 * 1024 * 1024


def upload_many(
    file_blob_pairs,
    skip_if_exists=False,
    upload_kwargs=None,
    threads=4,
    deadline=None,
    raise_exception=False,
):
    """Upload many files concurrently via a worker pool.

    This function is a PREVIEW FEATURE: the API may change in a future version.

    :type file_blob_pairs: List(Tuple(IOBase or str, 'google.cloud.storage.blob.Blob'))
    :param file_blob_pairs:
        A list of tuples of a file or filename and a blob. Each file will be
        uploaded to the corresponding blob by using blob.upload_from_file() or
        blob.upload_from_filename() as appropriate.

    :type skip_if_exists: bool
    :param skip_if_exists:
        If True, blobs that already have a live version will not be overwritten.
        This is accomplished by setting "if_generation_match = 0" on uploads.
        Uploads so skipped will result in a 412 Precondition Failed response
        code, which will be included in the return value but not raised
        as an exception regardless of the value of raise_exception.

    :type upload_kwargs: dict
    :param upload_kwargs:
        A dictionary of keyword arguments to pass to the upload method. Refer
        to the documentation for blob.upload_from_file() or
        blob.upload_from_filename() for more information. The dict is directly
        passed into the upload methods and is not validated by this function.

    :type threads: int
    :param threads:
        The number of threads to use in the worker pool. This is passed to
        `concurrent.futures.ThreadPoolExecutor` as the `max_worker`; refer
        to standard library documentation for details.

        The performance impact of this value depends on the use case, but
        generally, smaller files benefit from more threads and larger files
        don't benefit from more threads. Too many threads can slow operations,
        especially with large files, due to contention over the Python GIL.

    :type deadline: int
    :param deadline:
        The number of seconds to wait for all threads to resolve. If the
        deadline is reached, all threads will be terminated regardless of their
        progress and concurrent.futures.TimeoutError will be raised. This can be
        left as the default of None (no deadline) for most use cases.

    :type raise_exception: bool
    :param raise_exception:
        If True, instead of adding exceptions to the list of return values,
        instead they will be raised. Note that encountering an exception on one
        operation will not prevent other operations from starting. Exceptions
        are only processed and potentially raised after all operations are
        complete in success or failure.

        If skip_if_exists is True, 412 Precondition Failed responses are
        considered part of normal operation and are not raised as an exception.

    :raises: :exc:`concurrent.futures.TimeoutError` if deadline is exceeded.

    :rtype: list
    :returns: A list of results corresponding to, in order, each item in the
        input list. If an exception was received, it will be the result
        for that operation. Otherwise, the return value from the successful
        upload method is used (typically, None).
    """
    if upload_kwargs is None:
        upload_kwargs = {}
    if skip_if_exists:
        upload_kwargs["if_generation_match"] = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for path_or_file, blob in file_blob_pairs:
            method = (
                blob.upload_from_filename
                if isinstance(path_or_file, str)
                else blob.upload_from_file
            )
            futures.append(executor.submit(method, path_or_file, **upload_kwargs))
    results = []
    concurrent.futures.wait(
        futures, timeout=deadline, return_when=concurrent.futures.ALL_COMPLETED
    )
    for future in futures:
        exp = future.exception()

        # If raise_exception is False, don't call future.result()
        if exp and not raise_exception:
            results.append(exp)
        # If skip_if_exists and the exception is PreconditionFailed, do same.
        elif exp and skip_if_exists and isinstance(exp, exceptions.PreconditionFailed):
            results.append(exp)
        # Get the real result. If there was an exception not handled above,
        # this will raise it.
        else:
            results.append(future.result())
    return results


def download_many(
    blob_file_pairs,
    download_kwargs=None,
    threads=4,
    deadline=None,
    raise_exception=False,
):
    """Download many blobs concurrently via a worker pool.

    This function is a PREVIEW FEATURE: the API may change in a future version.

    :type blob_file_pairs: List(Tuple('google.cloud.storage.blob.Blob', IOBase or str))
    :param blob_file_pairs:
        A list of tuples of blob and a file or filename. Each blob will be
        downloaded to the corresponding blob by using blob.download_to_file() or
        blob.download_to_filename() as appropriate.

        Note that blob.download_to_filename() does not delete the destination
        file if the download fails.

    :type download_kwargs: dict
    :param download_kwargs:
        A dictionary of keyword arguments to pass to the download method. Refer
        to the documentation for blob.download_to_file() or
        blob.download_to_filename() for more information. The dict is directly
        passed into the download methods and is not validated by this function.

    :type threads: int
    :param threads:
        The number of threads to use in the worker pool. This is passed to
        `concurrent.futures.ThreadPoolExecutor` as the `max_worker`; refer
        to standard library documentation for details.

        The performance impact of this value depends on the use case, but
        generally, smaller files benefit from more threads and larger files
        don't benefit from more threads. Too many threads can slow operations,
        especially with large files, due to contention over the Python GIL.

    :type deadline: int
    :param deadline:
        The number of seconds to wait for all threads to resolve. If the
        deadline is reached, all threads will be terminated regardless of their
        progress and concurrent.futures.TimeoutError will be raised. This can be
        left as the default of None (no deadline) for most use cases.

    :type raise_exception: bool
    :param raise_exception:
        If True, instead of adding exceptions to the list of return values,
        instead they will be raised. Note that encountering an exception on one
        operation will not prevent other operations from starting. Exceptions
        are only processed and potentially raised after all operations are
        complete in success or failure.

    :raises: :exc:`concurrent.futures.TimeoutError` if deadline is exceeded.

    :rtype: list
    :returns: A list of results corresponding to, in order, each item in the
        input list. If an exception was received, it will be the result
        for that operation. Otherwise, the return value from the successful
        download method is used (typically, None).
    """

    if download_kwargs is None:
        download_kwargs = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for blob, path_or_file in blob_file_pairs:
            method = (
                blob.download_to_filename
                if isinstance(path_or_file, str)
                else blob.download_to_file
            )
            futures.append(executor.submit(method, path_or_file, **download_kwargs))
    results = []
    concurrent.futures.wait(
        futures, timeout=deadline, return_when=concurrent.futures.ALL_COMPLETED
    )
    for future in futures:
        if not raise_exception:
            exp = future.exception()
            if exp:
                results.append(exp)
                continue
        results.append(future.result())
    return results


def upload_many_from_filenames(
    bucket,
    filenames,
    source_directory="",
    blob_name_prefix="",
    skip_if_exists=False,
    blob_constructor_kwargs=None,
    upload_kwargs=None,
    threads=4,
    deadline=None,
    raise_exception=False,
):
    """Upload many files concurrently by their filenames.

    This function is a PREVIEW FEATURE: the API may change in a future version.

    The destination blobs are automatically created, with blob names based on
    the source filenames and the blob_name_prefix.

    For example, if the `filenames` include "images/icon.jpg",
    `source_directory` is "/home/myuser/", and `blob_name_prefix` is "myfiles/",
    then the file at "/home/myuser/images/icon.jpg" will be uploaded to a blob
    named "myfiles/images/icon.jpg".

    :type bucket: 'google.cloud.storage.bucket.Bucket'
    :param bucket:
        The bucket which will contain the uploaded blobs.

    :type filenames: list(str)
    :param filenames:
        A list of filenames to be uploaded. This may include part of the path.
        The full path to the file must be source_directory + filename.

    :type source_directory: str
    :param source_directory:
        A string that will be prepended (with os.path.join()) to each filename
        in the input list, in order to find the source file for each blob.
        Unlike the filename itself, the source_directory does not affect the
        name of the uploaded blob.

        For instance, if the source_directory is "/tmp/img/" and a filename is
        "0001.jpg", with an empty blob_name_prefix, then the file uploaded will
        be "/tmp/img/0001.jpg" and the destination blob will be "0001.jpg".

        This parameter can be an empty string.

        Note that this parameter allows directory traversal (e.g. "/", "../")
        and is not intended for unsanitized end user input.

    :type blob_name_prefix: str
    :param blob_name_prefix:
        A string that will be prepended to each filename in the input list, in
        order to determine the name of the destination blob. Unlike the filename
        itself, the prefix string does not affect the location the library will
        look for the source data on the local filesystem.

        For instance, if the source_directory is "/tmp/img/", the
        blob_name_prefix is "myuser/mystuff-" and a filename is "0001.jpg" then
        the file uploaded will be "/tmp/img/0001.jpg" and the destination blob
        will be "myuser/mystuff-0001.jpg".

        The blob_name_prefix can be blank (an empty string).

    :type skip_if_exists: bool
    :param skip_if_exists:
        If True, blobs that already have a live version will not be overwritten.
        This is accomplished by setting "if_generation_match = 0" on uploads.
        Uploads so skipped will result in a 412 Precondition Failed response
        code, which will be included in the return value, but not raised
        as an exception regardless of the value of raise_exception.

    :type blob_constructor_kwargs: dict
    :param blob_constructor_kwargs:
        A dictionary of keyword arguments to pass to the blob constructor. Refer
        to the documentation for blob.Blob() for more information. The dict is
        directly passed into the constructor and is not validated by this
        function. `name` and `bucket` keyword arguments are reserved by this
        function and will result in an error if passed in here.

    :type upload_kwargs: dict
    :param upload_kwargs:
        A dictionary of keyword arguments to pass to the upload method. Refer
        to the documentation for blob.upload_from_file() or
        blob.upload_from_filename() for more information. The dict is directly
        passed into the upload methods and is not validated by this function.

    :type threads: int
    :param threads:
        The number of threads to use in the worker pool. This is passed to
        `concurrent.futures.ThreadPoolExecutor` as the `max_worker`; refer
        to standard library documentation for details.

        The performance impact of this value depends on the use case, but
        generally, smaller files benefit from more threads and larger files
        don't benefit from more threads. Too many threads can slow operations,
        especially with large files, due to contention over the Python GIL.

    :type deadline: int
    :param deadline:
        The number of seconds to wait for all threads to resolve. If the
        deadline is reached, all threads will be terminated regardless of their
        progress and concurrent.futures.TimeoutError will be raised. This can be
        left as the default of None (no deadline) for most use cases.

    :type raise_exception: bool
    :param raise_exception:
        If True, instead of adding exceptions to the list of return values,
        instead they will be raised. Note that encountering an exception on one
        operation will not prevent other operations from starting. Exceptions
        are only processed and potentially raised after all operations are
        complete in success or failure.

        If skip_if_exists is True, 412 Precondition Failed responses are
        considered part of normal operation and are not raised as an exception.

    :raises: :exc:`concurrent.futures.TimeoutError` if deadline is exceeded.

    :rtype: list
    :returns: A list of results corresponding to, in order, each item in the
        input list. If an exception was received, it will be the result
        for that operation. Otherwise, the return value from the successful
        upload method is used (typically, None).
    """
    if blob_constructor_kwargs is None:
        blob_constructor_kwargs = {}

    file_blob_pairs = []

    for filename in filenames:
        path = os.path.join(source_directory, filename)
        blob_name = blob_name_prefix + filename
        blob = bucket.blob(blob_name, **blob_constructor_kwargs)
        file_blob_pairs.append((path, blob))

    return upload_many(
        file_blob_pairs,
        skip_if_exists=skip_if_exists,
        upload_kwargs=upload_kwargs,
        threads=threads,
        deadline=deadline,
        raise_exception=raise_exception,
    )


def download_many_to_path(
    bucket,
    blob_names,
    destination_directory="",
    blob_name_prefix="",
    download_kwargs=None,
    threads=4,
    deadline=None,
    create_directories=True,
    raise_exception=False,
):
    """Download many files concurrently by their blob names.

    This function is a PREVIEW FEATURE: the API may change in a future version.

    The destination files are automatically created, with paths based on the
    source blob_names and the destination_directory.

    The destination files are not automatically deleted if their downloads fail,
    so please check the return value of this function for any exceptions, or
    enable `raise_exception=True`, and process the files accordingly.

    For example, if the `blob_names` include "icon.jpg", `destination_directory`
    is "/home/myuser/", and `blob_name_prefix` is "images/", then the blob named
    "images/icon.jpg" will be downloaded to a file named
    "/home/myuser/icon.jpg".

    :type bucket: 'google.cloud.storage.bucket.Bucket'
    :param bucket:
        The bucket which contains the blobs to be downloaded

    :type blob_names: list(str)
    :param blob_names:
        A list of blobs to be downloaded. The blob name in this string will be
        used to determine the destination file path as well.

        The full name to the blob must be blob_name_prefix + blob_name. The
        blob_name is separate from the blob_name_prefix because the blob_name
        will also determine the name of the destination blob. Any shared part of
        the blob names that need not be part of the destination path should be
        included in the blob_name_prefix.

    :type destination_directory: str
    :param destination_directory:
        A string that will be prepended (with os.path.join()) to each blob_name
        in the input list, in order to determine the destination path for that
        blob.

        For instance, if the destination_directory string is "/tmp/img" and a
        blob_name is "0001.jpg", with an empty blob_name_prefix, then the source
        blob "0001.jpg" will be downloaded to destination "/tmp/img/0001.jpg" .

        This parameter can be an empty string.

        Note that this parameter allows directory traversal (e.g. "/", "../")
        and is not intended for unsanitized end user input.

    :type blob_name_prefix: str
    :param blob_name_prefix:
        A string that will be prepended to each blob_name in the input list, in
        order to determine the name of the source blob. Unlike the blob_name
        itself, the prefix string does not affect the destination path on the
        local filesystem. For instance, if the destination_directory is
        "/tmp/img/", the blob_name_prefix is "myuser/mystuff-" and a blob_name
        is "0001.jpg" then the source blob "myuser/mystuff-0001.jpg" will be
        downloaded to "/tmp/img/0001.jpg". The blob_name_prefix can be blank
        (an empty string).

    :type download_kwargs: dict
    :param download_kwargs:
        A dictionary of keyword arguments to pass to the download method. Refer
        to the documentation for blob.download_to_file() or
        blob.download_to_filename() for more information. The dict is directly
        passed into the download methods and is not validated by this function.

    :type threads: int
    :param threads:
        The number of threads to use in the worker pool. This is passed to
        `concurrent.futures.ThreadPoolExecutor` as the `max_worker` param; refer
        to standard library documentation for details.

        The performance impact of this value depends on the use case, but
        generally, smaller files benefit from more threads and larger files
        don't benefit from more threads. Too many threads can slow operations,
        especially with large files, due to contention over the Python GIL.

    :type deadline: int
    :param deadline:
        The number of seconds to wait for all threads to resolve. If the
        deadline is reached, all threads will be terminated regardless of their
        progress and concurrent.futures.TimeoutError will be raised. This can be
        left as the default of None (no deadline) for most use cases.

    :type create_directories: bool
    :param create_directories:
        If True, recursively create any directories that do not exist. For
        instance, if downloading object "images/img001.png", create the
        directory "images" before downloading.

    :type raise_exception: bool
    :param raise_exception:
        If True, instead of adding exceptions to the list of return values,
        instead they will be raised. Note that encountering an exception on one
        operation will not prevent other operations from starting. Exceptions
        are only processed and potentially raised after all operations are
        complete in success or failure. If skip_if_exists is True, 412
        Precondition Failed responses are considered part of normal operation
        and are not raised as an exception.

    :raises: :exc:`concurrent.futures.TimeoutError` if deadline is exceeded.

    :rtype: list
    :returns: A list of results corresponding to, in order, each item in the
        input list. If an exception was received, it will be the result
        for that operation. Otherwise, the return value from the successful
        download method is used (typically, None).
    """
    blob_file_pairs = []

    for blob_name in blob_names:
        full_blob_name = blob_name_prefix + blob_name
        path = os.path.join(destination_directory, blob_name)
        if create_directories:
            directory, _ = os.path.split(path)
            os.makedirs(directory, exist_ok=True)
        blob_file_pairs.append((bucket.blob(full_blob_name), path))

    return download_many(
        blob_file_pairs,
        download_kwargs=download_kwargs,
        threads=threads,
        deadline=deadline,
        raise_exception=raise_exception,
    )
