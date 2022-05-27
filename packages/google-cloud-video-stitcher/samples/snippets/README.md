# Video Stitcher API Python Samples

This directory contains samples for the Video Stitcher API. Use this API to
generate dynamic content for delivery to client devices. You can call the Video
Stitcher API from your servers to dynamically insert ads into video-on-demand
and live streams for your users. For more information, see the
[Video Stitcher API documentation](https://cloud.google.com/video-stitcher/).

## Setup

To run the samples, you need to first follow the steps in
[Before you begin](https://cloud.google.com/video-stitcher/docs/how-to/before-you-begin).

For more information on authentication, refer to the
[Authentication Getting Started Guide](https://cloud.google.com/docs/authentication/getting-started).

## Install Dependencies

1. Clone python-video-stitcher and change directories to the sample directory
you want to use.

        $ git clone https://github.com/googleapis/python-video-stitcher.git

1. Install [pip](https://pip.pypa.io/) and
[virtualenv](https://virtualenv.pypa.io/) if you do not already have them. You
may want to refer to the
[Python Development Environment Setup Guide](https://cloud.google.com/python/setup)
for Google Cloud Platform for instructions.

1. Create a virtualenv. Samples are compatible with Python 3.6+.

        $ virtualenv env
        $ source env/bin/activate

1. Install the dependencies needed to run the samples.

        $ pip install -r requirements.txt

## Testing

Make sure to enable the Video Stitcher API on the test project. Set the
following environment variables:

*   `GOOGLE_CLOUD_PROJECT`
*   `GOOGLE_CLOUD_PROJECT_NUMBER`