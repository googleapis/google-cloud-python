output="Please refer to each API's \`CHANGELOG.md\` file under the \`packages/\` directory\n\nChangelogs\n-----\n"

SCRIPT_ROOT=$(realpath $(dirname "${BASH_SOURCE[0]}"))
PACKAGES_URL=https://github.com/googleapis/google-cloud-python/tree/main/packages

for package in $SCRIPT_ROOT/../packages/*/ ; do
    package_dir=$(basename $package)
    output+="[$package_dir]("$PACKAGES_URL/$package_dir"/CHANGELOG.md)\n"    
done

echo -e $output > $SCRIPT_ROOT/../CHANGELOG.md
