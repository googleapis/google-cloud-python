# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import os

from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.utils import InterfaceError

from django_spanner import USE_EMULATOR


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
    max_query_params = 900
    # Spanner does not support parameterized defaults in DDL
    requires_literal_defaults = True

    if os.environ.get("RUNNING_SPANNER_BACKEND_TESTS") == "1":
        supports_foreign_keys = False
    else:
        supports_foreign_keys = True
    can_create_inline_fk = False
    supports_ignore_conflicts = False
    supports_partial_indexes = False
    supports_regex_backreferencing = False
    supports_select_for_update_with_limit = False
    supports_sequence_reset = False
    supports_timezones = False
    supports_transactions = True
    if USE_EMULATOR:
        # Emulator does not support json.
        supports_json_field = False
        # Emulator does not support check constrints.
        supports_column_check_constraints = False
        supports_table_check_constraints = False
    else:
        supports_column_check_constraints = True
        supports_table_check_constraints = True
        supports_json_field = True
    supports_primitives_in_json_field = False
    supports_composite_primary_keys = True
    # Spanner does not support order by null modifiers.
    supports_order_by_nulls_modifier = False
    # Spanner does not support SELECTing an arbitrary expression that also
    # appears in the GROUP BY clause.
    supports_subqueries_in_group_by = False
    uses_savepoints = True
    can_rollback_tests = False  # Spanner savepoints are no-ops; rely on flush.
    supports_aggregate_filter_clause = False
    # Spanner does not support expression indexes
    # example: CREATE INDEX index_name ON table (LOWER(column_name))
    supports_expression_indexes = False
    supports_stored_generated_columns = True

    # Django tests that aren't supported by Spanner.
    skip_tests = (
        "backends.base.test_base.DatabaseWrapperLoggingTests.test_commit_debug_log",
        "backends.base.test_base.ExecuteWrapperTests.test_wrapper_debug",
        "backends.base.test_base.MultiDatabaseTests.test_multi_database_init_connection_state_called_once",
        "backends.tests.BackendTestCase.test_cursor_execute_with_pyformat",
        "backends.tests.BackendTestCase.test_cursor_executemany",
        "backends.tests.BackendTestCase.test_cursor_executemany_with_iterator",
        "backends.tests.BackendTestCase.test_cursor_executemany_with_pyformat",
        "backends.tests.BackendTestCase.test_cursor_executemany_with_pyformat_iterator",
        "backends.tests.BackendTestCase.test_queries",
        "backends.tests.BackendTestCase.test_queries_bare_where",
        "backends.tests.BackendTestCase.test_queries_logger",
        "backends.tests.LastExecutedQueryTest.test_last_executed_query",
        "backends.tests.LastExecutedQueryTest.test_last_executed_query_dict",
        "backends.tests.LastExecutedQueryTest.test_last_executed_query_dict_overlap_keys",
        "backends.tests.LastExecutedQueryTest.test_last_executed_query_with_duplicate_params",
        "constraints.tests.CheckConstraintTests.test_database_default",
        "constraints.tests.CheckConstraintTests.test_validate",
        "constraints.tests.CheckConstraintTests.test_validate_boolean_expressions",
        "constraints.tests.CheckConstraintTests.test_validate_custom_error",
        "constraints.tests.CheckConstraintTests.test_validate_generated_field_stored",
        "constraints.tests.CheckConstraintTests.test_validate_pk_field",
        "constraints.tests.UniqueConstraintTests.test_validate_case_when",
        "constraints.tests.UniqueConstraintTests.test_validate_expression_condition",
        "constraints.tests.UniqueConstraintTests.test_validate_expression_generated_field_stored",
        "constraints.tests.UniqueConstraintTests.test_validate_fields_generated_field_stored_nulls_distinct",
        "custom_pk.tests.CustomPKTests.test_auto_field_subclass_create",
        "datetimes.tests.DateTimesTests.test_21432",
        "db_functions.comparison.test_cast.CastTests.test_cast_from_db_date_to_datetime",
        "db_functions.comparison.test_cast.CastTests.test_cast_to_decimal_field",
        "db_functions.datetime.test_extract_trunc.DateFunctionTests.test_extract_func",
        "db_functions.datetime.test_extract_trunc.DateFunctionTests.test_extract_iso_weekday_func",
        "db_functions.datetime.test_extract_trunc.DateFunctionTests.test_extract_lookup_name_sql_injection",
        "db_functions.datetime.test_extract_trunc.DateFunctionTests.test_trunc_lookup_name_sql_injection",
        "db_functions.datetime.test_extract_trunc.DateFunctionTests.test_trunc_time_comparison",
        "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_extract_func",
        "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_extract_func_with_timezone",
        "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_extract_iso_weekday_func",
        "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_extract_lookup_name_sql_injection",
        "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_func_with_timezone",
        "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_lookup_name_sql_injection",
        "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_time_comparison",
        "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_timezone_applied_before_truncation",
        "db_functions.json.test_json_object.JSONObjectTests.test_basic",
        "db_functions.json.test_json_object.JSONObjectTests.test_empty",
        "db_functions.json.test_json_object.JSONObjectTests.test_expressions",
        "db_functions.json.test_json_object.JSONObjectTests.test_nested_empty_json_object",
        "db_functions.json.test_json_object.JSONObjectTests.test_nested_json_object",
        "db_functions.json.test_json_object.JSONObjectTests.test_order_by_key",
        "db_functions.json.test_json_object.JSONObjectTests.test_order_by_nested_key",
        "db_functions.json.test_json_object.JSONObjectTests.test_textfield",
        "db_functions.math.test_cos.CosTests.test_transform",
        "db_functions.math.test_degrees.DegreesTests.test_decimal",
        "db_functions.math.test_mod.ModTests.test_float",
        "db_functions.math.test_random.RandomTests.test",
        "db_functions.text.test_concat.ConcatTests.test_concat_non_str",
        "db_functions.text.test_md5.MD5Tests.test_basic",
        "db_functions.text.test_md5.MD5Tests.test_transform",
        "db_functions.text.test_sha1.SHA1Tests.test_basic",
        "db_functions.text.test_sha1.SHA1Tests.test_transform",
        "db_functions.text.test_sha224.SHA224Tests.test_basic",
        "db_functions.text.test_sha224.SHA224Tests.test_transform",
        "db_functions.text.test_sha256.SHA256Tests.test_basic",
        "db_functions.text.test_sha256.SHA256Tests.test_transform",
        "db_functions.text.test_sha384.SHA384Tests.test_basic",
        "db_functions.text.test_sha384.SHA384Tests.test_transform",
        "db_functions.text.test_sha512.SHA512Tests.test_basic",
        "db_functions.text.test_sha512.SHA512Tests.test_transform",
        "defer_regress.tests.DeferRegressionTest.test_self_referential_one_to_one",
        "empty.tests.EmptyModelTests.test_empty",
        "expressions.test_queryset_values.ValuesExpressionsTests.test_values_expression",
        "expressions.tests.BasicExpressionsTests.test_filter_with_join",
        "expressions.tests.BasicExpressionsTests.test_nested_subquery_join_outer_ref",
        "expressions.tests.BasicExpressionsTests.test_outerref_mixed_case_table_name",
        "expressions.tests.BasicExpressionsTests.test_ticket_16731_startswith_lookup",
        "expressions.tests.ExpressionOperatorTests.test_lefthand_bitwise_xor_right_null",
        "expressions.tests.ExpressionOperatorTests.test_lefthand_division",
        "expressions.tests.ExpressionOperatorTests.test_lefthand_power",
        "expressions.tests.ExpressionOperatorTests.test_right_hand_division",
        "expressions.tests.ExpressionOperatorTests.test_righthand_power",
        "expressions.tests.FTimeDeltaTests.test_date_comparison",
        "expressions.tests.FTimeDeltaTests.test_date_minus_duration",
        "expressions.tests.FTimeDeltaTests.test_delta_add",
        "expressions.tests.FTimeDeltaTests.test_duration_with_datetime",
        "expressions.tests.FTimeDeltaTests.test_durationfield_multiply_divide",
        "expressions.tests.FTimeDeltaTests.test_mixed_comparisons1",
        "expressions.tests.FTimeDeltaTests.test_mixed_comparisons2",
        "foreign_object.test_tuple_lookups.TupleLookupsTests.test_exact",
        "foreign_object.test_tuple_lookups.TupleLookupsTests.test_gt",
        "foreign_object.test_tuple_lookups.TupleLookupsTests.test_gte",
        "foreign_object.test_tuple_lookups.TupleLookupsTests.test_in",
        "foreign_object.test_tuple_lookups.TupleLookupsTests.test_in_subquery",
        "foreign_object.test_tuple_lookups.TupleLookupsTests.test_isnull",
        "foreign_object.test_tuple_lookups.TupleLookupsTests.test_lt",
        "foreign_object.test_tuple_lookups.TupleLookupsTests.test_lte",
        "foreign_object.test_tuple_lookups.TupleLookupsTests.test_tuple_in_subquery",
        "foreign_object.tests.MultiColumnFKTests.test_double_nested_query",
        "foreign_object.tests.MultiColumnFKTests.test_forward_in_lookup_filters_correctly",
        "foreign_object.tests.MultiColumnFKTests.test_prefetch_foreignobject_hidden_forward",
        "foreign_object.tests.MultiColumnFKTests.test_translations",
        "generic_relations.test_forms.GenericInlineFormsetTests.test_options",
        "generic_relations.tests.GenericRelationsTests.test_add_bulk_false",
        "generic_relations.tests.GenericRelationsTests.test_unsaved_generic_foreign_key_parent_bulk_create",
        "generic_relations.tests.GenericRelationsTests.test_unsaved_generic_foreign_key_parent_save",
        "generic_relations_regress.tests.GenericRelationTests.test_charlink_filter",
        "generic_relations_regress.tests.GenericRelationTests.test_textlink_filter",
        "generic_relations_regress.tests.GenericRelationTests.test_ticket_20378",
        "generic_relations_regress.tests.GenericRelationTests.test_ticket_20564",
        "generic_relations_regress.tests.GenericRelationTests.test_ticket_20564_nullable_fk",
        "get_or_create.tests.UpdateOrCreateTests.test_integrity",
        "get_or_create.tests.UpdateOrCreateTests.test_manual_primary_key_test",
        "get_or_create.tests.UpdateOrCreateTests.test_update_only_defaults_and_pre_save_fields_when_local_fields",
        "get_or_create.tests.UpdateOrCreateTestsWithManualPKs.test_create_with_duplicate_primary_key",
        "many_to_many.tests.ManyToManyTests.test_add",
        "many_to_many.tests.ManyToManyTests.test_add_existing_different_type",
        "many_to_one_null.tests.ManyToOneNullTests.test_set_clear_non_bulk",
        "many_to_one_null.tests.ManyToOneNullTests.test_unsaved",
        "model_inheritance.tests.ModelInheritanceDataTests.test_update_query_counts",
        "model_inheritance.tests.ModelInheritanceTests.test_create_child_no_update",
        "model_inheritance.tests.ModelInheritanceTests.test_create_copy_with_inherited_m2m",
        "model_inheritance.tests.ModelInheritanceTests.test_create_diamond_mti_common_parent",
        "model_inheritance.tests.ModelInheritanceTests.test_create_diamond_mti_default_pk",
        "queries.test_q.QCheckTests.test_basic",
        "queries.test_q.QCheckTests.test_boolean_expression",
        "queries.test_q.QCheckTests.test_expression",
        "queries.test_qs_combinators.QuerySetSetOperationTests.test_union_empty_slice",
        "queries.test_qs_combinators.QuerySetSetOperationTests.test_union_with_extra_and_values_list",
        "queries.test_qs_combinators.QuerySetSetOperationTests.test_union_with_select_related_and_order",
        "queries.test_qs_combinators.QuerySetSetOperationTests.test_union_with_values_list_and_order",
        "schema.tests.SchemaTests.test_add_auto_field",
        "schema.tests.SchemaTests.test_add_field_both_defaults_preserves_db_default",
        "schema.tests.SchemaTests.test_add_field_durationfield_with_default",
        "schema.tests.SchemaTests.test_add_generated_field_contains",
        "schema.tests.SchemaTests.test_add_text_field_with_db_default",
        "schema.tests.SchemaTests.test_alter_auto_field_quoted_db_column",
        "schema.tests.SchemaTests.test_alter_auto_field_to_char_field",
        "schema.tests.SchemaTests.test_alter_auto_field_to_integer_field",
        "schema.tests.SchemaTests.test_alter_field_default_dropped",
        "schema.tests.SchemaTests.test_alter_int_pk_to_int_unique",
        "schema.tests.SchemaTests.test_alter_not_unique_field_to_primary_key",
        "schema.tests.SchemaTests.test_alter_null_to_not_null",
        "schema.tests.SchemaTests.test_alter_null_with_default_value_deferred_constraints",
        "schema.tests.SchemaTests.test_alter_pk_with_self_referential_field",
        "schema.tests.SchemaTests.test_alter_primary_key_quoted_db_table",
        "schema.tests.SchemaTests.test_alter_primary_key_the_same_name",
        "schema.tests.SchemaTests.test_alter_text_field_to_date_field",
        "schema.tests.SchemaTests.test_alter_text_field_to_datetime_field",
        "schema.tests.SchemaTests.test_alter_text_field_to_not_null_with_default_value",
        "schema.tests.SchemaTests.test_alter_text_field_to_time_field",
        "schema.tests.SchemaTests.test_autofield_to_o2o",
        "schema.tests.SchemaTests.test_char_field_pk_to_auto_field",
        "schema.tests.SchemaTests.test_ci_cs_db_collation",
        "schema.tests.SchemaTests.test_db_default_output_field_resolving",
        "schema.tests.SchemaTests.test_m2m_rename_field_in_target_model",
        "schema.tests.SchemaTests.test_m2m_repoint",
        "schema.tests.SchemaTests.test_m2m_repoint_custom",
        "schema.tests.SchemaTests.test_m2m_repoint_inherited",
        "schema.tests.SchemaTests.test_primary_key",
        "schema.tests.SchemaTests.test_referenced_field_without_constraint_rename_inside_atomic_block",
        "schema.tests.SchemaTests.test_rename",
        "schema.tests.SchemaTests.test_rename_column_renames_deferred_sql_references",
        "schema.tests.SchemaTests.test_rename_keep_db_default",
        "schema.tests.SchemaTests.test_rename_keep_null_status",
        "schema.tests.SchemaTests.test_rename_referenced_field",
        "schema.tests.SchemaTests.test_unique",
        "schema.tests.SchemaTests.test_unique_name_quoting",
        "schema.tests.SchemaTests.test_unsupported_transactional_ddl_disallowed",
        "select_related.tests.SelectRelatedTests.test_field_traversal",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_save_doesnt_clear_data_async",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_session_asave_does_not_resurrect_session_logged_out_in_other_context",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_session_get_decoded",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_session_key_empty_string_invalid",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_session_key_is_read_only",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_session_key_too_short_invalid",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_session_key_valid_string_saved",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_session_load_does_not_create_record",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_session_load_does_not_create_record_async",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_session_save_does_not_resurrect_session_logged_out_in_other_context",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_session_str",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_sessionmanager_save",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_setdefault",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_setdefault_async",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_store",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_store_async",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_update",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_update_async",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_values",
        "sessions_tests.tests.DatabaseSessionWithTimeZoneTests.test_values_async",
        "sessions_tests.tests.SessionMiddlewareTests.test_empty_session_saved",
        "sessions_tests.tests.SessionMiddlewareTests.test_flush_empty_without_session_cookie_doesnt_set_cookie",
        "sessions_tests.tests.SessionMiddlewareTests.test_httponly_session_cookie",
        "sessions_tests.tests.SessionMiddlewareTests.test_no_httponly_session_cookie",
        "sessions_tests.tests.SessionMiddlewareTests.test_samesite_session_cookie",
        "sessions_tests.tests.SessionMiddlewareTests.test_secure_session_cookie",
        "sessions_tests.tests.SessionMiddlewareTests.test_session_delete_on_end",
        "sessions_tests.tests.SessionMiddlewareTests.test_session_delete_on_end_with_custom_domain_and_path",
        "sessions_tests.tests.SessionMiddlewareTests.test_session_save_on_500",
        "sessions_tests.tests.SessionMiddlewareTests.test_session_save_on_5xx",
        "sessions_tests.tests.SessionMiddlewareTests.test_session_update_error_redirect",
        "sites_tests.tests.SitesFrameworkTests.test_check_site_id",
        "sites_tests.tests.SitesFrameworkTests.test_clear_site_cache",
        "sites_tests.tests.SitesFrameworkTests.test_clear_site_cache_domain",
        "sites_tests.tests.SitesFrameworkTests.test_delete_all_sites_clears_cache",
        "sites_tests.tests.SitesFrameworkTests.test_domain_name_with_whitespaces",
        "sites_tests.tests.SitesFrameworkTests.test_get_current_site",
        "sites_tests.tests.SitesFrameworkTests.test_get_current_site_host_with_trailing_dot",
        "sites_tests.tests.SitesFrameworkTests.test_get_current_site_no_site_id",
        "sites_tests.tests.SitesFrameworkTests.test_get_current_site_no_site_id_and_handle_port_fallback",
        "sites_tests.tests.SitesFrameworkTests.test_site_cache",
        "sites_tests.tests.SitesFrameworkTests.test_site_manager",
        "sites_tests.tests.SitesFrameworkTests.test_site_natural_key",
        "sites_tests.tests.SitesFrameworkTests.test_unique_domain",
        "sites_tests.tests.SitesFrameworkTests.test_valid_site_id",
        "transaction_hooks.tests.TestConnectionOnCommit.test_discards_hooks_from_rolled_back_savepoint",
        "transaction_hooks.tests.TestConnectionOnCommit.test_inner_savepoint_rolled_back_with_outer",
        "transaction_hooks.tests.TestConnectionOnCommit.test_no_savepoints_atomic_merged_with_outer",
        "update_only_fields.tests.UpdateOnlyFieldsTests.test_num_queries_inheritance",
        "update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_fk_defer",
        "update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_inheritance",
        "update_only_fields.tests.UpdateOnlyFieldsTests.test_update_fields_inheritance_defer",
        "view_tests.tests.test_defaults.DefaultsTests.test_bad_request",
        "view_tests.tests.test_defaults.DefaultsTests.test_csrf_token_in_404",
        "view_tests.tests.test_defaults.DefaultsTests.test_custom_bad_request_template",
        "view_tests.tests.test_defaults.DefaultsTests.test_custom_templates",
        "view_tests.tests.test_defaults.DefaultsTests.test_custom_templates_wrong",
        "view_tests.tests.test_defaults.DefaultsTests.test_error_pages",
        "view_tests.tests.test_defaults.DefaultsTests.test_get_absolute_url_attributes",
        "view_tests.tests.test_defaults.DefaultsTests.test_page_not_found",
        "view_tests.tests.test_defaults.DefaultsTests.test_server_error",
        # Chunk 2 Failures
        "delete.tests.DeletionTests.test_bulk",
        "delete.tests.DeletionTests.test_cannot_defer_constraint_checks",
        "delete.tests.DeletionTests.test_deletion_order",
        "delete.tests.DeletionTests.test_large_delete",
        "delete.tests.DeletionTests.test_large_delete_related",
        "delete.tests.DeletionTests.test_only_referenced_fields_selected",
        "delete.tests.DeletionTests.test_pk_none",
        "delete.tests.DeletionTests.test_proxied_model_duplicate_queries",
        "delete.tests.FastDeleteTests.test_fast_delete_aggregation",
        "delete.tests.FastDeleteTests.test_fast_delete_all",
        "delete.tests.FastDeleteTests.test_fast_delete_combined_relationships",
        "delete.tests.FastDeleteTests.test_fast_delete_empty_no_update_can_self_select",
        "delete.tests.FastDeleteTests.test_fast_delete_empty_result_set",
        "delete.tests.FastDeleteTests.test_fast_delete_fk",
        "delete.tests.FastDeleteTests.test_fast_delete_full_match",
        "delete.tests.FastDeleteTests.test_fast_delete_inheritance",
        "delete.tests.FastDeleteTests.test_fast_delete_joined_qs",
        "delete.tests.FastDeleteTests.test_fast_delete_large_batch",
        "delete.tests.FastDeleteTests.test_fast_delete_m2m",
        "delete.tests.FastDeleteTests.test_fast_delete_qs",
        "delete.tests.FastDeleteTests.test_fast_delete_revm2m",
        "delete_regress.tests.DeleteLockingTest.test_concurrent_delete",
        "delete_regress.tests.DeleteTests.test_self_reference_with_through_m2m_at_second_level",
        "delete_regress.tests.SetQueryCountTests.test_set_querycount",
        "delete_regress.tests.Ticket19102Tests.test_ticket_19102_annotate",
        "delete_regress.tests.Ticket19102Tests.test_ticket_19102_defer",
        "delete_regress.tests.Ticket19102Tests.test_ticket_19102_extra",
        "delete_regress.tests.Ticket19102Tests.test_ticket_19102_select_related",
        "fixtures.tests.ForwardReferenceTests.test_forward_reference_fk_natural_key",
        "fixtures.tests.ForwardReferenceTests.test_forward_reference_m2m",
        "fixtures.tests.ForwardReferenceTests.test_forward_reference_m2m_natural_key",
        "known_related_objects.tests.ExistingRelatedInstancesTests.test_multilevel_reverse_fk_select_related",
        "known_related_objects.tests.ExistingRelatedInstancesTests.test_reverse_fk_select_related_multiple",
        "known_related_objects.tests.ExistingRelatedInstancesTests.test_reverse_one_to_one_multi_prefetch_related",
        "known_related_objects.tests.ExistingRelatedInstancesTests.test_reverse_one_to_one_multi_select_related",
        "lookup.tests.LookupQueryingTests.test_annotate_greater_than_or_equal_float",
        "lookup.tests.LookupQueryingTests.test_annotate_less_than_float",
        "lookup.tests.LookupQueryingTests.test_in_lookup_in_filter",
        "lookup.tests.LookupTests.test_exact_query_rhs_with_selected_columns",
        "lookup.tests.LookupTests.test_get_next_previous_by",
        "lookup.tests.LookupTests.test_in_ignore_none",
        "lookup.tests.LookupTests.test_in_ignore_none_with_unhashable_items",
        "lookup.tests.LookupTests.test_lookup_direct_value_rhs_unwrapped",
        "lookup.tests.LookupTests.test_values_list",
        "model_formsets.tests.ModelFormsetTest.test_edit_only_object_outside_of_queryset",
        "model_formsets.tests.ModelFormsetTest.test_prevent_change_outer_model_and_create_invalid_data",
        "model_inheritance_regress.tests.ModelInheritanceTest.test_id_field_update_on_ancestor_change",
        "model_inheritance_regress.tests.ModelInheritanceTest.test_issue_6755",
    )

    if os.environ.get("SPANNER_EMULATOR_HOST", None):
        # Some code isn't yet supported by the Spanner emulator.
        pass
