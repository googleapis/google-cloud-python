WITH `bfcte_0` AS (
  SELECT
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    LPAD(`string_col`, GREATEST(LENGTH(`string_col`), 10), '-') AS `bfcol_1`,
    RPAD(`string_col`, GREATEST(LENGTH(`string_col`), 10), '-') AS `bfcol_2`,
    RPAD(
      LPAD(
        `string_col`,
        CAST(FLOOR(SAFE_DIVIDE(GREATEST(LENGTH(`string_col`), 10) - LENGTH(`string_col`), 2)) AS INT64) + LENGTH(`string_col`),
        '-'
      ),
      GREATEST(LENGTH(`string_col`), 10),
      '-'
    ) AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `left`,
  `bfcol_2` AS `right`,
  `bfcol_3` AS `both`
FROM `bfcte_1`