WITH `bfcte_0` AS (
  SELECT
    `json_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`json_types`
), `bfcte_1` AS (
  SELECT
    *,
    INT64(`bfcol_0`) AS `bfcol_1`,
    FLOAT64(`bfcol_0`) AS `bfcol_2`,
    BOOL(`bfcol_0`) AS `bfcol_3`,
    STRING(`bfcol_0`) AS `bfcol_4`,
    SAFE.INT64(`bfcol_0`) AS `bfcol_5`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `int64_col`,
  `bfcol_2` AS `float64_col`,
  `bfcol_3` AS `bool_col`,
  `bfcol_4` AS `string_col`,
  `bfcol_5` AS `int64_w_safe`
FROM `bfcte_1`