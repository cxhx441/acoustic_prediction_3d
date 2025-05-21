import os

def resource_path(relative_path: str) -> str:
    """ find resource files no matter where the working directory is."""
    base = os.path.dirname(os.path.abspath(__file__))
    returning = os.path.normpath(os.path.join(base, "..", "resources", relative_path))
    return os.path.normpath(os.path.join(base, "..", "resources", relative_path))

def bed_image_path(relative_path: str) -> str:
    """ find bed_image no matter where the working directory is."""
    base = os.path.dirname(os.path.abspath(__file__))
    returning = os.path.normpath(os.path.join(base, "..", "project_data", relative_path))
    return os.path.normpath(os.path.join(base, "..", "project_data", relative_path))
