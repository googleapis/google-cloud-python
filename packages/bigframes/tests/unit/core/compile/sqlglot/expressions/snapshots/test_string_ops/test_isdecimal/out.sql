SELECT
  REGEXP_CONTAINS(`string_col`, '^(\\p{Nd})+$') AS `string_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`