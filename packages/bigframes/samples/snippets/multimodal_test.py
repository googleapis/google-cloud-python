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


def test_multimodal_dataframe(gcs_bucket_snippets: str) -> None:
    # destination folder must be in a GCS bucket that the BQ connection service account (default or user provided) has write access to.
    dst_bucket = f"gs://{gcs_bucket_snippets}"
    # [START bigquery_dataframes_multimodal_dataframe_create]
    import bigframes

    # Flags to control preview image/video preview size
    bigframes.options.display.blob_display_width = 300

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
    # [END bigquery_dataframes_multimodal_dataframe_merge]

    # [START bigquery_dataframes_multimodal_dataframe_filter]
    # Filter images and display, you can also display audio and video types. Use width/height parameters to constrain window sizes.
    df_image[df_image["author"] == "alice"]["image"].blob.display()
    # [END bigquery_dataframes_multimodal_dataframe_filter]

    # [START bigquery_dataframes_multimodal_dataframe_image_transform]
    df_image["blurred"] = df_image["image"].blob.image_blur(
        (20, 20), dst=f"{dst_bucket}/image_blur_transformed/", engine="opencv"
    )
    df_image["resized"] = df_image["image"].blob.image_resize(
        (300, 200), dst=f"{dst_bucket}/image_resize_transformed/", engine="opencv"
    )
    df_image["normalized"] = df_image["image"].blob.image_normalize(
        alpha=50.0,
        beta=150.0,
        norm_type="minmax",
        dst=f"{dst_bucket}/image_normalize_transformed/",
        engine="opencv",
    )

    # You can also chain functions together
    df_image["blur_resized"] = df_image["blurred"].blob.image_resize(
        (300, 200), dst=f"{dst_bucket}/image_blur_resize_transformed/", engine="opencv"
    )
    df_image
    # [END bigquery_dataframes_multimodal_dataframe_image_transform]

    # [START bigquery_dataframes_multimodal_dataframe_ml_text]
    from bigframes.ml import llm

    gemini = llm.GeminiTextGenerator(model_name="gemini-2.0-flash-001")

    # Deal with first 2 images as example
    df_image = df_image.head(2)

    # Ask the same question on the images
    df_image = df_image.head(2)
    answer = gemini.predict(df_image, prompt=["what item is it?", df_image["image"]])
    answer[["ml_generate_text_llm_result", "image"]]
    # [END bigquery_dataframes_multimodal_dataframe_ml_text]

    # [START bigquery_dataframes_multimodal_dataframe_ml_text_alt]
    # Ask different questions
    df_image["question"] = [  # type: ignore
        "what item is it?",
        "what color is the picture?",
    ]
    answer_alt = gemini.predict(
        df_image, prompt=[df_image["question"], df_image["image"]]
    )
    answer_alt[["ml_generate_text_llm_result", "image"]]
    # [END bigquery_dataframes_multimodal_dataframe_ml_text_alt]

    # [START bigquery_dataframes_multimodal_dataframe_ml_embed]
    # Generate embeddings on images
    embed_model = llm.MultimodalEmbeddingGenerator()
    embeddings = embed_model.predict(df_image["image"])
    embeddings
    # [END bigquery_dataframes_multimodal_dataframe_ml_embed]

    # [START bigquery_dataframes_multimodal_dataframe_pdf_chunk]
    # PDF chunking
    df_pdf = bpd.from_glob_path(
        "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/documents/*", name="pdf"
    )
    df_pdf["chunked"] = df_pdf["pdf"].blob.pdf_chunk(engine="pypdf")
    chunked = df_pdf["chunked"].explode()
    chunked
    # [END bigquery_dataframes_multimodal_dataframe_pdf_chunk]
    assert df_image is not None
    assert answer is not None
    assert answer_alt is not None
    assert embeddings is not None
    assert chunked is not None


