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
    '/projects/([^/]+)/instances/([^/]+)/databases/([^/]+)$'
)


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


reINSTANCE_CONFIG = re.compile('^projects/([^/]+)/instanceConfigs/([^/]+)$')


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
    match = reINSTANCE_CONFIG.match(instance_config or '')
    if not match:
        return "'%s' does not match pattern %s" % (instance_config, reINSTANCE_CONFIG.pattern)

    matches = match.groups()
    if len(matches) != reINSTANCE_CONFIG.groups:
        return "'%s' does not match pattern %s\ngot %s:: %s" % (
                        instance_config, reINSTANCE_CONFIG.pattern, matches, reINSTANCE_CONFIG.groups)

    return None


STMT_DDL = 'DDL'
STMT_NON_UPDATING = 'NON_UPDATING'
STMT_UPDATING = 'UPDATING'
STMT_INSERT = 'INSERT'

# Heuristic for identifying statements that don't need to be run as updates.
re_NON_UPDATE = re.compile(r'^\s*(SELECT|ANALYZE|AUDIT|EXPLAIN|SHOW)', re.IGNORECASE)

# DDL statements follow https://cloud.google.com/spanner/docs/data-definition-language
re_DDL = re.compile(r'^\s*(CREATE|ALTER|DROP)', re.IGNORECASE | re.DOTALL)

re_IS_INSERT = re.compile(r'^\s*(INSERT)', re.IGNORECASE | re.DOTALL)


def classify_stmt(sql):
    if re_DDL.match(sql):
        return STMT_DDL
    elif re_IS_INSERT.match(sql):
        return STMT_INSERT
    elif re_NON_UPDATE.match(sql):
        return STMT_NON_UPDATING
    else:
        return STMT_UPDATING


re_INSERT = re.compile(
    # Only match the `INSERT INTO <table_name> (columns...)
    # otherwise the rest of the statement could be a complex
    # operation.
    r'^\s*INSERT INTO (?P<table_name>[^\s\(\)]+)\s+\((?P<columns>[^\(\)]+)\)',
    re.IGNORECASE | re.DOTALL,
)

re_VALUES_TILL_END = re.compile(
    r'VALUES\s*\(.+$',
    re.IGNORECASE | re.DOTALL,
)

re_VALUES_PYFORMAT = re.compile(
    # To match: (%s, %s,....%s)
    r'(\(\s*%s[^\(\)]+\))',
    re.DOTALL,
)


def parse_insert(insert_sql):
    match = re_INSERT.search(insert_sql)
    if not match:
        return None

    parsed = {
        'table': match.group('table_name'),
        'columns': [mi.strip() for mi in match.group('columns').split(',')],
    }
    after_VALUES_sql = re_VALUES_TILL_END.findall(insert_sql)
    if after_VALUES_sql:
        values_pyformat = re_VALUES_PYFORMAT.findall(after_VALUES_sql[0])
        if values_pyformat:
            parsed['values_pyformat'] = values_pyformat

    return parsed


re_PYFORMAT = re.compile(r'(%s|%\([^\(\)]+\)s)+', re.DOTALL)


def sql_pyformat_args_to_spanner(sql, params):
    """
    Transform pyformat set SQL to named arguments for Cloud Spanner.
    For example:
        SQL:      'SELECT * from t where f1=%s, f2=%s, f3=%s'
        Params:   ('a', 23, '888***')
    becomes:
        SQL:      'SELECT * from t where f1=@a0, f2=@a1, f3=@a2'
        Params:   {'a0': 'a', 'a1': 23, 'a2': '888***'}

    OR
        SQL:      'SELECT * from t where f1=%(f1)s, f2=%(f2)s, f3=%(f3)s'
        Params:   {'f1': 'a', 'f2': 23, 'f3': '888***', 'extra': 'aye')
    becomes:
        SQL:      'SELECT * from t where f1=@a0, f2=@a1, f3=@a2'
        Params:   {'a0': 'a', 'a1': 23, 'a2': '888***'}
    """
    if not params:
        return sql, params

    found_pyformat_placeholders = re_PYFORMAT.findall(sql)
    params_is_dict = isinstance(params, dict)

    if params_is_dict:
        if not found_pyformat_placeholders:
            return sql, params
    else:
        n_params = len(params) if params else 0
        n_matches = len(found_pyformat_placeholders)
        if n_matches != n_params:
            raise Error(
                'pyformat_args mismatch\ngot %d args from %s\n'
                'want %d args in %s' % (n_matches, found_pyformat_placeholders, n_params, params))

    if len(params) == 0:
        return sql, params

    named_args = {}
    # We've now got for example:
    # Case a) Params is a non-dict
    #   SQL:      'SELECT * from t where f1=%s, f2=%s, f3=%s'
    #   Params:   ('a', 23, '888***')
    # Case b) Params is a dict and the matches are %(value)s'
    for i, pyfmt in enumerate(found_pyformat_placeholders):
        key = 'a%d' % i
        sql = sql.replace(pyfmt, '@'+key, 1)
        if params_is_dict:
            # The '%(key)s' case, so interpolate it.
            resolved_value = pyfmt % params
            named_args[key] = resolved_value
        else:
            named_args[key] = params[i]

    return sql, named_args
