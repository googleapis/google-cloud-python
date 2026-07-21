[//]: # "This README.md file is auto-generated, all changes to this file will be lost."
[//]: # "To regenerate it, use `python -m synthtool`."

## Python Samples for Cloud Bigtable

This directory contains samples for Cloud Bigtable, which may be used as a refererence for how to use this product. 
Samples, quickstarts, and other documentation are available at <a href="https://cloud.google.com/bigtable">cloud.google.com</a>.


### Metric Scaler

This sample demonstrates how to use Stackdriver Monitoring to scale Cloud Bigtable based on CPU usage.


<a href="https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-bigtable&page=editor&open_in_editor=metricscaler.py"><img alt="Open in Cloud Shell" src="http://gstatic.com/cloudssh/images/open-btn.png"> 
</a>

To run this sample:

1. If this is your first time working with GCP products, you will need to set up [the Cloud SDK][cloud_sdk] or utilize [Google Cloud Shell][gcloud_shell]. This sample may [require authetication][authentication] and you will need to [enable billing][enable_billing].

1. Make a fork of this repo and clone the branch locally, then navigate to the sample directory you want to use.

1. Install the dependencies needed to run the samples.

        pip install -r requirements.txt

1. Run the sample using

        python metricscaler.py



<pre>usage: metricscaler.py [-h] [--high_cpu_threshold HIGH_CPU_THRESHOLD] [--low_cpu_threshold LOW_CPU_THRESHOLD] [--short_sleep SHORT_SLEEP] [--long_sleep LONG_SLEEP] bigtable_instance bigtable_cluster<br>usage: metricscaler.py [-h] [--high_cpu_threshold HIGH_CPU_THRESHOLD] <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;[--low_cpu_threshold LOW_CPU_THRESHOLD] <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;[--short_sleep SHORT_SLEEP] [--long_sleep LONG_SLEEP] <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;bigtable_instance bigtable_cluster <br><br> <br>Scales Cloud Bigtable clusters based on CPU usage. <br><br> <br>positional arguments: <br>&nbsp; bigtable_instance &nbsp; &nbsp; ID of the Cloud Bigtable instance to connect to. <br>&nbsp; bigtable_cluster &nbsp; &nbsp; &nbsp;ID of the Cloud Bigtable cluster to connect to. <br><br> <br>optional arguments: <br>&nbsp; -h, --help &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;show this help message and exit <br>&nbsp; --high_cpu_threshold HIGH_CPU_THRESHOLD <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; If Cloud Bigtable CPU usage is above this threshold, <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; scale up <br>&nbsp; --low_cpu_threshold LOW_CPU_THRESHOLD <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; If Cloud Bigtable CPU usage is below this threshold, <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; scale down <br>&nbsp; --short_sleep SHORT_SLEEP <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; How long to sleep in seconds between checking metrics <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; after no scale operation <br>&nbsp; --long_sleep LONG_SLEEP <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; How long to sleep in seconds between checking metrics <br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; after a scaling operation</pre>

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
