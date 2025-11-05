WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` STRING, `bfcol_1` INT64>>[STRUCT('POINT(1 1)', 0)])
), `bfcte_1` AS (
  SELECT
    *,
    ST_REGIONSTATS(
      `bfcol_0`,
      'ee://some/raster/uri',
      band => 'band1',
      include => 'some equation',
      options => JSON '{"scale": 100}'
    ) AS `bfcol_2`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_2`.`min` AS `bfcol_5`,
    `bfcol_2`.`max` AS `bfcol_6`,
    `bfcol_2`.`sum` AS `bfcol_7`,
    `bfcol_2`.`count` AS `bfcol_8`,
    `bfcol_2`.`mean` AS `bfcol_9`,
    `bfcol_2`.`area` AS `bfcol_10`
  FROM `bfcte_1`
)
SELECT
  `bfcol_5` AS `min`,
  `bfcol_6` AS `max`,
  `bfcol_7` AS `sum`,
  `bfcol_8` AS `count`,
  `bfcol_9` AS `mean`,
  `bfcol_10` AS `area`
FROM `bfcte_2`
ORDER BY
  `bfcol_1` ASC NULLS LAST