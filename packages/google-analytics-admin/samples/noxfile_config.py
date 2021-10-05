TEST_CONFIG_OVERRIDE = {
    # An envvar key for determining the project id to use. Change it
    # to 'BUILD_SPECIFIC_GCLOUD_PROJECT' if you want to opt in using a
    # build specific Cloud project. You can also use your own string
    # to use your own Cloud project.
    "gcloud_project_env": "BUILD_SPECIFIC_GCLOUD_PROJECT",
    # 'gcloud_project_env': 'BUILD_SPECIFIC_GCLOUD_PROJECT',
    # A dictionary you want to inject into your test. Don't put any
    # secrets here. These values will override predefined values.
    "envs": {
        "GA_TEST_PROPERTY_ID": "276206997",
        "GA_TEST_ACCOUNT_ID": "199820965",
        "GA_TEST_USER_LINK_ID": "103401743041912607932",
        "GA_TEST_PROPERTY_USER_LINK_ID": "105231969274497648555",
        "GA_TEST_ANDROID_APP_DATA_STREAM_ID": "2828100949",
        "GA_TEST_IOS_APP_DATA_STREAM_ID": "2828089289",
        "GA_TEST_WEB_DATA_STREAM_ID": "2828068992",
    },
}
