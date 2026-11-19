# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import datetime
import unittest

from django.db import connection
from django.db.utils import IntegrityError
from django.test import TransactionTestCase
from django.utils import timezone

from django_spanner import USE_EMULATOR
from tests.system.django_spanner.utils import (
    setup_database,
    setup_instance,
    teardown_database,
    teardown_instance,
)

from .models import Event


@unittest.skipIf(USE_EMULATOR, "Check Constraint is not implemented in emulator.")
class TestCheckConstraint(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        setup_instance()
        setup_database()
        with connection.schema_editor() as editor:
            # Create the table
            editor.create_model(Event)

    @classmethod
    def tearDownClass(cls):
        with connection.schema_editor() as editor:
            # delete the table
            editor.delete_model(Event)
        teardown_database()
        teardown_instance()

    def test_insert_valid_value(self):
        """
        Tests model object creation with Event model.
        """
        now = timezone.now()
        now_plus_10 = now + datetime.timedelta(minutes=10)
        event_valid = Event(start_date=now, end_date=now_plus_10)
        event_valid.save()
        qs1 = Event.objects.filter().values("start_date")
        self.assertEqual(qs1[0]["start_date"], now)
        # Delete data from Event table.
        Event.objects.all().delete()

    def test_insert_invalid_value(self):
        """
        Tests model object creation with invalid data in Event model.
        """
        now = timezone.now()
        now_minus_1_day = now - timezone.timedelta(days=1)
        event_invalid = Event(start_date=now, end_date=now_minus_1_day)
        with self.assertRaises(IntegrityError):
            event_invalid.save()


class TestCheckConstraintValidation(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        setup_instance()
        setup_database()

    @classmethod
    def tearDownClass(cls):
        teardown_database()
        teardown_instance()

    def test_validate_check_constraint(self):
        import decimal
        import uuid

        from django.core.exceptions import ValidationError
        from django.db import models, transaction
        from django.db.models.lookups import Exact
        from django.test.utils import isolate_apps

        with isolate_apps("django_spanner"):
            self._run_check_constraint_validation_assertions(
                decimal, uuid, ValidationError, models, transaction, Exact
            )

    def _run_check_constraint_validation_assertions(
        self, decimal, uuid, ValidationError, models, transaction, Exact
    ):
        class ValidationSample(models.Model):
            name = models.CharField(max_length=50, null=True)
            price = models.IntegerField(null=True)
            max_price = models.IntegerField(null=True)
            is_active = models.BooleanField(null=True)
            rating = models.FloatField(null=True)
            blob = models.BinaryField(null=True)
            birth_date = models.DateField(null=True)
            created_at = models.DateTimeField(null=True)
            start_time = models.TimeField(null=True)
            amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
            duration = models.DurationField(null=True)
            uid = models.UUIDField(null=True)
            parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
            double_price = models.GeneratedField(
                expression=models.F("price") * 2,
                output_field=models.IntegerField(),
                db_persist=True,
            )

            class Meta:
                app_label = "django_spanner"
                constraints = [
                    models.CheckConstraint(
                        condition=models.Q(price__gt=0),
                        name="model_positive_price",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(double_price__gt=0),
                        name="model_positive_double_price",
                    ),
                ]

        with self.assertNoLogs("django.db.models", level="WARNING"):
            constraint = models.CheckConstraint(
                condition=models.Q(price__gt=0),
                name="positive_price",
                violation_error_code="invalid_price",
                violation_error_message="Price must be positive.",
            )

            # Valid value passes.
            constraint.validate(ValidationSample, ValidationSample(price=10))

            # Invalid value raises ValidationError with custom code/message.
            with self.assertRaisesRegex(
                ValidationError, "Price must be positive."
            ) as ctx:
                constraint.validate(ValidationSample, ValidationSample(price=0))
            self.assertEqual(ctx.exception.code, "invalid_price")

            # Excluded field skips validation.
            constraint.validate(
                ValidationSample, ValidationSample(price=0), exclude={"price"}
            )

            # Nullable field passes (SQL CHECK semantics: NULL -> UNKNOWN -> pass).
            constraint.validate(ValidationSample, ValidationSample(price=None))

            # Compound condition with NULL and FALSE must fail validation (NULL AND FALSE = FALSE).
            compound_constraint = models.CheckConstraint(
                condition=models.Q(price__gt=0) & models.Q(is_active=True),
                name="positive_and_active",
            )
            compound_constraint.validate(
                ValidationSample, ValidationSample(price=None, is_active=True)
            )
            with self.assertRaisesRegex(ValidationError, "positive_and_active"):
                compound_constraint.validate(
                    ValidationSample, ValidationSample(price=None, is_active=False)
                )

            # Negation and OR with NULL preserve SQL three-valued logic.
            negated_constraint = models.CheckConstraint(
                condition=~models.Q(price__gt=0),
                name="not_positive_price",
            )
            negated_constraint.validate(ValidationSample, ValidationSample(price=None))
            with self.assertRaisesRegex(ValidationError, "not_positive_price"):
                negated_constraint.validate(ValidationSample, ValidationSample(price=5))

            or_constraint = models.CheckConstraint(
                condition=models.Q(price__gt=0) | models.Q(is_active=True),
                name="positive_or_active",
            )
            or_constraint.validate(
                ValidationSample, ValidationSample(price=None, is_active=False)
            )

            # Field-to-field F() comparison.
            range_constraint = models.CheckConstraint(
                condition=models.Q(price__lte=models.F("max_price")),
                name="price_lte_max",
            )
            range_constraint.validate(
                ValidationSample, ValidationSample(price=10, max_price=20)
            )
            with self.assertRaisesRegex(ValidationError, "price_lte_max"):
                range_constraint.validate(
                    ValidationSample, ValidationSample(price=30, max_price=20)
                )

            # FloatField comparisons (including non-integers, inf, nan, and None).
            float_constraint = models.CheckConstraint(
                condition=models.Q(rating__gt=0.0),
                name="positive_rating",
            )
            float_constraint.validate(ValidationSample, ValidationSample(rating=1.5))
            float_constraint.validate(ValidationSample, ValidationSample(rating=2.0))
            float_constraint.validate(ValidationSample, ValidationSample(rating=None))
            float_constraint.validate(
                ValidationSample, ValidationSample(rating=float("inf"))
            )
            for bad_rating in (-1.5, 0.0, float("-inf"), float("nan")):
                with self.assertRaisesRegex(ValidationError, "positive_rating"):
                    float_constraint.validate(
                        ValidationSample, ValidationSample(rating=bad_rating)
                    )

            # BinaryField equality and NULL.
            blob_constraint = models.CheckConstraint(
                condition=models.Q(blob=b"ok"),
                name="blob_is_ok",
            )
            blob_constraint.validate(ValidationSample, ValidationSample(blob=b"ok"))
            blob_constraint.validate(ValidationSample, ValidationSample(blob=None))
            with self.assertRaisesRegex(ValidationError, "blob_is_ok"):
                blob_constraint.validate(
                    ValidationSample, ValidationSample(blob=b"bad")
                )

            # String lookup on NULL passes cleanly without DatabaseError.
            name_constraint = models.CheckConstraint(
                condition=models.Q(name__icontains="ok"),
                name="name_contains_ok",
            )
            name_constraint.validate(ValidationSample, ValidationSample(name="ok"))
            name_constraint.validate(ValidationSample, ValidationSample(name=None))
            with self.assertRaisesRegex(ValidationError, "name_contains_ok"):
                name_constraint.validate(ValidationSample, ValidationSample(name="bad"))

            # Date, DateTime, Time, Decimal, Duration, and UUID fields.
            date_val = datetime.date(2025, 1, 15)
            date_constraint = models.CheckConstraint(
                condition=models.Q(birth_date__gte=date_val), name="date_gte"
            )
            date_constraint.validate(
                ValidationSample, ValidationSample(birth_date=date_val)
            )
            date_constraint.validate(
                ValidationSample, ValidationSample(birth_date=None)
            )
            with self.assertRaisesRegex(ValidationError, "date_gte"):
                date_constraint.validate(
                    ValidationSample,
                    ValidationSample(birth_date=datetime.date(2020, 1, 1)),
                )

            dt_val = datetime.datetime(
                2025, 1, 15, 12, 30, 0, tzinfo=datetime.timezone.utc
            )
            dt_constraint = models.CheckConstraint(
                condition=models.Q(created_at__gte=dt_val), name="dt_gte"
            )
            dt_constraint.validate(
                ValidationSample, ValidationSample(created_at=dt_val)
            )
            dt_constraint.validate(ValidationSample, ValidationSample(created_at=None))
            with self.assertRaisesRegex(ValidationError, "dt_gte"):
                dt_constraint.validate(
                    ValidationSample,
                    ValidationSample(
                        created_at=datetime.datetime(
                            2020, 1, 1, tzinfo=datetime.timezone.utc
                        )
                    ),
                )

            time_val = datetime.time(12, 30, 0)
            time_constraint = models.CheckConstraint(
                condition=models.Q(start_time__gte=time_val), name="time_gte"
            )
            time_constraint.validate(
                ValidationSample, ValidationSample(start_time=time_val)
            )
            time_constraint.validate(
                ValidationSample, ValidationSample(start_time=None)
            )
            with self.assertRaisesRegex(ValidationError, "time_gte"):
                time_constraint.validate(
                    ValidationSample,
                    ValidationSample(start_time=datetime.time(8, 0, 0)),
                )

            dec_constraint = models.CheckConstraint(
                condition=models.Q(amount__gte=decimal.Decimal("1.50")), name="dec_gte"
            )
            dec_constraint.validate(
                ValidationSample, ValidationSample(amount=decimal.Decimal("2.00"))
            )
            dec_constraint.validate(ValidationSample, ValidationSample(amount=None))
            with self.assertRaisesRegex(ValidationError, "dec_gte"):
                dec_constraint.validate(
                    ValidationSample, ValidationSample(amount=decimal.Decimal("1.00"))
                )

            dur_constraint = models.CheckConstraint(
                condition=models.Q(duration__gte=datetime.timedelta(seconds=10)),
                name="dur_gte",
            )
            dur_constraint.validate(
                ValidationSample,
                ValidationSample(duration=datetime.timedelta(seconds=15)),
            )
            dur_constraint.validate(ValidationSample, ValidationSample(duration=None))
            with self.assertRaisesRegex(ValidationError, "dur_gte"):
                dur_constraint.validate(
                    ValidationSample,
                    ValidationSample(duration=datetime.timedelta(seconds=5)),
                )

            uid_val = uuid.UUID("12345678-1234-5678-1234-567812345678")
            uid_constraint = models.CheckConstraint(
                condition=models.Q(uid=uid_val), name="uid_eq"
            )
            uid_constraint.validate(ValidationSample, ValidationSample(uid=uid_val))
            uid_constraint.validate(ValidationSample, ValidationSample(uid=None))
            with self.assertRaisesRegex(ValidationError, "uid_eq"):
                uid_constraint.validate(
                    ValidationSample, ValidationSample(uid=uuid.uuid4())
                )

            # Boolean expressions, GeneratedField, PK field, and validate_constraints().
            expr_constraint = models.CheckConstraint(
                condition=models.ExpressionWrapper(
                    models.F("is_active"), output_field=models.BooleanField()
                ),
                name="expr_active",
            )
            expr_constraint.validate(ValidationSample, ValidationSample(is_active=True))
            expr_constraint.validate(ValidationSample, ValidationSample(is_active=None))
            with self.assertRaisesRegex(ValidationError, "expr_active"):
                expr_constraint.validate(
                    ValidationSample, ValidationSample(is_active=False)
                )

            exact_constraint = models.CheckConstraint(
                condition=Exact(models.F("price"), 10), name="exact_price_10"
            )
            exact_constraint.validate(ValidationSample, ValidationSample(price=10))
            with self.assertRaisesRegex(ValidationError, "exact_price_10"):
                exact_constraint.validate(ValidationSample, ValidationSample(price=5))

            case_constraint = models.CheckConstraint(
                condition=models.Case(
                    models.When(price__gt=0, then=models.Value(True)),
                    default=models.Value(False),
                    output_field=models.BooleanField(),
                ),
                name="case_positive",
            )
            case_constraint.validate(ValidationSample, ValidationSample(price=1))
            with self.assertRaisesRegex(ValidationError, "case_positive"):
                case_constraint.validate(ValidationSample, ValidationSample(price=0))

            pk_constraint = models.CheckConstraint(
                condition=models.Q(pk__gt=0), name="pk_positive"
            )
            pk_constraint.validate(ValidationSample, ValidationSample(id=1))
            pk_constraint.validate(ValidationSample, ValidationSample(id=None))
            with self.assertRaisesRegex(ValidationError, "pk_positive"):
                pk_constraint.validate(ValidationSample, ValidationSample(id=-1))

            ValidationSample(price=5).validate_constraints()
            ValidationSample(price=None).validate_constraints()
            with self.assertRaisesRegex(ValidationError, "model_positive_double_price"):
                ValidationSample(price=-5).validate_constraints()

            # Works cleanly inside an active atomic block without poisoning the transaction.
            with transaction.atomic():
                constraint.validate(ValidationSample, ValidationSample(price=None))
                constraint.validate(ValidationSample, ValidationSample(price=1))

            # ForeignKey, EmptyResultSet (__in=[]), and FullResultSet (~Q(__in=[])).
            fk_constraint = models.CheckConstraint(
                condition=models.Q(parent__gt=0), name="parent_positive"
            )
            fk_constraint.validate(ValidationSample, ValidationSample(parent_id=1))
            fk_constraint.validate(ValidationSample, ValidationSample(parent=None))
            with self.assertRaisesRegex(ValidationError, "parent_positive"):
                fk_constraint.validate(ValidationSample, ValidationSample(parent_id=-1))

            empty_in_constraint = models.CheckConstraint(
                condition=models.Q(price__in=[]), name="empty_in"
            )
            with self.assertRaisesRegex(ValidationError, "empty_in"):
                empty_in_constraint.validate(
                    ValidationSample, ValidationSample(price=1)
                )
            with self.assertRaisesRegex(ValidationError, "empty_in"):
                empty_in_constraint.validate(
                    ValidationSample, ValidationSample(price=None)
                )

            full_in_constraint = models.CheckConstraint(
                condition=~models.Q(price__in=[]), name="full_in"
            )
            full_in_constraint.validate(ValidationSample, ValidationSample(price=1))
