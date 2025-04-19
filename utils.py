import os

def get_base_name(filepath):
    """Returns the filename without the extension."""
    return os.path.splitext(os.path.basename(filepath))[0]

# You can add more utility functions here as needed