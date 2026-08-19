SELECT
  LOWER(`string_col`) = `string_col` AND UPPER(`string_col`) <> `string_col` AS `string_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`