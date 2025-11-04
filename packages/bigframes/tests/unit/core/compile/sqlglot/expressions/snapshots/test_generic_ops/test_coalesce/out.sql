WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`,
    `int64_too` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bfcol_0` AS `bfcol_2`,
    COALESCE(`bfcol_1`, `bfcol_0`) AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `int64_col`,
  `bfcol_3` AS `int64_too`
FROM `bfcte_1`