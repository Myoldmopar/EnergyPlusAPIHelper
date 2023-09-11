import sys
from pathlib import Path
from typing import Optional


def get_eplus_path_from_argv1() -> Optional[Path]:
    """If there is one argv, get the installation from it, otherwise leave it be inferred."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    return None
