# Automated Dependency Version Scanner

This tool scans the repository for hardcoded references to specific dependency versions (like Python 3.7) that need to be upgraded or removed.

## Usage

Run the script from the repository root:

```bash
python3 scripts/version_scanner/version_scanner.py -d <dependency> -v <version> [options]
```

### Options

*   `-d`, `--dependency`: The dependency name (e.g., `python`).
*   `-v`, `--version`: The specific version to search for (e.g., `3.7`).
*   `-p`, `--path`: Root directory to scan (defaults to current directory).
*   `--package`: Specific package directory to scan (useful for testing).
*   `--package-file`: Path to a file containing a list of package directories to scan.
*   `--config`: Path to the regex configuration file (defaults to `regex_config.yaml`).
*   `-o`, `--output`: Path to the output CSV file.
*   `--github-repo`: GitHub repository URL base for generating links.
*   `--branch`: GitHub branch for links (defaults to `main`).

## Configuration

The scanner uses a YAML configuration file (`regex_config.yaml`) to define rules and regex patterns.

## Ignoring Directories

You can create a `.scannerignore` file in the directory you are scanning (usually the repo root) to list directories to skip, one per line.
