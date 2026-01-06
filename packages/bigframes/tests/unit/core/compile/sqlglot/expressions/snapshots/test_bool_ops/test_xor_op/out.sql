WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `int64_col`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `rowindex` AS `bfcol_6`,
    `bool_col` AS `bfcol_7`,
    `int64_col` AS `bfcol_8`,
    `int64_col` ^ `int64_col` AS `bfcol_9`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_6` AS `bfcol_14`,
    `bfcol_7` AS `bfcol_15`,
    `bfcol_8` AS `bfcol_16`,
    `bfcol_9` AS `bfcol_17`,
    (
      `bfcol_7` AND NOT `bfcol_7`
    ) OR (
      NOT `bfcol_7` AND `bfcol_7`
    ) AS `bfcol_18`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *,
    `bfcol_14` AS `bfcol_24`,
    `bfcol_15` AS `bfcol_25`,
    `bfcol_16` AS `bfcol_26`,
    `bfcol_17` AS `bfcol_27`,
    `bfcol_18` AS `bfcol_28`,
    (
      `bfcol_15` AND NOT CAST(NULL AS BOOLEAN)
    )
    OR (
      NOT `bfcol_15` AND CAST(NULL AS BOOLEAN)
    ) AS `bfcol_29`
  FROM `bfcte_2`
)
SELECT
  `bfcol_24` AS `rowindex`,
  `bfcol_25` AS `bool_col`,
  `bfcol_26` AS `int64_col`,
  `bfcol_27` AS `int_and_int`,
  `bfcol_28` AS `bool_and_bool`,
  `bfcol_29` AS `bool_and_null`
FROM `bfcte_3`