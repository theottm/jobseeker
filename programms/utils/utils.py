from pathlib import Path
import os

def get_project_root() -> str:
    """Returns project root folder."""
    return os.path.abspath(Path(__file__).parent.parent.parent)
