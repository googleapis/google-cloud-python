import os
import shutil
import subprocess
from pathlib import Path


def run_cookie_daemon(kokoro_artifacts_dir):
    gcompute_tools = Path(kokoro_artifacts_dir, "gcompute-tools")
    subprocess.check_call(
        [
            "git",
            "clone",
            "https://gerrit.googlesource.com/gcompute-tools",
            gcompute_tools,
        ]
    )
    subprocess.check_call([gcompute_tools / "git-cookie-authdaemon"])


def clone_git_on_borg_repo(repo_url):
    subprocess.check_call(["git", "clone", repo_url])
    repo = Path(repo_url)
    os.chdir(repo.name)
    subprocess.check_call(["git", "remote", "add", "direct", repo_url])

    return repo


def push_changes(repo, language, package, version):
    subprocess.check_call(["git", "add", repo])
    subprocess.check_call(["git", "status"])
    commit_msg = f"Publish documentation for {language}/{package}/{version}"
    subprocess.check_call(["git", "commit", "-m", commit_msg])
    subprocess.check_call(["git", "push", "direct", "master"])


def main():
    kokoro_artifacts_dir = os.environ["KOKORO_ARTIFACTS_DIR"]
    package = os.environ["PACKAGE"]
    language = os.environ["GITHUB_PACKAGE_LANGUAGE"]
    version = os.environ["GITHUB_PACKAGE_VERSION"]
    package_root = os.environ["GITHUB_PACKAGE_ROOT"]
    package_documentation = os.environ["GITHUB_PACKAGE_DOCUMENTATION"]

    os.chdir(package_root)
    run_cookie_daemon(kokoro_artifacts_dir)

    repo_url = "https://devrel.googlesource.com/cloud-docs/library-reference-docs"
    repo = clone_git_on_borg_repo(repo_url)

    # Copy docs to repo
    shutil.copytree(package_documentation, repo / language / package / version)
    push_changes(repo, language, package, version)  # Commit and push


if __name__ == "__main__":
    main()
