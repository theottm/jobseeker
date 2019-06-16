from pathlib import Path
import os
from os.path import dirname

def get_project_root() -> str:
    """Returns project root folder."""
    return os.path.abspath(dirname(dirname(dirname(__file__))))
