WITH `bfcte_0` AS (
  SELECT
    *,
    `bfcol_0` AS `bfcol_3`,
    `bfcol_1` + 1 AS `bfcol_4`
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` INT64, `bfcol_1` INT64, `bfcol_2` INT64>>[STRUCT(0, 123456789, 0), STRUCT(1, -987654321, 1), STRUCT(2, 314159, 2), STRUCT(3, CAST(NULL AS INT64), 3), STRUCT(4, -234892, 4), STRUCT(5, 55555, 5), STRUCT(6, 101202303, 6), STRUCT(7, -214748367, 7), STRUCT(8, 2, 8)])
)
SELECT
  `bfcol_3` AS `bfcol_5`,
  `bfcol_4` AS `bfcol_6`,
  `bfcol_2` AS `bfcol_7`
FROM `bfcte_0`