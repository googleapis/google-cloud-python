*   Tag commit

        git tag -a x.x.x -m 'Version x.x.x'

*   and push to github

        git push pandas-gbq master --tags

*  Upload to PyPI

        git clean -xfd
        python setup.py register sdist bdist_wheel --universal
        twine upload dist/*

*  Do a pull-request to the feedstock on `pandas-gbq-feedstock <https://github.com/conda-forge/pandas-gbq-feedstock/>`__

        update the version
        update the SHA256 (retrieve from PyPI)
