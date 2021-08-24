#!/bin/bash
# Run this script in the root of the repo. Warning this bash script will wipe out any uncommitted work.
# This script also requires the following file migratemainowlbot be placed in the same directory
git reset --hard
git clean -dfx
git checkout master
git pull
git pull origin master
git checkout -b migrate-default-branch-to-main
sed -i -e 's/master/main/g' .kokoro/*.sh
sed -i -e 's/blob\/master\/CONTRIBUTING.rst/blob\/main\/CONTRIBUTING.rst/g' CONTRIBUTING.rst
sed -i -e 's/blob\/master\/noxfile.py/blob\/main\/noxfile.py/g' CONTRIBUTING.rst
sed -i -e 's/GOOGLE_CLOUD_TESTING_BRANCH="master"/GOOGLE_CLOUD_TESTING_BRANCH="main"/g' CONTRIBUTING.rst
sed -i -e 's/``master``/``main``/g' CONTRIBUTING.rst
sed -i -e 's/upstream into master/upstream into main/g' CONTRIBUTING.rst
sed -i -e 's/upstream\/master/upstream\/main/g' CONTRIBUTING.rst
curl https://raw.githubusercontent.com/googleapis/google-cloud-python/main-migration/scripts/main_migration/migratemainowlbot -o migratemainowlbot
sed -i '/the microgenerator has a good coveragerc file/r migratemainowlbot' owlbot.py
rm migratemainowlbot
git commit -a -m "docs: migrate default branch from master to main"
git push origin migrate-default-branch-to-main


