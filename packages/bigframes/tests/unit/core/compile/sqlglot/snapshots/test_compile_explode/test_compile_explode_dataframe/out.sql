WITH `bfcte_0` AS (
  SELECT
    `int_list_col`,
    `rowindex`,
    `string_list_col`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`
), `bfcte_1` AS (
  SELECT
    *
    REPLACE (`int_list_col`[SAFE_OFFSET(`bfcol_13`)] AS `int_list_col`, `string_list_col`[SAFE_OFFSET(`bfcol_13`)] AS `string_list_col`)
  FROM `bfcte_0`
  LEFT JOIN UNNEST(GENERATE_ARRAY(0, LEAST(ARRAY_LENGTH(`int_list_col`) - 1, ARRAY_LENGTH(`string_list_col`) - 1))) AS `bfcol_13` WITH OFFSET AS `bfcol_7`
)
SELECT
  `rowindex`,
  `rowindex` AS `rowindex_1`,
  `int_list_col`,
  `string_list_col`
FROM `bfcte_1`
ORDER BY
  `bfcol_7` ASC NULLS LAST