def test_multimodal_example(gcs_bucket_snippets: str) -> None:
    BUCKET = gcs_bucket_snippets
    # [START bigquery_dataframes_multimodal_load]
    import bigframes.bigquery as bbq
    import bigframes.pandas as bpd

    bbq.load_data(
        "cymbal_pets.products",
        write_disposition="OVERWRITE",
        from_files_options={
            "format": "avro",
            "uris": [
                "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/tables/products/products_*.avro"
            ],
        },
    )
    # [END bigquery_dataframes_multimodal_load]

    # [START bigquery_dataframes_multimodal_create_images]
    bbq.create_external_table(
        "cymbal_pets.product_images",
        replace=True,
        connection_name="us.cymbal_conn",
        options={
            "object_metadata": "SIMPLE",
            "uris": [
                "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/*.png"
            ],
        },
    )
    # [END bigquery_dataframes_multimodal_create_images]

    # [START bigquery_dataframes_multimodal_create_manuals]
    bbq.create_external_table(
        "cymbal_pets.product_manuals",
        replace=True,
        connection_name="us.cymbal_conn",
        options={
            "object_metadata": "SIMPLE",
            "uris": [
                "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/documents/*.pdf"
            ],
        },
    )
    # [END bigquery_dataframes_multimodal_create_manuals]

    # [START bigquery_dataframes_multimodal_create_gemini]
    gemini_model = bbq.ml.create_model(
        "cymbal_pets.gemini",
        replace=True,
        connection_name="us.cymbal_conn",
        options={"endpoint": "gemini-2.5-flash"},
    )
    # [END bigquery_dataframes_multimodal_create_gemini]

    # [START bigquery_dataframes_multimodal_create_embedding]
    embedding_model = bbq.ml.create_model(
        "cymbal_pets.embedding_model",
        replace=True,
        connection_name="us.cymbal_conn",
        options={"endpoint": "multimodalembedding@001"},
    )
    # [END bigquery_dataframes_multimodal_create_embedding]

    # [START bigquery_dataframes_multimodal_create_df_products_mm]
    df_images = bpd.read_gbq("SELECT * FROM cymbal_pets.product_images")
    df_products = bpd.read_gbq("cymbal_pets.products")

    df_products_mm = df_images.merge(df_products, on="uri").drop(columns="uri")
    df_products_mm = df_products_mm.rename(columns={"ref": "image"})
    # [END bigquery_dataframes_multimodal_create_df_products_mm]

    # [START bigquery_dataframes_multimodal_show_df_products_mm]
    df_products_mm[["product_name", "image"]]
    # [END bigquery_dataframes_multimodal_show_df_products_mm]

    # [START bigquery_dataframes_multimodal_image_description]
    df_products_mm["url"] = bbq.obj.get_access_url(
        df_products_mm["image"], "R"
    ).to_frame()
    df_products_mm["prompt0"] = "Can you describe the following image?"

    df_products_mm["prompt"] = bbq.struct(df_products_mm[["prompt0", "url"]])
    df_products_mm = bbq.ai.generate_table(
        gemini_model, df_products_mm, output_schema={"image_description": "STRING"}
    )

    df_products_mm = df_products_mm[
        [
            "product_id",
            "product_name",
            "brand",
            "category",
            "subcategory",
            "animal_type",
            "search_keywords",
            "price",
            "description",
            "inventory_level",
            "supplier_id",
            "average_rating",
            "image",
            "image_description",
        ]
    ]
    # [END bigquery_dataframes_multimodal_image_description]

    # [START bigquery_dataframes_multimodal_generate_animal_type]
    df_prompt = bbq.obj.get_access_url(df_products_mm["image"], "R").to_frame()
    df_prompt[
        "prompt0"
    ] = "For the image of a pet product, concisely generate the following metadata: 1) animal_type and 2) 5 SEO search keywords, and 3) product subcategory."

    df_products_mm["prompt"] = bbq.struct(df_prompt[["prompt0", "image"]])

    df_products_mm = df_products_mm.drop(
        columns=["animal_type", "search_keywords", "subcategory"]
    )
    df_products_mm = bbq.ai.generate_table(
        gemini_model,
        df_products_mm,
        output_schema="animal_type STRING, search_keywords ARRAY<STRING>, subcategory STRING",
    )
    # [END bigquery_dataframes_multimodal_generate_animal_type]

    # [START bigquery_dataframes_multimodal_show_animal_type]
    df_products_mm[
        [
            "product_name",
            "image_description",
            "animal_type",
            "search_keywords",
            "subcategory",
        ]
    ]
    # [END bigquery_dataframes_multimodal_show_animal_type]

    # [START bigquery_dataframes_multimodal_brand_description]
    df_agg = df_products_mm[
        ["image", "description", "category", "subcategory", "brand"]
    ]
    df_agg["image"] = bbq.obj.get_access_url(df_products_mm["image"], "R")
    df_agg = bbq.array_agg(df_agg.groupby(by=["brand"]))

    df_agg["cnt"] = bbq.array_length(df_agg["image"])

    df_prompt = df_agg[["image", "description", "category", "subcategory"]]
    df_prompt[
        "prompt0"
    ] = "Use the images and text to give one concise brand description for a website brand page. Return the description only. "

    df_agg["prompt"] = bbq.struct(
        df_prompt[["prompt0", "image", "description", "category", "subcategory"]]
    )

    df_agg = df_agg.reset_index()

    df_agg = bbq.ai.generate_table(
        gemini_model, df_agg, output_schema={"brand_description": "STRING"}
    )
    df_agg[["brand", "brand_description", "cnt"]]
    # [END bigquery_dataframes_multimodal_brand_description]

    # [START bigquery_dataframes_multimodal_define_to_grayscale]
    @bpd.udf(
        dataset="cymbal_pets",
        name="to_grayscale",
        packages=["numpy", "opencv-python"],
        bigquery_connection="us.cymbal_conn",
        max_batching_rows=1,
    )
    def to_grayscale(src_ref: str, dst_ref: str) -> str:
        import json
        from urllib.request import Request, urlopen

        import cv2 as cv
        import numpy as np

        src_json = json.loads(src_ref)
        srcUrl = src_json["access_urls"]["read_url"]

        dst_json = json.loads(dst_ref)
        dstUrl = dst_json["access_urls"]["write_url"]

        req = urlopen(srcUrl)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv.imdecode(arr, -1)  # 'Load it as it is'

        # Convert the image to grayscale
        gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Send POST request to the URL
        _, img_encoded = cv.imencode(".png", gray_image)

        req = Request(
            url=dstUrl,
            data=img_encoded.tobytes(),
            method="PUT",
            headers={
                "Content-Type": "image/png",
            },
        )
        with urlopen(req):
            pass
        return dst_ref

    # [END bigquery_dataframes_multimodal_define_to_grayscale]

    # [START bigquery_dataframes_multimodal_apply_to_grayscale]
    df_grayscale = df_products_mm[["product_id", "product_name", "image"]]
    df_grayscale[
        "gray_image_uri"
    ] = f"gs://{BUCKET}/cymbal-pets-images/grayscale/" + df_grayscale[
        "image"
    ].struct.field(
        "uri"
    ).str.extract(
        r"([^/]+)$"
    )

    df_grayscale["gray_image"] = bbq.obj.make_ref(
        df_grayscale["gray_image_uri"], "us.cymbal_conn"
    )

    df_grayscale["image_url"] = bbq.to_json_string(
        bbq.obj.get_access_url(df_grayscale["image"], "r")
    )
    df_grayscale["gray_image_url"] = bbq.to_json_string(
        bbq.obj.get_access_url(df_grayscale["gray_image"], "rw")
    )

    df_grayscale[["image_url", "gray_image_url"]].apply(to_grayscale, axis=1)
    # [END bigquery_dataframes_multimodal_apply_to_grayscale]

    # [START bigquery_dataframes_multimodal_define_chunk_pdf]
    @bpd.udf(
        dataset="cymbal_pets",
        name="chunk_pdf",
        packages=["pypdf"],
        bigquery_connection="us.cymbal_conn",
        max_batching_rows=1,
    )
    def chunk_pdf(src_ref: str, chunk_size: int, overlap_size: int) -> list[str]:
        import io
        import json
        from urllib.request import urlopen

        from pypdf import PdfReader  # type: ignore

        src_json = json.loads(src_ref)
        srcUrl = src_json["access_urls"]["read_url"]

        req = urlopen(srcUrl)
        pdf_file = io.BytesIO(bytearray(req.read()))
        reader = PdfReader(pdf_file, strict=False)

        # extract and chunk text simultaneously
        all_text_chunks = []
        curr_chunk = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                curr_chunk += page_text
                # split the accumulated text into chunks of a specific size with overlaop
                # this loop implements a sliding window approach to create chunks
                while len(curr_chunk) >= chunk_size:
                    split_idx = curr_chunk.rfind(" ", 0, chunk_size)
                    if split_idx == -1:
                        split_idx = chunk_size
                    actual_chunk = curr_chunk[:split_idx]
                    all_text_chunks.append(actual_chunk)
                    overlap = curr_chunk[split_idx + 1 : split_idx + 1 + overlap_size]
                    curr_chunk = overlap + curr_chunk[split_idx + 1 + overlap_size :]
        if curr_chunk:
            all_text_chunks.append(curr_chunk)

        return all_text_chunks

    # [END bigquery_dataframes_multimodal_define_chunk_pdf]

    # [START bigquery_dataframes_multimodal_apply_chunk_pdf]
    df_manuals = bpd.read_gbq("SELECT * FROM cymbal_pets.product_manuals")
    df_manuals["url"] = bbq.to_json_string(
        bbq.obj.get_access_url(df_manuals["ref"], "R")
    )

    df_manuals["chunk_size"] = 1000
    df_manuals["overlap_size"] = 100

    df_manuals["chunked"] = df_manuals[["url", "chunk_size", "overlap_size"]].apply(
        chunk_pdf, axis=1
    )
    # [END bigquery_dataframes_multimodal_apply_chunk_pdf]

    # [START bigquery_dataframes_multimodal_analyze_pdf]
    df_chunked = df_manuals["chunked"].explode().to_frame()
    df_chunked[
        "prompt0"
    ] = "Can you summarize the product manual as bullet points? Highlight the legal clauses"

    df_chunked["prompt"] = bbq.struct(df_chunked[["prompt0", "chunked"]])

    result = bbq.ai.generate_text(gemini_model, df_chunked["prompt"])
    result
    # [END bigquery_dataframes_multimodal_analyze_pdf]

    # [START bigquery_dataframes_multimodal_create_embed_table]
    df_products_mm["content"] = bbq.obj.get_access_url(df_products_mm["image"], "R")
    df_embed = bbq.ai.generate_embedding(
        embedding_model, df_products_mm[["content", "product_id"]]
    )

    df_embed.to_gbq("cymbal_pets.products_embedding", if_exists="replace")
    # [END bigquery_dataframes_multimodal_create_embed_table]

    # [START bigquery_dataframes_multimodal_vector_search]
    df_image = bpd.DataFrame(
        {
            "uri": [
                "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/cozy-naps-cat-scratching-post-with-condo.png"
            ]
        }
    ).cache()
    df_image["image"] = bbq.obj.make_ref(df_image["uri"], "us.cymbal_conn")
    df_search = bbq.ai.generate_embedding(
        embedding_model,
        bbq.obj.get_access_url(bbq.obj.fetch_metadata(df_image["image"]), "R"),
    )

    search_result = bbq.vector_search(
        "cymbal_pets.products_embedding", "embedding", df_search["embedding"]
    )
    search_result
    # [END bigquery_dataframes_multimodal_vector_search]

    # [START bigquery_dataframes_create_external_table_all]
    bbq.create_external_table(
        "cymbal_pets.product_manuals_all",
        replace=True,
        connection_name="us.cymbal_conn",
        options={
            "object_metadata": "SIMPLE",
            "uris": [
                "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/documents/*.pdf",
                "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/document_chunks/*.pdf",
            ],
        },
    )
    # [END bigquery_dataframes_create_external_table_all]

    # [START bigquery_dataframes_create_manual_to_chunks]
    df1 = bpd.read_gbq("SELECT * FROM cymbal_pets.product_manuals_all").sort_values(
        "uri"
    )
    df2 = df1.copy()
    df1["name"] = df1["uri"].str.extract(r".*/([^.]*).[^/]+")
    df2["name"] = df2["uri"].str.extract(r".*/([^.]*)_page[0-9]+.[^/]+")
    df_manuals_all = df1.merge(df2, on="name")
    df_manuals_agg = (
        bbq.array_agg(df_manuals_all[["ref_x", "uri_x"]].groupby("uri_x"))["ref_x"]
        .str[0]
        .to_frame()
    )
    df_manuals_agg["chunks"] = bbq.array_agg(
        df_manuals_all[["ref_y", "uri_x"]].groupby("uri_x")
    )["ref_y"]
    # [END bigquery_dataframes_create_manual_to_chunks]

    # [START bigquery_dataframes_show_manual_to_chunks]
    df_manuals_agg
    # [END bigquery_dataframes_show_manual_to_chunks]

    # [START bigquery_dataframes_generate_pages_summary]
    df_manuals_agg["chunks_url"] = bbq.array_agg(
        bbq.obj.get_access_url(df_manuals_agg.explode("chunks")["chunks"], "R").groupby(
            "uri_x"
        )
    )
    df_manuals_agg[
        "prompt0"
    ] = "Can you provide a page by page summary for the first 3 pages of the attached manual? Only write one line for each page. The pages are provided in serial order"
    df_manuals_agg["prompt"] = bbq.struct(df_manuals_agg[["prompt0", "chunks_url"]])

    result = bbq.ai.generate_text(gemini_model, df_manuals_agg["prompt"])["result"]
    result
    # [END bigquery_dataframes_generate_pages_summary]

    # [START bigquery_dataframes_generate_each_page_summary]
    result = bbq.ai.generate_table(
        gemini_model,
        df_manuals_agg["prompt"],
        output_schema={
            "page1_summary": "STRING",
            "page2_summary": "STRING",
            "page3_summary": "STRING",
        },
    )[["page1_summary", "page2_summary", "page3_summary"]]
    result
    # [END bigquery_dataframes_generate_each_page_summary]
