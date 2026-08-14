WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_8` STRING, `bfcol_9` INT64, `bfcol_10` INT64>>[STRUCT('L_EXTENDEDPRICE', 0, 0)])
), `bfcte_1` AS (
  SELECT
    `P_PARTKEY` AS `bfcol_15`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PART` AS `bft_1`
  WHERE
    (
      `P_BRAND` = 'Brand#23'
    ) AND (
      `P_CONTAINER` = 'MED BOX'
    )
), `bfcte_2` AS (
  SELECT
    `L_PARTKEY` AS `bfcol_3`,
    `L_QUANTITY` AS `bfcol_4`,
    `L_EXTENDEDPRICE` AS `bfcol_5`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_0`
), `bfcte_3` AS (
  SELECT
    `L_PARTKEY` AS `bfcol_6`,
    `L_QUANTITY` AS `bfcol_7`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_0`
), `bfcte_4` AS (
  SELECT
    `bfcol_4` AS `bfcol_16`,
    `bfcol_5` AS `bfcol_17`,
    `bfcol_15` AS `bfcol_18`
  FROM `bfcte_2`
  RIGHT JOIN `bfcte_1`
    ON `bfcol_3` = `bfcol_15`
), `bfcte_5` AS (
  SELECT
    `bfcol_15`,
    AVG(`bfcol_7`) AS `bfcol_21`
  FROM `bfcte_3`
  RIGHT JOIN `bfcte_1`
    ON `bfcol_6` = `bfcol_15`
  GROUP BY
    `bfcol_15`
), `bfcte_6` AS (
  SELECT
    `bfcol_15` AS `bfcol_24`,
    `bfcol_21` * 0.2 AS `bfcol_25`
  FROM `bfcte_5`
), `bfcte_7` AS (
  SELECT
    `bfcol_24`,
    `bfcol_25`,
    `bfcol_16`,
    `bfcol_17`,
    `bfcol_18`,
    `bfcol_17` AS `bfcol_29`,
    `bfcol_16` < `bfcol_25` AS `bfcol_30`
  FROM `bfcte_6`
  INNER JOIN `bfcte_4`
    ON `bfcol_24` = `bfcol_18`
  WHERE
    `bfcol_16` < `bfcol_25`
), `bfcte_8` AS (
  SELECT
    COALESCE(SUM(`bfcol_29`), 0) AS `bfcol_34`
  FROM `bfcte_7`
), `bfcte_9` AS (
  SELECT
    `bfcol_34`,
    0 AS `bfcol_35`
  FROM `bfcte_8`
), `bfcte_10` AS (
  SELECT
    `bfcol_8`,
    `bfcol_9`,
    `bfcol_10`,
    `bfcol_34`,
    `bfcol_35`,
    CASE WHEN `bfcol_10` = 0 THEN `bfcol_34` END AS `bfcol_36`,
    IF(`bfcol_35` = 0, CASE WHEN `bfcol_10` = 0 THEN `bfcol_34` END, NULL) AS `bfcol_41`
  FROM `bfcte_0`
  CROSS JOIN `bfcte_9`
), `bfcte_11` AS (
  SELECT
    `bfcol_8`,
    `bfcol_9`,
    ANY_VALUE(`bfcol_41`) AS `bfcol_45`
  FROM `bfcte_10`
  GROUP BY
    `bfcol_8`,
    `bfcol_9`
)
SELECT
  ROUND(IEEE_DIVIDE(`bfcol_45`, 7.0), 2) AS `AVG_YEARLY`
FROM `bfcte_11`
ORDER BY
  `bfcol_9` ASC NULLS LAST,
  `bfcol_8` ASC NULLS LAST