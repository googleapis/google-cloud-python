# -*- coding: utf-8 -*-
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
#
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.devtools.artifactregistry.v1",
    manifest={
        "DockerImage",
        "ListDockerImagesRequest",
        "ListDockerImagesResponse",
        "GetDockerImageRequest",
    },
)


class DockerImage(proto.Message):
    r"""DockerImage represents a docker artifact. The following fields are
    returned as untyped metadata in the Version resource, using
    camelcase keys (i.e. metadata.imageSizeBytes):

    -  imageSizeBytes
    -  mediaType
    -  buildTime

    Attributes:
        name (str):
            Required. registry_location, project_id, repository_name and
            image id forms a unique image
            name:\ ``projects/<project_id>/locations/<location>/repository/<repository_name>/dockerImages/<docker_image>``.
            For example,
            "projects/test-project/locations/us-west4/repositories/test-repo/dockerImages/
            nginx@sha256:e9954c1fc875017be1c3e36eca16be2d9e9bccc4bf072163515467d6a823c7cf",
            where "us-west4" is the registry_location, "test-project" is
            the project_id, "test-repo" is the repository_name and
            "nginx@sha256:e9954c1fc875017be1c3e36eca16be2d9e9bccc4bf072163515467d6a823c7cf"
            is the image's digest.
        uri (str):
            Required. URL to access the image.
            Example:
            us-west4-docker.pkg.dev/test-project/test-repo/nginx@sha256:e9954c1fc875017be1c3e36eca16be2d9e9bccc4bf072163515467d6a823c7cf
        tags (Sequence[str]):
            Tags attached to this image.
        image_size_bytes (int):
            Calculated size of the image.
            This field is returned as the
            'metadata.imageSizeBytes' field in the Version
            resource.
        upload_time (google.protobuf.timestamp_pb2.Timestamp):
            Time the image was uploaded.
        media_type (str):
            Media type of this image, e.g.
            "application/vnd.docker.distribution.manifest.v2+json".
            This field is returned as the
            'metadata.mediaType' field in the Version
            resource.
        build_time (google.protobuf.timestamp_pb2.Timestamp):
            The time this image was built.
            This field is returned as the
            'metadata.buildTime' field in the Version
            resource.
            The build time is returned to the client as an
            RFC 3339 string, which can be easily used with
            the JavaScript Date constructor.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    uri = proto.Field(
        proto.STRING,
        number=2,
    )
    tags = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    image_size_bytes = proto.Field(
        proto.INT64,
        number=4,
    )
    upload_time = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    media_type = proto.Field(
        proto.STRING,
        number=6,
    )
    build_time = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )


class ListDockerImagesRequest(proto.Message):
    r"""The request to list docker images.

    Attributes:
        parent (str):
            Required. The name of the parent resource
            whose docker images will be listed.
        page_size (int):
            The maximum number of artifacts to return.
        page_token (str):
            The next_page_token value returned from a previous list
            request, if any.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListDockerImagesResponse(proto.Message):
    r"""The response from listing docker images.

    Attributes:
        docker_images (Sequence[google.cloud.artifactregistry_v1.types.DockerImage]):
            The docker images returned.
        next_page_token (str):
            The token to retrieve the next page of
            artifacts, or empty if there are no more
            artifacts to return.
    """

    @property
    def raw_page(self):
        return self

    docker_images = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DockerImage",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetDockerImageRequest(proto.Message):
    r"""The request to get docker images.

    Attributes:
        name (str):
            Required. The name of the docker images.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
