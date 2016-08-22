# Copyright 2016 Google Inc. All rights reserved.
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

"""Check if all public modules are included in our docs."""


from __future__ import print_function

import os
import sys
import warnings

from sphinx.ext.intersphinx import fetch_inventory


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
OBJECT_INVENTORY_RELPATH = os.path.join('_build', 'html', 'objects.inv')
IGNORED_PREFIXES = ('test_', '_')
IGNORED_MODULES = frozenset([
    'gcloud.__init__',
    'gcloud.bigquery.__init__',
    'gcloud.bigtable.__init__',
    'gcloud.datastore.__init__',
    'gcloud.dns.__init__',
    'gcloud.error_reporting.__init__',
    'gcloud.iterator',
    'gcloud.logging.__init__',
    'gcloud.logging.handlers.__init__',
    'gcloud.logging.handlers.transports.__init__',
    'gcloud.monitoring.__init__',
    'gcloud.pubsub.__init__',
    'gcloud.resource_manager.__init__',
    'gcloud.storage.__init__',
    'gcloud.streaming.__init__',
    'gcloud.streaming.buffered_stream',
    'gcloud.streaming.exceptions',
    'gcloud.streaming.http_wrapper',
    'gcloud.streaming.stream_slice',
    'gcloud.streaming.transfer',
    'gcloud.streaming.util',
    'gcloud.translate.__init__',
])


class SphinxApp(object):
    """Mock app to interact with Sphinx helpers."""
    warn = warnings.warn
    srcdir = DOCS_DIR


def is_valid_module(filename):
    """Determines if a filename is a valid Python module.

    Assumes if is just the end of a path (i.e. does not contain
    ``os.path.sep``.

    :type filename: string
    :param filename: The name of a file.

    :rtype: bool
    :returns: Flag indicating if the filename is valid.
    """
    if not filename.endswith('.py'):
        return False
    if filename == '__init__.py':
        return True
    for prefix in IGNORED_PREFIXES:
        if filename.startswith(prefix):
            return False
    return True


def get_public_modules(path, base_package=None):
    """Get list of all public modules relative to a path.

    :type path: string
    :param path: The path containing the python modules.

    :type base_package: string
    :param base_package: (Optional) A package to prepend in
                         front of the path.

    :rtype: list
    :returns: List of all modules found.
    """
    result = []
    for subdir, _, files in os.walk(path):
        # Skip folders that start with _.
        if any([part.startswith('_')
                for part in subdir.split(os.path.sep)]):
            continue
        _, rel_dir = subdir.split(path)
        rel_dir = rel_dir.lstrip(os.path.sep)
        for filename in files:
            if is_valid_module(filename):
                mod_name, _ = os.path.splitext(filename)
                rel_path = os.path.join(rel_dir, mod_name)
                if base_package is not None:
                    rel_path = os.path.join(base_package, rel_path)
                # Turn into a Python module rather than a file path.
                result.append(rel_path.replace(os.path.sep, '.'))

    return result


def main():
    """Main script to verify modules included."""
    mock_uri = ''
    inventory = fetch_inventory(SphinxApp, mock_uri,
                                OBJECT_INVENTORY_RELPATH)
    sphinx_mods = set(inventory['py:module'].keys())

    library_dir = os.path.join(BASE_DIR, 'gcloud')
    public_mods = get_public_modules(library_dir,
                                     base_package='gcloud')
    public_mods = set(public_mods)

    if not sphinx_mods <= public_mods:
        unexpected_mods = sphinx_mods - public_mods
        message = ['Unexpected error. There were modules referenced by '
                   'Sphinx that are not among the public modules.']
        message.extend(['- %s' % (mod,) for mod in unexpected_mods])
        print('\n'.join(message), file=sys.stderr)
        sys.exit(1)

    undocumented_mods = public_mods - sphinx_mods
    # Remove ignored modules.
    undocumented_mods -= IGNORED_MODULES
    if undocumented_mods:
        message_parts = ['Found undocumented public modules:']
        message_parts.extend(['- ' + mod_name
                              for mod_name in sorted(undocumented_mods)])
        print('\n'.join(message_parts), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
