WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_0`,
    `int_list_col` AS `bfcol_1`,
    `string_list_col` AS `bfcol_2`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`
), `bfcte_1` AS (
  SELECT
    *
    REPLACE (`bfcol_1`[SAFE_OFFSET(`bfcol_13`)] AS `bfcol_1`, `bfcol_2`[SAFE_OFFSET(`bfcol_13`)] AS `bfcol_2`)
  FROM `bfcte_0`
  CROSS JOIN UNNEST(GENERATE_ARRAY(0, LEAST(ARRAY_LENGTH(`bfcol_1`) - 1, ARRAY_LENGTH(`bfcol_2`) - 1))) AS `bfcol_13` WITH OFFSET AS `bfcol_7`
)
SELECT
  `bfcol_0` AS `rowindex`,
  `bfcol_0` AS `rowindex_1`,
  `bfcol_1` AS `int_list_col`,
  `bfcol_2` AS `string_list_col`
FROM `bfcte_1`
ORDER BY
  `bfcol_7` ASC NULLS LAST