import subprocess
import os
import tarfile
from pathlib import Path


def run_subprocess(command, cwd=None, timeout=1200, retries=3):
    """
    Runs a shell command as a subprocess with a timeout and retry logic.

    Args:
        command (str): The shell command to execute.
        cwd (str): Optional. The working directory to run the command in.
        timeout (int): Timeout for the command in seconds.
        retries (int): Number of times to retry the command if it times out.

    Returns:
        str: The stripped stdout from the command.
    """
    # Prepending 'cd' to the command makes it more robust, especially in
    # container environments where the `cwd` argument can be tricky.
    if cwd:
        command = f"{command}"
        
    print(f"\n> Executing command:\n  $ {command}")


    for attempt in range(retries):
        try:
            # Increased timeout (e.g., 1200 seconds = 20 minutes) for large downloads.
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            # Print stdout/stderr for debugging purposes
            if result.stdout:
                print("--- stdout ---\n" + result.stdout)
            if result.stderr:
                print("--- stderr ---\n" + result.stderr)
            return result.stdout.strip() # Success, exit the loop
        except subprocess.CalledProcessError as e:
            print(f"\nERROR: A command failed with exit code {e.returncode} on attempt {attempt + 1}")
            print(f"Command: {e.cmd}")
            # Do not print stdout/stderr on exit code 2 as it's often noisy and unhelpful.
            if e.returncode != 2:
                if e.stdout:
                    print(f"Stdout:\n{e.stdout}")
                if e.stderr:
                    print(f"Stderr:\n{e.stderr}")
            if attempt + 1 >= retries:
                raise # Raise the exception on the last attempt
        except subprocess.TimeoutExpired as e:
            print(f"\nWARNING: The command timed out after {e.timeout} seconds on attempt {attempt + 1}.")
            if attempt + 1 < retries:
                print("   Retrying in 10 seconds...")
                time.sleep(10)
            else:
                print(f"\nERROR: The command failed after {retries} attempts.")
                if e.stdout:
                     print(f"Stdout:\n{e.stdout}")
                if e.stderr:
                    print(f"Stderr:\n{e.stderr}")
                raise # Raise the exception on the last attempt

    # This part should not be reachable if retries are exhausted, but as a fallback
    raise Exception("Command failed after all retry attempts.")

def run_generation(library_id, googleapis_repo_path, target_repo_path):
    """
    Orchestrates the entire code generation process for a given library.
    This function replaces the logic of the old `owlbot copy-code` command.
    """
    print("Starting code generation run...")

    # In a real implementation, this would consult the mapping file to get a
    # list of API paths. For this example, we derive a single path.
    api_path = f"google/cloud/{library_id.split('-')[-1]}/v1"
    print(f"--- Starting generation for API path: {api_path} ---")

    # Step 1: Determine the correct Bazel rule to build.
    print("\n1. Determining Bazel rule...")
    bazel_query_command = f"bazelisk query 'filter(\"-py$\", kind(\"rule\", //{api_path}/...:*))'"
    # Give the first query command more time and retries as it may trigger downloads
    bazel_rule = run_subprocess(bazel_query_command, cwd=googleapis_repo_path, timeout=1800, retries=3)
    if not bazel_rule:
        print(f"ERROR: No Bazel rule found for API path: {api_path}")
        return
    print(f"   Found Bazel rule: {bazel_rule}")

    # Step 2: Run bazelisk to execute the bazel rule, which generates the code.
    print("\n2. Running Bazel build to generate tarball...")
    bazel_build_command = f"bazelisk build {bazel_rule}"
    run_subprocess(bazel_build_command, cwd=googleapis_repo_path)
    print("   Bazel build completed.")

    # Step 3: Locate the generated tarball.
    print("\n3. Locating generated tarball...")
    bazel_bin_command = "bazelisk info bazel-bin"
    bazel_bin = run_subprocess(bazel_bin_command, cwd=googleapis_repo_path)
    bazel_rule_path = bazel_rule.split(":")[0].replace("//", "")
    tar_gz_filename = bazel_rule.split(":")[1] + ".tar.gz"
    tar_path = os.path.join(bazel_bin, bazel_rule_path, tar_gz_filename)
    print(f"   Tarball found at: {tar_path}")

    # Step 4: Prepare the staging directory.
    print("\n4. Preparing staging directory...")
    # This path convention should match what the post-processor expects.
    # In this example, we use a placeholder version 'v1'.
    staging_dir = os.path.join(target_repo_path, "owl-bot-staging", library_id, "v1")
    os.makedirs(staging_dir, exist_ok=True)
    print(f"   Staging directory: {staging_dir}")

    # Step 5: Extract the tarball into the staging directory using Python.
    print("\n5. Extracting tarball...")
    with tarfile.open(tar_path, "r:gz") as tar:
        # Use strip_components logic by adjusting member paths
        for member in tar.getmembers():
            parts = member.path.split(os.sep)
            if len(parts) > 1:
                member.path = os.path.join(*parts[1:])
                tar.extract(member, path=staging_dir)
    print("   Extraction complete.")

    # Step 6: Run the post-processor.
    print("\n6. Running synthtool post-processor...")
    synthtool_command = "python3 -m synthtool.languages.python_mono_repo"
    run_subprocess(synthtool_command, cwd=target_repo_path)
    print("   Post-processing complete.")

    print("\nGeneration run finished successfully!")



if __name__ == '__main__':
    # --- Example Usage ---
    # Define the parameters for a sample run.
    # In a real scenario, these would be passed in from the CLI orchestrator.
    library_id = "google-cloud-language"
    # lib_api_version = "v1"
    # lib_api_path = "google/cloud/language/v1"
    
    # IMPORTANT: Replace these paths with the actual paths on your local machine
    # /usr/local/google/home/omairn/git/googleapis/googleapis:/workspace/googleapis
    # /usr/local/google/home/omairn/git/googleapis/google-cloud-python:/workspace/google-cloud-python 
    googleapis_repo = "/workspace/googleapis"
    python_mono_repo = "/workspace/google-cloud-python"

    # googleapis_repo = Path("/usr/local/google/home/omairn/git/googleapis/googleapis")
    # python_mono_repo = Path("/usr/local/google/home/omairn/git/googleapis/google-cloud-python")

    print("Starting example generation run...")
    # Check if paths are placeholders
    success = run_generation(library_id, googleapis_repo, python_mono_repo)
    if success:
        print("\nExample run finished successfully.")
    else:
        print("\nExample run failed.")
