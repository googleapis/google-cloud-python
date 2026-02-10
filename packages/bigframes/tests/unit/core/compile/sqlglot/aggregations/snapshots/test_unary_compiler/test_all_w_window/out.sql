SELECT
  COALESCE(LOGICAL_AND(`bool_col`) OVER (), TRUE) AS `agg_bool`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`