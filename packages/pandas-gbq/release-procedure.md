*   Tag commit

        git tag -a x.x.x -m 'Version x.x.x'

*   and push to github

        git push pandas-gbq master --tags

*  Upload to PyPI

        git clean -xfd
        python setup.py register sdist bdist_wheel --universal
        twine upload dist/*

*   Update anaconda recipe.

    This should happen automatically within a day or two.

*   Update conda recipe feedstock on `conda-forge <https://conda-forge.github.io/>`_.
