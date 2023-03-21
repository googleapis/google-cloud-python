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

import io
import inspect
import os
import warnings
import pickle
import copyreg

from google.api_core import exceptions
from google.cloud.storage import Client
from google.cloud.storage import Blob

warnings.warn(
    "The module `transfer_manager` is a preview feature. Functionality and API "
    "may change. This warning will be removed in a future release."
)


TM_DEFAULT_CHUNK_SIZE = 32 * 1024 * 1024
DEFAULT_MAX_WORKERS = 8


# Constants to be passed in as `worker_type`.
PROCESS = "process"
THREAD = "thread"


_cached_clients = {}


def _deprecate_threads_param(func):
    def convert_threads_or_raise(*args, **kwargs):
        binding = inspect.signature(func).bind(*args, **kwargs)
        threads = binding.arguments.get("threads")
        if threads:
            worker_type = binding.arguments.get("worker_type")
            max_workers = binding.arguments.get("max_workers")
            if worker_type or max_workers:  # Parameter conflict
                raise ValueError(
                    "The `threads` parameter is deprecated and conflicts with its replacement parameters, `worker_type` and `max_workers`."
                )
            # No conflict, so issue a warning and set worker_type and max_workers.
            warnings.warn(
                "The `threads` parameter is deprecated. Please use `worker_type` and `max_workers` parameters instead."
            )
            args = binding.args
            kwargs = binding.kwargs
            kwargs["worker_type"] = THREAD
            kwargs["max_workers"] = threads
            return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return convert_threads_or_raise


