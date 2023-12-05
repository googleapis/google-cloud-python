# This file is used to generate a requirements.txt file
# using packages from this monorepo and split repositories in the
# googleapis organization on Github.

SCRIPT_ROOT=$(realpath $(dirname "${BASH_SOURCE[0]}"))

output+=""

# Get packages from this monorepo
for package in $SCRIPT_ROOT/../../packages/*/ ; do
    if [[ -f $package"/.repo-metadata.json" ]]; then
        distribution_name=$(jq ".distribution_name" $package"/.repo-metadata.json")
        # See https://github.com/googleapis/google-cloud-python/issues/12094
        # See https://github.com/googleapis/google-cloud-python/issues/12095
        if [[ ! -z "${distribution_name}" ]] && [[ ! ${distribution_name} = "google-cloud-alloydb-connectors" ]] && [[ ! ${distribution_name} = "google-cloud-billing-budgets" ]] ; then
            output+=$(echo $distribution_name | tr -d '"')
            output+="\n"
        fi
    fi
done

echo -e $output > mono_repo_packages.in

# Concatenate packages from split repos and this repo into a single file
cat split_repo_packages.in mono_repo_packages.in > all_packages.in

# In python specific environments, run `pip install --ignore-installed --upgrade pip-tools` and one of the following
pip-compile --generate-hashes --allow-unsafe all_packages.in --output-file all_packages_3.7.txt
pip-compile --generate-hashes --allow-unsafe all_packages.in --output-file all_packages_3.8.txt
pip-compile --generate-hashes --allow-unsafe all_packages.in --output-file all_packages_3.9.txt
pip-compile --generate-hashes --allow-unsafe all_packages.in --output-file all_packages_3.10.txt
pip-compile --generate-hashes --allow-unsafe all_packages.in --output-file all_packages_3.11.txt
# TODO: Python 3.12 is only supported in pre-release. Uncomment once it is released
# pip-compile --generate-hashes --allow-unsafe all_packages.in --output-file all_packages_3.12.txt
pip-compile --generate-hashes --allow-unsafe all_packages.in --pre --output-file all_packages_pre_release_3.7.txt
pip-compile --generate-hashes --allow-unsafe all_packages.in --pre --output-file all_packages_pre_release_3.8.txt
pip-compile --generate-hashes --allow-unsafe all_packages.in --pre --output-file all_packages_pre_release_3.9.txt
pip-compile --generate-hashes --allow-unsafe all_packages.in --pre --output-file all_packages_pre_release_3.10.txt
pip-compile --generate-hashes --allow-unsafe all_packages.in --pre --output-file all_packages_pre_release_3.11.txt
pip-compile --generate-hashes --allow-unsafe all_packages.in --pre --output-file all_packages_pre_release_3.12.txt