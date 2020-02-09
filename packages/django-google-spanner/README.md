# django-spanner
ORM plugin for using Cloud Spanner as a database for Django.

## Table of contents
- [Installing it](#installing-it)
- [Using it](#using-it)
    - [Format](#format)
    - [Example](#example)
- [Running tests](#running-tests)
    - [Functional tests](#functional-tests)
    - [Django integration tests](#django-integration-tests)
- [Overall design](#overall-design)
- [How it works](#how-it-works)
- [dbapi](#dbapi)

## Installing it
```shell
pip3 install --user .
```

## Using it
After [installing it](#installing-it), you'll need to edit your Django `settings.py` file
and particularly the `DATABASES` section to point to an EXISTING database, of the format:

### Format

```python
DATABASES = {
    'default': {
        'ENGINE': 'spanner.django',
        'PROJECT': '<project_id>',
        'INSTANCE': '<instance_id>',
        'NAME': '<database_name>',
        # Only include this if you need to specify where to retrieve the
        # service account JSON for the credentials to connect to Cloud Spanner.
        'OPTIONS': {
            'credentials_uri': '<credentials_uri>',
        },
    },
}
```

### Example
For example:

```python
DATABASES = {
    'default': {
        'ENGINE': 'spanner.django',
        'PROJECT': 'appdev-soda-spanner-staging', # Or the GCP project-id
        'INSTANCE': 'django-dev1', # Or the Cloud Spanner instance
        'DATABASE': 'db1', # Or the Cloud Spanner database to use
    }
}
```

## Running tests

### Functional tests
We have functional tests for individual components that can be run by
```shell
tox
```

### Django integration tests
We run full integration tests with Django's test suite, on Travis Continuous Integration before every
pull request is merged. Please see the file [.travis.yml](./.travis.yml)

## How it works

### Overall design
![](./assets/spanner-django.png)

### Internals
![](./assets/spanner-django-internals.png)

## dbapi

The [spanner.dbapi](./spanner/django) package implements the [Python Database Connectivity v2 API](https://www.python.org/dev/peps/pep-0249/)

and can be used with the code snippet:

```python
import time

from spanner.dbapi import connect

def main():
    conn = connect('cloudspanner:/projects/odeke-sandbox/instances/django-dev1/databases/db1')
    t1 = time.time()
    cur = conn.cursor()
    cur.execute("""
    SELECT
        date,
        EXTRACT(ISOYEAR FROM date) AS isoyear,
        EXTRACT(ISOWEEK FROM date) AS isoweek,
        EXTRACT(YEAR FROM date) AS year,
        EXTRACT(WEEK FROM date) AS week
    FROM UNNEST(GENERATE_DATE_ARRAY('2015-12-23', '2016-01-09')) AS date
    ORDER BY date;
    """)
    for row in cur:
       print('description', cur.description)
       print(row)
    conn.close()

    t2 = time.time()
    print('Time spent ', t2-t1)

if __name__ == '__main__':
    main()
````

which produces

```shell
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2015, 12, 23), 2015, 52, 2015, 51]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2015, 12, 24), 2015, 52, 2015, 51]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2015, 12, 25), 2015, 52, 2015, 51]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2015, 12, 26), 2015, 52, 2015, 51]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2015, 12, 27), 2015, 52, 2015, 52]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2015, 12, 28), 2015, 53, 2015, 52]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2015, 12, 29), 2015, 53, 2015, 52]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2015, 12, 30), 2015, 53, 2015, 52]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2015, 12, 31), 2015, 53, 2015, 52]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2016, 1, 1), 2015, 53, 2016, 0]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2016, 1, 2), 2015, 53, 2016, 0]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2016, 1, 3), 2015, 53, 2016, 1]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2016, 1, 4), 2016, 1, 2016, 1]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2016, 1, 5), 2016, 1, 2016, 1]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2016, 1, 6), 2016, 1, 2016, 1]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2016, 1, 7), 2016, 1, 2016, 1]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2016, 1, 8), 2016, 1, 2016, 1]
description (Column(name='date', type_code=5), Column(name='isoyear', type_code=2), Column(name='isoweek', type_code=2), Column(name='year', type_code=2), Column(name='week', type_code=2))
[datetime.date(2016, 1, 9), 2016, 1, 2016, 1]
Time spent  1.6195518970489502
```
