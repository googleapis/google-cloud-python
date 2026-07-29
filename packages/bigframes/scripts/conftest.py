import sys
from pathlib import Path

# inserts scripts into path so that tests can import
project_root = Path(__file__).parent.parent
scripts_dir = project_root / "scripts"

sys.path.insert(0, str(scripts_dir))
