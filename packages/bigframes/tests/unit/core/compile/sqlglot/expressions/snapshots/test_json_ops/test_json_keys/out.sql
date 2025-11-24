WITH `bfcte_0` AS (
  SELECT
    `json_col`
  FROM `bigframes-dev`.`sqlglot_test`.`json_types`
), `bfcte_1` AS (
  SELECT
    *,
    JSON_KEYS(`json_col`, NULL) AS `bfcol_1`,
    JSON_KEYS(`json_col`, 2) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `json_keys`,
  `bfcol_2` AS `json_keys_w_max_depth`
FROM `bfcte_1`