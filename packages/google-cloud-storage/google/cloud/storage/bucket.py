# Copyright 2014 Google LLC
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

"""Create / interact with Google Cloud Storage buckets."""

import base64
import copy
import datetime
import functools
import json
import warnings

import six
from six.moves.urllib.parse import urlsplit

from google.api_core import page_iterator
from google.api_core import datetime_helpers
from google.cloud._helpers import _datetime_to_rfc3339
from google.cloud._helpers import _NOW
from google.cloud._helpers import _rfc3339_to_datetime
from google.cloud.exceptions import NotFound
from google.api_core.iam import Policy
from google.cloud.storage import _signing
from google.cloud.storage._helpers import _PropertyMixin
from google.cloud.storage._helpers import _scalar_property
from google.cloud.storage._helpers import _validate_name
from google.cloud.storage._signing import generate_signed_url_v2
from google.cloud.storage._signing import generate_signed_url_v4
from google.cloud.storage.acl import BucketACL
from google.cloud.storage.acl import DefaultObjectACL
from google.cloud.storage.blob import Blob
from google.cloud.storage.constants import _DEFAULT_TIMEOUT
from google.cloud.storage.constants import ARCHIVE_STORAGE_CLASS
from google.cloud.storage.constants import COLDLINE_STORAGE_CLASS
from google.cloud.storage.constants import DUAL_REGION_LOCATION_TYPE
from google.cloud.storage.constants import (
    DURABLE_REDUCED_AVAILABILITY_LEGACY_STORAGE_CLASS,
)
from google.cloud.storage.constants import MULTI_REGIONAL_LEGACY_STORAGE_CLASS
from google.cloud.storage.constants import MULTI_REGION_LOCATION_TYPE
from google.cloud.storage.constants import NEARLINE_STORAGE_CLASS
from google.cloud.storage.constants import REGIONAL_LEGACY_STORAGE_CLASS
from google.cloud.storage.constants import REGION_LOCATION_TYPE
from google.cloud.storage.constants import STANDARD_STORAGE_CLASS
from google.cloud.storage.notification import BucketNotification
from google.cloud.storage.notification import NONE_PAYLOAD_FORMAT


_UBLA_BPO_ENABLED_MESSAGE = (
    "Pass only one of 'uniform_bucket_level_access_enabled' / "
    "'bucket_policy_only_enabled' to 'IAMConfiguration'."
)
_BPO_ENABLED_MESSAGE = (
    "'IAMConfiguration.bucket_policy_only_enabled' is deprecated.  "
    "Instead, use 'IAMConfiguration.uniform_bucket_level_access_enabled'."
)
_UBLA_BPO_LOCK_TIME_MESSAGE = (
    "Pass only one of 'uniform_bucket_level_access_lock_time' / "
    "'bucket_policy_only_lock_time' to 'IAMConfiguration'."
)
_BPO_LOCK_TIME_MESSAGE = (
    "'IAMConfiguration.bucket_policy_only_lock_time' is deprecated.  "
    "Instead, use 'IAMConfiguration.uniform_bucket_level_access_lock_time'."
)
_LOCATION_SETTER_MESSAGE = (
    "Assignment to 'Bucket.location' is deprecated, as it is only "
    "valid before the bucket is created. Instead, pass the location "
    "to `Bucket.create`."
)
_API_ACCESS_ENDPOINT = "https://storage.googleapis.com"


def _blobs_page_start(iterator, page, response):
    """Grab prefixes after a :class:`~google.cloud.iterator.Page` started.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type page: :class:`~google.cloud.api.core.page_iterator.Page`
    :param page: The page that was just created.

    :type response: dict
    :param response: The JSON API response for a page of blobs.
    """
    page.prefixes = tuple(response.get("prefixes", ()))
    iterator.prefixes.update(page.prefixes)


def _item_to_blob(iterator, item):
    """Convert a JSON blob to the native object.

    .. note::

        This assumes that the ``bucket`` attribute has been
        added to the iterator after being created.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that has retrieved the item.

    :type item: dict
    :param item: An item to be converted to a blob.

    :rtype: :class:`.Blob`
    :returns: The next blob in the page.
    """
    name = item.get("name")
    blob = Blob(name, bucket=iterator.bucket)
    blob._set_properties(item)
    return blob


def _item_to_notification(iterator, item):
    """Convert a JSON blob to the native object.

    .. note::

        This assumes that the ``bucket`` attribute has been
        added to the iterator after being created.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that has retrieved the item.

    :type item: dict
    :param item: An item to be converted to a blob.

    :rtype: :class:`.BucketNotification`
    :returns: The next notification being iterated.
    """
    return BucketNotification.from_api_repr(item, bucket=iterator.bucket)


class LifecycleRuleConditions(dict):
    """Map a single lifecycle rule for a bucket.

    See: https://cloud.google.com/storage/docs/lifecycle

    :type age: int
    :param age: (optional) apply rule action to items whos age, in days,
                exceeds this value.

    :type created_before: datetime.date
    :param created_before: (optional) apply rule action to items created
                           before this date.

    :type is_live: bool
    :param is_live: (optional) if true, apply rule action to non-versioned
                    items, or to items with no newer versions. If false, apply
                    rule action to versioned items with at least one newer
                    version.

    :type matches_storage_class: list(str), one or more of
                                 :attr:`Bucket.STORAGE_CLASSES`.
    :param matches_storage_class: (optional) apply rule action to items which
                                  whose storage class matches this value.

    :type number_of_newer_versions: int
    :param number_of_newer_versions: (optional) apply rule action to versioned
                                     items having N newer versions.

    :raises ValueError: if no arguments are passed.
    """

    def __init__(
        self,
        age=None,
        created_before=None,
        is_live=None,
        matches_storage_class=None,
        number_of_newer_versions=None,
        _factory=False,
    ):
        conditions = {}

        if age is not None:
            conditions["age"] = age

        if created_before is not None:
            conditions["createdBefore"] = created_before.isoformat()

        if is_live is not None:
            conditions["isLive"] = is_live

        if matches_storage_class is not None:
            conditions["matchesStorageClass"] = matches_storage_class

        if number_of_newer_versions is not None:
            conditions["numNewerVersions"] = number_of_newer_versions

        if not _factory and not conditions:
            raise ValueError("Supply at least one condition")

        super(LifecycleRuleConditions, self).__init__(conditions)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory:  construct instance from resource.

        :type resource: dict
        :param resource: mapping as returned from API call.

        :rtype: :class:`LifecycleRuleConditions`
        :returns: Instance created from resource.
        """
        instance = cls(_factory=True)
        instance.update(resource)
        return instance

    @property
    def age(self):
        """Conditon's age value."""
        return self.get("age")

    @property
    def created_before(self):
        """Conditon's created_before value."""
        before = self.get("createdBefore")
        if before is not None:
            return datetime_helpers.from_iso8601_date(before)

    @property
    def is_live(self):
        """Conditon's 'is_live' value."""
        return self.get("isLive")

    @property
    def matches_storage_class(self):
        """Conditon's 'matches_storage_class' value."""
        return self.get("matchesStorageClass")

    @property
    def number_of_newer_versions(self):
        """Conditon's 'number_of_newer_versions' value."""
        return self.get("numNewerVersions")


class LifecycleRuleDelete(dict):
    """Map a lifecycle rule deleting matching items.

    :type kw: dict
    :params kw: arguments passed to :class:`LifecycleRuleConditions`.
    """

    def __init__(self, **kw):
        conditions = LifecycleRuleConditions(**kw)
        rule = {"action": {"type": "Delete"}, "condition": dict(conditions)}
        super(LifecycleRuleDelete, self).__init__(rule)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory:  construct instance from resource.

        :type resource: dict
        :param resource: mapping as returned from API call.

        :rtype: :class:`LifecycleRuleDelete`
        :returns: Instance created from resource.
        """
        instance = cls(_factory=True)
        instance.update(resource)
        return instance


class LifecycleRuleSetStorageClass(dict):
    """Map a lifecycle rule upating storage class of matching items.

    :type storage_class: str, one of :attr:`Bucket.STORAGE_CLASSES`.
    :param storage_class: new storage class to assign to matching items.

    :type kw: dict
    :params kw: arguments passed to :class:`LifecycleRuleConditions`.
    """

    def __init__(self, storage_class, **kw):
        conditions = LifecycleRuleConditions(**kw)
        rule = {
            "action": {"type": "SetStorageClass", "storageClass": storage_class},
            "condition": dict(conditions),
        }
        super(LifecycleRuleSetStorageClass, self).__init__(rule)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory:  construct instance from resource.

        :type resource: dict
        :param resource: mapping as returned from API call.

        :rtype: :class:`LifecycleRuleDelete`
        :returns: Instance created from resource.
        """
        action = resource["action"]
        instance = cls(action["storageClass"], _factory=True)
        instance.update(resource)
        return instance


