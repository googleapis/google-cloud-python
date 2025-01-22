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
from typing import cast, Optional, Union

import IPython.display as ipy_display
import requests

from bigframes import clients
import bigframes.dataframe
from bigframes.operations import base
import bigframes.operations as ops
import bigframes.series


class BlobAccessor(base.SeriesMethods):
    def __init__(self, *args, **kwargs):
        if not bigframes.options.experiments.blob:
            raise NotImplementedError()

        super().__init__(*args, **kwargs)

    def uri(self) -> bigframes.series.Series:
        """URIs of the Blob.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Returns:
            BigFrames Series: URIs as string."""
        s = bigframes.series.Series(self._block)

        return s.struct.field("uri")

    def authorizer(self) -> bigframes.series.Series:
        """Authorizers of the Blob.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Returns:
            BigFrames Series: Autorithers(connection) as string."""
        s = bigframes.series.Series(self._block)

        return s.struct.field("authorizer")

    def version(self) -> bigframes.series.Series:
        """Versions of the Blob.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Returns:
            BigFrames Series: Version as string."""
        # version must be retrieved after fetching metadata
        return self._apply_unary_op(ops.obj_fetch_metadata_op).struct.field("version")

    def metadata(self) -> bigframes.series.Series:
        """Retrieve the metadata of the Blob.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Returns:
            BigFrames Series: JSON metadata of the Blob. Contains fields: content_type, md5_hash, size and updated(time)."""
        details_json = self._apply_unary_op(ops.obj_fetch_metadata_op).struct.field(
            "details"
        )
        import bigframes.bigquery as bbq

        return bbq.json_extract(details_json, "$.gcs_metadata").rename("metadata")

    def content_type(self) -> bigframes.series.Series:
        """Retrieve the content type of the Blob.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Returns:
            BigFrames Series: string of the content type."""
        return (
            self.metadata()
            ._apply_unary_op(ops.JSONValue(json_path="$.content_type"))
            .rename("content_type")
        )

    def md5_hash(self) -> bigframes.series.Series:
        """Retrieve the md5 hash of the Blob.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Returns:
            BigFrames Series: string of the md5 hash."""
        return (
            self.metadata()
            ._apply_unary_op(ops.JSONValue(json_path="$.md5_hash"))
            .rename("md5_hash")
        )

    def size(self) -> bigframes.series.Series:
        """Retrieve the file size of the Blob.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Returns:
            BigFrames Series: file size in bytes."""
        return (
            self.metadata()
            ._apply_unary_op(ops.JSONValue(json_path="$.size"))
            .rename("size")
            .astype("Int64")
        )

    def updated(self) -> bigframes.series.Series:
        """Retrieve the updated time of the Blob.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Returns:
            BigFrames Series: updated time as UTC datetime."""
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
            bigframes Series: ObjectRefRuntime JSON.
        """
        s = self._apply_unary_op(ops.obj_fetch_metadata_op) if with_metadata else self

        return s._apply_unary_op(ops.ObjGetAccessUrl(mode=mode))

    def read_url(self) -> bigframes.series.Series:
        """Retrieve the read URL of the Blob.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Returns:
            BigFrames Series: Read only URLs."""
        return self._get_runtime(mode="R")._apply_unary_op(
            ops.JSONValue(json_path="$.access_urls.read_url")
        )

    def write_url(self) -> bigframes.series.Series:
        """Retrieve the write URL of the Blob.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Returns:
            BigFrames Series: Writable URLs."""
        return self._get_runtime(mode="RW")._apply_unary_op(
            ops.JSONValue(json_path="$.access_urls.write_url")
        )

    def display(self, n: int = 3, *, content_type: str = ""):
        """Display the blob content in the IPython Notebook environment. Only works for image type now.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Args:
            n (int, default 3): number of sample blob objects to display.
            content_type (str, default ""): content type of the blob. If unset, use the blob metadata of the storage. Possible values are "image", "audio" and "video".
        """
        # col name doesn't matter here. Rename to avoid column name conflicts
        df = bigframes.series.Series(self._block).rename("blob_col").head(n).to_frame()

        df["read_url"] = df["blob_col"].blob.read_url()

        if content_type:
            df["content_type"] = content_type
        else:
            df["content_type"] = df["blob_col"].blob.content_type()

        def display_single_url(read_url: str, content_type: str):
            content_type = content_type.casefold()

            if content_type.startswith("image"):
                ipy_display.display(ipy_display.Image(url=read_url))
            elif content_type.startswith("audio"):
                # using url somehow doesn't work with audios
                response = requests.get(read_url)
                ipy_display.display(ipy_display.Audio(response.content))
            elif content_type.startswith("video"):
                ipy_display.display(ipy_display.Video(url=read_url))
            else:  # display as raw data
                response = requests.get(read_url)
                ipy_display.display(response.content)

        for _, row in df.iterrows():
            display_single_url(row["read_url"], row["content_type"])

    def image_blur(
        self,
        ksize: tuple[int, int],
        *,
        dst: Union[str, bigframes.series.Series],
        connection: Optional[str] = None,
    ) -> bigframes.series.Series:
        """Blurs images.

        .. note::
            BigFrames Blob is still under experiments. It may not work and subject to change in the future.

        Args:
            ksize (tuple(int, int)): Kernel size.
            dst (str or bigframes.series.Series): Destination GCS folder str or blob series.
            connection (str or None, default None): BQ connection used for function internet transactions, and the output blob if "dst" is str. If None, uses default connection of the session.

        Returns:
            BigFrames Blob Series
        """
        import bigframes.blob._functions as blob_func

        connection = connection or self._block.session._bq_connection
        connection = clients.resolve_full_bq_connection_name(
            connection,
            default_project=self._block.session._project,
            default_location=self._block.session._location,
        )

        if isinstance(dst, str):
            dst = os.path.join(dst, "")
            src_uri = bigframes.series.Series(self._block).struct.explode()["uri"]
            # Replace src folder with dst folder, keep the file names.
            dst_uri = src_uri.str.replace(r"^.*\/(.*)$", rf"{dst}\1", regex=True)
            dst = cast(
                bigframes.series.Series, dst_uri.str.to_blob(connection=connection)
            )

        image_blur_udf = blob_func.TransformFunction(
            blob_func.image_blur_def,
            session=self._block.session,
            connection=connection,
        ).udf()

        src_rt = self._get_runtime(mode="R")
        dst_rt = dst.blob._get_runtime(mode="RW")

        src_rt = src_rt._apply_unary_op(ops.ToJSONString())
        dst_rt = dst_rt._apply_unary_op(ops.ToJSONString())

        df = src_rt.to_frame().join(dst_rt.to_frame(), how="outer")
        df["ksize_x"], df["ksize_y"] = ksize

        res = df.apply(image_blur_udf, axis=1)
        res.cache()  # to execute the udf

        return dst
