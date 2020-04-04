# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.utils import InterfaceError


class DatabaseFeatures(BaseDatabaseFeatures):
    can_introspect_big_integer_field = False
    can_introspect_duration_field = False
    closed_cursor_error_class = InterfaceError
    # https://cloud.google.com/spanner/quotas#query_limits
    max_query_params = 950
    supports_foreign_keys = False
    supports_ignore_conflicts = False
    supports_partial_indexes = False
    supports_regex_backreferencing = False
    supports_timezones = False
    supports_transactions = False
    supports_column_check_constraints = False
    supports_table_check_constraints = False
    uses_savepoints = False

    # Django tests that aren't supported by Spanner.
    skip_tests = (
        # No foreign key constraints in Spanner.
        'backends.tests.FkConstraintsTests.test_check_constraints',
        'fixtures_regress.tests.TestFixtures.test_loaddata_raises_error_when_fixture_has_invalid_foreign_key',
        # No Django transaction management in Spanner.
        'basic.tests.SelectOnSaveTests.test_select_on_save_lying_update',
        # django_spanner monkey patches AutoField to have a default value.
        'basic.tests.ModelTest.test_hash',
        'm2m_through_regress.tests.ToFieldThroughTests.test_m2m_relations_unusable_on_null_pk_obj',
        'many_to_many.tests.ManyToManyTests.test_add',
        'many_to_one.tests.ManyToOneTests.test_fk_assignment_and_related_object_cache',
        'many_to_one.tests.ManyToOneTests.test_relation_unsaved',
        'model_fields.test_durationfield.TestSerialization.test_dumping',
        'model_fields.test_uuid.TestSerialization.test_dumping',
        'model_fields.test_booleanfield.ValidationTest.test_nullbooleanfield_blank',
        'one_to_one.tests.OneToOneTests.test_get_reverse_on_unsaved_object',
        'one_to_one.tests.OneToOneTests.test_set_reverse_on_unsaved_object',
        'one_to_one.tests.OneToOneTests.test_unsaved_object',
        'queries.test_bulk_update.BulkUpdateNoteTests.test_unsaved_models',
        'serializers.test_json.JsonSerializerTestCase.test_pkless_serialized_strings',
        'serializers.test_json.JsonSerializerTestCase.test_serialize_with_null_pk',
        'serializers.test_json.JsonSerializerTestCase.test_json_serializer_natural_keys',
        'serializers.test_json.JsonSerializerTestCase.test_python_serializer_natural_keys',
        'timezones.tests.LegacyDatabaseTests.test_cursor_execute_accepts_naive_datetime',
        'timezones.tests.NewDatabaseTests.test_cursor_execute_accepts_naive_datetime',
        'validation.test_custom_messages.CustomMessagesTests.test_custom_null_message',
        'validation.test_custom_messages.CustomMessagesTests.test_custom_simple_validator_message',
        'validation.test_unique.PerformUniqueChecksTest.test_primary_key_unique_check_not_performed_when_adding_and_pk_not_specified',  # noqa
        'validation.test_unique.PerformUniqueChecksTest.test_primary_key_unique_check_not_performed_when_not_adding',
        'validation.test_validators.TestModelsWithValidators.test_custom_validator_passes_for_correct_value',
        'validation.test_validators.TestModelsWithValidators.test_custom_validator_raises_error_for_incorrect_value',
        'validation.test_validators.TestModelsWithValidators.test_field_validators_can_be_any_iterable',
        # Tests that assume a serial pk.
        'admin_filters.tests.ListFiltersTests.test_booleanfieldlistfilter_nullbooleanfield',
        'admin_filters.tests.ListFiltersTests.test_booleanfieldlistfilter_tuple',
        'admin_filters.tests.ListFiltersTests.test_booleanfieldlistfilter',
        'admin_filters.tests.ListFiltersTests.test_datefieldlistfilter_with_time_zone_support',
        'admin_filters.tests.ListFiltersTests.test_datefieldlistfilter',
        'admin_filters.tests.ListFiltersTests.test_fieldlistfilter_underscorelookup_tuple',
        'admin_filters.tests.ListFiltersTests.test_fk_with_to_field',
        'admin_filters.tests.ListFiltersTests.test_listfilter_genericrelation',
        'admin_filters.tests.ListFiltersTests.test_lookup_with_non_string_value_underscored',
        'admin_filters.tests.ListFiltersTests.test_lookup_with_non_string_value',
        'admin_filters.tests.ListFiltersTests.test_relatedfieldlistfilter_manytomany',
        'admin_filters.tests.ListFiltersTests.test_simplelistfilter',
        'admin_inlines.tests.TestInline.test_inline_hidden_field_no_column',
        'admin_utils.test_logentry.LogEntryTests.test_logentry_change_message',
        'admin_utils.test_logentry.LogEntryTests.test_logentry_change_message_localized_datetime_input',
        'admin_utils.test_logentry.LogEntryTests.test_proxy_model_content_type_is_used_for_log_entries',
        'admin_views.tests.AdminViewPermissionsTest.test_history_view',
        'aggregation.test_filter_argument.FilteredAggregateTests.test_plain_annotate',
        'aggregation.tests.AggregateTestCase.test_annotate_basic',
        'aggregation.tests.AggregateTestCase.test_annotation',
        'aggregation.tests.AggregateTestCase.test_filtering',
        'aggregation_regress.tests.AggregationTests.test_more_more',
        'aggregation_regress.tests.AggregationTests.test_more_more_more',
        'aggregation_regress.tests.AggregationTests.test_ticket_11293',
        'defer_regress.tests.DeferRegressionTest.test_ticket_23270',
        'distinct_on_fields.tests.DistinctOnTests.test_basic_distinct_on',
        'generic_relations_regress.tests.GenericRelationTests.test_annotate',
        'get_earliest_or_latest.tests.TestFirstLast',
        'known_related_objects.tests.ExistingRelatedInstancesTests.test_reverse_one_to_one_multi_prefetch_related',
        'known_related_objects.tests.ExistingRelatedInstancesTests.test_reverse_one_to_one_multi_select_related',
        'lookup.tests.LookupTests.test_get_next_previous_by',
        'lookup.tests.LookupTests.test_values_list',
        'migrations.test_operations.OperationTests.test_alter_order_with_respect_to',
        'model_fields.tests.GetChoicesOrderingTests.test_get_choices_reverse_related_field',
        'model_formsets_regress.tests.FormfieldShouldDeleteFormTests.test_custom_delete',
        'multiple_database.tests.RouterTestCase.test_generic_key_cross_database_protection',
        'ordering.tests.OrderingTests.test_default_ordering_by_f_expression',
        'ordering.tests.OrderingTests.test_order_by_fk_attname',
        'ordering.tests.OrderingTests.test_order_by_override',
        'ordering.tests.OrderingTests.test_order_by_pk',
        'queries.test_bulk_update.BulkUpdateNoteTests.test_multiple_fields',
        'queries.test_bulk_update.BulkUpdateTests.test_inherited_fields',
        'queries.tests.Queries1Tests.test_ticket9411',
        'queries.tests.Queries4Tests.test_ticket15316_exclude_true',
        'queries.tests.Queries5Tests.test_ticket7256',
        'queries.tests.SubqueryTests.test_related_sliced_subquery',
        'queries.tests.Ticket14056Tests.test_ticket_14056',
        'queries.tests.RelatedLookupTypeTests.test_values_queryset_lookup',
        'raw_query.tests.RawQueryTests.test_annotations',
        'raw_query.tests.RawQueryTests.test_get_item',
        'select_related.tests.SelectRelatedTests.test_field_traversal',
        'syndication_tests.tests.SyndicationFeedTest.test_rss2_feed',
        'syndication_tests.tests.SyndicationFeedTest.test_latest_post_date',
        'syndication_tests.tests.SyndicationFeedTest.test_rss091_feed',
        'syndication_tests.tests.SyndicationFeedTest.test_template_feed',
        # datetimes retrieved from the database with the wrong hour when
        # USE_TZ = True: https://github.com/orijtech/spanner-orm/issues/193
        'datetimes.tests.DateTimesTests.test_21432',
        'db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_func_with_timezone',
        'db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_timezone_applied_before_truncation',  # noqa
        # extract() with timezone not working as expected:
        # https://github.com/orijtech/spanner-orm/issues/191
        'timezones.tests.NewDatabaseTests.test_query_datetimes',
        # using NULL with + crashes: https://github.com/orijtech/spanner-orm/issues/201
        'annotations.tests.NonAggregateAnnotationTestCase.test_combined_annotation_commutative',
        # Spanner loses DecimalField precision due to conversion to float:
        # https://github.com/orijtech/spanner-orm/pull/133#pullrequestreview-328482925
        'aggregation.tests.AggregateTestCase.test_decimal_max_digits_has_no_effect',
        'aggregation.tests.AggregateTestCase.test_related_aggregate',
        'db_functions.comparison.test_cast.CastTests.test_cast_to_decimal_field',
        'model_fields.test_decimalfield.DecimalFieldTests.test_fetch_from_db_without_float_rounding',
        'model_fields.test_decimalfield.DecimalFieldTests.test_roundtrip_with_trailing_zeros',
        # No CHECK constraints in Spanner.
        'model_fields.test_integerfield.PositiveIntegerFieldTests.test_negative_values',
        # 'DatabaseWrapper' object has no attribute 'pattern_ops'
        # https://github.com/orijtech/spanner-orm/issues/178
        'expressions.tests.BasicExpressionsTests.test_ticket_16731_startswith_lookup',
        'expressions.tests.ExpressionsTests.test_insensitive_patterns_escape',
        'expressions.tests.ExpressionsTests.test_patterns_escape',
        'lookup.tests.LookupTests.test_pattern_lookups_with_substr',
        # Spanner doesn't supoprt the variance the standard deviation database
        # functions:
        'aggregation.test_filter_argument.FilteredAggregateTests.test_filtered_numerical_aggregates',
        'aggregation_regress.tests.AggregationTests.test_stddev',
        # SELECT list expression references <column> which is neither grouped
        # nor aggregated: https://github.com/orijtech/spanner-orm/issues/245
        'aggregation_regress.tests.AggregationTests.test_annotated_conditional_aggregate',
        'aggregation_regress.tests.AggregationTests.test_annotation_with_value',
        'expressions.tests.BasicExpressionsTests.test_filtering_on_annotate_that_uses_q',
        # "No matching signature for operator" crash when comparing TIMESTAMP
        # and DATE: https://github.com/orijtech/django-spanner/issues/255
        'expressions.tests.BasicExpressionsTests.test_outerref_mixed_case_table_name',
        'expressions.tests.FTimeDeltaTests.test_mixed_comparisons1',
        # duration arithmetic fails with dates: No matching signature for
        # function TIMESTAMP_ADD: https://github.com/orijtech/django-spanner/issues/253
        'expressions.tests.FTimeDeltaTests.test_date_comparison',
        'expressions.tests.FTimeDeltaTests.test_date_minus_duration',
        'expressions.tests.FTimeDeltaTests.test_delta_add',
        'expressions.tests.FTimeDeltaTests.test_duration_with_datetime',
        'expressions.tests.FTimeDeltaTests.test_mixed_comparisons2',
        # integer division produces a float result, which can't be assigned to
        # an integer column:
        # https://github.com/orijtech/django-spanner/issues/331
        'expressions.tests.ExpressionOperatorTests.test_lefthand_division',
        'expressions.tests.ExpressionOperatorTests.test_right_hand_division',
        # power operator produces a float result, which can't be assigned to
        # an integer column:
        # https://github.com/orijtech/django-spanner/issues/331
        'expressions.tests.ExpressionOperatorTests.test_lefthand_power',
        'expressions.tests.ExpressionOperatorTests.test_righthand_power',
        # Cloud Spanner's docs: "The rows that are returned by LIMIT and OFFSET
        # is unspecified unless these operators are used after ORDER BY."
        'aggregation_regress.tests.AggregationTests.test_sliced_conditional_aggregate',
        'queries.tests.QuerySetBitwiseOperationTests.test_or_with_both_slice',
        'queries.tests.QuerySetBitwiseOperationTests.test_or_with_both_slice_and_ordering',
        'queries.tests.QuerySetBitwiseOperationTests.test_or_with_lhs_slice',
        'queries.tests.QuerySetBitwiseOperationTests.test_or_with_rhs_slice',
        'queries.tests.SubqueryTests.test_slice_subquery_and_query',
        # Cloud Spanner limit: "Number of functions exceeds the maximum
        # allowed limit of 1000."
        'queries.test_bulk_update.BulkUpdateTests.test_large_batch',
        # Spanner doesn't support random ordering.
        'ordering.tests.OrderingTests.test_random_ordering',
        # No matching signature for function MOD for argument types: FLOAT64,
        # FLOAT64. Supported signatures: MOD(INT64, INT64)
        'db_functions.math.test_mod.ModTests.test_decimal',
        'db_functions.math.test_mod.ModTests.test_float',
        # casting DateField to DateTimeField adds an unexpected hour:
        # https://github.com/orijtech/spanner-orm/issues/260
        'db_functions.comparison.test_cast.CastTests.test_cast_from_db_date_to_datetime',
        # Obscure error with auth_tests:
        # https://github.com/orijtech/spanner-orm/issues/271
        'auth_tests.test_admin_multidb.MultiDatabaseTests.test_add_view',
        # Tests that by-pass using django_spanner and generate
        # invalid DDL: https://github.com/orijtech/django-spanner/issues/298
        'cache.tests.CreateCacheTableForDBCacheTests',
        'cache.tests.DBCacheTests',
        'cache.tests.DBCacheWithTimeZoneTests',
        # Tests that require savepoints.
        'get_or_create.tests.UpdateOrCreateTests.test_integrity',
        'get_or_create.tests.UpdateOrCreateTests.test_manual_primary_key_test',
        'get_or_create.tests.UpdateOrCreateTestsWithManualPKs.test_create_with_duplicate_primary_key',
        'test_utils.tests.TestBadSetUpTestData.test_failure_in_setUpTestData_should_rollback_transaction',
        # Spanner doesn't support views.
        'inspectdb.tests.InspectDBTransactionalTests.test_include_views',
        'introspection.tests.IntrospectionTests.test_table_names_with_views',
        # No sequence for AutoField in Spanner.
        'introspection.tests.IntrospectionTests.test_sequence_list',
        # DatabaseIntrospection.get_key_columns() is only required if this
        # backend needs it (which it currently doesn't).
        'introspection.tests.IntrospectionTests.test_get_key_columns',
        # DatabaseIntrospection.get_relations() isn't implemented:
        # https://github.com/orijtech/django-spanner/issues/311
        'introspection.tests.IntrospectionTests.test_get_relations',
        # pyformat parameters not supported on INSERT:
        # https://github.com/orijtech/django-spanner/issues/343
        'backends.tests.BackendTestCase.test_cursor_execute_with_pyformat',
        'backends.tests.BackendTestCase.test_cursor_executemany_with_pyformat',
        'backends.tests.BackendTestCase.test_cursor_executemany_with_pyformat_iterator',
        # duplicate table raises GoogleAPICallError rather than DatabaseError:
        # https://github.com/orijtech/django-spanner/issues/344
        'backends.tests.BackendTestCase.test_duplicate_table_error',
        # Spanner limitation: Cannot change type of column.
        'schema.tests.SchemaTests.test_alter_auto_field_to_char_field',
        'schema.tests.SchemaTests.test_alter_text_field_to_date_field',
        'schema.tests.SchemaTests.test_alter_text_field_to_datetime_field',
        'schema.tests.SchemaTests.test_alter_text_field_to_time_field',
        # Spanner limitation: Cannot rename tables and columns.
        'migrations.test_operations.OperationTests.test_alter_fk_non_fk',
        'migrations.test_operations.OperationTests.test_alter_model_table',
        'migrations.test_operations.OperationTests.test_alter_model_table_m2m',
        'migrations.test_operations.OperationTests.test_rename_field',
        'migrations.test_operations.OperationTests.test_rename_field_reloads_state_on_fk_target_changes',
        'migrations.test_operations.OperationTests.test_rename_m2m_model_after_rename_field',
        'migrations.test_operations.OperationTests.test_rename_m2m_target_model',
        'migrations.test_operations.OperationTests.test_rename_m2m_through_model',
        'migrations.test_operations.OperationTests.test_rename_model',
        'migrations.test_operations.OperationTests.test_rename_model_with_m2m',
        'migrations.test_operations.OperationTests.test_rename_model_with_self_referential_fk',
        'migrations.test_operations.OperationTests.test_rename_model_with_self_referential_m2m',
        'migrations.test_operations.OperationTests.test_rename_model_with_superclass_fk',
        'migrations.test_operations.OperationTests.test_repoint_field_m2m',
        'schema.tests.SchemaTests.test_alter_db_table_case',
        'schema.tests.SchemaTests.test_alter_pk_with_self_referential_field',
        'schema.tests.SchemaTests.test_rename',
        'schema.tests.SchemaTests.test_db_table',
        'schema.tests.SchemaTests.test_m2m_rename_field_in_target_model',
        'schema.tests.SchemaTests.test_m2m_repoint',
        'schema.tests.SchemaTests.test_m2m_repoint_custom',
        'schema.tests.SchemaTests.test_m2m_repoint_inherited',
        'schema.tests.SchemaTests.test_rename_column_renames_deferred_sql_references',
        'schema.tests.SchemaTests.test_rename_keep_null_status',
        'schema.tests.SchemaTests.test_rename_referenced_field',
        'schema.tests.SchemaTests.test_rename_table_renames_deferred_sql_references',
        'schema.tests.SchemaTests.test_referenced_field_without_constraint_rename_inside_atomic_block',
        'schema.tests.SchemaTests.test_referenced_table_without_constraint_rename_inside_atomic_block',
        'schema.tests.SchemaTests.test_unique_name_quoting',
        # Spanner limitation: Cannot change a field to a primary key.
        'schema.tests.SchemaTests.test_alter_not_unique_field_to_primary_key',
        # Spanner limitation: Cannot drop column in primary key.
        'schema.tests.SchemaTests.test_primary_key',
        # Spanner limitation:  Cannot remove a column from the primary key.
        'schema.tests.SchemaTests.test_alter_int_pk_to_int_unique',
        # changing a not null constraint isn't allowed if it affects an index:
        # https://github.com/orijtech/django-spanner/issues/378
        'migrations.test_operations.OperationTests.test_alter_field_with_index',
        # parsing INSERT with one inlined value and one placeholder fails:
        # https://github.com/orijtech/django-spanner/issues/393
        'migrations.test_operations.OperationTests.test_run_sql_params',
        # This test doesn't flush the database properly:
        # https://code.djangoproject.com/ticket/31398
        'multiple_database.tests.AuthTestCase',
        # "Permission errors are not swallowed":
        # https://github.com/googleapis/python-spanner-django/issues/407
        'file_uploads.tests.DirectoryCreationTests.test_readonly_root',
        # Migrations data  persistance issue to be investigated:
        # https://github.com/googleapis/python-spanner-django/issues/408
        'migration_test_data_persistence.tests.MigrationDataNormalPersistenceTestCase.test_persistence',
    )
