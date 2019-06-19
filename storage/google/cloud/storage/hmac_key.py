# Copyright 2019 Google LLC
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

from google.cloud.exceptions import NotFound
from google.cloud._helpers import _rfc3339_to_datetime


class HMACKeyMetadata(object):
    """Metadata about an HMAC service account key withn Cloud Storage.

    :type client: :class:`~google.cloud.stoage.client.Client`
    :param client: client associated with the key metadata.
    """

    ACTIVE_STATE = "ACTIVE"
    """Key is active, and may be used to sign requests."""
    INACTIVE_STATE = "INACTIVE"
    """Key is inactive, and may not be used to sign requests.

    It can be re-activated via :meth:`update`.
    """
    DELETED_STATE = "DELETED"
    """Key is deleted.  It cannot be re-activated."""

    _SETTABLE_STATES = (ACTIVE_STATE, INACTIVE_STATE)

    def __init__(self, client):
        self._client = client
        self._properties = {}

    @property
    def access_id(self):
        """ID of the key.

        :rtype: str or None
        :returns: unique identifier of the key within a project.
        """
        return self._properties.get("accessId")

    @property
    def etag(self):
        """ETag identifying the version of the key metadata.

        :rtype: str or None
        :returns: ETag for the version of the key's metadata.
        """
        return self._properties.get("etag")

    @property
    def project(self):
        """Project ID associated with the key.

        :rtype: str or None
        :returns: project identfier for the key.
        """
        return self._properties.get("projectId")

    @property
    def service_account_email(self):
        """Service account e-mail address associated with the key.

        :rtype: str or None
        :returns: e-mail address for the service account which created the key.
        """
        return self._properties.get("serviceAccountEmail")

    @property
    def state(self):
        """Get / set key's state.

        One of:
            - ``ACTIVE``
            - ``INACTIVE``
            - ``DELETED``

        :rtype: str or None
        :returns: key's current state.
        """
        return self._properties.get("state")

    @state.setter
    def state(self, value):
        if value not in self._SETTABLE_STATES:
            raise ValueError(
                "State may only be set to one of: {}".format(
                    ", ".join(self._SETTABLE_STATES)
                )
            )

        self._properties["state"] = value

    @property
    def time_created(self):
        """Retrieve the timestamp at which the HMAC key was created.

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from RFC3339 valid timestamp, or
                  ``None`` if the bucket's resource has not been loaded
                  from the server.
        """
        value = self._properties.get("timeCreated")
        if value is not None:
            return _rfc3339_to_datetime(value)

    @property
    def updated(self):
        """Retrieve the timestamp at which the HMAC key was created.

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from RFC3339 valid timestamp, or
                  ``None`` if the bucket's resource has not been loaded
                  from the server.
        """
        value = self._properties.get("updated")
        if value is not None:
            return _rfc3339_to_datetime(value)

    @property
    def path(self):
        """Resource path for the metadata's key."""

        if self.access_id is None:
            raise ValueError("No 'access_id' set.")

        project = self.project
        if project is None:
            project = self._client.project

        return "/projects/{}/hmacKeys/{}".format(project, self.access_id)

    def exists(self):
        """Determine whether or not the key for this metadata exists.

        :rtype: bool
        :returns: True if the key exists in Cloud Storage.
        """
        try:
            self._client._connection.api_request(method="GET", path=self.path)
        except NotFound:
            return False
        else:
            return True

    def reload(self):
        """Reload properties from Cloud Storage.

        :raises :class:`~google.api_core.exceptions.NotFound`:
            if the key does not exist on the back-end.
        """
        self._properties = self._client._connection.api_request(
            method="GET", path=self.path
        )

    def update(self):
        """Save writable properties to Cloud Storage.

        :raises :class:`~google.api_core.exceptions.NotFound`:
            if the key does not exist on the back-end.
        """
        payload = {"state": self.state}
        self._properties = self._client._connection.api_request(
            method="POST", path=self.path, data=payload
        )

    def delete(self):
        """Delete the key from Cloud Storage.

        :raises :class:`~google.api_core.exceptions.NotFound`:
            if the key does not exist on the back-end.
        """
        if self.state != self.INACTIVE_STATE:
            raise ValueError("Cannot delete key if not in 'INACTIVE' state.")

        self._client._connection.api_request(
            method="DELETE", path=self.path
        )
