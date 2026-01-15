WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    COALESCE(LOGICAL_OR(`bool_col`), FALSE) AS `bfcol_2`,
    COALESCE(LOGICAL_OR(`int64_col` <> 0), FALSE) AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `bool_col`,
  `bfcol_3` AS `int64_col`
FROM `bfcte_1`