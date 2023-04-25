from google.maps import mapsplatformdatasets_v1alpha

async def sample_create_dataset():
    # Create a client
    client = mapsplatformdatasets_v1alpha.MapsPlatformDatasetsV1AlphaAsyncClient()
    
    project_id = "<cloud project name or unique number>"

    # Initialize request argument(s)
    request = mapsplatformdatasets_v1alpha.CreateDatasetRequest(
        parent = project_id,
    )

    # Make the request
    response = await client.create_dataset(request=request)

    # Handle the response
    print(response)
