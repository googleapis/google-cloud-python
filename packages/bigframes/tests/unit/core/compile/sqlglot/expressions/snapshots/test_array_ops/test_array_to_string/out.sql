WITH `bfcte_0` AS (
  SELECT
    `string_list_col`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`
), `bfcte_1` AS (
  SELECT
    *,
    ARRAY_TO_STRING(`string_list_col`, '.') AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `string_list_col`
FROM `bfcte_1`