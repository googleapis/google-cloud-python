import os

from google.cloud import translate_v3
from google.cloud.translate_v3.types import translation_service

# 🚀 1. ACTIVATE MONKEY PATCHING (Auto-Instrumentation)
# This reaches into the gRPC library and wraps standard functions dynamically.
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient

GrpcInstrumentorClient().instrument()
print("✅ gRPC Client Auto-Instrumentation activated!")

# 2. Standard OTel SDK Setup (Same as before, so we can see the console output)
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

print("Initializing TracerProvider...")
provider = TracerProvider()
exporter = ConsoleSpanExporter()
provider.add_span_processor(SimpleSpanProcessor(exporter))
trace.set_tracer_provider(provider)
print("TracerProvider initialized.")

# 3. Instantiate Client (Standard GAPIC, NO manual instrumentation used here)
print("Instantiating TranslationServiceClient...")
client = translate_v3.TranslationServiceClient()
print("TranslationServiceClient instantiated.")

# 4. Create Request
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

# 5. Call API
print("Sending translate request...")
try:
    response = client.translate_text(request)
    print("Translation Response received.")
    print(f"Translated text: {response.translations[0].translated_text}")
except Exception as e:
    print(f"API Call failed: {e}")

print("Done. Check console output for traces.")
