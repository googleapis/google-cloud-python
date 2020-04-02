#!/bin/bash
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -eo pipefail

cd github/python-spanner-django

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Debug: show build environment
env | grep KOKORO

# Setup service account credentials.
export GOOGLE_APPLICATION_CREDENTIALS=${KOKORO_GFILE_DIR}/service-account.json

# Setup project id.
export PROJECT_ID=$(cat "${KOKORO_GFILE_DIR}/project-id.json")

# Install tox
python3.6 -m pip install --upgrade --quiet tox flake8 isort
python3.6 -m tox --version

python3.6 -m tox
python3.6 -m isort --recursive --check-only --diff
python3.6 -m flake8

# Run with the Django test apps.
export RUNNING_SPANNER_BACKEND_TESTS=1
export DJANGO_TEST_APPS="admin_changelist admin_custom_urls admin_docs admin_inlines admin_ordering aggregation aggregation_regress annotations backends basic bulk_create cache choices custom_columns indexes inline_formsets introspection invalid_models_tests known_related_objects lookup max_lengths m2m_and_m2o m2m_intermediary m2m_multiple m2m_recursive m2m_regress m2m_signals m2m_through m2m_through_regress m2o_recursive managers_regress many_to_many many_to_one many_to_one_null max_lengths migrate_signals migrations.test_operations migration_test_data_persistence"

pip3 install .
mkdir -p django_tests && git clone --depth 1 --single-branch --branch spanner-2.2.x https://github.com/timgraham/django.git django_tests/django
# cd django_tests/django && pip3 install -e .; cd ../../

# Install dependencies for Django tests.
sudo apt-get update
apt-get install -y libffi-dev libjpeg-dev zlib1g-dev libmemcached-dev
cd django_tests/django && pip3 install -e . && pip3 install -r tests/requirements/py3.txt; cd ../../
./bin/parallelize_tests_linux
