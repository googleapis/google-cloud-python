WITH `bfcte_0` AS (
  SELECT
    `int64_col`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE
      WHEN LOGICAL_OR(`int64_col` = 0) OVER (PARTITION BY `string_col`)
      THEN 0
      ELSE EXP(
        SUM(CASE WHEN `int64_col` = 0 THEN 0 ELSE LN(ABS(`int64_col`)) END) OVER (PARTITION BY `string_col`)
      ) * IF(
        MOD(
          SUM(CASE WHEN SIGN(`int64_col`) < 0 THEN 1 ELSE 0 END) OVER (PARTITION BY `string_col`),
          2
        ) = 1,
        -1,
        1
      )
    END AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `agg_int64`
FROM `bfcte_1`