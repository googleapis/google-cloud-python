# Copyright 2019. PyData Development Team
# Distributed under BSD 3-Clause License.
# See LICENSE.txt for details.

"""System tests for read_gbq code samples."""

from .. import read_gbq_legacy
from .. import read_gbq_simple


def test_read_gbq_legacy(project_id):
    df = read_gbq_legacy.main(project_id)
    assert df is not None
    assert "ZA" in df["alpha_2_code"].values
    assert "South Africa" in df["country_name"].values


def test_read_gbq_simple(project_id):
    df = read_gbq_simple.main(project_id)
    assert df is not None
    assert "AU" in df["alpha_2_code"].values
    assert "Australia" in df["country_name"].values
