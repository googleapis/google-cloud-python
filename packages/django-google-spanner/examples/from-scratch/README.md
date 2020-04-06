## django-spanner for Django tutorial

This example shows how to use django-spanner for Cloud Spanner as a backend database for [Django's tutorials](https://docs.djangoproject.com/en/2.2/intro/tutorial01/)

### Walkthrough the introduction to Django

### Install django-spanner
We'll need to install `django-spanner`, by cloning this repository and then running `pip3 install`
```shell
git clone https://github.com/googleapis/django-spanner
pip3 install .
```

### Ensure you have a Cloud Spanner database already created
If you haven't already, please follow the steps to install [Cloud Spanner](https://cloud.google.com/spanner/docs/getting-started/set-up),
or visit this [codelab](https://opencensus.io/codelabs/spanner/#0)

**You'll need to ensure that your Google Application Default Credentials are properly downloaded and saved in your environment.**

### Follow the tutorial
Please follow the guides in https://docs.djangoproject.com/en/2.2/intro/tutorial01/ until the end with a single DISTINCTION:

### Update your settings.py file to use django-spanner
After we have a Cloud Spanner database created, we'll need a few variables:
* ProjectID
* Instance name
* Database name aka DisplayName

Once in, please edit the file `hc/local_settings.py` and make the section `DATABASES` into the following:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django_spanner',
        'PROJECT': PROJECT_ID,
        'INSTANCE': SPANNER_INSTANCE,
        'NAME': SPANNER_DATABASE_NAME,
    }
}
```

and for example here is a filled in database where:

* `PROJECT_ID`: spanner-appdev
* INSTANCE: instance
* NAME: `healthchecks_db`

which when filled out, will look like this

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_spanner',
        'PROJECT': 'spanner-appdev',
        'INSTANCE': 'instance',
        'NAME': 'healthchecks_db',
    }
}
```


### Apply the migrations
Please run:
```shell
$ python3 manage.py migrate
```

and that'll take a while running, but when done, it will look like the following

<details>

```shell
$ python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying sessions.0001_initial... OK
```
</details>

### Now run your server
After those migrations are completed, that will be all. Please continue on with the guides.

### Comprehensive hands-on guide
For a more comprehensive, step by step hands-on guide, please visit [using django-spanner from scratch](https://orijtech-161805.firebaseapp.com/quickstart/new_app/)


### References

Resource|URL
---|---
Cloud Spanner homepage|https://cloud.google.com/spanner/
django-spanner project's source code|https://github.com/googleapis/python-spanner-django/
django-spanner from scratch|https://orijtech-161805.firebaseapp.com/quickstart/new_app/
