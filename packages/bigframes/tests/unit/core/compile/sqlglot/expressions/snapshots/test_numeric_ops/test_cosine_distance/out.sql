WITH `bfcte_0` AS (
  SELECT
    `float_list_col`,
    `int_list_col`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`
), `bfcte_1` AS (
  SELECT
    *,
    ML.DISTANCE(`int_list_col`, `int_list_col`, 'COSINE') AS `bfcol_2`,
    ML.DISTANCE(`float_list_col`, `float_list_col`, 'COSINE') AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `int_list_col`,
  `bfcol_3` AS `float_list_col`
FROM `bfcte_1`