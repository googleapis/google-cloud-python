from setuptools import find_packages
from setuptools import setup

setup(
    name='expenses',
    version='0.1',
    description='Expense report upload (example for gcloud.datastore)',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'gcloud',
    ],
    entry_points={
        'console_scripts': [
            'submit_expenses = expenses.scripts.submit_expenses:main',
            'review_expenses = expenses.scripts.review_expenses:main',
        ],
    },
)
