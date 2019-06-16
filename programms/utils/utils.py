from os.path import dirname

def get_project_root():
    """Returns project root folder."""
    return dirname(dirname(dirname(__file__)))
