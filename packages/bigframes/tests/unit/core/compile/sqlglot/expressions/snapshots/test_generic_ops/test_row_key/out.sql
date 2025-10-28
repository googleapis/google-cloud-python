WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `bytes_col` AS `bfcol_1`,
    `date_col` AS `bfcol_2`,
    `datetime_col` AS `bfcol_3`,
    `geography_col` AS `bfcol_4`,
    `int64_col` AS `bfcol_5`,
    `int64_too` AS `bfcol_6`,
    `numeric_col` AS `bfcol_7`,
    `float64_col` AS `bfcol_8`,
    `rowindex` AS `bfcol_9`,
    `rowindex_2` AS `bfcol_10`,
    `string_col` AS `bfcol_11`,
    `time_col` AS `bfcol_12`,
    `timestamp_col` AS `bfcol_13`,
    `duration_col` AS `bfcol_14`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CONCAT(
      CAST(FARM_FINGERPRINT(
        CONCAT(
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_9` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_0` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_1` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_2` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_3` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(ST_ASTEXT(`bfcol_4`), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_5` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_6` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_7` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_8` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_9` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_10` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(`bfcol_11`, ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_12` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_13` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_14` AS STRING), ''), '\\', '\\\\'))
        )
      ) AS STRING),
      CAST(FARM_FINGERPRINT(
        CONCAT(
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_9` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_0` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_1` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_2` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_3` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(ST_ASTEXT(`bfcol_4`), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_5` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_6` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_7` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_8` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_9` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_10` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(`bfcol_11`, ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_12` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_13` AS STRING), ''), '\\', '\\\\')),
          CONCAT('\\', REPLACE(COALESCE(CAST(`bfcol_14` AS STRING), ''), '\\', '\\\\')),
          '_'
        )
      ) AS STRING),
      CAST(RAND() AS STRING)
    ) AS `bfcol_31`
  FROM `bfcte_0`
)
SELECT
  `bfcol_31` AS `row_key`
FROM `bfcte_1`