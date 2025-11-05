WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` STRING, `bfcol_1` INT64>>[STRUCT('POINT(1 1)', 0)])
), `bfcte_1` AS (
  SELECT
    *,
    ST_SIMPLIFY(`bfcol_0`, 123.125) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `0`
FROM `bfcte_1`
ORDER BY
  `bfcol_1` ASC NULLS LAST