WITH `bfcte_0` AS (
  SELECT
    `string_list_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`
), `bfcte_1` AS (
  SELECT
    *,
    ARRAY_TO_STRING(`bfcol_0`, '.') AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `string_list_col`
FROM `bfcte_1`