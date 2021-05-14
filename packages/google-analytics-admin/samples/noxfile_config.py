TEST_CONFIG_OVERRIDE = {
    # You can opt out from the test for specific Python versions.
    "ignored_versions": ["2.7"],
    # Old samples are opted out of enforcing Python type hints
    # All new samples should feature them
    "enforce_type_hints": True,
    # An envvar key for determining the project id to use. Change it
    # to 'BUILD_SPECIFIC_GCLOUD_PROJECT' if you want to opt in using a
    # build specific Cloud project. You can also use your own string
    # to use your own Cloud project.
    "gcloud_project_env": "GOOGLE_CLOUD_PROJECT",
    # 'gcloud_project_env': 'BUILD_SPECIFIC_GCLOUD_PROJECT',
    # A dictionary you want to inject into your test. Don't put any
    # secrets here. These values will override predefined values.
    "envs": {
        "GA_TEST_PROPERTY_ID": "222596558",
        "GA_TEST_ACCOUNT_ID": "123",
        "GA_TEST_USER_LINK_ID": "123",
        "GA_TEST_ANDROID_APP_DATA_STREAM_ID": "123",
        "GA_TEST_IOS_APP_DATA_STREAM_ID": "123",
        "GA_TEST_WEB_DATA_STREAM_ID": "123",
    },
}
