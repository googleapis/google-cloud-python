# python-sqlalchemy-spanner

Usage example:

```python
from sqlalchemy import create_engine, select, MetaData, Table

engine = create_engine(
    "spanner:///projects/project-id/instances/instance-id/databases/database-id"
)

table = Table("table-id", MetaData(bind=engine), autoload=True)
for row in select(["*"], from_obj=table).execute().fetchall():
    print(row)
```