import csv
import os
import subprocess
import pytest

def test_integration_scan(tmp_path):
    # Paths to real tools
    scanner_path = os.path.abspath("version_scanner.py")
    config_path = os.path.abspath("regex_config.yaml")
    
    # Static data directory
    data_dir = os.path.abspath("tests/data")
    
    # Run the scanner in the tmp_path so the output file is created there
    cmd = [
        "python3", scanner_path,
        "-d", "python",
        "-v", "3.7",
        "-p", data_dir,
        "--config", config_path,
        "-o", "scanner_report.csv"
    ]
    
    result = subprocess.run(cmd, cwd=tmp_path, capture_output=True, text=True, check=True)
    
    report_file = tmp_path / "scanner_report.csv"
    assert report_file.exists(), f"Report file not found. Stderr: {result.stderr}"
    
    with open(report_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    # We expect at least some matches when we build the data directory
    assert len(rows) > 0
