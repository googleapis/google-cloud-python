# -*- coding: utf-8 -*-
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
#
from google.pubsub_v1 import gapic_version as package_version

import google.api_core as api_core
import sys

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.publisher import PublisherClient
from .services.publisher import PublisherAsyncClient
from .services.schema_service import SchemaServiceClient
from .services.schema_service import SchemaServiceAsyncClient
from .services.subscriber import SubscriberClient
from .services.subscriber import SubscriberAsyncClient

from .types.pubsub import AcknowledgeRequest
from .types.pubsub import BigQueryConfig
from .types.pubsub import CloudStorageConfig
from .types.pubsub import CreateSnapshotRequest
from .types.pubsub import DeadLetterPolicy
from .types.pubsub import DeleteSnapshotRequest
from .types.pubsub import DeleteSubscriptionRequest
from .types.pubsub import DeleteTopicRequest
from .types.pubsub import DetachSubscriptionRequest
from .types.pubsub import DetachSubscriptionResponse
from .types.pubsub import ExpirationPolicy
from .types.pubsub import GetSnapshotRequest
from .types.pubsub import GetSubscriptionRequest
from .types.pubsub import GetTopicRequest
from .types.pubsub import IngestionDataSourceSettings
from .types.pubsub import IngestionFailureEvent
from .types.pubsub import JavaScriptUDF
from .types.pubsub import ListSnapshotsRequest
from .types.pubsub import ListSnapshotsResponse
from .types.pubsub import ListSubscriptionsRequest
from .types.pubsub import ListSubscriptionsResponse
from .types.pubsub import ListTopicSnapshotsRequest
from .types.pubsub import ListTopicSnapshotsResponse
from .types.pubsub import ListTopicsRequest
from .types.pubsub import ListTopicsResponse
from .types.pubsub import ListTopicSubscriptionsRequest
from .types.pubsub import ListTopicSubscriptionsResponse
from .types.pubsub import MessageStoragePolicy
from .types.pubsub import MessageTransform
from .types.pubsub import ModifyAckDeadlineRequest
from .types.pubsub import ModifyPushConfigRequest
from .types.pubsub import PlatformLogsSettings
from .types.pubsub import PublishRequest
from .types.pubsub import PublishResponse
from .types.pubsub import PubsubMessage
from .types.pubsub import PullRequest
from .types.pubsub import PullResponse
from .types.pubsub import PushConfig
from .types.pubsub import ReceivedMessage
from .types.pubsub import RetryPolicy
from .types.pubsub import SchemaSettings
from .types.pubsub import SeekRequest
from .types.pubsub import SeekResponse
from .types.pubsub import Snapshot
from .types.pubsub import StreamingPullRequest
from .types.pubsub import StreamingPullResponse
from .types.pubsub import Subscription
from .types.pubsub import Topic
from .types.pubsub import UpdateSnapshotRequest
from .types.pubsub import UpdateSubscriptionRequest
from .types.pubsub import UpdateTopicRequest
from .types.schema import CommitSchemaRequest
from .types.schema import CreateSchemaRequest
from .types.schema import DeleteSchemaRequest
from .types.schema import DeleteSchemaRevisionRequest
from .types.schema import GetSchemaRequest
from .types.schema import ListSchemaRevisionsRequest
from .types.schema import ListSchemaRevisionsResponse
from .types.schema import ListSchemasRequest
from .types.schema import ListSchemasResponse
from .types.schema import RollbackSchemaRequest
from .types.schema import Schema
from .types.schema import ValidateMessageRequest
from .types.schema import ValidateMessageResponse
from .types.schema import ValidateSchemaRequest
from .types.schema import ValidateSchemaResponse
from .types.schema import Encoding
from .types.schema import SchemaView

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.pubsub_v1")  # type: ignore
    api_core.check_dependency_versions("google.pubsub_v1")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import warnings
        import sys

        _py_version_str = sys.version.split()[0]
        _package_label = "google.pubsub_v1"
        if sys.version_info < (3, 9):
            warnings.warn(
                "You are using a non-supported Python version "
                + f"({_py_version_str}).  Google will not post any further "
                + f"updates to {_package_label} supporting this Python version. "
                + "Please upgrade to the latest Python version, or at "
                + f"least to Python 3.9, and then update {_package_label}.",
                FutureWarning,
            )
        if sys.version_info[:2] == (3, 9):
            warnings.warn(
                f"You are using a Python version ({_py_version_str}) "
                + f"which Google will stop supporting in {_package_label} in "
                + "January 2026. Please "
                + "upgrade to the latest Python version, or at "
                + "least to Python 3.10, before then, and "
                + f"then update {_package_label}.",
                FutureWarning,
            )

        def parse_version_to_tuple(version_string: str):
            """Safely converts a semantic version string to a comparable tuple of integers.
            Example: "4.25.8" -> (4, 25, 8)
            Ignores non-numeric parts and handles common version formats.
            Args:
                version_string: Version string in the format "x.y.z" or "x.y.z<suffix>"
            Returns:
                Tuple of integers for the parsed version string.
            """
            parts = []
            for part in version_string.split("."):
                try:
                    parts.append(int(part))
                except ValueError:
                    # If it's a non-numeric part (e.g., '1.0.0b1' -> 'b1'), stop here.
                    # This is a simplification compared to 'packaging.parse_version', but sufficient
                    # for comparing strictly numeric semantic versions.
                    break
            return tuple(parts)

        def _get_version(dependency_name):
            try:
                version_string: str = metadata.version(dependency_name)
                parsed_version = parse_version_to_tuple(version_string)
                return (parsed_version, version_string)
            except Exception:
                # Catch exceptions from metadata.version() (e.g., PackageNotFoundError)
                # or errors during parse_version_to_tuple
                return (None, "--")

        _dependency_package = "google.protobuf"
        _next_supported_version = "4.25.8"
        _next_supported_version_tuple = (4, 25, 8)
        _recommendation = " (we recommend 6.x)"
        (_version_used, _version_used_string) = _get_version(_dependency_package)
        if _version_used and _version_used < _next_supported_version_tuple:
            warnings.warn(
                f"Package {_package_label} depends on "
                + f"{_dependency_package}, currently installed at version "
                + f"{_version_used_string}. Future updates to "
                + f"{_package_label} will require {_dependency_package} at "
                + f"version {_next_supported_version} or higher{_recommendation}."
                + " Please ensure "
                + "that either (a) your Python environment doesn't pin the "
                + f"version of {_dependency_package}, so that updates to "
                + f"{_package_label} can require the higher version, or "
                + "(b) you manually update your Python environment to use at "
                + f"least version {_next_supported_version} of "
                + f"{_dependency_package}.",
                FutureWarning,
            )
    except Exception:
        warnings.warn(
            "Could not determine the version of Python "
            + "currently being used. To continue receiving "
            + "updates for {_package_label}, ensure you are "
            + "using a supported version of Python; see "
            + "https://devguide.python.org/versions/"
        )

