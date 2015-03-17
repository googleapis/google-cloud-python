# Copyright 2015 Google Inc. All rights reserved.
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

Allows the storage package to infer the current project, default bucket
and connection from the enviroment.
"""


import os

from gcloud._helpers import _lazy_property_deco


_PROJECT_ENV_VAR_NAME = 'GCLOUD_PROJECT'


def _get_production_project():
    """Gets the production project if it can be inferred."""
    return os.getenv(_PROJECT_ENV_VAR_NAME)


def _determine_default_project(project=None):
    """Determine default project ID explicitly or implicitly as fall-back.

    In implicit case, currently only supports enviroment variable but will
    support App Engine, Compute Engine and other environments in the future.

    Local environment variable used is:
    - GCLOUD_PROJECT

    :type project: string
    :param project: Optional. The project name to use as default.

    :rtype: string or ``NoneType``
    :returns: Default project if it can be determined.
    """
    if project is None:
        project = _get_production_project()

    return project


def set_default_project(project=None):
    """Set default project either explicitly or implicitly as fall-back.

    :type project: string
    :param project: Optional. The project name to use as default.

    :raises: :class:`EnvironmentError` if no project was found.
    """
    project = _determine_default_project(project=project)
    if project is not None:
        _DEFAULTS.project = project
    else:
        raise EnvironmentError('No project could be inferred.')


class _DefaultsContainer(object):
    """Container for defaults.

    :type project: string
    :param project: Persistent implied project from environment.

    :type bucket: :class:`gcloud.storage.bucket.Bucket`
    :param bucket: Persistent implied default bucket from environment.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: Persistent implied connection from environment.
    """

    @_lazy_property_deco
    @staticmethod
    def project():
        """Return the implicit default project."""
        return _determine_default_project()

    def __init__(self, project=None, bucket=None, connection=None,
                 implicit=False):
        if project is not None or not implicit:
            self.project = project
        self.bucket = bucket
        self.connection = connection


def get_default_project():
    """Get default project.

    :rtype: string or ``NoneType``
    :returns: The default project if one has been set.
    """
    return _DEFAULTS.project


def get_default_bucket():
    """Get default bucket.

    :rtype: :class:`gcloud.storage.bucket.Bucket` or ``NoneType``
    :returns: The default bucket if one has been set.
    """
    return _DEFAULTS.bucket


def get_default_connection():
    """Get default connection.

    :rtype: :class:`gcloud.storage.connection.Connection` or ``NoneType``
    :returns: The default connection if one has been set.
    """
    return _DEFAULTS.connection


_DEFAULTS = _DefaultsContainer(implicit=True)
