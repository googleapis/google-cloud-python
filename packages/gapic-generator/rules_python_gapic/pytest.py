import sys
import pytest
import os


if __name__ == '__main__':
    sys.exit(pytest.main([
        '--disable-pytest-warnings',
        '--quiet',
        os.path.dirname(os.path.abspath(__file__))
    ]))
