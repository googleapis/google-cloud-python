# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (t
# you may not use this file except in compliance wi
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in
# distributed under the License is distributed on a
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, eit
# See the License for the specific language governi
# limitations under the License.


def test_create_single_timeseries() -> None:
    # [START bigquery_dataframes_single_timeseries_forecasting_model_tutorial]
    import bigframes.pandas as bpd

    # Start by loading the historical data from BigQuerythat you want to analyze and forecast.
    # This clause indicates that you are querying the ga_sessions_* tables in the google_analytics_sample dataset.
    # Read and visualize the time series you want to forecast.
    df = bpd.read_gbq("bigquery-public-data.google_analytics_sample.ga_sessions_*")
    parsed_date = bpd.to_datetime(df.date, format="%Y%m%d", utc=True)
    parsed_date.name = "parsed_date"
    visits = df["totals"].struct.field("visits")
    visits.name = "total_visits"
    total_visits = visits.groupby(parsed_date).sum()

    # Expected output: total_visits.head()
    # parsed_date
    # 2016-08-01 00:00:00+00:00    1711
    # 2016-08-02 00:00:00+00:00    2140
    # 2016-08-03 00:00:00+00:00    2890
    # 2016-08-04 00:00:00+00:00    3161
    # 2016-08-05 00:00:00+00:00    2702
    # Name: total_visits, dtype: Int64

    total_visits.plot.line()

    # [END bigquery_dataframes_single_timeseries_forecasting_model_tutorial]

    # [START bigquery_dataframes_single_timeseries_forecasting_model_tutorial_create]
    from bigframes.ml import forecasting
    import bigframes.pandas as bpd

    # Create a time series model to forecast total site visits:
    # The auto_arima option defaults to True, so the auto.ARIMA algorithm automatically
    # tunes the hyperparameters in the model.
    # The data_frequency option defaults to 'auto_frequency so the training
    # process automatically infers the data frequency of the input time series.
    # The decompose_time_series option defaults to True, so that information about
    # the time series data is returned when you evaluate the model in the next step.
    model = forecasting.ARIMAPlus()
    model.auto_arima = True
    model.data_frequency = "auto_frequency"
    model.decompose_time_series = True

    # Use the data loaded in the previous step to fit the model
    training_data = total_visits.to_frame().reset_index(drop=False)

    X = training_data[["parsed_date"]]
    y = training_data[["total_visits"]]

    model.fit(X, y)
    # [END bigquery_dataframes_single_timeseries_forecasting_model_tutorial_create]

    # [START bigquery_dataframes_single_timeseries_forecasting_model_tutorial_coef]
    coef = model.coef_
    print(coef.peek())

    # Expected output:
    #       ar_coefficients   ma_coefficients   intercept_or_drift
    #   0	 [0.40944762]	   [-0.81168198]	      0.0
    # [END bigquery_dataframes_single_timeseries_forecasting_model_tutorial_coef]

    # [START bigquery_dataframes_single_timeseries_forecasting_model_tutorial_evaluate]
    # Evaluate the time series models by using the summary() function. The summary()
    # function shows you the evaluation metrics of all the candidate models evaluated
    # during the process of automatic hyperparameter tuning.
    summary = model.summary(
        show_all_candidate_models=True,
    )
    print(summary.peek())

    # Expected output:
    # row   non_seasonal_p	non_seasonal_d	non_seasonal_q	has_drift	log_likelihood	AIC	variance	seasonal_periods	has_holiday_effect	has_spikes_and_dips	has_step_changes	error_message
    #  0	      0	              1	               3	      True	     -2464.255656	4938.511313	     42772.506055	        ['WEEKLY']	            False	        False	            True
    #  1	      2	              1	               0	      False	     -2473.141651	4952.283303	     44942.416463	        ['WEEKLY']	            False	        False	            True
    #  2	      1	              1	               0 	      False	     -2479.880885	4963.76177	     46642.953433	        ['WEEKLY']	            False	        False	            True
    #  3	      0	              1	               1	      False	     -2470.632377	4945.264753	     44319.379307	        ['WEEKLY']	            False	        False	            True
    #  4	      2	              1	               1	      True	     -2463.671247	4937.342493	     42633.299513	        ['WEEKLY']	            False	        False	            True
    # [END bigquery_dataframes_single_timeseries_forecasting_model_tutorial_evaluate]

    # [START bigquery_dataframes_single_timeseries_forecasting_model_tutorial_forecast]
    prediction = model.predict(horizon=30, confidence_level=0.8)

    print(prediction.peek())
    # Expected output:
    #           forecast_timestamp	   forecast_value	standard_error	confidence_level	prediction_interval_lower_bound	    prediction_interval_upper_bound	    confidence_interval_lower_bound	    confidence_interval_upper_bound
    # 11	2017-08-13 00:00:00+00:00	1845.439732	      328.060405	      0.8	                 1424.772257	                      2266.107208	                     1424.772257	                     2266.107208
    # 29	2017-08-31 00:00:00+00:00	2615.993932	      431.286628	      0.8	                 2062.960849	                      3169.027015	                     2062.960849	                     3169.027015
    # 7	    2017-08-09 00:00:00+00:00	2639.285993	      300.301186	      0.8	                 2254.213792	                      3024.358193	                     2254.213792	                     3024.358193
    # 25	2017-08-27 00:00:00+00:00	1853.735689	      410.596551	      0.8	                 1327.233216	                      2380.238162	                     1327.233216	                     2380.238162
    # 1	    2017-08-03 00:00:00+00:00	2621.33159	      241.093355	      0.8	                 2312.180802	                      2930.482379	                     2312.180802	                     2930.482379
    # [END bigquery_dataframes_single_timeseries_forecasting_model_tutorial_forecast]

    # [START bigquery_dataframes_single_timeseries_forecasting_model_tutorial_explain_forecast]
    ex_pred = model.predict_explain(horizon=30, confidence_level=0.8)

    print(ex_pred.head(4))
    # Expected output:
    #       time_series_timestamp	  time_series_type	    time_series_data	time_series_adjusted_data	 standard_error	   confidence_level	   prediction_interval_lower_bound	   prediction_interval_upper_bound	  trend	   seasonal_period_yearly	  seasonal_period_quarterly	    seasonal_period_monthly	   seasonal_period_weekly	  seasonal_period_daily	    holiday_effect	   spikes_and_dips	   step_changes	   residual
    # 0	  2016-08-01 00:00:00+00:00	      history	             1711.0	               505.716474	           206.939556	         <NA>	                    <NA>	                            <NA>	               0.0	           <NA>	                        <NA>	                     <NA>	                 169.611938	                  <NA>	                <NA>	            <NA>	       1205.283526	   336.104536
    # 1	  2016-08-02 00:00:00+00:00	      history	             2140.0	               623.137701	           206.939556	         <NA>	                    <NA>	                            <NA>	            336.104428	       <NA>	                        <NA>	                     <NA>	                 287.033273	                  <NA>	                <NA>	            <NA>	       1205.283526	   311.578773
    # 2	  2016-08-03 00:00:00+00:00	      history	             2890.0	               1008.655091	           206.939556	         <NA>	                    <NA>	                            <NA>	            563.514213	       <NA>	                        <NA>	                     <NA>	                 445.140878	                  <NA>	                <NA>	            <NA>	       1205.283526	   676.061383
    # 3	  2016-08-04 00:00:00+00:00	      history	             3161.0	               1389.40959	           206.939556	         <NA>	                    <NA>	                            <NA>	            986.317236	       <NA>	                        <NA>	                     <NA>	                 403.092354	                  <NA>	                <NA>	            <NA>	       1205.283526	   566.306884
    # 4	  2016-08-05 00:00:00+00:00	      history	             2702.0	               1394.395741	           206.939556	         <NA>	                    <NA>	                            <NA>	            1248.707386	       <NA>	                        <NA>	                     <NA>	                 145.688355	                  <NA>	                <NA>	            <NA>	       1205.283526	   102.320733
    # 5	  2016-08-06 00:00:00+00:00	      history	             1663.0	               437.09243	           206.939556	         <NA>	                    <NA>	                            <NA>	            1188.59004	       <NA>	                        <NA>	                     <NA>	                 -751.49761	                  <NA>	                <NA>	            <NA>	       1205.283526	    20.624044
    # [END bigquery_dataframes_single_timeseries_forecasting_model_tutorial_explain_forecast]
    assert coef is not None
    assert ex_pred is not None
    assert summary is not None
    assert model is not None
    assert parsed_date is not None
    assert prediction is not None
    assert total_visits is not None
