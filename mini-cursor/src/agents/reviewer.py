import os
import re
from src.state import AgentState
from src.tools.shell_ops import execute_shell_command
from src.tools.file_ops import write_file, read_file

def _extract_package_names(text: str) -> list:
    lines = text.strip().split('\n')
    packages = []
    for line in lines:
        line = line.strip().strip('-').strip()
        line = re.sub(r'^(pip install|requirements:?\s*)', '', line, flags=re.IGNORECASE)
        line = re.sub(r'[>=<~!].*$', '', line)
        line = line.strip()
        if line and re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', line):
            packages.append(line)
    return packages

def reviewer_node(state: AgentState):
    current_file = state["current_file"]
    print(f"\n--- [REVIEWER] Inspecting: {current_file} ---")
    
    if "requirements.txt" in current_file:
        content = read_file(current_file)
        packages = _extract_package_names(content)
        
        if not packages:
            print("--- [REVIEWER] ⚠️ No valid packages found ---")
            return {"error_context": None, "retry_count": 0}
        
        print(f"--- [REVIEWER] 📦 Creating venv and installing: {packages} ---")
        
        execute_shell_command("python3 -m venv .venv")
        
        working_packages = []
        for pkg in packages:
            result = execute_shell_command(f".venv/bin/pip install {pkg}")
            if "COMMAND SUCCESS" in result or "already satisfied" in result.lower():
                working_packages.append(pkg)
                print(f"--- [REVIEWER] ✅ {pkg} installed ---")
            else:
                print(f"--- [REVIEWER] ❌ {pkg} failed ---")
        
        if working_packages:
            write_file("requirements.txt", "\n".join(working_packages))
            print(f"--- [REVIEWER] ✅ All installed: {working_packages} ---")
        else:
            write_file("requirements.txt", "")
        
        return {"error_context": None, "retry_count": 0}
    
    elif current_file and current_file.endswith(".py"):
        command = f"python3 -m py_compile {current_file}"
        result = execute_shell_command(command)
        
        if "COMMAND SUCCESS" in result:
            print(f"--- [REVIEWER] ✅ Syntax Pass: {current_file} ---")
            return {"error_context": None, "retry_count": 0}
        else:
            print(f"--- [REVIEWER] ❌ Syntax Fail: {current_file} ---")
            error_msg = result.split("STDERR:")[-1].strip()
            return {
                "error_context": error_msg,
                "retry_count": state.get("retry_count", 0) + 1
            }
    
    else:
        print(f"--- [REVIEWER] ⚠️ Skipping check for: {current_file} ---")
        return {"error_context": None}
