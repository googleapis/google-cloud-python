WITH `bfcte_0` AS (
  SELECT
    `int_list_col`,
    `numeric_list_col`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`
), `bfcte_1` AS (
  SELECT
    *,
    ML.DISTANCE(`int_list_col`, `int_list_col`, 'EUCLIDEAN') AS `bfcol_2`,
    ML.DISTANCE(`numeric_list_col`, `numeric_list_col`, 'EUCLIDEAN') AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `int_list_col`,
  `bfcol_3` AS `numeric_list_col`
FROM `bfcte_1`