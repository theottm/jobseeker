from pathlib import Path

def get_project_root() -> str:
    """Returns project root folder."""
    return str(Path(__file__).parent.parent.parent) + "/"
