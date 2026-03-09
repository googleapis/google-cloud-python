CREATE MODEL `my_arima_model`
OPTIONS(model_type = 'ARIMA_PLUS')
AS (
  training_data AS (SELECT * FROM sales), custom_holiday AS (SELECT * FROM holidays)
)