WITH `bfcte_0` AS (
  SELECT
    `O_ORDERKEY` AS `bfcol_0`,
    `O_ORDERDATE` AS `bfcol_1`,
    `O_ORDERPRIORITY` AS `bfcol_2`
  FROM `bigframes-dev`.`tpch`.`ORDERS` AS `bft_1` FOR SYSTEM_TIME AS OF '2026-03-10T18:00:00'
), `bfcte_1` AS (
  SELECT
    `L_ORDERKEY` AS `bfcol_3`,
    `L_COMMITDATE` AS `bfcol_4`,
    `L_RECEIPTDATE` AS `bfcol_5`
  FROM `bigframes-dev`.`tpch`.`LINEITEM` AS `bft_0` FOR SYSTEM_TIME AS OF '2026-03-10T18:00:00'
), `bfcte_2` AS (
  SELECT
    `bfcol_3`,
    `bfcol_4`,
    `bfcol_5`,
    `bfcol_0`,
    `bfcol_1`,
    `bfcol_2`,
    `bfcol_3` AS `bfcol_11`,
    `bfcol_4` AS `bfcol_12`,
    `bfcol_5` AS `bfcol_13`,
    `bfcol_2` AS `bfcol_14`,
    (
      `bfcol_1` >= CAST('1993-07-01' AS DATE)
    )
    AND (
      `bfcol_1` < CAST('1993-10-01' AS DATE)
    ) AS `bfcol_15`,
    `bfcol_3` AS `bfcol_25`,
    `bfcol_2` AS `bfcol_26`,
    `bfcol_4` < `bfcol_5` AS `bfcol_27`
  FROM `bfcte_1`
  INNER JOIN `bfcte_0`
    ON `bfcol_3` = `bfcol_0`
  WHERE
    (
      `bfcol_1` >= CAST('1993-07-01' AS DATE)
    )
    AND (
      `bfcol_1` < CAST('1993-10-01' AS DATE)
    )
    AND `bfcol_4` < `bfcol_5`
), `bfcte_3` AS (
  SELECT
    `bfcol_26`,
    `bfcol_25`,
    COUNT(1) AS `bfcol_33`
  FROM `bfcte_2`
  GROUP BY
    `bfcol_26`,
    `bfcol_25`
), `bfcte_4` AS (
  SELECT
    `bfcol_26`,
    COUNT(`bfcol_25`) AS `bfcol_36`
  FROM `bfcte_3`
  GROUP BY
    `bfcol_26`
)
SELECT
  `bfcol_26` AS `O_ORDERPRIORITY`,
  `bfcol_36` AS `ORDER_COUNT`
FROM `bfcte_4`
ORDER BY
  `bfcol_26` ASC NULLS LAST