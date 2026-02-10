SELECT
  IF(SUBSTRING(`string_col`, 2, 1) <> '', SUBSTRING(`string_col`, 2, 1), NULL) AS `string_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`