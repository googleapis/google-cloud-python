from setuptools import find_packages, setup

install_requires = [
    'django >= 2.0',
    'google-cloud >= 0.34.0',
    'google-cloud-spanner >= 1.8.0',
]

setup(
        name='spanner',
        version='0.0.1',
        author='Google LLC',
        author_email='cloud-spanner-developers@googlegroups.com',
        description=('Bridge to enable using Django with Spanner.'),
        license='Apache 2.0',
        packages=find_packages(exclude=['tests']),
        install_requires=install_requires,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache 2 License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Utilities',
            'Framework :: Django',
            'Framework :: Django :: 2.1',
            'Framework :: Django :: 2.2',
            'Framework :: Django :: 3.0',
        ],
)
