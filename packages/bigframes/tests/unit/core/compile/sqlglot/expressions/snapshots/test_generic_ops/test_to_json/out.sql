SELECT
  IF(`int64_col` IS NULL, NULL, TO_JSON(`int64_col`)) AS `int64_col`,
  IF(`float64_col` IS NULL, NULL, TO_JSON(`float64_col`)) AS `float64_col`,
  IF(`bool_col` IS NULL, NULL, TO_JSON(`bool_col`)) AS `bool_col`,
  SAFE.PARSE_JSON(`string_col`) AS `string_col`,
  IF(`bool_col` IS NULL, NULL, TO_JSON(`bool_col`)) AS `bool_w_safe`,
  SAFE.PARSE_JSON(`string_col`) AS `string_w_safe`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`