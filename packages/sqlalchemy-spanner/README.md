# Spanner dialect for SQLAlchemy

Spanner dialect for SQLAlchemy represents an interface API designed to make it possible to control Cloud Spanner databases with SQLAlchemy API. The dialect is built on top of [the Spanner DB API](https://github.com/googleapis/python-spanner/tree/master/google/cloud/spanner_dbapi), which is designed in accordance with [PEP-249](https://www.python.org/dev/peps/pep-0249/).

**NOTE: This project is still in DEVELOPMENT. It may make breaking changes without prior notice and should not yet be used for production purposes.**  

- [Cloud Spanner product documentation](https://cloud.google.com/spanner/docs)
- [SQLAlchemy product documentation](https://www.sqlalchemy.org/)

Quick Start
-----------

In order to use this package, you first need to go through the following steps:

1. [Select or create a Cloud Platform project.](https://console.cloud.google.com/project)
2. [Enable billing for your project.](https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project)
3. [Enable the Google Cloud Spanner API.](https://cloud.google.com/spanner)
4. [Setup Authentication.](https://googleapis.dev/python/google-api-core/latest/auth.html)

Installation
-----------

To install an in-development version of the package, clone its Git-repository:
```
git clone https://github.com/cloudspannerecosystem/python-spanner-sqlalchemy.git
```
Next install the package from the package `setup.py` file:
```
python setup.py install
```
During setup the dialect will be registered with entry points.

A Minimal App
-----------
**Create a table**
```python
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)

engine = create_engine(
    "spanner:///projects/project-id/instances/instance-id/databases/database-id"
)
metadata = MetaData(bind=engine)

user = Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("user_name", String(16), nullable=False),
)

metadata.create_all(engine)
```
**Insert a row**
```python
from sqlalchemy import (
    MetaData,
    Table,
    create_engine,
)

engine = create_engine(
    "spanner:///projects/project-id/instances/instance-id/databases/database-id"
)
user = Table("users", MetaData(bind=engine), autoload=True)

with engine.begin() as connection:
    connection.execute(user.insert(), {"user_id": 1, "user_name": "Full Name"})
```

**Read**
```python
from sqlalchemy import MetaData, Table, create_engine, select

engine = create_engine(
    "spanner:///projects/project-id/instances/instance-id/databases/database-id"
)
table = Table("users", MetaData(bind=engine), autoload=True)

with engine.begin() as connection:
    for row in connection.execute(select(["*"], from_obj=table)).fetchall():
        print(row)
```

Migration
-----------
SQLAlchemy uses [Alembic](https://alembic.sqlalchemy.org/en/latest/#) tool to organize database migrations.

**Warning!**  
A migration script can produce a lot of DDL statements. In case of executing every one of them separately performance and budget spending issues can occur. To avoid them it's highly recommended to use [Alembic batch context](https://cloud.google.com/spanner/docs/schema-updates) feature to pack DDL statements into more economical groups of statements.

Features and limitations
-----------
**Unique constraints**  
Cloud Spanner doesn't support direct UNIQUE constraints creation. In order to achieve column values uniqueness UNIQUE indexes should be used.

Instead of direct UNIQUE constraint creation:
```python
Table(
    'table',
    metadata,
    Column('col1', Integer),
    UniqueConstraint('col1', name='uix_1')
)
```
Create a UNIQUE index:
```python
Table(
    'table',
    metadata,
    Column('col1', Integer),
    Index("uix_1", "col1", unique=True),
)
```
**Autocommit mode**  
Spanner dialect supports both `SERIALIZABLE` and `AUTOCOMMIT` isolation levels. `SERIALIZABLE` is the default one, where transactions need to be committed manually. `AUTOCOMMIT` mode corresponds to automatically committing of a query right in its execution time.

Isolation level change example:
```python
from sqlalchemy import create_engine

eng = create_engine("spanner:///projects/project-id/instances/instance-id/databases/database-id")
autocommit_engine = eng.execution_options(isolation_level="AUTOCOMMIT")
```

**DDL and transactions**  
DDL statements are executed outside the regular transactions mechanism, which means DDL statements will not be rolled back on normal transaction rollback.

**Dropping a table**  
Cloud Spanner, by default, doesn't drop tables, which have secondary indexes and/or foreign key constraints. In Spanner dialect for SQLAlchemy, however, this restriction is omitted - if a table you are trying to delete has indexes/foreign keys, they will be dropped automatically right before dropping the table.

**Data types**  
Data types table mapping SQLAlchemy types to Cloud Spanner types:

| SQLAlchemy  | Spanner |
| ------------- | ------------- |
| INTEGER  | INT64  |
| BIGINT  | INT64  |
| DECIMAL  | NUMERIC  |
| FLOAT  | FLOAT64  |
| TEXT  | STRING  |
| ARRAY  | ARRAY  |
| BINARY  | BYTES  |
| VARCHAR  | STRING  |
| CHAR  | STRING  |
| BOOLEAN  | BOOL  |
| DATETIME  | TIMESTAMP  |
| NUMERIC  | NUMERIC  |


**Other limitations**  
- WITH RECURSIVE statement is not supported.
- Named schemas are not supported.
- Temporary tables are not supported, real tables are used instead.
- Numeric type dimensions (scale and precision) are constant. See the [docs](https://cloud.google.com/spanner/docs/data-types#numeric_types).

Best practices
-----------
When a SQLAlchemy function is called, a new connection to a database is established and a Spanner session object is fetched. In case of connectionless execution these fetches are done for every `execute()` call, which can cause a significant latency. To avoid initiating a Spanner session on every `execute()` call it's recommended to write code in connection-bounded fashion. Once a `Connection()` object is explicitly initiated, it fetches a Spanner session object and uses it for all the following calls made on this `Connection()` object.

Non-optimal connectionless use:
```python
# execute() is called on object, which is not a Connection() object
insert(user).values(user_id=1, user_name="Full Name").execute()
```
Optimal connection-bounded use:
```python
with engine.begin() as connection:
    # execute() is called on a Connection() object
    connection.execute(user.insert(), {"user_id": 1, "user_name": "Full Name"})
```
Connectionless way of use is also deprecated since SQLAlchemy 2.0 and soon will be removed (see in [SQLAlchemy docs](https://docs.sqlalchemy.org/en/14/core/connections.html#connectionless-execution-implicit-execution)).

Contributing
------------

Contributions to this library are welcome and encouraged.

See [CONTRIBUTING](https://github.com/cloudspannerecosystem/python-spanner-sqlalchemy/blob/main/contributing.md) for more information on how to get
started.

Please note that this project is released with a Contributor Code of Conduct.
By participating in this project you agree to abide by its terms. See the [Code
of Conduct](https://github.com/cloudspannerecosystem/python-spanner-sqlalchemy/blob/main/code-of-conduct.md) for more information.
