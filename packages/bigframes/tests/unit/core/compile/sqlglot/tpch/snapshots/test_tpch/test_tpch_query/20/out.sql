WITH `bfcte_0` AS (
  SELECT
    `P_PARTKEY`,
    `P_NAME`,
    `P_PARTKEY` AS `bfcol_15`,
    STARTS_WITH(`P_NAME`, 'forest') AS `bfcol_16`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PART` AS `bft_4` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
  WHERE
    STARTS_WITH(`P_NAME`, 'forest')
), `bfcte_1` AS (
  SELECT
    `PS_PARTKEY` AS `bfcol_2`,
    `PS_SUPPKEY` AS `bfcol_3`,
    `PS_AVAILQTY` AS `bfcol_4`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PARTSUPP` AS `bft_3` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_2` AS (
  SELECT
    `L_PARTKEY`,
    `L_SUPPKEY`,
    `L_QUANTITY`,
    `L_SHIPDATE`,
    `L_PARTKEY` AS `bfcol_17`,
    `L_SUPPKEY` AS `bfcol_18`,
    `L_QUANTITY` AS `bfcol_19`,
    (
      `L_SHIPDATE` >= CAST('1994-01-01' AS DATE)
    )
    AND (
      `L_SHIPDATE` < CAST('1995-01-01' AS DATE)
    ) AS `bfcol_20`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_2` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
  WHERE
    (
      `L_SHIPDATE` >= CAST('1994-01-01' AS DATE)
    )
    AND (
      `L_SHIPDATE` < CAST('1995-01-01' AS DATE)
    )
), `bfcte_3` AS (
  SELECT
    `N_NATIONKEY` AS `bfcol_35`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`NATION` AS `bft_1` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
  WHERE
    `N_NAME` = 'CANADA'
), `bfcte_4` AS (
  SELECT
    `S_SUPPKEY` AS `bfcol_11`,
    `S_NAME` AS `bfcol_12`,
    `S_ADDRESS` AS `bfcol_13`,
    `S_NATIONKEY` AS `bfcol_14`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`SUPPLIER` AS `bft_0` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_5` AS (
  SELECT
    `bfcol_15`
  FROM `bfcte_0`
  GROUP BY
    `bfcol_15`
), `bfcte_6` AS (
  SELECT
    `bfcol_17`,
    `bfcol_18`,
    COALESCE(SUM(`bfcol_19`), 0) AS `bfcol_36`
  FROM `bfcte_2`
  GROUP BY
    `bfcol_17`,
    `bfcol_18`
), `bfcte_7` AS (
  SELECT
    `bfcol_11` AS `bfcol_41`,
    `bfcol_12` AS `bfcol_42`,
    `bfcol_13` AS `bfcol_43`
  FROM `bfcte_4`
  INNER JOIN `bfcte_3`
    ON `bfcol_14` = `bfcol_35`
), `bfcte_8` AS (
  SELECT
    `bfcol_15` AS `bfcol_31`
  FROM `bfcte_5`
), `bfcte_9` AS (
  SELECT
    `bfcol_17` AS `bfcol_48`,
    `bfcol_18` AS `bfcol_49`,
    `bfcol_36` * 0.5 AS `bfcol_50`
  FROM `bfcte_6`
), `bfcte_10` AS (
  SELECT
    *,
    `bfcol_2` IN ((
        SELECT
          *
        FROM `bfcte_8`
    )) AS `bfcol_37`
  FROM `bfcte_1`
), `bfcte_11` AS (
  SELECT
    `bfcol_2` AS `bfcol_51`,
    `bfcol_3` AS `bfcol_52`,
    `bfcol_4` AS `bfcol_53`
  FROM `bfcte_10`
  WHERE
    `bfcol_37`
), `bfcte_12` AS (
  SELECT
    `bfcol_48`,
    `bfcol_49`,
    `bfcol_50`,
    `bfcol_51`,
    `bfcol_52`,
    `bfcol_53`,
    `bfcol_52` AS `bfcol_57`,
    `bfcol_53` > `bfcol_50` AS `bfcol_58`
  FROM `bfcte_9`
  INNER JOIN `bfcte_11`
    ON `bfcol_49` = `bfcol_52` AND `bfcol_48` = `bfcol_51`
  WHERE
    `bfcol_53` > `bfcol_50`
), `bfcte_13` AS (
  SELECT
    `bfcol_57`
  FROM `bfcte_12`
  GROUP BY
    `bfcol_57`
), `bfcte_14` AS (
  SELECT
    `bfcol_57` AS `bfcol_61`
  FROM `bfcte_13`
), `bfcte_15` AS (
  SELECT
    *,
    `bfcol_41` IN ((
        SELECT
          *
        FROM `bfcte_14`
    )) AS `bfcol_62`
  FROM `bfcte_7`
)
SELECT
  `bfcol_42` AS `S_NAME`,
  `bfcol_43` AS `S_ADDRESS`
FROM `bfcte_15`
WHERE
  `bfcol_62`
ORDER BY
  `bfcol_42` ASC NULLS LAST