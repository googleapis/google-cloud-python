SELECT
  ST_BUFFER(`geography_col`, 1.0, 8.0, FALSE) AS `geography_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`