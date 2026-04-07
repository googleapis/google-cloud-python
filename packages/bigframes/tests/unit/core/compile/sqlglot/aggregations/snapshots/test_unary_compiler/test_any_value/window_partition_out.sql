SELECT
  ANY_VALUE(`int64_col`) OVER (PARTITION BY `string_col`) AS `agg_int64`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`