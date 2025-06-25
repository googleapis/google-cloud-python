WITH `bfcte_0` AS (
  SELECT
    `rowindex` AS `bfcol_0`,
    `string_list_col` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`
), `bfcte_1` AS (
  SELECT
    *,
    ARRAY(
      SELECT
        el
      FROM UNNEST(`bfcol_1`) AS el WITH OFFSET AS slice_idx
      WHERE
        slice_idx >= 1 AND slice_idx < 5
    ) AS `bfcol_4`
  FROM `bfcte_0`
)
SELECT
  `bfcol_0` AS `rowindex`,
  `bfcol_4` AS `string_list_col`
FROM `bfcte_1`