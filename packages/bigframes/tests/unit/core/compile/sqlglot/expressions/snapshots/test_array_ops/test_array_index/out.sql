SELECT
  IF(SUBSTRING(`string_col`, 2, 1) <> '', SUBSTRING(`string_col`, 2, 1), NULL) AS `string_index`,
  [`int64_col`, `int64_too`][SAFE_OFFSET(1)] AS `array_index`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`