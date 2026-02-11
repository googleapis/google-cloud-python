SELECT
  NOT IS_INF(`float64_col`) OR IS_NAN(`float64_col`) AS `float64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`