SELECT
  SAFE.INT64(`json_col`) AS `int64_col`,
  SAFE.FLOAT64(`json_col`) AS `float64_col`,
  SAFE.BOOL(`json_col`) AS `bool_col`,
  SAFE.STRING(`json_col`) AS `string_col`,
  SAFE.INT64(`json_col`) AS `int64_w_safe`
FROM `bigframes-dev`.`sqlglot_test`.`json_types` AS `bft_0`