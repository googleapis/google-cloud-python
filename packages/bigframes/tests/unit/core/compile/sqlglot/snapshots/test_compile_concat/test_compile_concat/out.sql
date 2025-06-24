WITH `bfcte_1` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` INT64, `bfcol_1` INT64, `bfcol_2` INT64, `bfcol_3` STRING, `bfcol_4` INT64>>[STRUCT(0, 123456789, 0, 'Hello, World!', 0), STRUCT(1, -987654321, 1, 'こんにちは', 1), STRUCT(2, 314159, 2, '  ¡Hola Mundo!  ', 2), STRUCT(3, CAST(NULL AS INT64), 3, CAST(NULL AS STRING), 3), STRUCT(4, -234892, 4, 'Hello, World!', 4), STRUCT(5, 55555, 5, 'Güten Tag!', 5), STRUCT(6, 101202303, 6, 'capitalize, This ', 6), STRUCT(7, -214748367, 7, ' سلام', 7), STRUCT(8, 2, 8, 'T', 8)])
), `bfcte_3` AS (
  SELECT
    *,
    `bfcol_4` AS `bfcol_10`
  FROM `bfcte_1`
), `bfcte_5` AS (
  SELECT
    *,
    0 AS `bfcol_16`
  FROM `bfcte_3`
), `bfcte_6` AS (
  SELECT
    `bfcol_0` AS `bfcol_17`,
    `bfcol_2` AS `bfcol_18`,
    `bfcol_1` AS `bfcol_19`,
    `bfcol_3` AS `bfcol_20`,
    `bfcol_16` AS `bfcol_21`,
    `bfcol_10` AS `bfcol_22`
  FROM `bfcte_5`
), `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_23` INT64, `bfcol_24` INT64, `bfcol_25` INT64, `bfcol_26` STRING, `bfcol_27` INT64>>[STRUCT(0, 123456789, 0, 'Hello, World!', 0), STRUCT(1, -987654321, 1, 'こんにちは', 1), STRUCT(2, 314159, 2, '  ¡Hola Mundo!  ', 2), STRUCT(3, CAST(NULL AS INT64), 3, CAST(NULL AS STRING), 3), STRUCT(4, -234892, 4, 'Hello, World!', 4), STRUCT(5, 55555, 5, 'Güten Tag!', 5), STRUCT(6, 101202303, 6, 'capitalize, This ', 6), STRUCT(7, -214748367, 7, ' سلام', 7), STRUCT(8, 2, 8, 'T', 8)])
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_27` AS `bfcol_33`
  FROM `bfcte_0`
), `bfcte_4` AS (
  SELECT
    *,
    1 AS `bfcol_39`
  FROM `bfcte_2`
), `bfcte_7` AS (
  SELECT
    `bfcol_23` AS `bfcol_40`,
    `bfcol_25` AS `bfcol_41`,
    `bfcol_24` AS `bfcol_42`,
    `bfcol_26` AS `bfcol_43`,
    `bfcol_39` AS `bfcol_44`,
    `bfcol_33` AS `bfcol_45`
  FROM `bfcte_4`
), `bfcte_8` AS (
  SELECT
    *
  FROM (
    SELECT
      `bfcol_17` AS `bfcol_46`,
      `bfcol_18` AS `bfcol_47`,
      `bfcol_19` AS `bfcol_48`,
      `bfcol_20` AS `bfcol_49`,
      `bfcol_21` AS `bfcol_50`,
      `bfcol_22` AS `bfcol_51`
    FROM `bfcte_6`
    UNION ALL
    SELECT
      `bfcol_40` AS `bfcol_46`,
      `bfcol_41` AS `bfcol_47`,
      `bfcol_42` AS `bfcol_48`,
      `bfcol_43` AS `bfcol_49`,
      `bfcol_44` AS `bfcol_50`,
      `bfcol_45` AS `bfcol_51`
    FROM `bfcte_7`
  )
)
SELECT
  `bfcol_46` AS `rowindex`,
  `bfcol_47` AS `rowindex_1`,
  `bfcol_48` AS `int64_col`,
  `bfcol_49` AS `string_col`
FROM `bfcte_8`
ORDER BY
  `bfcol_50` ASC NULLS LAST,
  `bfcol_51` ASC NULLS LAST