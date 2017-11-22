"""A setup module for the GAPIC BigQuery Data Transfer API library.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import io
import sys

install_requires = [
    'google-api-core>=0.1.0, <0.2.0dev',
    'google-auth>=1.0.2, <2.0dev',
    'googleapis-common-protos[grpc]>=1.5.2, <2.0dev',
    'requests>=2.18.4, <3.0dev',
]

with io.open('README.rst', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='google-cloud-bigquerydatatransfer',
    version='0.15.4',
    author='Google Inc',
    author_email='googleapis-packages@google.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    description='GAPIC library for the BigQuery Data Transfer API',
    include_package_data=True,
    long_description=long_description,
    install_requires=install_requires,
    license='Apache 2.0',
    packages=find_packages(),
    namespace_packages=['google', 'google.cloud'],
    url='https://github.com/googleapis/googleapis')
