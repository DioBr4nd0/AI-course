import os

WORKSPACE_DIR = "workspace"

def _get_safe_path(filename: str) -> str:
    """ Enforces sandbox security"""
    if not os.path.exists(WORKSPACE_DIR):
        os.makedirs(WORKSPACE_DIR)
    
    safe_name = os.path.basename(filename)
    return os.path.join(WORKSPACE_DIR, safe_name)

def write_file(filename: str, content: str) -> str:
    """Writes content to the sandbox"""
    try:
        path = _get_safe_path(filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"SUCCESS: Written to {filename}"
    except Exception as e:
        return f"ERROR: Failed to write {filename}: {str(e)}"

def read_file(filename: str) -> str:
    """Reads conent from the sandbox"""
    try:
        path = _get_safe_path(filename)
        if not os.path.exists(path):
            return "ERROR: File does not exist."
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERROR: Failed to read{filename}: {str(e)}"

def list_files() -> str:
    """Lists all files in the sandbox"""
    if not os.path.exists(WORKSPACE_DIR):
        return "Workspace is empty"
    files = os.listdir(WORKSPACE_DIR)
    return str(files)
    