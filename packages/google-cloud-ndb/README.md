# Google Datastore `ndb` Client Library

## Introduction

`ndb` is a client library for use with [Google Cloud Datastore][0].
It was designed specifically to be used from within the
[Google App Engine][1] Python runtime.

## Overview

Learn how to use the `ndb` library by visiting the Google Cloud Platform
[documentation][2].

[0]: https://cloud.google.com/datastore
[1]: https://cloud.google.com/appengine
[2]: https://cloud.google.com/appengine/docs/python/ndb/

## Installation 

Install this library in a virtualenv using pip. virtualenv is a tool to create isolated Python environments. The basic problem it addresses is one of dependencies and versions, and indirectly permissions.

With virtualenv, it's possible to install this library without needing system install permissions, and without clashing with the installed system dependencies.

### Supported Python Versions
Python >= 3.6

As this package is designed to work in the [AppEngine runtime](https://cloud.google.com/appengine/docs/python/) Python 3.6+ are supported. 

### Mac/Linux
```
pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install google-cloud-ndb
```

### Windows
```
pip install virtualenv
virtualenv <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install google-cloud-ndb
```
