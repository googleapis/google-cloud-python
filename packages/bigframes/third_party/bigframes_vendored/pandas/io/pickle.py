# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/io/pickle.py
""" pickle compat """
from __future__ import annotations

from pandas._typing import (
    CompressionOptions,
    FilePath,
    ReadPickleBuffer,
    StorageOptions,
)

from bigframes import constants


class PickleIOMixin:
    def read_pickle(
        self,
        filepath_or_buffer: FilePath | ReadPickleBuffer,
        compression: CompressionOptions = "infer",
        storage_options: StorageOptions = None,
    ):
        """Load pickled BigFrames object (or any object) from file.

        .. note::
            If the content of the pickle file is a Series and its name attribute is None,
            the name will be set to '0' by default.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> gcs_path = "gs://bigframes-dev-testing/test_pickle.pkl"
            >>> df = bpd.read_pickle(filepath_or_buffer=gcs_path)

        Args:
            filepath_or_buffer (str, path object, or file-like object):
                String, path object (implementing os.PathLike[str]), or file-like object
                implementing a binary readlines() function. Also accepts URL. URL is not
                limited to S3 and GCS.
            compression (str or dict, default 'infer'):
                For on-the-fly decompression of on-disk data. If 'infer' and
                'filepath_or_buffer' is path-like, then detect compression from the following
                extensions: '.gz', '.bz2', '.zip', '.xz', '.zst', '.tar', '.tar.gz', '.tar.xz'
                or '.tar.bz2' (otherwise no compression). If using 'zip' or 'tar', the ZIP
                file must contain only one data file to be read in. Set to None for no
                decompression. Can also be a dict with key 'method' set to one of {'zip',
                'gzip', 'bz2', 'zstd', 'tar'} and other key-value pairs are forwarded to
                zipfile.ZipFile, gzip.GzipFile, bz2.BZ2File, zstandard.ZstdDecompressor or
                tarfile.TarFile, respectively. As an example, the following could be passed
                for Zstandard decompression using a custom compression dictionary
                compression={'method': 'zstd', 'dict_data': my_compression_dict}.
            storage_options (dict, default None):
                Extra options that make sense for a particular storage connection, e.g. host,
                port, username, password, etc. For HTTP(S) URLs the key-value pairs are
                forwarded to urllib.request.Request as header options. For other URLs (e.g.
                starting with “s3://”, and “gcs://”) the key-value pairs are forwarded to
                fsspec.open. Please see fsspec and urllib for more details, and for more
                examples on storage options refer here.

        Returns:
            bigframes.dataframe.DataFrame or bigframes.series.Series: same type as object
                stored in file.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
