# Copyright 2016 Google Inc.
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

"""Helper to determine package from tag.
Get the current package directory corresponding to the Circle Tag.
"""

from __future__ import print_function

import os
import re
import sys


TAG_RE = re.compile(r"""
    ^
    (?P<pkg>
        (([a-z]+)-)*)            # pkg-name-with-hyphens- (empty allowed)
    ([0-9]+)\.([0-9]+)\.([0-9]+)  # Version x.y.z (x, y, z all ints)
    $
""", re.VERBOSE)
TAG_ENV = 'CIRCLE_TAG'
ERROR_MSG = '%s env. var. not set' % (TAG_ENV,)
BAD_TAG_MSG = 'Invalid tag name: %s. Expected pkg-name-x.y.z'
_SCRIPTS_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(_SCRIPTS_DIR, '..'))


def main():
    """Get the current package directory.
    Prints the package directory out so callers can consume it.
    """
    if TAG_ENV not in os.environ:
        print(ERROR_MSG, file=sys.stderr)
        sys.exit(1)

    tag_name = os.environ[TAG_ENV]
    match = TAG_RE.match(tag_name)
    if match is None:
        print(BAD_TAG_MSG % (tag_name,), file=sys.stderr)
        sys.exit(1)

    pkg_name = match.group('pkg')
    if pkg_name is None:
        print(ROOT_DIR)
    else:
        pkg_dir = pkg_name.rstrip('-').replace('-', '_')
        print(os.path.join(ROOT_DIR, pkg_dir))


if __name__ == '__main__':
    main()
