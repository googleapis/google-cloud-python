# Ensure you are on the sandbox branch
git checkout experiment-testing-infra

# Loop through the first 15 packages and inject an actual test file
for dir in $(find packages -mindepth 1 -maxdepth 1 -type d | head -n 15); do
  # Ensure the target directory exists
  mkdir -p "${dir}/tests/unit"
  
  # Inject the passing test
  cat << 'EOF' > "${dir}/tests/unit/test_scale_validation.py"
def test_fan_out_execution():
    """Verify L5 Fan-Out architecture executes successfully."""
    assert True
EOF
done

# Commit and push the massive execution test
git add packages/
git commit -m "test: inject dummy unit tests across 15 packages to verify concurrent execution"
git push origin ci-architecture-prototype