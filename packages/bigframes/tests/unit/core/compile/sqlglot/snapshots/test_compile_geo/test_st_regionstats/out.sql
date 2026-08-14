WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` STRING, `bfcol_1` INT64>>[STRUCT('POINT(1 1)', 0)])
)
SELECT
  ST_REGIONSTATS(
    `bfcol_0`,
    'ee://some/raster/uri',
    band => 'band1',
    include => 'some equation',
    options => JSON '{"scale": 100}'
  ).`min`,
  ST_REGIONSTATS(
    `bfcol_0`,
    'ee://some/raster/uri',
    band => 'band1',
    include => 'some equation',
    options => JSON '{"scale": 100}'
  ).`max`,
  ST_REGIONSTATS(
    `bfcol_0`,
    'ee://some/raster/uri',
    band => 'band1',
    include => 'some equation',
    options => JSON '{"scale": 100}'
  ).`sum`,
  ST_REGIONSTATS(
    `bfcol_0`,
    'ee://some/raster/uri',
    band => 'band1',
    include => 'some equation',
    options => JSON '{"scale": 100}'
  ).`count`,
  ST_REGIONSTATS(
    `bfcol_0`,
    'ee://some/raster/uri',
    band => 'band1',
    include => 'some equation',
    options => JSON '{"scale": 100}'
  ).`mean`,
  ST_REGIONSTATS(
    `bfcol_0`,
    'ee://some/raster/uri',
    band => 'band1',
    include => 'some equation',
    options => JSON '{"scale": 100}'
  ).`area`
FROM `bfcte_0`
ORDER BY
  `bfcol_1` ASC NULLS LAST