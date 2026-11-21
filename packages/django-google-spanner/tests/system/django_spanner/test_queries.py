# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from decimal import Decimal

from django.db import connection
from django.test import TransactionTestCase

from .models import Author
from .utils import (
    setup_database,
    setup_instance,
    teardown_database,
    teardown_instance,
)


class TestQueries(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        setup_instance()
        setup_database()
        with connection.schema_editor() as editor:
            # Create the tables
            editor.create_model(Author)

    @classmethod
    def tearDownClass(cls):
        with connection.schema_editor() as editor:
            # delete the table
            editor.delete_model(Author)
        teardown_database()
        teardown_instance()

    def test_insert_and_fetch_value(self):
        """
        Tests model object creation with Author model.
        Inserting data into the model and retrieving it.
        """
        author_kent = Author(
            first_name="Arthur",
            last_name="Kent",
            rating=Decimal("4.1"),
        )
        author_kent.save()
        qs1 = Author.objects.all().values("first_name", "last_name")
        self.assertEqual(qs1[0]["first_name"], "Arthur")
        self.assertEqual(qs1[0]["last_name"], "Kent")
        # Delete data from Author table.
        Author.objects.all().delete()

    def test_typed_value_expressions_in_queries(self):
        """Verify typed Value(None, ...) and float Value() work in ORM queries."""
        from django.db import models
        from django.db.models.functions import Coalesce

        Author.objects.create(
            first_name="Arthur",
            last_name="Kent",
            rating=Decimal("4.1"),
        )
        try:
            union_rows = list(
                Author.objects.values_list("first_name", "last_name").union(
                    Author.objects.values_list(
                        "first_name",
                        models.Value(
                            None, output_field=models.CharField(max_length=20)
                        ),
                    )
                )
            )
            self.assertEqual(set(union_rows), {("Arthur", "Kent"), ("Arthur", None)})

            annotated = list(
                Author.objects.annotate(
                    null_text=models.Value(
                        None, output_field=models.CharField(max_length=20)
                    ),
                    coalesced=Coalesce(
                        models.Value(
                            None, output_field=models.CharField(max_length=20)
                        ),
                        models.Value("fallback"),
                    ),
                    cased=models.Case(
                        models.When(first_name="Arthur", then=models.Value("ok")),
                        default=models.Value(
                            None, output_field=models.CharField(max_length=20)
                        ),
                    ),
                    float_val=models.Value(1.5, output_field=models.FloatField()),
                ).values("null_text", "coalesced", "cased", "float_val")
            )
            self.assertEqual(
                annotated,
                [
                    {
                        "null_text": None,
                        "coalesced": "fallback",
                        "cased": "ok",
                        "float_val": 1.5,
                    }
                ],
            )
        finally:
            Author.objects.all().delete()
