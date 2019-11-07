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

from .exceptions import Error


def resolve_project_id(project_id):
    if project_id == 'DEFAULT_PROJECT_ID' or not project_id:
        # Resolve it from the environment.
        raise Error(
                'Cannot yet resolve the project_id from the environment')
    else:
        return project_id


def parse_spanner_url(spanner_url):
    # cloudspanner:[//host[:port]]/projects/<project-id>/instances/<instance-id>/databases/<database-name>[?property-name=property-value[;]]*
    #
    # Examples:
    # cloudspanner://spanner.googleapis.com/projects/test-project-012345/instances/test-instance/databases/dev-db
    if not spanner_url:
        raise Error('expecting a non-blank spanner_url')

    o = urlparse(spanner_url or '')
    if o.scheme == '':
        raise Error('expecting cloudspanner as the scheme')

    if o.scheme != 'cloudspanner':
        raise Error('invalid scheme {got}, expected {want}'.format(
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

    return filter_out_unset_keys(combined)


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

    as_bools = ['autocommit', 'readonly']
    for as_bool_key in as_bools:
        value = kvp.get(as_bool_key, None)
        if value is None:
            continue

        as_bool_value = True
        if value == '1' or value == '0':
            as_bool_value = value == '1'
        elif value == 'True' or value == 'true':
            as_bool_value = True
        elif value == 'False' or value == 'False':
            as_bool_value = False

        kvp[as_bool_key] = as_bool_value

    return kvp


rePROJECTID_INSTANCE_DBNAME = re.compile(
        '/projects/([^/]+)/instances/([^/]+)/databases/([^/]+)$', re.UNICODE)


def parse_projectid_instance_dbname(url_path):
    matches = rePROJECTID_INSTANCE_DBNAME.findall(url_path)
    if len(matches) != 1:
        raise Error('%s does not match pattern %s' % (
                        url_path, rePROJECTID_INSTANCE_DBNAME.pattern))

    head = matches[0]
    g, w = len(head), rePROJECTID_INSTANCE_DBNAME.groups
    if g != w:
        raise Error('unmatched groups, got %d want %d' % (g, w))

    project_id, instance, database = head
    return dict(
            project_id=project_id,
            instance=instance,
            database=database,
    )


def extract_connection_params(settings_dict):
    """
    Examines settings_dict and depending on the provided
    keys will try to retrieve Cloud Spanner connection parameters.

    Args:
        settings_dict: a dict containing either:
            a) 'SPANNER_URL' as the key and expecting a URL of the
                form:
                    "cloudspanner:[//host[:port]]/project/<project_id>/
                    instances/<instance-id>/databases/<database-name>?
                    property-name=property-value"
                for example:
                {
                    "SPANNER_URL": "cloudspanner:/projects/appdev/instances/dev1/databases/db1?"
                                   "instance_config=projects/appdev/instanceConfigs/regional-us-west2"
                }

            b) Otherwise expects parameters whose keys are capitalized and
               are of the form:
                {
                    "NAME":             "<database_name>",
                    "INSTANCE":         "<instance_name>",
                    "AUTOCOMMIT":       True or False,
                    "READONLY":         True or False,
                    "PROJECT_ID":       "<project_id>",
                    "INSTANCE_CONFIG":  "[instance configuration if using a brand new database]",
                }

    Returns:
        A dict of the form:
        {
            "autocommit": <True otherwise omitted if zero-value>,
            "database": <database name otherwise omitted if zero-value>,
            "instance": <instance name otherwise omitted if zero-value>,
            "instance_config": <instance configuration otherwise omitted if zero-value>,
            "project_id": <project_id otherwise omitted if zero-value>,
            "readonly": <True otherwise omitted if zero-value>
        }
    """

    spanner_url = settings_dict.get('SPANNER_URL', None)
    if spanner_url:
        return parse_spanner_url(spanner_url)
    else:
        all_unfiltered = dict(
            autocommit=settings_dict.get('AUTOCOMMIT'),
            database=settings_dict.get('NAME'),
            instance=settings_dict.get('INSTANCE'),
            instance_config=settings_dict.get('INSTANCE_CONFIG'),
            project_id=resolve_project_id(settings_dict.get('PROJECT_ID')),
            readonly=settings_dict.get('READONLY'),
        )

        # Filter them to remove any unnecessary
        # None's whose keys have no associated value.
        return filter_out_unset_keys(all_unfiltered)


def filter_out_unset_keys(unfiltered):
    # Filter them to remove any unnecessary
    # None's whose keys have no associated value.
    return {key: value for key, value in unfiltered.items() if value}


reINSTANCE_CONFIG = re.compile('^projects/([^/]+)/instanceConfigs/([^/]+)$', re.UNICODE)


def validate_instance_config(instance_config):
    """
    Validates that instance_config matches the pattern
        ^projects/([^/]+)/instanceConfigs/([^/]+)$
    and for an example, looks like:
        projects/odeke-sandbox/instanceConfigs/regional-us-west2

    Args:
        instance_config: a non-empty string

    Returns:
        A non-empty string on validation failure or None if properly validated.
    """
    matches = reINSTANCE_CONFIG.findall(instance_config or '')
    if len(matches) != reINSTANCE_CONFIG.groups:
        return '%s does not match pattern %s' % (
                        instance_config, reINSTANCE_CONFIG.pattern)

    return None


STMT_DDL = 'DDL'
STMT_NON_UPDATING = 'NON_UPDATING'
STMT_UPDATING = 'UPDATING'

# Heuristic for identifying statements that don't need to be run as updates.
re_NON_UPDATE = re.compile(r'^\s*(SELECT|ANALYZE|AUDIT|EXPLAIN|SHOW)', re.UNICODE | re.IGNORECASE)

# DDL statements follow https://cloud.google.com/spanner/docs/data-definition-language
re_DDL = re.compile(
    r'^\s*(CREATE TABLE|CREATE DATABASE|ALTER TABLE|DROP TABLE|DROP INDEX)',
    re.UNICODE | re.IGNORECASE
)


def classify_stmt(sql):
    if re_DDL.match(sql):
        return STMT_DDL
    elif re_NON_UPDATE.match(sql):
        return STMT_NON_UPDATING
    else:
        return STMT_UPDATING
