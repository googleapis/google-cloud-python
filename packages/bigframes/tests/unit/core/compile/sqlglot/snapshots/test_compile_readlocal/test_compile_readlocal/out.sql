SELECT
  *
FROM UNNEST(ARRAY<STRUCT<`bfcol_0` INT64, `bfcol_1` INT64, `bfcol_2` BOOLEAN, `bfcol_3` STRING, `bfcol_4` INT64>>[(1, -10, TRUE, 'b', 0), (2, 20, CAST(NULL AS BOOLEAN), 'aa', 1), (3, 30, FALSE, 'ccc', 2)])