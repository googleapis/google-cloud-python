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

"""Helper functions for shared behavior."""

import re

from gcloud._helpers import _name_from_project_path


_TOPIC_TEMPLATE = re.compile(r"""
    projects/            # static prefix
    (?P<project>[^/]+)   # initial letter, wordchars + hyphen
    /topics/             # static midfix
    (?P<name>[^/]+)      # initial letter, wordchars + allowed punc
""", re.VERBOSE)


_SUBSCRIPTION_TEMPLATE = re.compile(r"""
    projects/            # static prefix
    (?P<project>[^/]+)   # initial letter, wordchars + hyphen
    /subscriptions/      # static midfix
    (?P<name>[^/]+)      # initial letter, wordchars + allowed punc
""", re.VERBOSE)


def topic_name_from_path(path, project):
    """Validate a topic URI path and get the topic name.

    :type path: string
    :param path: URI path for a topic API request.

    :type project: string
    :param project: The project associated with the request. It is
                    included for validation purposes.

    :rtype: string
    :returns: Topic name parsed from ``path``.
    :raises: :class:`ValueError` if the ``path`` is ill-formed or if
             the project from the ``path`` does not agree with the
             ``project`` passed in.
    """
    return _name_from_project_path(path, project, _TOPIC_TEMPLATE)


def subscription_name_from_path(path, project):
    """Validate a subscription URI path and get the subscription name.

    :type path: string
    :param path: URI path for a subscription API request.

    :type project: string
    :param project: The project associated with the request. It is
                    included for validation purposes.

    :rtype: string
    :returns: subscription name parsed from ``path``.
    :raises: :class:`ValueError` if the ``path`` is ill-formed or if
             the project from the ``path`` does not agree with the
             ``project`` passed in.
    """
    return _name_from_project_path(path, project, _SUBSCRIPTION_TEMPLATE)
