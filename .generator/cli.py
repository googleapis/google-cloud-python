import click #TODO: Figure out we can do this without click.
from pathlib import Path
import subprocess
import os
import glob
import synthtool
from synthtool import gcp


def configure():
    """This is unused at the moment"""
    pass


def generate():
    # source = Path("/usr/local/google/home/omairn/git/googleapis/googleapis")
    # generate_request = Path("/usr/local/google/home/omairn/git/googleapis/google-cloud-python/.librarian/generator-input/generate-request.json")
    # _input = Path("/usr/local/google/home/omairn/git/googleapis/google-cloud-python/.librarian/generator-input/")
    # output = Path("/usr/local/google/home/omairn/git/googleapis/google-cloud-python")
    source = "/workspace/googleapis"
    output = "/workspace/google-cloud-python"
    
    # hardcoding this for testing purposes:
    api_path = "google/cloud/language/v1"
    library_id = "google-cloud-language"
  
    # Get the rule for the API path that we need to build:
    # Source: https://github.com/googleapis/repo-automation-bots/blob/main/packages/bazel-bot/docker-image/generate-googleapis-gen.sh#L84
    # bazel_command = f"bazelisk query 'filter(\"-py$\", kind(\"rule\", //{api_path}/...:*))'"
    # # subprocess.run([bazel_command], cwd=source, shell=True)

    # TODO: Read up on check_output
    # bazel_rule = subprocess.check_output(bazel_command, cwd=source, shell=True).decode("utf-8").strip()
    # print(bazel_rule)

    # bazel_command = f"bazelisk build {bazel_rule}"
    # subprocess.run([bazel_command], cwd=source, shell=True)

    bazel_command = "bazelisk info bazel-bin"
    bazel_bin = subprocess.check_output(bazel_command, cwd=source, shell=True).decode("utf-8").strip()

    # bazel_rule: //google/cloud/language/v1:language-v1-py
    
    bazel_rule_split = bazel_rule.split(":")
    parent_dir = bazel_rule_split[0].replace("//", "")
    print(parent_dir)
    # subprocess.run(f"ls {parent_dir}", cwd=bazel_bin, shell=True)
    tar_gz_file = bazel_rule_split[1] + ".tar.gz"
    print(tar_gz_file)

    # tar_gz_file = "/usr/local/google/home/omairn/.cache/bazel/_bazel_omairn/9febfd2a38daa3aed258879a45f94c15/execroot/com_google_googleapis/bazel-out/k8-fastbuild/bin/google/cloud/language/v1/language-v1-py.tar.gz"


    # For some APIs like `google-cloud-workflows`, we will be adding to the same directory,
    # so don't fail if the directory exists
    api_version = api_path.split("/")[-1]
    os.makedirs(f"{output}/owl-bot-staging/{library_id}/{api_version}", exist_ok=True)

    
    # Extract the tar file and copy the code in owl-bot-staging:
    # TODO: Investigate why strip-components is needed
    # This step gets rid of the use of copy code and .OwlBot.yaml
    subprocess.run(
        f"tar -xvf {bazel_bin}/{parent_dir}/{tar_gz_file} --strip-components=1", cwd=f"{output}/owl-bot-staging/{library_id}/{api_version}", shell=True
    )

    # Remove all the tar files. This should be part of the design.
    # Commenting this out since we want the tar file for testing purposes.
    # subprocess.run(f"rm -rf *.tar.gz", cwd=tmp_dir, shell=True)


    # Run the post processor:
    # Alternative: We can call a function directly from synthtool since we're in Python.
    os.chdir(output)
    subprocess.run("python3 -m synthtool.languages.python_mono_repo", cwd=output, shell=True)

# gke-hub is an example edge-case.

def build():
    """This is unused at the moment"""
    pass


def main():
    generate()

main()