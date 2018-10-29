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


def clone_git_on_borg_repo():
    cwd = os.getcwd()

    repo_name = "library-reference-docs"
    subprocess.check_call(["git", "clone","https://devrel.googlesource.com/cloud-docs/library-reference-docs"])
    os.chdir(repo_name)
    subprocess.check_call(["git", "remote", "add", "direct", "https://devrel.googlesource.com/_direct/cloud-docs/library-reference-docs"])
    os.chdir(cwd)

    return repo_name


def push_changes(language, package, version):
    subprocess.check_call(["git", "add", "."])
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

    repo = clone_git_on_borg_repo()

    # Copy docs to repo
    dest = Path(repo, language, package, version)
    if os.path.isdir(dest):
      shutil.rmtree(dest)

    shutil.copytree(package_documentation, Path(repo, language, package, version))
    os.chdir(repo)
    push_changes(repo, language, package, version)  # Commit and push


if __name__ == "__main__":
    main()
