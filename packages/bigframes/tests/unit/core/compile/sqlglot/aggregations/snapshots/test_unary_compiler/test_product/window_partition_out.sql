SELECT
  CASE
    WHEN LOGICAL_OR(`int64_col` = 0) OVER (PARTITION BY `string_col`)
    THEN 0
    ELSE POWER(
      2,
      SUM(IF(`int64_col` = 0, 0, LOG(ABS(`int64_col`), 2))) OVER (PARTITION BY `string_col`)
    ) * POWER(
      -1,
      MOD(
        SUM(CASE WHEN SIGN(`int64_col`) = -1 THEN 1 ELSE 0 END) OVER (PARTITION BY `string_col`),
        2
      )
    )
  END AS `agg_int64`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`