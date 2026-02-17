SELECT
  INT64(`json_col`) AS `int64_col`,
  FLOAT64(`json_col`) AS `float64_col`,
  BOOL(`json_col`) AS `bool_col`,
  STRING(`json_col`) AS `string_col`,
  SAFE.INT64(`json_col`) AS `int64_w_safe`
FROM `bigframes-dev`.`sqlglot_test`.`json_types` AS `bft_0`