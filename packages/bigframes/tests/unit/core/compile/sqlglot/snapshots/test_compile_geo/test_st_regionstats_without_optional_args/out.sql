WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` STRING, `bfcol_1` INT64>>[STRUCT('POINT(1 1)', 0)])
)
SELECT
  ST_REGIONSTATS(`bfcol_0`, 'ee://some/raster/uri').`min`,
  ST_REGIONSTATS(`bfcol_0`, 'ee://some/raster/uri').`max`,
  ST_REGIONSTATS(`bfcol_0`, 'ee://some/raster/uri').`sum`,
  ST_REGIONSTATS(`bfcol_0`, 'ee://some/raster/uri').`count`,
  ST_REGIONSTATS(`bfcol_0`, 'ee://some/raster/uri').`mean`,
  ST_REGIONSTATS(`bfcol_0`, 'ee://some/raster/uri').`area`
FROM `bfcte_0`
ORDER BY
  `bfcol_1` ASC NULLS LAST