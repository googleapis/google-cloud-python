SELECT
  CASE
    WHEN STARTS_WITH(`string_col`, '-')
    THEN CONCAT('-', LPAD(SUBSTRING(`string_col`, 2), GREATEST(LENGTH(`string_col`), 10) - 1, '0'))
    ELSE LPAD(`string_col`, GREATEST(LENGTH(`string_col`), 10), '0')
  END AS `string_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`