import os
from src.state import AgentState
from src.tools.shell_ops import execute_shell_command

def reviewer_node(state: AgentState):
    current_file = state["current_file"]
    print(f"\n--- [REVIEWER] Inspecting: {current_file} ---")
    
    # --- CASE 1: Dependency Management ---
    if "requirements.txt" in current_file:
        print("--- [REVIEWER] 📦 Detected Dependency File. Installing... ---")
        # We assume the file is in 'workspace/' so we point pip there
        command = "pip install -r requirements.txt"
        result = execute_shell_command(command)
        
        if "COMMAND SUCCESS" in result:
            print("--- [REVIEWER] ✅ Dependencies Installed Successfully ---")
            return {"error_context": None, "revision_count": 0}
        else:
            print("--- [REVIEWER] ❌ Dependency Installation Failed ---")
            # Return the pip error so the Engineer can fix the package name
            error_msg = result.split("STDERR:")[-1].strip()
            return {
                "error_context": f"PIP INSTALL ERROR: {error_msg}",
                "revision_count": state.get("revision_count", 0) + 1
            }

    # --- CASE 2: Python Syntax Check ---
    elif current_file.endswith(".py"):
        # run py_compile
        command = f"python -m py_compile {current_file}"
        result = execute_shell_command(command)
        
        if "COMMAND SUCCESS" in result:
            print(f"--- [REVIEWER] ✅ Syntax Pass: {current_file} ---")
            return {"error_context": None, "revision_count": 0}
        else:
            print(f"--- [REVIEWER] ❌ Syntax Fail: {current_file} ---")
            error_msg = result.split("STDERR:")[-1].strip()
            return {
                "error_context": error_msg,
                "revision_count": state.get("revision_count", 0) + 1
            }

    # --- CASE 3: Unknown File Type ---
    else:
        print(f"--- [REVIEWER] ⚠️ Skipping check for unknown file type: {current_file} ---")
        return {"error_context": None}