@_deprecate_threads_param
def upload_many(
    file_blob_pairs,
    skip_if_exists=False,
    upload_kwargs=None,
    threads=None,
    deadline=None,
    raise_exception=False,
    worker_type=PROCESS,
    max_workers=DEFAULT_MAX_WORKERS,
):
    """Upload many files concurrently via a worker pool.

    This function is a PREVIEW FEATURE: the API may change in a future version.

    :type file_blob_pairs: List(Tuple(IOBase or str, 'google.cloud.storage.blob.Blob'))
    :param file_blob_pairs:
        A list of tuples of a file or filename and a blob. Each file will be
        uploaded to the corresponding blob by using blob.upload_from_file() or
        blob.upload_from_filename() as appropriate.

        File handlers are only supported if worker_type is set to THREAD.
        If worker_type is set to PROCESS, please use filenames only.

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
        ***DEPRECATED*** Sets `worker_type` to THREAD and `max_workers` to the
        number specified. If `worker_type` or `max_workers` are set explicitly,
        this parameter should be set to None. Please use `worker_type` and
        `max_workers` instead of this parameter.

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

    :type worker_type: str
    :param worker_type:
        The worker type to use; one of google.cloud.storage.transfer_manager.PROCESS
        or google.cloud.storage.transfer_manager.THREAD.

        Although the exact performance impact depends on the use case, in most
        situations the PROCESS worker type will use more system resources (both
        memory and CPU) and result in faster operations than THREAD workers.

        Because the subprocesses of the PROCESS worker type can't access memory
        from the main process, Client objects have to be serialized and then
        recreated in each subprocess. The serialization of the Client object
        for use in subprocesses is an approximation and may not capture every
        detail of the Client object, especially if the Client was modified after
        its initial creation or if `Client._http` was modified in any way.

        THREAD worker types are observed to be relatively efficient for
        operations with many small files, but not for operations with large
        files. PROCESS workers are recommended for large file operations.

        PROCESS workers do not support writing to file handlers. Please refer
        to files by filename only when using PROCESS workers.

    :type max_workers: int
    :param max_workers:
        The maximum number of workers to create to handle the workload.

        With PROCESS workers, a larger number of workers will consume more
        system resources (memory and CPU) at once.

        How many workers is optimal depends heavily on the specific use case,
        and the default is a conservative number that should work okay in most
        cases without consuming excessive resources.

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
        upload_kwargs = upload_kwargs.copy()
        upload_kwargs["if_generation_match"] = 0

    pool_class, needs_pickling = _get_pool_class_and_requirements(worker_type)

    with pool_class(max_workers=max_workers) as executor:
        futures = []
        for path_or_file, blob in file_blob_pairs:
            # File objects are only supported by the THREAD worker because they can't
            # be pickled.
            if needs_pickling and not isinstance(path_or_file, str):
                raise ValueError(
                    "Passing in a file object is only supported by the THREAD worker type. Please either select THREAD workers, or pass in filenames only."
                )

            futures.append(
                executor.submit(
                    _call_method_on_maybe_pickled_blob,
                    _pickle_blob(blob) if needs_pickling else blob,
                    "upload_from_filename"
                    if isinstance(path_or_file, str)
                    else "upload_from_file",
                    path_or_file,
                    **upload_kwargs,
                )
            )
        concurrent.futures.wait(
            futures, timeout=deadline, return_when=concurrent.futures.ALL_COMPLETED
        )

    results = []
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


@_deprecate_threads_param
def download_many(
    blob_file_pairs,
    download_kwargs=None,
    threads=None,
    deadline=None,
    raise_exception=False,
    worker_type=PROCESS,
    max_workers=DEFAULT_MAX_WORKERS,
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

        File handlers are only supported if worker_type is set to THREAD.
        If worker_type is set to PROCESS, please use filenames only.

    :type download_kwargs: dict
    :param download_kwargs:
        A dictionary of keyword arguments to pass to the download method. Refer
        to the documentation for blob.download_to_file() or
        blob.download_to_filename() for more information. The dict is directly
        passed into the download methods and is not validated by this function.

    :type threads: int
    :param threads:
        ***DEPRECATED*** Sets `worker_type` to THREAD and `max_workers` to the
        number specified. If `worker_type` or `max_workers` are set explicitly,
        this parameter should be set to None. Please use `worker_type` and
        `max_workers` instead of this parameter.

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

    :type worker_type: str
    :param worker_type:
        The worker type to use; one of google.cloud.storage.transfer_manager.PROCESS
        or google.cloud.storage.transfer_manager.THREAD.

        Although the exact performance impact depends on the use case, in most
        situations the PROCESS worker type will use more system resources (both
        memory and CPU) and result in faster operations than THREAD workers.

        Because the subprocesses of the PROCESS worker type can't access memory
        from the main process, Client objects have to be serialized and then
        recreated in each subprocess. The serialization of the Client object
        for use in subprocesses is an approximation and may not capture every
        detail of the Client object, especially if the Client was modified after
        its initial creation or if `Client._http` was modified in any way.

        THREAD worker types are observed to be relatively efficient for
        operations with many small files, but not for operations with large
        files. PROCESS workers are recommended for large file operations.

        PROCESS workers do not support writing to file handlers. Please refer
        to files by filename only when using PROCESS workers.

    :type max_workers: int
    :param max_workers:
        The maximum number of workers to create to handle the workload.

        With PROCESS workers, a larger number of workers will consume more
        system resources (memory and CPU) at once.

        How many workers is optimal depends heavily on the specific use case,
        and the default is a conservative number that should work okay in most
        cases without consuming excessive resources.

    :raises: :exc:`concurrent.futures.TimeoutError` if deadline is exceeded.

    :rtype: list
    :returns: A list of results corresponding to, in order, each item in the
        input list. If an exception was received, it will be the result
        for that operation. Otherwise, the return value from the successful
        download method is used (typically, None).
    """

    if download_kwargs is None:
        download_kwargs = {}

    pool_class, needs_pickling = _get_pool_class_and_requirements(worker_type)

    with pool_class(max_workers=max_workers) as executor:
        futures = []
        for blob, path_or_file in blob_file_pairs:
            # File objects are only supported by the THREAD worker because they can't
            # be pickled.
            if needs_pickling and not isinstance(path_or_file, str):
                raise ValueError(
                    "Passing in a file object is only supported by the THREAD worker type. Please either select THREAD workers, or pass in filenames only."
                )

            futures.append(
                executor.submit(
                    _call_method_on_maybe_pickled_blob,
                    _pickle_blob(blob) if needs_pickling else blob,
                    "download_to_filename"
                    if isinstance(path_or_file, str)
                    else "download_to_file",
                    path_or_file,
                    **download_kwargs,
                )
            )
        concurrent.futures.wait(
            futures, timeout=deadline, return_when=concurrent.futures.ALL_COMPLETED
        )

    results = []
    for future in futures:
        # If raise_exception is False, don't call future.result()
        if not raise_exception:
            exp = future.exception()
            if exp:
                results.append(exp)
                continue
        # Get the real result. If there was an exception, this will raise it.
        results.append(future.result())
    return results


