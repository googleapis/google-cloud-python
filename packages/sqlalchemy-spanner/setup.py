from setuptools import setup

setup(
    name="sqlalchemy-spanner",
    version='0.1',
    description="SQLAlchemy dialect integrated into Spanner database",
    author='QLogic LLC',
    author_email='cloud-spanner-developers@googlegroups.com',
    packages=['spanner'],
    classifiers=[
        "Intended Audience :: Developers",
    ],
    install_requires=[
        'sqlalchemy>=1.1.13',
        'google-cloud-spanner==3.0.0'
    ],
    entry_points={
        'sqlalchemy.dialects': [
            'spanner = spanner.sqlalchemy_spanner:SpannerDialect'
        ]
    }
)
