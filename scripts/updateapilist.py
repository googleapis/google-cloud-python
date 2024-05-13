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

import os
import requests
from typing import List, Optional


class MissingGithubToken(ValueError):
    """Raised when the GITHUB_TOKEN environment variable is not set"""

    pass

RAW_CONTENT_BASE_URL = "https://raw.githubusercontent.com"
MONO_REPO_PATH_FORMAT = "googleapis/google-cloud-python/main/packages/{repo_slug}"
SPLIT_REPO_PATH_FORMAT = "{repo_slug}/main"
REPO_METADATA_FILENAME = ".repo-metadata.json"


MONO_REPO = "googleapis/google-cloud-python"
REPO_EXCLUSION = [
    # core libraries
    "googleapis/python-api-core",
    "googleapis/python-cloud-core",
    # proto only packages
    "googleapis/python-api-common-protos",
    # testing utilities
    "googleapis/python-test-utils",
]

PACKAGE_RESPONSE_KEY = "name"
REPO_RESPONSE_KEY = "full_name"

BASE_API = "https://api.github.com"


class CloudClient:
    repo: str = None
    title: str = None
    release_level: str = None
    distribution_name: str = None
    issue_tracker: str = None

    def __init__(self, repo: dict):
        self.repo = repo["repo"]
        # For now, strip out "Google Cloud" to standardize the titles
        self.title = repo["name_pretty"].replace("Google ", "").replace("Cloud ", "")
        self.release_level = repo["release_level"]
        self.distribution_name = repo["distribution_name"]
        self.issue_tracker = repo.get("issue_tracker")

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
    
    url = f"https://github.com/{client.repo}"
    if client.repo == MONO_REPO:
        url += f"/tree/main/packages/{client.distribution_name}"

    content_row = [
        f"   * - `{client.title} <{url}>`_\n",
        f"     - " + client.release_level + "\n",
        f"     - |PyPI-{client.distribution_name}|\n",   
    ]

    if client.issue_tracker:
        content_row.append(f"     - `File an Issue <{client.issue_tracker}>`_\n")

    return (content_row, pypi_badge)


def generate_table_contents(clients: List[CloudClient]) -> List[str]:
    content_rows = [
        "\n",
        ".. list-table::\n",
        "   :header-rows: 1\n",
        "\n",
        "   * - Client\n",
        "     - Release Level\n",
        "     - Version\n",
        "     - Issue Tracker\n",
    ]

    pypi_links = ["\n"]
    for client in clients:
        content_row, pypi_link = client_row(client)
        content_rows += content_row
        pypi_links.append(pypi_link)

    return content_rows + pypi_links


def allowed_repo(repo) -> bool:
    return (
        repo[REPO_RESPONSE_KEY].startswith("googleapis/python-")
        and repo[REPO_RESPONSE_KEY] not in REPO_EXCLUSION
        and not repo[REPO_RESPONSE_KEY]
    )


def client_for_repo(repo_slug, is_split_repo: bool = True) -> Optional[CloudClient]:
    path = SPLIT_REPO_PATH_FORMAT if is_split_repo else MONO_REPO_PATH_FORMAT
    path = path.format(repo_slug=repo_slug)
    url = f"{RAW_CONTENT_BASE_URL}/{path}/{REPO_METADATA_FILENAME}"
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        return

    return CloudClient(response.json())


def get_clients_batch_from_response_json(response_json, is_split_repo: bool = True) -> List[CloudClient]:
    repos_key = REPO_RESPONSE_KEY if is_split_repo else PACKAGE_RESPONSE_KEY
    return [client_for_repo(repo[repos_key], is_split_repo) for repo in response_json if (not is_split_repo or allowed_repo(repo))]


def mono_repo_clients(token: str) -> List[CloudClient]:
    # all mono repo clients
    url = f"{BASE_API}/repos/{MONO_REPO}/contents/packages"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url=url, headers=headers)

    return get_clients_batch_from_response_json(response.json(), is_split_repo=False)


def split_repo_clients(token: str) -> List[CloudClient]:
    
    first_request = True
    while first_request or 'next' in response.links:
        if first_request:
            url = f"{BASE_API}/search/repositories?page=1"
            first_request = False
        else:
            url = response.links['next']['url']
        headers = {'Authorization': f'token {token}'}
        params = {'per_page': 100, "q": "python- in:name org:googleapis"}
        response = requests.get(url=url, params=params, headers=headers)
        repositories = response.json().get("items", [])
        if len(repositories) == 0:
            break
        return get_clients_batch_from_response_json(repositories)


def get_token():
    if 'GITHUB_TOKEN' not in os.environ:
        raise MissingGithubToken("Please include a GITHUB_TOKEN env var.")
    
    token = os.environ['GITHUB_TOKEN']
    return token


def all_clients() -> List[CloudClient]:
    clients = []
    token = get_token()
    
    clients.extend(split_repo_clients(token))
    clients.extend(mono_repo_clients(token))

    # remove empty clients
    return [client for client in clients if client]


clients = sorted(all_clients())
table_contents = generate_table_contents(clients)
replace_content_in_readme(table_contents)
