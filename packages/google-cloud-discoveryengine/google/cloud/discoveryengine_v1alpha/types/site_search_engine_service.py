# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.discoveryengine.v1alpha",
    manifest={
        "RecrawlUrisRequest",
        "RecrawlUrisResponse",
        "RecrawlUrisMetadata",
    },
)


class RecrawlUrisRequest(proto.Message):
    r"""Request message for
    [SiteSearchEngineService.RecrawlUris][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.RecrawlUris]
    method.

    Attributes:
        site_search_engine (str):
            Required. Full resource name of the
            [SiteSearchEngine][google.cloud.discoveryengine.v1alpha.SiteSearchEngine],
            such as
            ``projects/*/locations/*/collections/*/dataStores/*/siteSearchEngine``.
        uris (MutableSequence[str]):
            Required. List of URIs to crawl. At most 10K URIs are
            supported, otherwise an INVALID_ARGUMENT error is thrown.
            Each URI should match at least one
            [TargetSite][google.cloud.discoveryengine.v1alpha.TargetSite]
            in ``site_search_engine``.
    """

    site_search_engine: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uris: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class RecrawlUrisResponse(proto.Message):
    r"""Response message for
    [SiteSearchEngineService.RecrawlUris][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.RecrawlUris]
    method.

    Attributes:
        failure_samples (MutableSequence[google.cloud.discoveryengine_v1alpha.types.RecrawlUrisResponse.FailureInfo]):
            Details for a sample of up to 10 ``failed_uris``.
        failed_uris (MutableSequence[str]):
            URIs that were not crawled before the LRO
            terminated.
    """

    class FailureInfo(proto.Message):
        r"""Details about why a particular URI failed to be crawled. Each
        FailureInfo contains one FailureReason per CorpusType.

        Attributes:
            uri (str):
                URI that failed to be crawled.
            failure_reasons (MutableSequence[google.cloud.discoveryengine_v1alpha.types.RecrawlUrisResponse.FailureInfo.FailureReason]):
                List of failure reasons by corpus type (e.g.
                desktop, mobile).
        """

        class FailureReason(proto.Message):
            r"""Details about why crawling failed for a particular
            CorpusType, e.g. DESKTOP and MOBILE crawling may fail for
            different reasons.

            Attributes:
                corpus_type (google.cloud.discoveryengine_v1alpha.types.RecrawlUrisResponse.FailureInfo.FailureReason.CorpusType):
                    DESKTOP, MOBILE, or CORPUS_TYPE_UNSPECIFIED.
                error_message (str):
                    Reason why the URI was not crawled.
            """

            class CorpusType(proto.Enum):
                r"""CorpusType for the failed crawling operation.

                Values:
                    CORPUS_TYPE_UNSPECIFIED (0):
                        Default value.
                    DESKTOP (1):
                        Denotes a crawling attempt for the desktop
                        version of a page.
                    MOBILE (2):
                        Denotes a crawling attempt for the mobile
                        version of a page.
                """
                CORPUS_TYPE_UNSPECIFIED = 0
                DESKTOP = 1
                MOBILE = 2

            corpus_type: "RecrawlUrisResponse.FailureInfo.FailureReason.CorpusType" = (
                proto.Field(
                    proto.ENUM,
                    number=1,
                    enum="RecrawlUrisResponse.FailureInfo.FailureReason.CorpusType",
                )
            )
            error_message: str = proto.Field(
                proto.STRING,
                number=2,
            )

        uri: str = proto.Field(
            proto.STRING,
            number=1,
        )
        failure_reasons: MutableSequence[
            "RecrawlUrisResponse.FailureInfo.FailureReason"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="RecrawlUrisResponse.FailureInfo.FailureReason",
        )

    failure_samples: MutableSequence[FailureInfo] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=FailureInfo,
    )
    failed_uris: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class RecrawlUrisMetadata(proto.Message):
    r"""Metadata related to the progress of the
    [SiteSearchEngineService.RecrawlUris][google.cloud.discoveryengine.v1alpha.SiteSearchEngineService.RecrawlUris]
    operation. This will be returned by the
    google.longrunning.Operation.metadata field.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Operation create time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Operation last update time. If the operation
            is done, this is also the finish time.
        invalid_uris (MutableSequence[str]):
            Unique URIs in the request that don't match
            any TargetSite in the DataStore, only match
            TargetSites that haven't been fully indexed, or
            match a TargetSite with type EXCLUDE.
        valid_uris_count (int):
            Total number of unique URIs in the request that are not in
            invalid_uris.
        success_count (int):
            Total number of URIs that have been crawled
            so far.
        pending_count (int):
            Total number of URIs that have yet to be
            crawled.
        quota_exceeded_count (int):
            Total number of URIs that were rejected due
            to insufficient indexing resources.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    invalid_uris: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    valid_uris_count: int = proto.Field(
        proto.INT32,
        number=4,
    )
    success_count: int = proto.Field(
        proto.INT32,
        number=5,
    )
    pending_count: int = proto.Field(
        proto.INT32,
        number=6,
    )
    quota_exceeded_count: int = proto.Field(
        proto.INT32,
        number=7,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
