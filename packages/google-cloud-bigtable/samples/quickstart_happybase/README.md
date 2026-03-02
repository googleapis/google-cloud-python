[//]: # "This README.md file is auto-generated, all changes to this file will be lost."
[//]: # "To regenerate it, use `python -m synthtool`."

## Python Samples for Cloud Bigtable

This directory contains samples for Cloud Bigtable, which may be used as a refererence for how to use this product. 
Samples, quickstarts, and other documentation are available at <a href="https://cloud.google.com/bigtable">cloud.google.com</a>.


### Quickstart using HappyBase

Demonstrates of Cloud Bigtable using HappyBase. This sample creates a Bigtable client, connects to an instance and then to a table, then closes the connection.


<a href="https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-bigtable&page=editor&open_in_editor=main.py"><img alt="Open in Cloud Shell" src="http://gstatic.com/cloudssh/images/open-btn.png"> 
</a>

To run this sample:

1. If this is your first time working with GCP products, you will need to set up [the Cloud SDK][cloud_sdk] or utilize [Google Cloud Shell][gcloud_shell]. This sample may [require authetication][authentication] and you will need to [enable billing][enable_billing].

1. Make a fork of this repo and clone the branch locally, then navigate to the sample directory you want to use.

1. Install the dependencies needed to run the samples.

        pip install -r requirements.txt

1. Run the sample using

        python main.py



<pre>usage: main.py [-h] [--table TABLE] project_id instance_id<br>usage: main.py [-h] [--table TABLE] project_id instance_id <br><br> <br>positional arguments: <br>&nbsp; project_id &nbsp; &nbsp; Your Cloud Platform project ID. <br>&nbsp; instance_id &nbsp; &nbsp;ID of the Cloud Bigtable instance to connect to. <br><br> <br>optional arguments: <br>&nbsp; -h, --help &nbsp; &nbsp; show this help message and exit <br>&nbsp; --table TABLE &nbsp;Existing table used in the quickstart. (default: my-table)</code

## Additional Information

You can read the documentation for more details on API usage and use GitHub
to <a href="https://github.com/googleapis/python-bigtable">browse the source</a> and [report issues][issues].

### Contributing
View the [contributing guidelines][contrib_guide], the [Python style guide][py_style] for more information.

[authentication]: https://cloud.google.com/docs/authentication/getting-started
[enable_billing]:https://cloud.google.com/apis/docs/getting-started#enabling_billing
[client_library_python]: https://googlecloudplatform.github.io/google-cloud-python/
[issues]: https://github.com/GoogleCloudPlatform/google-cloud-python/issues
[contrib_guide]: https://github.com/googleapis/google-cloud-python/blob/main/CONTRIBUTING.rst
[py_style]: http://google.github.io/styleguide/pyguide.html
[cloud_sdk]: https://cloud.google.com/sdk/docs
[gcloud_shell]: https://cloud.google.com/shell/docs
[gcloud_shell]: https://cloud.google.com/shell/docs
