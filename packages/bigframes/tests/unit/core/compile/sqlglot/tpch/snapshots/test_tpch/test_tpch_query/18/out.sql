WITH `bfcte_0` AS (
  SELECT
    `C_CUSTKEY` AS `bfcol_0`,
    `C_NAME` AS `bfcol_1`
  FROM `bigframes-dev`.`tpch`.`CUSTOMER` AS `bft_2` FOR SYSTEM_TIME AS OF '2026-03-10T18:00:00'
), `bfcte_1` AS (
  SELECT
    `L_ORDERKEY` AS `bfcol_2`,
    `L_QUANTITY` AS `bfcol_3`
  FROM `bigframes-dev`.`tpch`.`LINEITEM` AS `bft_1` FOR SYSTEM_TIME AS OF '2026-03-10T18:00:00'
), `bfcte_2` AS (
  SELECT
    `O_ORDERKEY` AS `bfcol_4`,
    `O_CUSTKEY` AS `bfcol_5`,
    `O_TOTALPRICE` AS `bfcol_6`,
    `O_ORDERDATE` AS `bfcol_7`
  FROM `bigframes-dev`.`tpch`.`ORDERS` AS `bft_0` FOR SYSTEM_TIME AS OF '2026-03-10T18:00:00'
), `bfcte_3` AS (
  SELECT
    `bfcol_2`,
    COALESCE(SUM(`bfcol_3`), 0) AS `bfcol_8`
  FROM `bfcte_1`
  WHERE
    NOT `bfcol_2` IS NULL
  GROUP BY
    `bfcol_2`
), `bfcte_4` AS (
  SELECT
    `bfcol_2`,
    `bfcol_8`,
    `bfcol_2` AS `bfcol_9`,
    `bfcol_8` > 300 AS `bfcol_10`
  FROM `bfcte_3`
  WHERE
    `bfcol_8` > 300
), `bfcte_5` AS (
  SELECT
    `bfcol_9`
  FROM `bfcte_4`
  GROUP BY
    `bfcol_9`
), `bfcte_6` AS (
  SELECT
    `bfcol_9` AS `bfcol_13`
  FROM `bfcte_5`
), `bfcte_7` AS (
  SELECT
    *,
    STRUCT(COALESCE(`bfcol_4`, 0) AS `bfpart1`, COALESCE(`bfcol_4`, 1) AS `bfpart2`) IN (
      (
        SELECT
          STRUCT(COALESCE(`bfcol_13`, 0) AS `bfpart1`, COALESCE(`bfcol_13`, 1) AS `bfpart2`)
        FROM `bfcte_6`
      )
    ) AS `bfcol_14`
  FROM `bfcte_2`
), `bfcte_8` AS (
  SELECT
    `bfcol_4` AS `bfcol_20`,
    `bfcol_5` AS `bfcol_21`,
    `bfcol_6` AS `bfcol_22`,
    `bfcol_7` AS `bfcol_23`
  FROM `bfcte_7`
  WHERE
    `bfcol_14`
), `bfcte_9` AS (
  SELECT
    `bfcol_20` AS `bfcol_24`,
    `bfcol_21` AS `bfcol_25`,
    `bfcol_22` AS `bfcol_26`,
    `bfcol_23` AS `bfcol_27`,
    `bfcol_3` AS `bfcol_28`
  FROM `bfcte_8`
  INNER JOIN `bfcte_1`
    ON COALESCE(`bfcol_20`, 0) = COALESCE(`bfcol_2`, 0)
    AND COALESCE(`bfcol_20`, 1) = COALESCE(`bfcol_2`, 1)
), `bfcte_10` AS (
  SELECT
    `bfcol_1`,
    `bfcol_0`,
    `bfcol_24`,
    `bfcol_27`,
    `bfcol_26`,
    COALESCE(SUM(`bfcol_28`), 0) AS `bfcol_35`
  FROM `bfcte_9`
  INNER JOIN `bfcte_0`
    ON COALESCE(`bfcol_25`, 0) = COALESCE(`bfcol_0`, 0)
    AND COALESCE(`bfcol_25`, 1) = COALESCE(`bfcol_0`, 1)
  WHERE
    NOT `bfcol_1` IS NULL
    AND NOT `bfcol_0` IS NULL
    AND NOT `bfcol_24` IS NULL
    AND NOT `bfcol_27` IS NULL
    AND NOT `bfcol_26` IS NULL
  GROUP BY
    `bfcol_1`,
    `bfcol_0`,
    `bfcol_24`,
    `bfcol_27`,
    `bfcol_26`
)
SELECT
  `bfcol_1` AS `C_NAME`,
  `bfcol_0` AS `C_CUSTKEY`,
  `bfcol_24` AS `O_ORDERKEY`,
  `bfcol_27` AS `O_ORDERDAT`,
  `bfcol_26` AS `O_TOTALPRICE`,
  `bfcol_35` AS `COL6`
FROM `bfcte_10`
ORDER BY
  `bfcol_26` DESC,
  `bfcol_27` ASC NULLS LAST,
  `bfcol_1` ASC NULLS LAST,
  `bfcol_0` ASC NULLS LAST,
  `bfcol_24` ASC NULLS LAST
LIMIT 100