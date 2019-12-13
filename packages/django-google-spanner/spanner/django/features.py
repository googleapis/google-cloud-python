from django.db.backends.base.features import BaseDatabaseFeatures


class DatabaseFeatures(BaseDatabaseFeatures):
    # https://cloud.google.com/spanner/quotas#query_limits
    max_query_params = 950
    supports_foreign_keys = False
    supports_regex_backreferencing = False
    supports_timezones = False
    supports_transactions = False
    supports_column_check_constraints = False
    supports_table_check_constraints = False

    # Django tests that aren't supported by Spanner.
    skip_tests = (
        # No Django transaction management in Spanner.
        'basic.tests.SelectOnSaveTests.test_select_on_save_lying_update',
        # spanner.django monkey patches AutoField to have a default value.
        'basic.tests.ModelTest.test_hash',
        'model_fields.test_durationfield.TestSerialization.test_dumping',
        'model_fields.test_uuid.TestSerialization.test_dumping',
        'model_fields.test_booleanfield.ValidationTest.test_nullbooleanfield_blank',
        'timezones.tests.LegacyDatabaseTests.test_cursor_execute_accepts_naive_datetime',
        'timezones.tests.NewDatabaseTests.test_cursor_execute_accepts_naive_datetime',
        # Tests that assume a serial pk.
        'admin_views.tests.AdminViewPermissionsTest.test_history_view',
        'aggregation_regress.tests.AggregationTests.test_more_more',
        'aggregation_regress.tests.AggregationTests.test_more_more_more',
        'aggregation_regress.tests.AggregationTests.test_ticket_11293',
        'defer_regress.tests.DeferRegressionTest.test_ticket_23270',
        'distinct_on_fields.tests.DistinctOnTests.test_basic_distinct_on',
        'generic_relations_regress.tests.GenericRelationTests.test_annotate',
        'lookup.tests.LookupTests.test_get_next_previous_by',
        'lookup.tests.LookupTests.test_values_list',
        'migrations.test_operations.OperationTests.test_alter_order_with_respect_to',
        'model_fields.tests.GetChoicesOrderingTests.test_get_choices_reverse_related_field',
        'model_formsets_regress.tests.FormfieldShouldDeleteFormTests.test_custom_delete',
        'multiple_database.tests.RouterTestCase.test_generic_key_cross_database_protection',
        'ordering.tests.OrderingTests.test_order_by_fk_attname',
        'ordering.tests.OrderingTests.test_order_by_pk',
        'queries.test_bulk_update.BulkUpdateNoteTests.test_multiple_fields',
        'queries.test_bulk_update.BulkUpdateTests.test_inherited_fields',
        'queries.tests.Queries1Tests.test_ticket9411',
        'queries.tests.Ticket14056Tests.test_ticket_14056',
        'queries.tests.RelatedLookupTypeTests.test_values_queryset_lookup',
        'syndication_tests.tests.SyndicationFeedTest.test_rss2_feed',
        'syndication_tests.tests.SyndicationFeedTest.test_latest_post_date',
        'syndication_tests.tests.SyndicationFeedTest.test_rss091_feed',
        'syndication_tests.tests.SyndicationFeedTest.test_template_feed',
        # can't use QuerySet.dates() on DateTimeField:
        # https://github.com/orijtech/spanner-orm/issues/182
        'dates.tests.DatesTests.test_dates_trunc_datetime_fields',
        # datetimes retrieved from the database with the wrong hour when
        # USE_TZ = True: https://github.com/orijtech/spanner-orm/issues/193
        'datetimes.tests.DateTimesTests.test_21432',
        'timezones.tests.ForcedTimeZoneDatabaseTests.test_read_datetime'
        # Cursor.description returns None on raw queries:
        # https://github.com/orijtech/spanner-orm/issues/155
        'timezones.tests.LegacyDatabaseTests.test_raw_sql',
        'timezones.tests.NewDatabaseTests.test_raw_sql',
        # implement DatabaseOperations.date_interval_sql()
        # https://github.com/orijtech/spanner-orm/issues/184
        'timezones.tests.NewDatabaseTests.test_update_with_timedelta',
        # Unable to infer type for parameter:
        # https://github.com/orijtech/spanner-orm/issues/185
        'timezones.tests.LegacyDatabaseTests.test_cursor_execute_returns_naive_datetime',
        'timezones.tests.NewDatabaseTests.test_cursor_execute_returns_naive_datetime',
        # To be investigated...
        'timezones.tests.NewDatabaseTests.test_query_datetime_lookups',
        # extract() with timezone not working as expected:
        # https://github.com/orijtech/spanner-orm/issues/191
        'timezones.tests.NewDatabaseTests.test_query_datetimes',
        # To be investigated: https://github.com/orijtech/spanner-orm/issues/135
        'admin_changelist.tests.ChangeListTests.test_multiuser_edit',
        # FailedPrecondition and AlreadyExists should be raised as IntegrityError:
        # https://github.com/orijtech/spanner-orm/issues/154
        'model_fields.test_booleanfield.BooleanFieldTests.test_null_default',
        # Implement DatabaseOperations.datetime_cast_date_sql():
        # https://github.com/orijtech/spanner-orm/issues/170
        'model_fields.test_datetimefield.DateTimeFieldTests.test_lookup_date_with_use_tz',
        'model_fields.test_datetimefield.DateTimeFieldTests.test_lookup_date_without_use_tz',
        # DecimalField lookups crash:
        # https://github.com/orijtech/spanner-orm/issues/168
        'lookup.test_decimalfield.DecimalFieldLookupTests.test_gt',
        'lookup.test_decimalfield.DecimalFieldLookupTests.test_gte',
        'lookup.test_decimalfield.DecimalFieldLookupTests.test_lt',
        'lookup.test_decimalfield.DecimalFieldLookupTests.test_lte',
        'model_fields.test_decimalfield.DecimalFieldTests.test_filter_with_strings',
        # Spanner loses DecimalField precision due to conversion to float:
        # https://github.com/orijtech/spanner-orm/pull/133#pullrequestreview-328482925
        'model_fields.test_decimalfield.DecimalFieldTests.test_fetch_from_db_without_float_rounding',
        'model_fields.test_decimalfield.DecimalFieldTests.test_roundtrip_with_trailing_zeros',
        # No UNIQUE constraints in Spanner.
        'model_fields.test_filefield.FileFieldTests.test_unique_when_same_filename',
        # No CHECK constraints in Spanner.
        'model_fields.test_integerfield.PositiveIntegerFieldTests.test_negative_values',
        # No matching signature for function REGEXP_CONTAINS for argument
        # types: INT64, INT64: https://github.com/orijtech/spanner-orm/issues/177
        'lookup.tests.LookupTests.test_lookup_int_as_str',
        # 'DatabaseWrapper' object has no attribute 'pattern_ops'
        # https://github.com/orijtech/spanner-orm/issues/178
        'lookup.tests.LookupTests.test_pattern_lookups_with_substr',
    )
