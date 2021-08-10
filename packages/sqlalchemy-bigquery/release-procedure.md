# sqlalchemy-bigquery release procedure

*   Checkout master branch

        git fetch upstream master
        git checkout master
        git rebase -i upstream/master

*   Update version number in `setup.py`

*   Update `CHANGELOG.md`

*   Commit and push

        git commit -m "Release x.x.x"
        git push upstream master

*   Build the package

        git clean -xfd
        python setup.py register sdist bdist_wheel --universal

*   Upload to test PyPI

        twine upload --repository testpypi dist/*

*   Try out test PyPI package

        pip install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple sqlalchemy-bigquery

*   Upload to PyPI

        twine upload dist/*

*   Tag release on GitHub

