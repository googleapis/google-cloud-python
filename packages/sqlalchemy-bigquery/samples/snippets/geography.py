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
    # [START bigquery_sqlalchemy_create_table_with_geography]
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, String
    from sqlalchemy_bigquery import GEOGRAPHY

    Base = declarative_base()

    class Lake(Base):
        __tablename__ = "lakes"

        name = Column(String, primary_key=True)
        geog = Column(GEOGRAPHY)

    # [END bigquery_sqlalchemy_create_table_with_geography]
    Lake.__table__.create(engine)

    # [START bigquery_sqlalchemy_insert_geography]
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy_bigquery import WKT

    Session = sessionmaker(bind=engine)
    session = Session()

    lake = Lake(name="Majeur", geog="POLYGON((0 0,1 0,1 1,0 1,0 0))")
    lake2 = Lake(name="Garde", geog=WKT("POLYGON((1 0,3 0,3 2,1 2,1 0))"))
    b = WKT("POLYGON((3 0,6 0,6 3,3 3,3 0))").wkb
    lake3 = Lake(name="Orta", geog=b)

    session.add_all((lake, lake2, lake3))
    session.commit()
    # [END bigquery_sqlalchemy_insert_geography]

    # [START bigquery_sqlalchemy_query_geography_wkb]
    from sqlalchemy import func

    lakes_touching_lake2 = list(
        session.query(Lake).filter(func.ST_Touches(Lake.geog, lake2.geog))
    )
    # [END bigquery_sqlalchemy_query_geography_wkb]
    # [START bigquery_sqlalchemy_query_geography_text]
    lakes_containing = list(
        session.query(Lake).filter(func.ST_Contains(Lake.geog, "POINT(4 1)"))
    )
    # [END bigquery_sqlalchemy_query_geography_text]
    return lakes_touching_lake2, lakes_containing
