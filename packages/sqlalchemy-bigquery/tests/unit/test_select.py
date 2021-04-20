import sqlalchemy


def test_labels_not_forced(faux_conn):
    metadata = sqlalchemy.MetaData()
    table = sqlalchemy.Table(
        "some_table", metadata, sqlalchemy.Column("id", sqlalchemy.Integer)
    )
    metadata.create_all(faux_conn.engine)
    result = faux_conn.execute(sqlalchemy.select([table.c.id]))
    assert result.keys() == ["id"]  # Look! Just the column name!
