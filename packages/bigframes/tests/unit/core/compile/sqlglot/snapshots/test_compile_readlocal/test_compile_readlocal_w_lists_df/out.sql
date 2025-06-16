WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` INT64, `bfcol_1` ARRAY<INT64>, `bfcol_2` ARRAY<BOOLEAN>, `bfcol_3` ARRAY<FLOAT64>, `bfcol_4` ARRAY<STRING>, `bfcol_5` ARRAY<STRING>, `bfcol_6` ARRAY<FLOAT64>, `bfcol_7` ARRAY<STRING>, `bfcol_8` INT64>>[STRUCT(
    0,
    [1],
    [TRUE],
    [1.2, 2.3],
    ['2021-07-21'],
    ['2021-07-21 11:39:45'],
    [1.2, 2.3, 3.4],
    ['abc', 'de', 'f'],
    0
  ), STRUCT(
    1,
    [1, 2],
    [TRUE, FALSE],
    [1.1],
    ['2021-07-21', '1987-03-28'],
    ['1999-03-14 17:22:00'],
    [5.5, 2.3],
    ['a', 'bc', 'de'],
    1
  ), STRUCT(
    2,
    [1, 2, 3],
    [TRUE],
    [0.5, -1.9, 2.3],
    ['2017-08-01', '2004-11-22'],
    ['1979-06-03 03:20:45'],
    [1.7000000000000002],
    ['', 'a'],
    2
  )])
), `bfcte_1` AS (
  SELECT
    `bfcol_0` AS `bfcol_9`,
    `bfcol_1` AS `bfcol_10`,
    `bfcol_2` AS `bfcol_11`,
    `bfcol_3` AS `bfcol_12`,
    `bfcol_4` AS `bfcol_13`,
    `bfcol_5` AS `bfcol_14`,
    `bfcol_6` AS `bfcol_15`,
    `bfcol_7` AS `bfcol_16`,
    `bfcol_8` AS `bfcol_17`
  FROM `bfcte_0`
)
SELECT
  `bfcol_9` AS `rowindex`,
  `bfcol_10` AS `int_list_col`,
  `bfcol_11` AS `bool_list_col`,
  `bfcol_12` AS `float_list_col`,
  `bfcol_13` AS `date_list_col`,
  `bfcol_14` AS `date_time_list_col`,
  `bfcol_15` AS `numeric_list_col`,
  `bfcol_16` AS `string_list_col`
FROM `bfcte_1`
ORDER BY
  `bfcol_17` ASC NULLS LAST