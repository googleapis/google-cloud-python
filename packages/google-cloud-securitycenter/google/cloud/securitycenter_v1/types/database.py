# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.securitycenter.v1",
    manifest={
        "Database",
    },
)


class Database(proto.Message):
    r"""Represents database access information, such as queries.
    A database may be a sub-resource of an instance (as in the case
    of CloudSQL instances or Cloud Spanner instances), or the
    database instance itself. Some database resources may not have
    the full resource name populated because these resource types
    are not yet supported by Cloud Asset Inventory (e.g. CloudSQL
    databases).  In these cases only the display name will be
    provided.

    Attributes:
        name (str):
            The full resource name of the database the
            user connected to, if it is supported by CAI.
            (https://google.aip.dev/122#full-resource-names)
        display_name (str):
            The human readable name of the database the
            user connected to.
        user_name (str):
            The username used to connect to the DB. This
            may not necessarily be an IAM principal, and has
            no required format.
        query (str):
            The SQL statement associated with the
            relevant access.
        grantees (MutableSequence[str]):
            The target usernames/roles/groups of a SQL
            privilege grant (not an IAM policy change).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    user_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    query: str = proto.Field(
        proto.STRING,
        number=4,
    )
    grantees: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
