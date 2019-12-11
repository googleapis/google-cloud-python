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
        # Tests that assume a serial pk.
        'admin_views.tests.AdminViewPermissionsTest.test_history_view',
        'aggregation_regress.tests.AggregationTests.test_more_more',
        'aggregation_regress.tests.AggregationTests.test_more_more_more',
        'aggregation_regress.tests.AggregationTests.test_ticket_11293',
        'defer_regress.tests.DeferRegressionTest.test_ticket_23270',
        'distinct_on_fields.tests.DistinctOnTests.test_basic_distinct_on',
        'generic_relations_regress.tests.GenericRelationTests.test_annotate',
        'migrations.test_operations.OperationTests.test_alter_order_with_respect_to',
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
        # To be investigated: https://github.com/orijtech/spanner-orm/issues/135
        'admin_changelist.tests.ChangeListTests.test_multiuser_edit',
    )
