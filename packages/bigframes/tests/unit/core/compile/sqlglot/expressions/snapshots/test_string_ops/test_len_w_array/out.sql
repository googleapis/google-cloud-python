WITH `bfcte_0` AS (
  SELECT
    `int_list_col`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`
), `bfcte_1` AS (
  SELECT
    *,
    ARRAY_LENGTH(`int_list_col`) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `int_list_col`
FROM `bfcte_1`