@_deprecate_threads_param
def upload_many_from_filenames(
    bucket,
    filenames,
    source_directory="",
    blob_name_prefix="",
    skip_if_exists=False,
    blob_constructor_kwargs=None,
    upload_kwargs=None,
    threads=None,
    deadline=None,
    raise_exception=False,
    worker_type=PROCESS,
    max_workers=DEFAULT_MAX_WORKERS,
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
        ***DEPRECATED*** Sets `worker_type` to THREAD and `max_workers` to the
        number specified. If `worker_type` or `max_workers` are set explicitly,
        this parameter should be set to None. Please use `worker_type` and
        `max_workers` instead of this parameter.

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

    :type worker_type: str
    :param worker_type:
        The worker type to use; one of google.cloud.storage.transfer_manager.PROCESS
        or google.cloud.storage.transfer_manager.THREAD.

        Although the exact performance impact depends on the use case, in most
        situations the PROCESS worker type will use more system resources (both
        memory and CPU) and result in faster operations than THREAD workers.

        Because the subprocesses of the PROCESS worker type can't access memory
        from the main process, Client objects have to be serialized and then
        recreated in each subprocess. The serialization of the Client object
        for use in subprocesses is an approximation and may not capture every
        detail of the Client object, especially if the Client was modified after
        its initial creation or if `Client._http` was modified in any way.

        THREAD worker types are observed to be relatively efficient for
        operations with many small files, but not for operations with large
        files. PROCESS workers are recommended for large file operations.

    :type max_workers: int
    :param max_workers:
        The maximum number of workers to create to handle the workload.

        With PROCESS workers, a larger number of workers will consume more
        system resources (memory and CPU) at once.

        How many workers is optimal depends heavily on the specific use case,
        and the default is a conservative number that should work okay in most
        cases without consuming excessive resources.

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
        deadline=deadline,
        raise_exception=raise_exception,
        worker_type=worker_type,
        max_workers=max_workers,
    )


@_deprecate_threads_param
def download_many_to_path(
    bucket,
    blob_names,
    destination_directory="",
    blob_name_prefix="",
    download_kwargs=None,
    threads=None,
    deadline=None,
    create_directories=True,
    raise_exception=False,
    worker_type=PROCESS,
    max_workers=DEFAULT_MAX_WORKERS,
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
        ***DEPRECATED*** Sets `worker_type` to THREAD and `max_workers` to the
        number specified. If `worker_type` or `max_workers` are set explicitly,
        this parameter should be set to None. Please use `worker_type` and
        `max_workers` instead of this parameter.

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

    :type worker_type: str
    :param worker_type:
        The worker type to use; one of google.cloud.storage.transfer_manager.PROCESS
        or google.cloud.storage.transfer_manager.THREAD.

        Although the exact performance impact depends on the use case, in most
        situations the PROCESS worker type will use more system resources (both
        memory and CPU) and result in faster operations than THREAD workers.

        Because the subprocesses of the PROCESS worker type can't access memory
        from the main process, Client objects have to be serialized and then
        recreated in each subprocess. The serialization of the Client object
        for use in subprocesses is an approximation and may not capture every
        detail of the Client object, especially if the Client was modified after
        its initial creation or if `Client._http` was modified in any way.

        THREAD worker types are observed to be relatively efficient for
        operations with many small files, but not for operations with large
        files. PROCESS workers are recommended for large file operations.

    :type max_workers: int
    :param max_workers:
        The maximum number of workers to create to handle the workload.

        With PROCESS workers, a larger number of workers will consume more
        system resources (memory and CPU) at once.

        How many workers is optimal depends heavily on the specific use case,
        and the default is a conservative number that should work okay in most
        cases without consuming excessive resources.

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
        deadline=deadline,
        raise_exception=raise_exception,
        worker_type=worker_type,
        max_workers=max_workers,
    )