_default = object()


class IAMConfiguration(dict):
    """Map a bucket's IAM configuration.

    :type bucket: :class:`Bucket`
    :params bucket: Bucket for which this instance is the policy.

    :type uniform_bucket_level_access_enabled: bool
    :params bucket_policy_only_enabled:
        (optional) whether the IAM-only policy is enabled for the bucket.

    :type uniform_bucket_level_locked_time: :class:`datetime.datetime`
    :params uniform_bucket_level_locked_time:
        (optional) When the bucket's IAM-only policy was enabled.
        This value should normally only be set by the back-end API.

    :type bucket_policy_only_enabled: bool
    :params bucket_policy_only_enabled:
        Deprecated alias for :data:`uniform_bucket_level_access_enabled`.

    :type bucket_policy_only_locked_time: :class:`datetime.datetime`
    :params bucket_policy_only_locked_time:
        Deprecated alias for :data:`uniform_bucket_level_access_locked_time`.
    """

    def __init__(
        self,
        bucket,
        uniform_bucket_level_access_enabled=_default,
        uniform_bucket_level_access_locked_time=_default,
        bucket_policy_only_enabled=_default,
        bucket_policy_only_locked_time=_default,
    ):
        if bucket_policy_only_enabled is not _default:

            if uniform_bucket_level_access_enabled is not _default:
                raise ValueError(_UBLA_BPO_ENABLED_MESSAGE)

            warnings.warn(_BPO_ENABLED_MESSAGE, DeprecationWarning, stacklevel=2)
            uniform_bucket_level_access_enabled = bucket_policy_only_enabled

        if bucket_policy_only_locked_time is not _default:

            if uniform_bucket_level_access_locked_time is not _default:
                raise ValueError(_UBLA_BPO_LOCK_TIME_MESSAGE)

            warnings.warn(_BPO_LOCK_TIME_MESSAGE, DeprecationWarning, stacklevel=2)
            uniform_bucket_level_access_locked_time = bucket_policy_only_locked_time

        if uniform_bucket_level_access_enabled is _default:
            uniform_bucket_level_access_enabled = False

        data = {
            "uniformBucketLevelAccess": {"enabled": uniform_bucket_level_access_enabled}
        }
        if uniform_bucket_level_access_locked_time is not _default:
            data["uniformBucketLevelAccess"]["lockedTime"] = _datetime_to_rfc3339(
                uniform_bucket_level_access_locked_time
            )
        super(IAMConfiguration, self).__init__(data)
        self._bucket = bucket

    @classmethod
    def from_api_repr(cls, resource, bucket):
        """Factory:  construct instance from resource.

        :type bucket: :class:`Bucket`
        :params bucket: Bucket for which this instance is the policy.

        :type resource: dict
        :param resource: mapping as returned from API call.

        :rtype: :class:`IAMConfiguration`
        :returns: Instance created from resource.
        """
        instance = cls(bucket)
        instance.update(resource)
        return instance

    @property
    def bucket(self):
        """Bucket for which this instance is the policy.

        :rtype: :class:`Bucket`
        :returns: the instance's bucket.
        """
        return self._bucket

    @property
    def uniform_bucket_level_access_enabled(self):
        """If set, access checks only use bucket-level IAM policies or above.

        :rtype: bool
        :returns: whether the bucket is configured to allow only IAM.
        """
        ubla = self.get("uniformBucketLevelAccess", {})
        return ubla.get("enabled", False)

    @uniform_bucket_level_access_enabled.setter
    def uniform_bucket_level_access_enabled(self, value):
        ubla = self.setdefault("uniformBucketLevelAccess", {})
        ubla["enabled"] = bool(value)
        self.bucket._patch_property("iamConfiguration", self)

    @property
    def uniform_bucket_level_access_locked_time(self):
        """Deadline for changing :attr:`uniform_bucket_level_access_enabled` from true to false.

        If the bucket's :attr:`uniform_bucket_level_access_enabled` is true, this property
        is time time after which that setting becomes immutable.

        If the bucket's :attr:`uniform_bucket_level_access_enabled` is false, this property
        is ``None``.

        :rtype: Union[:class:`datetime.datetime`, None]
        :returns:  (readonly) Time after which :attr:`uniform_bucket_level_access_enabled` will
                   be frozen as true.
        """
        ubla = self.get("uniformBucketLevelAccess", {})
        stamp = ubla.get("lockedTime")
        if stamp is not None:
            stamp = _rfc3339_to_datetime(stamp)
        return stamp

    @property
    def bucket_policy_only_enabled(self):
        """Deprecated alias for :attr:`uniform_bucket_level_access_enabled`.

        :rtype: bool
        :returns: whether the bucket is configured to allow only IAM.
        """
        return self.uniform_bucket_level_access_enabled

    @bucket_policy_only_enabled.setter
    def bucket_policy_only_enabled(self, value):
        warnings.warn(_BPO_ENABLED_MESSAGE, DeprecationWarning, stacklevel=2)
        self.uniform_bucket_level_access_enabled = value

    @property
    def bucket_policy_only_locked_time(self):
        """Deprecated alias for :attr:`uniform_bucket_level_access_locked_time`.

        :rtype: Union[:class:`datetime.datetime`, None]
        :returns:
            (readonly) Time after which :attr:`bucket_policy_only_enabled` will
            be frozen as true.
        """
        return self.uniform_bucket_level_access_locked_time


