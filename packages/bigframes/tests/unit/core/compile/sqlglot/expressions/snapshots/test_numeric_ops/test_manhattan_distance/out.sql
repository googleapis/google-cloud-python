WITH `bfcte_0` AS (
  SELECT
    `float_list_col`,
    `numeric_list_col`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`
), `bfcte_1` AS (
  SELECT
    *,
    ML.DISTANCE(`float_list_col`, `float_list_col`, 'MANHATTAN') AS `bfcol_2`,
    ML.DISTANCE(`numeric_list_col`, `numeric_list_col`, 'MANHATTAN') AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `float_list_col`,
  `bfcol_3` AS `numeric_list_col`
FROM `bfcte_1`