def download_chunks_concurrently(
    blob,
    filename,
    chunk_size=TM_DEFAULT_CHUNK_SIZE,
    download_kwargs=None,
    deadline=None,
    worker_type=PROCESS,
    max_workers=DEFAULT_MAX_WORKERS,
):
    """Download a single file in chunks, concurrently.

    This function is a PREVIEW FEATURE: the API may change in a future version.

    In some environments, using this feature with mutiple processes will result
    in faster downloads of large files.

    Using this feature with multiple threads is unlikely to improve download
    performance under normal circumstances due to Python interpreter threading
    behavior. The default is therefore to use processes instead of threads.

    Checksumming (md5 or crc32c) is not supported for chunked operations. Any
    `checksum` parameter passed in to download_kwargs will be ignored.

    :type bucket: 'google.cloud.storage.bucket.Bucket'
    :param bucket:
        The bucket which contains the blobs to be downloaded

    :type blob: `google.cloud.storage.Blob`
    :param blob:
        The blob to be downloaded.

    :type filename: str
    :param filename:
        The destination filename or path.

    :type download_kwargs: dict
    :param download_kwargs:
        A dictionary of keyword arguments to pass to the download method. Refer
        to the documentation for blob.download_to_file() or
        blob.download_to_filename() for more information. The dict is directly
        passed into the download methods and is not validated by this function.

        Keyword arguments "start" and "end" which are not supported and will
        cause a ValueError if present.

    :type deadline: int
    :param deadline:
        The number of seconds to wait for all threads to resolve. If the
        deadline is reached, all threads will be terminated regardless of their
        progress and concurrent.futures.TimeoutError will be raised. This can be
        left as the default of None (no deadline) for most use cases.

    :type worker_type: str
    :param worker_type:
        The worker type to use; one of google.cloud.storage.transfer_manager.PROCESS
        or google.cloud.storage.transfer_manager.THREAD.

        Although the exact performance impact depends on the use case, in most
        situations the PROCESS worker type will use more system resources (both
        memory and CPU) and result in faster operations than THREAD workers.

        Because the subprocesses of the PROCESS worker type can't access memory
        from the main process, Client objects have to be serialized and then
        recreated in each subprocess. The serialization of the Client object
        for use in subprocesses is an approximation and may not capture every
        detail of the Client object, especially if the Client was modified after
        its initial creation or if `Client._http` was modified in any way.

        THREAD worker types are observed to be relatively efficient for
        operations with many small files, but not for operations with large
        files. PROCESS workers are recommended for large file operations.

    :type max_workers: int
    :param max_workers:
        The maximum number of workers to create to handle the workload.

        With PROCESS workers, a larger number of workers will consume more
        system resources (memory and CPU) at once.

        How many workers is optimal depends heavily on the specific use case,
        and the default is a conservative number that should work okay in most
        cases without consuming excessive resources.

    :raises: :exc:`concurrent.futures.TimeoutError` if deadline is exceeded.
    """

    if download_kwargs is None:
        download_kwargs = {}
    if "start" in download_kwargs or "end" in download_kwargs:
        raise ValueError(
            "Download arguments 'start' and 'end' are not supported by download_chunks_concurrently."
        )

    # We must know the size and the generation of the blob.
    if not blob.size or not blob.generation:
        blob.reload()

    pool_class, needs_pickling = _get_pool_class_and_requirements(worker_type)
    # Pickle the blob ahead of time (just once, not once per chunk) if needed.
    maybe_pickled_blob = _pickle_blob(blob) if needs_pickling else blob

    futures = []

    # Create and/or truncate the destination file to prepare for sparse writing.
    with open(filename, "wb") as _:
        pass

    with pool_class(max_workers=max_workers) as executor:
        cursor = 0
        end = blob.size
        while cursor < end:
            start = cursor
            cursor = min(cursor + chunk_size, end)
            futures.append(
                executor.submit(
                    _download_and_write_chunk_in_place,
                    maybe_pickled_blob,
                    filename,
                    start=start,
                    end=cursor - 1,
                    download_kwargs=download_kwargs,
                )
            )

        concurrent.futures.wait(
            futures, timeout=deadline, return_when=concurrent.futures.ALL_COMPLETED
        )

    # Raise any exceptions. Successful results can be ignored.
    for future in futures:
        future.result()
    return None


