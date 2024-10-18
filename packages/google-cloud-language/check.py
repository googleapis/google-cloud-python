# sync gRPC
from google.cloud import language_v2
client = language_v2.LanguageServiceClient()
text_content = 'Good Morning'
language_code = "en"
document = {
    "content": text_content,
    "type_": language_v2.Document.Type.PLAIN_TEXT,
    "language_code": language_code,
}
def custom_callback(response):
    print(f"something{response.trailing_metadata()}")
response = client.analyze_sentiment(
    request={"document": document, "encoding_type": language_v2.EncodingType.UTF8},
    raw_response_callback=custom_callback
)
print(response)

# async gRPC
import asyncio

from google.cloud import language_v2
async def test_language():
    client = language_v2.LanguageServiceAsyncClient()
    text_content = 'Good Morning'
    language_code = "en"
    document = {
        "content": text_content,
        "type_": language_v2.Document.Type.PLAIN_TEXT,
        "language_code": language_code,
    }
    async def custom_callback(response):
        trailing_metadata= await response.trailing_metadata()
        print(f"something{trailing_metadata}")

    response = await client.analyze_sentiment(
        request={"document": document, "encoding_type": language_v2.EncodingType.UTF8},
        raw_response_callback=custom_callback
    )
    print(response)

asyncio.run(test_language())

# sync REST
from google.cloud import language_v2
client = language_v2.LanguageServiceClient(transport="rest")
text_content = 'Good Morning'
language_code = "en"
document = {
    "content": text_content,
    "type_": language_v2.Document.Type.PLAIN_TEXT,
    "language_code": language_code,
}
def custom_callback(response):
    print(f"something{response.headers}")
response = client.analyze_sentiment(
    request={"document": document, "encoding_type": language_v2.EncodingType.UTF8},
    raw_response_callback=custom_callback,
)
print(response)
