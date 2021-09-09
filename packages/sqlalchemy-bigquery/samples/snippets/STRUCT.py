# Copyright (c) 2021 The sqlalchemy-bigquery Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


def example(engine):
    # fmt: off
    # [START bigquery_sqlalchemy_create_table_with_struct]
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, String, Integer, Float
    from sqlalchemy_bigquery import STRUCT

    Base = declarative_base()

    class Car(Base):
        __tablename__ = "Cars"

        model = Column(String, primary_key=True)
        engine = Column(
            STRUCT(
                cylinder=STRUCT(("count", Integer),
                                ("compression", Float)),
                horsepower=Integer)
            )

    # [END bigquery_sqlalchemy_create_table_with_struct]
    Car.__table__.create(engine)

    # [START bigquery_sqlalchemy_insert_struct]
    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker(bind=engine)
    session = Session()

    sebring = Car(model="Sebring",
                  engine=dict(
                      cylinder=dict(
                          count=6,
                          compression=18.0),
                      horsepower=235))
    townc = Car(model="Town and Counttry",
                engine=dict(
                    cylinder=dict(
                        count=6,
                        compression=16.0),
                    horsepower=251))
    xj8 = Car(model="XJ8",
              engine=dict(
                  cylinder=dict(
                      count=8,
                      compression=10.75),
                  horsepower=575))

    session.add_all((sebring, townc, xj8))
    session.commit()

    # [END bigquery_sqlalchemy_insert_struct]

    # [START bigquery_sqlalchemy_query_struct]
    sixes = session.query(Car).filter(Car.engine.cylinder.count == 6)
    # [END bigquery_sqlalchemy_query_struct]
    sixes1 = list(sixes)

    # [START bigquery_sqlalchemy_query_STRUCT]
    sixes = session.query(Car).filter(Car.engine.CYLINDER.COUNT == 6)
    # [END bigquery_sqlalchemy_query_STRUCT]
    sixes2 = list(sixes)

    # [START bigquery_sqlalchemy_query_getitem]
    sixes = session.query(Car).filter(Car.engine["cylinder"]["count"] == 6)
    # [END bigquery_sqlalchemy_query_getitem]
    # fmt: on
    sixes3 = list(sixes)

    return sixes1, sixes2, sixes3
