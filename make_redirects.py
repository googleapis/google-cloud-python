import re
import os
import random
import requests

from pathlib import Path

api_names_dictionary = {
    "api_core": "google-api-core",
    "core": "google-api-core",
    "asset": "cloudasset",
    "automl": "automl",
    "bigquery": "bigquery",
    "bigquery_datatransfer": "bigquerydatatransfer",
    "bigquery_storage": "bigquerystorage",
    "bigtable": "bigtable",
    "container": "container",
    "containeranalysis": "containeranalysis",
    "datacatalog": "datacatalog",
    "datalabeling": "datalabeling",
    "dataproc": "dataproc",
    "datastore": "datastore",
    "dlp": "dlp",
    "dns": "dns",
    "error-reporting": "clouderrorreporting",
    "firestore": "firestore",
    "grafeas": "grafeas",
    "iam": "cloudiam",
    "iot": "cloudiot",
    "irm": "irm",
    "kms": "cloudkms",
    "language": "language",
    "logging": "logging",
    "monitoring": "monitoring",
    "oslogin": "oslogin",
    "pubsub": "pubsub",
    "redis": "redis",
    "resource-manager": "cloudresourcemanager",
    "runtimeconfig": "runtimeconfig",
    "scheduler": "cloudscheduler",
    "securitycenter": "securitycenter",
    "spanner": "spanner",
    "speech": "speech",
    "storage": "storage",
    "talent": "talent",
    "tasks": "cloudtasks",
    "texttospeech": "texttospeech",
    "trace": "cloudtrace",
    "translate": "translation",
    "videointelligence": "videointelligence",
    "vision": "vision",
    "webrisk": "webrisk",
    "websecurityscanner": "websecurityscanner",
}


def get_files_with_extension(dirName, extension=".html"):
    files = []

    for file in Path(dirName).glob(f"**/*{extension}"):
        if file.suffix == extension:
            files.append(str(file))

    return files


def get_api_from_path(path):
    # some exceptions are easier to capture here than in regex
    if "google/api_core" in path:
        return "google-api-core"
    if "grafeas/grafeas" in path:
        return "grafeas"
    if "iam_credentials" in path:
        return "cloudiam"
    if "spanner" in path:  # for spanner_admin
        return "spanner"
    if "containeranalysis" in path:  # under google/cloud/devtools
        return "containeranalysis"
    if "google/cloud/vision" in path:  # for vision helper
        return "vision"
    if "google/cloud/errorreporting" in path or "error_reporting" in path:
        return "clouderrorreporting"
    if "google/cloud/resource_manager" in path:
        return "cloudresourcemanager"
    if "google/cloud/client" in path:  # google cloud client class
        return "google-cloud-core"

    module_api_regex = r"google\/cloud\/(?P<api>.*?)(_v.*)?(\/.*|\.(html|md))"
    match = re.match(module_api_regex, path)

    if match:
        api = match.group("api")
        if api in api_names_dictionary:
            return api_names_dictionary[api]
        api = api.replace("_", "").replace("-", "").replace("cloud", "")
        if api in api_names_dictionary:
            return api_names_dictionary[api]

    return None


def make_redirects(dirname, ext=".html"):
    """
	Assembles a dictionary where key is file path
	and value is the googleapis.dev url
	"""
    GOOGLEAPIS_ROOT = f"https://googleapis.dev/python"
    content_page_regex = fr"{dirname}\/(?P<api>[^\/]*?)\/(?P<path>.*)"
    module_page_regex = fr"{dirname}\/_modules\/(?P<path>.*)"

    redirects = {}
    bad_paths = []

    html_files = get_files_with_extension(dirname, extension=ext)
    # import pdb; pdb.set_trace();
    print(f"{len(html_files)} files found in '{dirname}'.")
    for file in html_files:
        match = re.match(module_page_regex, file)
        if match:  # case 1: module level source code page
            api = get_api_from_path(match.group("path"))
            if api is not None:
                redirect_link = f"{GOOGLEAPIS_ROOT}/{api}/latest"
            else:
                bad_paths.append(file)
        else:
            match = re.match(content_page_regex, file)
            if match:  # case 2: api content page
                api = match.group("api")
                path = match.group("path")
                # google-cloud-core and google-api-core docs are split in googleapis.dev
                if api == "core":
                    if f"client{ext}" == path or f"config{ext}" == path:
                        redirect = f"{GOOGLEAPIS_ROOT}/google-cloud-core/latest/{path}"
                    elif f"core_changelog{ext}" == path:
                        redirect = (
                            f"{GOOGLEAPIS_ROOT}/google-cloud-core/latest/changelog.html"
                        )
                    elif f"api_core_changelog{ext}" == path:
                        redirect = (
                            f"{GOOGLEAPIS_ROOT}/google-api-core/latest/changelog.html"
                        )
                    else:
                        redirect = f"{GOOGLEAPIS_ROOT}/google-api-core/latest/{path}"
                    redirects[file] = redirect.replace(".md", ".html")
                else:
                    redirect = (
                        f"{GOOGLEAPIS_ROOT}/{api_names_dictionary[api]}/latest/{path}"
                    ).replace(".md", ".html")
                    # Some APIs have alternate names for the index page
                    redirect = redirect.replace(f"/usage.html", f"/index.html").replace(
                        f"/starting.html", f"/index.html"
                    )
                    redirects[file] = redirect
            else:  # case 3: other (top-level page )
                bad_paths.append(file)

    for path in bad_paths:
        # redirect files that don't belong to an api to the google-cloud-python repo readme
        redirects[
            path
        ] = "https://github.com/googleapis/google-cloud-python#google-cloud-python-client"

    return redirects, bad_paths


def add_redirect(path, url):
    HTML_TEMPLATE = f"""<html>
<head>
 <meta http-equiv="refresh" content="1; url={url}" />
 <script>
   window.location.href = "{url}"
 </script>
</head>
</html>
"""
    with open(path, "w") as f:
        f.write(HTML_TEMPLATE)


def add_redirect_to_md(path, url):
    MD_TEMPLATE = f"""---
redirect_to: "{url}"
---

"""
    with open(path, "w") as f:
        f.write(MD_TEMPLATE)


if __name__ == "__main__":

    #########################
    ## Redirects for /latest
    #########################
    redirects, bad_paths = make_redirects("latest")

    # Get a dictionary of paths to urls
    print("An appropriate API could not be determined for these paths.")
    for path in bad_paths:
        print(f"* {path}")

    not_found_urls = []

    for path, url in redirects.items():
        resp = requests.get(url)
        if resp.status_code == 200:
            add_redirect(path, url)
        else:
            not_found_urls.append(url)

    print("These URLs currently 404 ")
    for url in not_found_urls:
        print(f"* {url}")

    ###########################
    ## Redirects for /stable
    ###########################
    redirects, bad_paths = make_redirects("stable", ext=".md")

    # Get a dictionary of paths to urls
    print("An appropriate API could not be determined for these paths.")
    for path in bad_paths:
        print(f"* {path}")

    not_found_urls = []

    for path, url in redirects.items():
        resp = requests.get(url)
        if resp.status_code == 200:
            add_redirect_to_md(path, url)
        else:
            not_found_urls.append(url)

    print("These URLs currently 404 ")
    for url in not_found_urls:
        print(f"* {url}")
