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
    # PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
    path_parts = path.split('/')
    if (len(path_parts) != 4 or path_parts[0] != 'projects' or
            path_parts[2] != 'topics'):
        raise ValueError('Expected path to be of the form '
                         'projects/{project}/topics/{topic_name}')
    if (len(path_parts) != 4 or path_parts[0] != 'projects' or
            path_parts[2] != 'topics' or path_parts[1] != project):
        raise ValueError('Project from client should agree with '
                         'project from resource.')

    return path_parts[3]
