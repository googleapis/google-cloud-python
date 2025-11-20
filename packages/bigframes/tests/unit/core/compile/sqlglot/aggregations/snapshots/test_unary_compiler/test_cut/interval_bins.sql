WITH `bfcte_0` AS (
  SELECT
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE
      WHEN `int64_col` > 0 AND `int64_col` <= 1
      THEN STRUCT(0 AS `left_exclusive`, 1 AS `right_inclusive`)
      WHEN `int64_col` > 1 AND `int64_col` <= 2
      THEN STRUCT(1 AS `left_exclusive`, 2 AS `right_inclusive`)
    END AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `interval_bins`
FROM `bfcte_1`