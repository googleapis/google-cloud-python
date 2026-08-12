WITH `bfcte_0` AS (
  SELECT
    `int_list_col`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types` AS `bft_0`
), `bfcte_1` AS (
  SELECT
    COALESCE(LOGICAL_OR(ARRAY_LENGTH(`int_list_col`) > 0), FALSE) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `int_list_col`
FROM `bfcte_1`