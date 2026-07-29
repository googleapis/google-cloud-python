CREATE EXTERNAL TABLE IF NOT EXISTS `my-project.my_dataset.my_table` (
  `col1` INT64
) OPTIONS (
  format='CSV',
  uris=['gs://bucket/path*']
)