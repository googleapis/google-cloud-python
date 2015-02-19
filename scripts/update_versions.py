# Copyright 2014 Google Inc. All rights reserved.
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

"""Simple script to update the gcloud versions list and file."""

import json
import os
from pkg_resources import get_distribution


LI_TEMPLATE = '<li><a href="%s/index.html">%s</a></li>'
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
GH_PAGES_DIR = os.path.abspath(os.path.join(SCRIPTS_DIR, '..', 'ghpages'))
VERSIONS_TMPL = os.path.join(SCRIPTS_DIR, 'versions.html.template')
JSON_VERSIONS = os.path.join(GH_PAGES_DIR, 'versions.json')
VERSIONS_FILE = os.path.join(GH_PAGES_DIR, 'versions.html')


def update_versions(new_version):
    """Updates JSON file with list of versions.

    Reads and writes JSON to ``JSON_VERSIONS`` file. Does not write
    if ``new_version`` is already contained.

    :type new_version: string
    :param new_version: New version being added.

    :rtype: list of strings
    :returns: List of all versions.
    """
    with open(JSON_VERSIONS, 'r') as file_obj:
        versions = json.load(file_obj)

    if new_version not in versions:
        versions.insert(0, new_version)

        with open(JSON_VERSIONS, 'w') as file_obj:
            json.dump(versions, file_obj)

    return versions


def render_template(new_version):
    """Renders static versions page.

    :type new_version: string
    :param new_version: New version being added.

    :rtype: string
    :returns: Rendered versions page.
    """
    versions = update_versions(new_version)

    with open(VERSIONS_TMPL, 'r') as file_obj:
        page_template = file_obj.read()

    versions_list = '\n'.join([LI_TEMPLATE % (version, version)
                               for version in versions])

    return page_template.format(versions=versions_list)


def main():
    """Creates new versions.html template."""
    new_version = get_distribution('gcloud').version
    rendered = render_template(new_version)
    with open(VERSIONS_FILE, 'w') as file_obj:
        file_obj.write(rendered)


if __name__ == '__main__':
    main()
