WITH `bfcte_0` AS (
  SELECT
    `O_ORDERKEY` AS `bfcol_32`,
    `O_CUSTKEY` AS `bfcol_33`,
    `O_ORDERDATE` AS `bfcol_34`,
    `O_SHIPPRIORITY` AS `bfcol_35`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`ORDERS` AS `bft_2` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
  WHERE
    `O_ORDERDATE` < CAST('1995-03-15' AS DATE)
), `bfcte_1` AS (
  SELECT
    `L_ORDERKEY` AS `bfcol_36`,
    `L_EXTENDEDPRICE` AS `bfcol_37`,
    `L_DISCOUNT` AS `bfcol_38`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_1` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
  WHERE
    `L_SHIPDATE` > CAST('1995-03-15' AS DATE)
), `bfcte_2` AS (
  SELECT
    `C_CUSTKEY` AS `bfcol_39`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`CUSTOMER` AS `bft_0` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
  WHERE
    `C_MKTSEGMENT` = 'BUILDING'
), `bfcte_3` AS (
  SELECT
    `bfcol_37` AS `bfcol_40`,
    `bfcol_38` AS `bfcol_41`,
    `bfcol_32` AS `bfcol_42`,
    `bfcol_33` AS `bfcol_43`,
    `bfcol_34` AS `bfcol_44`,
    `bfcol_35` AS `bfcol_45`
  FROM `bfcte_1`
  INNER JOIN `bfcte_0`
    ON `bfcol_36` = `bfcol_32`
), `bfcte_4` AS (
  SELECT
    `bfcol_39`,
    `bfcol_40`,
    `bfcol_41`,
    `bfcol_42`,
    `bfcol_43`,
    `bfcol_44`,
    `bfcol_45`,
    `bfcol_42` AS `bfcol_51`,
    `bfcol_44` AS `bfcol_52`,
    `bfcol_45` AS `bfcol_53`,
    `bfcol_40` * (
      1 - `bfcol_41`
    ) AS `bfcol_54`
  FROM `bfcte_2`
  INNER JOIN `bfcte_3`
    ON `bfcol_39` = `bfcol_43`
), `bfcte_5` AS (
  SELECT
    `bfcol_51`,
    `bfcol_52`,
    `bfcol_53`,
    COALESCE(SUM(`bfcol_54`), 0) AS `bfcol_59`
  FROM `bfcte_4`
  GROUP BY
    `bfcol_51`,
    `bfcol_52`,
    `bfcol_53`
)
SELECT
  `bfcol_51` AS `L_ORDERKEY`,
  `bfcol_59` AS `REVENUE`,
  `bfcol_52` AS `O_ORDERDATE`,
  `bfcol_53` AS `O_SHIPPRIORITY`
FROM `bfcte_5`
ORDER BY
  `bfcol_59` DESC,
  `bfcol_52` ASC NULLS LAST,
  `bfcol_51` ASC NULLS LAST,
  `bfcol_53` ASC NULLS LAST
LIMIT 10