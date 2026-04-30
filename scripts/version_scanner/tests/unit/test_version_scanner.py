import csv
import os
import re
from unittest.mock import patch
import pytest
import yaml
from version_scanner import ConfigManager, scan_file, write_csv_report

# Test ConfigManager
@pytest.mark.parametrize("dependency, version, expected", [
    (
        "python", 
        "3.7", 
        {"name": "python", "version": "3.7", "major": "3", "minor": "7", "minor_plus_one": "8", "minor_minus_one": "6"}
    ),
    (
        "protobuf", 
        "4.25.8", 
        {"name": "protobuf", "version": "4.25.8", "major": "4", "minor": "25", "patch": "8", "minor_plus_one": "26", "minor_minus_one": "24"}
    ),
    (
        "foo", 
        "3", 
        {"name": "foo", "version": "3", "major": "3"}
    ),
])
def test_compute_variables(dependency, version, expected):
    cm = ConfigManager("dummy_path", dependency, version)
    vars = cm._compute_variables()
    assert vars == expected

# Test scan_file
def test_scan_file_positive(tmp_path):
    test_file = tmp_path / "test.py"
    test_file.write_text("python_requires = '>=3.7'\n")
    
    rules = [
        {"name": "python_requires_check", "pattern": re.compile(r"python_requires\s*=\s*['\"]>=3\.7['\"]")}
    ]
    
    results = scan_file(str(test_file), rules)
    assert len(results) == 1
    assert results[0]["rule_name"] == "python_requires_check"
    assert results[0]["line_number"] == 1
    assert results[0]["matched_string"] == "python_requires = '>=3.7'"

def test_scan_file_negative(tmp_path):
    test_file = tmp_path / "test.py"
    test_file.write_text("python_requires = '>=3.8'\n")
    
    rules = [
        {"name": "python_requires_check", "pattern": re.compile(r"python_requires\s*=\s*['\"]>=3\.7['\"]")}
    ]
    
    results = scan_file(str(test_file), rules)
    assert len(results) == 0

# Test directory scan simulation
def test_directory_scan(tmp_path):
    # Create dummy files
    p1 = tmp_path / "pkg1"
    p1.mkdir()
    f1 = p1 / "setup.py"
    f1.write_text("python_requires = '>=3.7'\n")
    
    p2 = tmp_path / "pkg2"
    p2.mkdir()
    f2 = p2 / "clean.py"
    f2.write_text("print('Hello')\n")
    
    rules = [
        {"name": "python_requires_check", "pattern": re.compile(r"python_requires\s*=\s*['\"]>=3\.7['\"]")}
    ]
    
    results = []
    for root, dirs, files in os.walk(tmp_path):
        for file in files:
            file_path = os.path.join(root, file)
            results.extend(scan_file(file_path, rules))
            
    assert len(results) == 1
    assert results[0]["rule_name"] == "python_requires_check"

# Test write_csv_report
def test_write_csv_report(tmp_path):
    output_file = tmp_path / "report.csv"
    matches = [
        {
            "file_path": "./setup.py",
            "rule_name": "python_requires_check",
            "line_number": 1,
            "matched_string": "python_requires = '>=3.7'",
            "context_line": "python_requires = '>=3.7'"
        }
    ]
    
    write_csv_report(str(output_file), matches)
    
    assert output_file.exists()
    
    with open(output_file, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    assert rows[0]["file_path"] == "./setup.py"
    assert rows[0]["rule_name"] == "python_requires_check"
    assert rows[0]["line_number"] == "1"
    assert rows[0]["matched_string"] == "python_requires = '>=3.7'"
    assert rows[0]["context_line"] == "python_requires = '>=3.7'"


def test_load_config(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
rules:
  - name: test_rule
    rules:
      - python{version}
""")
    
    cm = ConfigManager(str(config_file), "python", "3.7")
    rules = cm.load_config()
    
    assert len(rules) == 1
    assert rules[0]["name"] == "test_rule"
    assert rules[0]["pattern"] == "python3.7"


@pytest.mark.parametrize("template, expected_warning", [
    ("python{missing_var}", "Warning: Missing variable for interpolation"),
    ("python{version", "Warning: Invalid format string"),
])
def test_load_config_error_handling(tmp_path, capsys, template, expected_warning):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(f"""
rules:
  - name: test_rule
    rules:
      - {template}
""")
    
    cm = ConfigManager(str(config_file), "python", "3.7")
    rules = cm.load_config()
    
    assert len(rules) == 0
    
    captured = capsys.readouterr()
    assert expected_warning in captured.err


def test_load_config_permission_error(tmp_path, capsys):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("rules: []")
    
    cm = ConfigManager(str(config_file), "python", "3.7")
    
    with patch("builtins.open", side_effect=PermissionError("Permission denied")):
        with pytest.raises(SystemExit) as excinfo:
            cm.load_config()
            
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Permission denied reading config file" in captured.err




def test_regex_examples_from_config():
    """Test that examples in config match at least one rule in the group."""
    config_path = "regex_config.yaml"
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        pytest.fail(f"Config file not found: {config_path}")
        
    rules_list = config.get("rules", [])
    
    # Variables for interpolation (simulate Python 3.7)
    vars = {
        "major": "3",
        "minor": "7",
        "version": "3.7",
        "minor_plus_one": "8",
        "minor_minus_one": "6"
    }
    
    for rule_group in rules_list:
        name = rule_group.get("name")
        examples = rule_group.get("examples", [])
        templates = rule_group.get("rules", [])
        
        if not examples or not templates:
            continue
            
        compiled_patterns = []
        for template in templates:
            try:
                resolved = template.strip().format(**vars)
                compiled_patterns.append(re.compile(resolved))
            except KeyError:
                continue
                
        for example in examples:
            matched = False
            for pattern in compiled_patterns:
                if pattern.search(example):
                    matched = True
                    break
            assert matched, f"Example '{example}' in group '{name}' did not match any pattern."
