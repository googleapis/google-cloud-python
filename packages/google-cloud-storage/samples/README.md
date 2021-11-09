
<img src="https://avatars2.githubusercontent.com/u/2810941?v=3&s=96" alt="Google Cloud Platform logo" title="Google Cloud Platform" align="right" height="96" width="96"/>

# Google Cloud Storage Python Samples

[![Open in Cloud Shell][shell_img]][shell_link]


This directory contains samples for Google Cloud Storage.
[Cloud Storage](https://cloud.google.com/storage/docs) allows world-wide
storage and retrieval of any amount of data at any time. You can use Google
Cloud Storage for a range of scenarios including serving website content,
storing data for archival and disaster recovery, or distributing large data
objects to users via direct download.

## Setup

### Before you begin

Before running the samples, make sure you've followed the steps outlined in
[Quick Start](https://github.com/googleapis/python-storage#quick-start).

### Authentication
This sample requires you to have authentication setup. Refer to the [Authentication Getting Started Guide](https://cloud.google.com/docs/authentication/getting-started)
for instructions on setting up credentials for applications.

### Install Dependencies
1. Clone this repository and change to the sample directory you want to use.
    ```
    git clone https://github.com/googleapis/python-storage.git
    ```

2. Install [pip](https://pip.pypa.io/) and [virtualenv](https://virtualenv.pypa.io) if you do not already have them. You may want to refer to the [Python Development Environment Setup Guide](https://cloud.google.com/python/setup) for Google Cloud Platform for instructions.

3. Create a virtualenv. Samples are compatible with Python 3.6+.
    ```
    virtualenv env
    source env/bin/activate
    ```

4. Install the dependencies needed to run the samples.
    ```
    cd samples/snippets
    pip install -r requirements.txt
    ```

## Samples
<details>
    <summary><b>List of Samples</b></summary>

* [Activate HMAC Key](#activate-hmac-key)
* [Add Bucket Conditional IAM Binding](#add-bucket-conditional-iam-binding)
* [Add Bucket Default Owner](#add-bucket-default-owner)
* [Add Bucket IAM Member](#add-bucket-iam-member)
* [Add Bucket Label](#add-bucket-label)
* [Add Bucket Owner](#add-bucket-owner)
* [Add File Owner](#add-file-owner)
* [Bucket Delete Default KMS Key](#bucket-delete-default-kms-key)
* [Change Default Storage Class](#change-default-storage-class)
* [Change File Storage Class](#change-file-storage-class)
* [Compose File](#compose-file)
* [Configure Retries](#configure-retries)
* [Copy File](#copy-file)
* [Copy File Archived Generation](#copy-file-archived-generation)
* [CORS Configuration](#cors-configuration)
* [Create Bucket](#create-bucket)
* [Create Bucket Class Location](#create-bucket-class-location)
* [Create HMAC Key](#create-hmac-key)
* [Deactivate HMAC Key](#deactivate-hmac-key)
* [Define Bucket Website Configuration](#define-bucket-website-configuration)
* [Delete Bucket](#delete-bucket)
* [Delete File](#delete-file)
* [Delete File Archived Generation](#delete-file-archived-generation)
* [Delete HMAC Key](#delete-hmac-key)
* [Disable Bucket Lifecycle Management](#disable-bucket-lifecycle-management)
* [Disable Default Event Based Hold](#disable-default-event-based-hold)
* [Disable Requester Pays](#disable-requester-pays)
* [Disable Uniform Bucket Level Access](#disable-uniform-bucket-level-access)
* [Disable Versioning](#disable-versioning)
* [Download Encrypted File](#download-encrypted-file)
* [Download File](#download-file)
* [Download File Requester Pays](#download-file-requester-pays)
* [Download Public File](#download-public-file)
* [Enable Bucket Lifecycle Management](#enable-bucket-lifecycle-management)
* [Enable Default Event Based Hold](#enable-default-event-based-hold)
* [Enable Requester Pays](#enable-requester-pays)
* [Enable Uniform Bucket Level Access](#enable-uniform-bucket-level-access)
* [Enable Versioning](#enable-versioning)
* [FileIO Write-Read] (#fileio-write-read)
* [FileIO Pandas] (#fileio-pandas)
* [Generate Encryption Key](#generate-encryption-key)
* [Generate Signed Post Policy V4](#generate-signed-post-policy-v4)
* [Generate Signed Url V2](#generate-signed-url-v2)
* [Generate Signed Url V4](#generate-signed-url-v4)
* [Generate Upload Signed Url V4](#generate-upload-signed-url-v4)
* [Get Bucket Labels](#get-bucket-labels)
* [Get Bucket Metadata](#get-bucket-metadata)
* [Get Default Event Based Hold](#get-default-event-based-hold)
* [Get HMAC Key](#get-hmac-key)
* [Get Metadata](#get-metadata)
* [Get Public Access Prevention](#get-public-access-prevention)
* [Get Requester Pays Status](#get-requester-pays-status)
* [Get Retention Policy](#get-retention-policy)
* [Get Service Account](#get-service-account)
* [Get Uniform Bucket Level Access](#get-uniform-bucket-level-access)
* [List Buckets](#list-buckets)
* [List File Archived Generations](#list-file-archived-generations)
* [List Files](#list-files)
* [List Files With Prefix](#list-files-with-prefix)
* [List HMAC Keys](#list-hmac-keys)
* [Lock Retention Policy](#lock-retention-policy)
* [Make Public](#make-public)
* [Move File](#move-file)
* [Object CSEK To CMEK](#object-csek-to-cmek)
* [Object Get KMS Key](#object-get-kms-key)
* [Print Bucket ACL](#print-bucket-acl)
* [Print Bucket ACL For User](#print-bucket-acl-for-user)
* [Print File ACL](#print-file-acl)
* [Print File ACL For User](#print-file-acl-for-user)
* [Release Event Based Hold](#release-event-based-hold)
* [Release Temporary Hold](#release-temporary-hold)
* [Remove Bucket Conditional IAM Binding](#remove-bucket-conditional-iam-binding)
* [Remove Bucket Default Owner](#remove-bucket-default-owner)
* [Remove Bucket IAM Member](#remove-bucket-iam-member)
* [Remove Bucket Label](#remove-bucket-label)
* [Remove Bucket Owner](#remove-bucket-owner)
* [Remove Cors Configuration](#remove-cors-configuration)
* [Remove File Owner](#remove-file-owner)
* [Remove Retention Policy](#remove-retention-policy)
* [Rename File](#rename-file)
* [Rotate Encryption Key](#rotate-encryption-key)
* [Set Bucket Default KMS Key](#set-bucket-default-kms-key)
* [Set Bucket Public IAM](#set-bucket-public-iam)
* [Set Event Based Hold](#set-event-based-hold)
* [Set Metadata](#set-metadata)
* [Set Public Access Prevention Enforced](#set-public-access-prevention-enforced)
* [Set Public Access Prevention Inherited](#set-public-access-prevention-inherited)
* [Set Public Access Prevention Unspecified](#set-public-access-prevention-unspecified)
* [Set Retention Policy](#set-retention-policy)
* [Set Temporary Hold](#set-temporary-hold)
* [Upload Encrypted File](#upload-encrypted-file)
* [Upload File](#upload-file)
* [Upload With KMS Key](#upload-with-kms-key)
* [View Bucket IAM Members](#view-bucket-iam-members)

</details>

-----
### Activate HMAC Key
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_activate_hmac_key.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_activate_hmac_key.py). To run this sample:


`python storage_activate_hmac_key.py`

-----

### Add Bucket Conditional IAM Binding
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_add_bucket_conditional_iam_binding.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_add_bucket_conditional_iam_binding.py). To run this sample:


`python storage_add_bucket_conditional_iam_binding.py`

-----
### Add Bucket Default Owner
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_add_bucket_default_owner.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_add_bucket_default_owner.py). To run this sample:


`python storage_add_bucket_default_owner.py`

-----
### Add Bucket IAM Member
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_add_bucket_iam_member.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_add_bucket_iam_member.py). To run this sample:


`python storage_add_bucket_iam_member.py`

-----
### Add Bucket Label
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_add_bucket_label.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_add_bucket_label.py). To run this sample:


`python storage_add_bucket_label.py`

-----
### Add Bucket Owner
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_add_bucket_owner.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_add_bucket_owner.py). To run this sample:


`python storage_add_bucket_owner.py`

-----
### Add File Owner
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_add_file_owner.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_add_file_owner.py). To run this sample:


`python storage_add_file_owner.py`

-----
### Bucket Delete Default KMS Key
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_bucket_delete_default_kms_key.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_bucket_delete_default_kms_key.py). To run this sample:


`python storage_bucket_delete_default_kms_key.py`

-----
### Change Default Storage Class
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_change_default_storage_class.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_change_default_storage_class.py). To run this sample:


`python storage_change_default_storage_class.py`

-----
### Change File Storage Class
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_change_file_storage_class.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_change_file_storage_class.py). To run this sample:


`python storage_change_file_storage_class.py`

-----
### Compose File
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_compose_file.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_compose_file.py). To run this sample:


`python storage_compose_file.py`

-----
### Configure Retries
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_configure_retries.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_configure_retries.py). To run this sample:


`python storage_configure_retries.py`

-----
### Copy File
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_copy_file.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_copy_file.py). To run this sample:


`python storage_copy_file.py`

-----
### Copy File Archived Generation
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_copy_file_archived_generation.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_copy_file_archived_generation.py). To run this sample:


`python storage_copy_file_archived_generation.py`

-----
### CORS Configuration
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_cors_configuration.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_cors_configuration.py). To run this sample:


`python storage_cors_configuration.py`

-----
### Create Bucket
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_create_bucket.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_create_bucket.py). To run this sample:


`python storage_create_bucket.py`

-----
### Create Bucket Class Location
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_create_bucket_class_location.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_create_bucket_class_location.py). To run this sample:


`python storage_create_bucket_class_location.py`

-----
### Create HMAC Key
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_create_hmac_key.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_create_hmac_key.py). To run this sample:


`python storage_create_hmac_key.py`

-----
### Deactivate HMAC Key
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_deactivate_hmac_key.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_deactivate_hmac_key.py). To run this sample:


`python storage_deactivate_hmac_key.py`

-----
### Define Bucket Website Configuration
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_define_bucket_website_configuration.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_define_bucket_website_configuration.py). To run this sample:


`python storage_define_bucket_website_configuration.py`

-----
### Delete Bucket
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_delete_bucket.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_delete_bucket.py). To run this sample:


`python storage_delete_bucket.py`

-----
### Delete File
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_delete_file.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_delete_file.py). To run this sample:


`python storage_delete_file.py`

-----
### Delete File Archived Generation
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_delete_file_archived_generation.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_delete_file_archived_generation.py). To run this sample:


`python storage_delete_file_archived_generation.py`

-----
### Delete HMAC Key
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_delete_hmac_key.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_delete_hmac_key.py). To run this sample:


`python storage_delete_hmac_key.py`

-----
### Disable Bucket Lifecycle Management
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_disable_bucket_lifecycle_management.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_disable_bucket_lifecycle_management.py). To run this sample:


`python storage_disable_bucket_lifecycle_management.py`

-----
### Disable Default Event Based Hold
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_disable_default_event_based_hold.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_disable_default_event_based_hold.py). To run this sample:


`python storage_disable_default_event_based_hold.py`

-----
### Disable Requester Pays
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_disable_requester_pays.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_disable_requester_pays.py). To run this sample:


`python storage_disable_requester_pays.py`

-----
### Disable Uniform Bucket Level Access
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_disable_uniform_bucket_level_access.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_disable_uniform_bucket_level_access.py). To run this sample:


`python storage_disable_uniform_bucket_level_access.py`

-----
### Disable Versioning
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_disable_versioning.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_disable_versioning.py). To run this sample:


`python storage_disable_versioning.py`

-----
### Download Encrypted File
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_download_encrypted_file.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_download_encrypted_file.py). To run this sample:


`python storage_download_encrypted_file.py`

-----
### Download File
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_download_file.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_download_file.py). To run this sample:


`python storage_download_file.py`

-----
### Download File Requester Pays
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_download_file_requester_pays.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_download_file_requester_pays.py). To run this sample:


`python storage_download_file_requester_pays.py`

-----
### Download Public File
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_download_public_file.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_download_public_file.py). To run this sample:


`python storage_download_public_file.py`

-----
### Enable Bucket Lifecycle Management
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_enable_bucket_lifecycle_management.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_enable_bucket_lifecycle_management.py). To run this sample:


`python storage_enable_bucket_lifecycle_management.py`

-----
### Enable Default Event Based Hold
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_enable_default_event_based_hold.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_enable_default_event_based_hold.py). To run this sample:


`python storage_enable_default_event_based_hold.py`

-----
### Enable Requester Pays
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_enable_requester_pays.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_enable_requester_pays.py). To run this sample:


`python storage_enable_requester_pays.py`

-----
### Enable Uniform Bucket Level Access
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_enable_uniform_bucket_level_access.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_enable_uniform_bucket_level_access.py). To run this sample:


`python storage_enable_uniform_bucket_level_access.py`

-----
### Enable Versioning
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_enable_versioning.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_enable_versioning.py). To run this sample:


`python storage_enable_versioning.py`

-----
### FileIO Write-Read
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_fileio_write_read.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_fileio_write_read.py). To run this sample:


`python storage_fileio_write_read.py <BUCKET_NAME> <BLOB_NAME>`
-----
### FileIO Pandas
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_fileio_pandas.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_fileio_pandas.py). To run this sample:


`python storage_fileio_pandas.py <BUCKET_NAME> <BLOB_NAME>`
-----
### Generate Encryption Key
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_generate_encryption_key.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_generate_encryption_key.py). To run this sample:


`python storage_generate_encryption_key.py`

-----
### Generate Signed Post Policy V4
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_generate_signed_post_policy_v4.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_generate_signed_post_policy_v4.py). To run this sample:


`python storage_generate_signed_post_policy_v4.py`

-----
### Generate Signed Url V2
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_generate_signed_url_v2.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_generate_signed_url_v2.py). To run this sample:


`python storage_generate_signed_url_v2.py`

-----
### Generate Signed Url V4
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_generate_signed_url_v4.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_generate_signed_url_v4.py). To run this sample:


`python storage_generate_signed_url_v4.py`

-----
### Generate Upload Signed Url V4
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_generate_upload_signed_url_v4.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_generate_upload_signed_url_v4.py). To run this sample:


`python storage_generate_upload_signed_url_v4.py`

-----
### Get Bucket Labels
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_get_bucket_labels.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_get_bucket_labels.py). To run this sample:


`python storage_get_bucket_labels.py`

-----
### Get Bucket Metadata
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_get_bucket_metadata.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_get_bucket_metadata.py). To run this sample:


`python storage_get_bucket_metadata.py`

-----
### Get Default Event Based Hold
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_get_default_event_based_hold.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_get_default_event_based_hold.py). To run this sample:


`python storage_get_default_event_based_hold.py`

-----
### Get HMAC Key
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_get_hmac_key.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_get_hmac_key.py). To run this sample:


`python storage_get_hmac_key.py`

-----
### Get Metadata
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_get_metadata.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_get_metadata.py). To run this sample:


`python storage_get_metadata.py`

-----
### Get Public Access Prevention
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_get_public_access_prevention.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_get_public_access_prevention.py). To run this sample:


`python storage_get_public_access_prevention.py`

-----
### Get Requester Pays Status
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_get_requester_pays_status.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_get_requester_pays_status.py). To run this sample:


`python storage_get_requester_pays_status.py`

-----
### Get Retention Policy
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_get_retention_policy.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_get_retention_policy.py). To run this sample:


`python storage_get_retention_policy.py`

-----
### Get Service Account
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_get_service_account.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_get_service_account.py). To run this sample:


`python storage_get_service_account.py`

-----
### Get Uniform Bucket Level Access
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_get_uniform_bucket_level_access.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_get_uniform_bucket_level_access.py). To run this sample:


`python storage_get_uniform_bucket_level_access.py`

-----
### List Buckets
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_list_buckets.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_list_buckets.py). To run this sample:


`python storage_list_buckets.py`

-----
### List File Archived Generations
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_list_file_archived_generations.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_list_file_archived_generations.py). To run this sample:


`python storage_list_file_archived_generations.py`

-----
### List Files
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_list_files.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_list_files.py). To run this sample:


`python storage_list_files.py`

-----
### List Files With Prefix
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_list_files_with_prefix.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_list_files_with_prefix.py). To run this sample:


`python storage_list_files_with_prefix.py`

-----
### List HMAC Keys
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_list_hmac_keys.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_list_hmac_keys.py). To run this sample:


`python storage_list_hmac_keys.py`

-----
### Lock Retention Policy
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_lock_retention_policy.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_lock_retention_policy.py). To run this sample:


`python storage_lock_retention_policy.py`

-----
### Make Public
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_make_public.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_make_public.py). To run this sample:


`python storage_make_public.py`

-----
### Move File
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_move_file.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_move_file.py). To run this sample:


`python storage_move_file.py`

-----
### Object CSEK To CMEK
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_object_csek_to_cmek.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_object_csek_to_cmek.py). To run this sample:


`python storage_object_csek_to_cmek.py`

-----
### Object Get KMS Key
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_object_get_kms_key.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_object_get_kms_key.py). To run this sample:


`python storage_object_get_kms_key.py`

-----
### Print Bucket ACL
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_print_bucket_acl.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_print_bucket_acl.py). To run this sample:


`python storage_print_bucket_acl.py`

-----
### Print Bucket ACL For User
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_print_bucket_acl_for_user.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_print_bucket_acl_for_user.py). To run this sample:


`python storage_print_bucket_acl_for_user.py`

-----
### Print File ACL
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_print_file_acl.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_print_file_acl.py). To run this sample:


`python storage_print_file_acl.py`

-----
### Print File ACL For User
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_print_file_acl_for_user.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_print_file_acl_for_user.py). To run this sample:


`python storage_print_file_acl_for_user.py`

-----
### Release Event Based Hold
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_release_event_based_hold.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_release_event_based_hold.py). To run this sample:


`python storage_release_event_based_hold.py`

-----
### Release Temporary Hold
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_release_temporary_hold.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_release_temporary_hold.py). To run this sample:


`python storage_release_temporary_hold.py`

-----
### Remove Bucket Conditional IAM Binding
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_remove_bucket_conditional_iam_binding.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_remove_bucket_conditional_iam_binding.py). To run this sample:


`python storage_remove_bucket_conditional_iam_binding.py`

-----
### Remove Bucket Default Owner
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_remove_bucket_default_owner.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_remove_bucket_default_owner.py). To run this sample:


`python storage_remove_bucket_default_owner.py`

-----
### Remove Bucket IAM Member
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_remove_bucket_iam_member.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_remove_bucket_iam_member.py). To run this sample:


`python storage_remove_bucket_iam_member.py`

-----
### Remove Bucket Label
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_remove_bucket_label.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_remove_bucket_label.py). To run this sample:


`python storage_remove_bucket_label.py`

-----
### Remove Bucket Owner
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_remove_bucket_owner.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_remove_bucket_owner.py). To run this sample:


`python storage_remove_bucket_owner.py`

-----
### Remove CORS Configuration
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_remove_cors_configuration.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_remove_cors_configuration.py). To run this sample:


`python storage_remove_cors_configuration.py`

-----
### Remove File Owner
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_remove_file_owner.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_remove_file_owner.py). To run this sample:


`python storage_remove_file_owner.py`

-----
### Remove Retention Policy
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_remove_retention_policy.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_remove_retention_policy.py). To run this sample:


`python storage_remove_retention_policy.py`

-----
### Rename File
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_rename_file.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_rename_file.py). To run this sample:


`python storage_rename_file.py`

-----
### Rotate Encryption Key
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_rotate_encryption_key.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_rotate_encryption_key.py). To run this sample:


`python storage_rotate_encryption_key.py`

-----
### Set Bucket Default KMS Key
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_set_bucket_default_kms_key.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_set_bucket_default_kms_key.py). To run this sample:


`python storage_set_bucket_default_kms_key.py`

-----
### Set Bucket Public IAM
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_set_bucket_public_iam.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_set_bucket_public_iam.py). To run this sample:


`python storage_set_bucket_public_iam.py`

-----
### Set Event Based Hold
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_set_event_based_hold.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_set_event_based_hold.py). To run this sample:


`python storage_set_event_based_hold.py`

-----
### Set Metadata
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_set_metadata.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_set_metadata.py). To run this sample:


`python storage_set_metadata.py`

-----
### Set Public Access Prevention Enforced
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_set_public_access_prevention_enforced.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_set_public_access_prevention_enforced.py). To run this sample:


`python storage_set_public_access_prevention_enforced.py`

-----
### Set Public Access Prevention Inherited
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_set_public_access_prevention_inherited.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_set_public_access_prevention_inherited.py). To run this sample:


`python storage_set_public_access_prevention_inherited.py`

-----
### Set Public Access Prevention Unspecified
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_set_public_access_prevention_unspecified.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_set_public_access_prevention_unspecified.py). To run this sample:


`python storage_set_public_access_prevention_unspecified.py`

-----
### Set Retention Policy
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_set_retention_policy.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_set_retention_policy.py). To run this sample:


`python storage_set_retention_policy.py`

-----
### Set Temporary Hold
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_set_temporary_hold.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_set_temporary_hold.py). To run this sample:


`python storage_set_temporary_hold.py`

-----
### Upload Encrypted File
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_upload_encrypted_file.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_upload_encrypted_file.py). To run this sample:


`python storage_upload_encrypted_file.py`

-----
### Upload File
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_upload_file.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_upload_file.py). To run this sample:


`python storage_upload_file.py`

-----
### Upload With KMS Key
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_upload_with_kms_key.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_upload_with_kms_key.py). To run this sample:


`python storage_upload_with_kms_key.py`

-----
### View Bucket IAM Members
[![Open in Cloud Shell][shell_img]](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/snippets/storage_view_bucket_iam_members.py,samples/README.md)

View the [source code](https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_view_bucket_iam_members.py). To run this sample:


`python storage_view_bucket_iam_members.py`

-----

## Running tests locally

Before running the tests, make sure you've followed the steps outlined in
[Setup](#setup).

### Install nox
```
pip install nox
```

### Set environment variables

You can run tests locally using your own gcs project or with a valid service account in project `python-docs-samples-tests`. This outlines the workflow of running tests locally using your own gcs project. 

Refer to [`noxfile_config.py`](https://github.com/googleapis/python-storage/blob/main/samples/snippets/noxfile_config.py) and [a list of environment variables](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/testing/test-env.tmpl.sh) that can be set manually. Not every test needs all of these variables. 
The common environment variables used in the storage samples include:

    export GOOGLE_CLOUD_PROJECT=[your-project-name]
    export MAIN_GOOGLE_CLOUD_PROJECT=[your-project-name]
    export BUILD_SPECIFIC_GCLOUD_PROJECT=[your-project-name]
    export HMAC_KEY_TEST_SERVICE_ACCOUNT=[your-service-account]
    export CLOUD_KMS_KEY=[your-kms-key]
    export GOOGLE_APPLICATION_CREDENTIALS=[your-credentials]
    
See [Other Resources](#other-resources) on how to create credentials, keys, and secrets

### Run tests with nox
```
nox -s lint
nox -s py-3.7 -- snippets_test.py
nox -s py-3.7 -- snippets_test.py::test_list_blobs
```

### Special test configurations
There are restrictions on the testing projects used in Kokoro. For instance,
we change the service account based on different test sessions to avoid 
hitting the maximum limit of HMAC keys on a single service account.
Another example is `requester_pays_test.py` needs to use a different Storage bucket, and looks for an environment variable `REQUESTER_PAYS_TEST_BUCKET`.
Please refer to [`noxfile_config.py`](https://github.com/googleapis/python-storage/blob/main/samples/snippets/noxfile_config.py) , [kokoro configs](https://github.com/googleapis/python-storage/tree/main/.kokoro/samples), and test files to see if there are special test configurations required.


### Other Resources
* [Create Cloud KMS Keys](https://cloud.google.com/kms/docs/creating-keys)
* [Create HMAC Keys](https://cloud.google.com/storage/docs/authentication/managing-hmackeys)
* [Create Service Accounts](https://cloud.google.com/docs/authentication/getting-started#creating_a_service_account)

[shell_img]: https://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/googleapis/python-storage&page=editor&open_in_editor=samples/README.md
[product-docs]: https://cloud.google.com/storage