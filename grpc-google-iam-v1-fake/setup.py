import setuptools

from setuptools import find_packages
from setuptools import setup

install_requires = [
  'grpcio>=1.0.0, <2.0.0',
  'googleapis-common-protos[grpc]>=1.3.4, <2.0.0'
]

setuptools.setup(
  name='grpc-google-iam-v1',
  version='0.10.0',
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
    'Programming Language :: Python :: Implementation :: CPython',
  ],
  description='GRPC library for the google-iam-v1 service',
  long_description=open('README.rst').read(),
  install_requires=install_requires,
  license='Apache-2.0',
  packages=find_packages(),
  namespace_packages=['google', 'google.iam', ],
  url='https://github.com/googleapis/googleapis'
)
