WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `float64_col`,
    `int64_col`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    PARSE_JSON(CAST(`int64_col` AS STRING)) AS `bfcol_4`,
    PARSE_JSON(CAST(`float64_col` AS STRING)) AS `bfcol_5`,
    PARSE_JSON(CAST(`bool_col` AS STRING)) AS `bfcol_6`,
    PARSE_JSON(`string_col`) AS `bfcol_7`,
    PARSE_JSON(CAST(`bool_col` AS STRING)) AS `bfcol_8`,
    SAFE.PARSE_JSON(`string_col`) AS `bfcol_9`
  FROM `bfcte_0`
)
SELECT
  `bfcol_4` AS `int64_col`,
  `bfcol_5` AS `float64_col`,
  `bfcol_6` AS `bool_col`,
  `bfcol_7` AS `string_col`,
  `bfcol_8` AS `bool_w_safe`,
  `bfcol_9` AS `string_w_safe`
FROM `bfcte_1`