WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `int64_col` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    VAR_POP(`bfcol_1`) AS `bfcol_4`,
    VAR_POP(CAST(`bfcol_0` AS INT64)) AS `bfcol_5`
  FROM `bfcte_0`
)
SELECT
  `bfcol_4` AS `int64_col`,
  `bfcol_5` AS `bool_col`
FROM `bfcte_1`