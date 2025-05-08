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


def test_explicit_matrix_factorization(random_model_id: str) -> None:
    your_model_id = random_model_id

    # [START bigquery_dataframes_bqml_mf_explicit_create_dataset]
    import google.cloud.bigquery

    bqclient = google.cloud.bigquery.Client()
    bqclient.create_dataset("bqml_tutorial", exists_ok=True)
    # [END bigquery_dataframes_bqml_mf_explicit_create_dataset]

    # [START bigquery_dataframes_bqml_mf_explicit_upload_movielens]
    import io
    import zipfile

    import google.api_core.exceptions
    import requests

    try:
        # Check if you've already created the Movielens tables to avoid downloading
        # and uploading the dataset unnecessarily.
        bqclient.get_table("bqml_tutorial.ratings")
        bqclient.get_table("bqml_tutorial.movies")
    except google.api_core.exceptions.NotFound:
        # Download the https://grouplens.org/datasets/movielens/1m/ dataset.
        ml1m = requests.get("http://files.grouplens.org/datasets/movielens/ml-1m.zip")
        ml1m_file = io.BytesIO(ml1m.content)
        ml1m_zip = zipfile.ZipFile(ml1m_file)

        # Upload the ratings data into the ratings table.
        with ml1m_zip.open("ml-1m/ratings.dat") as ratings_file:
            ratings_content = ratings_file.read()

        ratings_csv = io.BytesIO(ratings_content.replace(b"::", b","))
        ratings_config = google.cloud.bigquery.LoadJobConfig()
        ratings_config.source_format = "CSV"
        ratings_config.write_disposition = "WRITE_TRUNCATE"
        ratings_config.schema = [
            google.cloud.bigquery.SchemaField("user_id", "INT64"),
            google.cloud.bigquery.SchemaField("item_id", "INT64"),
            google.cloud.bigquery.SchemaField("rating", "FLOAT64"),
            google.cloud.bigquery.SchemaField("timestamp", "TIMESTAMP"),
        ]
        bqclient.load_table_from_file(
            ratings_csv, "bqml_tutorial.ratings", job_config=ratings_config
        ).result()

        # Upload the movie data into the movies table.
        with ml1m_zip.open("ml-1m/movies.dat") as movies_file:
            movies_content = movies_file.read()

        movies_csv = io.BytesIO(movies_content.replace(b"::", b"@"))
        movies_config = google.cloud.bigquery.LoadJobConfig()
        movies_config.source_format = "CSV"
        movies_config.field_delimiter = "@"
        movies_config.write_disposition = "WRITE_TRUNCATE"
        movies_config.schema = [
            google.cloud.bigquery.SchemaField("movie_id", "INT64"),
            google.cloud.bigquery.SchemaField("movie_title", "STRING"),
            google.cloud.bigquery.SchemaField("genre", "STRING"),
        ]
        bqclient.load_table_from_file(
            movies_csv, "bqml_tutorial.movies", job_config=movies_config
        ).result()
    # [END bigquery_dataframes_bqml_mf_explicit_upload_movielens]

    # [START bigquery_dataframes_bqml_mf_explicit_create]
    from bigframes.ml import decomposition
    import bigframes.pandas as bpd

    # Load data from BigQuery
    bq_df = bpd.read_gbq(
        "bqml_tutorial.ratings", columns=("user_id", "item_id", "rating")
    )

    # Create the Matrix Factorization model
    model = decomposition.MatrixFactorization(
        num_factors=34,
        feedback_type="explicit",
        user_col="user_id",
        item_col="item_id",
        rating_col="rating",
        l2_reg=9.83,
    )
    model.fit(bq_df)
    model.to_gbq(
        your_model_id, replace=True  # For example: "bqml_tutorial.mf_explicit"
    )
    # [END bigquery_dataframes_bqml_mf_explicit_create]
    # [START bigquery_dataframes_bqml_mf_explicit_evaluate]
    # Evaluate the model using the score() function
    model.score(bq_df)
    # Output:
    # mean_absolute_error	mean_squared_error	mean_squared_log_error	median_absolute_error	r2_score	explained_variance
    # 0.485403	                0.395052	        0.025515	            0.390573	        0.68343	        0.68343
    # [END bigquery_dataframes_bqml_mf_explicit_evaluate]
    # [START bigquery_dataframes_bqml_mf_explicit_recommend_df]
    # Use predict() to get the predicted rating for each movie for 5 users
    subset = bq_df[["user_id"]].head(5)
    predicted = model.predict(subset)
    print(predicted)
    # Output:
    #   predicted_rating	user_id	 item_id	rating
    # 0	    4.206146	     4354	  968	     4.0
    # 1	    4.853099	     3622	  3521	     5.0
    # 2	    2.679067	     5543	  920	     2.0
    # 3	    4.323458	     445	  3175	     5.0
    # 4	    3.476911	     5535	  235	     4.0
    # [END bigquery_dataframes_bqml_mf_explicit_recommend_df]
    # [START bigquery_dataframes_bqml_mf_explicit_recommend_model]
    # import bigframes.bigquery as bbq

    # Load movies
    movies = bpd.read_gbq("bqml_tutorial.movies")

    # Merge the movies df with the previously created predicted df
    merged_df = bpd.merge(predicted, movies, left_on="item_id", right_on="movie_id")

    # Separate users and predicted data, setting the index to 'movie_id'
    users = merged_df[["user_id", "movie_id"]].set_index("movie_id")

    # Take the predicted data and sort it in descending order by 'predicted_rating', setting the index to 'movie_id'
    sort_data = (
        merged_df[["movie_title", "genre", "predicted_rating", "movie_id"]]
        .sort_values(by="predicted_rating", ascending=False)
        .set_index("movie_id")
    )

    # re-merge the separated dfs by index
    merged_user = sort_data.join(users, how="outer")

    # group the users and set the user_id as the index
    merged_user.groupby("user_id").head(5).set_index("user_id").sort_index()
    print(merged_user)
    # Output:
    # 	            movie_title	                genre	        predicted_rating
    # user_id
    #   1	    Saving Private Ryan (1998)	Action|Drama|War	    5.19326
    #   1	        Fargo (1996)	       Crime|Drama|Thriller	    4.996954
    #   1	    Driving Miss Daisy (1989)	    Drama	            4.983671
    #   1	        Ben-Hur (1959)	       Action|Adventure|Drama	4.877622
    #   1	     Schindler's List (1993)	   Drama|War	        4.802336
    #   2	    Saving Private Ryan (1998)	Action|Drama|War	    5.19326
    #   2	        Braveheart (1995)	    Action|Drama|War	    5.174145
    #   2	        Gladiator (2000)	      Action|Drama	        5.066372
    #   2	        On Golden Pond (1981)	     Drama	            5.01198
    #   2	    Driving Miss Daisy (1989)	     Drama	            4.983671
    # [END bigquery_dataframes_bqml_mf_explicit_recommend_model]
