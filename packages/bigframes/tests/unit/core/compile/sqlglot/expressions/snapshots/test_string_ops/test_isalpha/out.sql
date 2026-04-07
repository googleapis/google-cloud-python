SELECT
  REGEXP_CONTAINS(`string_col`, '^\\p{L}+$') AS `string_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`