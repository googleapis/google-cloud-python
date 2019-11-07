# spanner-orm
Spanner Object Relation Mappers

![](./assets/spanner-django.png)

## Installing it
```shell
pip install .
```

## dbapi

This package implements the Python Database Connectivity API https://www.python.org/dev/peps/pep-0249/

with the following program:

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

### Django connection params

Settings should be a dict containing either:

a) 'SPANNER_URL' as the key and expecting a URL of the form:
```
cloudspanner:[//host[:port]]/project/<project_id>/instances/
<instance-id>/databases/<database-name>?property-name=property-value
```
For example:
```python
DATABASE={
    'default': {
        "SPANNER_URL":  "cloudspanner:/projects/appdev/instances/dev1/databases/db1?"
                        "instance_config=projects/appdev/instanceConfigs/regional-us-west2"
    }
}
```

b) Otherwise expects parameters whose keys are capitalized and
are of the form:
```python
{
    "NAME":             "<database_name>",
    "INSTANCE":         "<instance_name>",
    "AUTOCOMMIT":       True or False,
    "READONLY":         True or False,
    "PROJECT_ID":       "<project_id>",
    "INSTANCE_CONFIG":  "[instance configuration if using a brand new database]",
}
```

for example:

```python
{
    "NAME":             "db1",
    "INSTANCE":         "dev1",
    "AUTOCOMMIT":       True,
    "READONLY":         False,
    "PROJECT_ID":       "appdev",
    "INSTANCE_CONFIG":  "projects/appdev/instanceConfigs/regional-us-west2",
}
```
