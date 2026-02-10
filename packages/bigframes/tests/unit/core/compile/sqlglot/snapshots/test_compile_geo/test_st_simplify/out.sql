WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` STRING, `bfcol_1` INT64>>[STRUCT('POINT(1 1)', 0)])
)
SELECT
  ST_SIMPLIFY(`bfcol_0`, 123.125) AS `0`
FROM `bfcte_0`
ORDER BY
  `bfcol_1` ASC NULLS LAST