# Copyright 2020 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

from typing import List, Optional
import requests


class CloudClient:
    repo: str = None
    title: str = None
    release_level: str = None
    distribution_name: str = None

    def __init__(self, repo: dict):
        self.repo = repo["repo"]
        # For now, strip out "Google Cloud" to standardize the titles
        self.title = repo["name_pretty"].replace("Google ", "").replace("Cloud ", "")
        self.release_level = repo["release_level"]
        self.distribution_name = repo["distribution_name"]

    # For sorting, we want to sort by release level, then API pretty_name
    def __lt__(self, other):
        if self.release_level == other.release_level:
            return self.title < other.title

        return other.release_level < self.release_level

    def __repr__(self):
        return repr((self.release_level, self.title))


def replace_content_in_readme(content_rows: List[str]) -> None:
    START_MARKER = ".. API_TABLE_START"
    END_MARKER = ".. API_TABLE_END"
    newlines = []
    repl_open = False
    with open("README.rst", "r") as f:
        for line in f:
            if not repl_open:
                newlines.append(line)

            if line.startswith(START_MARKER):
                repl_open = True
                newlines = newlines + content_rows
            elif line.startswith(END_MARKER):
                newlines.append("\n")
                newlines.append(line)
                repl_open = False

    with open("README.rst", "w") as f:
        for line in newlines:
            f.write(line)


def client_row(client: CloudClient) -> str:
    pypi_badge = f""".. |PyPI-{client.distribution_name}| image:: https://img.shields.io/pypi/v/{client.distribution_name}.svg
     :target: https://pypi.org/project/{client.distribution_name}\n"""

    content_row = [
        f"   * - `{client.title} <https://github.com/{client.repo}>`_\n",
        f"     - " + "|" + client.release_level + "|\n"
        f"     - |PyPI-{client.distribution_name}|\n",
    ]

    return (content_row, pypi_badge)


def generate_table_contents(clients: List[CloudClient]) -> List[str]:
    content_rows = [
        "\n",
        ".. list-table:: Libraries\n",
        "   :header-rows: 1\n",
        "\n",
        "   * - Client\n",
        "     - Release Level\n",
        "     - Version\n",
    ]

    pypi_links = ["\n"]
    for client in clients:
        content_row, pypi_link = client_row(client)
        content_rows += content_row
        pypi_links.append(pypi_link)

    return content_rows + pypi_links


REPO_METADATA_URL_FORMAT = (
    "https://raw.githubusercontent.com/{repo_slug}/master/.repo-metadata.json"
)


def client_for_repo(repo_slug) -> Optional[CloudClient]:
    url = REPO_METADATA_URL_FORMAT.format(repo_slug=repo_slug)
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        return

    return CloudClient(response.json())


REPO_LIST_JSON = "https://raw.githubusercontent.com/googleapis/sloth/master/repos.json"
REPO_EXCLUSION = [
    # core libraries
    "googleapis/python-api-core",
    "googleapis/python-cloud-core",
    # proto only packages
    "googleapis/python-org-policy",
    "googleapis/python-os-config",
    "googleapis/python-access-context-manager",
    "googleapis/python-api-common-protos",
    # testing utilities
    "googleapis/python-test-utils",
]


def allowed_repo(repo) -> bool:
    return (
        repo["language"] == "python"
        and repo["repo"].startswith("googleapis/python-")
        and repo["repo"] not in REPO_EXCLUSION
    )


def all_clients() -> List[CloudClient]:
    response = requests.get(REPO_LIST_JSON)
    clients = [
        client_for_repo(repo["repo"])
        for repo in response.json()["repos"]
        if allowed_repo(repo)
    ]
    # remove empty clients
    return [client for client in clients if client]


clients = sorted(all_clients())
table_contents = generate_table_contents(clients)
replace_content_in_readme(table_contents)
