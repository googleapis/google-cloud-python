"""A setup module for the GAPIC Dialogflow API library.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import io

install_requires = [
    'google-api-core[grpc]<2.0.0dev,>=0.1.4',
    'googleapis-common-protos[grpc]>=1.5.2, <2.0dev',
]

with io.open('README.rst', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='dialogflow',
    version='0.4.0',
    author='Google LLC',
    author_email='googleapis-packages@google.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
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
    description='Client library for the Dialogflow API',
    include_package_data=True,
    long_description=long_description,
    install_requires=install_requires,
    license='Apache 2.0',
    packages=find_packages(),
    url='https://github.com/dialogflow/dialogflow-python-client-v2',
)
