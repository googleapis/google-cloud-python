SELECT
  COALESCE(LOGICAL_OR(`bool_col`) OVER (), FALSE) AS `agg_bool`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`