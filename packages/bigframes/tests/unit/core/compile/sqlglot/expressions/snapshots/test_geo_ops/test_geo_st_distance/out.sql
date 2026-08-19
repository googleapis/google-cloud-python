SELECT
  ST_DISTANCE(`geography_col`, `geography_col`, TRUE) AS `spheroid`,
  ST_DISTANCE(`geography_col`, `geography_col`, FALSE) AS `no_spheroid`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`