def _download_and_write_chunk_in_place(
    maybe_pickled_blob, filename, start, end, download_kwargs
):
    if isinstance(maybe_pickled_blob, Blob):
        blob = maybe_pickled_blob
    else:
        blob = pickle.loads(maybe_pickled_blob)
    with open(
        filename, "rb+"
    ) as f:  # Open in mixed read/write mode to avoid truncating or appending
        f.seek(start)
        return blob.download_to_file(f, start=start, end=end, **download_kwargs)


def _call_method_on_maybe_pickled_blob(
    maybe_pickled_blob, method_name, *args, **kwargs
):
    """Helper function that runs inside a thread or subprocess.

    `maybe_pickled_blob` is either a blob (for threads) or a specially pickled
    blob (for processes) because the default pickling mangles clients which are
    attached to blobs."""

    if isinstance(maybe_pickled_blob, Blob):
        blob = maybe_pickled_blob
    else:
        blob = pickle.loads(maybe_pickled_blob)
    return getattr(blob, method_name)(*args, **kwargs)


def _reduce_client(cl):
    """Replicate a Client by constructing a new one with the same params."""

    client_object_id = id(cl)
    project = cl.project
    credentials = cl._credentials
    _http = None  # Can't carry this over
    client_info = cl._initial_client_info
    client_options = cl._initial_client_options

    return _LazyClient, (
        client_object_id,
        project,
        credentials,
        _http,
        client_info,
        client_options,
    )


def _pickle_blob(blob):
    """Pickle a Blob (and its Bucket and Client) and return a bytestring."""

    # We need a custom pickler to process Client objects, which are attached to
    # Buckets (and therefore to Blobs in turn). Unfortunately, the Python
    # multiprocessing library doesn't seem to have a good way to use a custom
    # pickler, and using copyreg will mutate global state and affect code
    # outside of the client library. Instead, we'll pre-pickle the object and
    # pass the bytestring in.
    f = io.BytesIO()
    p = pickle.Pickler(f)
    p.dispatch_table = copyreg.dispatch_table.copy()
    p.dispatch_table[Client] = _reduce_client
    p.dump(blob)
    return f.getvalue()


def _get_pool_class_and_requirements(worker_type):
    """Returns the pool class, and whether the pool requires pickled Blobs."""

    if worker_type == PROCESS:
        # Use processes. Pickle blobs with custom logic to handle the client.
        return (concurrent.futures.ProcessPoolExecutor, True)
    elif worker_type == THREAD:
        # Use threads. Pass blobs through unpickled.
        return (concurrent.futures.ThreadPoolExecutor, False)
    else:
        raise ValueError(
            "The worker_type must be google.cloud.storage.transfer_manager.PROCESS or google.cloud.storage.transfer_manager.THREAD"
        )


class _LazyClient:
    """An object that will transform into either a cached or a new Client"""

    def __new__(cls, id, *args, **kwargs):
        cached_client = _cached_clients.get(id)
        if cached_client:
            return cached_client
        else:
            cached_client = Client(*args, **kwargs)
            _cached_clients[id] = cached_client
            return cached_client
