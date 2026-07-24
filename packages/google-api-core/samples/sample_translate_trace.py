import os

from google.cloud import translate_v3
from google.cloud.translate_v3.types import translation_service
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# 1. Setup OTel with Console Exporter
provider = TracerProvider()
exporter = ConsoleSpanExporter()
provider.add_span_processor(SimpleSpanProcessor(exporter))
trace.set_tracer_provider(provider)

# 2. Instantiate Client
# Using standard Application Default Credentials (ADC).
client = translate_v3.TranslationServiceClient()

# 3. Create Request
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "callovian")
parent = f"projects/{project_id}/locations/global"

request = translation_service.TranslateTextRequest(
    contents=["Hello, world!", "OpenTelemetry is braw!"],
    target_language_code="es",
    source_language_code="en",
    model=f"{parent}/models/general/nmt",
    mime_type="text/plain",
    parent=parent,
)

# 4. Call API
print("Sending translate request...")
try:
    response = client.translate_text(request)
    print("Translation Response received.")
    print(f"Translated text: {response.translations[0].translated_text}")
except Exception as e:
    print(f"API Call failed (expected if no real credentials): {e}")

print("Done. Check console output for traces.")
