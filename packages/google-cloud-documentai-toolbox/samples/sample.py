"""Sample for using SDK"""

from typing import List

from google.cloud.document_ai_sdk import DocumentWrapper

GCS_PREFIX = "gcs_prefix"


def print_urls(gcs_prefix):
    merged_document = DocumentWrapper(gcs_prefix)

    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    for urls in merged_document.pages.search_pages(regex):
        print(urls)


def main() -> None:
    print_urls(GCS_PREFIX)


if __name__ == "__main__":
    main()
