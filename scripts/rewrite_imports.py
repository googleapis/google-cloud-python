# Copyright 2015 Google Inc.
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

"""Build script for rewriting imports for protobuf generated modules.

Intended to be used for Google Cloud Bigtable protos (google/bigtable/v1)
and the dependent modules (google/api and google/protobuf).
"""

import sys


IMPORT_TEMPLATE = 'import %s'
IMPORT_FROM_TEMPLATE = 'from %s import '
REPLACEMENTS = {
    # Bigtable v2
    'google.bigtable.v2': 'google.cloud.bigtable._generated',
    'google.bigtable.admin.v2': 'google.cloud.bigtable._generated',
}


def transform_old_to_new(line, old_module, new_module,
                         ignore_import_from=False):
    """Transforms from an old module to a new one.

    First checks if a line starts with
        "from {old_module} import ..."
    then checks if the line contains
        "import {old_module} ..."
    then checks if the line starts with (ignoring whitespace)
        "{old_module} ..."
    and finally checks if the line contians
        "'some-dict-key': {old_module} ..."

    In any of these cases, "{old_module}" is replaced with "{new_module}".
    If none match, nothing is returned.

    :type line: str
    :param line: The line to be transformed.

    :type old_module: str
    :param old_module: The import to be re-written.

    :type new_module: str
    :param new_module: The new location of the re-written import.

    :type ignore_import_from: bool
    :param ignore_import_from: Flag to determine if the "from * import"
                               statements should be ignored.

    :rtype: :class:`str` or :data:`NoneType <types.NoneType>`
    :returns: The transformed line if the old module was found, otherwise
              does nothing.
    """
    if not ignore_import_from:
        import_from_statement = IMPORT_FROM_TEMPLATE % (old_module,)
        if line.startswith(import_from_statement):
            new_import_from_statement = IMPORT_FROM_TEMPLATE % (new_module,)
            # Only replace the first instance of the import statement.
            return line.replace(import_from_statement,
                                new_import_from_statement, 1)

    # If the line doesn't start with a "from * import *" statement, it
    # may still contain a "import * ..." statement.
    import_statement = IMPORT_TEMPLATE % (old_module,)
    if import_statement in line:
        new_import_statement = IMPORT_TEMPLATE % (new_module,)
        # Only replace the first instance of the import statement.
        return line.replace(import_statement,
                            new_import_statement, 1)

    # Also need to change references to the standalone imports. As a
    # stop-gap we fix references to them at the beginning of a line
    # (ignoring whitespace).
    if line.lstrip().startswith(old_module):
        # Only replace the first instance of the old_module.
        return line.replace(old_module, new_module, 1)

    # Finally check for usage in dictionaries.
    if ': ' + old_module in line:
        # Only replace the first instance of the old_module.
        return line.replace(': ' + old_module, ': ' + new_module, 1)


def transform_line(line):
    """Transforms an import line in a PB2 module.

    If the line is not an import of one of the packages in ``REPLACEMENTS``,
    does nothing and returns the original. Otherwise it replaces the package
    matched with our local package.

    :type line: str
    :param line: The line to be transformed.

    :rtype: str
    :returns: The transformed line.
    """
    # Work around https://github.com/grpc/grpc/issues/7101
    if line == 'import ':
        return ''

    for old_module, new_module in REPLACEMENTS.iteritems():
        result = transform_old_to_new(line, old_module, new_module)
        if result is not None:
            return result

    # If no matches, there is nothing to transform.
    return line


def rewrite_file(filename):
    """Rewrites a given PB2 modules.

    :type filename: str
    :param filename: The name of the file to be rewritten.
    """
    with open(filename, 'rU') as file_obj:
        content_lines = file_obj.read().split('\n')

    new_content = []
    for line in content_lines:
        new_content.append(transform_line(line))

    with open(filename, 'w') as file_obj:
        file_obj.write('\n'.join(new_content))


def main():
    """Rewrites all PB2 files."""
    for filename in sys.argv[1:]:
        rewrite_file(filename)


if __name__ == '__main__':
    main()
