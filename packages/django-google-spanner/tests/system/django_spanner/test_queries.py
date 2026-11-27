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

    def test_pattern_lookups_literal_metacharacters(self):
        """Verify contains/startswith/endswith treat regex metacharacters literally."""
        from django.db import models

        class _UpperCaseTransform(models.Transform):
            lookup_name = "upper"
            function = "UPPER"
            bilateral = True

        Author.objects.bulk_create(
            [
                Author(first_name=".*", last_name=".*", rating=Decimal("1.0")),
                Author(
                    first_name="Hello.*",
                    last_name="hello.*",
                    rating=Decimal("2.0"),
                ),
                Author(
                    first_name="50%_off",
                    last_name="50%_",
                    rating=Decimal("5.0"),
                ),
                Author(
                    first_name="[unclosed",
                    last_name="[",
                    rating=Decimal("4.0"),
                ),
                Author(
                    first_name="line1\nline2",
                    last_name="multiline",
                    rating=Decimal("6.0"),
                ),
            ]
        )
        models.CharField.register_lookup(_UpperCaseTransform)
        try:

            def first_names(queryset):
                return set(queryset.values_list("first_name", flat=True))

            self.assertEqual(
                first_names(Author.objects.filter(first_name__contains=".*")),
                {".*", "Hello.*"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__contains=models.Value(".*"))
                ),
                {".*", "Hello.*"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(
                        first_name__contains=models.Value("[unclosed")
                    )
                ),
                {"[unclosed"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__icontains=models.Value("HELLO.*"))
                ),
                {"Hello.*"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__startswith=models.Value("50%_"))
                ),
                {"50%_off"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__startswith=models.F("last_name"))
                ),
                {".*", "50%_off", "[unclosed"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(
                        first_name__istartswith=models.Value("HELLO.*")
                    )
                ),
                {"Hello.*"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__endswith=models.Value(".*"))
                ),
                {".*", "Hello.*"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__iendswith=models.F("last_name"))
                ),
                {".*", "Hello.*"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__startswith=models.F("rating"))
                ),
                {"50%_off"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__upper__contains=".*")),
                {".*", "Hello.*"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__icontains="hello.*")),
                {"Hello.*"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__startswith="50%_")),
                {"50%_off"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__endswith=".*")),
                {".*", "Hello.*"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__contains="\n")),
                {"line1\nline2"},
            )
            all_names = {".*", "Hello.*", "50%_off", "[unclosed", "line1\nline2"}
            self.assertEqual(
                first_names(Author.objects.filter(first_name__contains="")),
                all_names,
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__startswith="")),
                all_names,
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__endswith="")),
                all_names,
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(
                        first_name__contains=models.Subquery(
                            Author.objects.filter(last_name="[").values("last_name")[:1]
                        )
                    )
                ),
                {"[unclosed"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(
                        first_name__contains=models.Subquery(
                            Author.objects.none().values("last_name")[:1]
                        )
                    )
                ),
                set(),
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__contains=models.Value(None))
                ),
                set(),
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__startswith=models.Value(None))
                ),
                set(),
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__endswith=models.Value(None))
                ),
                set(),
            )
        finally:
            models.CharField._unregister_lookup(_UpperCaseTransform)
            Author.objects.all().delete()

    def test_iexact_and_regex_lookups(self):
        """Verify iexact matches literally while regex and iregex evaluate patterns."""
        from django.db import models

        class _UpperCaseTransform(models.Transform):
            lookup_name = "upper"
            function = "UPPER"
            bilateral = True

        Author.objects.bulk_create(
            [
                Author(first_name=".*", last_name="other", rating=Decimal("1.0")),
                Author(
                    first_name="Hello.*",
                    last_name="hello.*",
                    rating=Decimal("2.0"),
                ),
                Author(
                    first_name="HelloWorld",
                    last_name="world",
                    rating=Decimal("3.0"),
                ),
                Author(
                    first_name="[unclosed",
                    last_name="other",
                    rating=Decimal("4.0"),
                ),
                Author(
                    first_name="1.5",
                    last_name="float",
                    rating=Decimal("5.0"),
                ),
                Author(
                    first_name="1.50",
                    last_name="decimal",
                    rating=Decimal("6.0"),
                ),
                Author(
                    first_name=r"a\b",
                    last_name="backslash",
                    rating=Decimal("7.0"),
                ),
                Author(
                    first_name="Café",
                    last_name="unicode",
                    rating=Decimal("8.0"),
                ),
                Author(
                    first_name="line1\nline2",
                    last_name="multiline",
                    rating=Decimal("9.0"),
                ),
                Author(
                    first_name="Straße",
                    last_name="german",
                    rating=Decimal("10.0"),
                ),
            ]
        )
        models.CharField.register_lookup(_UpperCaseTransform)
        try:

            def first_names(queryset):
                return set(queryset.values_list("first_name", flat=True))

            self.assertEqual(
                first_names(Author.objects.filter(first_name__iexact=".*")),
                {".*"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__iexact="[UNCLOSED")),
                {"[unclosed"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__iexact=1.5)),
                {"1.5"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__iexact=Decimal("1.50"))),
                {"1.50"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__iexact=models.Value(1.5))
                ),
                {"1.5"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__iexact=r"a\b")),
                {r"a\b"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__iexact="CAFÉ")),
                {"Café"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__iexact="LINE1\nLINE2")),
                {"line1\nline2"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__iexact="")),
                set(),
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__iexact=models.Value(None))
                ),
                set(),
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(
                        first_name__iexact=models.Subquery(
                            Author.objects.filter(last_name="hello.*").values(
                                "last_name"
                            )[:1]
                        )
                    )
                ),
                {"Hello.*"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__iexact="STRASSE")),
                {"Straße"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(
                        first_name__iexact=models.Subquery(
                            Author.objects.none().values("last_name")[:1]
                        )
                    )
                ),
                set(),
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__in=[".*", "Hello.*"]).exclude(
                        first_name__iexact=".*"
                    )
                ),
                {"Hello.*"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__iexact=models.Value("HELLO.*"))
                ),
                {"Hello.*"},
            )
            self.assertEqual(
                first_names(
                    Author.objects.filter(first_name__iexact=models.F("last_name"))
                ),
                {"Hello.*"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__upper__iexact="HELLO")),
                set(),
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__upper__iexact="HELLO.*")),
                {"Hello.*"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__regex=r"^Hello\.\*$")),
                {"Hello.*"},
            )
            self.assertEqual(
                first_names(Author.objects.filter(first_name__iregex=r"^hello")),
                {"Hello.*", "HelloWorld"},
            )
        finally:
            models.CharField._unregister_lookup(_UpperCaseTransform)
            Author.objects.all().delete()
