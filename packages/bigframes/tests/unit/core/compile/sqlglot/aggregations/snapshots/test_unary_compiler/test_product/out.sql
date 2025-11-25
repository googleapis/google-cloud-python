WITH `bfcte_0` AS (
  SELECT
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    CASE
      WHEN LOGICAL_OR(`int64_col` = 0)
      THEN 0
      ELSE EXP(SUM(CASE WHEN `int64_col` = 0 THEN 0 ELSE LN(ABS(`int64_col`)) END)) * IF(MOD(SUM(CASE WHEN SIGN(`int64_col`) < 0 THEN 1 ELSE 0 END), 2) = 1, -1, 1)
    END AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `int64_col`
FROM `bfcte_1`