WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_5` STRING, `bfcol_6` INT64, `bfcol_7` INT64>>[STRUCT('TOTAL_REVENUE', 0, 0)])
), `bfcte_1` AS (
  SELECT
    `L_SUPPKEY`,
    `L_EXTENDEDPRICE`,
    `L_DISCOUNT`,
    `L_SHIPDATE`,
    `L_SUPPKEY` AS `bfcol_12`,
    `L_EXTENDEDPRICE` AS `bfcol_13`,
    `L_DISCOUNT` AS `bfcol_14`,
    (
      `L_SHIPDATE` >= CAST('1996-01-01' AS DATE)
    )
    AND (
      `L_SHIPDATE` < CAST('1996-04-01' AS DATE)
    ) AS `bfcol_15`,
    `L_SUPPKEY` AS `bfcol_23`,
    `L_EXTENDEDPRICE` * (
      1 - `L_DISCOUNT`
    ) AS `bfcol_24`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_1` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
  WHERE
    (
      `L_SHIPDATE` >= CAST('1996-01-01' AS DATE)
    )
    AND (
      `L_SHIPDATE` < CAST('1996-04-01' AS DATE)
    )
), `bfcte_2` AS (
  SELECT
    `S_SUPPKEY` AS `bfcol_4`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`SUPPLIER` AS `bft_0` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_3` AS (
  SELECT
    `S_SUPPKEY` AS `bfcol_8`,
    `S_NAME` AS `bfcol_9`,
    `S_ADDRESS` AS `bfcol_10`,
    `S_PHONE` AS `bfcol_11`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`SUPPLIER` AS `bft_0` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_4` AS (
  SELECT
    `bfcol_23`,
    COALESCE(SUM(`bfcol_24`), 0) AS `bfcol_27`
  FROM `bfcte_1`
  GROUP BY
    `bfcol_23`
), `bfcte_5` AS (
  SELECT
    `bfcol_23` AS `bfcol_30`,
    ROUND(`bfcol_27`, 2) AS `bfcol_31`
  FROM `bfcte_4`
), `bfcte_6` AS (
  SELECT
    MAX(`bfcol_31`) AS `bfcol_38`
  FROM `bfcte_2`
  INNER JOIN `bfcte_5`
    ON `bfcol_4` = `bfcol_30`
), `bfcte_7` AS (
  SELECT
    `bfcol_8` AS `bfcol_33`,
    `bfcol_9` AS `bfcol_34`,
    `bfcol_10` AS `bfcol_35`,
    `bfcol_11` AS `bfcol_36`,
    `bfcol_31` AS `bfcol_37`
  FROM `bfcte_3`
  INNER JOIN `bfcte_5`
    ON `bfcol_8` = `bfcol_30`
), `bfcte_8` AS (
  SELECT
    `bfcol_38`,
    0 AS `bfcol_39`
  FROM `bfcte_6`
), `bfcte_9` AS (
  SELECT
    `bfcol_5`,
    `bfcol_6`,
    `bfcol_7`,
    `bfcol_38`,
    `bfcol_39`,
    CASE WHEN `bfcol_7` = 0 THEN `bfcol_38` END AS `bfcol_40`,
    IF(`bfcol_39` = 0, CASE WHEN `bfcol_7` = 0 THEN `bfcol_38` END, NULL) AS `bfcol_45`
  FROM `bfcte_0`
  CROSS JOIN `bfcte_8`
), `bfcte_10` AS (
  SELECT
    `bfcol_5`,
    `bfcol_6`,
    ANY_VALUE(`bfcol_45`) AS `bfcol_49`
  FROM `bfcte_9`
  GROUP BY
    `bfcol_5`,
    `bfcol_6`
), `bfcte_11` AS (
  SELECT
    `bfcol_49` AS `bfcol_50`
  FROM `bfcte_10`
)
SELECT
  `bfcol_33` AS `S_SUPPKEY`,
  `bfcol_34` AS `S_NAME`,
  `bfcol_35` AS `S_ADDRESS`,
  `bfcol_36` AS `S_PHONE`,
  `bfcol_37` AS `TOTAL_REVENUE`
FROM `bfcte_7`
CROSS JOIN `bfcte_11`
WHERE
  `bfcol_37` = `bfcol_50`
ORDER BY
  `bfcol_33` ASC NULLS LAST