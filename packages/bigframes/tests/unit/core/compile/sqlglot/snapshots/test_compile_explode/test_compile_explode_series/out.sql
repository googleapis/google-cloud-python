WITH `bfcte_0` AS (
  SELECT
    `rowindex`,
    `int_list_col`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types` AS `bft_0`
), `bfcte_1` AS (
  SELECT
    *
    REPLACE (`bfcol_8` AS `int_list_col`)
  FROM `bfcte_0`
  LEFT JOIN UNNEST(`int_list_col`) AS `bfcol_8` WITH OFFSET AS `bfcol_4`
)
SELECT
  `rowindex`,
  `int_list_col`
FROM `bfcte_1`
ORDER BY
  `bfcol_4` ASC NULLS LAST