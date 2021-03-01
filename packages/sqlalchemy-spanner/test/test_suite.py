# -*- coding: utf-8 -*-
#
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sqlalchemy.testing import config
from sqlalchemy.testing import eq_
from sqlalchemy.testing import provide_metadata
from sqlalchemy.testing.schema import Column
from sqlalchemy.testing.schema import Table
from sqlalchemy import literal_column
from sqlalchemy import select
from sqlalchemy import String

from sqlalchemy.testing.suite.test_update_delete import *  # noqa: F401, F403
from sqlalchemy.testing.suite.test_dialect import *  # noqa: F401, F403

from sqlalchemy.testing.suite.test_dialect import (  # noqa: F401, F403
    EscapingTest as _EscapingTest,
)


class EscapingTest(_EscapingTest):
    @provide_metadata
    def test_percent_sign_round_trip(self):
        """Test that the DBAPI accommodates for escaped / nonescaped
        percent signs in a way that matches the compiler

        SPANNER OVERRIDE
        Cloud Spanner supports tables with empty primary key, but
        only single one row can be inserted into such a table -
        following insertions will fail with `Row [] already exists".
        Overriding the test to avoid the same failure.
        """
        m = self.metadata
        t = Table("t", m, Column("data", String(50)))
        t.create(config.db)
        with config.db.begin() as conn:
            conn.execute(t.insert(), dict(data="some % value"))

            eq_(
                conn.scalar(
                    select([t.c.data]).where(
                        t.c.data == literal_column("'some % value'")
                    )
                ),
                "some % value",
            )

            conn.execute(t.delete())
            conn.execute(t.insert(), dict(data="some %% other value"))
            eq_(
                conn.scalar(
                    select([t.c.data]).where(
                        t.c.data == literal_column("'some %% other value'")
                    )
                ),
                "some %% other value",
            )
