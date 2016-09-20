import os

from setuptools import setup


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(PROJECT_ROOT, 'README.rst')) as file_obj:
    README = file_obj.read()


REQUIREMENTS = [
    'google-cloud-bigquery',
    'google-cloud-bigtable',
    'google-cloud-core',  # Redunant
    'google-cloud-datastore',
    'google-cloud-dns',
    'google-cloud-error-reporting',
    'google-cloud-happybase',
    'google-cloud-language',
    'google-cloud-logging',
    'google-cloud-monitoring',
    # 'google-cloud-natural-language',  # Synonym for -language
    'google-cloud-pubsub',
    'google-cloud-resource-manager',
    'google-cloud-speech',
    'google-cloud-storage',
    'google-cloud-translate',
    'google-cloud-vision',
]

setup(
    name='google-cloud',
    version='0.19.0',
    description='API Client library for Google Cloud',
    author='Google Cloud Platform',
    author_email='jjg+google-cloud-python@google.com',
    long_description=README,
    scripts=[],
    url='https://github.com/GoogleCloudPlatform/google-cloud-python',
    license='Apache 2.0',
    platforms='Posix; MacOS X; Windows',
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
    ]
)