class Bucket(_PropertyMixin):
    """A class representing a Bucket on Cloud Storage.

    :type client: :class:`google.cloud.storage.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the bucket (which requires a project).

    :type name: str
    :param name: The name of the bucket. Bucket names must start and end with a
                 number or letter.

    :type user_project: str
    :param user_project: (Optional) the project ID to be billed for API
                         requests made via this instance.
    """

    _MAX_OBJECTS_FOR_ITERATION = 256
    """Maximum number of existing objects allowed in iteration.

    This is used in Bucket.delete() and Bucket.make_public().
    """

    STORAGE_CLASSES = (
        STANDARD_STORAGE_CLASS,
        NEARLINE_STORAGE_CLASS,
        COLDLINE_STORAGE_CLASS,
        ARCHIVE_STORAGE_CLASS,
        MULTI_REGIONAL_LEGACY_STORAGE_CLASS,  # legacy
        REGIONAL_LEGACY_STORAGE_CLASS,  # legacy
        DURABLE_REDUCED_AVAILABILITY_LEGACY_STORAGE_CLASS,  # legacy
    )
    """Allowed values for :attr:`storage_class`.

    Default value is :attr:`STANDARD_STORAGE_CLASS`.

    See
    https://cloud.google.com/storage/docs/json_api/v1/buckets#storageClass
    https://cloud.google.com/storage/docs/storage-classes
    """

    _LOCATION_TYPES = (
        MULTI_REGION_LOCATION_TYPE,
        REGION_LOCATION_TYPE,
        DUAL_REGION_LOCATION_TYPE,
    )
    """Allowed values for :attr:`location_type`."""

    def __init__(self, client, name=None, user_project=None):
        name = _validate_name(name)
        super(Bucket, self).__init__(name=name)
        self._client = client
        self._acl = BucketACL(self)
        self._default_object_acl = DefaultObjectACL(self)
        self._label_removals = set()
        self._user_project = user_project

    def __repr__(self):
        return "<Bucket: %s>" % (self.name,)

    @property
    def client(self):
        """The client bound to this bucket."""
        return self._client

    def _set_properties(self, value):
        """Set the properties for the current object.

        :type value: dict or :class:`google.cloud.storage.batch._FutureDict`
        :param value: The properties to be set.
        """
        self._label_removals.clear()
        return super(Bucket, self)._set_properties(value)

    @property
    def user_project(self):
        """Project ID to be billed for API requests made via this bucket.

        If unset, API requests are billed to the bucket owner.

        :rtype: str
        """
        return self._user_project

    @classmethod
    def from_string(cls, uri, client=None):
        """Get a constructor for bucket object by URI.

        :type uri: str
        :param uri: The bucket uri pass to get bucket object.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.

        :rtype: :class:`google.cloud.storage.bucket.Bucket`
        :returns: The bucket object created.

        Example:
            Get a constructor for bucket object by URI..

            >>> from google.cloud import storage
            >>> from google.cloud.storage.bucket import Bucket
            >>> client = storage.Client()
            >>> bucket = Bucket.from_string("gs://bucket",client)
        """
        scheme, netloc, path, query, frag = urlsplit(uri)

        if scheme != "gs":
            raise ValueError("URI scheme must be gs")

        return cls(client, name=netloc)

    def blob(
        self,
        blob_name,
        chunk_size=None,
        encryption_key=None,
        kms_key_name=None,
        generation=None,
    ):
        """Factory constructor for blob object.

        .. note::
          This will not make an HTTP request; it simply instantiates
          a blob object owned by this bucket.

        :type blob_name: str
        :param blob_name: The name of the blob to be instantiated.

        :type chunk_size: int
        :param chunk_size: The size of a chunk of data whenever iterating
                           (in bytes). This must be a multiple of 256 KB per
                           the API specification.

        :type encryption_key: bytes
        :param encryption_key:
            Optional 32 byte encryption key for customer-supplied encryption.

        :type kms_key_name: str
        :param kms_key_name:
            Optional resource name of KMS key used to encrypt blob's content.

        :type generation: long
        :param generation: Optional. If present, selects a specific revision of
                           this object.

        :rtype: :class:`google.cloud.storage.blob.Blob`
        :returns: The blob object created.
        """
        return Blob(
            name=blob_name,
            bucket=self,
            chunk_size=chunk_size,
            encryption_key=encryption_key,
            kms_key_name=kms_key_name,
            generation=generation,
        )

    def notification(
        self,
        topic_name,
        topic_project=None,
        custom_attributes=None,
        event_types=None,
        blob_name_prefix=None,
        payload_format=NONE_PAYLOAD_FORMAT,
    ):
        """Factory:  create a notification resource for the bucket.

        See: :class:`.BucketNotification` for parameters.

        :rtype: :class:`.BucketNotification`
        """
        return BucketNotification(
            self,
            topic_name,
            topic_project=topic_project,
            custom_attributes=custom_attributes,
            event_types=event_types,
            blob_name_prefix=blob_name_prefix,
            payload_format=payload_format,
        )

    def exists(self, client=None, timeout=_DEFAULT_TIMEOUT):
        """Determines whether or not this bucket exists.

        If :attr:`user_project` is set, bills the API request to that project.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.
        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: bool
        :returns: True if the bucket exists in Cloud Storage.
        """
        client = self._require_client(client)
        # We only need the status code (200 or not) so we seek to
        # minimize the returned payload.
        query_params = {"fields": "name"}

        if self.user_project is not None:
            query_params["userProject"] = self.user_project

        try:
            # We intentionally pass `_target_object=None` since fields=name
            # would limit the local properties.
            client._connection.api_request(
                method="GET",
                path=self.path,
                query_params=query_params,
                _target_object=None,
                timeout=timeout,
            )
            # NOTE: This will not fail immediately in a batch. However, when
            #       Batch.finish() is called, the resulting `NotFound` will be
            #       raised.
            return True
        except NotFound:
            return False

    def create(
        self,
        client=None,
        project=None,
        location=None,
        predefined_acl=None,
        predefined_default_object_acl=None,
        timeout=_DEFAULT_TIMEOUT,
    ):
        """Creates current bucket.

        If the bucket already exists, will raise
        :class:`google.cloud.exceptions.Conflict`.

        This implements "storage.buckets.insert".

        If :attr:`user_project` is set, bills the API request to that project.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use. If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :type project: str
        :param project: Optional. The project under which the bucket is to
                        be created. If not passed, uses the project set on
                        the client.
        :raises ValueError: if :attr:`user_project` is set.
        :raises ValueError: if ``project`` is None and client's
                            :attr:`project` is also None.

        :type location: str
        :param location: Optional. The location of the bucket. If not passed,
                         the default location, US, will be used. See
                         https://cloud.google.com/storage/docs/bucket-locations

        :type predefined_acl: str
        :param predefined_acl:
            Optional. Name of predefined ACL to apply to bucket. See:
            https://cloud.google.com/storage/docs/access-control/lists#predefined-acl

        :type predefined_default_object_acl: str
        :param predefined_default_object_acl:
            Optional. Name of predefined ACL to apply to bucket's objects. See:
            https://cloud.google.com/storage/docs/access-control/lists#predefined-acl

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.
        """
        if self.user_project is not None:
            raise ValueError("Cannot create bucket with 'user_project' set.")

        client = self._require_client(client)

        if project is None:
            project = client.project

        if project is None:
            raise ValueError("Client project not set:  pass an explicit project.")

        query_params = {"project": project}

        if predefined_acl is not None:
            predefined_acl = BucketACL.validate_predefined(predefined_acl)
            query_params["predefinedAcl"] = predefined_acl

        if predefined_default_object_acl is not None:
            predefined_default_object_acl = DefaultObjectACL.validate_predefined(
                predefined_default_object_acl
            )
            query_params["predefinedDefaultObjectAcl"] = predefined_default_object_acl

        properties = {key: self._properties[key] for key in self._changes}
        properties["name"] = self.name

        if location is not None:
            properties["location"] = location

        api_response = client._connection.api_request(
            method="POST",
            path="/b",
            query_params=query_params,
            data=properties,
            _target_object=self,
            timeout=timeout,
        )
        self._set_properties(api_response)

    def patch(self, client=None, timeout=_DEFAULT_TIMEOUT):
        """Sends all changed properties in a PATCH request.

        Updates the ``_properties`` with the response from the backend.

        If :attr:`user_project` is set, bills the API request to that project.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current object.
        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.
        """
        # Special case: For buckets, it is possible that labels are being
        # removed; this requires special handling.
        if self._label_removals:
            self._changes.add("labels")
            self._properties.setdefault("labels", {})
            for removed_label in self._label_removals:
                self._properties["labels"][removed_label] = None

        # Call the superclass method.
        return super(Bucket, self).patch(client=client, timeout=timeout)

    @property
    def acl(self):
        """Create our ACL on demand."""
        return self._acl

    @property
    def default_object_acl(self):
        """Create our defaultObjectACL on demand."""
        return self._default_object_acl

    @staticmethod
    def path_helper(bucket_name):
        """Relative URL path for a bucket.

        :type bucket_name: str
        :param bucket_name: The bucket name in the path.

        :rtype: str
        :returns: The relative URL path for ``bucket_name``.
        """
        return "/b/" + bucket_name

    @property
    def path(self):
        """The URL path to this bucket."""
        if not self.name:
            raise ValueError("Cannot determine path without bucket name.")

        return self.path_helper(self.name)

    def get_blob(
        self,
        blob_name,
        client=None,
        encryption_key=None,
        generation=None,
        timeout=_DEFAULT_TIMEOUT,
        **kwargs
    ):
        """Get a blob object by name.

        This will return None if the blob doesn't exist:

        .. literalinclude:: snippets.py
          :start-after: [START get_blob]
          :end-before: [END get_blob]

        If :attr:`user_project` is set, bills the API request to that project.

        :type blob_name: str
        :param blob_name: The name of the blob to retrieve.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :type encryption_key: bytes
        :param encryption_key:
            Optional 32 byte encryption key for customer-supplied encryption.
            See
            https://cloud.google.com/storage/docs/encryption#customer-supplied.

        :type generation: long
        :param generation: Optional. If present, selects a specific revision of
                           this object.

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :param kwargs: Keyword arguments to pass to the
                       :class:`~google.cloud.storage.blob.Blob` constructor.

        :rtype: :class:`google.cloud.storage.blob.Blob` or None
        :returns: The blob object if it exists, otherwise None.
        """
        blob = Blob(
            bucket=self,
            name=blob_name,
            encryption_key=encryption_key,
            generation=generation,
            **kwargs
        )
        try:
            # NOTE: This will not fail immediately in a batch. However, when
            #       Batch.finish() is called, the resulting `NotFound` will be
            #       raised.
            blob.reload(client=client, timeout=timeout)
        except NotFound:
            return None
        else:
            return blob

    def list_blobs(
        self,
        max_results=None,
        page_token=None,
        prefix=None,
        delimiter=None,
        versions=None,
        projection="noAcl",
        fields=None,
        client=None,
        timeout=_DEFAULT_TIMEOUT,
    ):
        """Return an iterator used to find blobs in the bucket.

        .. note::
          Direct use of this method is deprecated. Use ``Client.list_blobs`` instead.

        If :attr:`user_project` is set, bills the API request to that project.

        :type max_results: int
        :param max_results:
            (Optional) The maximum number of blobs to return.

        :type page_token: str
        :param page_token:
            (Optional) If present, return the next batch of blobs, using the
            value, which must correspond to the ``nextPageToken`` value
            returned in the previous response.  Deprecated: use the ``pages``
            property of the returned iterator instead of manually passing the
            token.

        :type prefix: str
        :param prefix: (Optional) prefix used to filter blobs.

        :type delimiter: str
        :param delimiter: (Optional) Delimiter, used with ``prefix`` to
                          emulate hierarchy.

        :type versions: bool
        :param versions: (Optional) Whether object versions should be returned
                         as separate blobs.

        :type projection: str
        :param projection: (Optional) If used, must be 'full' or 'noAcl'.
                           Defaults to ``'noAcl'``. Specifies the set of
                           properties to return.

        :type fields: str
        :param fields:
            (Optional) Selector specifying which fields to include
            in a partial response. Must be a list of fields. For
            example to get a partial response with just the next
            page token and the name and language of each blob returned:
            ``'items(name,contentLanguage),nextPageToken'``.
            See: https://cloud.google.com/storage/docs/json_api/v1/parameters#fields

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of all :class:`~google.cloud.storage.blob.Blob`
                  in this bucket matching the arguments.
        """
        extra_params = {"projection": projection}

        if prefix is not None:
            extra_params["prefix"] = prefix

        if delimiter is not None:
            extra_params["delimiter"] = delimiter

        if versions is not None:
            extra_params["versions"] = versions

        if fields is not None:
            extra_params["fields"] = fields

        if self.user_project is not None:
            extra_params["userProject"] = self.user_project

        client = self._require_client(client)
        path = self.path + "/o"
        api_request = functools.partial(client._connection.api_request, timeout=timeout)
        iterator = page_iterator.HTTPIterator(
            client=client,
            api_request=api_request,
            path=path,
            item_to_value=_item_to_blob,
            page_token=page_token,
            max_results=max_results,
            extra_params=extra_params,
            page_start=_blobs_page_start,
        )
        iterator.bucket = self
        iterator.prefixes = set()
        return iterator

    def list_notifications(self, client=None, timeout=_DEFAULT_TIMEOUT):
        """List Pub / Sub notifications for this bucket.

        See:
        https://cloud.google.com/storage/docs/json_api/v1/notifications/list

        If :attr:`user_project` is set, bills the API request to that project.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.
        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: list of :class:`.BucketNotification`
        :returns: notification instances
        """
        client = self._require_client(client)
        path = self.path + "/notificationConfigs"
        api_request = functools.partial(client._connection.api_request, timeout=timeout)
        iterator = page_iterator.HTTPIterator(
            client=client,
            api_request=api_request,
            path=path,
            item_to_value=_item_to_notification,
        )
        iterator.bucket = self
        return iterator

    def delete(self, force=False, client=None, timeout=_DEFAULT_TIMEOUT):
        """Delete this bucket.

        The bucket **must** be empty in order to submit a delete request. If
        ``force=True`` is passed, this will first attempt to delete all the
        objects / blobs in the bucket (i.e. try to empty the bucket).

        If the bucket doesn't exist, this will raise
        :class:`google.cloud.exceptions.NotFound`.  If the bucket is not empty
        (and ``force=False``), will raise
        :class:`google.cloud.exceptions.Conflict`.

        If ``force=True`` and the bucket contains more than 256 objects / blobs
        this will cowardly refuse to delete the objects (or the bucket). This
        is to prevent accidental bucket deletion and to prevent extremely long
        runtime of this method.

        If :attr:`user_project` is set, bills the API request to that project.

        :type force: bool
        :param force: If True, empties the bucket's objects then deletes it.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.
        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response on each request.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :raises: :class:`ValueError` if ``force`` is ``True`` and the bucket
                 contains more than 256 objects / blobs.
        """
        client = self._require_client(client)
        query_params = {}

        if self.user_project is not None:
            query_params["userProject"] = self.user_project

        if force:
            blobs = list(
                self.list_blobs(
                    max_results=self._MAX_OBJECTS_FOR_ITERATION + 1,
                    client=client,
                    timeout=timeout,
                )
            )
            if len(blobs) > self._MAX_OBJECTS_FOR_ITERATION:
                message = (
                    "Refusing to delete bucket with more than "
                    "%d objects. If you actually want to delete "
                    "this bucket, please delete the objects "
                    "yourself before calling Bucket.delete()."
                ) % (self._MAX_OBJECTS_FOR_ITERATION,)
                raise ValueError(message)

            # Ignore 404 errors on delete.
            self.delete_blobs(
                blobs, on_error=lambda blob: None, client=client, timeout=timeout
            )

        # We intentionally pass `_target_object=None` since a DELETE
        # request has no response value (whether in a standard request or
        # in a batch request).
        client._connection.api_request(
            method="DELETE",
            path=self.path,
            query_params=query_params,
            _target_object=None,
            timeout=timeout,
        )

    def delete_blob(
        self, blob_name, client=None, generation=None, timeout=_DEFAULT_TIMEOUT
    ):
        """Deletes a blob from the current bucket.

        If the blob isn't found (backend 404), raises a
        :class:`google.cloud.exceptions.NotFound`.

        For example:

        .. literalinclude:: snippets.py
          :start-after: [START delete_blob]
          :end-before: [END delete_blob]

        If :attr:`user_project` is set, bills the API request to that project.

        :type blob_name: str
        :param blob_name: A blob name to delete.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :type generation: long
        :param generation: Optional. If present, permanently deletes a specific
                           revision of this object.

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :raises: :class:`google.cloud.exceptions.NotFound` (to suppress
                 the exception, call ``delete_blobs``, passing a no-op
                 ``on_error`` callback, e.g.:

        .. literalinclude:: snippets.py
            :start-after: [START delete_blobs]
            :end-before: [END delete_blobs]

        """
        client = self._require_client(client)
        blob = Blob(blob_name, bucket=self, generation=generation)

        # We intentionally pass `_target_object=None` since a DELETE
        # request has no response value (whether in a standard request or
        # in a batch request).
        client._connection.api_request(
            method="DELETE",
            path=blob.path,
            query_params=blob._query_params,
            _target_object=None,
            timeout=timeout,
        )

    def delete_blobs(self, blobs, on_error=None, client=None, timeout=_DEFAULT_TIMEOUT):
        """Deletes a list of blobs from the current bucket.

        Uses :meth:`delete_blob` to delete each individual blob.

        If :attr:`user_project` is set, bills the API request to that project.

        :type blobs: list
        :param blobs: A list of :class:`~google.cloud.storage.blob.Blob`-s or
                      blob names to delete.

        :type on_error: callable
        :param on_error: (Optional) Takes single argument: ``blob``. Called
                         called once for each blob raising
                         :class:`~google.cloud.exceptions.NotFound`;
                         otherwise, the exception is propagated.

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response. The timeout applies to each individual
            blob delete request.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :raises: :class:`~google.cloud.exceptions.NotFound` (if
                 `on_error` is not passed).
        """
        for blob in blobs:
            try:
                blob_name = blob
                if not isinstance(blob_name, six.string_types):
                    blob_name = blob.name
                self.delete_blob(blob_name, client=client, timeout=timeout)
            except NotFound:
                if on_error is not None:
                    on_error(blob)
                else:
                    raise

    def copy_blob(
        self,
        blob,
        destination_bucket,
        new_name=None,
        client=None,
        preserve_acl=True,
        source_generation=None,
        timeout=_DEFAULT_TIMEOUT,
    ):
        """Copy the given blob to the given bucket, optionally with a new name.

        If :attr:`user_project` is set, bills the API request to that project.

        :type blob: :class:`google.cloud.storage.blob.Blob`
        :param blob: The blob to be copied.

        :type destination_bucket: :class:`google.cloud.storage.bucket.Bucket`
        :param destination_bucket: The bucket into which the blob should be
                                   copied.

        :type new_name: str
        :param new_name: (optional) the new name for the copied file.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :type preserve_acl: bool
        :param preserve_acl: Optional. Copies ACL from old blob to new blob.
                             Default: True.

        :type source_generation: long
        :param source_generation: Optional. The generation of the blob to be
                                  copied.

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: :class:`google.cloud.storage.blob.Blob`
        :returns: The new Blob.
        """
        client = self._require_client(client)
        query_params = {}

        if self.user_project is not None:
            query_params["userProject"] = self.user_project

        if source_generation is not None:
            query_params["sourceGeneration"] = source_generation

        if new_name is None:
            new_name = blob.name

        new_blob = Blob(bucket=destination_bucket, name=new_name)
        api_path = blob.path + "/copyTo" + new_blob.path
        copy_result = client._connection.api_request(
            method="POST",
            path=api_path,
            query_params=query_params,
            _target_object=new_blob,
            timeout=timeout,
        )

        if not preserve_acl:
            new_blob.acl.save(acl={}, client=client, timeout=timeout)

        new_blob._set_properties(copy_result)
        return new_blob

    def rename_blob(self, blob, new_name, client=None, timeout=_DEFAULT_TIMEOUT):
        """Rename the given blob using copy and delete operations.

        If :attr:`user_project` is set, bills the API request to that project.

        Effectively, copies blob to the same bucket with a new name, then
        deletes the blob.

        .. warning::

          This method will first duplicate the data and then delete the
          old blob.  This means that with very large objects renaming
          could be a very (temporarily) costly or a very slow operation.

        :type blob: :class:`google.cloud.storage.blob.Blob`
        :param blob: The blob to be renamed.

        :type new_name: str
        :param new_name: The new name for this blob.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response. The timeout applies to each individual
            request.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: :class:`Blob`
        :returns: The newly-renamed blob.
        """
        same_name = blob.name == new_name

        new_blob = self.copy_blob(blob, self, new_name, client=client, timeout=timeout)

        if not same_name:
            blob.delete(client=client, timeout=timeout)

        return new_blob

    @property
    def cors(self):
        """Retrieve or set CORS policies configured for this bucket.

        See http://www.w3.org/TR/cors/ and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        .. note::

           The getter for this property returns a list which contains
           *copies* of the bucket's CORS policy mappings.  Mutating the list
           or one of its dicts has no effect unless you then re-assign the
           dict via the setter.  E.g.:

           >>> policies = bucket.cors
           >>> policies.append({'origin': '/foo', ...})
           >>> policies[1]['maxAgeSeconds'] = 3600
           >>> del policies[0]
           >>> bucket.cors = policies
           >>> bucket.update()

        :setter: Set CORS policies for this bucket.
        :getter: Gets the CORS policies for this bucket.

        :rtype: list of dictionaries
        :returns: A sequence of mappings describing each CORS policy.
        """
        return [copy.deepcopy(policy) for policy in self._properties.get("cors", ())]

    @cors.setter
    def cors(self, entries):
        """Set CORS policies configured for this bucket.

        See http://www.w3.org/TR/cors/ and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :type entries: list of dictionaries
        :param entries: A sequence of mappings describing each CORS policy.
        """
        self._patch_property("cors", entries)

    default_event_based_hold = _scalar_property("defaultEventBasedHold")
    """Are uploaded objects automatically placed under an even-based hold?

    If True, uploaded objects will be placed under an event-based hold to
    be released at a future time. When released an object will then begin
    the retention period determined by the policy retention period for the
    object bucket.

    See https://cloud.google.com/storage/docs/json_api/v1/buckets

    If the property is not set locally, returns ``None``.

    :rtype: bool or ``NoneType``
    """

    @property
    def default_kms_key_name(self):
        """Retrieve / set default KMS encryption key for objects in the bucket.

        See https://cloud.google.com/storage/docs/json_api/v1/buckets

        :setter: Set default KMS encryption key for items in this bucket.
        :getter: Get default KMS encryption key for items in this bucket.

        :rtype: str
        :returns: Default KMS encryption key, or ``None`` if not set.
        """
        encryption_config = self._properties.get("encryption", {})
        return encryption_config.get("defaultKmsKeyName")

    @default_kms_key_name.setter
    def default_kms_key_name(self, value):
        """Set default KMS encryption key for objects in the bucket.

        :type value: str or None
        :param value: new KMS key name (None to clear any existing key).
        """
        encryption_config = self._properties.get("encryption", {})
        encryption_config["defaultKmsKeyName"] = value
        self._patch_property("encryption", encryption_config)

    @property
    def labels(self):
        """Retrieve or set labels assigned to this bucket.

        See
        https://cloud.google.com/storage/docs/json_api/v1/buckets#labels

        .. note::

           The getter for this property returns a dict which is a *copy*
           of the bucket's labels.  Mutating that dict has no effect unless
           you then re-assign the dict via the setter.  E.g.:

           >>> labels = bucket.labels
           >>> labels['new_key'] = 'some-label'
           >>> del labels['old_key']
           >>> bucket.labels = labels
           >>> bucket.update()

        :setter: Set labels for this bucket.
        :getter: Gets the labels for this bucket.

        :rtype: :class:`dict`
        :returns: Name-value pairs (string->string) labelling the bucket.
        """
        labels = self._properties.get("labels")
        if labels is None:
            return {}
        return copy.deepcopy(labels)

    @labels.setter
    def labels(self, mapping):
        """Set labels assigned to this bucket.

        See
        https://cloud.google.com/storage/docs/json_api/v1/buckets#labels

        :type mapping: :class:`dict`
        :param mapping: Name-value pairs (string->string) labelling the bucket.
        """
        # If any labels have been expressly removed, we need to track this
        # so that a future .patch() call can do the correct thing.
        existing = set([k for k in self.labels.keys()])
        incoming = set([k for k in mapping.keys()])
        self._label_removals = self._label_removals.union(existing.difference(incoming))
        mapping = {k: str(v) for k, v in mapping.items()}

        # Actually update the labels on the object.
        self._patch_property("labels", copy.deepcopy(mapping))

    @property
    def etag(self):
        """Retrieve the ETag for the bucket.

        See https://tools.ietf.org/html/rfc2616#section-3.11 and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: str or ``NoneType``
        :returns: The bucket etag or ``None`` if the bucket's
                  resource has not been loaded from the server.
        """
        return self._properties.get("etag")

    @property
    def id(self):
        """Retrieve the ID for the bucket.

        See https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: str or ``NoneType``
        :returns: The ID of the bucket or ``None`` if the bucket's
                  resource has not been loaded from the server.
        """
        return self._properties.get("id")

    @property
    def iam_configuration(self):
        """Retrieve IAM configuration for this bucket.

        :rtype: :class:`IAMConfiguration`
        :returns: an instance for managing the bucket's IAM configuration.
        """
        info = self._properties.get("iamConfiguration", {})
        return IAMConfiguration.from_api_repr(info, self)

    @property
    def lifecycle_rules(self):
        """Retrieve or set lifecycle rules configured for this bucket.

        See https://cloud.google.com/storage/docs/lifecycle and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        .. note::

           The getter for this property returns a list which contains
           *copies* of the bucket's lifecycle rules mappings.  Mutating the
           list or one of its dicts has no effect unless you then re-assign
           the dict via the setter.  E.g.:

           >>> rules = bucket.lifecycle_rules
           >>> rules.append({'origin': '/foo', ...})
           >>> rules[1]['rule']['action']['type'] = 'Delete'
           >>> del rules[0]
           >>> bucket.lifecycle_rules = rules
           >>> bucket.update()

        :setter: Set lifestyle rules for this bucket.
        :getter: Gets the lifestyle rules for this bucket.

        :rtype: generator(dict)
        :returns: A sequence of mappings describing each lifecycle rule.
        """
        info = self._properties.get("lifecycle", {})
        for rule in info.get("rule", ()):
            action_type = rule["action"]["type"]
            if action_type == "Delete":
                yield LifecycleRuleDelete.from_api_repr(rule)
            elif action_type == "SetStorageClass":
                yield LifecycleRuleSetStorageClass.from_api_repr(rule)
            else:
                raise ValueError("Unknown lifecycle rule: {}".format(rule))

    @lifecycle_rules.setter
    def lifecycle_rules(self, rules):
        """Set lifestyle rules configured for this bucket.

        See https://cloud.google.com/storage/docs/lifecycle and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :type entries: list of dictionaries
        :param entries: A sequence of mappings describing each lifecycle rule.
        """
        rules = [dict(rule) for rule in rules]  # Convert helpers if needed
        self._patch_property("lifecycle", {"rule": rules})

    def clear_lifecyle_rules(self):
        """Set lifestyle rules configured for this bucket.

        See https://cloud.google.com/storage/docs/lifecycle and
             https://cloud.google.com/storage/docs/json_api/v1/buckets
        """
        self.lifecycle_rules = []

    def add_lifecycle_delete_rule(self, **kw):
        """Add a "delete" rule to lifestyle rules configured for this bucket.

        See https://cloud.google.com/storage/docs/lifecycle and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        .. literalinclude:: snippets.py
          :start-after: [START add_lifecycle_delete_rule]
          :end-before: [END add_lifecycle_delete_rule]

        :type kw: dict
        :params kw: arguments passed to :class:`LifecycleRuleConditions`.
        """
        rules = list(self.lifecycle_rules)
        rules.append(LifecycleRuleDelete(**kw))
        self.lifecycle_rules = rules

    def add_lifecycle_set_storage_class_rule(self, storage_class, **kw):
        """Add a "delete" rule to lifestyle rules configured for this bucket.

        See https://cloud.google.com/storage/docs/lifecycle and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        .. literalinclude:: snippets.py
          :start-after: [START add_lifecycle_set_storage_class_rule]
          :end-before: [END add_lifecycle_set_storage_class_rule]

        :type storage_class: str, one of :attr:`STORAGE_CLASSES`.
        :param storage_class: new storage class to assign to matching items.

        :type kw: dict
        :params kw: arguments passed to :class:`LifecycleRuleConditions`.
        """
        rules = list(self.lifecycle_rules)
        rules.append(LifecycleRuleSetStorageClass(storage_class, **kw))
        self.lifecycle_rules = rules

    _location = _scalar_property("location")

    @property
    def location(self):
        """Retrieve location configured for this bucket.

        See https://cloud.google.com/storage/docs/json_api/v1/buckets and
        https://cloud.google.com/storage/docs/bucket-locations

        Returns ``None`` if the property has not been set before creation,
        or if the bucket's resource has not been loaded from the server.
        :rtype: str or ``NoneType``
        """
        return self._location

    @location.setter
    def location(self, value):
        """(Deprecated) Set `Bucket.location`

        This can only be set at bucket **creation** time.

        See https://cloud.google.com/storage/docs/json_api/v1/buckets and
        https://cloud.google.com/storage/docs/bucket-locations

        .. warning::

            Assignment to 'Bucket.location' is deprecated, as it is only
            valid before the bucket is created. Instead, pass the location
            to `Bucket.create`.
        """
        warnings.warn(_LOCATION_SETTER_MESSAGE, DeprecationWarning, stacklevel=2)
        self._location = value

    @property
    def location_type(self):
        """Retrieve or set the location type for the bucket.

        See https://cloud.google.com/storage/docs/storage-classes

        :setter: Set the location type for this bucket.
        :getter: Gets the the location type for this bucket.

        :rtype: str or ``NoneType``
        :returns:
            If set, one of
            :attr:`~google.cloud.storage.constants.MULTI_REGION_LOCATION_TYPE`,
            :attr:`~google.cloud.storage.constants.REGION_LOCATION_TYPE`, or
            :attr:`~google.cloud.storage.constants.DUAL_REGION_LOCATION_TYPE`,
            else ``None``.
        """
        return self._properties.get("locationType")

    def get_logging(self):
        """Return info about access logging for this bucket.

        See https://cloud.google.com/storage/docs/access-logs#status

        :rtype: dict or None
        :returns: a dict w/ keys, ``logBucket`` and ``logObjectPrefix``
                  (if logging is enabled), or None (if not).
        """
        info = self._properties.get("logging")
        return copy.deepcopy(info)

    def enable_logging(self, bucket_name, object_prefix=""):
        """Enable access logging for this bucket.

        See https://cloud.google.com/storage/docs/access-logs

        :type bucket_name: str
        :param bucket_name: name of bucket in which to store access logs

        :type object_prefix: str
        :param object_prefix: prefix for access log filenames
        """
        info = {"logBucket": bucket_name, "logObjectPrefix": object_prefix}
        self._patch_property("logging", info)

    def disable_logging(self):
        """Disable access logging for this bucket.

        See https://cloud.google.com/storage/docs/access-logs#disabling
        """
        self._patch_property("logging", None)

    @property
    def metageneration(self):
        """Retrieve the metageneration for the bucket.

        See https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: int or ``NoneType``
        :returns: The metageneration of the bucket or ``None`` if the bucket's
                  resource has not been loaded from the server.
        """
        metageneration = self._properties.get("metageneration")
        if metageneration is not None:
            return int(metageneration)

    @property
    def owner(self):
        """Retrieve info about the owner of the bucket.

        See https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: dict or ``NoneType``
        :returns: Mapping of owner's role/ID. Returns ``None`` if the bucket's
                  resource has not been loaded from the server.
        """
        return copy.deepcopy(self._properties.get("owner"))

    @property
    def project_number(self):
        """Retrieve the number of the project to which the bucket is assigned.

        See https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: int or ``NoneType``
        :returns: The project number that owns the bucket or ``None`` if
                  the bucket's resource has not been loaded from the server.
        """
        project_number = self._properties.get("projectNumber")
        if project_number is not None:
            return int(project_number)

    @property
    def retention_policy_effective_time(self):
        """Retrieve the effective time of the bucket's retention policy.

        :rtype: datetime.datetime or ``NoneType``
        :returns: point-in time at which the bucket's retention policy is
                  effective, or ``None`` if the property is not
                  set locally.
        """
        policy = self._properties.get("retentionPolicy")
        if policy is not None:
            timestamp = policy.get("effectiveTime")
            if timestamp is not None:
                return _rfc3339_to_datetime(timestamp)

    @property
    def retention_policy_locked(self):
        """Retrieve whthere the bucket's retention policy is locked.

        :rtype: bool
        :returns: True if the bucket's policy is locked, or else False
                  if the policy is not locked, or the property is not
                  set locally.
        """
        policy = self._properties.get("retentionPolicy")
        if policy is not None:
            return policy.get("isLocked")

    @property
    def retention_period(self):
        """Retrieve or set the retention period for items in the bucket.

        :rtype: int or ``NoneType``
        :returns: number of seconds to retain items after upload or release
                  from event-based lock, or ``None`` if the property is not
                  set locally.
        """
        policy = self._properties.get("retentionPolicy")
        if policy is not None:
            period = policy.get("retentionPeriod")
            if period is not None:
                return int(period)

    @retention_period.setter
    def retention_period(self, value):
        """Set the retention period for items in the bucket.

        :type value: int
        :param value:
            number of seconds to retain items after upload or release from
            event-based lock.

        :raises ValueError: if the bucket's retention policy is locked.
        """
        policy = self._properties.setdefault("retentionPolicy", {})
        if value is not None:
            policy["retentionPeriod"] = str(value)
        else:
            policy = None
        self._patch_property("retentionPolicy", policy)

    @property
    def self_link(self):
        """Retrieve the URI for the bucket.

        See https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: str or ``NoneType``
        :returns: The self link for the bucket or ``None`` if
                  the bucket's resource has not been loaded from the server.
        """
        return self._properties.get("selfLink")

    @property
    def storage_class(self):
        """Retrieve or set the storage class for the bucket.

        See https://cloud.google.com/storage/docs/storage-classes

        :setter: Set the storage class for this bucket.
        :getter: Gets the the storage class for this bucket.

        :rtype: str or ``NoneType``
        :returns:
            If set, one of
            :attr:`~google.cloud.storage.constants.NEARLINE_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.COLDLINE_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.ARCHIVE_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.STANDARD_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.MULTI_REGIONAL_LEGACY_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.REGIONAL_LEGACY_STORAGE_CLASS`,
            or
            :attr:`~google.cloud.storage.constants.DURABLE_REDUCED_AVAILABILITY_LEGACY_STORAGE_CLASS`,
            else ``None``.
        """
        return self._properties.get("storageClass")

    @storage_class.setter
    def storage_class(self, value):
        """Set the storage class for the bucket.

        See https://cloud.google.com/storage/docs/storage-classes

        :type value: str
        :param value:
            One of
            :attr:`~google.cloud.storage.constants.NEARLINE_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.COLDLINE_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.ARCHIVE_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.STANDARD_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.MULTI_REGIONAL_LEGACY_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.REGIONAL_LEGACY_STORAGE_CLASS`,
            or
            :attr:`~google.cloud.storage.constants.DURABLE_REDUCED_AVAILABILITY_LEGACY_STORAGE_CLASS`,
        """
        if value not in self.STORAGE_CLASSES:
            raise ValueError("Invalid storage class: %s" % (value,))
        self._patch_property("storageClass", value)

    @property
    def time_created(self):
        """Retrieve the timestamp at which the bucket was created.

        See https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from RFC3339 valid timestamp, or
                  ``None`` if the bucket's resource has not been loaded
                  from the server.
        """
        value = self._properties.get("timeCreated")
        if value is not None:
            return _rfc3339_to_datetime(value)

    @property
    def versioning_enabled(self):
        """Is versioning enabled for this bucket?

        See  https://cloud.google.com/storage/docs/object-versioning for
        details.

        :setter: Update whether versioning is enabled for this bucket.
        :getter: Query whether versioning is enabled for this bucket.

        :rtype: bool
        :returns: True if enabled, else False.
        """
        versioning = self._properties.get("versioning", {})
        return versioning.get("enabled", False)

    @versioning_enabled.setter
    def versioning_enabled(self, value):
        """Enable versioning for this bucket.

        See  https://cloud.google.com/storage/docs/object-versioning for
        details.

        :type value: convertible to boolean
        :param value: should versioning be enabled for the bucket?
        """
        self._patch_property("versioning", {"enabled": bool(value)})

    @property
    def requester_pays(self):
        """Does the requester pay for API requests for this bucket?

        See https://cloud.google.com/storage/docs/requester-pays for
        details.

        :setter: Update whether requester pays for this bucket.
        :getter: Query whether requester pays for this bucket.

        :rtype: bool
        :returns: True if requester pays for API requests for the bucket,
                  else False.
        """
        versioning = self._properties.get("billing", {})
        return versioning.get("requesterPays", False)

    @requester_pays.setter
    def requester_pays(self, value):
        """Update whether requester pays for API requests for this bucket.

        See  https://cloud.google.com/storage/docs/<DOCS-MISSING> for
        details.

        :type value: convertible to boolean
        :param value: should requester pay for API requests for the bucket?
        """
        self._patch_property("billing", {"requesterPays": bool(value)})

    def configure_website(self, main_page_suffix=None, not_found_page=None):
        """Configure website-related properties.

        See https://cloud.google.com/storage/docs/hosting-static-website

        .. note::
          This (apparently) only works
          if your bucket name is a domain name
          (and to do that, you need to get approved somehow...).

        If you want this bucket to host a website, just provide the name
        of an index page and a page to use when a blob isn't found:

        .. literalinclude:: snippets.py
          :start-after: [START configure_website]
          :end-before: [END configure_website]

        You probably should also make the whole bucket public:

        .. literalinclude:: snippets.py
            :start-after: [START make_public]
            :end-before: [END make_public]

        This says: "Make the bucket public, and all the stuff already in
        the bucket, and anything else I add to the bucket.  Just make it
        all public."

        :type main_page_suffix: str
        :param main_page_suffix: The page to use as the main page
                                 of a directory.
                                 Typically something like index.html.

        :type not_found_page: str
        :param not_found_page: The file to use when a page isn't found.
        """
        data = {"mainPageSuffix": main_page_suffix, "notFoundPage": not_found_page}
        self._patch_property("website", data)

    def disable_website(self):
        """Disable the website configuration for this bucket.

        This is really just a shortcut for setting the website-related
        attributes to ``None``.
        """
        return self.configure_website(None, None)

    def get_iam_policy(
        self, client=None, requested_policy_version=None, timeout=_DEFAULT_TIMEOUT
    ):
        """Retrieve the IAM policy for the bucket.

        See
        https://cloud.google.com/storage/docs/json_api/v1/buckets/getIamPolicy

        If :attr:`user_project` is set, bills the API request to that project.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :type requested_policy_version: int or ``NoneType``
        :param requested_policy_version: Optional. The version of IAM policies to request.
                                         If a policy with a condition is requested without
                                         setting this, the server will return an error.
                                         This must be set to a value of 3 to retrieve IAM
                                         policies containing conditions. This is to prevent
                                         client code that isn't aware of IAM conditions from
                                         interpreting and modifying policies incorrectly.
                                         The service might return a policy with version lower
                                         than the one that was requested, based on the
                                         feature syntax in the policy fetched.

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: :class:`google.api_core.iam.Policy`
        :returns: the policy instance, based on the resource returned from
                  the ``getIamPolicy`` API request.

        Example:

        .. code-block:: python

           from google.cloud.storage.iam import STORAGE_OBJECT_VIEWER_ROLE

           policy = bucket.get_iam_policy(requested_policy_version=3)

           policy.version = 3

           # Add a binding to the policy via it's bindings property
           policy.bindings.append({
               "role": STORAGE_OBJECT_VIEWER_ROLE,
               "members": {"serviceAccount:account@project.iam.gserviceaccount.com", ...},
               # Optional:
               "condition": {
                   "title": "prefix"
                   "description": "Objects matching prefix"
                   "expression": "resource.name.startsWith(\"projects/project-name/buckets/bucket-name/objects/prefix\")"
               }
           })

           bucket.set_iam_policy(policy)
        """
        client = self._require_client(client)
        query_params = {}

        if self.user_project is not None:
            query_params["userProject"] = self.user_project

        if requested_policy_version is not None:
            query_params["optionsRequestedPolicyVersion"] = requested_policy_version

        info = client._connection.api_request(
            method="GET",
            path="%s/iam" % (self.path,),
            query_params=query_params,
            _target_object=None,
            timeout=timeout,
        )
        return Policy.from_api_repr(info)

    def set_iam_policy(self, policy, client=None, timeout=_DEFAULT_TIMEOUT):
        """Update the IAM policy for the bucket.

        See
        https://cloud.google.com/storage/docs/json_api/v1/buckets/setIamPolicy

        If :attr:`user_project` is set, bills the API request to that project.

        :type policy: :class:`google.api_core.iam.Policy`
        :param policy: policy instance used to update bucket's IAM policy.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: :class:`google.api_core.iam.Policy`
        :returns: the policy instance, based on the resource returned from
                  the ``setIamPolicy`` API request.
        """
        client = self._require_client(client)
        query_params = {}

        if self.user_project is not None:
            query_params["userProject"] = self.user_project

        resource = policy.to_api_repr()
        resource["resourceId"] = self.path
        info = client._connection.api_request(
            method="PUT",
            path="%s/iam" % (self.path,),
            query_params=query_params,
            data=resource,
            _target_object=None,
            timeout=timeout,
        )
        return Policy.from_api_repr(info)

    def test_iam_permissions(self, permissions, client=None, timeout=_DEFAULT_TIMEOUT):
        """API call:  test permissions

        See
        https://cloud.google.com/storage/docs/json_api/v1/buckets/testIamPermissions

        If :attr:`user_project` is set, bills the API request to that project.

        :type permissions: list of string
        :param permissions: the permissions to check

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: list of string
        :returns: the permissions returned by the ``testIamPermissions`` API
                  request.
        """
        client = self._require_client(client)
        query_params = {"permissions": permissions}

        if self.user_project is not None:
            query_params["userProject"] = self.user_project

        path = "%s/iam/testPermissions" % (self.path,)
        resp = client._connection.api_request(
            method="GET", path=path, query_params=query_params, timeout=timeout
        )
        return resp.get("permissions", [])

    def make_public(
        self, recursive=False, future=False, client=None, timeout=_DEFAULT_TIMEOUT
    ):
        """Update bucket's ACL, granting read access to anonymous users.

        :type recursive: bool
        :param recursive: If True, this will make all blobs inside the bucket
                          public as well.

        :type future: bool
        :param future: If True, this will make all objects created in the
                       future public as well.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.
        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response. The timeout applies to each underlying
            request.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :raises ValueError:
            If ``recursive`` is True, and the bucket contains more than 256
            blobs.  This is to prevent extremely long runtime of this
            method.  For such buckets, iterate over the blobs returned by
            :meth:`list_blobs` and call
            :meth:`~google.cloud.storage.blob.Blob.make_public`
            for each blob.
        """
        self.acl.all().grant_read()
        self.acl.save(client=client, timeout=timeout)

        if future:
            doa = self.default_object_acl
            if not doa.loaded:
                doa.reload(client=client, timeout=timeout)
            doa.all().grant_read()
            doa.save(client=client, timeout=timeout)

        if recursive:
            blobs = list(
                self.list_blobs(
                    projection="full",
                    max_results=self._MAX_OBJECTS_FOR_ITERATION + 1,
                    client=client,
                    timeout=timeout,
                )
            )
            if len(blobs) > self._MAX_OBJECTS_FOR_ITERATION:
                message = (
                    "Refusing to make public recursively with more than "
                    "%d objects. If you actually want to make every object "
                    "in this bucket public, iterate through the blobs "
                    "returned by 'Bucket.list_blobs()' and call "
                    "'make_public' on each one."
                ) % (self._MAX_OBJECTS_FOR_ITERATION,)
                raise ValueError(message)

            for blob in blobs:
                blob.acl.all().grant_read()
                blob.acl.save(client=client, timeout=timeout)

    def make_private(
        self, recursive=False, future=False, client=None, timeout=_DEFAULT_TIMEOUT
    ):
        """Update bucket's ACL, revoking read access for anonymous users.

        :type recursive: bool
        :param recursive: If True, this will make all blobs inside the bucket
                          private as well.

        :type future: bool
        :param future: If True, this will make all objects created in the
                       future private as well.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response. The timeout applies to each underlying
            request.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :raises ValueError:
            If ``recursive`` is True, and the bucket contains more than 256
            blobs.  This is to prevent extremely long runtime of this
            method.  For such buckets, iterate over the blobs returned by
            :meth:`list_blobs` and call
            :meth:`~google.cloud.storage.blob.Blob.make_private`
            for each blob.
        """
        self.acl.all().revoke_read()
        self.acl.save(client=client, timeout=timeout)

        if future:
            doa = self.default_object_acl
            if not doa.loaded:
                doa.reload(client=client, timeout=timeout)
            doa.all().revoke_read()
            doa.save(client=client, timeout=timeout)

        if recursive:
            blobs = list(
                self.list_blobs(
                    projection="full",
                    max_results=self._MAX_OBJECTS_FOR_ITERATION + 1,
                    client=client,
                    timeout=timeout,
                )
            )
            if len(blobs) > self._MAX_OBJECTS_FOR_ITERATION:
                message = (
                    "Refusing to make private recursively with more than "
                    "%d objects. If you actually want to make every object "
                    "in this bucket private, iterate through the blobs "
                    "returned by 'Bucket.list_blobs()' and call "
                    "'make_private' on each one."
                ) % (self._MAX_OBJECTS_FOR_ITERATION,)
                raise ValueError(message)

            for blob in blobs:
                blob.acl.all().revoke_read()
                blob.acl.save(client=client, timeout=timeout)

    def generate_upload_policy(self, conditions, expiration=None, client=None):
        """Create a signed upload policy for uploading objects.

        This method generates and signs a policy document. You can use
        `policy documents`_ to allow visitors to a website to upload files to
        Google Cloud Storage without giving them direct write access.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START policy_document]
            :end-before: [END policy_document]

        .. _policy documents:
            https://cloud.google.com/storage/docs/xml-api\
            /post-object#policydocument

        :type expiration: datetime
        :param expiration: Optional expiration in UTC. If not specified, the
                           policy will expire in 1 hour.

        :type conditions: list
        :param conditions: A list of conditions as described in the
                          `policy documents`_ documentation.

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :rtype: dict
        :returns: A dictionary of (form field name, form field value) of form
                  fields that should be added to your HTML upload form in order
                  to attach the signature.
        """
        client = self._require_client(client)
        credentials = client._base_connection.credentials
        _signing.ensure_signed_credentials(credentials)

        if expiration is None:
            expiration = _NOW() + datetime.timedelta(hours=1)

        conditions = conditions + [{"bucket": self.name}]

        policy_document = {
            "expiration": _datetime_to_rfc3339(expiration),
            "conditions": conditions,
        }

        encoded_policy_document = base64.b64encode(
            json.dumps(policy_document).encode("utf-8")
        )
        signature = base64.b64encode(credentials.sign_bytes(encoded_policy_document))

        fields = {
            "bucket": self.name,
            "GoogleAccessId": credentials.signer_email,
            "policy": encoded_policy_document.decode("utf-8"),
            "signature": signature.decode("utf-8"),
        }

        return fields

    def lock_retention_policy(self, client=None, timeout=_DEFAULT_TIMEOUT):
        """Lock the bucket's retention policy.

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :raises ValueError:
            if the bucket has no metageneration (i.e., new or never reloaded);
            if the bucket has no retention policy assigned;
            if the bucket's retention policy is already locked.
        """
        if "metageneration" not in self._properties:
            raise ValueError("Bucket has no retention policy assigned: try 'reload'?")

        policy = self._properties.get("retentionPolicy")

        if policy is None:
            raise ValueError("Bucket has no retention policy assigned: try 'reload'?")

        if policy.get("isLocked"):
            raise ValueError("Bucket's retention policy is already locked.")

        client = self._require_client(client)

        query_params = {"ifMetagenerationMatch": self.metageneration}

        if self.user_project is not None:
            query_params["userProject"] = self.user_project

        path = "/b/{}/lockRetentionPolicy".format(self.name)
        api_response = client._connection.api_request(
            method="POST",
            path=path,
            query_params=query_params,
            _target_object=self,
            timeout=timeout,
        )
        self._set_properties(api_response)

    def generate_signed_url(
        self,
        expiration=None,
        api_access_endpoint=_API_ACCESS_ENDPOINT,
        method="GET",
        headers=None,
        query_parameters=None,
        client=None,
        credentials=None,
        version=None,
    ):
        """Generates a signed URL for this bucket.

        .. note::

            If you are on Google Compute Engine, you can't generate a signed
            URL using GCE service account. Follow `Issue 50`_ for updates on
            this. If you'd like to be able to generate a signed URL from GCE,
            you can use a standard service account from a JSON file rather
            than a GCE service account.

        .. _Issue 50: https://github.com/GoogleCloudPlatform/\
                      google-auth-library-python/issues/50

        If you have a bucket that you want to allow access to for a set
        amount of time, you can use this method to generate a URL that
        is only valid within a certain time period.

        This is particularly useful if you don't want publicly
        accessible buckets, but don't want to require users to explicitly
        log in.

        :type expiration: Union[Integer, datetime.datetime, datetime.timedelta]
        :param expiration: Point in time when the signed URL should expire.

        :type api_access_endpoint: str
        :param api_access_endpoint: Optional URI base.

        :type method: str
        :param method: The HTTP verb that will be used when requesting the URL.

        :type headers: dict
        :param headers:
            (Optional) Additional HTTP headers to be included as part of the
            signed URLs.  See:
            https://cloud.google.com/storage/docs/xml-api/reference-headers
            Requests using the signed URL *must* pass the specified header
            (name and value) with each request for the URL.

        :type query_parameters: dict
        :param query_parameters:
            (Optional) Additional query paramtersto be included as part of the
            signed URLs.  See:
            https://cloud.google.com/storage/docs/xml-api/reference-headers#query

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.


        :type credentials: :class:`google.auth.credentials.Credentials` or
                           :class:`NoneType`
        :param credentials: The authorization credentials to attach to requests.
                            These credentials identify this application to the service.
                            If none are specified, the client will attempt to ascertain
                            the credentials from the environment.

        :type version: str
        :param version: (Optional) The version of signed credential to create.
                        Must be one of 'v2' | 'v4'.

        :raises: :exc:`ValueError` when version is invalid.
        :raises: :exc:`TypeError` when expiration is not a valid type.
        :raises: :exc:`AttributeError` if credentials is not an instance
                of :class:`google.auth.credentials.Signing`.

        :rtype: str
        :returns: A signed URL you can use to access the resource
                  until expiration.
        """
        if version is None:
            version = "v2"
        elif version not in ("v2", "v4"):
            raise ValueError("'version' must be either 'v2' or 'v4'")

        resource = "/{bucket_name}".format(bucket_name=self.name)

        if credentials is None:
            client = self._require_client(client)
            credentials = client._credentials

        if version == "v2":
            helper = generate_signed_url_v2
        else:
            helper = generate_signed_url_v4

        return helper(
            credentials,
            resource=resource,
            expiration=expiration,
            api_access_endpoint=api_access_endpoint,
            method=method.upper(),
            headers=headers,
            query_parameters=query_parameters,
        )
