SELECT
  COALESCE(SUM(`int64_col`) OVER (PARTITION BY `string_col`), 0) AS `agg_int64`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`