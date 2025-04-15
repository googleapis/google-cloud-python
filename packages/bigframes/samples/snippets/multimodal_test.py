# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def test_multimodal_dataframe(gcs_dst_bucket: str) -> None:
    # destination folder must be in a GCS bucket that the BQ connection service account (default or user provided) has write access to.
    dst_bucket = gcs_dst_bucket
    # [START bigquery_dataframes_multimodal_dataframe_create]
    import bigframes

    # Flag to enable the feature
    bigframes.options.experiments.blob = True

    import bigframes.pandas as bpd

    # Create blob columns from wildcard path.
    df_image = bpd.from_glob_path(
        "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/*", name="image"
    )
    # Other ways are: from string uri column
    # df = bpd.DataFrame({"uri": ["gs://<my_bucket>/<my_file_0>", "gs://<my_bucket>/<my_file_1>"]})
    # df["blob_col"] = df["uri"].str.to_blob()

    # From an existing object table
    # df = bpd.read_gbq_object_table("<my_object_table>", name="blob_col")

    # Take only the 5 images to deal with. Preview the content of the Mutimodal DataFrame
    df_image = df_image.head(5)
    df_image
    # [END bigquery_dataframes_multimodal_dataframe_create]

    # [START bigquery_dataframes_multimodal_dataframe_merge]
    # Combine unstructured data with structured data
    df_image["author"] = ["alice", "bob", "bob", "alice", "bob"]  # type: ignore
    df_image["content_type"] = df_image["image"].blob.content_type()
    df_image["size"] = df_image["image"].blob.size()
    df_image["updated"] = df_image["image"].blob.updated()
    df_image

    # Filter images and display, you can also display audio and video types
    df_image[df_image["author"] == "alice"]["image"].blob.display()
    # [END bigquery_dataframes_multimodal_dataframe_merge]

    # [START bigquery_dataframes_multimodal_dataframe_image_transform]
    df_image["blurred"] = df_image["image"].blob.image_blur(
        (20, 20), dst=f"{dst_bucket}/image_blur_transformed/"
    )
    df_image["resized"] = df_image["image"].blob.image_resize(
        (300, 200), dst=f"{dst_bucket}/image_resize_transformed/"
    )
    df_image["normalized"] = df_image["image"].blob.image_normalize(
        alpha=50.0,
        beta=150.0,
        norm_type="minmax",
        dst=f"{dst_bucket}/image_normalize_transformed/",
    )

    # You can also chain functions together
    df_image["blur_resized"] = df_image["blurred"].blob.image_resize(
        (300, 200), dst=f"{dst_bucket}/image_blur_resize_transformed/"
    )
    df_image
    # [END bigquery_dataframes_multimodal_dataframe_image_transform]

    # [START bigquery_dataframes_multimodal_dataframe_ai]
    from bigframes.ml import llm

    gemini = llm.GeminiTextGenerator(model_name="gemini-1.5-flash-002")

    # Deal with first 2 images as example
    df_image = df_image.head(2)

    # Ask the same question on the images
    df_image = df_image.head(2)
    answer = gemini.predict(df_image, prompt=["what item is it?", df_image["image"]])
    answer[["ml_generate_text_llm_result", "image"]]

    # Ask different questions
    df_image["question"] = [  # type: ignore
        "what item is it?",
        "what color is the picture?",
    ]
    answer_alt = gemini.predict(
        df_image, prompt=[df_image["question"], df_image["image"]]
    )
    answer_alt[["ml_generate_text_llm_result", "image"]]

    # Generate embeddings on images
    embed_model = llm.MultimodalEmbeddingGenerator()
    embeddings = embed_model.predict(df_image["image"])
    embeddings
    # [END bigquery_dataframes_multimodal_dataframe_ai]

    # [START bigquery_dataframes_multimodal_dataframe_pdf_chunk]
    # PDF chunking
    df_pdf = bpd.from_glob_path(
        "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/documents/*", name="pdf"
    )
    df_pdf["chunked"] = df_pdf["pdf"].blob.pdf_chunk()
    chunked = df_pdf["chunked"].explode()
    chunked
    # [END bigquery_dataframes_multimodal_dataframe_pdf_chunk]
    assert df_image is not None
    assert answer is not None
    assert answer_alt is not None
    assert embeddings is not None
    assert chunked is not None
