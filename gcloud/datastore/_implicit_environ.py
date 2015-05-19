# Copyright 2014 Google Inc. All rights reserved.
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

"""Module to provide implicit behavior based on enviroment.

Allows the datastore package to infer the current dataset ID and
connection from the enviroment.
"""

import os

from gcloud._helpers import _app_engine_id
from gcloud._helpers import _compute_engine_id
from gcloud._helpers import _lazy_property_deco
from gcloud.datastore.connection import Connection


_DATASET_ENV_VAR_NAME = 'GCLOUD_DATASET_ID'
_GCD_DATASET_ENV_VAR_NAME = 'DATASTORE_DATASET'


def _get_production_dataset_id():
    """Gets the production application ID if it can be inferred."""
    return os.getenv(_DATASET_ENV_VAR_NAME)


def _get_gcd_dataset_id():
    """Gets the GCD application ID if it can be inferred."""
    return os.getenv(_GCD_DATASET_ENV_VAR_NAME)


def _determine_default_dataset_id(dataset_id=None):
    """Determine default dataset ID explicitly or implicitly as fall-back.

    In implicit case, supports four environments. In order of precedence, the
    implicit environments are:

    * GCLOUD_DATASET_ID environment variable
    * DATASTORE_DATASET environment variable (for ``gcd`` testing)
    * Google App Engine application ID
    * Google Compute Engine project ID (from metadata server)

    :type dataset_id: string
    :param dataset_id: Optional. The dataset ID to use as default.

    :rtype: string or ``NoneType``
    :returns: Default dataset ID if it can be determined.
    """
    if dataset_id is None:
        dataset_id = _get_production_dataset_id()

    if dataset_id is None:
        dataset_id = _get_gcd_dataset_id()

    if dataset_id is None:
        dataset_id = _app_engine_id()

    if dataset_id is None:
        dataset_id = _compute_engine_id()

    return dataset_id


def set_default_dataset_id(dataset_id=None):
    """Set default dataset ID either explicitly or implicitly as fall-back.

    In implicit case, supports four environments. In order of precedence, the
    implicit environments are:

    * GCLOUD_DATASET_ID environment variable
    * DATASTORE_DATASET environment variable (for ``gcd`` testing)
    * Google App Engine application ID
    * Google Compute Engine project ID (from metadata server)

    :type dataset_id: string
    :param dataset_id: Optional. The dataset ID to use as default.

    :raises: :class:`EnvironmentError` if no dataset ID was implied.
    """
    dataset_id = _determine_default_dataset_id(dataset_id=dataset_id)
    if dataset_id is not None:
        _DEFAULTS.dataset_id = dataset_id
    else:
        raise EnvironmentError('No dataset ID could be inferred.')


def get_default_dataset_id():
    """Get default dataset ID.

    :rtype: string or ``NoneType``
    :returns: The default dataset ID if one has been set.
    """
    return _DEFAULTS.dataset_id


def set_default_connection(connection=None):
    """Set default connection either explicitly or implicitly as fall-back.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: A connection provided to be the default.
    """
    _DEFAULTS.connection = connection or Connection.from_environment()


def get_default_connection():
    """Get default connection.

    :rtype: :class:`gcloud.datastore.connection.Connection` or ``NoneType``
    :returns: The default connection if one has been set.
    """
    return _DEFAULTS.connection


class _DefaultsContainer(object):
    """Container for defaults.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: Persistent implied connection from environment.

    :type dataset_id: string
    :param dataset_id: Persistent implied dataset ID from environment.
    """

    @_lazy_property_deco
    @staticmethod
    def dataset_id():
        """Return the implicit default dataset ID."""
        return _determine_default_dataset_id()

    @_lazy_property_deco
    @staticmethod
    def connection():
        """Return the implicit default connection.."""
        return Connection.from_environment()

    def __init__(self, connection=None, dataset_id=None, implicit=False):
        if connection is not None or not implicit:
            self.connection = connection
        if dataset_id is not None or not implicit:
            self.dataset_id = dataset_id


_DEFAULTS = _DefaultsContainer(implicit=True)
