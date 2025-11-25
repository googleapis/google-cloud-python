WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `float64_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bool_col` AS `bfcol_3`,
    `int64_col` AS `bfcol_4`,
    `float64_col` AS `bfcol_5`,
    (
      `int64_col` >= 0
    ) AND (
      `int64_col` <= 10
    ) AS `bfcol_6`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *
  FROM `bfcte_1`
  WHERE
    `bfcol_6`
), `bfcte_3` AS (
  SELECT
    *,
    POWER(`bfcol_4`, `bfcol_4`) AS `bfcol_14`,
    POWER(`bfcol_4`, `bfcol_5`) AS `bfcol_15`,
    POWER(`bfcol_5`, `bfcol_4`) AS `bfcol_16`,
    POWER(`bfcol_5`, `bfcol_5`) AS `bfcol_17`,
    POWER(`bfcol_4`, CAST(`bfcol_3` AS INT64)) AS `bfcol_18`,
    POWER(CAST(`bfcol_3` AS INT64), `bfcol_4`) AS `bfcol_19`
  FROM `bfcte_2`
)
SELECT
  `bfcol_14` AS `int_pow_int`,
  `bfcol_15` AS `int_pow_float`,
  `bfcol_16` AS `float_pow_int`,
  `bfcol_17` AS `float_pow_float`,
  `bfcol_18` AS `int_pow_bool`,
  `bfcol_19` AS `bool_pow_int`
FROM `bfcte_3`