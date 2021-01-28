#!/bin/sh

# Copyright (c) 2020 Google LLC. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

set -x pipefail

sudo apt-get update -y
sudo apt-get install -y libmemcached-dev

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

export DJANGO_TESTS_DIR="django_tests_dir"
mkdir -p $DJANGO_TESTS_DIR

if [ $SPANNER_EMULATOR_HOST != 0 ]
then
    pip3 install .
    pip3 install -e 'git+https://github.com/q-logic/python-spanner-django.git@dj_tests_against_emulator#egg=django-google-spanner'
    git clone --depth 1 --single-branch --branch spanner-2.2.x https://github.com/timgraham/django.git $DJANGO_TESTS_DIR/django
fi

# Install dependencies for Django tests.
sudo apt-get update
sudo apt-get install -y libffi-dev libjpeg-dev zlib1g-devel

cd $DJANGO_TESTS_DIR/django && pip3 install -e . && pip3 install -r tests/requirements/py3.txt; cd ../../

python3 create_test_instance.py

# If no SPANNER_TEST_DB is set, generate a unique one
# so that we can have multiple tests running without
# conflicting which changes and constraints. We'll always
# cleanup the created database.
TEST_DBNAME=${SPANNER_TEST_DB:-$(python3 -c 'import os, time; print(chr(ord("a") + time.time_ns() % 26)+os.urandom(10).hex())')}
TEST_DBNAME_OTHER="$TEST_DBNAME-ot"
INSTANCE=${SPANNER_TEST_INSTANCE:-django-tests}
PROJECT=${PROJECT_ID}
SPANNER_EMULATOR_HOST=${SPANNER_EMULATOR_HOST}
GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
SETTINGS_FILE="$TEST_DBNAME-settings"
TESTS_DIR=${DJANGO_TESTS_DIR:-django_tests}
TEST_APPS=${DJANGO_TEST_APPS}

create_settings() {
    cat << ! > "$SETTINGS_FILE.py"
DATABASES = {
   'default': {
       'ENGINE': 'django_spanner',
       'PROJECT': "$PROJECT",
       'INSTANCE': "$INSTANCE",
       'NAME': "$TEST_DBNAME",
   },
   'other': {
       'ENGINE': 'django_spanner',
       'PROJECT': "$PROJECT",
       'INSTANCE': "$INSTANCE",
       'NAME': "$TEST_DBNAME_OTHER",
   },
}
SECRET_KEY = 'spanner_tests_secret_key'
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
!
}

cd $TESTS_DIR/django/tests
create_settings

python3 runtests.py $TEST_APPS --verbosity=3 --noinput --settings $SETTINGS_FILE