SELECT
  REGEXP_CONTAINS(`string_col`, '^\\s+$') AS `string_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`