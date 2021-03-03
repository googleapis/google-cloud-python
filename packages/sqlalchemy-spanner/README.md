# python-sqlalchemy-spanner

**NOTE: This project is still in DEVELOPMENT. It may make breaking changes without prior notice and should not yet be used for production purposes.**  

**Usage example**:

```python
from sqlalchemy import create_engine, select, MetaData, Table

engine = create_engine(
    "spanner:///projects/project-id/instances/instance-id/databases/database-id"
)

table = Table("table-id", MetaData(bind=engine), autoload=True)
for row in select(["*"], from_obj=table).execute().fetchall():
    print(row)
```
