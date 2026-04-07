SELECT
  CONCAT(
    CAST(FARM_FINGERPRINT(
      CONCAT(
        CONCAT('\\', REPLACE(COALESCE(CAST(`rowindex` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`bool_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`bytes_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`date_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`datetime_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(ST_ASTEXT(`geography_col`), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`int64_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`int64_too` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`numeric_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`float64_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`rowindex` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`rowindex_2` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(`string_col`, ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`time_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`timestamp_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`duration_col` AS STRING), ''), '\\', '\\\\'))
      )
    ) AS STRING),
    CAST(FARM_FINGERPRINT(
      CONCAT(
        CONCAT('\\', REPLACE(COALESCE(CAST(`rowindex` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`bool_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`bytes_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`date_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`datetime_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(ST_ASTEXT(`geography_col`), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`int64_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`int64_too` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`numeric_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`float64_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`rowindex` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`rowindex_2` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(`string_col`, ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`time_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`timestamp_col` AS STRING), ''), '\\', '\\\\')),
        CONCAT('\\', REPLACE(COALESCE(CAST(`duration_col` AS STRING), ''), '\\', '\\\\')),
        '_'
      )
    ) AS STRING),
    CAST(RAND() AS STRING)
  ) AS `row_key`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`