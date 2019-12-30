#!/bin/sh

# exit when any command fails
set -e

# If no SPANNER_TEST_DB is set, generate a unique one
# so that we can have multiple tests running without
# conflicting which changes and constraints. We'll always
# cleanup the created database.
TEST_DBNAME=${SPANNER_TEST_DB:-testdb-$(python3 -c 'import random; print(random.randint(1e3, 0x7fffffff))')}
TEST_DBNAME_OTHER="$TEST_DBNAME-other"
TEST_APPS=${DJANGO_TEST_APPS:-basic}
INSTANCE=${SPANNER_TEST_INSTANCE:-django-tests}
PROJECT=${SPANNER_TEST_PROJECT:-appdev-soda-spanner-staging}
SETTINGS_FILE="$TEST_DBNAME-settings"

checkout_django() {
    mkdir -p django_tests && cd django_tests
    git clone --depth 1 --single-branch --branch spanner-2.2.x https://github.com/timgraham/django.git
    cd django && pip3 install -e .
    pip3 install -r tests/requirements/py3.txt
}

create_settings() {
    cat << ! > "$SETTINGS_FILE.py"
DATABASES = {
   'default': {
       'ENGINE': 'spanner.django',
       'PROJECT': "$PROJECT",
       'INSTANCE': "$INSTANCE",
       'NAME': "$TEST_DBNAME",
   },
   'other': {
       'ENGINE': 'spanner.django',
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

run_django_tests() {
    cd tests
    create_settings
    echo -e "\033[32mRunning Django tests $TEST_APPS\033[00m"
    python3 runtests.py $TEST_APPS --verbosity=2 --noinput --settings $SETTINGS_FILE
}

install_spanner_django() {
    pip3 install .
}

install_spanner_django
checkout_django
run_django_tests
