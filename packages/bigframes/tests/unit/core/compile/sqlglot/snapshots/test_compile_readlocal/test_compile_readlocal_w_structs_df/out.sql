WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` INT64, `bfcol_1` STRUCT<name STRING, age INT64, address STRUCT<city STRING, country STRING>>, `bfcol_2` INT64>>[STRUCT(
    1,
    STRUCT(
      'Alice' AS `name`,
      30 AS `age`,
      STRUCT('New York' AS `city`, 'USA' AS `country`) AS `address`
    ),
    0
  ), STRUCT(
    2,
    STRUCT(
      'Bob' AS `name`,
      25 AS `age`,
      STRUCT('London' AS `city`, 'UK' AS `country`) AS `address`
    ),
    1
  )])
), `bfcte_1` AS (
  SELECT
    `bfcol_0` AS `bfcol_3`,
    `bfcol_1` AS `bfcol_4`,
    `bfcol_2` AS `bfcol_5`
  FROM `bfcte_0`
)
SELECT
  `bfcol_3` AS `id`,
  `bfcol_4` AS `person`
FROM `bfcte_1`
ORDER BY
  `bfcol_5` ASC NULLS LAST