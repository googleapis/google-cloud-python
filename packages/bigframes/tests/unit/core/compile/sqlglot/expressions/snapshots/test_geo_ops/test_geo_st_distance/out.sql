WITH `bfcte_0` AS (
  SELECT
    `geography_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    ST_DISTANCE(`geography_col`, `geography_col`, TRUE) AS `bfcol_1`,
    ST_DISTANCE(`geography_col`, `geography_col`, FALSE) AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `spheroid`,
  `bfcol_2` AS `no_spheroid`
FROM `bfcte_1`