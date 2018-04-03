*   Tag commit

        git tag -a x.x.x -m 'Version x.x.x'

*   and push to github

        git push pandas-gbq master --tags

*  Build the package

        git clean -xfd
        python setup.py register sdist bdist_wheel --universal

*  Upload to test PyPI

       twine upload --repository testpypi dist/*

* Try out test PyPI package

       pip install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pandas-gbq

*  Upload to PyPI

        twine upload dist/*

*  Do a pull-request to the feedstock on `pandas-gbq-feedstock <https://github.com/conda-forge/pandas-gbq-feedstock/>`__

        update the version
        update the SHA256 (retrieve from PyPI)
