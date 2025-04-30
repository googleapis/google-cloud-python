SELECT
  *
FROM UNNEST(ARRAY<STRUCT<`bfcol_0` INT64, `bfcol_1` STRUCT<name STRING, age INT64, address STRUCT<city STRING, country STRING>>, `bfcol_2` INT64>>[(
  1,
  STRUCT(
    'Alice' AS `name`,
    30 AS `age`,
    STRUCT('New York' AS `city`, 'USA' AS `country`) AS `address`
  ),
  0
), (
  2,
  STRUCT(
    'Bob' AS `name`,
    25 AS `age`,
    STRUCT('London' AS `city`, 'UK' AS `country`) AS `address`
  ),
  1
)])