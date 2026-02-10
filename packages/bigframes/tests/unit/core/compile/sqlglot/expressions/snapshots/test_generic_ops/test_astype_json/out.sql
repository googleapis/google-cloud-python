SELECT
  PARSE_JSON(CAST(`int64_col` AS STRING)) AS `int64_col`,
  PARSE_JSON(CAST(`float64_col` AS STRING)) AS `float64_col`,
  PARSE_JSON(CAST(`bool_col` AS STRING)) AS `bool_col`,
  PARSE_JSON(`string_col`) AS `string_col`,
  PARSE_JSON(CAST(`bool_col` AS STRING)) AS `bool_w_safe`,
  SAFE.PARSE_JSON(`string_col`) AS `string_w_safe`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`