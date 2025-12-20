
*   Send PR to prepare release on scheduled date.

*   Verify your local repository is on the latest changes. `rebase -i` should be noop.

        git fetch pandas-gbq master
        git checkout master
        git rebase -i pandas-gbq/master
        git diff pandas-gbq/master

*   Tag commit

        git tag -a x.x.x -m 'Version x.x.x'

*   Push to GitHub

        git push pandas-gbq master --tags

*   Build the package

        git clean -xfd
        python setup.py register sdist bdist_wheel

*   Upload to test PyPI

        twine upload --repository testpypi dist/*

*   Try out test PyPI package

        pip install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pandas-gbq

*   Upload to PyPI

        twine upload dist/*

*   Create the [release on GitHub](https://github.com/googleapis/python-bigquery-pandas/releases/new) using the tag created earlier.

    *   Upload wheel and source zip from `dist/` directory.
