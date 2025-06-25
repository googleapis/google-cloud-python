WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_0`,
    `int_list_col` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`
), `bfcte_1` AS (
  SELECT
    *
    REPLACE (`bfcol_8` AS `bfcol_1`)
  FROM `bfcte_0`
  CROSS JOIN UNNEST(`bfcol_1`) AS `bfcol_8` WITH OFFSET AS `bfcol_4`
)
SELECT
  `bfcol_0` AS `rowindex`,
  `bfcol_1` AS `int_list_col`
FROM `bfcte_1`
ORDER BY
  `bfcol_4` ASC NULLS LAST