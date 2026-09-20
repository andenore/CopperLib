import os
import sys
from pathlib import Path

source = os.environ.get("COPPERSCRIPT_SOURCE")
if source:
    sys.path.insert(0, str(Path(source)))
