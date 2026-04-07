WITH `bfcte_0` AS (
  SELECT
    `L_ORDERKEY` AS `bfcol_0`,
    `L_SHIPDATE` AS `bfcol_1`,
    `L_COMMITDATE` AS `bfcol_2`,
    `L_RECEIPTDATE` AS `bfcol_3`,
    `L_SHIPMODE` AS `bfcol_4`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_1`
), `bfcte_1` AS (
  SELECT
    `O_ORDERKEY` AS `bfcol_5`,
    `O_ORDERPRIORITY` AS `bfcol_6`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`ORDERS` AS `bft_0`
), `bfcte_2` AS (
  SELECT
    `bfcol_5`,
    `bfcol_6`,
    `bfcol_0`,
    `bfcol_1`,
    `bfcol_2`,
    `bfcol_3`,
    `bfcol_4`,
    `bfcol_6` AS `bfcol_12`,
    `bfcol_4` AS `bfcol_13`,
    (
      (
        (
          COALESCE(COALESCE(`bfcol_4` IN ('MAIL', 'SHIP'), FALSE), FALSE)
          AND (
            `bfcol_2` < `bfcol_3`
          )
        )
        AND (
          `bfcol_1` < `bfcol_2`
        )
      )
      AND (
        `bfcol_3` >= CAST('1994-01-01' AS DATE)
      )
    )
    AND (
      `bfcol_3` < CAST('1995-01-01' AS DATE)
    ) AS `bfcol_14`,
    `bfcol_6` AS `bfcol_20`,
    `bfcol_4` AS `bfcol_21`,
    CAST(COALESCE(COALESCE(`bfcol_6` IN ('1-URGENT', '2-HIGH'), FALSE), FALSE) AS INT64) AS `bfcol_22`,
    `bfcol_4` AS `bfcol_26`,
    CAST(COALESCE(COALESCE(`bfcol_6` IN ('1-URGENT', '2-HIGH'), FALSE), FALSE) AS INT64) AS `bfcol_27`,
    CAST(NOT (
      COALESCE(COALESCE(`bfcol_6` IN ('1-URGENT', '2-HIGH'), FALSE), FALSE)
    ) AS INT64) AS `bfcol_28`
  FROM `bfcte_1`
  INNER JOIN `bfcte_0`
    ON `bfcol_5` = `bfcol_0`
  WHERE
    (
      (
        (
          COALESCE(COALESCE(`bfcol_4` IN ('MAIL', 'SHIP'), FALSE), FALSE)
          AND (
            `bfcol_2` < `bfcol_3`
          )
        )
        AND (
          `bfcol_1` < `bfcol_2`
        )
      )
      AND (
        `bfcol_3` >= CAST('1994-01-01' AS DATE)
      )
    )
    AND (
      `bfcol_3` < CAST('1995-01-01' AS DATE)
    )
), `bfcte_3` AS (
  SELECT
    `bfcol_26`,
    COALESCE(SUM(`bfcol_27`), 0) AS `bfcol_32`,
    COALESCE(SUM(`bfcol_28`), 0) AS `bfcol_33`
  FROM `bfcte_2`
  GROUP BY
    `bfcol_26`
)
SELECT
  `bfcol_26` AS `L_SHIPMODE`,
  `bfcol_32` AS `HIGH_LINE_COUNT`,
  `bfcol_33` AS `LOW_LINE_COUNT`
FROM `bfcte_3`
ORDER BY
  `bfcol_26` ASC NULLS LAST