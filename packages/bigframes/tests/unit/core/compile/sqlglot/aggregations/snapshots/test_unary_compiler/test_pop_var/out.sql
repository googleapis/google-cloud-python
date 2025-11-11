WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    VAR_POP(`int64_col`) AS `bfcol_4`,
    VAR_POP(CAST(`bool_col` AS INT64)) AS `bfcol_5`
  FROM `bfcte_0`
)
SELECT
  `bfcol_4` AS `int64_col`,
  `bfcol_5` AS `bool_col`
FROM `bfcte_1`