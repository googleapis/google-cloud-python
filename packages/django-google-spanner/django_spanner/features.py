# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import os

from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.utils import InterfaceError


class DatabaseFeatures(BaseDatabaseFeatures):
    can_introspect_big_integer_field = False
    can_introspect_duration_field = False
    can_introspect_foreign_keys = False
    # TimeField is introspected as DateTimeField because they both use
    # TIMESTAMP.
    can_introspect_time_field = False
    closed_cursor_error_class = InterfaceError
    # Spanner uses REGEXP_CONTAINS which is case-sensitive.
    has_case_insensitive_like = False
    # https://cloud.google.com/spanner/quotas#query_limits
    max_query_params = 950
    supports_foreign_keys = False
    supports_ignore_conflicts = False
    supports_partial_indexes = False
    supports_regex_backreferencing = False
    supports_select_for_update_with_limit = False
    supports_sequence_reset = False
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
        'generic_relations.test_forms.GenericInlineFormsetTests.test_options',
        'generic_relations.tests.GenericRelationsTests.test_unsaved_instance_on_generic_foreign_key',
        'generic_relations_regress.tests.GenericRelationTests.test_target_model_is_unsaved',
        'm2m_through_regress.tests.ToFieldThroughTests.test_m2m_relations_unusable_on_null_pk_obj',
        'many_to_many.tests.ManyToManyTests.test_add',
        'many_to_one.tests.ManyToOneTests.test_fk_assignment_and_related_object_cache',
        'many_to_one.tests.ManyToOneTests.test_relation_unsaved',
        'model_fields.test_durationfield.TestSerialization.test_dumping',
        'model_fields.test_uuid.TestSerialization.test_dumping',
        'model_fields.test_booleanfield.ValidationTest.test_nullbooleanfield_blank',
        'model_inheritance.tests.ModelInheritanceTests.test_create_child_no_update',
        'model_regress.tests.ModelTests.test_get_next_prev_by_field_unsaved',
        'one_to_one.tests.OneToOneTests.test_get_reverse_on_unsaved_object',
        'one_to_one.tests.OneToOneTests.test_set_reverse_on_unsaved_object',
        'one_to_one.tests.OneToOneTests.test_unsaved_object',
        'queries.test_bulk_update.BulkUpdateNoteTests.test_unsaved_models',
        'serializers.test_json.JsonSerializerTestCase.test_pkless_serialized_strings',
        'serializers.test_json.JsonSerializerTestCase.test_serialize_with_null_pk',
        'serializers.test_xml.XmlSerializerTestCase.test_pkless_serialized_strings',
        'serializers.test_xml.XmlSerializerTestCase.test_serialize_with_null_pk',
        'serializers.test_yaml.YamlSerializerTestCase.test_pkless_serialized_strings',
        'serializers.test_yaml.YamlSerializerTestCase.test_serialize_with_null_pk',
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
        'extra_regress.tests.ExtraRegressTests.test_regression_7314_7372',
        'generic_relations_regress.tests.GenericRelationTests.test_annotate',
        'get_earliest_or_latest.tests.TestFirstLast',
        'known_related_objects.tests.ExistingRelatedInstancesTests.test_reverse_one_to_one_multi_prefetch_related',
        'known_related_objects.tests.ExistingRelatedInstancesTests.test_reverse_one_to_one_multi_select_related',
        'lookup.tests.LookupTests.test_get_next_previous_by',
        'lookup.tests.LookupTests.test_values_list',
        'migrations.test_operations.OperationTests.test_alter_order_with_respect_to',
        'model_fields.tests.GetChoicesOrderingTests.test_get_choices_reverse_related_field',
        'model_formsets.tests.ModelFormsetTest.test_custom_pk',
        'model_formsets_regress.tests.FormfieldShouldDeleteFormTests.test_custom_delete',
        'multiple_database.tests.RouterTestCase.test_generic_key_cross_database_protection',
        'ordering.tests.OrderingTests.test_default_ordering_by_f_expression',
        'ordering.tests.OrderingTests.test_order_by_fk_attname',
        'ordering.tests.OrderingTests.test_order_by_override',
        'ordering.tests.OrderingTests.test_order_by_pk',
        'prefetch_related.test_prefetch_related_objects.PrefetchRelatedObjectsTests.test_m2m_then_m2m',
        'prefetch_related.tests.CustomPrefetchTests.test_custom_qs',
        'prefetch_related.tests.CustomPrefetchTests.test_nested_prefetch_related_are_not_overwritten',
        'prefetch_related.tests.DirectPrefechedObjectCacheReuseTests.test_detect_is_fetched',
        'prefetch_related.tests.DirectPrefechedObjectCacheReuseTests.test_detect_is_fetched_with_to_attr',
        'prefetch_related.tests.ForeignKeyToFieldTest.test_m2m',
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
        # contains lookup crashes with bilateral transform:
        # https://github.com/googleapis/python-spanner-django/issues/419
        'custom_lookups.tests.BilateralTransformTests.test_bilateral_upper',
        # Spanner doesn't support the variance the standard deviation database
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
        # This test doesn't raise NotSupportedError because Spanner doesn't
        # support select for update either (besides the "with limit"
        # restriction).
        'select_for_update.tests.SelectForUpdateTests.test_unsupported_select_for_update_with_limit',
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
        # Tests that fail during tear down on databases that don't support
        # transactions: https://github.com/orijtech/spanner-orm/issues/271
        'admin_views.test_multidb.MultiDatabaseTests.test_add_view',
        'admin_views.test_multidb.MultiDatabaseTests.test_change_view',
        'admin_views.test_multidb.MultiDatabaseTests.test_delete_view',
        'auth_tests.test_admin_multidb.MultiDatabaseTests.test_add_view',
        'contenttypes_tests.test_models.ContentTypesMultidbTests.test_multidb',
        # Tests that by-pass using django_spanner and generate
        # invalid DDL: https://github.com/orijtech/django-spanner/issues/298
        'cache.tests.CreateCacheTableForDBCacheTests',
        'cache.tests.DBCacheTests',
        'cache.tests.DBCacheWithTimeZoneTests',
        # Tests that require transactions.
        'transaction_hooks.tests.TestConnectionOnCommit.test_does_not_execute_if_transaction_rolled_back',
        'transaction_hooks.tests.TestConnectionOnCommit.test_hooks_cleared_after_rollback',
        'transaction_hooks.tests.TestConnectionOnCommit.test_hooks_cleared_on_reconnect',
        'transaction_hooks.tests.TestConnectionOnCommit.test_no_hooks_run_from_failed_transaction',
        'transaction_hooks.tests.TestConnectionOnCommit.test_no_savepoints_atomic_merged_with_outer',
        # Tests that require savepoints.
        'get_or_create.tests.UpdateOrCreateTests.test_integrity',
        'get_or_create.tests.UpdateOrCreateTests.test_manual_primary_key_test',
        'get_or_create.tests.UpdateOrCreateTestsWithManualPKs.test_create_with_duplicate_primary_key',
        'test_utils.tests.TestBadSetUpTestData.test_failure_in_setUpTestData_should_rollback_transaction',
        'transaction_hooks.tests.TestConnectionOnCommit.test_discards_hooks_from_rolled_back_savepoint',
        'transaction_hooks.tests.TestConnectionOnCommit.test_inner_savepoint_rolled_back_with_outer',
        'transaction_hooks.tests.TestConnectionOnCommit.test_inner_savepoint_does_not_affect_outer',
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
        'migrations.test_commands.MigrateTests.test_migrate_fake_initial',
        'migrations.test_commands.MigrateTests.test_migrate_initial_false',
        'migrations.test_executor.ExecutorTests.test_soft_apply',
        # Spanner limitation: Cannot change type of column.
        'migrations.test_executor.ExecutorTests.test_alter_id_type_with_fk',
        'schema.tests.SchemaTests.test_alter_auto_field_to_char_field',
        'schema.tests.SchemaTests.test_alter_text_field_to_date_field',
        'schema.tests.SchemaTests.test_alter_text_field_to_datetime_field',
        'schema.tests.SchemaTests.test_alter_text_field_to_time_field',
        # Spanner limitation: Cannot rename tables and columns.
        'contenttypes_tests.test_operations.ContentTypeOperationsTests',
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
        # Spanner limitation: migrations aren't atomic since Spanner doesn't
        # support transactions.
        'migrations.test_executor.ExecutorTests.test_atomic_operation_in_non_atomic_migration',
        # changing a not null constraint isn't allowed if it affects an index:
        # https://github.com/orijtech/django-spanner/issues/378
        'migrations.test_operations.OperationTests.test_alter_field_with_index',
        # parsing INSERT with one inlined value and one placeholder fails:
        # https://github.com/orijtech/django-spanner/issues/393
        'migrations.test_operations.OperationTests.test_run_sql_params',
        # This test doesn't flush the database properly:
        # https://code.djangoproject.com/ticket/31398
        'multiple_database.tests.AuthTestCase',
        # This test isn't isolated on databases like Spanner that don't
        # support transactions: https://code.djangoproject.com/ticket/31413
        'migrations.test_loader.LoaderTests.test_loading_squashed',
        # Probably due to django-spanner setting a default on AutoField:
        # https://github.com/googleapis/python-spanner-django/issues/422
        'model_inheritance_regress.tests.ModelInheritanceTest.test_issue_6755',
        # Probably due to django-spanner setting a default on AutoField:
        # https://github.com/googleapis/python-spanner-django/issues/424
        'model_formsets.tests.ModelFormsetTest.test_prevent_change_outer_model_and_create_invalid_data',
        'model_formsets_regress.tests.FormfieldShouldDeleteFormTests.test_no_delete',
        'model_formsets_regress.tests.FormsetTests.test_extraneous_query_is_not_run',
    )
    # Kokoro-specific skips.
    if os.environ.get('KOKORO_JOB_NAME'):
        skip_tests += (
            # os.chmod() doesn't work on Kokoro?
            'file_uploads.tests.DirectoryCreationTests.test_readonly_root',
            # Tests that sometimes fail on Kokoro for unknown reasons.
            'contenttypes_tests.test_models.ContentTypesTests.test_cache_not_shared_between_managers',
            'migration_test_data_persistence.tests.MigrationDataNormalPersistenceTestCase.test_persistence',
            'servers.test_liveserverthread.LiveServerThreadTest.test_closes_connections',
        )

    if os.environ.get('SPANNER_EMULATOR_HOST', None):
        # Some code isn't yet supported by the Spanner emulator.
        skip_tests += (
            # Untyped parameters are not supported:
            # https://github.com/GoogleCloudPlatform/cloud-spanner-emulator#features-and-limitations
            'admin_changelist.test_date_hierarchy.DateHierarchyTests.test_bounded_params',  # noqa
            'admin_changelist.test_date_hierarchy.DateHierarchyTests.test_bounded_params_with_time_zone',  # noqa
            'admin_changelist.test_date_hierarchy.DateHierarchyTests.test_invalid_params',  # noqa
            'admin_changelist.tests.ChangeListTests.test_builtin_lookup_in_search_fields',  # noqa
            'admin_changelist.tests.ChangeListTests.test_changelist_view_list_editable_changed_objects_uses_filter',  # noqa
            'admin_changelist.tests.ChangeListTests.test_computed_list_display_localization',  # noqa
            'admin_changelist.tests.ChangeListTests.test_custom_lookup_in_search_fields',  # noqa
            'admin_changelist.tests.ChangeListTests.test_custom_lookup_with_pk_shortcut',  # noqa
            'admin_changelist.tests.ChangeListTests.test_custom_paginator',  # noqa
            'admin_changelist.tests.ChangeListTests.test_deterministic_order_for_model_ordered_by_its_manager',  # noqa
            'admin_changelist.tests.ChangeListTests.test_deterministic_order_for_unordered_model',  # noqa
            'admin_changelist.tests.ChangeListTests.test_distinct_for_inherited_m2m_in_list_filter',  # noqa
            'admin_changelist.tests.ChangeListTests.test_distinct_for_m2m_in_list_filter',  # noqa
            'admin_changelist.tests.ChangeListTests.test_distinct_for_m2m_to_inherited_in_list_filter',  # noqa
            'admin_changelist.tests.ChangeListTests.test_distinct_for_many_to_many_at_second_level_in_search_fields',  # noqa
            'admin_changelist.tests.ChangeListTests.test_distinct_for_non_unique_related_object_in_list_filter',  # noqa
            'admin_changelist.tests.ChangeListTests.test_distinct_for_non_unique_related_object_in_search_fields',  # noqa
            'admin_changelist.tests.ChangeListTests.test_distinct_for_through_m2m_at_second_level_in_list_filter',  # noqa
            'admin_changelist.tests.ChangeListTests.test_distinct_for_through_m2m_in_list_filter',  # noqa
            'admin_changelist.tests.ChangeListTests.test_dynamic_list_display',  # noqa
            'admin_changelist.tests.ChangeListTests.test_dynamic_list_display_links',  # noqa
            'admin_changelist.tests.ChangeListTests.test_dynamic_list_filter',  # noqa
            'admin_changelist.tests.ChangeListTests.test_dynamic_search_fields',  # noqa
            'admin_changelist.tests.ChangeListTests.test_get_edited_object_ids',  # noqa
            'admin_changelist.tests.ChangeListTests.test_get_list_editable_queryset',  # noqa
            'admin_changelist.tests.ChangeListTests.test_get_list_editable_queryset_with_regex_chars_in_prefix',  # noqa
            'admin_changelist.tests.ChangeListTests.test_get_select_related_custom_method',  # noqa
            'admin_changelist.tests.ChangeListTests.test_multiuser_edit',  # noqa
            'admin_changelist.tests.ChangeListTests.test_no_distinct_for_m2m_in_list_filter_without_params',  # noqa
            'admin_changelist.tests.ChangeListTests.test_no_list_display_links',  # noqa
            'admin_changelist.tests.ChangeListTests.test_object_tools_displayed_no_add_permission',  # noqa
            'admin_changelist.tests.ChangeListTests.test_pagination',  # noqa
            'admin_changelist.tests.ChangeListTests.test_pagination_page_range',  # noqa
            'admin_changelist.tests.ChangeListTests.test_pk_in_search_fields',  # noqa
            'admin_changelist.tests.ChangeListTests.test_result_list_editable',  # noqa
            'admin_changelist.tests.ChangeListTests.test_result_list_editable_html',  # noqa
            'admin_changelist.tests.ChangeListTests.test_result_list_empty_changelist_value',  # noqa
            'admin_changelist.tests.ChangeListTests.test_result_list_html',  # noqa
            'admin_changelist.tests.ChangeListTests.test_result_list_set_empty_value_display_in_model_admin',  # noqa
            'admin_changelist.tests.ChangeListTests.test_result_list_set_empty_value_display_on_admin_site',  # noqa
            'admin_changelist.tests.ChangeListTests.test_select_related_as_empty_tuple',  # noqa
            'admin_changelist.tests.ChangeListTests.test_select_related_as_tuple',  # noqa
            'admin_changelist.tests.ChangeListTests.test_select_related_preserved',  # noqa
            'admin_changelist.tests.ChangeListTests.test_show_all',  # noqa
            'admin_changelist.tests.ChangeListTests.test_spanning_relations_with_custom_lookup_in_search_fields',  # noqa
            'admin_changelist.tests.ChangeListTests.test_specified_ordering_by_f_expression',  # noqa
            'admin_changelist.tests.ChangeListTests.test_specified_ordering_by_f_expression_without_asc_desc',  # noqa
            'admin_changelist.tests.ChangeListTests.test_total_ordering_optimization',  # noqa
            'admin_changelist.tests.ChangeListTests.test_tuple_list_display',  # noqa
            'admin_changelist.tests.GetAdminLogTests.test_no_user',  # noqa
            'admin_custom_urls.tests.AdminCustomUrlsTest.test_add_with_GET_args',  # noqa
            'admin_custom_urls.tests.AdminCustomUrlsTest.test_admin_URLs_no_clash',  # noqa
            'admin_custom_urls.tests.AdminCustomUrlsTest.test_basic_add_GET',  # noqa
            'admin_custom_urls.tests.AdminCustomUrlsTest.test_basic_add_POST',  # noqa
            'admin_custom_urls.tests.AdminCustomUrlsTest.test_post_save_add_redirect',  # noqa
            'admin_custom_urls.tests.AdminCustomUrlsTest.test_post_save_change_redirect',  # noqa
            'admin_custom_urls.tests.AdminCustomUrlsTest.test_post_url_continue',  # noqa
            'admin_docs.test_middleware.XViewMiddlewareTest.test_callable_object_view',  # noqa
            'admin_docs.test_middleware.XViewMiddlewareTest.test_xview_class',  # noqa
            'admin_docs.test_middleware.XViewMiddlewareTest.test_xview_func',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_bookmarklets',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_index',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_missing_docutils',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_model_index',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_namespaced_view_detail',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_no_sites_framework',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_template_detail',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_templatefilter_index',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_templatetag_index',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_view_detail',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_view_detail_as_method',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_view_detail_illegal_import',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_view_index',  # noqa
            'admin_docs.test_views.AdminDocViewTests.test_view_index_with_method',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_bookmarklets',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_index',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_missing_docutils',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_model_index',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_namespaced_view_detail',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_no_sites_framework',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_template_detail',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_templatefilter_index',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_templatetag_index',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_view_detail',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_view_detail_as_method',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_view_detail_illegal_import',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_view_index',  # noqa
            'admin_docs.test_views.AdminDocViewWithMultipleEngines.test_view_index_with_method',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_app_not_found',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_descriptions_render_correctly',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_instance_of_property_methods_are_displayed',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_method_data_types',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_method_excludes',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_methods_with_arguments',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_methods_with_arguments_display_arguments',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_methods_with_arguments_display_arguments_default_value',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_methods_with_multiple_arguments_display_arguments',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_model_detail_title',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_model_docstring_renders_correctly',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_model_not_found',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_model_with_many_to_one',  # noqa
            'admin_docs.test_views.TestModelDetailView.test_model_with_no_backward_relations_render_only_relevant_fields',  # noqa
            'admin_inlines.tests.TestInline.test_callable_lookup',  # noqa
            'admin_inlines.tests.TestInline.test_can_delete',  # noqa
            'admin_inlines.tests.TestInline.test_create_inlines_on_inherited_model',  # noqa
            'admin_inlines.tests.TestInline.test_custom_form_tabular_inline_label',  # noqa
            'admin_inlines.tests.TestInline.test_custom_form_tabular_inline_overridden_label',  # noqa
            'admin_inlines.tests.TestInline.test_custom_get_extra_form',  # noqa
            'admin_inlines.tests.TestInline.test_custom_min_num',  # noqa
            'admin_inlines.tests.TestInline.test_custom_pk_shortcut',  # noqa
            'admin_inlines.tests.TestInline.test_help_text',  # noqa
            'admin_inlines.tests.TestInline.test_inline_editable_pk',  # noqa
            'admin_inlines.tests.TestInline.test_inline_nonauto_noneditable_inherited_pk',  # noqa
            'admin_inlines.tests.TestInline.test_inline_nonauto_noneditable_pk',  # noqa
            'admin_inlines.tests.TestInline.test_inline_primary',  # noqa
            'admin_inlines.tests.TestInline.test_inlines_show_change_link_registered',  # noqa
            'admin_inlines.tests.TestInline.test_inlines_show_change_link_unregistered',  # noqa
            'admin_inlines.tests.TestInline.test_localize_pk_shortcut',  # noqa
            'admin_inlines.tests.TestInline.test_many_to_many_inlines',  # noqa
            'admin_inlines.tests.TestInline.test_min_num',  # noqa
            'admin_inlines.tests.TestInline.test_no_parent_callable_lookup',  # noqa
            'admin_inlines.tests.TestInline.test_non_related_name_inline',  # noqa
            'admin_inlines.tests.TestInline.test_noneditable_inline_has_field_inputs',  # noqa
            'admin_inlines.tests.TestInline.test_readonly_stacked_inline_label',  # noqa
            'admin_inlines.tests.TestInline.test_stacked_inline_edit_form_contains_has_original_class',  # noqa
            'admin_inlines.tests.TestInline.test_tabular_inline_column_css_class',  # noqa
            'admin_inlines.tests.TestInline.test_tabular_inline_show_change_link_false_registered',  # noqa
            'admin_inlines.tests.TestInline.test_tabular_model_form_meta_readonly_field',  # noqa
            'admin_inlines.tests.TestInline.test_tabular_non_field_errors',  # noqa
            'admin_inlines.tests.TestInlineMedia.test_all_inline_media',  # noqa
            'admin_inlines.tests.TestInlineMedia.test_inline_media_only_base',  # noqa
            'admin_inlines.tests.TestInlineMedia.test_inline_media_only_inline',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_add_fk_add_perm',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_add_fk_noperm',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_add_m2m_add_perm',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_add_m2m_noperm',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_add_m2m_view_only_perm',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_change_fk_add_change_perm',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_change_fk_add_perm',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_change_fk_all_perms',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_change_fk_change_del_perm',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_change_fk_change_perm',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_change_fk_noperm',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_change_m2m_add_perm',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_change_m2m_change_perm',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_change_m2m_noperm',  # noqa
            'admin_inlines.tests.TestInlinePermissions.test_inline_change_m2m_view_only_perm',  # noqa
            'admin_inlines.tests.TestInlineProtectedOnDelete.test_deleting_inline_with_protected_delete_does_not_validate',  # noqa
            'admin_inlines.tests.TestReadOnlyChangeViewInlinePermissions.test_add_url_not_allowed',  # noqa
            'admin_inlines.tests.TestReadOnlyChangeViewInlinePermissions.test_extra_inlines_are_not_shown',  # noqa
            'admin_inlines.tests.TestReadOnlyChangeViewInlinePermissions.test_get_to_change_url_is_allowed',  # noqa
            'admin_inlines.tests.TestReadOnlyChangeViewInlinePermissions.test_inline_delete_buttons_are_not_shown',  # noqa
            'admin_inlines.tests.TestReadOnlyChangeViewInlinePermissions.test_inlines_are_rendered_as_read_only',  # noqa
            'admin_inlines.tests.TestReadOnlyChangeViewInlinePermissions.test_main_model_is_rendered_as_read_only',  # noqa
            'admin_inlines.tests.TestReadOnlyChangeViewInlinePermissions.test_post_to_change_url_not_allowed',  # noqa
            'admin_inlines.tests.TestReadOnlyChangeViewInlinePermissions.test_submit_line_shows_only_close_button',  # noqa
            'admin_ordering.tests.TestAdminOrdering.test_dynamic_ordering',  # noqa
            'aggregation.tests.AggregateTestCase.test_add_implementation',  # noqa
            'aggregation.tests.AggregateTestCase.test_aggregate_alias',  # noqa
            'aggregation.tests.AggregateTestCase.test_aggregate_annotation',  # noqa
            'aggregation.tests.AggregateTestCase.test_aggregate_in_order_by',  # noqa
            'aggregation.tests.AggregateTestCase.test_aggregate_multi_join',  # noqa
            'aggregation.tests.AggregateTestCase.test_aggregate_over_complex_annotation',  # noqa
            'aggregation.tests.AggregateTestCase.test_aggregation_expressions',  # noqa
            'aggregation.tests.AggregateTestCase.test_annotate_defer',  # noqa
            'aggregation.tests.AggregateTestCase.test_annotate_defer_select_related',  # noqa
            'aggregation.tests.AggregateTestCase.test_annotate_m2m',  # noqa
            'aggregation.tests.AggregateTestCase.test_annotate_ordering',  # noqa
            'aggregation.tests.AggregateTestCase.test_annotate_over_annotate',  # noqa
            'aggregation.tests.AggregateTestCase.test_annotate_values',  # noqa
            'aggregation.tests.AggregateTestCase.test_annotate_values_aggregate',  # noqa
            'aggregation.tests.AggregateTestCase.test_annotate_values_list',  # noqa
            'aggregation.tests.AggregateTestCase.test_annotated_aggregate_over_annotated_aggregate',  # noqa
            'aggregation.tests.AggregateTestCase.test_annotation_expressions',  # noqa
            'aggregation.tests.AggregateTestCase.test_arguments_must_be_expressions',  # noqa
            'aggregation.tests.AggregateTestCase.test_avg_decimal_field',  # noqa
            'aggregation.tests.AggregateTestCase.test_avg_duration_field',  # noqa
            'aggregation.tests.AggregateTestCase.test_backwards_m2m_annotate',  # noqa
            'aggregation.tests.AggregateTestCase.test_combine_different_types',  # noqa
            'aggregation.tests.AggregateTestCase.test_complex_aggregations_require_kwarg',  # noqa
            'aggregation.tests.AggregateTestCase.test_complex_values_aggregation',  # noqa
            'aggregation.tests.AggregateTestCase.test_count',  # noqa
            'aggregation.tests.AggregateTestCase.test_count_distinct_expression',  # noqa
            'aggregation.tests.AggregateTestCase.test_count_star',  # noqa
            'aggregation.tests.AggregateTestCase.test_dates_with_aggregation',  # noqa
            'aggregation.tests.AggregateTestCase.test_empty_aggregate',  # noqa
            'aggregation.tests.AggregateTestCase.test_even_more_aggregate',  # noqa
            'aggregation.tests.AggregateTestCase.test_expression_on_aggregation',  # noqa
            'aggregation.tests.AggregateTestCase.test_filter_aggregate',  # noqa
            'aggregation.tests.AggregateTestCase.test_fkey_aggregate',  # noqa
            'aggregation.tests.AggregateTestCase.test_grouped_annotation_in_group_by',  # noqa
            'aggregation.tests.AggregateTestCase.test_missing_output_field_raises_error',  # noqa
            'aggregation.tests.AggregateTestCase.test_more_aggregation',  # noqa
            'aggregation.tests.AggregateTestCase.test_multi_arg_aggregate',  # noqa
            'aggregation.tests.AggregateTestCase.test_multiple_aggregates',  # noqa
            'aggregation.tests.AggregateTestCase.test_non_grouped_annotation_not_in_group_by',  # noqa
            'aggregation.tests.AggregateTestCase.test_nonaggregate_aggregation_throws',  # noqa
            'aggregation.tests.AggregateTestCase.test_nonfield_annotation',  # noqa
            'aggregation.tests.AggregateTestCase.test_order_of_precedence',  # noqa
            'aggregation.tests.AggregateTestCase.test_reverse_fkey_annotate',  # noqa
            'aggregation.tests.AggregateTestCase.test_single_aggregate',  # noqa
            'aggregation.tests.AggregateTestCase.test_sum_distinct_aggregate',  # noqa
            'aggregation.tests.AggregateTestCase.test_sum_duration_field',  # noqa
            'aggregation.tests.AggregateTestCase.test_ticket11881',  # noqa
            'aggregation.tests.AggregateTestCase.test_ticket12886',  # noqa
            'aggregation.tests.AggregateTestCase.test_ticket17424',  # noqa
            'aggregation.tests.AggregateTestCase.test_values_aggregation',  # noqa
            'aggregation.tests.AggregateTestCase.test_values_annotation_with_expression',  # noqa
            'aggregation_regress.tests.JoinPromotionTests.test_ticket_21150',  # noqa
            'aggregation_regress.tests.SelfReferentialFKTests.test_ticket_24748',  # noqa
            'annotations.tests.NonAggregateAnnotationTestCase.test_custom_functions',  # noqa
            'annotations.tests.NonAggregateAnnotationTestCase.test_custom_functions_can_ref_other_functions',  # noqa
            'auth_tests.test_auth_backends.AllowAllUsersModelBackendTest.test_authenticate',  # noqa
            'auth_tests.test_auth_backends.AllowAllUsersModelBackendTest.test_get_user',  # noqa
            'auth_tests.test_auth_backends.AuthenticateTests.test_skips_backends_without_arguments',  # noqa
            'auth_tests.test_auth_backends.AuthenticateTests.test_type_error_raised',  # noqa
            'auth_tests.test_auth_backends.ChangedBackendSettingsTest.test_changed_backend_settings',  # noqa
            'auth_tests.test_auth_backends.CustomPermissionsUserModelBackendTest.test_anonymous_has_no_permissions',  # noqa
            'auth_tests.test_auth_backends.CustomPermissionsUserModelBackendTest.test_authentication_timing',  # noqa
            'auth_tests.test_auth_backends.CustomPermissionsUserModelBackendTest.test_custom_perms',  # noqa
            'auth_tests.test_auth_backends.CustomPermissionsUserModelBackendTest.test_get_all_superuser_permissions',  # noqa
            'auth_tests.test_auth_backends.CustomPermissionsUserModelBackendTest.test_has_no_object_perm',  # noqa
            'auth_tests.test_auth_backends.CustomPermissionsUserModelBackendTest.test_has_perm',  # noqa
            'auth_tests.test_auth_backends.CustomPermissionsUserModelBackendTest.test_inactive_has_no_permissions',  # noqa
            'auth_tests.test_auth_backends.CustomUserModelBackendAuthenticateTest.test_authenticate',  # noqa
            'auth_tests.test_auth_backends.ExtensionUserModelBackendTest.test_anonymous_has_no_permissions',  # noqa
            'auth_tests.test_auth_backends.ExtensionUserModelBackendTest.test_authentication_timing',  # noqa
            'auth_tests.test_auth_backends.ExtensionUserModelBackendTest.test_custom_perms',  # noqa
            'auth_tests.test_auth_backends.ExtensionUserModelBackendTest.test_get_all_superuser_permissions',  # noqa
            'auth_tests.test_auth_backends.ExtensionUserModelBackendTest.test_has_no_object_perm',  # noqa
            'auth_tests.test_auth_backends.ExtensionUserModelBackendTest.test_has_perm',  # noqa
            'auth_tests.test_auth_backends.ExtensionUserModelBackendTest.test_inactive_has_no_permissions',  # noqa
            'auth_tests.test_auth_backends.ImportedBackendTests.test_backend_path',  # noqa
            'auth_tests.test_auth_backends.ImproperlyConfiguredUserModelTest.test_does_not_shadow_exception',  # noqa
            'auth_tests.test_auth_backends.InActiveUserBackendTest.test_has_module_perms',  # noqa
            'auth_tests.test_auth_backends.InActiveUserBackendTest.test_has_perm',  # noqa
            'auth_tests.test_auth_backends.ModelBackendTest.test_anonymous_has_no_permissions',  # noqa
            'auth_tests.test_auth_backends.ModelBackendTest.test_authenticate_inactive',  # noqa
            'auth_tests.test_auth_backends.ModelBackendTest.test_authenticate_user_without_is_active_field',  # noqa
            'auth_tests.test_auth_backends.ModelBackendTest.test_authentication_timing',  # noqa
            'auth_tests.test_auth_backends.ModelBackendTest.test_custom_perms',  # noqa
            'auth_tests.test_auth_backends.ModelBackendTest.test_get_all_superuser_permissions',  # noqa
            'auth_tests.test_auth_backends.ModelBackendTest.test_has_no_object_perm',  # noqa
            'auth_tests.test_auth_backends.ModelBackendTest.test_has_perm',  # noqa
            'auth_tests.test_auth_backends.ModelBackendTest.test_inactive_has_no_permissions',  # noqa
            'auth_tests.test_auth_backends.NoBackendsTest.test_raises_exception',  # noqa
            'auth_tests.test_auth_backends.PermissionDeniedBackendTest.test_authenticates',  # noqa
            'auth_tests.test_auth_backends.PermissionDeniedBackendTest.test_has_perm',  # noqa
            'auth_tests.test_auth_backends.PermissionDeniedBackendTest.test_has_perm_denied',  # noqa
            'auth_tests.test_auth_backends.PermissionDeniedBackendTest.test_permission_denied',  # noqa
            'auth_tests.test_auth_backends.RowlevelBackendTest.test_get_all_permissions',  # noqa
            'auth_tests.test_auth_backends.RowlevelBackendTest.test_get_group_permissions',  # noqa
            'auth_tests.test_auth_backends.RowlevelBackendTest.test_has_perm',  # noqa
            'auth_tests.test_auth_backends.SelectingBackendTests.test_backend_path_login_with_explicit_backends',  # noqa
            'auth_tests.test_auth_backends.SelectingBackendTests.test_backend_path_login_without_authenticate_multiple_backends',  # noqa
            'auth_tests.test_auth_backends.SelectingBackendTests.test_backend_path_login_without_authenticate_single_backend',  # noqa
            'auth_tests.test_auth_backends.SelectingBackendTests.test_non_string_backend',  # noqa
            'auth_tests.test_auth_backends.UUIDUserTests.test_login',  # noqa
            'auth_tests.test_basic.BasicTestCase.test_superuser',  # noqa
            'auth_tests.test_basic.BasicTestCase.test_unicode_username',  # noqa
            'auth_tests.test_basic.BasicTestCase.test_user',  # noqa
            'auth_tests.test_basic.BasicTestCase.test_user_no_email',  # noqa
            'auth_tests.test_basic.TestGetUser.test_get_user',  # noqa
            'auth_tests.test_context_processors.AuthContextProcessorTests.test_message_attrs',  # noqa
            'auth_tests.test_context_processors.AuthContextProcessorTests.test_perm_in_perms_attrs',  # noqa
            'auth_tests.test_context_processors.AuthContextProcessorTests.test_perms_attrs',  # noqa
            'auth_tests.test_context_processors.AuthContextProcessorTests.test_session_is_accessed',  # noqa
            'auth_tests.test_context_processors.AuthContextProcessorTests.test_session_not_accessed',  # noqa
            'auth_tests.test_context_processors.AuthContextProcessorTests.test_user_attrs',  # noqa
            'auth_tests.test_decorators.LoginRequiredTestCase.testCallable',  # noqa
            'auth_tests.test_decorators.LoginRequiredTestCase.testLoginRequired',  # noqa
            'auth_tests.test_decorators.LoginRequiredTestCase.testLoginRequiredNextUrl',  # noqa
            'auth_tests.test_decorators.LoginRequiredTestCase.testView',  # noqa
            'auth_tests.test_decorators.PermissionsRequiredDecoratorTest.test_many_permissions_in_set_pass',  # noqa
            'auth_tests.test_decorators.PermissionsRequiredDecoratorTest.test_many_permissions_pass',  # noqa
            'auth_tests.test_decorators.PermissionsRequiredDecoratorTest.test_permissioned_denied_exception_raised',  # noqa
            'auth_tests.test_decorators.PermissionsRequiredDecoratorTest.test_permissioned_denied_redirect',  # noqa
            'auth_tests.test_decorators.PermissionsRequiredDecoratorTest.test_single_permission_pass',  # noqa
            'auth_tests.test_forms.AdminPasswordChangeFormTest.test_missing_passwords',  # noqa
            'auth_tests.test_forms.AdminPasswordChangeFormTest.test_non_matching_passwords',  # noqa
            'auth_tests.test_forms.AdminPasswordChangeFormTest.test_one_password',  # noqa
            'auth_tests.test_forms.AdminPasswordChangeFormTest.test_password_whitespace_not_stripped',  # noqa
            'auth_tests.test_forms.AdminPasswordChangeFormTest.test_success',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_custom_login_allowed_policy',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_get_invalid_login_error',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_inactive_user',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_inactive_user_i18n',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_inactive_user_incorrect_password',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_integer_username',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_invalid_username',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_login_failed',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_password_whitespace_not_stripped',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_success',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_unicode_username',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_username_field_label',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_username_field_label_empty_string',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_username_field_label_not_set',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_username_field_max_length_defaults_to_254',  # noqa
            'auth_tests.test_forms.AuthenticationFormTest.test_username_field_max_length_matches_user_model',  # noqa
            'auth_tests.test_forms.PasswordChangeFormTest.test_field_order',  # noqa
            'auth_tests.test_forms.PasswordChangeFormTest.test_incorrect_password',  # noqa
            'auth_tests.test_forms.PasswordChangeFormTest.test_password_verification',  # noqa
            'auth_tests.test_forms.PasswordChangeFormTest.test_password_whitespace_not_stripped',  # noqa
            'auth_tests.test_forms.PasswordChangeFormTest.test_success',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_cleaned_data',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_custom_email_constructor',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_custom_email_field',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_custom_email_subject',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_inactive_user',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_invalid_email',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_nonexistent_email',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_preserve_username_case',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_save_html_email_template_name',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_save_plaintext_email',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_unusable_password',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_user_email_domain_unicode_collision',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_user_email_domain_unicode_collision_nonexistent',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_user_email_unicode_collision',  # noqa
            'auth_tests.test_forms.PasswordResetFormTest.test_user_email_unicode_collision_nonexistent',  # noqa
            'auth_tests.test_forms.SetPasswordFormTest.test_help_text_translation',  # noqa
            'auth_tests.test_forms.SetPasswordFormTest.test_password_verification',  # noqa
            'auth_tests.test_forms.SetPasswordFormTest.test_password_whitespace_not_stripped',  # noqa
            'auth_tests.test_forms.SetPasswordFormTest.test_success',  # noqa
            'auth_tests.test_forms.SetPasswordFormTest.test_validates_password',  # noqa
            'auth_tests.test_forms.UserChangeFormTest.test_bug_14242',  # noqa
            'auth_tests.test_forms.UserChangeFormTest.test_bug_17944_empty_password',  # noqa
            'auth_tests.test_forms.UserChangeFormTest.test_bug_17944_unknown_password_algorithm',  # noqa
            'auth_tests.test_forms.UserChangeFormTest.test_bug_17944_unmanageable_password',  # noqa
            'auth_tests.test_forms.UserChangeFormTest.test_bug_19133',  # noqa
            'auth_tests.test_forms.UserChangeFormTest.test_bug_19349_bound_password_field',  # noqa
            'auth_tests.test_forms.UserChangeFormTest.test_custom_form',  # noqa
            'auth_tests.test_forms.UserChangeFormTest.test_password_excluded',  # noqa
            'auth_tests.test_forms.UserChangeFormTest.test_unusable_password',  # noqa
            'auth_tests.test_forms.UserChangeFormTest.test_username_validity',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_both_passwords',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_custom_form',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_custom_form_hidden_username_field',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_custom_form_with_different_username_field',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_duplicate_normalized_unicode',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_invalid_data',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_normalize_username',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_password_help_text',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_password_verification',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_password_whitespace_not_stripped',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_success',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_unicode_username',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_user_already_exists',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_user_create_form_validates_password_with_all_data',  # noqa
            'auth_tests.test_forms.UserCreationFormTest.test_validates_password',  # noqa
            'auth_tests.test_handlers.ModWsgiHandlerTestCase.test_check_password',  # noqa
            'auth_tests.test_handlers.ModWsgiHandlerTestCase.test_check_password_custom_user',  # noqa
            'auth_tests.test_handlers.ModWsgiHandlerTestCase.test_groups_for_user',  # noqa
            'auth_tests.test_management.ChangepasswordManagementCommandTestCase.test_get_pass',  # noqa
            'auth_tests.test_management.ChangepasswordManagementCommandTestCase.test_get_pass_no_input',  # noqa
            'auth_tests.test_management.ChangepasswordManagementCommandTestCase.test_nonexistent_username',  # noqa
            'auth_tests.test_management.ChangepasswordManagementCommandTestCase.test_password_validation',  # noqa
            'auth_tests.test_management.ChangepasswordManagementCommandTestCase.test_system_username',  # noqa
            'auth_tests.test_management.ChangepasswordManagementCommandTestCase.test_that_changepassword_command_changes_joes_password',  # noqa
            'auth_tests.test_management.ChangepasswordManagementCommandTestCase.test_that_changepassword_command_works_with_nonascii_output',  # noqa
            'auth_tests.test_management.ChangepasswordManagementCommandTestCase.test_that_max_tries_exits_1',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_basic_usage',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_default_username',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_email_in_username',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_existing_username',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_existing_username_non_interactive',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_existing_username_provided_via_option_and_interactive',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_fields_with_fk',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_fields_with_fk_interactive',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_invalid_username',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_non_ascii_verbose_name',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_passing_stdin',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_password_validation',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_password_validation_bypass',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_swappable_user',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_swappable_user_username_non_unique',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_validate_password_against_required_fields',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_validate_password_against_username',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_validation_blank_password_entered',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_validation_mismatched_passwords',  # noqa
            'auth_tests.test_management.CreatesuperuserManagementCommandTestCase.test_verbosity_zero',  # noqa
            'auth_tests.test_management.GetDefaultUsernameTestCase.test_existing',  # noqa
            'auth_tests.test_management.MultiDBChangepasswordManagementCommandTestCase.test_that_changepassword_command_with_database_option_uses_given_db',  # noqa
            'auth_tests.test_management.MultiDBCreatesuperuserTestCase.test_createsuperuser_command_with_database_option',  # noqa
            'auth_tests.test_middleware.TestAuthenticationMiddleware.test_changed_password_invalidates_session',  # noqa
            'auth_tests.test_middleware.TestAuthenticationMiddleware.test_no_password_change_doesnt_invalidate_session',  # noqa
            'auth_tests.test_migrations.ProxyModelWithDifferentAppLabelTests.test_user_has_now_proxy_model_permissions',  # noqa
            'auth_tests.test_migrations.ProxyModelWithDifferentAppLabelTests.test_user_keeps_same_permissions_after_migrating_backward',  # noqa
            'auth_tests.test_migrations.ProxyModelWithSameAppLabelTests.test_user_keeps_same_permissions_after_migrating_backward',  # noqa
            'auth_tests.test_migrations.ProxyModelWithSameAppLabelTests.test_user_still_has_proxy_model_permissions',  # noqa
            'auth_tests.test_mixins.AccessMixinTests.test_access_mixin_permission_denied_response',  # noqa
            'auth_tests.test_mixins.AccessMixinTests.test_stacked_mixins_missing_permission',  # noqa
            'auth_tests.test_mixins.AccessMixinTests.test_stacked_mixins_not_logged_in',  # noqa
            'auth_tests.test_mixins.AccessMixinTests.test_stacked_mixins_success',  # noqa
            'auth_tests.test_mixins.LoginRequiredMixinTests.test_login_required',  # noqa
            'auth_tests.test_mixins.PermissionsRequiredMixinTests.test_many_permissions_pass',  # noqa
            'auth_tests.test_mixins.PermissionsRequiredMixinTests.test_permissioned_denied_exception_raised',  # noqa
            'auth_tests.test_mixins.PermissionsRequiredMixinTests.test_permissioned_denied_redirect',  # noqa
            'auth_tests.test_mixins.PermissionsRequiredMixinTests.test_single_permission_pass',  # noqa
            'auth_tests.test_models.AbstractUserTestCase.test_check_password_upgrade',  # noqa
            'auth_tests.test_models.AbstractUserTestCase.test_last_login_default',  # noqa
            'auth_tests.test_models.AbstractUserTestCase.test_user_double_save',  # noqa
            'auth_tests.test_models.IsActiveTestCase.test_builtin_user_isactive',  # noqa
            'auth_tests.test_models.IsActiveTestCase.test_is_active_field_default',  # noqa
            'auth_tests.test_models.NaturalKeysTestCase.test_user_natural_key',  # noqa
            'auth_tests.test_models.TestCreateSuperUserSignals.test_create_superuser',  # noqa
            'auth_tests.test_models.TestCreateSuperUserSignals.test_create_user',  # noqa
            'auth_tests.test_models.UserManagerTestCase.test_create_user',  # noqa
            'auth_tests.test_models.UserManagerTestCase.test_create_user_is_staff',  # noqa
            'auth_tests.test_remote_user.AllowAllUsersRemoteUserBackendTest.test_header_disappears',  # noqa
            'auth_tests.test_remote_user.AllowAllUsersRemoteUserBackendTest.test_inactive_user',  # noqa
            'auth_tests.test_remote_user.AllowAllUsersRemoteUserBackendTest.test_known_user',  # noqa
            'auth_tests.test_remote_user.AllowAllUsersRemoteUserBackendTest.test_last_login',  # noqa
            'auth_tests.test_remote_user.AllowAllUsersRemoteUserBackendTest.test_unknown_user',  # noqa
            'auth_tests.test_remote_user.AllowAllUsersRemoteUserBackendTest.test_user_switch_forces_new_login',  # noqa
            'auth_tests.test_remote_user.CustomHeaderRemoteUserTest.test_header_disappears',  # noqa
            'auth_tests.test_remote_user.CustomHeaderRemoteUserTest.test_inactive_user',  # noqa
            'auth_tests.test_remote_user.CustomHeaderRemoteUserTest.test_known_user',  # noqa
            'auth_tests.test_remote_user.CustomHeaderRemoteUserTest.test_last_login',  # noqa
            'auth_tests.test_remote_user.CustomHeaderRemoteUserTest.test_unknown_user',  # noqa
            'auth_tests.test_remote_user.CustomHeaderRemoteUserTest.test_user_switch_forces_new_login',  # noqa
            'auth_tests.test_remote_user.PersistentRemoteUserTest.test_header_disappears',  # noqa
            'auth_tests.test_remote_user.PersistentRemoteUserTest.test_inactive_user',  # noqa
            'auth_tests.test_remote_user.PersistentRemoteUserTest.test_known_user',  # noqa
            'auth_tests.test_remote_user.PersistentRemoteUserTest.test_last_login',  # noqa
            'auth_tests.test_remote_user.PersistentRemoteUserTest.test_unknown_user',  # noqa
            'auth_tests.test_remote_user.PersistentRemoteUserTest.test_user_switch_forces_new_login',  # noqa
            'auth_tests.test_remote_user.RemoteUserCustomTest.test_header_disappears',  # noqa
            'auth_tests.test_remote_user.RemoteUserCustomTest.test_inactive_user',  # noqa
            'auth_tests.test_remote_user.RemoteUserCustomTest.test_known_user',  # noqa
            'auth_tests.test_remote_user.RemoteUserCustomTest.test_last_login',  # noqa
            'auth_tests.test_remote_user.RemoteUserCustomTest.test_unknown_user',  # noqa
            'auth_tests.test_remote_user.RemoteUserCustomTest.test_user_switch_forces_new_login',  # noqa
            'auth_tests.test_remote_user.RemoteUserNoCreateTest.test_header_disappears',  # noqa
            'auth_tests.test_remote_user.RemoteUserNoCreateTest.test_inactive_user',  # noqa
            'auth_tests.test_remote_user.RemoteUserNoCreateTest.test_known_user',  # noqa
            'auth_tests.test_remote_user.RemoteUserNoCreateTest.test_last_login',  # noqa
            'auth_tests.test_remote_user.RemoteUserNoCreateTest.test_user_switch_forces_new_login',  # noqa
            'auth_tests.test_remote_user.RemoteUserTest.test_header_disappears',  # noqa
            'auth_tests.test_remote_user.RemoteUserTest.test_inactive_user',  # noqa
            'auth_tests.test_remote_user.RemoteUserTest.test_known_user',  # noqa
            'auth_tests.test_remote_user.RemoteUserTest.test_last_login',  # noqa
            'auth_tests.test_remote_user.RemoteUserTest.test_unknown_user',  # noqa
            'auth_tests.test_remote_user.RemoteUserTest.test_user_switch_forces_new_login',  # noqa
            'auth_tests.test_remote_user_deprecation.RemoteUserCustomTest.test_configure_user_deprecation_warning',  # noqa
            'auth_tests.test_signals.SignalTestCase.test_failed_login_without_request',  # noqa
            'auth_tests.test_signals.SignalTestCase.test_login',  # noqa
            'auth_tests.test_signals.SignalTestCase.test_login_with_custom_user_without_last_login_field',  # noqa
            'auth_tests.test_signals.SignalTestCase.test_logout',  # noqa
            'auth_tests.test_signals.SignalTestCase.test_logout_anonymous',  # noqa
            'auth_tests.test_signals.SignalTestCase.test_update_last_login',  # noqa
            'auth_tests.test_templates.AuthTemplateTests.test_PasswordChangeDoneView',  # noqa
            'auth_tests.test_templates.AuthTemplateTests.test_PasswordResetChangeView',  # noqa
            'auth_tests.test_templates.AuthTemplateTests.test_PasswordResetCompleteView',  # noqa
            'auth_tests.test_templates.AuthTemplateTests.test_PasswordResetConfirmView_invalid_token',  # noqa
            'auth_tests.test_templates.AuthTemplateTests.test_PasswordResetConfirmView_valid_token',  # noqa
            'auth_tests.test_templates.AuthTemplateTests.test_PasswordResetDoneView',  # noqa
            'auth_tests.test_templates.AuthTemplateTests.test_PasswordResetView',  # noqa
            'auth_tests.test_tokens.TokenGeneratorTest.test_10265',  # noqa
            'auth_tests.test_tokens.TokenGeneratorTest.test_check_token_with_nonexistent_token_and_user',  # noqa
            'auth_tests.test_tokens.TokenGeneratorTest.test_make_token',  # noqa
            'auth_tests.test_tokens.TokenGeneratorTest.test_timeout',  # noqa
            'auth_tests.test_tokens.TokenGeneratorTest.test_token_with_different_secret',  # noqa
            'auth_tests.test_validators.UserAttributeSimilarityValidatorTest.test_validate',  # noqa
            'auth_tests.test_views.AuthViewNamedURLTests.test_named_urls',  # noqa
            'auth_tests.test_views.ChangePasswordTest.test_password_change_done_fails',  # noqa
            'auth_tests.test_views.ChangePasswordTest.test_password_change_done_succeeds',  # noqa
            'auth_tests.test_views.ChangePasswordTest.test_password_change_fails_with_invalid_old_password',  # noqa
            'auth_tests.test_views.ChangePasswordTest.test_password_change_fails_with_mismatched_passwords',  # noqa
            'auth_tests.test_views.ChangePasswordTest.test_password_change_redirect_custom',  # noqa
            'auth_tests.test_views.ChangePasswordTest.test_password_change_redirect_custom_named',  # noqa
            'auth_tests.test_views.ChangePasswordTest.test_password_change_redirect_default',  # noqa
            'auth_tests.test_views.ChangePasswordTest.test_password_change_succeeds',  # noqa
            'auth_tests.test_views.ChangelistTests.test_changelist_disallows_password_lookups',  # noqa
            'auth_tests.test_views.ChangelistTests.test_password_change_bad_url',  # noqa
            'auth_tests.test_views.ChangelistTests.test_user_change_different_user_password',  # noqa
            'auth_tests.test_views.ChangelistTests.test_user_change_email',  # noqa
            'auth_tests.test_views.ChangelistTests.test_user_change_password',  # noqa
            'auth_tests.test_views.ChangelistTests.test_user_change_password_passes_user_to_has_change_permission',  # noqa
            'auth_tests.test_views.ChangelistTests.test_user_not_change',  # noqa
            'auth_tests.test_views.ChangelistTests.test_view_user_password_is_readonly',  # noqa
            'auth_tests.test_views.CustomUserPasswordResetTest.test_confirm_valid_custom_user',  # noqa
            'auth_tests.test_views.LoginRedirectAuthenticatedUser.test_default',  # noqa
            'auth_tests.test_views.LoginRedirectAuthenticatedUser.test_guest',  # noqa
            'auth_tests.test_views.LoginRedirectAuthenticatedUser.test_permission_required_logged_in',  # noqa
            'auth_tests.test_views.LoginRedirectAuthenticatedUser.test_permission_required_not_logged_in',  # noqa
            'auth_tests.test_views.LoginRedirectAuthenticatedUser.test_redirect',  # noqa
            'auth_tests.test_views.LoginRedirectAuthenticatedUser.test_redirect_loop',  # noqa
            'auth_tests.test_views.LoginRedirectAuthenticatedUser.test_redirect_param',  # noqa
            'auth_tests.test_views.LoginRedirectAuthenticatedUser.test_redirect_url',  # noqa
            'auth_tests.test_views.LoginRedirectUrlTest.test_custom',  # noqa
            'auth_tests.test_views.LoginRedirectUrlTest.test_default',  # noqa
            'auth_tests.test_views.LoginRedirectUrlTest.test_named',  # noqa
            'auth_tests.test_views.LoginRedirectUrlTest.test_remote',  # noqa
            'auth_tests.test_views.LoginSuccessURLAllowedHostsTest.test_success_url_allowed_hosts_safe_host',  # noqa
            'auth_tests.test_views.LoginSuccessURLAllowedHostsTest.test_success_url_allowed_hosts_same_host',  # noqa
            'auth_tests.test_views.LoginSuccessURLAllowedHostsTest.test_success_url_allowed_hosts_unsafe_host',  # noqa
            'auth_tests.test_views.LoginTest.test_current_site_in_context_after_login',  # noqa
            'auth_tests.test_views.LoginTest.test_login_csrf_rotate',  # noqa
            'auth_tests.test_views.LoginTest.test_login_form_contains_request',  # noqa
            'auth_tests.test_views.LoginTest.test_login_session_without_hash_session_key',  # noqa
            'auth_tests.test_views.LoginTest.test_security_check',  # noqa
            'auth_tests.test_views.LoginTest.test_security_check_https',  # noqa
            'auth_tests.test_views.LoginTest.test_session_key_flushed_on_login',  # noqa
            'auth_tests.test_views.LoginTest.test_session_key_flushed_on_login_after_password_change',  # noqa
            'auth_tests.test_views.LoginURLSettings.test_https_login_url',  # noqa
            'auth_tests.test_views.LoginURLSettings.test_lazy_login_url',  # noqa
            'auth_tests.test_views.LoginURLSettings.test_login_url_with_querystring',  # noqa
            'auth_tests.test_views.LoginURLSettings.test_named_login_url',  # noqa
            'auth_tests.test_views.LoginURLSettings.test_remote_login_url',  # noqa
            'auth_tests.test_views.LoginURLSettings.test_remote_login_url_with_next_querystring',  # noqa
            'auth_tests.test_views.LoginURLSettings.test_standard_login_url',  # noqa
            'auth_tests.test_views.LogoutTest.test_14377',  # noqa
            'auth_tests.test_views.LogoutTest.test_logout_default',  # noqa
            'auth_tests.test_views.LogoutTest.test_logout_doesnt_cache',  # noqa
            'auth_tests.test_views.LogoutTest.test_logout_preserve_language',  # noqa
            'auth_tests.test_views.LogoutTest.test_logout_redirect_url_named_setting',  # noqa
            'auth_tests.test_views.LogoutTest.test_logout_redirect_url_setting',  # noqa
            'auth_tests.test_views.LogoutTest.test_logout_with_custom_redirect_argument',  # noqa
            'auth_tests.test_views.LogoutTest.test_logout_with_named_redirect',  # noqa
            'auth_tests.test_views.LogoutTest.test_logout_with_next_page_specified',  # noqa
            'auth_tests.test_views.LogoutTest.test_logout_with_overridden_redirect_url',  # noqa
            'auth_tests.test_views.LogoutTest.test_logout_with_post',  # noqa
            'auth_tests.test_views.LogoutTest.test_logout_with_redirect_argument',  # noqa
            'auth_tests.test_views.LogoutTest.test_security_check',  # noqa
            'auth_tests.test_views.LogoutTest.test_security_check_https',  # noqa
            'auth_tests.test_views.LogoutTest.test_success_url_allowed_hosts_safe_host',  # noqa
            'auth_tests.test_views.LogoutTest.test_success_url_allowed_hosts_same_host',  # noqa
            'auth_tests.test_views.LogoutTest.test_success_url_allowed_hosts_unsafe_host',  # noqa
            'auth_tests.test_views.LogoutThenLoginTests.test_default_logout_then_login',  # noqa
            'auth_tests.test_views.LogoutThenLoginTests.test_logout_then_login_with_custom_login',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_complete',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_different_passwords',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_display_user_from_form',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_invalid',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_invalid_hash',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_invalid_post',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_invalid_user',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_link_redirects_to_set_password_page',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_login_post_reset',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_login_post_reset_already_logged_in',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_login_post_reset_custom_backend',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_overflow_user',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_redirect_custom',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_redirect_custom_named',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_redirect_default',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_confirm_valid',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_email_found',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_email_found_custom_from',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_email_not_found',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_extra_email_context',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_html_mail_template',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_invalid_link_if_going_directly_to_the_final_reset_password_url',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_poisoned_http_host',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_poisoned_http_host_admin_site',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_reset_custom_redirect',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_reset_custom_redirect_named',  # noqa
            'auth_tests.test_views.PasswordResetTest.test_reset_redirect_default',  # noqa
            'auth_tests.test_views.RedirectToLoginTests.test_redirect_to_login_with_lazy',  # noqa
            'auth_tests.test_views.RedirectToLoginTests.test_redirect_to_login_with_lazy_and_unicode',  # noqa
            'auth_tests.test_views.SessionAuthenticationTests.test_user_password_change_updates_session',  # noqa
            'auth_tests.test_views.UUIDUserPasswordResetTest.test_confirm_invalid_uuid',  # noqa
            'auth_tests.test_views.UUIDUserPasswordResetTest.test_confirm_valid_custom_user',  # noqa
            'auth_tests.test_views.UUIDUserTests.test_admin_password_change',  # noqa
            'backends.tests.FkConstraintsTests.test_disable_constraint_checks_context_manager',  # noqa
            'backends.tests.FkConstraintsTests.test_disable_constraint_checks_manually',  # noqa
            'backends.tests.FkConstraintsTests.test_integrity_checks_on_creation',  # noqa
            'backends.tests.FkConstraintsTests.test_integrity_checks_on_update',  # noqa
            'basic.tests.ModelTest.test_ticket_20278',
            'basic.tests.ModelRefreshTests.test_lookup_in_fields',
            'basic.tests.ModelRefreshTests.test_prefetched_cache_cleared',
            'basic.tests.ModelRefreshTests.test_lookup_in_fields',
            'basic.tests.ModelRefreshTests.test_prefetched_cache_cleared',
            'basic.tests.ModelRefreshTests.test_refresh_fk',
            'basic.tests.ModelRefreshTests.test_refresh_fk_on_delete_set_null',
            'basic.tests.ModelRefreshTests.test_refresh_null_fk',
            'basic.tests.ModelRefreshTests.test_unknown_kwarg',
            'bulk_create.tests.BulkCreateTests.test_bulk_insert_nullable_fields',  # noqa
            'custom_pk.tests.CustomPKTests.test_required_pk',  # noqa
            'custom_pk.tests.CustomPKTests.test_unique_pk',  # noqa
            'datatypes.tests.DataTypesTestCase.test_boolean_type',  # noqa
            'datatypes.tests.DataTypesTestCase.test_date_type',  # noqa
            'datatypes.tests.DataTypesTestCase.test_textfields_str',  # noqa
            'datatypes.tests.DataTypesTestCase.test_time_field',  # noqa
            'datatypes.tests.DataTypesTestCase.test_year_boundaries',  # noqa
            'dates.tests.DatesTests.test_related_model_traverse',  # noqa
            'datetimes.tests.DateTimesTests.test_datetimes_has_lazy_iterator',  # noqa
            'datetimes.tests.DateTimesTests.test_datetimes_returns_available_dates_for_given_scope_and_given_field',  # noqa
            'datetimes.tests.DateTimesTests.test_related_model_traverse',  # noqa
            'db_functions.comparison.test_cast.CastTests.test_cast_from_db_datetime_to_date',  # noqa
            'db_functions.comparison.test_cast.CastTests.test_cast_from_db_datetime_to_date_group_by',  # noqa
            'db_functions.comparison.test_cast.CastTests.test_cast_from_db_datetime_to_time',  # noqa
            'db_functions.comparison.test_cast.CastTests.test_cast_from_field',  # noqa
            'db_functions.comparison.test_cast.CastTests.test_cast_from_python',  # noqa
            'db_functions.comparison.test_cast.CastTests.test_cast_from_python_to_date',  # noqa
            'db_functions.comparison.test_cast.CastTests.test_cast_from_python_to_datetime',  # noqa
            'db_functions.comparison.test_cast.CastTests.test_cast_from_value',  # noqa
            'db_functions.comparison.test_cast.CastTests.test_cast_to_char_field_with_max_length',  # noqa
            'db_functions.comparison.test_cast.CastTests.test_cast_to_char_field_without_max_length',  # noqa
            'db_functions.comparison.test_cast.CastTests.test_cast_to_integer',  # noqa
            'db_functions.comparison.test_cast.CastTests.test_cast_to_text_field',  # noqa
            'db_functions.comparison.test_coalesce.CoalesceTests.test_basic',  # noqa
            'db_functions.comparison.test_coalesce.CoalesceTests.test_mixed_values',  # noqa
            'db_functions.comparison.test_coalesce.CoalesceTests.test_ordering',  # noqa
            'db_functions.comparison.test_greatest.GreatestTests.test_all_null',  # noqa
            'db_functions.comparison.test_greatest.GreatestTests.test_basic',  # noqa
            'db_functions.comparison.test_greatest.GreatestTests.test_coalesce_workaround',  # noqa
            'db_functions.comparison.test_greatest.GreatestTests.test_propagates_null',  # noqa
            'db_functions.comparison.test_greatest.GreatestTests.test_related_field',  # noqa
            'db_functions.comparison.test_greatest.GreatestTests.test_update',  # noqa
            'db_functions.comparison.test_least.LeastTests.test_all_null',  # noqa
            'db_functions.comparison.test_least.LeastTests.test_basic',  # noqa
            'db_functions.comparison.test_least.LeastTests.test_coalesce_workaround',  # noqa
            'db_functions.comparison.test_least.LeastTests.test_propagates_null',  # noqa
            'db_functions.comparison.test_least.LeastTests.test_related_field',  # noqa
            'db_functions.comparison.test_least.LeastTests.test_update',  # noqa
            'db_functions.comparison.test_nullif.NullIfTests.test_basic',  # noqa
            'db_functions.comparison.test_nullif.NullIfTests.test_null_argument',  # noqa
            'db_functions.comparison.test_nullif.NullIfTests.test_too_few_args',  # noqa
            'db_functions.datetime.test_extract_trunc.DateFunctionTests.test_extract_none',  # noqa
            'db_functions.datetime.test_extract_trunc.DateFunctionTests.test_trunc_date_none',  # noqa
            'db_functions.datetime.test_extract_trunc.DateFunctionTests.test_trunc_none',  # noqa
            'db_functions.datetime.test_extract_trunc.DateFunctionTests.test_trunc_subquery_with_parameters',  # noqa
            'db_functions.datetime.test_extract_trunc.DateFunctionTests.test_trunc_time_func',  # noqa
            'db_functions.datetime.test_extract_trunc.DateFunctionTests.test_trunc_time_none',  # noqa
            'db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_extract_none',  # noqa
            'db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_date_none',  # noqa
            'db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_none',  # noqa
            'db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_subquery_with_parameters',  # noqa
            'db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_time_func',  # noqa
            'db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_time_none',  # noqa
            'db_functions.datetime.test_now.NowTests.test_basic',  # noqa
            'db_functions.math.test_abs.AbsTests.test_null',  # noqa
            'db_functions.math.test_acos.ACosTests.test_null',  # noqa
            'db_functions.math.test_asin.ASinTests.test_null',  # noqa
            'db_functions.math.test_atan.ATanTests.test_null',  # noqa
            'db_functions.math.test_atan2.ATan2Tests.test_null',  # noqa
            'db_functions.math.test_ceil.CeilTests.test_decimal',  # noqa
            'db_functions.math.test_ceil.CeilTests.test_float',  # noqa
            'db_functions.math.test_ceil.CeilTests.test_integer',  # noqa
            'db_functions.math.test_ceil.CeilTests.test_null',  # noqa
            'db_functions.math.test_ceil.CeilTests.test_transform',  # noqa
            'db_functions.math.test_cos.CosTests.test_null',  # noqa
            'db_functions.math.test_cot.CotTests.test_null',  # noqa
            'db_functions.math.test_degrees.DegreesTests.test_null',  # noqa
            'db_functions.math.test_exp.ExpTests.test_null',  # noqa
            'db_functions.math.test_floor.FloorTests.test_null',  # noqa
            'db_functions.math.test_ln.LnTests.test_null',  # noqa
            'db_functions.math.test_log.LogTests.test_null',  # noqa
            'db_functions.math.test_mod.ModTests.test_null',  # noqa
            'db_functions.math.test_power.PowerTests.test_decimal',  # noqa
            'db_functions.math.test_power.PowerTests.test_float',  # noqa
            'db_functions.math.test_power.PowerTests.test_integer',  # noqa
            'db_functions.math.test_power.PowerTests.test_null',  # noqa
            'db_functions.math.test_radians.RadiansTests.test_null',  # noqa
            'db_functions.math.test_round.RoundTests.test_null',  # noqa
            'db_functions.math.test_sin.SinTests.test_null',  # noqa
            'db_functions.math.test_sqrt.SqrtTests.test_null',  # noqa
            'db_functions.math.test_tan.TanTests.test_null',  # noqa
            'db_functions.tests.FunctionTests.test_func_transform_bilateral',  # noqa
            'db_functions.tests.FunctionTests.test_func_transform_bilateral_multivalue',  # noqa
            'db_functions.tests.FunctionTests.test_function_as_filter',  # noqa
            'db_functions.tests.FunctionTests.test_nested_function_ordering',  # noqa
            'db_functions.text.test_chr.ChrTests.test_basic',  # noqa
            'db_functions.text.test_chr.ChrTests.test_non_ascii',  # noqa
            'db_functions.text.test_chr.ChrTests.test_transform',  # noqa
            'db_functions.text.test_concat.ConcatTests.test_basic',  # noqa
            'db_functions.text.test_concat.ConcatTests.test_many',  # noqa
            'db_functions.text.test_concat.ConcatTests.test_mixed_char_text',  # noqa
            'db_functions.text.test_left.LeftTests.test_basic',  # noqa
            'db_functions.text.test_left.LeftTests.test_expressions',  # noqa
            'db_functions.text.test_left.LeftTests.test_invalid_length',  # noqa
            'db_functions.text.test_length.LengthTests.test_basic',  # noqa
            'db_functions.text.test_length.LengthTests.test_ordering',  # noqa
            'db_functions.text.test_length.LengthTests.test_transform',  # noqa
            'db_functions.text.test_lower.LowerTests.test_basic',  # noqa
            'db_functions.text.test_lower.LowerTests.test_transform',  # noqa
            'db_functions.text.test_ord.OrdTests.test_basic',  # noqa
            'db_functions.text.test_ord.OrdTests.test_transform',  # noqa
            'db_functions.text.test_pad.PadTests.test_combined_with_length',  # noqa
            'db_functions.text.test_pad.PadTests.test_pad',  # noqa
            'db_functions.text.test_repeat.RepeatTests.test_basic',  # noqa
            'db_functions.text.test_replace.ReplaceTests.test_case_sensitive',  # noqa
            'db_functions.text.test_replace.ReplaceTests.test_replace_expression',  # noqa
            'db_functions.text.test_replace.ReplaceTests.test_replace_with_default_arg',  # noqa
            'db_functions.text.test_replace.ReplaceTests.test_replace_with_empty_string',  # noqa
            'db_functions.text.test_replace.ReplaceTests.test_update',  # noqa
            'db_functions.text.test_reverse.ReverseTests.test_basic',  # noqa
            'db_functions.text.test_reverse.ReverseTests.test_expressions',  # noqa
            'db_functions.text.test_reverse.ReverseTests.test_null',  # noqa
            'db_functions.text.test_reverse.ReverseTests.test_transform',  # noqa
            'db_functions.text.test_right.RightTests.test_basic',  # noqa
            'db_functions.text.test_right.RightTests.test_expressions',  # noqa
            'db_functions.text.test_right.RightTests.test_invalid_length',  # noqa
            'db_functions.text.test_strindex.StrIndexTests.test_annotate_charfield',  # noqa
            'db_functions.text.test_strindex.StrIndexTests.test_annotate_textfield',  # noqa
            'db_functions.text.test_strindex.StrIndexTests.test_filtering',  # noqa
            'db_functions.text.test_strindex.StrIndexTests.test_order_by',  # noqa
            'db_functions.text.test_strindex.StrIndexTests.test_unicode_values',  # noqa
            'db_functions.text.test_substr.SubstrTests.test_basic',  # noqa
            'db_functions.text.test_substr.SubstrTests.test_expressions',  # noqa
            'db_functions.text.test_substr.SubstrTests.test_start',  # noqa
            'db_functions.text.test_trim.TrimTests.test_trim',  # noqa
            'db_functions.text.test_trim.TrimTests.test_trim_transform',  # noqa
            'db_functions.text.test_upper.UpperTests.test_basic',  # noqa
            'db_functions.text.test_upper.UpperTests.test_transform',  # noqa
            'defer_regress.tests.DeferAnnotateSelectRelatedTest.test_defer_annotate_select_related',  # noqa
            'delete_regress.tests.DeleteCascadeTransactionTests.test_inheritance',  # noqa
            'expressions.test_queryset_values.ValuesExpressionsTests.test_chained_values_with_expression',  # noqa
            'expressions.test_queryset_values.ValuesExpressionsTests.test_values_expression',  # noqa
            'expressions.test_queryset_values.ValuesExpressionsTests.test_values_expression_group_by',  # noqa
            'expressions.test_queryset_values.ValuesExpressionsTests.test_values_list_expression',  # noqa
            'expressions.test_queryset_values.ValuesExpressionsTests.test_values_list_expression_flat',  # noqa
            'expressions.tests.BasicExpressionsTests.test_annotate_values_aggregate',  # noqa
            'expressions.tests.BasicExpressionsTests.test_annotate_values_filter',  # noqa
            'expressions.tests.BasicExpressionsTests.test_annotations_within_subquery',  # noqa
            'expressions.tests.BasicExpressionsTests.test_arithmetic',  # noqa
            'expressions.tests.BasicExpressionsTests.test_exist_single_field_output_field',  # noqa
            'expressions.tests.BasicExpressionsTests.test_explicit_output_field',  # noqa
            'expressions.tests.BasicExpressionsTests.test_filter_inter_attribute',  # noqa
            'expressions.tests.BasicExpressionsTests.test_filter_with_join',  # noqa
            'expressions.tests.BasicExpressionsTests.test_in_subquery',  # noqa
            'expressions.tests.BasicExpressionsTests.test_incorrect_field_in_F_expression',  # noqa
            'expressions.tests.BasicExpressionsTests.test_incorrect_joined_field_in_F_expression',  # noqa
            'expressions.tests.BasicExpressionsTests.test_nested_subquery',  # noqa
            'expressions.tests.BasicExpressionsTests.test_nested_subquery_outer_ref_2',  # noqa
            'expressions.tests.BasicExpressionsTests.test_nested_subquery_outer_ref_with_autofield',  # noqa
            'expressions.tests.BasicExpressionsTests.test_new_object_create',  # noqa
            'expressions.tests.BasicExpressionsTests.test_new_object_save',  # noqa
            'expressions.tests.BasicExpressionsTests.test_object_create_with_aggregate',  # noqa
            'expressions.tests.BasicExpressionsTests.test_object_update',  # noqa
            'expressions.tests.BasicExpressionsTests.test_object_update_fk',  # noqa
            'expressions.tests.BasicExpressionsTests.test_object_update_unsaved_objects',  # noqa
            'expressions.tests.BasicExpressionsTests.test_order_by_exists',  # noqa
            'expressions.tests.BasicExpressionsTests.test_order_of_operations',  # noqa
            'expressions.tests.BasicExpressionsTests.test_outerref',  # noqa
            'expressions.tests.BasicExpressionsTests.test_outerref_with_operator',  # noqa
            'expressions.tests.BasicExpressionsTests.test_parenthesis_priority',  # noqa
            'expressions.tests.BasicExpressionsTests.test_pickle_expression',  # noqa
            'expressions.tests.BasicExpressionsTests.test_subquery',  # noqa
            'expressions.tests.BasicExpressionsTests.test_subquery_filter_by_aggregate',  # noqa
            'expressions.tests.BasicExpressionsTests.test_subquery_references_joined_table_twice',  # noqa
            'expressions.tests.BasicExpressionsTests.test_ticket_11722_iexact_lookup',  # noqa
            'expressions.tests.BasicExpressionsTests.test_ticket_18375_chained_filters',  # noqa
            'expressions.tests.BasicExpressionsTests.test_ticket_18375_join_reuse',  # noqa
            'expressions.tests.BasicExpressionsTests.test_ticket_18375_kwarg_ordering',  # noqa
            'expressions.tests.BasicExpressionsTests.test_ticket_18375_kwarg_ordering_2',  # noqa
            'expressions.tests.BasicExpressionsTests.test_update',  # noqa
            'expressions.tests.BasicExpressionsTests.test_update_inherited_field_value',  # noqa
            'expressions.tests.BasicExpressionsTests.test_update_with_fk',  # noqa
            'expressions.tests.BasicExpressionsTests.test_update_with_none',  # noqa
            'expressions.tests.BasicExpressionsTests.test_uuid_pk_subquery',  # noqa
            'expressions.tests.ExpressionsNumericTests.test_complex_expressions',  # noqa
            'expressions.tests.ExpressionsNumericTests.test_fill_with_value_from_same_object',  # noqa
            'expressions.tests.ExpressionsNumericTests.test_filter_not_equals_other_field',  # noqa
            'expressions.tests.ExpressionsNumericTests.test_increment_value',  # noqa
            'expressions.tests.ExpressionsTests.test_F_reuse',  # noqa
            'expressions.tests.IterableLookupInnerExpressionsTests.test_expressions_in_lookups_join_choice',  # noqa
            'expressions.tests.IterableLookupInnerExpressionsTests.test_in_lookup_allows_F_expressions_and_expressions_for_datetimes',  # noqa
            'expressions.tests.IterableLookupInnerExpressionsTests.test_in_lookup_allows_F_expressions_and_expressions_for_integers',  # noqa
            'expressions.tests.IterableLookupInnerExpressionsTests.test_range_lookup_allows_F_expressions_and_expressions_for_integers',  # noqa
            'expressions.tests.ValueTests.test_update_TimeField_using_Value',  # noqa
            'expressions.tests.ValueTests.test_update_UUIDField_using_Value',  # noqa
            'fixtures.tests.FixtureLoadingTests.test_loaddata_error_message',  # noqa
            'fixtures.tests.ForwardReferenceTests.test_forward_reference_fk',  # noqa
            'fixtures.tests.ForwardReferenceTests.test_forward_reference_m2m',  # noqa
            'get_or_create.tests.GetOrCreateTests.test_get_or_create_invalid_params',  # noqa
            'get_or_create.tests.GetOrCreateTestsWithManualPKs.test_create_with_duplicate_primary_key',  # noqa
            'get_or_create.tests.GetOrCreateTestsWithManualPKs.test_get_or_create_raises_IntegrityError_plus_traceback',  # noqa
            'introspection.tests.IntrospectionTests.test_get_constraints',  # noqa
            'introspection.tests.IntrospectionTests.test_get_constraints_index_types',  # noqa
            'introspection.tests.IntrospectionTests.test_get_constraints_indexes_orders',  # noqa
            'introspection.tests.IntrospectionTests.test_get_primary_key_column',  # noqa
            'lookup.tests.LookupTests.test_custom_field_none_rhs',  # noqa
            'lookup.tests.LookupTests.test_custom_lookup_none_rhs',  # noqa
            'lookup.tests.LookupTests.test_escaping',  # noqa
            'lookup.tests.LookupTests.test_exact_none_transform',  # noqa
            'lookup.tests.LookupTests.test_exclude',  # noqa
            'lookup.tests.LookupTests.test_in_bulk_lots_of_ids',  # noqa
            'lookup.tests.LookupTests.test_lookup_collision',  # noqa
            'lookup.tests.LookupTests.test_regex',  # noqa
            'lookup.tests.LookupTests.test_regex_non_string',  # noqa
            'lookup.tests.LookupTests.test_regex_null',  # noqa
            'm2m_through.tests.M2mThroughReferentialTests.test_through_fields_self_referential',  # noqa
            'm2m_through.tests.M2mThroughTests.test_add_on_m2m_with_intermediate_model_value_required_fails',  # noqa
            'm2m_through.tests.M2mThroughTests.test_add_on_reverse_m2m_with_intermediate_model',  # noqa
            'm2m_through.tests.M2mThroughTests.test_clear_on_reverse_removes_all_the_m2m_relationships',  # noqa
            'm2m_through.tests.M2mThroughTests.test_clear_removes_all_the_m2m_relationships',  # noqa
            'm2m_through.tests.M2mThroughTests.test_create_on_m2m_with_intermediate_model_value_required_fails',  # noqa
            'm2m_through.tests.M2mThroughTests.test_create_on_reverse_m2m_with_intermediate_model',  # noqa
            'm2m_through.tests.M2mThroughTests.test_custom_related_name_doesnt_conflict_with_fky_related_name',  # noqa
            'm2m_through.tests.M2mThroughTests.test_custom_related_name_forward_non_empty_qs',  # noqa
            'm2m_through.tests.M2mThroughTests.test_custom_related_name_reverse_non_empty_qs',  # noqa
            'm2m_through.tests.M2mThroughTests.test_filter_on_intermediate_model',  # noqa
            'm2m_through.tests.M2mThroughTests.test_get_on_intermediate_model',  # noqa
            'm2m_through.tests.M2mThroughTests.test_get_or_create_on_m2m_with_intermediate_model_value_required_fails',  # noqa
            'm2m_through.tests.M2mThroughTests.test_order_by_relational_field_through_model',  # noqa
            'm2m_through.tests.M2mThroughTests.test_query_first_model_by_intermediate_model_attribute',  # noqa
            'm2m_through.tests.M2mThroughTests.test_query_model_by_attribute_name_of_related_model',  # noqa
            'm2m_through.tests.M2mThroughTests.test_query_model_by_custom_related_name',  # noqa
            'm2m_through.tests.M2mThroughTests.test_query_model_by_intermediate_can_return_non_unique_queryset',  # noqa
            'm2m_through.tests.M2mThroughTests.test_query_model_by_related_model_name',  # noqa
            'm2m_through.tests.M2mThroughTests.test_query_second_model_by_intermediate_model_attribute',  # noqa
            'm2m_through.tests.M2mThroughTests.test_remove_on_m2m_with_intermediate_model',  # noqa
            'm2m_through.tests.M2mThroughTests.test_remove_on_reverse_m2m_with_intermediate_model',  # noqa
            'm2m_through.tests.M2mThroughTests.test_retrieve_intermediate_items',  # noqa
            'm2m_through.tests.M2mThroughTests.test_retrieve_reverse_intermediate_items',  # noqa
            'm2m_through.tests.M2mThroughTests.test_set_on_m2m_with_intermediate_model',  # noqa
            'm2m_through.tests.M2mThroughTests.test_set_on_m2m_with_intermediate_model_value_required_fails',  # noqa
            'm2m_through.tests.M2mThroughTests.test_set_on_reverse_m2m_with_intermediate_model',  # noqa
            'm2m_through.tests.M2mThroughTests.test_update_or_create_on_m2m_with_intermediate_model_value_required_fails',  # noqa
            'm2m_through_regress.tests.M2MThroughTestCase.test_join_trimming_forwards',  # noqa
            'm2m_through_regress.tests.M2MThroughTestCase.test_join_trimming_reverse',  # noqa
            'm2m_through_regress.tests.M2MThroughTestCase.test_retrieve_forward_m2m_items',  # noqa
            'm2m_through_regress.tests.M2MThroughTestCase.test_retrieve_forward_m2m_items_via_custom_id_intermediary',  # noqa
            'm2m_through_regress.tests.M2MThroughTestCase.test_retrieve_reverse_m2m_items',  # noqa
            'm2m_through_regress.tests.M2MThroughTestCase.test_retrieve_reverse_m2m_items_via_custom_id_intermediary',  # noqa
            'm2m_through_regress.tests.ThroughLoadDataTestCase.test_sequence_creation',  # noqa
            'm2m_through_regress.tests.ToFieldThroughTests.test_add_null_reverse',  # noqa
            'm2m_through_regress.tests.ToFieldThroughTests.test_add_null_reverse_related',  # noqa
            'm2m_through_regress.tests.ToFieldThroughTests.test_add_related_null',  # noqa
            'm2o_recursive.tests.ManyToOneRecursiveTests.test_m2o_recursive',  # noqa
            'm2o_recursive.tests.MultipleManyToOneRecursiveTests.test_m2o_recursive2',  # noqa
            'managers_regress.tests.ManagersRegressionTests.test_field_can_be_called_exact',  # noqa
            'managers_regress.tests.ManagersRegressionTests.test_regress_3871',  # noqa
            'many_to_one.tests.ManyToOneTests.test_add_after_prefetch',  # noqa
            'many_to_one.tests.ManyToOneTests.test_add_then_remove_after_prefetch',  # noqa
            'many_to_one.tests.ManyToOneTests.test_cached_foreign_key_with_to_field_not_cleared_by_save',  # noqa
            'many_to_one.tests.ManyToOneTests.test_multiple_foreignkeys',  # noqa
            'many_to_one.tests.ManyToOneTests.test_reverse_foreign_key_instance_to_field_caching',  # noqa
            'many_to_one.tests.ManyToOneTests.test_set_after_prefetch',  # noqa
            'many_to_one_null.tests.ManyToOneNullTests.test_add_efficiency',  # noqa
            'many_to_one_null.tests.ManyToOneNullTests.test_assign_clear_related_set',  # noqa
            'many_to_one_null.tests.ManyToOneNullTests.test_assign_with_queryset',  # noqa
            'many_to_one_null.tests.ManyToOneNullTests.test_clear_efficiency',  # noqa
            'many_to_one_null.tests.ManyToOneNullTests.test_created_via_related_set',  # noqa
            'many_to_one_null.tests.ManyToOneNullTests.test_created_without_related',  # noqa
            'many_to_one_null.tests.ManyToOneNullTests.test_get_related',  # noqa
            'many_to_one_null.tests.ManyToOneNullTests.test_related_null_to_field',  # noqa
            'many_to_one_null.tests.ManyToOneNullTests.test_related_set',  # noqa
            'many_to_one_null.tests.ManyToOneNullTests.test_remove_from_wrong_set',  # noqa
            'many_to_one_null.tests.ManyToOneNullTests.test_set',  # noqa
            'many_to_one_null.tests.ManyToOneNullTests.test_set_clear_non_bulk',  # noqa
            'migrations.test_operations.OperationTests.test_add_binaryfield',  # noqa
            'migrations.test_operations.OperationTests.test_add_charfield',  # noqa
            'migrations.test_operations.OperationTests.test_add_constraint',  # noqa
            'migrations.test_operations.OperationTests.test_add_constraint_percent_escaping',  # noqa
            'migrations.test_operations.OperationTests.test_add_field',  # noqa
            'migrations.test_operations.OperationTests.test_add_field_m2m',  # noqa
            'migrations.test_operations.OperationTests.test_add_field_preserve_default',  # noqa
            'migrations.test_operations.OperationTests.test_add_index',  # noqa
            'migrations.test_operations.OperationTests.test_add_index_state_forwards',  # noqa
            'migrations.test_operations.OperationTests.test_add_or_constraint',  # noqa
            'migrations.test_operations.OperationTests.test_add_partial_unique_constraint',  # noqa
            'migrations.test_operations.OperationTests.test_add_textfield',  # noqa
            'migrations.test_operations.OperationTests.test_alter_field',  # noqa
            'migrations.test_operations.OperationTests.test_alter_field_m2m',  # noqa
            'migrations.test_operations.OperationTests.test_alter_field_pk',  # noqa
            'migrations.test_operations.OperationTests.test_alter_field_pk_fk',  # noqa
            'migrations.test_operations.OperationTests.test_alter_field_reloads_state_on_fk_target_changes',  # noqa
            'migrations.test_operations.OperationTests.test_alter_field_reloads_state_on_fk_with_to_field_target_changes',  # noqa
            'migrations.test_operations.OperationTests.test_alter_fk',  # noqa
            'migrations.test_operations.OperationTests.test_alter_index_together',  # noqa
            'migrations.test_operations.OperationTests.test_alter_index_together_remove',  # noqa
            'migrations.test_operations.OperationTests.test_alter_model_managers',  # noqa
            'migrations.test_operations.OperationTests.test_alter_model_managers_emptying',  # noqa
            'migrations.test_operations.OperationTests.test_alter_model_options',  # noqa
            'migrations.test_operations.OperationTests.test_alter_model_options_emptying',  # noqa
            'migrations.test_operations.OperationTests.test_alter_model_table_none',  # noqa
            'migrations.test_operations.OperationTests.test_alter_model_table_noop',  # noqa
            'migrations.test_operations.OperationTests.test_alter_unique_together',  # noqa
            'migrations.test_operations.OperationTests.test_alter_unique_together_remove',  # noqa
            'migrations.test_operations.OperationTests.test_autofield_foreignfield_growth',  # noqa
            'migrations.test_operations.OperationTests.test_column_name_quoting',  # noqa
            'migrations.test_operations.OperationTests.test_create_model',  # noqa
            'migrations.test_operations.OperationTests.test_create_model_inheritance',  # noqa
            'migrations.test_operations.OperationTests.test_create_model_m2m',  # noqa
            'migrations.test_operations.OperationTests.test_create_model_managers',  # noqa
            'migrations.test_operations.OperationTests.test_create_model_with_constraint',  # noqa
            'migrations.test_operations.OperationTests.test_create_model_with_duplicate_base',  # noqa
            'migrations.test_operations.OperationTests.test_create_model_with_duplicate_field_name',  # noqa
            'migrations.test_operations.OperationTests.test_create_model_with_duplicate_manager_name',  # noqa
            'migrations.test_operations.OperationTests.test_create_model_with_partial_unique_constraint',  # noqa
            'migrations.test_operations.OperationTests.test_create_model_with_unique_after',  # noqa
            'migrations.test_operations.OperationTests.test_create_proxy_model',  # noqa
            'migrations.test_operations.OperationTests.test_create_unmanaged_model',  # noqa
            'migrations.test_operations.OperationTests.test_delete_model',  # noqa
            'migrations.test_operations.OperationTests.test_delete_mti_model',  # noqa
            'migrations.test_operations.OperationTests.test_delete_proxy_model',  # noqa
            'migrations.test_operations.OperationTests.test_model_with_bigautofield',  # noqa
            'migrations.test_operations.OperationTests.test_remove_constraint',  # noqa
            'migrations.test_operations.OperationTests.test_remove_field',  # noqa
            'migrations.test_operations.OperationTests.test_remove_field_m2m',  # noqa
            'migrations.test_operations.OperationTests.test_remove_field_m2m_with_through',  # noqa
            'migrations.test_operations.OperationTests.test_remove_fk',  # noqa
            'migrations.test_operations.OperationTests.test_remove_index',  # noqa
            'migrations.test_operations.OperationTests.test_remove_index_state_forwards',  # noqa
            'migrations.test_operations.OperationTests.test_remove_partial_unique_constraint',  # noqa
            'migrations.test_operations.OperationTests.test_rename_missing_field',  # noqa
            'migrations.test_operations.OperationTests.test_rename_model_state_forwards',  # noqa
            'migrations.test_operations.OperationTests.test_rename_referenced_field_state_forward',  # noqa
            'migrations.test_operations.OperationTests.test_run_python',  # noqa
            'migrations.test_operations.OperationTests.test_run_python_atomic',  # noqa
            'migrations.test_operations.OperationTests.test_run_python_noop',  # noqa
            'migrations.test_operations.OperationTests.test_run_python_related_assignment',  # noqa
            'migrations.test_operations.OperationTests.test_run_sql',  # noqa
            'migrations.test_operations.OperationTests.test_run_sql_noop',  # noqa
            'migrations.test_operations.OperationTests.test_run_sql_params_invalid',  # noqa
            'migrations.test_operations.OperationTests.test_separate_database_and_state',  # noqa
            'migrations.test_operations.OperationTests.test_separate_database_and_state2',  # noqa
            'model_fields.test_booleanfield.BooleanFieldTests.test_null_default',  # noqa
            'model_fields.test_durationfield.TestSaveLoad.test_create_empty',  # noqa
            'model_fields.test_genericipaddressfield.GenericIPAddressFieldTests.test_blank_string_saved_as_null',  # noqa
            'model_fields.test_genericipaddressfield.GenericIPAddressFieldTests.test_null_value',  # noqa
            'model_fields.test_imagefield.TwoImageFieldTests.test_dimensions',  # noqa
            'model_fields.test_imagefield.TwoImageFieldTests.test_field_save_and_delete_methods',  # noqa
            'model_fields.test_integerfield.BigIntegerFieldTests.test_backend_range_save',  # noqa
            'model_fields.test_integerfield.BigIntegerFieldTests.test_coercing',  # noqa
            'model_fields.test_integerfield.BigIntegerFieldTests.test_documented_range',  # noqa
            'model_fields.test_integerfield.BigIntegerFieldTests.test_types',  # noqa
            'model_fields.test_uuid.TestQuerying.test_exact',  # noqa
            'model_fields.test_uuid.TestQuerying.test_isnull',  # noqa
            'model_fields.test_uuid.TestSaveLoad.test_null_handling',  # noqa
            'multiple_database.tests.FixtureTestCase.test_fixture_loading',  # noqa
            'multiple_database.tests.FixtureTestCase.test_pseudo_empty_fixtures',  # noqa
            'multiple_database.tests.PickleQuerySetTestCase.test_pickling',  # noqa
            'multiple_database.tests.QueryTestCase.test_basic_queries',  # noqa
            'multiple_database.tests.QueryTestCase.test_default_creation',  # noqa
            'multiple_database.tests.QueryTestCase.test_foreign_key_cross_database_protection',  # noqa
            'multiple_database.tests.QueryTestCase.test_foreign_key_reverse_operations',  # noqa
            'multiple_database.tests.QueryTestCase.test_foreign_key_separation',  # noqa
            'multiple_database.tests.QueryTestCase.test_generic_key_cross_database_protection',  # noqa
            'multiple_database.tests.QueryTestCase.test_generic_key_deletion',  # noqa
            'multiple_database.tests.QueryTestCase.test_generic_key_reverse_operations',  # noqa
            'multiple_database.tests.QueryTestCase.test_generic_key_separation',  # noqa
            'multiple_database.tests.QueryTestCase.test_m2m_cross_database_protection',  # noqa
            'multiple_database.tests.QueryTestCase.test_m2m_deletion',  # noqa
            'multiple_database.tests.QueryTestCase.test_m2m_forward_operations',  # noqa
            'multiple_database.tests.QueryTestCase.test_m2m_reverse_operations',  # noqa
            'multiple_database.tests.QueryTestCase.test_m2m_separation',  # noqa
            'multiple_database.tests.QueryTestCase.test_o2o_cross_database_protection',  # noqa
            'multiple_database.tests.QueryTestCase.test_o2o_separation',  # noqa
            'multiple_database.tests.QueryTestCase.test_ordering',  # noqa
            'multiple_database.tests.QueryTestCase.test_other_creation',  # noqa
            'multiple_database.tests.QueryTestCase.test_raw',  # noqa
            'multiple_database.tests.QueryTestCase.test_refresh',  # noqa
            'multiple_database.tests.QueryTestCase.test_refresh_router_instance_hint',  # noqa
            'multiple_database.tests.QueryTestCase.test_related_manager',  # noqa
            'multiple_database.tests.RouteForWriteTestCase.test_m2m_add',  # noqa
            'multiple_database.tests.RouteForWriteTestCase.test_m2m_clear',  # noqa
            'multiple_database.tests.RouteForWriteTestCase.test_m2m_delete',  # noqa
            'multiple_database.tests.RouteForWriteTestCase.test_m2m_get_or_create',  # noqa
            'multiple_database.tests.RouteForWriteTestCase.test_m2m_remove',  # noqa
            'multiple_database.tests.RouteForWriteTestCase.test_m2m_update',  # noqa
            'multiple_database.tests.RouteForWriteTestCase.test_reverse_m2m_add',  # noqa
            'multiple_database.tests.RouteForWriteTestCase.test_reverse_m2m_clear',  # noqa
            'multiple_database.tests.RouteForWriteTestCase.test_reverse_m2m_delete',  # noqa
            'multiple_database.tests.RouteForWriteTestCase.test_reverse_m2m_get_or_create',  # noqa
            'multiple_database.tests.RouteForWriteTestCase.test_reverse_m2m_remove',  # noqa
            'multiple_database.tests.RouteForWriteTestCase.test_reverse_m2m_update',  # noqa
            'multiple_database.tests.RouterAttributeErrorTestCase.test_attribute_error_delete',  # noqa
            'multiple_database.tests.RouterAttributeErrorTestCase.test_attribute_error_m2m',  # noqa
            'multiple_database.tests.RouterAttributeErrorTestCase.test_attribute_error_read',  # noqa
            'multiple_database.tests.RouterModelArgumentTestCase.test_m2m_collection',  # noqa
            'multiple_database.tests.RouterTestCase.test_database_routing',  # noqa
            'multiple_database.tests.RouterTestCase.test_foreign_key_cross_database_protection',  # noqa
            'multiple_database.tests.RouterTestCase.test_generic_key_managers',  # noqa
            'multiple_database.tests.RouterTestCase.test_invalid_set_foreign_key_assignment',  # noqa
            'multiple_database.tests.RouterTestCase.test_m2m_cross_database_protection',  # noqa
            'multiple_database.tests.RouterTestCase.test_m2m_managers',  # noqa
            'multiple_database.tests.RouterTestCase.test_o2o_cross_database_protection',  # noqa
            'multiple_database.tests.RouterTestCase.test_partial_router',  # noqa
            'multiple_database.tests.SignalTests.test_database_arg_m2m',  # noqa
            'null_fk.tests.NullFkTests.test_combine_isnull',  # noqa
            'null_fk.tests.NullFkTests.test_null_fk',  # noqa
            'null_fk_ordering.tests.NullFkOrderingTests.test_ordering_across_null_fk',  # noqa
            'null_queries.tests.NullQueriesTests.test_reverse_relations',  # noqa
            'ordering.tests.OrderingTests.test_default_ordering',  # noqa
            'ordering.tests.OrderingTests.test_default_ordering_override',  # noqa
            'ordering.tests.OrderingTests.test_deprecated_values_annotate',  # noqa
            'ordering.tests.OrderingTests.test_extra_ordering',  # noqa
            'ordering.tests.OrderingTests.test_extra_ordering_quoting',  # noqa
            'ordering.tests.OrderingTests.test_extra_ordering_with_table_name',  # noqa
            'ordering.tests.OrderingTests.test_no_reordering_after_slicing',  # noqa
            'ordering.tests.OrderingTests.test_order_by_f_expression',  # noqa
            'ordering.tests.OrderingTests.test_order_by_f_expression_duplicates',  # noqa
            'ordering.tests.OrderingTests.test_order_by_nulls_first',  # noqa
            'ordering.tests.OrderingTests.test_order_by_nulls_first_and_last',  # noqa
            'ordering.tests.OrderingTests.test_order_by_nulls_last',  # noqa
            'ordering.tests.OrderingTests.test_orders_nulls_first_on_filtered_subquery',  # noqa
            'ordering.tests.OrderingTests.test_related_ordering_duplicate_table_reference',  # noqa
            'ordering.tests.OrderingTests.test_reverse_ordering_pure',  # noqa
            'ordering.tests.OrderingTests.test_reversed_ordering',  # noqa
            'ordering.tests.OrderingTests.test_stop_slicing',  # noqa
            'ordering.tests.OrderingTests.test_stop_start_slicing',  # noqa
            'queries.test_bulk_update.BulkUpdateNoteTests.test_batch_size',  # noqa
            'queries.test_bulk_update.BulkUpdateNoteTests.test_foreign_keys_do_not_lookup',  # noqa
            'queries.test_bulk_update.BulkUpdateNoteTests.test_functions',  # noqa
            'queries.test_bulk_update.BulkUpdateNoteTests.test_set_field_to_null',  # noqa
            'queries.test_bulk_update.BulkUpdateNoteTests.test_set_mixed_fields_to_null',  # noqa
            'queries.test_bulk_update.BulkUpdateNoteTests.test_simple',  # noqa
            'queries.test_bulk_update.BulkUpdateTests.test_custom_db_columns',  # noqa
            'queries.test_bulk_update.BulkUpdateTests.test_field_references',  # noqa
            'queries.test_bulk_update.BulkUpdateTests.test_ipaddressfield',  # noqa
            'queries.tests.CloneTests.test_evaluated_queryset_as_argument',  # noqa
            'queries.tests.ComparisonTests.test_ticket8597',  # noqa
            'queries.tests.ConditionalTests.test_in_list_limit',  # noqa
            'queries.tests.ConditionalTests.test_infinite_loop',  # noqa
            'queries.tests.ConditionalTests.test_null_ordering_added',  # noqa
            'queries.tests.DisjunctionPromotionTests.test_disjunction_promotion_select_related',  # noqa
            'queries.tests.DisjunctiveFilterTests.test_ticket7872',  # noqa
            'queries.tests.DisjunctiveFilterTests.test_ticket8283',  # noqa
            'queries.tests.IsNullTests.test_primary_key',  # noqa
            'queries.tests.IsNullTests.test_to_field',  # noqa
            'queries.tests.JoinReuseTest.test_inverted_q_across_relations',  # noqa
            'queries.tests.NullInExcludeTest.test_col_not_in_list_containing_null',  # noqa
            'queries.tests.NullInExcludeTest.test_double_exclude',  # noqa
            'queries.tests.NullInExcludeTest.test_null_in_exclude_qs',  # noqa
            'queries.tests.NullJoinPromotionOrTest.test_isnull_filter_promotion',  # noqa
            'queries.tests.NullJoinPromotionOrTest.test_null_join_demotion',  # noqa
            'queries.tests.NullJoinPromotionOrTest.test_ticket_17886',  # noqa
            'queries.tests.NullJoinPromotionOrTest.test_ticket_21366',  # noqa
            'queries.tests.NullJoinPromotionOrTest.test_ticket_21748',  # noqa
            'queries.tests.NullJoinPromotionOrTest.test_ticket_21748_complex_filter',  # noqa
            'queries.tests.NullJoinPromotionOrTest.test_ticket_21748_double_negated_and',  # noqa
            'queries.tests.NullJoinPromotionOrTest.test_ticket_21748_double_negated_or',  # noqa
            'queries.tests.NullableRelOrderingTests.test_join_already_in_query',  # noqa
            'queries.tests.NullableRelOrderingTests.test_ticket10028',  # noqa
            'queries.tests.Queries1Tests.test_avoid_infinite_loop_on_too_many_subqueries',  # noqa
            'queries.tests.Queries1Tests.test_common_mixed_case_foreign_keys',  # noqa
            'queries.tests.Queries1Tests.test_deferred_load_qs_pickling',  # noqa
            'queries.tests.Queries1Tests.test_double_exclude',  # noqa
            'queries.tests.Queries1Tests.test_error_raised_on_filter_with_dictionary',  # noqa
            'queries.tests.Queries1Tests.test_exclude',  # noqa
            'queries.tests.Queries1Tests.test_exclude_in',  # noqa
            'queries.tests.Queries1Tests.test_get_clears_ordering',  # noqa
            'queries.tests.Queries1Tests.test_heterogeneous_qs_combination',  # noqa
            'queries.tests.Queries1Tests.test_lookup_constraint_fielderror',  # noqa
            'queries.tests.Queries1Tests.test_nested_exclude',  # noqa
            'queries.tests.Queries1Tests.test_order_by_join_unref',  # noqa
            'queries.tests.Queries1Tests.test_order_by_tables',  # noqa
            'queries.tests.Queries1Tests.test_reasonable_number_of_subq_aliases',  # noqa
            'queries.tests.Queries1Tests.test_subquery_condition',  # noqa
            'queries.tests.Queries1Tests.test_ticket10205',  # noqa
            'queries.tests.Queries1Tests.test_ticket10432',  # noqa
            'queries.tests.Queries1Tests.test_ticket1050',  # noqa
            'queries.tests.Queries1Tests.test_ticket10742',  # noqa
            'queries.tests.Queries1Tests.test_ticket17429',  # noqa
            'queries.tests.Queries1Tests.test_ticket1801',  # noqa
            'queries.tests.Queries1Tests.test_ticket19672',  # noqa
            'queries.tests.Queries1Tests.test_ticket2091',  # noqa
            'queries.tests.Queries1Tests.test_ticket2253',  # noqa
            'queries.tests.Queries1Tests.test_ticket2306',  # noqa
            'queries.tests.Queries1Tests.test_ticket2400',  # noqa
            'queries.tests.Queries1Tests.test_ticket2496',  # noqa
            'queries.tests.Queries1Tests.test_ticket2902',  # noqa
            'queries.tests.Queries1Tests.test_ticket3037',  # noqa
            'queries.tests.Queries1Tests.test_ticket3141',  # noqa
            'queries.tests.Queries1Tests.test_ticket4358',  # noqa
            'queries.tests.Queries1Tests.test_ticket4464',  # noqa
            'queries.tests.Queries1Tests.test_ticket4510',  # noqa
            'queries.tests.Queries1Tests.test_ticket6074',  # noqa
            'queries.tests.Queries1Tests.test_ticket6154',  # noqa
            'queries.tests.Queries1Tests.test_ticket6981',  # noqa
            'queries.tests.Queries1Tests.test_ticket7076',  # noqa
            'queries.tests.Queries1Tests.test_ticket7096',  # noqa
            'queries.tests.Queries1Tests.test_ticket7098',  # noqa
            'queries.tests.Queries1Tests.test_ticket7155',  # noqa
            'queries.tests.Queries1Tests.test_ticket7181',  # noqa
            'queries.tests.Queries1Tests.test_ticket7235',  # noqa
            'queries.tests.Queries1Tests.test_ticket7277',  # noqa
            'queries.tests.Queries1Tests.test_ticket7323',  # noqa
            'queries.tests.Queries1Tests.test_ticket7378',  # noqa
            'queries.tests.Queries1Tests.test_ticket7791',  # noqa
            'queries.tests.Queries1Tests.test_ticket7813',  # noqa
            'queries.tests.Queries1Tests.test_ticket8439',  # noqa
            'queries.tests.Queries1Tests.test_ticket9926',  # noqa
            'queries.tests.Queries1Tests.test_ticket9985',  # noqa
            'queries.tests.Queries1Tests.test_ticket9997',  # noqa
            'queries.tests.Queries1Tests.test_ticket_10790_1',  # noqa
            'queries.tests.Queries1Tests.test_ticket_10790_2',  # noqa
            'queries.tests.Queries1Tests.test_ticket_10790_3',  # noqa
            'queries.tests.Queries1Tests.test_ticket_10790_4',  # noqa
            'queries.tests.Queries1Tests.test_ticket_10790_5',  # noqa
            'queries.tests.Queries1Tests.test_ticket_10790_6',  # noqa
            'queries.tests.Queries1Tests.test_ticket_10790_7',  # noqa
            'queries.tests.Queries1Tests.test_ticket_10790_8',  # noqa
            'queries.tests.Queries1Tests.test_ticket_10790_combine',  # noqa
            'queries.tests.Queries1Tests.test_ticket_20250',  # noqa
            'queries.tests.Queries1Tests.test_tickets_1878_2939',  # noqa
            'queries.tests.Queries1Tests.test_tickets_2076_7256',  # noqa
            'queries.tests.Queries1Tests.test_tickets_2080_3592',  # noqa
            'queries.tests.Queries1Tests.test_tickets_2874_3002',  # noqa
            'queries.tests.Queries1Tests.test_tickets_4088_4306',  # noqa
            'queries.tests.Queries1Tests.test_tickets_5321_7070',  # noqa
            'queries.tests.Queries1Tests.test_tickets_5324_6704',  # noqa
            'queries.tests.Queries1Tests.test_tickets_6180_6203',  # noqa
            'queries.tests.Queries1Tests.test_tickets_7087_12242',  # noqa
            'queries.tests.Queries1Tests.test_tickets_7204_7506',  # noqa
            'queries.tests.Queries1Tests.test_tickets_7448_7707',  # noqa
            'queries.tests.Queries2Tests.test_ticket12239',  # noqa
            'queries.tests.Queries2Tests.test_ticket4289',  # noqa
            'queries.tests.Queries2Tests.test_ticket7759',  # noqa
            'queries.tests.Queries4Tests.test_combine_join_reuse',  # noqa
            'queries.tests.Queries4Tests.test_join_reuse_order',  # noqa
            'queries.tests.Queries4Tests.test_order_by_resetting',  # noqa
            'queries.tests.Queries4Tests.test_order_by_reverse_fk',  # noqa
            'queries.tests.Queries4Tests.test_ticket10181',  # noqa
            'queries.tests.Queries4Tests.test_ticket11811',  # noqa
            'queries.tests.Queries4Tests.test_ticket14876',  # noqa
            'queries.tests.Queries4Tests.test_ticket15316_exclude_false',  # noqa
            'queries.tests.Queries4Tests.test_ticket15316_filter_false',  # noqa
            'queries.tests.Queries4Tests.test_ticket15316_filter_true',  # noqa
            'queries.tests.Queries4Tests.test_ticket15316_one2one_exclude_false',  # noqa
            'queries.tests.Queries4Tests.test_ticket15316_one2one_exclude_true',  # noqa
            'queries.tests.Queries4Tests.test_ticket15316_one2one_filter_false',  # noqa
            'queries.tests.Queries4Tests.test_ticket15316_one2one_filter_true',  # noqa
            'queries.tests.Queries4Tests.test_ticket24525',  # noqa
            'queries.tests.Queries4Tests.test_ticket7095',  # noqa
            'queries.tests.Queries5Tests.test_extra_select_literal_percent_s',  # noqa
            'queries.tests.Queries5Tests.test_ordering',  # noqa
            'queries.tests.Queries5Tests.test_ticket5261',  # noqa
            'queries.tests.Queries5Tests.test_ticket7045',  # noqa
            'queries.tests.Queries5Tests.test_ticket9848',  # noqa
            'queries.tests.Queries6Tests.test_distinct_ordered_sliced_subquery_aggregation',  # noqa
            'queries.tests.Queries6Tests.test_multiple_columns_with_the_same_name_slice',  # noqa
            'queries.tests.Queries6Tests.test_nested_queries_sql',  # noqa
            'queries.tests.Queries6Tests.test_parallel_iterators',  # noqa
            'queries.tests.Queries6Tests.test_ticket3739',  # noqa
            'queries.tests.Queries6Tests.test_ticket_11320',  # noqa
            'queries.tests.Queries6Tests.test_tickets_8921_9188',  # noqa
            'queries.tests.RawQueriesTests.test_ticket14729',  # noqa
            'queries.tests.RelabelCloneTest.test_ticket_19964',  # noqa
            'queries.tests.RelatedLookupTypeTests.test_correct_lookup',  # noqa
            'queries.tests.RelatedLookupTypeTests.test_wrong_backward_lookup',  # noqa
            'queries.tests.RelatedLookupTypeTests.test_wrong_type_lookup',  # noqa
            'queries.tests.ReverseJoinTrimmingTest.test_reverse_trimming',  # noqa
            'queries.tests.SubclassFKTests.test_ticket7778',  # noqa
            'queries.tests.Ticket20101Tests.test_ticket_20101',  # noqa
            'queries.tests.Ticket22429Tests.test_ticket_22429',  # noqa
            'queries.tests.ToFieldTests.test_nested_in_subquery',  # noqa
            'queries.tests.ToFieldTests.test_recursive_fk',  # noqa
            'queries.tests.ToFieldTests.test_recursive_fk_reverse',  # noqa
            'queries.tests.ValuesJoinPromotionTests.test_ticket_21376',  # noqa
            'queries.tests.ValuesQuerysetTests.test_extra_multiple_select_params_values_order_by',  # noqa
            'queries.tests.ValuesQuerysetTests.test_extra_select_params_values_order_in_extra',  # noqa
            'queries.tests.ValuesQuerysetTests.test_extra_values',  # noqa
            'queries.tests.ValuesQuerysetTests.test_extra_values_list',  # noqa
            'queries.tests.ValuesQuerysetTests.test_extra_values_order_in_extra',  # noqa
            'queries.tests.ValuesQuerysetTests.test_extra_values_order_multiple',  # noqa
            'queries.tests.ValuesQuerysetTests.test_extra_values_order_twice',  # noqa
            'queries.tests.ValuesQuerysetTests.test_field_error_values_list',  # noqa
            'queries.tests.ValuesQuerysetTests.test_flat_extra_values_list',  # noqa
            'queries.tests.ValuesQuerysetTests.test_flat_values_list',  # noqa
            'queries.tests.ValuesQuerysetTests.test_named_values_list_bad_field_name',  # noqa
            'queries.tests.ValuesQuerysetTests.test_named_values_list_expression',  # noqa
            'queries.tests.ValuesQuerysetTests.test_named_values_list_expression_with_default_alias',  # noqa
            'queries.tests.ValuesQuerysetTests.test_named_values_list_flat',  # noqa
            'queries.tests.ValuesQuerysetTests.test_named_values_list_with_fields',  # noqa
            'queries.tests.ValuesQuerysetTests.test_named_values_list_without_fields',  # noqa
            'queries.tests.WeirdQuerysetSlicingTests.test_empty_resultset_sql',  # noqa
            'queries.tests.WeirdQuerysetSlicingTests.test_empty_sliced_subquery',  # noqa
            'queries.tests.WeirdQuerysetSlicingTests.test_empty_sliced_subquery_exclude',  # noqa
            'queries.tests.WeirdQuerysetSlicingTests.test_tickets_7698_10202',  # noqa
            'queries.tests.WeirdQuerysetSlicingTests.test_zero_length_values_slicing',  # noqa
            'schema.tests.SchemaTests.test_add_datefield_and_datetimefield_use_effective_default',  # noqa
            'schema.tests.SchemaTests.test_add_field',  # noqa
            'schema.tests.SchemaTests.test_add_field_binary',  # noqa
            'schema.tests.SchemaTests.test_add_field_default_dropped',  # noqa
            'schema.tests.SchemaTests.test_add_field_default_transform',  # noqa
            'schema.tests.SchemaTests.test_add_field_remove_field',  # noqa
            'schema.tests.SchemaTests.test_add_field_temp_default',  # noqa
            'schema.tests.SchemaTests.test_add_field_temp_default_boolean',  # noqa
            'schema.tests.SchemaTests.test_add_field_use_effective_default',  # noqa
            'schema.tests.SchemaTests.test_add_foreign_key_long_names',  # noqa
            'schema.tests.SchemaTests.test_add_foreign_key_quoted_db_table',  # noqa
            'schema.tests.SchemaTests.test_add_foreign_object',  # noqa
            'schema.tests.SchemaTests.test_add_remove_index',  # noqa
            'schema.tests.SchemaTests.test_add_textfield_unhashable_default',  # noqa
            'schema.tests.SchemaTests.test_alter',  # noqa
            'schema.tests.SchemaTests.test_alter_auto_field_to_integer_field',  # noqa
            'schema.tests.SchemaTests.test_alter_charfield_to_null',  # noqa
            'schema.tests.SchemaTests.test_alter_field_add_index_to_integerfield',  # noqa
            'schema.tests.SchemaTests.test_alter_field_default_doesnt_perfom_queries',  # noqa
            'schema.tests.SchemaTests.test_alter_field_default_dropped',  # noqa
            'schema.tests.SchemaTests.test_alter_field_fk_keeps_index',  # noqa
            'schema.tests.SchemaTests.test_alter_field_fk_to_o2o',  # noqa
            'schema.tests.SchemaTests.test_alter_field_o2o_keeps_unique',  # noqa
            'schema.tests.SchemaTests.test_alter_field_o2o_to_fk',  # noqa
            'schema.tests.SchemaTests.test_alter_fk',  # noqa
            'schema.tests.SchemaTests.test_alter_fk_checks_deferred_constraints',  # noqa
            'schema.tests.SchemaTests.test_alter_fk_to_o2o',  # noqa
            'schema.tests.SchemaTests.test_alter_implicit_id_to_explicit',  # noqa
            'schema.tests.SchemaTests.test_alter_int_pk_to_autofield_pk',  # noqa
            'schema.tests.SchemaTests.test_alter_int_pk_to_bigautofield_pk',  # noqa
            'schema.tests.SchemaTests.test_alter_null_to_not_null',  # noqa
            'schema.tests.SchemaTests.test_alter_null_to_not_null_keeping_default',  # noqa
            'schema.tests.SchemaTests.test_alter_numeric_field_keep_null_status',  # noqa
            'schema.tests.SchemaTests.test_alter_o2o_to_fk',  # noqa
            'schema.tests.SchemaTests.test_alter_text_field',  # noqa
            'schema.tests.SchemaTests.test_alter_textfield_to_null',  # noqa
            'schema.tests.SchemaTests.test_alter_textual_field_keep_null_status',  # noqa
            'schema.tests.SchemaTests.test_alter_to_fk',  # noqa
            'schema.tests.SchemaTests.test_char_field_with_db_index_to_fk',  # noqa
            'schema.tests.SchemaTests.test_check_constraints',  # noqa
            'schema.tests.SchemaTests.test_context_manager_exit',  # noqa
            'schema.tests.SchemaTests.test_create_index_together',  # noqa
            'schema.tests.SchemaTests.test_creation_deletion',  # noqa
            'schema.tests.SchemaTests.test_creation_deletion_reserved_names',  # noqa
            'schema.tests.SchemaTests.test_fk',  # noqa
            'schema.tests.SchemaTests.test_fk_db_constraint',  # noqa
            'schema.tests.SchemaTests.test_fk_to_proxy',  # noqa
            'schema.tests.SchemaTests.test_foreign_key_index_long_names_regression',  # noqa
            'schema.tests.SchemaTests.test_index_together',  # noqa
            'schema.tests.SchemaTests.test_index_together_with_fk',  # noqa
            'schema.tests.SchemaTests.test_indexes',  # noqa
            'schema.tests.SchemaTests.test_m2m',  # noqa
            'schema.tests.SchemaTests.test_m2m_create',  # noqa
            'schema.tests.SchemaTests.test_m2m_create_custom',  # noqa
            'schema.tests.SchemaTests.test_m2m_create_inherited',  # noqa
            'schema.tests.SchemaTests.test_m2m_create_through',  # noqa
            'schema.tests.SchemaTests.test_m2m_create_through_custom',  # noqa
            'schema.tests.SchemaTests.test_m2m_create_through_inherited',  # noqa
            'schema.tests.SchemaTests.test_m2m_custom',  # noqa
            'schema.tests.SchemaTests.test_m2m_db_constraint',  # noqa
            'schema.tests.SchemaTests.test_m2m_db_constraint_custom',  # noqa
            'schema.tests.SchemaTests.test_m2m_db_constraint_inherited',  # noqa
            'schema.tests.SchemaTests.test_m2m_inherited',  # noqa
            'schema.tests.SchemaTests.test_m2m_through_alter',  # noqa
            'schema.tests.SchemaTests.test_m2m_through_alter_custom',  # noqa
            'schema.tests.SchemaTests.test_m2m_through_alter_inherited',  # noqa
            'schema.tests.SchemaTests.test_namespaced_db_table_create_index_name',  # noqa
            'schema.tests.SchemaTests.test_no_db_constraint_added_during_primary_key_change',  # noqa
            'schema.tests.SchemaTests.test_order_index',  # noqa
            'schema.tests.SchemaTests.test_remove_constraints_capital_letters',  # noqa
            'schema.tests.SchemaTests.test_remove_db_index_doesnt_remove_custom_indexes',  # noqa
            'schema.tests.SchemaTests.test_remove_field_check_does_not_remove_meta_constraints',  # noqa
            'schema.tests.SchemaTests.test_remove_field_unique_does_not_remove_meta_constraints',  # noqa
            'schema.tests.SchemaTests.test_remove_index_together_does_not_remove_meta_indexes',  # noqa
            'schema.tests.SchemaTests.test_remove_unique_together_does_not_remove_meta_constraints',  # noqa
            'schema.tests.SchemaTests.test_text_field_with_db_index',  # noqa
            'schema.tests.SchemaTests.test_text_field_with_db_index_to_fk',  # noqa
            'schema.tests.SchemaTests.test_unique',  # noqa
            'schema.tests.SchemaTests.test_unique_and_reverse_m2m',  # noqa
            'schema.tests.SchemaTests.test_unique_no_unnecessary_fk_drops',  # noqa
            'schema.tests.SchemaTests.test_unique_together',  # noqa
            'schema.tests.SchemaTests.test_unique_together_with_fk',  # noqa
            'schema.tests.SchemaTests.test_unique_together_with_fk_with_existing_index',  # noqa
            'schema.tests.SchemaTests.test_unsupported_transactional_ddl_disallowed',  # noqa
            'select_related_onetoone.tests.ReverseSelectRelatedTestCase.test_nullable_relation',  # noqa
            'select_related_onetoone.tests.ReverseSelectRelatedTestCase.test_self_relation',  # noqa
            'sessions_tests.tests.CustomDatabaseSessionTests.test_actual_expiry',  # noqa
            'sessions_tests.tests.CustomDatabaseSessionTests.test_clearsessions_command',  # noqa
            'sessions_tests.tests.CustomDatabaseSessionTests.test_cycle',  # noqa
            'sessions_tests.tests.CustomDatabaseSessionTests.test_cycle_with_no_session_cache',  # noqa
            'sessions_tests.tests.CustomDatabaseSessionTests.test_delete',  # noqa
            'sessions_tests.tests.CustomDatabaseSessionTests.test_flush',  # noqa
            'sessions_tests.tests.CustomDatabaseSessionTests.test_invalid_key',  # noqa
            'sessions_tests.tests.CustomDatabaseSessionTests.test_save',  # noqa
            'sessions_tests.tests.CustomDatabaseSessionTests.test_save_doesnt_clear_data',  # noqa
            'sessions_tests.tests.CustomDatabaseSessionTests.test_session_get_decoded',  # noqa
            'sessions_tests.tests.CustomDatabaseSessionTests.test_session_save_does_not_resurrect_session_logged_out_in_other_context',  # noqa
            'sessions_tests.tests.CustomDatabaseSessionTests.test_session_str',  # noqa
            'sessions_tests.tests.CustomDatabaseSessionTests.test_sessionmanager_save',  # noqa
            'sitemaps_tests.test_generic.GenericViewsSitemapTests.test_generic_sitemap',  # noqa
            'sitemaps_tests.test_generic.GenericViewsSitemapTests.test_generic_sitemap_attributes',  # noqa
            'sitemaps_tests.test_generic.GenericViewsSitemapTests.test_generic_sitemap_lastmod',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_cached_sitemap_index',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_empty_page',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_empty_sitemap',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_localized_priority',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_no_section',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_page_not_int',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_paged_sitemap',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_requestsite_sitemap',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_simple_custom_sitemap',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_simple_i18nsitemap_index',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_simple_sitemap',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_simple_sitemap_custom_index',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_simple_sitemap_index',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_simple_sitemap_section',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemap_get_urls_no_site_1',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemap_get_urls_no_site_2',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemap_item',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemap_last_modified',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemap_last_modified_date',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemap_last_modified_missing',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemap_last_modified_mixed',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemap_last_modified_tz',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemap_not_callable',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemap_without_entries',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemaps_lastmod_ascending',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemaps_lastmod_descending',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemaps_lastmod_mixed_ascending_last_modified_missing',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_sitemaps_lastmod_mixed_descending_last_modified_missing',  # noqa
            'sitemaps_tests.test_http.HTTPSitemapTests.test_x_robots_sitemap',  # noqa
            'sitemaps_tests.test_https.HTTPSDetectionSitemapTests.test_sitemap_index_with_https_request',  # noqa
            'sitemaps_tests.test_https.HTTPSDetectionSitemapTests.test_sitemap_section_with_https_request',  # noqa
            'sitemaps_tests.test_https.HTTPSSitemapTests.test_secure_sitemap_index',  # noqa
            'sitemaps_tests.test_https.HTTPSSitemapTests.test_secure_sitemap_section',  # noqa
            'sitemaps_tests.test_management.PingGoogleTests.test_args',  # noqa
            'sitemaps_tests.test_management.PingGoogleTests.test_default',  # noqa
            'sitemaps_tests.test_utils.PingGoogleTests.test_get_sitemap_full_url_exact_url',  # noqa
            'sitemaps_tests.test_utils.PingGoogleTests.test_get_sitemap_full_url_global',  # noqa
            'sitemaps_tests.test_utils.PingGoogleTests.test_get_sitemap_full_url_index',  # noqa
            'sitemaps_tests.test_utils.PingGoogleTests.test_get_sitemap_full_url_insecure',  # noqa
            'sitemaps_tests.test_utils.PingGoogleTests.test_get_sitemap_full_url_no_sites',  # noqa
            'sitemaps_tests.test_utils.PingGoogleTests.test_get_sitemap_full_url_not_detected',  # noqa
            'sitemaps_tests.test_utils.PingGoogleTests.test_something',  # noqa
            'string_lookup.tests.StringLookupTests.test_queries_on_textfields',  # noqa
            'test_client.tests.ClientTest.test_empty_post',  # noqa
            'test_client.tests.ClientTest.test_exception_following_nested_client_request',  # noqa
            'test_client.tests.ClientTest.test_external_redirect',  # noqa
            'test_client.tests.ClientTest.test_external_redirect_with_fetch_error_msg',  # noqa
            'test_client.tests.ClientTest.test_follow_307_and_308_preserves_get_params',  # noqa
            'test_client.tests.ClientTest.test_follow_307_and_308_preserves_post_data',  # noqa
            'test_client.tests.ClientTest.test_follow_307_and_308_preserves_put_body',  # noqa
            'test_client.tests.ClientTest.test_follow_307_and_308_redirect',  # noqa
            'test_client.tests.ClientTest.test_follow_redirect',  # noqa
            'test_client.tests.ClientTest.test_follow_relative_redirect',  # noqa
            'test_client.tests.ClientTest.test_follow_relative_redirect_no_trailing_slash',  # noqa
            'test_client.tests.ClientTest.test_force_login_with_backend',  # noqa
            'test_client.tests.ClientTest.test_force_login_with_backend_missing_get_user',  # noqa
            'test_client.tests.ClientTest.test_force_login_without_backend',  # noqa
            'test_client.tests.ClientTest.test_form_error',  # noqa
            'test_client.tests.ClientTest.test_form_error_with_template',  # noqa
            'test_client.tests.ClientTest.test_get_data_none',  # noqa
            'test_client.tests.ClientTest.test_get_post_view',  # noqa
            'test_client.tests.ClientTest.test_get_view',  # noqa
            'test_client.tests.ClientTest.test_incomplete_data_form',  # noqa
            'test_client.tests.ClientTest.test_incomplete_data_form_with_template',  # noqa
            'test_client.tests.ClientTest.test_insecure',  # noqa
            'test_client.tests.ClientTest.test_json_encoder_argument',  # noqa
            'test_client.tests.ClientTest.test_json_serialization',  # noqa
            'test_client.tests.ClientTest.test_logout',  # noqa
            'test_client.tests.ClientTest.test_logout_cookie_sessions',  # noqa
            'test_client.tests.ClientTest.test_logout_with_force_login',  # noqa
            'test_client.tests.ClientTest.test_mail_sending',  # noqa
            'test_client.tests.ClientTest.test_mass_mail_sending',  # noqa
            'test_client.tests.ClientTest.test_notfound_response',  # noqa
            'test_client.tests.ClientTest.test_permanent_redirect',  # noqa
            'test_client.tests.ClientTest.test_post',  # noqa
            'test_client.tests.ClientTest.test_post_data_none',  # noqa
            'test_client.tests.ClientTest.test_put',  # noqa
            'test_client.tests.ClientTest.test_query_string_encoding',  # noqa
            'test_client.tests.ClientTest.test_raw_post',  # noqa
            'test_client.tests.ClientTest.test_redirect',  # noqa
            'test_client.tests.ClientTest.test_redirect_http',  # noqa
            'test_client.tests.ClientTest.test_redirect_https',  # noqa
            'test_client.tests.ClientTest.test_redirect_to_strange_location',  # noqa
            'test_client.tests.ClientTest.test_redirect_with_query',  # noqa
            'test_client.tests.ClientTest.test_redirect_with_query_ordering',  # noqa
            'test_client.tests.ClientTest.test_relative_redirect',  # noqa
            'test_client.tests.ClientTest.test_relative_redirect_no_trailing_slash',  # noqa
            'test_client.tests.ClientTest.test_response_attached_request',  # noqa
            'test_client.tests.ClientTest.test_response_headers',  # noqa
            'test_client.tests.ClientTest.test_response_raises_multi_arg_exception',  # noqa
            'test_client.tests.ClientTest.test_response_resolver_match',  # noqa
            'test_client.tests.ClientTest.test_response_resolver_match_redirect_follow',  # noqa
            'test_client.tests.ClientTest.test_response_resolver_match_regular_view',  # noqa
            'test_client.tests.ClientTest.test_reverse_lazy_decodes',  # noqa
            'test_client.tests.ClientTest.test_secure',  # noqa
            'test_client.tests.ClientTest.test_session_engine_is_invalid',  # noqa
            'test_client.tests.ClientTest.test_session_modifying_view',  # noqa
            'test_client.tests.ClientTest.test_sessions_app_is_not_installed',  # noqa
            'test_client.tests.ClientTest.test_temporary_redirect',  # noqa
            'test_client.tests.ClientTest.test_trace',  # noqa
            'test_client.tests.ClientTest.test_unknown_page',  # noqa
            'test_client.tests.ClientTest.test_uploading_named_temp_file',  # noqa
            'test_client.tests.ClientTest.test_uploading_temp_file',  # noqa
            'test_client.tests.ClientTest.test_url_parameters',  # noqa
            'test_client.tests.ClientTest.test_valid_form',  # noqa
            'test_client.tests.ClientTest.test_valid_form_with_hints',  # noqa
            'test_client.tests.ClientTest.test_valid_form_with_template',  # noqa
            'test_client.tests.ClientTest.test_view_with_bad_login',  # noqa
            'test_client.tests.ClientTest.test_view_with_exception',  # noqa
            'test_client.tests.ClientTest.test_view_with_force_login',  # noqa
            'test_client.tests.ClientTest.test_view_with_force_login_and_custom_redirect',  # noqa
            'test_client.tests.ClientTest.test_view_with_inactive_force_login',  # noqa
            'test_client.tests.ClientTest.test_view_with_inactive_login',  # noqa
            'test_client.tests.ClientTest.test_view_with_login',  # noqa
            'test_client.tests.ClientTest.test_view_with_login_and_custom_redirect',  # noqa
            'test_client.tests.ClientTest.test_view_with_login_when_sessions_app_is_not_installed',  # noqa
            'test_client.tests.ClientTest.test_view_with_method_force_login',  # noqa
            'test_client.tests.ClientTest.test_view_with_method_login',  # noqa
            'test_client.tests.ClientTest.test_view_with_method_permissions',  # noqa
            'test_client.tests.ClientTest.test_view_with_permissions',  # noqa
            'test_client.tests.ClientTest.test_view_with_permissions_exception',  # noqa
            'test_client_regress.tests.AssertTemplateUsedTests.test_multiple_context',  # noqa
            'test_client_regress.tests.AssertTemplateUsedTests.test_no_context',  # noqa
            'test_client_regress.tests.AssertTemplateUsedTests.test_single_context',  # noqa
            'test_client_regress.tests.AssertTemplateUsedTests.test_template_rendered_multiple_times',  # noqa
            'test_client_regress.tests.ContextTests.test_15368',  # noqa
            'test_client_regress.tests.ContextTests.test_contextlist_get',  # noqa
            'test_client_regress.tests.ContextTests.test_contextlist_keys',  # noqa
            'test_client_regress.tests.ContextTests.test_inherited_context',  # noqa
            'test_client_regress.tests.ContextTests.test_nested_requests',  # noqa
            'test_client_regress.tests.ContextTests.test_single_context',  # noqa
            'test_client_regress.tests.ExceptionTests.test_exception_cleared',  # noqa
            'test_client_regress.tests.LoginTests.test_login_different_client',  # noqa
            'test_client_regress.tests.SessionEngineTests.test_login',  # noqa
            'test_client_regress.tests.SessionTests.test_login_with_user',  # noqa
            'test_client_regress.tests.SessionTests.test_login_without_signal',  # noqa
            'test_client_regress.tests.SessionTests.test_logout',  # noqa
            'test_client_regress.tests.SessionTests.test_logout_with_custom_auth_backend',  # noqa
            'test_client_regress.tests.SessionTests.test_logout_with_custom_user',  # noqa
            'test_client_regress.tests.SessionTests.test_logout_with_user',  # noqa
            'test_client_regress.tests.SessionTests.test_logout_without_user',  # noqa
            'test_client_regress.tests.SessionTests.test_session',  # noqa
            'test_client_regress.tests.SessionTests.test_session_initiated',  # noqa
            'timezones.tests.NewDatabaseTests.test_null_datetime',
            'transactions.tests.NonAutocommitTests.test_orm_query_after_error_and_rollback',  # noqa
            'update_only_fields.tests.UpdateOnlyFieldsTests.test_empty_update_fields',  # noqa
            'update_only_fields.tests.UpdateOnlyFieldsTests.test_num_queries_inheritance',  # noqa
            'update_only_fields.tests.UpdateOnlyFieldsTests.test_select_related_only_interaction',  # noqa
            'update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_basic',  # noqa
            'update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_fk_defer',  # noqa
            'update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_incorrect_params',  # noqa
            'update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_inheritance',  # noqa
            'update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_inheritance_defer',  # noqa
            'update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_inheritance_with_proxy_model',  # noqa
            'update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_m2m',  # noqa
            'update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_only_1',  # noqa
            'update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_only_repeated',  # noqa
            'update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_signals',  # noqa
            'validation.tests.BaseModelValidationTests.test_correct_FK_value_validates',  # noqa
            'validation.tests.BaseModelValidationTests.test_limited_FK_raises_error',  # noqa
            'validation.tests.GenericIPAddressFieldTests.test_empty_generic_ip_passes',  # noqa
            'validation.tests.GenericIPAddressFieldTests.test_v4_unpack_uniqueness_detection',  # noqa
            'validation.tests.GenericIPAddressFieldTests.test_v6_uniqueness_detection',  # noqa
        )
