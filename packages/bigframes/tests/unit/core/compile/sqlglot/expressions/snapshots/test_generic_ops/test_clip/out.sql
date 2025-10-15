WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`,
    `int64_too` AS `bfcol_1`,
    `rowindex` AS `bfcol_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    GREATEST(LEAST(`bfcol_2`, `bfcol_1`), `bfcol_0`) AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_3` AS `result_col`
FROM `bfcte_1`