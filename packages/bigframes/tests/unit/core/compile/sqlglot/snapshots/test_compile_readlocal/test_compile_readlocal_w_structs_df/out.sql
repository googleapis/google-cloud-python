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
)
SELECT
  `bfcol_0` AS `id`,
  `bfcol_1` AS `person`
FROM `bfcte_0`
ORDER BY
  `bfcol_2` ASC NULLS LAST