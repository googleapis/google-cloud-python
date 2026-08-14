WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` FLOAT64, `bfcol_1` FLOAT64, `bfcol_2` FLOAT64, `bfcol_3` FLOAT64, `bfcol_4` STRUCT<foo INT64>, `bfcol_5` STRUCT<foo INT64>, `bfcol_6` ARRAY<INT64>, `bfcol_7` INT64>>[STRUCT(
    CAST(NULL AS FLOAT64),
    CAST('Infinity' AS FLOAT64),
    CAST('-Infinity' AS FLOAT64),
    CAST(NULL AS FLOAT64),
    CAST(NULL AS STRUCT<foo INT64>),
    STRUCT(CAST(NULL AS INT64) AS `foo`),
    ARRAY<INT64>[],
    0
  ), STRUCT(1.0, 1.0, 1.0, 1.0, STRUCT(1 AS `foo`), STRUCT(1 AS `foo`), [1, 2], 1), STRUCT(2.0, 2.0, 2.0, 2.0, STRUCT(2 AS `foo`), STRUCT(2 AS `foo`), [3, 4], 2)])
)
SELECT
  `bfcol_0` AS `col_none`,
  `bfcol_1` AS `col_inf`,
  `bfcol_2` AS `col_neginf`,
  `bfcol_3` AS `col_nan`,
  `bfcol_4` AS `col_struct_none`,
  `bfcol_5` AS `col_struct_w_none`,
  `bfcol_6` AS `col_list_none`
FROM `bfcte_0`
ORDER BY
  `bfcol_7` ASC NULLS LAST