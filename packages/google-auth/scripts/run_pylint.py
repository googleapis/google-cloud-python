# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script runs Pylint on the specified source.

Before running Pylint, it generates a Pylint configuration on
the fly based on programmatic defaults.
"""

from __future__ import print_function

import collections
import copy
import io
import os
import subprocess
import sys

import six


_SCRIPTS_DIR = os.path.abspath(os.path.dirname(__file__))
PRODUCTION_RC = os.path.join(_SCRIPTS_DIR, 'pylintrc')
TEST_RC = os.path.join(_SCRIPTS_DIR, 'pylintrc.test')

_PRODUCTION_RC_ADDITIONS = {
    'MESSAGES CONTROL': {
        'disable': [
            'I',
            'import-error',
            'no-member',
            'protected-access',
            'redefined-variable-type',
            'similarities',
            'no-else-return',
        ],
    },
}
_PRODUCTION_RC_REPLACEMENTS = {
    'MASTER': {
        'ignore': ['CVS', '.git', '.cache', '.tox', '.nox'],
        'load-plugins': 'pylint.extensions.check_docs',
    },
    'REPORTS': {
        'reports': 'no',
    },
    'BASIC': {
        'method-rgx': '[a-z_][a-z0-9_]{2,40}$',
        'function-rgx': '[a-z_][a-z0-9_]{2,40}$',
    },
    'TYPECHECK': {
        'ignored-modules': ['six', 'google.protobuf'],
    },
    'DESIGN': {
        'min-public-methods': '0',
        'max-args': '10',
        'max-attributes': '15',
    },
}
_TEST_RC_ADDITIONS = copy.deepcopy(_PRODUCTION_RC_ADDITIONS)
_TEST_RC_ADDITIONS['MESSAGES CONTROL']['disable'].extend([
    'missing-docstring',
    'no-self-use',
    'redefined-outer-name',
    'unused-argument',
    'no-name-in-module',
])
_TEST_RC_REPLACEMENTS = copy.deepcopy(_PRODUCTION_RC_REPLACEMENTS)
_TEST_RC_REPLACEMENTS.setdefault('BASIC', {})
_TEST_RC_REPLACEMENTS['BASIC'].update({
    'good-names': ['i', 'j', 'k', 'ex', 'Run', '_', 'fh', 'pytestmark'],
    'method-rgx': '[a-z_][a-z0-9_]{2,80}$',
    'function-rgx': '[a-z_][a-z0-9_]{2,80}$',
})
IGNORED_FILES = ()

_ERROR_TEMPLATE = 'Pylint failed on {} with status {:d}.'
_LINT_FILESET_MSG = (
    'Keyword arguments rc_filename and description are both '
    'required. No other keyword arguments are allowed.')


def get_default_config():
    """Get the default Pylint configuration.

    .. note::

        The output of this function varies based on the current version of
        Pylint installed.

    Returns:
        str: The default Pylint configuration.
    """
    # Swallow STDERR if it says
    # "No config file found, using default configuration"
    result = subprocess.check_output(['pylint', '--generate-rcfile'],
                                     stderr=subprocess.PIPE)
    # On Python 3, this returns bytes (from STDOUT), so we
    # convert to a string.
    return result.decode('utf-8')


def read_config(contents):
    """Reads pylintrc config into native ConfigParser object.

    Args:
        contents (str): The contents of the file containing the INI config.

    Returns
        ConfigParser.ConfigParser: The parsed configuration.
    """
    file_obj = io.StringIO(contents)
    config = six.moves.configparser.ConfigParser()
    config.readfp(file_obj)
    return config


def _transform_opt(opt_val):
    """Transform a config option value to a string.

    If already a string, do nothing. If an iterable, then
    combine into a string by joining on ",".

    Args:
        opt_val (Union[str, list]): A config option's value.

    Returns:
        str: The option value converted to a string.
    """
    if isinstance(opt_val, (list, tuple)):
        return ','.join(opt_val)
    else:
        return opt_val


def lint_fileset(*dirnames, **kwargs):
    """Lints a group of files using a given rcfile.

    Keyword arguments are

    * ``rc_filename`` (``str``): The name of the Pylint config RC file.
    * ``description`` (``str``): A description of the files and configuration
                                 currently being run.

    Args:
        dirnames (tuple): Directories to run Pylint in.
        kwargs: The keyword arguments. The only keyword arguments
            are ``rc_filename`` and ``description`` and both
            are required.

    Raises:
        KeyError: If the wrong keyword arguments are used.
    """
    try:
        rc_filename = kwargs['rc_filename']
        description = kwargs['description']
        if len(kwargs) != 2:
            raise KeyError
    except KeyError:
        raise KeyError(_LINT_FILESET_MSG)

    pylint_shell_command = ['pylint', '--rcfile', rc_filename]
    pylint_shell_command.extend(dirnames)
    status_code = subprocess.call(pylint_shell_command)
    if status_code != 0:
        error_message = _ERROR_TEMPLATE.format(description, status_code)
        print(error_message, file=sys.stderr)
        sys.exit(status_code)


def make_rc(base_cfg, target_filename,
            additions=None, replacements=None):
    """Combines a base rc and additions into single file.

    Args:
        base_cfg (ConfigParser.ConfigParser): The configuration we are
            merging into.
        target_filename (str): The filename where the new configuration
            will be saved.
        additions (dict): (Optional) The values added to the configuration.
        replacements (dict): (Optional) The wholesale replacements for
            the new configuration.

    Raises:
        KeyError: if one of the additions or replacements does not
            already exist in the current config.
    """
    # Set-up the mutable default values.
    if additions is None:
        additions = {}
    if replacements is None:
        replacements = {}

    # Create fresh config, which must extend the base one.
    new_cfg = six.moves.configparser.ConfigParser()
    # pylint: disable=protected-access
    new_cfg._sections = copy.deepcopy(base_cfg._sections)
    new_sections = new_cfg._sections
    # pylint: enable=protected-access

    for section, opts in additions.items():
        curr_section = new_sections.setdefault(
            section, collections.OrderedDict())
        for opt, opt_val in opts.items():
            curr_val = curr_section.get(opt)
            if curr_val is None:
                raise KeyError('Expected to be adding to existing option.')
            curr_val = curr_val.rstrip(',')
            opt_val = _transform_opt(opt_val)
            curr_section[opt] = '%s, %s' % (curr_val, opt_val)

    for section, opts in replacements.items():
        curr_section = new_sections.setdefault(
            section, collections.OrderedDict())
        for opt, opt_val in opts.items():
            curr_val = curr_section.get(opt)
            if curr_val is None:
                raise KeyError('Expected to be replacing existing option.')
            opt_val = _transform_opt(opt_val)
            curr_section[opt] = '%s' % (opt_val,)

    with open(target_filename, 'w') as file_obj:
        new_cfg.write(file_obj)


def main():
    """Script entry point. Lints both sets of files."""
    default_config = read_config(get_default_config())
    make_rc(default_config, PRODUCTION_RC,
            additions=_PRODUCTION_RC_ADDITIONS,
            replacements=_PRODUCTION_RC_REPLACEMENTS)
    make_rc(default_config, TEST_RC,
            additions=_TEST_RC_ADDITIONS,
            replacements=_TEST_RC_REPLACEMENTS)
    lint_fileset('google', rc_filename=PRODUCTION_RC,
                 description='Library')
    lint_fileset('tests', 'system_tests', rc_filename=TEST_RC,
                 description='Test')


if __name__ == '__main__':
    main()
