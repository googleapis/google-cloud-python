
*   Send PR to prepare release on scheduled date.

    *   Add current date and any missing changes to [`docs/source/changelog.rst`](https://github.com/pydata/pandas-gbq/blob/master/docs/source/changelog.rst).

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
        python setup.py register sdist bdist_wheel --universal

*   Upload to test PyPI

        twine upload --repository testpypi dist/*

*   Try out test PyPI package

        pip install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pandas-gbq

*   Upload to PyPI

        twine upload dist/*

*   Create the [release on GitHub](https://github.com/pydata/pandas-gbq/releases/new) using the tag created earlier.

    *   Copy release notes from [changelog.rst](https://github.com/pydata/pandas-gbq/blob/master/docs/source/changelog.rst).
    *   Upload wheel and source zip from `dist/` directory.

*   Do a pull-request to the feedstock on `pandas-gbq-feedstock <https://github.com/conda-forge/pandas-gbq-feedstock/>`__
    (Or review PR from @regro-cf-autotick-bot which updates the feedstock).

    *   update the version
    *   update the SHA256 (retrieve from PyPI)
    *   update the dependencies (if they changed)