__all__ = (
    "PublisherAsyncClient",
    "SchemaServiceAsyncClient",
    "SubscriberAsyncClient",
    "AcknowledgeRequest",
    "BigQueryConfig",
    "CloudStorageConfig",
    "CommitSchemaRequest",
    "CreateSchemaRequest",
    "CreateSnapshotRequest",
    "DeadLetterPolicy",
    "DeleteSchemaRequest",
    "DeleteSchemaRevisionRequest",
    "DeleteSnapshotRequest",
    "DeleteSubscriptionRequest",
    "DeleteTopicRequest",
    "DetachSubscriptionRequest",
    "DetachSubscriptionResponse",
    "Encoding",
    "ExpirationPolicy",
    "GetSchemaRequest",
    "GetSnapshotRequest",
    "GetSubscriptionRequest",
    "GetTopicRequest",
    "IngestionDataSourceSettings",
    "IngestionFailureEvent",
    "JavaScriptUDF",
    "ListSchemaRevisionsRequest",
    "ListSchemaRevisionsResponse",
    "ListSchemasRequest",
    "ListSchemasResponse",
    "ListSnapshotsRequest",
    "ListSnapshotsResponse",
    "ListSubscriptionsRequest",
    "ListSubscriptionsResponse",
    "ListTopicSnapshotsRequest",
    "ListTopicSnapshotsResponse",
    "ListTopicSubscriptionsRequest",
    "ListTopicSubscriptionsResponse",
    "ListTopicsRequest",
    "ListTopicsResponse",
    "MessageStoragePolicy",
    "MessageTransform",
    "ModifyAckDeadlineRequest",
    "ModifyPushConfigRequest",
    "PlatformLogsSettings",
    "PublishRequest",
    "PublishResponse",
    "PublisherClient",
    "PubsubMessage",
    "PullRequest",
    "PullResponse",
    "PushConfig",
    "ReceivedMessage",
    "RetryPolicy",
    "RollbackSchemaRequest",
    "Schema",
    "SchemaServiceClient",
    "SchemaSettings",
    "SchemaView",
    "SeekRequest",
    "SeekResponse",
    "Snapshot",
    "StreamingPullRequest",
    "StreamingPullResponse",
    "SubscriberClient",
    "Subscription",
    "Topic",
    "UpdateSnapshotRequest",
    "UpdateSubscriptionRequest",
    "UpdateTopicRequest",
    "ValidateMessageRequest",
    "ValidateMessageResponse",
    "ValidateSchemaRequest",
    "ValidateSchemaResponse",
)
