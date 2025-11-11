WITH `bfcte_0` AS (
  SELECT
    `json_col`
  FROM `bigframes-dev`.`sqlglot_test`.`json_types`
), `bfcte_1` AS (
  SELECT
    *,
    JSON_EXTRACT_STRING_ARRAY(`json_col`, '$') AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `json_col`
FROM `bfcte_1`