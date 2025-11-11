WITH `bfcte_0` AS (
  SELECT
    `int64_col`,
    `int64_too`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `int64_col` AS `bfcol_2`,
    COALESCE(`int64_too`, `int64_col`) AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `int64_col`,
  `bfcol_3` AS `int64_too`
FROM `bfcte_1`