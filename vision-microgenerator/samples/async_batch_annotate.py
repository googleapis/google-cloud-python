from google.cloud import vision_v1

import six


def sample_async_batch_annotate_images(input_image_uri, output_uri):
    """Perform async batch image annotation"""

    client = vision_v1.ImageAnnotator()

    # input_image_uri = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    # output_uri = 'gs://your-bucket/prefix/'

    if isinstance(input_image_uri, six.binary_type):
        input_image_uri = input_image_uri.decode("utf-8")
    if isinstance(output_uri, six.binary_type):
        output_uri = output_uri.decode("utf-8")
    source = {"image_uri": input_image_uri}
    image = {"source": source}
    type_ = vision_v1.Feature.Type.LABEL_DETECTION
    features_element = {"type": type_}
    type_2 = vision_v1.Feature.Type.IMAGE_PROPERTIES
    features_element_2 = {"type": type_2}
    features = [features_element, features_element_2]

    request_object = vision_v1.AnnotateImageRequest(image=image, features=features)

    # The max number of responses to output in each JSON file
    batch_size = 2
    gcs_destination = vision_v1.GcsDestination(uri=output_uri)
    output_config = vision_v1.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size
    )

    batch_request_object = vision_v1.AsyncBatchAnnotateImagesRequest(
        requests=[request_object], output_config=output_config
    )

    # Make the request
    operation = client.async_batch_annotate_images(batch_request_object)

    print("Waiting for operation to complete...")
    response = operation.result()

    # The output is written to GCS with the provided output_uri as prefix
    gcs_output_uri = response.output_config.gcs_destination.uri
    print("Output written to GCS with prefix: {}".format(gcs_output_uri))


### Existing Sample, for comparison purposes
# from google.cloud import vision_v1
# from google.cloud.vision_v1 import enums
# import six

# def sample_async_batch_annotate_images(input_image_uri, output_uri):
#   """Perform async batch image annotation"""

#   client = vision_v1.ImageAnnotatorClient()

#   # input_image_uri = 'gs://cloud-samples-data/vision/label/wakeupcat.jpg'
#   # output_uri = 'gs://your-bucket/prefix/'

#   if isinstance(input_image_uri, six.binary_type):
#     input_image_uri = input_image_uri.decode('utf-8')
#   if isinstance(output_uri, six.binary_type):
#     output_uri = output_uri.decode('utf-8')
#   source = {'image_uri': input_image_uri}
#   image = {'source': source}
#   type_ = enums.Feature.Type.LABEL_DETECTION
#   features_element = {'type': type_}
#   type_2 = enums.Feature.Type.IMAGE_PROPERTIES
#   features_element_2 = {'type': type_2}
#   features = [features_element, features_element_2]
#   requests_element = {'image': image, 'features': features}
#   requests = [requests_element]
#   gcs_destination = {'uri': output_uri}

#   # The max number of responses to output in each JSON file
#   batch_size = 2
#   output_config = {'gcs_destination': gcs_destination, 'batch_size': batch_size}

#   operation = client.async_batch_annotate_images(requests, output_config)

#   print('Waiting for operation to complete...')
#   response = operation.result()

#   # The output is written to GCS with the provided output_uri as prefix
#   gcs_output_uri = response.output_config.gcs_destination.uri
#   print('Output written to GCS with prefix: {}'.format(gcs_output_uri))