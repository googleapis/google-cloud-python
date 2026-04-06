WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_7` FLOAT64, `bfcol_8` INT64, `bfcol_9` INT64>>[STRUCT(0.0, 0, 0)])
), `bfcte_1` AS (
  SELECT
    `PS_SUPPKEY` AS `bfcol_0`,
    `PS_AVAILQTY` AS `bfcol_1`,
    `PS_SUPPLYCOST` AS `bfcol_2`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PARTSUPP` AS `bft_2`
), `bfcte_2` AS (
  SELECT
    `PS_PARTKEY` AS `bfcol_10`,
    `PS_SUPPKEY` AS `bfcol_11`,
    `PS_AVAILQTY` AS `bfcol_12`,
    `PS_SUPPLYCOST` AS `bfcol_13`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PARTSUPP` AS `bft_2`
), `bfcte_3` AS (
  SELECT
    `S_SUPPKEY` AS `bfcol_3`,
    `S_NATIONKEY` AS `bfcol_4`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`SUPPLIER` AS `bft_1`
), `bfcte_4` AS (
  SELECT
    `N_NATIONKEY` AS `bfcol_18`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`NATION` AS `bft_0`
  WHERE
    `N_NAME` = 'GERMANY'
), `bfcte_5` AS (
  SELECT
    `bfcol_3` AS `bfcol_19`
  FROM `bfcte_4`
  INNER JOIN `bfcte_3`
    ON `bfcol_18` = `bfcol_4`
), `bfcte_6` AS (
  SELECT
    `bfcol_19`,
    `bfcol_0`,
    `bfcol_1`,
    `bfcol_2`,
    `bfcol_1` AS `bfcol_25`,
    `bfcol_2` AS `bfcol_26`,
    `bfcol_2` AS `bfcol_33`,
    `bfcol_1` AS `bfcol_34`,
    `bfcol_2` * `bfcol_1` AS `bfcol_40`
  FROM `bfcte_5`
  INNER JOIN `bfcte_1`
    ON `bfcol_19` = `bfcol_0`
), `bfcte_7` AS (
  SELECT
    `bfcol_19`,
    `bfcol_10`,
    `bfcol_11`,
    `bfcol_12`,
    `bfcol_13`,
    `bfcol_10` AS `bfcol_27`,
    `bfcol_13` * `bfcol_12` AS `bfcol_28`
  FROM `bfcte_5`
  INNER JOIN `bfcte_2`
    ON `bfcol_19` = `bfcol_11`
), `bfcte_8` AS (
  SELECT
    COALESCE(SUM(`bfcol_40`), 0) AS `bfcol_44`
  FROM `bfcte_6`
), `bfcte_9` AS (
  SELECT
    `bfcol_27`,
    COALESCE(SUM(`bfcol_28`), 0) AS `bfcol_35`
  FROM `bfcte_7`
  GROUP BY
    `bfcol_27`
), `bfcte_10` AS (
  SELECT
    `bfcol_44`,
    0 AS `bfcol_45`
  FROM `bfcte_8`
), `bfcte_11` AS (
  SELECT
    `bfcol_27` AS `bfcol_41`,
    ROUND(`bfcol_35`, 2) AS `bfcol_42`
  FROM `bfcte_9`
), `bfcte_12` AS (
  SELECT
    `bfcol_7`,
    `bfcol_8`,
    `bfcol_9`,
    `bfcol_44`,
    `bfcol_45`,
    CASE WHEN `bfcol_9` = 0 THEN `bfcol_44` END AS `bfcol_46`,
    IF(`bfcol_45` = 0, CASE WHEN `bfcol_9` = 0 THEN `bfcol_44` END, NULL) AS `bfcol_51`
  FROM `bfcte_0`
  CROSS JOIN `bfcte_10`
), `bfcte_13` AS (
  SELECT
    `bfcol_7`,
    `bfcol_8`,
    ANY_VALUE(`bfcol_51`) AS `bfcol_55`
  FROM `bfcte_12`
  GROUP BY
    `bfcol_7`,
    `bfcol_8`
), `bfcte_14` AS (
  SELECT
    `bfcol_55` * 0.0001 AS `bfcol_58`
  FROM `bfcte_13`
)
SELECT
  `bfcol_41` AS `PS_PARTKEY`,
  `bfcol_42` AS `VALUE`
FROM `bfcte_11`
CROSS JOIN `bfcte_14`
WHERE
  `bfcol_42` > `bfcol_58`
ORDER BY
  `bfcol_42` DESC