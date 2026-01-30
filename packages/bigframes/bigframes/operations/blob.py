# Copyright 2024 Google LLC
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

from __future__ import annotations

import os
from typing import cast, Literal, Optional, Union
import warnings

import pandas as pd
import requests

from bigframes import clients, dtypes
from bigframes.core.logging import log_adapter
import bigframes.dataframe
import bigframes.exceptions as bfe
import bigframes.operations as ops
import bigframes.series

FILE_FOLDER_REGEX = r"^.*\/(.*)$"
FILE_EXT_REGEX = r"(\.[0-9a-zA-Z]+$)"


@log_adapter.class_logger
class BlobAccessor:
    """
    Blob functions for Series and Index.

    .. note::
        BigFrames Blob is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
        Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
        and might have limited support. For more information, see the launch stage descriptions
        (https://cloud.google.com/products#product-launch-stages).
    """

    def __init__(self, data: bigframes.series.Series):
        self._data = data

    def uri(self) -> bigframes.series.Series:
        """URIs of the Blob.

        Returns:
            bigframes.series.Series: URIs as string."""
        s = bigframes.series.Series(self._data._block)

        return s.struct.field("uri")

    def authorizer(self) -> bigframes.series.Series:
        """Authorizers of the Blob.

        Returns:
            bigframes.series.Series: Autorithers(connection) as string."""
        s = bigframes.series.Series(self._data._block)

        return s.struct.field("authorizer")

    def version(self) -> bigframes.series.Series:
        """Versions of the Blob.

        Returns:
            bigframes.series.Series: Version as string."""
        # version must be retrieved after fetching metadata
        return self._data._apply_unary_op(ops.obj_fetch_metadata_op).struct.field(
            "version"
        )

    def metadata(self) -> bigframes.series.Series:
        """Retrieve the metadata of the Blob.

        Returns:
            bigframes.series.Series: JSON metadata of the Blob. Contains fields: content_type, md5_hash, size and updated(time)."""
        series_to_check = bigframes.series.Series(self._data._block)
        # Check if it's a struct series from a verbose operation
        if dtypes.is_struct_like(series_to_check.dtype):
            pyarrow_dtype = series_to_check.dtype.pyarrow_dtype
            if "content" in [field.name for field in pyarrow_dtype]:
                content_field_type = pyarrow_dtype.field("content").type
                content_bf_type = dtypes.arrow_dtype_to_bigframes_dtype(
                    content_field_type
                )
                if content_bf_type == dtypes.OBJ_REF_DTYPE:
                    series_to_check = series_to_check.struct.field("content")
        details_json = series_to_check._apply_unary_op(
            ops.obj_fetch_metadata_op
        ).struct.field("details")
        import bigframes.bigquery as bbq

        return bbq.json_extract(details_json, "$.gcs_metadata").rename("metadata")

    def content_type(self) -> bigframes.series.Series:
        """Retrieve the content type of the Blob.

        Returns:
            bigframes.series.Series: string of the content type."""
        return (
            self.metadata()
            ._apply_unary_op(ops.JSONValue(json_path="$.content_type"))
            .rename("content_type")
        )

    def md5_hash(self) -> bigframes.series.Series:
        """Retrieve the md5 hash of the Blob.

        Returns:
            bigframes.series.Series: string of the md5 hash."""
        return (
            self.metadata()
            ._apply_unary_op(ops.JSONValue(json_path="$.md5_hash"))
            .rename("md5_hash")
        )

    def size(self) -> bigframes.series.Series:
        """Retrieve the file size of the Blob.

        Returns:
            bigframes.series.Series: file size in bytes."""
        return (
            self.metadata()
            ._apply_unary_op(ops.JSONValue(json_path="$.size"))
            .rename("size")
            .astype("Int64")
        )

    def updated(self) -> bigframes.series.Series:
        """Retrieve the updated time of the Blob.

        Returns:
            bigframes.series.Series: updated time as UTC datetime."""
        import bigframes.pandas as bpd

        updated = (
            self.metadata()
            ._apply_unary_op(ops.JSONValue(json_path="$.updated"))
            .rename("updated")
            .astype("Int64")
        )

        return bpd.to_datetime(updated, unit="us", utc=True)

    def _get_runtime(
        self, mode: str, with_metadata: bool = False
    ) -> bigframes.series.Series:
        """Retrieve the ObjectRefRuntime as JSON.

        Args:
            mode (str): mode for the URLs, "R" for read, "RW" for read & write.
            metadata (bool, default False): whether to fetch the metadata in the ObjectRefRuntime.

        Returns:
            bigframes.series.Series: ObjectRefRuntime JSON.
        """
        s = (
            self._data._apply_unary_op(ops.obj_fetch_metadata_op)
            if with_metadata
            else self._data
        )

        return s._apply_unary_op(ops.ObjGetAccessUrl(mode=mode))

    def _df_apply_udf(
        self, df: bigframes.dataframe.DataFrame, udf
    ) -> bigframes.series.Series:
        # Catch and rethrow function axis=1 warning to be more user-friendly.
        with warnings.catch_warnings(record=True) as catched_warnings:
            s = df.apply(udf, axis=1)
        for w in catched_warnings:
            if isinstance(w.message, bfe.FunctionAxisOnePreviewWarning):
                warnings.warn(
                    "Blob Functions use bigframes DataFrame Managed function with axis=1 senario, which is a preview feature.",
                    category=w.category,
                    stacklevel=2,
                )
            else:
                warnings.warn_explicit(
                    message=w.message,
                    category=w.category,
                    filename=w.filename,
                    lineno=w.lineno,
                    source=w.source,
                )

        return s

    def _apply_udf_or_raise_error(
        self, df: bigframes.dataframe.DataFrame, udf, operation_name: str
    ) -> bigframes.series.Series:
        """Helper to apply UDF with consistent error handling."""
        try:
            res = self._df_apply_udf(df, udf)
        except Exception as e:
            raise RuntimeError(f"{operation_name} UDF execution failed: {e}") from e

        if res is None:
            raise RuntimeError(f"{operation_name} returned None result")

        return res

    def read_url(self) -> bigframes.series.Series:
        """Retrieve the read URL of the Blob.

        Returns:
            bigframes.series.Series: Read only URLs."""
        return self._get_runtime(mode="R")._apply_unary_op(
            ops.JSONValue(json_path="$.access_urls.read_url")
        )

    def write_url(self) -> bigframes.series.Series:
        """Retrieve the write URL of the Blob.

        Returns:
            bigframes.series.Series: Writable URLs."""
        return self._get_runtime(mode="RW")._apply_unary_op(
            ops.JSONValue(json_path="$.access_urls.write_url")
        )

    def display(
        self,
        n: int = 3,
        *,
        content_type: str = "",
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        """Display the blob content in the IPython Notebook environment. Only works for image type now.

        Args:
            n (int, default 3): number of sample blob objects to display.
            content_type (str, default ""): content type of the blob. If unset, use the blob metadata of the storage. Possible values are "image", "audio" and "video".
            width (int or None, default None): width in pixels that the image/video are constrained to. If unset, use the global setting in bigframes.options.display.blob_display_width, otherwise image/video's original size or ratio is used. No-op for other content types.
            height (int or None, default None): height in pixels that the image/video are constrained to. If unset, use the global setting in bigframes.options.display.blob_display_height, otherwise image/video's original size or ratio is used. No-op for other content types.
        """
        import IPython.display as ipy_display

        width = width or bigframes.options.display.blob_display_width
        height = height or bigframes.options.display.blob_display_height

        # col name doesn't matter here. Rename to avoid column name conflicts
        df = bigframes.series.Series(self._data._block).rename("blob_col").to_frame()

        df["read_url"] = df["blob_col"].blob.read_url()

        if content_type:
            df["content_type"] = content_type
        else:
            df["content_type"] = df["blob_col"].blob.content_type()

        pandas_df, _, query_job = df._block.retrieve_repr_request_results(n)
        df._set_internal_query_job(query_job)

        def display_single_url(
            read_url: Union[str, pd._libs.missing.NAType],
            content_type: Union[str, pd._libs.missing.NAType],
        ):
            if pd.isna(read_url):
                ipy_display.display("<NA>")
                return

            if pd.isna(content_type):  # display as raw data or error
                response = requests.get(read_url)
                ipy_display.display(response.content)
                return

            content_type = cast(str, content_type).casefold()

            if content_type.startswith("image"):
                ipy_display.display(
                    ipy_display.Image(url=read_url, width=width, height=height)
                )
            elif content_type.startswith("audio"):
                # using url somehow doesn't work with audios
                response = requests.get(read_url)
                ipy_display.display(ipy_display.Audio(response.content))
            elif content_type.startswith("video"):
                ipy_display.display(
                    ipy_display.Video(read_url, width=width, height=height)
                )
            else:  # display as raw data
                response = requests.get(read_url)
                ipy_display.display(response.content)

        for _, row in pandas_df.iterrows():
            display_single_url(row["read_url"], row["content_type"])

    @property
    def session(self):
        return self._data._block.session

    def _resolve_connection(self, connection: Optional[str] = None) -> str:
        """Resovle the BigQuery connection.

        Args:
            connection (str or None, default None): BQ connection used for
                function internet transactions, and the output blob if "dst" is
                str. If None, uses default connection of the session.

        Returns:
            str: the resolved BigQuery connection string in the format:
             "project.location.connection_id".

        Raises:
            ValueError: If the connection cannot be resolved to a valid string.
        """
        connection = connection or self._data._block.session._bq_connection
        return clients.get_canonical_bq_connection_id(
            connection,
            default_project=self._data._block.session._project,
            default_location=self._data._block.session._location,
        )

    def get_runtime_json_str(
        self, mode: str = "R", *, with_metadata: bool = False
    ) -> bigframes.series.Series:
        """Get the runtime (contains signed URL to access gcs data) and apply the ToJSONSTring transformation.

        Args:
            mode(str or str, default "R"): the mode for accessing the runtime.
                Default to "R". Possible values are "R" (read-only) and
                "RW" (read-write)
            with_metadata (bool, default False): whether to include metadata
                in the JSON string. Default to False.

        Returns:
            str: the runtime object in the JSON string.
        """
        runtime = self._get_runtime(mode=mode, with_metadata=with_metadata)
        return runtime._apply_unary_op(ops.ToJSONString())

    def exif(
        self,
        *,
        engine: Literal[None, "pillow"] = None,
        connection: Optional[str] = None,
        max_batching_rows: int = 8192,
        container_cpu: Union[float, int] = 0.33,
        container_memory: str = "512Mi",
        verbose: bool = False,
    ) -> bigframes.series.Series:
        """Extract EXIF data. Now only support image types.

        Args:
            engine ('pillow' or None, default None): The engine (bigquery or third party library) used for the function. The value must be specified.
            connection (str or None, default None): BQ connection used for function internet transactions, and the output blob if "dst" is str. If None, uses default connection of the session.
            max_batching_rows (int, default 8,192): Max number of rows per batch send to cloud run to execute the function.
            container_cpu (int or float, default 0.33): number of container CPUs. Possible values are [0.33, 8]. Floats larger than 1 are cast to intergers.
            container_memory (str, default "512Mi"): container memory size. String of the format <number><unit>. Possible values are from 512Mi to 32Gi.
            verbose (bool, default False): If True, returns a struct with status and content fields. If False, returns only the content.

        Returns:
            bigframes.series.Series: JSON series of key-value pairs if verbose=False, or struct with status and content if verbose=True.

        Raises:
            ValueError: If engine is not 'pillow'.
            RuntimeError: If EXIF extraction fails or returns invalid structure.
        """
        if engine is None or engine.casefold() != "pillow":
            raise ValueError("Must specify the engine, supported value is 'pillow'.")

        import bigframes.bigquery as bbq
        import bigframes.blob._functions as blob_func
        import bigframes.pandas as bpd

        connection = self._resolve_connection(connection)
        df = self.get_runtime_json_str(mode="R").to_frame()
        df["verbose"] = verbose

        exif_udf = blob_func.TransformFunction(
            blob_func.exif_func_def,
            session=self._data._block.session,
            connection=connection,
            max_batching_rows=max_batching_rows,
            container_cpu=container_cpu,
            container_memory=container_memory,
        ).udf()

        res = self._apply_udf_or_raise_error(df, exif_udf, "EXIF extraction")

        if verbose:
            try:
                exif_content_series = bbq.parse_json(
                    res._apply_unary_op(ops.JSONValue(json_path="$.content"))
                ).rename("exif_content")
                exif_status_series = res._apply_unary_op(
                    ops.JSONValue(json_path="$.status")
                )
            except Exception as e:
                raise RuntimeError(f"Failed to parse EXIF JSON result: {e}") from e
            results_df = bpd.DataFrame(
                {"status": exif_status_series, "content": exif_content_series}
            )
            results_struct = bbq.struct(results_df).rename("exif_results")
            return results_struct
        else:
            try:
                return bbq.parse_json(res)
            except Exception as e:
                raise RuntimeError(f"Failed to parse EXIF JSON result: {e}") from e

    def image_blur(
        self,
        ksize: tuple[int, int],
        *,
        engine: Literal[None, "opencv"] = None,
        dst: Optional[Union[str, bigframes.series.Series]] = None,
        connection: Optional[str] = None,
        max_batching_rows: int = 8192,
        container_cpu: Union[float, int] = 0.33,
        container_memory: str = "512Mi",
        verbose: bool = False,
    ) -> bigframes.series.Series:
        """Blurs images.

        Args:
            ksize (tuple(int, int)): Kernel size.
            engine ('opencv' or None, default None): The engine (bigquery or third party library) used for the function. The value must be specified.
            dst (str or bigframes.series.Series or None, default None): Output destination. Can be one of:
                str: GCS folder str. The output filenames are the same as the input files.
                blob Series: The output file paths are determined by the uris of the blob Series.
                None: Output to BQ as bytes.
                Encoding is determined by the extension of the output filenames (or input filenames if doesn't have output filenames). If filename doesn't have an extension, use ".jpeg" for encoding.
            connection (str or None, default None): BQ connection used for function internet transactions, and the output blob if "dst" is str. If None, uses default connection of the session.
            max_batching_rows (int, default 8,192): Max number of rows per batch send to cloud run to execute the function.
            container_cpu (int or float, default 0.33): number of container CPUs. Possible values are [0.33, 8]. Floats larger than 1 are cast to intergers.
            container_memory (str, default "512Mi"): container memory size. String of the format <number><unit>. Possible values are from 512Mi to 32Gi.
            verbose (bool, default False): If True, returns a struct with status and content fields. If False, returns only the content.

        Returns:
            bigframes.series.Series: blob Series if destination is GCS. Or bytes Series if destination is BQ. If verbose=True, returns struct with status and content.

        Raises:
            ValueError: If engine is not 'opencv' or parameters are invalid.
            RuntimeError: If image blur operation fails.
        """
        if engine is None or engine.casefold() != "opencv":
            raise ValueError("Must specify the engine, supported value is 'opencv'.")

        import bigframes.bigquery as bbq
        import bigframes.blob._functions as blob_func
        import bigframes.pandas as bpd

        connection = self._resolve_connection(connection)
        df = self.get_runtime_json_str(mode="R").to_frame()

        if dst is None:
            ext = self.uri().str.extract(FILE_EXT_REGEX)

            image_blur_udf = blob_func.TransformFunction(
                blob_func.image_blur_to_bytes_def,
                session=self._data._block.session,
                connection=connection,
                max_batching_rows=max_batching_rows,
                container_cpu=container_cpu,
                container_memory=container_memory,
            ).udf()

            df["ksize_x"], df["ksize_y"] = ksize
            df["ext"] = ext  # type: ignore
            df["verbose"] = verbose
            res = self._apply_udf_or_raise_error(df, image_blur_udf, "Image blur")

            if verbose:
                blurred_content_b64_series = res._apply_unary_op(
                    ops.JSONValue(json_path="$.content")
                )
                blurred_content_series = bbq.sql_scalar(
                    "FROM_BASE64({0})", columns=[blurred_content_b64_series]
                )
                blurred_status_series = res._apply_unary_op(
                    ops.JSONValue(json_path="$.status")
                )
                results_df = bpd.DataFrame(
                    {"status": blurred_status_series, "content": blurred_content_series}
                )
                results_struct = bbq.struct(results_df).rename("blurred_results")
                return results_struct
            else:
                blurred_bytes = bbq.sql_scalar(
                    "FROM_BASE64({0})", columns=[res]
                ).rename("blurred_bytes")
                return blurred_bytes

        if isinstance(dst, str):
            dst = os.path.join(dst, "")
            # Replace src folder with dst folder, keep the file names.
            dst_uri = self.uri().str.replace(FILE_FOLDER_REGEX, rf"{dst}\1", regex=True)
            dst = cast(
                bigframes.series.Series, dst_uri.str.to_blob(connection=connection)
            )

        ext = dst.blob.uri().str.extract(FILE_EXT_REGEX)

        image_blur_udf = blob_func.TransformFunction(
            blob_func.image_blur_def,
            session=self._data._block.session,
            connection=connection,
            max_batching_rows=max_batching_rows,
            container_cpu=container_cpu,
            container_memory=container_memory,
        ).udf()

        dst_rt = dst.blob.get_runtime_json_str(mode="RW")

        df = df.join(dst_rt, how="outer")
        df["ksize_x"], df["ksize_y"] = ksize
        df["ext"] = ext  # type: ignore
        df["verbose"] = verbose

        res = self._apply_udf_or_raise_error(df, image_blur_udf, "Image blur")
        res.cache()  # to execute the udf

        if verbose:
            blurred_status_series = res._apply_unary_op(
                ops.JSONValue(json_path="$.status")
            )
            results_df = bpd.DataFrame(
                {
                    "status": blurred_status_series,
                    "content": dst.blob.uri().str.to_blob(
                        connection=self._resolve_connection(connection)
                    ),
                }
            )
            results_struct = bbq.struct(results_df).rename("blurred_results")
            return results_struct
        else:
            return dst

    def image_resize(
        self,
        dsize: tuple[int, int] = (0, 0),
        *,
        engine: Literal[None, "opencv"] = None,
        fx: float = 0.0,
        fy: float = 0.0,
        dst: Optional[Union[str, bigframes.series.Series]] = None,
        connection: Optional[str] = None,
        max_batching_rows: int = 8192,
        container_cpu: Union[float, int] = 0.33,
        container_memory: str = "512Mi",
        verbose: bool = False,
    ):
        """Resize images.

        Args:
            dsize (tuple(int, int), default (0, 0)): Destination size. If set to 0, fx and fy parameters determine the size.
            engine ('opencv' or None, default None): The engine (bigquery or third party library) used for the function. The value must be specified.
            fx (float, default 0.0): scale factor along the horizontal axis. If set to 0.0, dsize parameter determines the output size.
            fy (float, defalut 0.0): scale factor along the vertical axis. If set to 0.0, dsize parameter determines the output size.
            dst (str or bigframes.series.Series or None, default None): Output destination. Can be one of:
                str: GCS folder str. The output filenames are the same as the input files.
                blob Series: The output file paths are determined by the uris of the blob Series.
                None: Output to BQ as bytes.
                Encoding is determined by the extension of the output filenames (or input filenames if doesn't have output filenames). If filename doesn't have an extension, use ".jpeg" for encoding.
            connection (str or None, default None): BQ connection used for function internet transactions, and the output blob if "dst" is str. If None, uses default connection of the session.
            max_batching_rows (int, default 8,192): Max number of rows per batch send to cloud run to execute the function.
            container_cpu (int or float, default 0.33): number of container CPUs. Possible values are [0.33, 8]. Floats larger than 1 are cast to intergers.
            container_memory (str, default "512Mi"): container memory size. String of the format <number><unit>. Possible values are from 512Mi to 32Gi.
            verbose (bool, default False): If True, returns a struct with status and content fields. If False, returns only the content.

        Returns:
            bigframes.series.Series: blob Series if destination is GCS. Or bytes Series if destination is BQ. If verbose=True, returns struct with status and content.

        Raises:
            ValueError: If engine is not 'opencv' or parameters are invalid.
            RuntimeError: If image resize operation fails.
        """
        if engine is None or engine.casefold() != "opencv":
            raise ValueError("Must specify the engine, supported value is 'opencv'.")

        dsize_set = dsize[0] > 0 and dsize[1] > 0
        fsize_set = fx > 0.0 and fy > 0.0
        if not dsize_set ^ fsize_set:
            raise ValueError(
                "Only one of dsize or (fx, fy) parameters must be set. And the set values must be positive. "
            )

        import bigframes.bigquery as bbq
        import bigframes.blob._functions as blob_func
        import bigframes.pandas as bpd

        connection = self._resolve_connection(connection)
        df = self.get_runtime_json_str(mode="R").to_frame()

        if dst is None:
            ext = self.uri().str.extract(FILE_EXT_REGEX)

            image_resize_udf = blob_func.TransformFunction(
                blob_func.image_resize_to_bytes_def,
                session=self._data._block.session,
                connection=connection,
                max_batching_rows=max_batching_rows,
                container_cpu=container_cpu,
                container_memory=container_memory,
            ).udf()

            df["dsize_x"], df["dsize_y"] = dsize
            df["fx"], df["fy"] = fx, fy
            df["ext"] = ext  # type: ignore
            df["verbose"] = verbose
            res = self._apply_udf_or_raise_error(df, image_resize_udf, "Image resize")

            if verbose:
                resized_content_b64_series = res._apply_unary_op(
                    ops.JSONValue(json_path="$.content")
                )
                resized_content_series = bbq.sql_scalar(
                    "FROM_BASE64({0})", columns=[resized_content_b64_series]
                )

                resized_status_series = res._apply_unary_op(
                    ops.JSONValue(json_path="$.status")
                )
                results_df = bpd.DataFrame(
                    {"status": resized_status_series, "content": resized_content_series}
                )
                results_struct = bbq.struct(results_df).rename("resized_results")
                return results_struct
            else:
                resized_bytes = bbq.sql_scalar(
                    "FROM_BASE64({0})", columns=[res]
                ).rename("resized_bytes")
                return resized_bytes

        if isinstance(dst, str):
            dst = os.path.join(dst, "")
            # Replace src folder with dst folder, keep the file names.
            dst_uri = self.uri().str.replace(FILE_FOLDER_REGEX, rf"{dst}\1", regex=True)
            dst = cast(
                bigframes.series.Series, dst_uri.str.to_blob(connection=connection)
            )

        ext = dst.blob.uri().str.extract(FILE_EXT_REGEX)

        image_resize_udf = blob_func.TransformFunction(
            blob_func.image_resize_def,
            session=self._data._block.session,
            connection=connection,
            max_batching_rows=max_batching_rows,
            container_cpu=container_cpu,
            container_memory=container_memory,
        ).udf()

        dst_rt = dst.blob.get_runtime_json_str(mode="RW")

        df = df.join(dst_rt, how="outer")
        df["dsize_x"], df["dsize_y"] = dsize
        df["fx"], df["fy"] = fx, fy
        df["ext"] = ext  # type: ignore
        df["verbose"] = verbose

        res = self._apply_udf_or_raise_error(df, image_resize_udf, "Image resize")
        res.cache()  # to execute the udf

        if verbose:
            resized_status_series = res._apply_unary_op(
                ops.JSONValue(json_path="$.status")
            )
            results_df = bpd.DataFrame(
                {
                    "status": resized_status_series,
                    "content": dst.blob.uri().str.to_blob(
                        connection=self._resolve_connection(connection)
                    ),
                }
            )
            results_struct = bbq.struct(results_df).rename("resized_results")
            return results_struct
        else:
            return dst

    def image_normalize(
        self,
        *,
        engine: Literal[None, "opencv"] = None,
        alpha: float = 1.0,
        beta: float = 0.0,
        norm_type: str = "l2",
        dst: Optional[Union[str, bigframes.series.Series]] = None,
        connection: Optional[str] = None,
        max_batching_rows: int = 8192,
        container_cpu: Union[float, int] = 0.33,
        container_memory: str = "512Mi",
        verbose: bool = False,
    ) -> bigframes.series.Series:
        """Normalize images.

        Args:
            engine ('opencv' or None, default None): The engine (bigquery or third party library) used for the function. The value must be specified.
            alpha (float, default 1.0): Norm value to normalize to or the lower range boundary in case of the range normalization.
            beta (float, default 0.0): Upper range boundary in case of the range normalization; it is not used for the norm normalization.
            norm_type (str, default "l2"): Normalization type. Accepted values are "inf", "l1", "l2" and "minmax".
            dst (str or bigframes.series.Series or None, default None): Output destination. Can be one of:
                str: GCS folder str. The output filenames are the same as the input files.
                blob Series: The output file paths are determined by the uris of the blob Series.
                None: Output to BQ as bytes.
                Encoding is determined by the extension of the output filenames (or input filenames if doesn't have output filenames). If filename doesn't have an extension, use ".jpeg" for encoding.
            connection (str or None, default None): BQ connection used for function internet transactions, and the output blob if "dst" is str. If None, uses default connection of the session.
            max_batching_rows (int, default 8,192): Max number of rows per batch send to cloud run to execute the function.
            container_cpu (int or float, default 0.33): number of container CPUs. Possible values are [0.33, 8]. Floats larger than 1 are cast to intergers.
            container_memory (str, default "512Mi"): container memory size. String of the format <number><unit>. Possible values are from 512Mi to 32Gi.
            verbose (bool, default False): If True, returns a struct with status and content fields. If False, returns only the content.

        Returns:
            bigframes.series.Series: blob Series if destination is GCS. Or bytes Series if destination is BQ. If verbose=True, returns struct with status and content.

        Raises:
            ValueError: If engine is not 'opencv' or parameters are invalid.
            RuntimeError: If image normalize operation fails.
        """
        if engine is None or engine.casefold() != "opencv":
            raise ValueError("Must specify the engine, supported value is 'opencv'.")

        import bigframes.bigquery as bbq
        import bigframes.blob._functions as blob_func
        import bigframes.pandas as bpd

        connection = self._resolve_connection(connection)
        df = self.get_runtime_json_str(mode="R").to_frame()

        if dst is None:
            ext = self.uri().str.extract(FILE_EXT_REGEX)

            image_normalize_udf = blob_func.TransformFunction(
                blob_func.image_normalize_to_bytes_def,
                session=self._data._block.session,
                connection=connection,
                max_batching_rows=max_batching_rows,
                container_cpu=container_cpu,
                container_memory=container_memory,
            ).udf()

            df["alpha"] = alpha
            df["beta"] = beta
            df["norm_type"] = norm_type
            df["ext"] = ext  # type: ignore
            df["verbose"] = verbose
            res = self._apply_udf_or_raise_error(
                df, image_normalize_udf, "Image normalize"
            )

            if verbose:
                normalized_content_b64_series = res._apply_unary_op(
                    ops.JSONValue(json_path="$.content")
                )
                normalized_bytes = bbq.sql_scalar(
                    "FROM_BASE64({0})", columns=[normalized_content_b64_series]
                )
                normalized_status_series = res._apply_unary_op(
                    ops.JSONValue(json_path="$.status")
                )
                results_df = bpd.DataFrame(
                    {"status": normalized_status_series, "content": normalized_bytes}
                )
                results_struct = bbq.struct(results_df).rename("normalized_results")
                return results_struct
            else:
                normalized_bytes = bbq.sql_scalar(
                    "FROM_BASE64({0})", columns=[res]
                ).rename("normalized_bytes")
                return normalized_bytes

        if isinstance(dst, str):
            dst = os.path.join(dst, "")
            # Replace src folder with dst folder, keep the file names.
            dst_uri = self.uri().str.replace(FILE_FOLDER_REGEX, rf"{dst}\1", regex=True)
            dst = cast(
                bigframes.series.Series, dst_uri.str.to_blob(connection=connection)
            )

        ext = dst.blob.uri().str.extract(FILE_EXT_REGEX)

        image_normalize_udf = blob_func.TransformFunction(
            blob_func.image_normalize_def,
            session=self._data._block.session,
            connection=connection,
            max_batching_rows=max_batching_rows,
            container_cpu=container_cpu,
            container_memory=container_memory,
        ).udf()

        dst_rt = dst.blob.get_runtime_json_str(mode="RW")

        df = df.join(dst_rt, how="outer")
        df["alpha"] = alpha
        df["beta"] = beta
        df["norm_type"] = norm_type
        df["ext"] = ext  # type: ignore
        df["verbose"] = verbose

        res = self._apply_udf_or_raise_error(df, image_normalize_udf, "Image normalize")
        res.cache()  # to execute the udf

        if verbose:
            normalized_status_series = res._apply_unary_op(
                ops.JSONValue(json_path="$.status")
            )
            results_df = bpd.DataFrame(
                {
                    "status": normalized_status_series,
                    "content": dst.blob.uri().str.to_blob(
                        connection=self._resolve_connection(connection)
                    ),
                }
            )
            results_struct = bbq.struct(results_df).rename("normalized_results")
            return results_struct
        else:
            return dst

    def pdf_extract(
        self,
        *,
        engine: Literal[None, "pypdf"] = None,
        connection: Optional[str] = None,
        max_batching_rows: int = 1,
        container_cpu: Union[float, int] = 2,
        container_memory: str = "1Gi",
        verbose: bool = False,
    ) -> bigframes.series.Series:
        """Extracts text from PDF URLs and saves the text as string.

        Args:
            engine ('pypdf' or None, default None): The engine (bigquery or third party library) used for the function. The value must be specified.
            connection (str or None, default None): BQ connection used for
                function internet transactions, and the output blob if "dst"
                is str. If None, uses default connection of the session.
            max_batching_rows (int, default 1): Max number of rows per batch
                send to cloud run to execute the function.
            container_cpu (int or float, default 2): number of container CPUs. Possible values are [0.33, 8]. Floats larger than 1 are cast to intergers.
            container_memory (str, default "1Gi"): container memory size. String of the format <number><unit>. Possible values are from 512Mi to 32Gi.
            verbose (bool, default "False"): controls the verbosity of the output.
                When set to True, both error messages and the extracted content
                are displayed. Conversely, when set to False, only the extracted
                content is presented, suppressing error messages.

        Returns:
            bigframes.series.Series: str or struct[str, str],
                depend on the "verbose" parameter.
                Contains the extracted text from the PDF file.
                Includes error messages if verbosity is enabled.

        Raises:
            ValueError: If engine is not 'pypdf'.
            RuntimeError: If PDF extraction fails or returns invalid structure.
        """
        if engine is None or engine.casefold() != "pypdf":
            raise ValueError("Must specify the engine, supported value is 'pypdf'.")

        import bigframes.bigquery as bbq
        import bigframes.blob._functions as blob_func
        import bigframes.pandas as bpd

        connection = self._resolve_connection(connection)

        pdf_extract_udf = blob_func.TransformFunction(
            blob_func.pdf_extract_def,
            session=self._data._block.session,
            connection=connection,
            max_batching_rows=max_batching_rows,
            container_cpu=container_cpu,
            container_memory=container_memory,
        ).udf()

        df = self.get_runtime_json_str(mode="R").to_frame()
        df["verbose"] = verbose

        res = self._apply_udf_or_raise_error(df, pdf_extract_udf, "PDF extraction")

        if verbose:
            # Extract content with error handling
            try:
                content_series = res._apply_unary_op(
                    ops.JSONValue(json_path="$.content")
                )
            except Exception as e:
                raise RuntimeError(
                    f"Failed to extract content field from PDF result: {e}"
                ) from e
            try:
                status_series = res._apply_unary_op(ops.JSONValue(json_path="$.status"))
            except Exception as e:
                raise RuntimeError(
                    f"Failed to extract status field from PDF result: {e}"
                ) from e

            res_df = bpd.DataFrame({"status": status_series, "content": content_series})
            struct_series = bbq.struct(res_df).rename("extracted_results")
            return struct_series
        else:
            return res.rename("extracted_content")

    def pdf_chunk(
        self,
        *,
        engine: Literal[None, "pypdf"] = None,
        connection: Optional[str] = None,
        chunk_size: int = 2000,
        overlap_size: int = 200,
        max_batching_rows: int = 1,
        container_cpu: Union[float, int] = 2,
        container_memory: str = "1Gi",
        verbose: bool = False,
    ) -> bigframes.series.Series:
        """Extracts and chunks text from PDF URLs and saves the text as
           arrays of strings.

        Args:
            engine ('pypdf' or None, default None): The engine (bigquery or third party library) used for the function. The value must be specified.
            connection (str or None, default None): BQ connection used for
                function internet transactions, and the output blob if "dst"
                is str. If None, uses default connection of the session.
            chunk_size (int, default 2000): the desired size of each text chunk
                (number of characters).
            overlap_size (int, default 200): the number of overlapping characters
                between consective chunks. The helps to ensure context is
                perserved across chunk boundaries.
            max_batching_rows (int, default 1): Max number of rows per batch
                send to cloud run to execute the function.
            container_cpu (int or float, default 2): number of container CPUs. Possible values are [0.33, 8]. Floats larger than 1 are cast to intergers.
            container_memory (str, default "1Gi"): container memory size. String of the format <number><unit>. Possible values are from 512Mi to 32Gi.
            verbose (bool, default "False"): controls the verbosity of the output.
                When set to True, both error messages and the extracted content
                are displayed. Conversely, when set to False, only the extracted
                content is presented, suppressing error messages.

        Returns:
            bigframe.series.Series: array[str] or struct[str, array[str]],
                depend on the "verbose" parameter.
                where each string is a chunk of text extracted from PDF.
                Includes error messages if verbosity is enabled.

        Raises:
            ValueError: If engine is not 'pypdf'.
            RuntimeError: If PDF chunking fails or returns invalid structure.
        """
        if engine is None or engine.casefold() != "pypdf":
            raise ValueError("Must specify the engine, supported value is 'pypdf'.")

        import bigframes.bigquery as bbq
        import bigframes.blob._functions as blob_func
        import bigframes.pandas as bpd

        connection = self._resolve_connection(connection)

        if chunk_size <= 0:
            raise ValueError("chunk_size must be a positive integer.")
        if overlap_size < 0:
            raise ValueError("overlap_size must be a non-negative integer.")
        if overlap_size >= chunk_size:
            raise ValueError("overlap_size must be smaller than chunk_size.")

        pdf_chunk_udf = blob_func.TransformFunction(
            blob_func.pdf_chunk_def,
            session=self._data._block.session,
            connection=connection,
            max_batching_rows=max_batching_rows,
            container_cpu=container_cpu,
            container_memory=container_memory,
        ).udf()

        df = self.get_runtime_json_str(mode="R").to_frame()
        df["chunk_size"] = chunk_size
        df["overlap_size"] = overlap_size
        df["verbose"] = verbose

        res = self._apply_udf_or_raise_error(df, pdf_chunk_udf, "PDF chunking")

        try:
            content_series = bbq.json_extract_string_array(res, "$.content")
        except Exception as e:
            raise RuntimeError(
                f"Failed to extract content array from PDF chunk result: {e}"
            ) from e

        if verbose:
            try:
                status_series = res._apply_unary_op(ops.JSONValue(json_path="$.status"))
            except Exception as e:
                raise RuntimeError(
                    f"Failed to extract status field from PDF chunk result: {e}"
                ) from e

            results_df = bpd.DataFrame(
                {"status": status_series, "content": content_series}
            )
            resultes_struct = bbq.struct(results_df).rename("chunked_results")
            return resultes_struct
        else:
            return bbq.json_extract_string_array(res, "$").rename("chunked_content")

    def audio_transcribe(
        self,
        *,
        engine: Literal["bigquery"] = "bigquery",
        connection: Optional[str] = None,
        model_name: Optional[
            Literal[
                "gemini-2.0-flash-001",
                "gemini-2.0-flash-lite-001",
            ]
        ] = None,
        verbose: bool = False,
    ) -> bigframes.series.Series:
        """
        Transcribe audio content using a Gemini multimodal model.

        Args:
            engine ('bigquery'): The engine (bigquery or third party library) used for the function.
            connection (str or None, default None): BQ connection used for
                function internet transactions, and the output blob if "dst"
                is str. If None, uses default connection of the session.
            model_name (str): The model for natural language tasks. Accepted
                values are "gemini-2.0-flash-lite-001", and "gemini-2.0-flash-001".
                See "https://ai.google.dev/gemini-api/docs/models" for model choices.
            verbose (bool, default "False"): controls the verbosity of the output.
                When set to True, both error messages and the transcribed content
                are displayed. Conversely, when set to False, only the transcribed
                content is presented, suppressing error messages.

        Returns:
            bigframes.series.Series: str or struct[str, str],
                depend on the "verbose" parameter.
                Contains the transcribed text from the audio file.
                Includes error messages if verbosity is enabled.

        Raises:
            ValueError: If engine is not 'bigquery'.
            RuntimeError: If the transcription result structure is invalid.
        """
        if engine.casefold() != "bigquery":
            raise ValueError("Must specify the engine, supported value is 'bigquery'.")

        import bigframes.bigquery as bbq
        import bigframes.pandas as bpd

        # col name doesn't matter here. Rename to avoid column name conflicts
        audio_series = bigframes.series.Series(self._data._block)

        prompt_text = "**Task:** Transcribe the provided audio. **Instructions:** - Your response must contain only the verbatim transcription of the audio. - Do not include any introductory text, summaries, or conversational filler in your response. The output should begin directly with the first word of the audio."

        # Convert the audio series to the runtime representation required by the model.
        audio_runtime = audio_series.blob._get_runtime("R", with_metadata=True)

        transcribed_results = bbq.ai.generate(
            prompt=(prompt_text, audio_runtime),
            connection_id=connection,
            endpoint=model_name,
            model_params={"generationConfig": {"temperature": 0.0}},
        )

        # Validate that the result is not None
        if transcribed_results is None:
            raise RuntimeError("Transcription returned None result")

        transcribed_content_series = transcribed_results.struct.field("result").rename(
            "transcribed_content"
        )

        if verbose:
            transcribed_status_series = transcribed_results.struct.field("status")
            results_df = bpd.DataFrame(
                {
                    "status": transcribed_status_series,
                    "content": transcribed_content_series,
                }
            )
            results_struct = bbq.struct(results_df).rename("transcription_results")
            return results_struct
        else:
            return transcribed_content_series.rename("transcribed_content")
