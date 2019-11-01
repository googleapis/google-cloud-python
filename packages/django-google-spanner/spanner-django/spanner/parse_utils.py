# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured

def resolve_project_id(project_id):
    if project_id == 'DEFAULT_PROJECT_ID' or not project_id:
        # Resolve it from the environment.
        raise ImproperlyConfigured(
                'Cannot yet resolve the project_id from the environment')
    else:
        return project_id


def parse_spanner_url(spanner_url):
    # cloudspanner:[//host[:port]]/projects/<project-id>/instances/<instance-id>/databases/<database-name>[?property-name=property-value[;]]*
    #
    # Examples:
    # cloudspanner://spanner.googleapis.com/projects/test-project-012345/instances/test-instance/databases/dev-db
    if not spanner_url:
        raise ImproperlyConfigured('expecting a non-blank spanner_url')

    o = urlparse(spanner_url or '')
    if o.scheme == '':
        raise ImproperlyConfigured('expecting cloudspanner as the scheme')

    if o.scheme != 'cloudspanner':
        raise ImproperlyConfigured('invalid scheme {got}, expected {want}'.format(
                                    got=o.scheme, want='cloudspanner'))

    properties = parse_properties(o.query)
    projectid_instance_dbname = parse_projectid_instance_dbname(o.path)

    combined = dict(host=o.netloc)

    maps = [properties, projectid_instance_dbname]
    for amap in maps:
        if not amap:
            continue

        for k, v in amap.items():
            combined[k] = v

    return combined


def parse_properties(kv_pairs, sep=';'):
    if kv_pairs == '':
        return None

    splits = kv_pairs.split(sep)

    kvp = {}
    for kv_str in splits:
        kvs = kv_str.split('=')
        if len(kvs) == 1:
            kvp[kvs[0]] = None
        elif len(kvs) == 2:
            kvp[kvs[0]] = kvs[1]
        else:
            kvp[kvs[0]] = kvs[1:]

    return kvp


rePROJECTID_INSTANCE_DBNAME = re.compile(
        '/projects/([^/]+)/instances/([^/]+)/databases/([^/]+)$', re.UNICODE)


def parse_projectid_instance_dbname(url_path):
    matches = rePROJECTID_INSTANCE_DBNAME.findall(url_path)
    if len(matches) != 1:
        raise ImproperlyConfigured('%s does not match pattern %s' % (
                        url_path, rePROJECTID_INSTANCE_DBNAME.pattern))

    head = matches[0]
    g, w = len(head), rePROJECTID_INSTANCE_DBNAME.groups
    if g != w:
        raise ImproperlyConfigured('unmatched groups, got %d want %d' % (g, w))

    project_id, instance, database = head
    return dict(
            project_id=project_id,
            instance=instance,
            database=database,
    )


def extract_connection_params(settings_dict):
        # We'll expect settings in the form of either:
        # {
        #   "NAME":         "spanner",
        #   "INSTANCE":     "instance",
        #   "AUTOCOMMIT":   True or False,
        #   "READ_ONLY":    True or False,
        #   "PROJECT_ID":   "<project_id>",
        # }
        #
        # OR
        # {
        #   "SPANNER_URL":  "cloudspanner:[//host[:port]]/project/<project_id>/instances/<instance-id>/databases/<database-name>?property-name=property-value
        # }

        if settings_dict['SPANNER_URL']:
            return parse_spanner_url(settings_dict['SPANNER_URL'])
        else:
            return dict(
                auto_commit=settings_dict['AUTO_COMMIT'],
                database=settings_dict['NAME'] or 'spanner',
                instance=settings_dict['INSTANCE'],
                project_id=resolve_project_id(settings_dict['PROJECT_ID']),
                read_only=settings_dict['READ_ONLY'],
            )
