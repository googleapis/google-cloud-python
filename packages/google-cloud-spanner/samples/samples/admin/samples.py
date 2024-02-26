#!/usr/bin/env python

# Copyright 2024 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to do basic operations using Cloud
Spanner.
For more information, see the README.rst under /spanner.
"""

import time

from google.cloud import spanner

OPERATION_TIMEOUT_SECONDS = 240


# [START spanner_create_instance]
def create_instance(instance_id):
    """Creates an instance."""
    from google.cloud.spanner_admin_instance_v1.types import spanner_instance_admin

    spanner_client = spanner.Client()

    config_name = "{}/instanceConfigs/regional-us-central1".format(
        spanner_client.project_name
    )

    operation = spanner_client.instance_admin_api.create_instance(
        parent=spanner_client.project_name,
        instance_id=instance_id,
        instance=spanner_instance_admin.Instance(
            config=config_name,
            display_name="This is a display name.",
            node_count=1,
            labels={
                "cloud_spanner_samples": "true",
                "sample_name": "snippets-create_instance-explicit",
                "created": str(int(time.time())),
            },
        ),
    )

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print("Created instance {}".format(instance_id))


# [END spanner_create_instance]


# [START spanner_create_instance_with_processing_units]
def create_instance_with_processing_units(instance_id, processing_units):
    """Creates an instance."""
    from google.cloud.spanner_admin_instance_v1.types import spanner_instance_admin

    spanner_client = spanner.Client()

    config_name = "{}/instanceConfigs/regional-us-central1".format(
        spanner_client.project_name
    )

    request = spanner_instance_admin.CreateInstanceRequest(
        parent=spanner_client.project_name,
        instance_id=instance_id,
        instance=spanner_instance_admin.Instance(
            config=config_name,
            display_name="This is a display name.",
            processing_units=processing_units,
            labels={
                "cloud_spanner_samples": "true",
                "sample_name": "snippets-create_instance_with_processing_units",
                "created": str(int(time.time())),
            },
        ),
    )

    operation = spanner_client.instance_admin_api.create_instance(request=request)

    print("Waiting for operation to complete...")
    instance = operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        "Created instance {} with {} processing units".format(
            instance_id, instance.processing_units
        )
    )


# [END spanner_create_instance_with_processing_units]


# [START spanner_create_database]
def create_database(instance_id, database_id):
    """Creates a database and tables for sample data."""
    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    request = spanner_database_admin.CreateDatabaseRequest(
        parent=instance.name,
        create_statement=f"CREATE DATABASE `{database_id}`",
        extra_statements=[
            """CREATE TABLE Singers (
            SingerId     INT64 NOT NULL,
            FirstName    STRING(1024),
            LastName     STRING(1024),
            SingerInfo   BYTES(MAX),
            FullName   STRING(2048) AS (
                ARRAY_TO_STRING([FirstName, LastName], " ")
            ) STORED
        ) PRIMARY KEY (SingerId)""",
            """CREATE TABLE Albums (
            SingerId     INT64 NOT NULL,
            AlbumId      INT64 NOT NULL,
            AlbumTitle   STRING(MAX)
        ) PRIMARY KEY (SingerId, AlbumId),
        INTERLEAVE IN PARENT Singers ON DELETE CASCADE""",
        ],
    )

    operation = spanner_client.database_admin_api.create_database(request=request)

    print("Waiting for operation to complete...")
    database = operation.result(OPERATION_TIMEOUT_SECONDS)

    print("Created database {} on instance {}".format(database.name, instance.name))


# [START spanner_update_database]
def update_database(instance_id, database_id):
    """Updates the drop protection setting for a database."""
    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    request = spanner_database_admin.UpdateDatabaseRequest(
        database=spanner_database_admin.Database(
            name="{}/databases/{}".format(instance.name, database_id),
            enable_drop_protection=True,
        ),
        update_mask={"paths": ["enable_drop_protection"]},
    )
    operation = spanner_client.database_admin_api.update_database(request=request)
    print(
        "Waiting for update operation for {}/databases/{} to complete...".format(
            instance.name, database_id
        )
    )
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print("Updated database {}/databases/{}.".format(instance.name, database_id))


# [END spanner_update_database]

# [END spanner_create_database]


# [START spanner_create_database_with_default_leader]
def create_database_with_default_leader(instance_id, database_id, default_leader):
    """Creates a database with tables with a default leader."""
    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    operation = spanner_client.database_admin_api.create_database(
        request=spanner_database_admin.CreateDatabaseRequest(
            parent=instance.name,
            create_statement=f"CREATE DATABASE `{database_id}`",
            extra_statements=[
                """CREATE TABLE Singers (
                    SingerId     INT64 NOT NULL,
                    FirstName    STRING(1024),
                    LastName     STRING(1024),
                    SingerInfo   BYTES(MAX)
                ) PRIMARY KEY (SingerId)""",
                """CREATE TABLE Albums (
                    SingerId     INT64 NOT NULL,
                    AlbumId      INT64 NOT NULL,
                    AlbumTitle   STRING(MAX)
                ) PRIMARY KEY (SingerId, AlbumId),
                INTERLEAVE IN PARENT Singers ON DELETE CASCADE""",
                "ALTER DATABASE {}"
                " SET OPTIONS (default_leader = '{}')".format(
                    database_id, default_leader
                ),
            ],
        )
    )

    print("Waiting for operation to complete...")
    database = operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        "Database {} created with default leader {}".format(
            database.name, database.default_leader
        )
    )


# [END spanner_create_database_with_default_leader]


# [START spanner_update_database_with_default_leader]
def update_database_with_default_leader(instance_id, database_id, default_leader):
    """Updates a database with tables with a default leader."""
    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            "ALTER DATABASE {}"
            " SET OPTIONS (default_leader = '{}')".format(database_id, default_leader)
        ],
    )
    operation = spanner_client.database_admin_api.update_database_ddl(request)

    operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        "Database {} updated with default leader {}".format(database_id, default_leader)
    )


# [END spanner_update_database_with_default_leader]


# [START spanner_create_database_with_encryption_key]
def create_database_with_encryption_key(instance_id, database_id, kms_key_name):
    """Creates a database with tables using a Customer Managed Encryption Key (CMEK)."""
    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin
    from google.cloud.spanner_admin_database_v1 import EncryptionConfig

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    request = spanner_database_admin.CreateDatabaseRequest(
        parent=instance.name,
        create_statement=f"CREATE DATABASE `{database_id}`",
        extra_statements=[
            """CREATE TABLE Singers (
            SingerId     INT64 NOT NULL,
            FirstName    STRING(1024),
            LastName     STRING(1024),
            SingerInfo   BYTES(MAX)
        ) PRIMARY KEY (SingerId)""",
            """CREATE TABLE Albums (
            SingerId     INT64 NOT NULL,
            AlbumId      INT64 NOT NULL,
            AlbumTitle   STRING(MAX)
        ) PRIMARY KEY (SingerId, AlbumId),
        INTERLEAVE IN PARENT Singers ON DELETE CASCADE""",
        ],
        encryption_config=EncryptionConfig(kms_key_name=kms_key_name),
    )

    operation = spanner_client.database_admin_api.create_database(request=request)

    print("Waiting for operation to complete...")
    database = operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        "Database {} created with encryption key {}".format(
            database.name, database.encryption_config.kms_key_name
        )
    )


# [END spanner_create_database_with_encryption_key]


def add_and_drop_database_roles(instance_id, database_id):
    """Showcases how to manage a user defined database role."""
    # [START spanner_add_and_drop_database_role]
    # instance_id = "your-spanner-instance"
    # database_id = "your-spanner-db-id"

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    role_parent = "new_parent"
    role_child = "new_child"

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            "CREATE ROLE {}".format(role_parent),
            "GRANT SELECT ON TABLE Singers TO ROLE {}".format(role_parent),
            "CREATE ROLE {}".format(role_child),
            "GRANT ROLE {} TO ROLE {}".format(role_parent, role_child),
        ],
    )
    operation = spanner_client.database_admin_api.update_database_ddl(request)

    operation.result(OPERATION_TIMEOUT_SECONDS)
    print(
        "Created roles {} and {} and granted privileges".format(role_parent, role_child)
    )

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            "REVOKE ROLE {} FROM ROLE {}".format(role_parent, role_child),
            "DROP ROLE {}".format(role_child),
        ],
    )
    operation = spanner_client.database_admin_api.update_database_ddl(request)

    operation.result(OPERATION_TIMEOUT_SECONDS)
    print("Revoked privileges and dropped role {}".format(role_child))

    # [END spanner_add_and_drop_database_role]


def create_table_with_datatypes(instance_id, database_id):
    """Creates a table with supported datatypes."""
    # [START spanner_create_table_with_datatypes]
    # instance_id = "your-spanner-instance"
    # database_id = "your-spanner-db-id"

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            """CREATE TABLE Venues (
            VenueId         INT64 NOT NULL,
            VenueName       STRING(100),
            VenueInfo       BYTES(MAX),
            Capacity        INT64,
            AvailableDates  ARRAY<DATE>,
            LastContactDate DATE,
            OutdoorVenue    BOOL,
            PopularityScore FLOAT64,
            LastUpdateTime  TIMESTAMP NOT NULL
            OPTIONS(allow_commit_timestamp=true)
        ) PRIMARY KEY (VenueId)"""
        ],
    )
    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        "Created Venues table on database {} on instance {}".format(
            database_id, instance_id
        )
    )
    # [END spanner_create_table_with_datatypes]


# [START spanner_add_json_column]
def add_json_column(instance_id, database_id):
    """Adds a new JSON column to the Venues table in the example database."""
    # instance_id = "your-spanner-instance"
    # database_id = "your-spanner-db-id"

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=["ALTER TABLE Venues ADD COLUMN VenueDetails JSON"],
    )

    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        'Altered table "Venues" on database {} on instance {}.'.format(
            database_id, instance_id
        )
    )


# [END spanner_add_json_column]


# [START spanner_add_numeric_column]
def add_numeric_column(instance_id, database_id):
    """Adds a new NUMERIC column to the Venues table in the example database."""

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=["ALTER TABLE Venues ADD COLUMN Revenue NUMERIC"],
    )

    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        'Altered table "Venues" on database {} on instance {}.'.format(
            database_id, instance_id
        )
    )


# [END spanner_add_numeric_column]


# [START spanner_create_table_with_timestamp_column]
def create_table_with_timestamp(instance_id, database_id):
    """Creates a table with a COMMIT_TIMESTAMP column."""

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            """CREATE TABLE Performances (
            SingerId     INT64 NOT NULL,
            VenueId      INT64 NOT NULL,
            EventDate    Date,
            Revenue      INT64,
            LastUpdateTime TIMESTAMP NOT NULL
            OPTIONS(allow_commit_timestamp=true)
        ) PRIMARY KEY (SingerId, VenueId, EventDate),
          INTERLEAVE IN PARENT Singers ON DELETE CASCADE"""
        ],
    )

    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        "Created Performances table on database {} on instance {}".format(
            database_id, instance_id
        )
    )


# [END spanner_create_table_with_timestamp_column]


# [START spanner_create_table_with_foreign_key_delete_cascade]
def create_table_with_foreign_key_delete_cascade(instance_id, database_id):
    """Creates a table with foreign key delete cascade action"""

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            """CREATE TABLE Customers (
               CustomerId INT64 NOT NULL,
               CustomerName STRING(62) NOT NULL,
               ) PRIMARY KEY (CustomerId)
            """,
            """
               CREATE TABLE ShoppingCarts (
               CartId INT64 NOT NULL,
               CustomerId INT64 NOT NULL,
               CustomerName STRING(62) NOT NULL,
               CONSTRAINT FKShoppingCartsCustomerId FOREIGN KEY (CustomerId)
               REFERENCES Customers (CustomerId) ON DELETE CASCADE
               ) PRIMARY KEY (CartId)
            """,
        ],
    )

    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        """Created Customers and ShoppingCarts table with FKShoppingCartsCustomerId
           foreign key constraint on database {} on instance {}""".format(
            database_id, instance_id
        )
    )


# [END spanner_create_table_with_foreign_key_delete_cascade]


# [START spanner_alter_table_with_foreign_key_delete_cascade]
def alter_table_with_foreign_key_delete_cascade(instance_id, database_id):
    """Alters a table with foreign key delete cascade action"""

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            """ALTER TABLE ShoppingCarts
               ADD CONSTRAINT FKShoppingCartsCustomerName
               FOREIGN KEY (CustomerName)
               REFERENCES Customers(CustomerName)
               ON DELETE CASCADE"""
        ],
    )

    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        """Altered ShoppingCarts table with FKShoppingCartsCustomerName
           foreign key constraint on database {} on instance {}""".format(
            database_id, instance_id
        )
    )


# [END spanner_alter_table_with_foreign_key_delete_cascade]


# [START spanner_drop_foreign_key_constraint_delete_cascade]
def drop_foreign_key_constraint_delete_cascade(instance_id, database_id):
    """Alter table to drop foreign key delete cascade action"""

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            """ALTER TABLE ShoppingCarts
               DROP CONSTRAINT FKShoppingCartsCustomerName"""
        ],
    )

    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        """Altered ShoppingCarts table to drop FKShoppingCartsCustomerName
           foreign key constraint on database {} on instance {}""".format(
            database_id, instance_id
        )
    )


# [END spanner_drop_foreign_key_constraint_delete_cascade]


# [START spanner_create_sequence]
def create_sequence(instance_id, database_id):
    """Creates the Sequence and insert data"""

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            "CREATE SEQUENCE Seq OPTIONS (sequence_kind = 'bit_reversed_positive')",
            """CREATE TABLE Customers (
            CustomerId     INT64 DEFAULT (GET_NEXT_SEQUENCE_VALUE(Sequence Seq)),
            CustomerName      STRING(1024)
            ) PRIMARY KEY (CustomerId)""",
        ],
    )

    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        "Created Seq sequence and Customers table, where the key column CustomerId uses the sequence as a default value on database {} on instance {}".format(
            database_id, instance_id
        )
    )

    def insert_customers(transaction):
        results = transaction.execute_sql(
            "INSERT INTO Customers (CustomerName) VALUES "
            "('Alice'), "
            "('David'), "
            "('Marc') "
            "THEN RETURN CustomerId"
        )
        for result in results:
            print("Inserted customer record with Customer Id: {}".format(*result))
        print(
            "Number of customer records inserted is {}".format(
                results.stats.row_count_exact
            )
        )

    database.run_in_transaction(insert_customers)


# [END spanner_create_sequence]


# [START spanner_alter_sequence]
def alter_sequence(instance_id, database_id):
    """Alters the Sequence and insert data"""

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            "ALTER SEQUENCE Seq SET OPTIONS (skip_range_min = 1000, skip_range_max = 5000000)",
        ],
    )

    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        "Altered Seq sequence to skip an inclusive range between 1000 and 5000000 on database {} on instance {}".format(
            database_id, instance_id
        )
    )

    def insert_customers(transaction):
        results = transaction.execute_sql(
            "INSERT INTO Customers (CustomerName) VALUES "
            "('Lea'), "
            "('Cataline'), "
            "('Smith') "
            "THEN RETURN CustomerId"
        )
        for result in results:
            print("Inserted customer record with Customer Id: {}".format(*result))
        print(
            "Number of customer records inserted is {}".format(
                results.stats.row_count_exact
            )
        )

    database.run_in_transaction(insert_customers)


# [END spanner_alter_sequence]


# [START spanner_drop_sequence]
def drop_sequence(instance_id, database_id):
    """Drops the Sequence"""

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            "ALTER TABLE Customers ALTER COLUMN CustomerId DROP DEFAULT",
            "DROP SEQUENCE Seq",
        ],
    )

    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        "Altered Customers table to drop DEFAULT from CustomerId column and dropped the Seq sequence on database {} on instance {}".format(
            database_id, instance_id
        )
    )


# [END spanner_drop_sequence]


# [START spanner_add_column]
def add_column(instance_id, database_id):
    """Adds a new column to the Albums table in the example database."""

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            "ALTER TABLE Albums ADD COLUMN MarketingBudget INT64",
        ],
    )

    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)
    print("Added the MarketingBudget column.")


# [END spanner_add_column]


# [START spanner_add_timestamp_column]
def add_timestamp_column(instance_id, database_id):
    """Adds a new TIMESTAMP column to the Albums table in the example database."""

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            "ALTER TABLE Albums ADD COLUMN LastUpdateTime TIMESTAMP "
            "OPTIONS(allow_commit_timestamp=true)"
        ],
    )

    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print(
        'Altered table "Albums" on database {} on instance {}.'.format(
            database_id, instance_id
        )
    )


# [END spanner_add_timestamp_column]


# [START spanner_create_index]
def add_index(instance_id, database_id):
    """Adds a simple index to the example database."""

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=["CREATE INDEX AlbumsByAlbumTitle ON Albums(AlbumTitle)"],
    )

    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print("Added the AlbumsByAlbumTitle index.")


# [END spanner_create_index]


# [START spanner_create_storing_index]
def add_storing_index(instance_id, database_id):
    """Adds an storing index to the example database."""

    from google.cloud.spanner_admin_database_v1.types import spanner_database_admin

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database.name,
        statements=[
            "CREATE INDEX AlbumsByAlbumTitle2 ON Albums(AlbumTitle)"
            "STORING (MarketingBudget)"
        ],
    )

    operation = spanner_client.database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print("Added the AlbumsByAlbumTitle2 index.")


# [END spanner_create_storing_index]


def enable_fine_grained_access(
    instance_id,
    database_id,
    iam_member="user:alice@example.com",
    database_role="new_parent",
    title="condition title",
):
    """Showcases how to enable fine grained access control."""
    # [START spanner_enable_fine_grained_access]
    # instance_id = "your-spanner-instance"
    # database_id = "your-spanner-db-id"
    # iam_member = "user:alice@example.com"
    # database_role = "new_parent"
    # title = "condition title"

    from google.type import expr_pb2
    from google.iam.v1 import iam_policy_pb2
    from google.iam.v1 import options_pb2
    from google.iam.v1 import policy_pb2

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    # The policy in the response from getDatabaseIAMPolicy might use the policy version
    # that you specified, or it might use a lower policy version. For example, if you
    # specify version 3, but the policy has no conditional role bindings, the response
    # uses version 1. Valid values are 0, 1, and 3.
    request = iam_policy_pb2.GetIamPolicyRequest(
        resource=database.name,
        options=options_pb2.GetPolicyOptions(requested_policy_version=3),
    )
    policy = spanner_client.database_admin_api.get_iam_policy(request=request)
    if policy.version < 3:
        policy.version = 3

    new_binding = policy_pb2.Binding(
        role="roles/spanner.fineGrainedAccessUser",
        members=[iam_member],
        condition=expr_pb2.Expr(
            title=title,
            expression=f'resource.name.endsWith("/databaseRoles/{database_role}")',
        ),
    )

    policy.version = 3
    policy.bindings.append(new_binding)
    set_request = iam_policy_pb2.SetIamPolicyRequest(
        resource=database.name,
        policy=policy,
    )
    spanner_client.database_admin_api.set_iam_policy(set_request)

    new_policy = spanner_client.database_admin_api.get_iam_policy(request=request)
    print(
        f"Enabled fine-grained access in IAM. New policy has version {new_policy.version}"
    )
    # [END spanner_enable_fine_grained_access]
